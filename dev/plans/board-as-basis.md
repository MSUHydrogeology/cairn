# Plan: the board as the basis for richer views -- a data output, and a guide to building on it

**Source proposal**: `dev/proposals/archive/2026-10-18-claude-board-as-basis.md`
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Assurance path**: high-assurance -- inherited from the proposal: `tools/board.py` is run by every adopter and its output becomes a published contract
**Opened**: 2026-10-18
**Waiting on Maintainer**: read the generated board page
**In brief**: `python tools/board.py --json` prints every proposal and plan as plain data, plus the roadmap rows that wait on you; a guide in Cairn's docs shows how to turn that into a page that is regenerated, never hand-kept; the proposal and plan templates ask for a one-sentence summary; Cairn ships no page.

## In brief

The **board** is the table `python tools/board.py` prints: one row for every open proposal and plan. For two days you have used a shared web page that shows the same facts. It is far easier to read, and it went stale several times a day because someone copies the facts into it by hand. This plan lets that page be rebuilt from Cairn's own files whenever you like, without Cairn shipping a page of its own.

1. **The board gets a data form.** `python tools/board.py --json` prints the board as *JSON*, a plain-text layout that programs read, so a script can build a page without scraping a table made for human eyes. For each proposal and plan it gives what the author wrote in the header lines (status, review tiers, opened date, source proposal, a `Waiting on Maintainer` line, a one-sentence `In brief` line), the title, and where the file sits. It also lists the rows of `dev/PLANNING.md` that say they wait on you. The board works nothing out: it still judges nothing, and "whose move is it" is not in the data.
2. **A guide shows how to build the page.** `docs/build-a-board-view.md` names every field, says what Cairn promises will not change, and gives a short script (standard library only) that writes a web page grouped by who acts next, with counts, the raw status beside each row, and the commit it was built from. It carries three small recipes: **what waits on you** (the list you asked for, which agrees with `python tools/board.py --maintainer`), plans finished by date, and which agent is working on what (a hint only). The guide is read in Cairn's published docs, `board.py --help` points to it, and it is not copied into projects.
3. **Authors are asked for the summary line.** The four proposal and plan templates gain a prompt for `**In brief**: <one plain sentence>`. A page shows that sentence in place of the title.
4. **A safety rule.** The board stops following a *symbolic link* (a file or folder that is really somewhere else, including one that is broken or points at itself) when it reads proposals, plans and `dev/PLANNING.md`. It names what it skipped in the terminal, in the data and at the foot of the page, so a skipped folder never looks like an empty board. Today it follows such links; I checked. A link a contributor commits could make the board print a header line from a file outside `dev/`.

Cairn ships no page, no `--html` flag and no view script. The example lives in the guide, where a test runs it so it cannot rot.

**Two fields and one figure beyond the proposal's tables.** The data carries two fields you did not see in the proposal: `roadmap_read`, which says whether the roadmap file was read, and `skipped_symlinks`, which lists links the board skipped. The page footer also reports how many live items carry a summary line, and says plainly when the board skipped something and the page is therefore incomplete. Each key only adds, and none can be removed later without a new version (`cairn-board/2`). They are the visible report of what the board could not read, and plan review kept them.

**What it costs the Maintainer.** No engine change, so no hand re-anchor of the engine's fingerprint (the AST baseline), and **no existing frozen file changes** (a *frozen file* is one whose exact bytes the gate manifest records). Two new files, a test and a fixture, match the manifest's frozen patterns and freeze at the next *re-anchor* (the supervised ceremony only you run). They join the row already queued on `dev/PLANNING.md`, which this plan's opening commit updates. One short reading by you once the guide and its example are written (chunk M, right after C4): open a generated page and say whether it tells you what needs you and what is in flight. Nothing is pushed.

**How we will know it worked.**

* You open the page the guide's script builds from this tree and can say what needs you and what is in flight without opening an artifact. That reading is the proposal's success criterion and is chunk M.
* The guide's "what waits on you" recipe returns exactly what `python tools/board.py --maintainer` lists, over every shape of header, status, blank line and roadmap row the tests build.
* A committed baseline of the data's keys and types fails a test if any key is renamed, retyped or dropped.
* The terminal board and `--maintainer` print byte for byte what they print today on a tree with no symbolic links.

**Terms.** A *header line* is a `**Field**: value` line above a file's first `##` heading; the board reads these and the title line. A *twin* is a byte-identical copy (`tools/board.py` and `templates/skills/_lib/board.py`). *Boundary A, B and C* are the three verification jobs in `AGENTS.md`: scoped checks while building, one full run on a clean commit, and the code reviewer's independent attempt to break it. A *view* is any page, table or panel built from the board's data.

## Source proposal

Accepted 2026-10-18 at `beb80330`. Revision 1 binds, with the changes the Maintainer made at the Decision (quoted from the Decision block, in the Maintainer's own words where the scribe recorded them):

* **"What waits on the Maintainer" is a recipe in the guide, not a deferral.** "For the board proposal, I'd put the what waits on my in the recipe, actually instead of deferring it."
* **Roadmap rows that declare a wait go into the `/1` data now** ("Yes, now"), so the recipe can list them.
* **The `**In brief**:` prompt goes into the proposal and plan templates now** ("Yes, add it now").
* **The fence warning stays in the terminal `--maintainer` view only** ("Terminal view only"). It is not in the data and not a recipe.
* **The guide is read in Cairn's published docs**, cited by `board.py --help`, and not copied into installs.
* **The "who acts next" lookup lives in the guide**, tested against `doctrine/lifecycle.md`.
* **The Scope delta is allowed as revised** (see *Scope delta*).
* **Review record.** The pass labelled External at `fe0d093c` is read as the usual review, per the review-stance Decision's migration answer. The Maintainer did not call for an External read.

The authorization, quoted verbatim in the Decision: "accept both as descried" ("both" names this proposal and the review-stance proposal).

**Built on landed work.** The maintainer-attention plan (archived at `9832c411`) added `python tools/board.py --maintainer` and the `Waiting on Maintainer` line in `72254d0e`. This plan extends that code, so the first chunk starts only from a tree holding that commit (`git merge-base --is-ancestor 72254d0e HEAD`; true at `72434d73`).

## Scope

Measured at `72434d73`, the HEAD when this plan was written. The plan executes the accepted text; it does not re-argue it. The names of functions are used below instead of line numbers, because three earlier plans edit neighbouring files.

### The contract this plan builds

Revision 1 and the Decision's changes are spread over several layers. This is the one table the implementer builds from; the plan decisions that fix its remaining details follow.

| Top-level key | Type | Holds |
|---|---|---|
| `schema` | string | `"cairn-board/1"`; present even when nothing is found |
| `includes_archive` | boolean | whether `--archive` was given, so no archived rows is not read as none exist |
| `artifacts` | array of records | every proposal and plan |
| `roadmap_waits` | array of roadmap records | `dev/PLANNING.md` rows that declare a wait |
| `roadmap_read` | boolean | whether `dev/PLANNING.md` was read, so an empty list is not read as nothing waits |
| `skipped_symlinks` | array of strings | repo-relative paths not read because they are, or sit under, a symbolic link (a broken or self-pointing link included) |

| Record key (`artifacts`) | Type | Source |
|---|---|---|
| `kind` | string, `"proposal"` or `"plan"` | the directory |
| `id` | string | the file name without `.md`; unique among live records only, so a consumer keys on `path` |
| `path` | string | repo-relative, `/` separators |
| `archived` | boolean | the file sits under `archive/` |
| `title` | string or null | the first `# ` line above the first `##` heading |
| `in_brief` | string or null | the `**In brief**:` header line |
| `status`, `review`, `plan_review`, `opened`, `source_proposal` | string or null | the `**Status**:`, `**Review**:`, `**Plan review**:`, `**Opened**:`, `**Source proposal**:` header lines, as written |
| `waiting_on_maintainer` | string or null | the `**Waiting on Maintainer**:` header line |

| Record key (`roadmap_waits`) | Type | Source |
|---|---|---|
| `line` | integer | the 1-based line of `dev/PLANNING.md`, numbered as Python's `str.splitlines()` numbers it (a form feed or U+2028 counts as a break; an editor or `grep -n` may number differently, D14) |
| `text` | string | what follows the marker on that row |

No value is derived. There is no `status_holder`, no `maintainer_waits` and no key about fences: the first two became guide recipes and the third stays in the terminal view (see *Scope delta*).

### Touched

| Surface | Files | Chunk |
|---|---|---|
| The board tool | `tools/board.py`; twin `templates/skills/_lib/board.py` | C1, C2 |
| Its record in Cairn's own install | `dev/.cairn/cairn-lock.yml`, a scoped finalize of one record (`tools/board.py`) | C1, C2 |
| The contract's tests and baseline | `bootstrap/tests/test_board_json_contract.py` (new), `bootstrap/tests/fixtures/board_json_v1_baseline.json` (new) | C1-C5 |
| The guide | `docs/build-a-board-view.md` (new) | C3, C4 |
| The board's entry in the tools page | `docs/tool-usage.md` | C3 |
| The summary-line prompt | `dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md`, `dev/plans/_template.md`, `templates/core/dev/plans/_template.md` | C5 |
| Board and changelog | `dev/PLANNING.md` (the opening commit joins the re-anchor row), `CHANGELOG.md` (the archive commit) | opening, archive |

The four templates are the whole set of proposal and plan templates, listed from the tree with `git ls-files | grep -E '(proposals|plans)/_template.md$'`. `dev/proposals/_template.md` and `dev/plans/_template.md` are Cairn's own customized copies, not twins of the `templates/core/` files (they differ), so each is edited on its own.

**Not touched**, each checked by `git diff --stat` over the implementation range (C6):

* `bootstrap/_scaffold/` and `bootstrap/scaffold.py` (so **no AST impact**).
* `doctrine/` and `AGENTS.md` (no doctrine change, so the rate-limit gate in `doctrine/rationale.md` is not engaged), including `doctrine/session-routines.md` and the session-start skill pair, which describe the plain board. The plain board does not change, so their sentences stay true; *Found while planning* lists them.
* `tools/session.py`. The terminal modes load its `encode_display`; `--json` loads no other file.
* `bootstrap/UPGRADE.md`: the guide points to it and does not edit it.
* `bootstrap/tests/test_replacement_tools.py`: frozen, holds the existing board tests, and runs unedited. The new tests live in the new file so no existing frozen byte changes.
* `bootstrap/tests/fixtures/gate_manifest.json` and `bootstrap/tests/fixtures/scaffold_ast_baseline.json`.

### Frozen files and the AST baseline

**Frozen files changed: none.** Measured: `frozen_files` in `bootstrap/tests/fixtures/gate_manifest.json` has 183 keys, and `_frozen_files()` in `bootstrap/tests/_gate_manifest.py` globs `bootstrap/*.py`, `bootstrap/tests/**/*.py`, `bootstrap/tests/fixtures/**/*`, `scripts/*.py` and `templates/modules/**/*.py`. Every file in *Touched* that exists today was tested against both the committed keys and the live glob, and none is in either. The instrument was checked against a known key: `bootstrap/tests/test_replacement_tools.py` is in both. `tools/board.py`, its twin (`templates/skills/`) and the four templates (`templates/core/` and `dev/`) are outside every pattern.

**Two new files will freeze.** `bootstrap/tests/test_board_json_contract.py` and `bootstrap/tests/fixtures/board_json_v1_baseline.json` match the live glob. Until the Maintainer's next re-anchor the verifier reports each as `FROZEN-NEW`, which is allowed; at the ceremony they become frozen. Three consequences:

* The pinned collection grows by the new test file's nodes. Their IDs are listed in the *Implementation verification* record at archive, as the earlier plans did.
* **Both files must be final before the ceremony.** An edit to either after it owes a second re-anchor. The archive commit says so on the board row.
* This is a gain as well as a cost. Once frozen, editing the baseline fixture to match a changed output is a `FROZEN-MODIFIED` hold at the ceremony, not a quiet edit. That closes, for the future, the hole the proposal's S5 admits (editing the baseline and the code together).

The opening commit adds a paragraph to the queued re-anchor row on `dev/PLANNING.md`, marked as planned and not yet changed, with the Decision's words quoted. **The re-anchor is the Maintainer's alone** (`bootstrap/REANCHOR_RUNBOOK.md`); an implementing agent must not perform it.

**AST: no change.** No file under `bootstrap/_scaffold/` and not `bootstrap/scaffold.py` is edited. The baseline is already not clean, for other work: at `72434d73`, `python bootstrap/tests/_ast_attest.py verify bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/_scaffold/*.py --known-new bootstrap/tests/fixtures/scaffold_ast_known_new.json` reports 4 CHANGED symbols (`_cmd_adopt_module` and `cmd_upgrade` in `upgrade.py`, `main` in `cli.py`, `seed_gitignore` in `install.py`), and `test_ast_attest.py` fails 2 of 30 nodes for that reason. The neutrality plan measured two symbols earlier today, so the figure is derived again at the tested commit's parent and at the tested commit, and the two must be equal (C6). The AST re-anchor is Maintainer-only and not this plan's.

### Lockfile and the install contract

* `tools/board.py` is a **verbatim** record (source `skills/_lib/board.py`) whose hash matches today (both copies hash to `67f705c6...`). Editing it makes the record stale, so C1 and C2 each reconcile it with a scoped `python bootstrap/scaffold.py upgrade --target . --finalize tools/board.py` in the same commit (precedent `2ea3f869`). Any later edit, such as a code-review fix, owes the same finalize in its own commit.
* `dev/plans/_template.md` and `dev/proposals/_template.md` are two of the 18 files `python bootstrap/verify_integrity.py --target .` reports as modified at `72434d73`. C5 edits both and **does not finalize them**: that would re-attest earlier, unreviewed drift. The count stays at the parent's. The two `templates/core/` copies are sources, not records.
* The lockfile schema is untouched.
* **Install contract: unchanged.** `python bootstrap/scaffold.py --manifest` lists destination, source and mode, never content, so changed bytes do not change it. The guide is under `docs/` and is not installed. C2 and C6 diff the manifest before and after; the diff is empty.

### Found while planning

* **The board follows symbolic links today.** In a scratch tree, with a plan linked from outside `dev/`, `dev/proposals` linked to a folder elsewhere, and `dev/PLANNING.md` linked to a file elsewhere, `python tools/board.py` listed the linked plan and the folder's proposal, and `--maintainer` listed the linked file's row. All three supply text from outside `dev/`. C1 reproduces this tree as its red-before-the-code case.
* **Broken, looping and non-regular entries are read as absence, or crash, today.** Measured by the Internal Security Review at `10ae6428`: a folder linked to itself gives "0 row(s)" with no mention; a dangling `dev/plans` link makes every plan silently absent; a dangling `dev/PLANNING.md` is called "missing"; a leaf linked to itself, and a folder named `x.md`, make the whole board fail with a traceback (exit 1); a named pipe called `x.md` makes it hang; `dev` linked, and `dev/plans/archive` linked under `--archive`, are read. Each is a case C1 builds.
* **The header reader is already one function for all three modes.** `_header_fields` feeds the plain board, `--maintainer` and the advisory. `--json` must call it too, so a header difference cannot hide between the data and the recipe (C2).
* **A naive code pattern misfires on this tool.** `compile\(` matches the three `re.compile(` lines in `tools/board.py`, so K3 leaves out a leading `re.`; the dynamic-load words match exactly two lines today, both in `_encode`.
* **`line` is Python's count.** The board numbers roadmap lines with `str.splitlines()`, which also breaks on a form feed and U+2028; `grep -n` does not (measured: `--maintainer` says line 6 where `grep -n` says line 4). D14 settles it.
* **A blank Waiting line counts as declared.** `--maintainer` lists a `**Waiting on Maintainer**:` line with nothing after it, so a blanked line stays visible. Revision 1's "absent is null, never an empty string" would collapse that case into "no line" and make the recipe drop it. D2 settles it.
* **The board arrived after 0.3.0.** `git ls-tree v0.3.0` has no `tools/board.py`; it was added on 2026-08-26 (`c54ddfd2`). Revision 1's guide sentence ("`--json` was added after Cairn 0.3.0") is true but incomplete: an install can lack the board entirely, or have a board that refuses `--json` (exit 2, "unrecognized arguments"). The guide says both (C3).
* **`awaiting-decision` is matched by a pattern, not a first word.** `--maintainer` lists a status when it starts with `awaiting-decision` not followed by a letter, digit or underscore, so `awaiting-decision -- note` lists. The recipe must use that same rule or the two drift (D9).
* **Starting figure for the summary-line signal.** At `72434d73`, 2 of 6 live artifacts and 2 of 137 in all carry an `**In brief**:` header line (the two proposals written after the line was introduced). The guide's page footer reports the live share, so the signal can be read where the Maintainer already looks.
* **The recipe for finished plans works on this tree.** `git log --diff-filter=A --name-status -- dev/plans/archive` printed 54 `A` rows for 54 archived plan files at `72434d73` (a rename inside the pathspec reads as an add). It covers plans only; a proposal archives at plan-open or at a Decision, a different event.
* **Another plan's tests read `--maintainer`.** `model-mapping-install-path` renders an install and runs `board.py --maintainer --root <tmp>` to see its seeded `Waiting on Maintainer` row listed. This plan keeps that output byte for byte, which C1 pins, so the two plans do not constrain each other's order.
* **Neutrality reads zero.** `python scripts/quality_gate.py --sub neutrality` printed `fail=0  info=56` at `72434d73`, with no hit in any file this plan edits. The criterion is "stays zero".
* **The advisory will name this plan.** The `M` row below says "MAINTAINER-ONLY", and `--maintainer`'s advisory line names every plan that says a fence word and declares no wait. That is by design and the same for the other open plans; chunk M writes the real line when it is reached.
* **Prose that describes the plain board stays true.** The sentences in `doctrine/session-routines.md` and the session-start skill (and its twin) say the board prints one row per proposal and plan with the header fields its author wrote, and that it judges nothing. The plain board does not change, so none of them is edited here.

### Plan decisions the proposal left open

The proposal fixes the contract's outline, not its remaining shape. These are choices this plan makes; plan review may overrule any of them, and D2, D4 and D7 are the ones I would look at first.

* **D1 The roadmap data.** `roadmap_waits` and `roadmap_read` are as in the contract table above. `line` is where the row sits in the file, not a derived value. A row's `text` is always a string (blank is the empty string) because the row exists. `roadmap_read` is false when `dev/PLANNING.md` is missing or is a symbolic link.
* **D2 Absent versus blank.** For every header-derived key, `null` means the line is not in the header block, and the empty string means the line is there with nothing after the colon. Reason: `--maintainer` lists a blanked Waiting line as declared, and the success test requires the recipe to match it. Collapsing blank into `null` would drop it silently. I read Revision 1's "absent is `null`, never an empty string" as being about absent lines. A view that writes `in_brief or title` is unaffected. If plan review overrules this, a blank wait must be carried some other way, and that is a change to the contract table.
* **D3 Files with no header.** The terminal board omits a proposal or plan that has no header lines. `--json` lists it with every header-derived key `null` (the title is still read), because a silent omission is the failure the other lists guard against, and a view can then show "status unknown".
* **D4 The link rule: its reach, its test and its report.** Revision 1 says "a symlinked artifact is skipped". The Internal Security Review measured that a linked folder, a linked `dev`, a linked `archive` and a linked `dev/PLANNING.md` supply outside text in the same way, and the Decision put the roadmap lines into the data. So the rule is: every path component strictly below the resolved root, from `dev` down to the leaf, and `dev/PLANNING.md`, is examined with `is_symlink()` (an `lstat`) **before any call that follows links** (`is_dir`, `is_file`, `exists`, `glob`, `read_text`). A link is skipped whether it is broken, points at itself or points at a file inside `dev/`: the rule is "is a link", not "points outside". The root is resolved first, so a link at or above the root (a home folder on a linked volume, or `--root` given as a link) is outside the rule and reads normally; a check that also tested folders above the root would empty the board for such an adopter. Every skip is reported: a `board: skipped (symbolic link, not read): <path>` line in the terminal modes, `skipped_symlinks` in the data, and a line at the foot of the page and in the recipe's result. A skip nobody can see reads as an empty board. Trees with no links print exactly what they print today.
* **D5 One reader for roadmap rows, one for header lines.** `--maintainer` and `--json` call one function for the roadmap rows, so the two cannot disagree about which rows wait (the proposal's own sentence for the dropped `maintainer_waits` list, kept for the data that remains). The plain board, `--maintainer` and `--json` also read header lines through the one existing `_header_fields`, and `--json` builds no second reader. C2 moves the roadmap reader out of `_waiting`, and the golden test (C1) pins `--maintainer` before and after.
* **D6 Failure path.** `--json` builds the whole document in memory and writes it once. A source that cannot be read is a failure, and so is an entry that is neither a link nor what it should be: an artifact leaf that is not a regular file (a folder named `x.md`, a named pipe, a device) or an entry in the artifact path that is not a folder. The same `lstat` that finds a link refuses these before any open, so a pipe cannot hang the board. A failure prints one line on standard error naming the path through `ascii()`, writes nothing to standard output and returns 1; the terminal modes print the same line and return 1 where today they print a traceback or hang. `dev/PLANNING.md` keeps today's reading once it is known not to be a link: a non-regular file reads as not read ("missing"), as `is_file()` says, and the golden test pins it. `--json` with `--maintainer` is a usage error (exit 2). The JSON path loads no other file; the terminal encoder in `tools/session.py` serves the terminal modes only, and a one-line comment beside `ascii()` says so, so that a later reader does not "fix" it to use the encoder.
* **D7 What the example does beyond `html.escape`.** It shows control and format characters (Unicode categories beginning with C) as visible `U+XXXX`, because `html.escape` leaves a right-to-left override in place, which is the class the proposal's S5 names. It cuts a long label to a fixed length on one line. The guide states that invisible filler characters outside category C (U+3164, U+115F, U+034F, U+FE0F, U+E0100) are shown raw: copying the terminal encoder's range table into the example would make a second table to keep in step. Its footer lists skipped paths and says the page is incomplete when there are any, and says "n of m live rows carry an In brief line", the numeric signal for the summary prompt. The share figure is the first thing to drop if the example grows past its cap.
* **D8 The stamp.** The page is stamped with `git rev-parse HEAD`. It reads the working tree, so an uncommitted header edit shows under that stamp. The guide says so and the example adds no dirty check, because a third subprocess is not accepted scope.
* **D9 The Maintainer group uses the board's own rule.** The recipe and the example test a status with the same pattern `--maintainer` uses, and a non-null `waiting_on_maintainer` counts as declared. Revision 1's "first word of the status, matched exactly" is kept for the lookup of the other holders, where it is a word match against a table. The first word is the leading run of lowercase letters and hyphens.
* **D10 Output form.** `json.dumps` with `sort_keys=True`, `ensure_ascii=True`, `indent=2` and a trailing newline. `artifacts` is ordered by `path` so the bytes are stable. Consumers are told not to rely on order, as Revision 1 says, and that `path` is the unique key: `(kind, id)` is unique among live records only, because a live and an archived file can share a name. That corrects a statement of fact in Revision 1's fifth promise and removes no outcome.
* **D11 How the lookup test reads the doctrine.** `doctrine/lifecycle.md` draws two diagrams with nodes written `ID["word<br/>(holder text)"]`. The test reads those labels and maps the holder text to a role by the first of Maintainer, author, reviewer, implementer that the text contains, in that order. The order matters: "a code reviewer, never the implementer" contains both the last two words, and the node means reviewer. A node with no holder text maps to "none named".
* **D12 The older-board sentence is broadened** (see *Found while planning*).
* **D13 Where chunk M sits.** After C4, because the page needs only the finished board, guide and example (C1 to C4). The `In brief` prompt (C5) changes what authors write later, not the page, which falls back to the title. M does not hold C5 or C6; code review can proceed while it is open. Archive waits on it.
* **D14 Roadmap line numbers.** `line` is the number Python's `str.splitlines()` gives, which `--maintainer` already prints, so the two agree and the terminal output does not change. The cost is that a form feed or U+2028 ahead of a row makes the number differ from an editor's or `grep -n`'s. The guide's field table says so and a node pins the case. The alternative (count `\n` lines) would change `--maintainer`'s number on trees holding those characters, and the accepted text says the terminal board does not change.
* **D15 Hardening not adopted.** Opening a leaf with `O_NOFOLLOW` and `O_NONBLOCK` and checking `fstat` would close the leaf half of the check-then-read race. It adds a second reader to a verbatim installed tool for a race the plan records as out of scope: the threat is a committed link, which exists before any check, and the `lstat` check already refuses links and non-regular files before any open.

**Plan review has run.** Both reviews (the Internal Security Review and the Internal pass) are answered in *Response to plan review*, which points at the cell each answer changed.

### Documentation / doctrine surface

| Layer | Files |
|---|---|
| Governing | none |
| Doctrine | none; no `doctrine/` or `AGENTS.md` change, so the rate-limit gate is not engaged |
| Descriptive | `docs/build-a-board-view.md` (new; routed to `docs/` because it describes current behaviour and how to extend it, per `docs/DOCUMENTATION_PLAN.md`); `docs/tool-usage.md` (the board's entry) |
| Authoring templates | the four templates (C5) |
| Deliberation | this plan; `dev/PLANNING.md` (the re-anchor row); `CHANGELOG.md` (the archive commit) |

## Sequence

The rows are in run order. All commits go to `master`; nothing is pushed. Implementation is sequential after the plans ahead (see *Sequencing*), and every chunk starts with the start guard (K0).

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **The shared reader refuses links, and says so.** `tools/board.py` and its twin read no symbolic-linked entry on the path from `dev` to an artifact, and not `dev/PLANNING.md` if it is one, in the plain board and in `--maintainer`, and print one footer line naming what was skipped; an entry that is neither a link nor a regular file or folder fails loudly instead of crashing or hanging. A golden test pins the terminal board and `--maintainer` first, on trees that hold the shapes the rule and C2 will move. The new test file is created here. Scoped finalize of `tools/board.py`. | `ready-to-implement`; `72254d0e` is an ancestor; `review-stance-and-lenses` has reached `awaiting-code-review` or later; K0 | one commit |
| C2 | **The data form.** `--json` prints the document in the contract table: the artifact records, `roadmap_waits` and `roadmap_read` from one shared reader, `skipped_symlinks`. The baseline fixture is created. `--help` cites the guide. The module docstring and help text stop saying "header blocks and nothing else". Twin byte-identical; scoped finalize. | C1; K0 | one commit |
| C3 | **The guide's contract half.** `docs/build-a-board-view.md` opens in plain words, then gives the three field tables, what will not change, the lookup table with its precedence rule, what the data can and cannot show, and how to reach and run it. `docs/tool-usage.md` gains `--json`, a link and a true description. Tests: the guide and the output agree; the lookup matches the lifecycle; the help citation resolves; the guide is not installed. | C2; K0 | one commit |
| C4 | **The guide's example and recipes.** The tagged worked example (a page grouped by who acts next, holding the "what waits on the Maintainer" function), the finished-plans and intent-join recipes, the section on keeping a page honest, and the note on handing the guide to an AI agent. Tests run every tagged block. | C3; K0 | one commit |
| M | **MAINTAINER-ONLY: read the page.** After C4 the agent runs the guide's example on the live tree, saves the page outside the repo, and gives the Maintainer its path with one question (see below). Archive waits on the answer; C5, C6 and code review do not. | C4 | the Maintainer |
| C5 | **The summary-line prompt.** The four templates gain a short paragraph above the rule and one header line below it. A test shows the board reads the line from each. Re-read the four files at edit time. | C2; K0, which here means none of the four templates is modified in the working tree and none is under a live claim | one commit |
| C6 | **Boundary B, then the record.** One full run on one clean commit; the result is written down; Status moves to `awaiting-code-review`. | C1-C5 | one commit |

**Run order and commits.**

* **C1 before C2.** The shared reader is hardened before new output is built on it, so the data form never exists in a version that follows links.
* **C5 follows M in the table but does not wait for the answer.** It starts when the start guard passes; it re-reads the four files and adds lines beside the other plans' cells.
* **Implementation is sequential after the plans ahead.** C1 starts once `review-stance-and-lenses` has reached `awaiting-code-review` or later. Interleaved commits would make each plan's Boundary B range and code-review range ambiguous. The plan that follows this one applies the same rule to this plan.
* **M and the Waiting line.** When work reaches M, write `**Waiting on Maintainer**: read the generated board page` in this plan's header block (29 characters, under the board's 48) and delete it when the Maintainer answers. The question is one sentence: "From this page alone, can you say what needs you and what is in flight? If not, what is missing?" The answer is recorded verbatim in *Implementation verification*. A request that fits the accepted guide and example (grouping, wording, ordering) is an ordinary edit to C4. A request for a new field is a new key in `/1`, which adds without a version change but is new scope, so it goes back to the Maintainer as a deviation request. If the answer changes tested bytes, the checks of the chunk that owns them repeat, and C6 repeats if it has run; that is the accepted cost of not holding Boundary B for a reading that may need nothing.
* **The re-anchor is not a chunk.** It is declared on the marked board row (the opening commit joins it), so this plan carries no second Waiting line for it. The agent's part is the board note at archive.

### Sequencing with the other plans

**The build order is the Maintainer's, set on 2026-10-18:** `neutrality-and-upgrade-slots`, `independent-scientific-check`, `review-stance-and-lenses`, **this plan**, `model-mapping-install-path`, then `stewardship-and-reuse`. It is his order, not one derived from the other plans' own texts, which differ about it; those texts are being corrected. Plan statuses are read at each chunk's start (`python tools/board.py`), not carried here. Chunks C1 to C4 touch none of the earlier plans' files except disjoint lockfile records and one paragraph of `docs/tool-usage.md`, and C5 re-reads the four templates at edit time. On 2026-10-19 the Maintainer placed both `board-as-basis` and `model-mapping-install-path` into the 0.4 release train (`dev/PLANNING.md`), so the two `FROZEN-NEW` files join the single combined Maintainer-run AST and gate-manifest ceremony at the 0.4 cut.

Files shared with the other plans, each read from that plan's own text:

| File | The other work | This plan | What to know |
|---|---|---|---|
| The four templates | `independent-scientific-check`: a new block after the security preflight and a paragraph in *Acceptance criteria*. `review-stance-and-lenses` (its C2): the Review preamble, the `**Review**:` and `**Tier**:` lines, the plan-review and code-review skeletons. `stewardship-and-reuse` (accepted, plan not open, after this plan): *Scope*, *Dispositions* and the deviation sentence | C5 adds a paragraph above the rule and one line after `**Opened**:` | different regions; the `**Review**:` line in the proposal templates sits two lines above mine, so a textual rebase. The first plan's new test reads its block and paragraph only; mine reads only the `**In brief**:` line. Neither pins the header |
| `docs/tool-usage.md`, the board entry | `review-stance-and-lenses` (its C6) changes "review tier" in the same paragraph | C3 corrects the description and adds `--json` and a link | same paragraph, two phrases; this plan runs later and re-reads |
| `doctrine/lifecycle.md` | `review-stance-and-lenses` (its C4) edits sentences about review | C3's lookup test reads the two diagrams' node labels at test time | it asserts the labels it finds, so a reworded label that changes a holder turns the test red, which is the intent. C3 records the labels it read |
| `doctrine/session-routines.md`, session-start skill and twin | `neutrality-and-upgrade-slots` (done) and `review-stance-and-lenses` (its C3, C4) edit phrases in the board paragraph | read, not edited | the paragraph describes the plain board, which does not change |
| `dev/.cairn/cairn-lock.yml` | `neutrality-and-upgrade-slots`: 12 records. `review-stance-and-lenses`: 3. `model-mapping-install-path`: the `scripts/check_model_selection.py` record | the `tools/board.py` record, in C1 and C2 | disjoint records; each commit reads the file fresh and checks the diff before committing (K2) |
| `dev/PLANNING.md`, `CHANGELOG.md` | every plan: the re-anchor row at opening, an entry at archive | the same | commit by path, read fresh, claim first |
| `tools/board.py --maintainer` output and the `dev/PLANNING.md` row grammar | `model-mapping-install-path` (after this plan) seeds a marked row in two presets and its tests read the output | C1 pins the output byte for byte | the plan that follows relies on the output; the pin protects it |
| The neutrality checker | `neutrality-and-upgrade-slots`: stricter after its C1, zero after its C7 | everything this plan ships is held to it | the criterion is "stays zero" |
| `bootstrap/UPGRADE.md`, `bootstrap/tests/test_verify_integrity.py` | `neutrality-and-upgrade-slots` edits both | the guide cites the first; the second is run, not edited | none |

**Against `model-mapping-install-path`.** It follows this plan, as the Maintainer ordered. The two share only housekeeping files (`dev/PLANNING.md`, `CHANGELOG.md`, disjoint lockfile records, the re-anchor row) and the pinned `--maintainer` output. The roadmap rows it seeds appear on the page from the day it lands, with no change here.

## Acceptance criteria

**Reading these criteria.** Each ends with *Red when*: a change that turns it red. Prose checks use `count(file, section, phrase)`, the number of times a fixed phrase occurs in a section, taken on whitespace-collapsed text; a phrase count is taken at the chunk's parent and must be 0 there, then the stated number at the chunk's commit. **Phrase counts are one-shot checks the implementer runs and records, except the ones that pin a promise or a safety sentence**, which a standing node holds: `ignore keys`, `cairn-board/2`, `CHANGELOG.md`, `live records only`, `must not overwrite` and `length` (the promise), and `never an approval record`, `skipped_symlinks`, `not that a Decision` and `whatever commit is checked out` (the safety sentences). Every other wording is review's job, because a standing node pinning prose freezes into a test file only the Maintainer can re-anchor. Every new test node lives in `bootstrap/tests/test_board_json_contract.py`, builds a scratch tree in `tmp_path`, and is shown failing before the code that satisfies it (K6). A test that loads `tools/board.py` reads it from the tree it sits in, so a scratch copy of the tool would never be read: the red and mutation runs use a throwaway `git worktree`. Scratch git repositories pass `-c user.name=... -c user.email=... -c commit.gpgsign=false` and set `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL` to the null device, as `test_portable_security_sweeps.py` does. Boundary C attacks the prose.

### Checks every chunk repeats (K0, K5 and K7 bind C1 to C5; K1 to K4 bind the code chunks C1 and C2; K6 binds every chunk's new test nodes)

Each chunk's commit body records the result of the checks that apply to it.

* **K0 -- the start guard.** Before a chunk edits a file: `git status --short -- <the files the chunk edits>` prints nothing, and `python tools/intent.py list` shows no live claim on them; then the chunk claims them. All agents of a session share one agent id, so `list` cannot say whose a claim is, and the clean status is the check that counts: `git commit <path>` commits a whole file, so another agent's unfinished edit would ride in under this chunk's message. *Red when* either shows a hit.

* **K1 -- twins.** `cmp tools/board.py templates/skills/_lib/board.py` exits 0, and `test_notice_install.py` (which reads both copies and the SPDX header) passes. *Red when* either copy was edited alone.
* **K2 -- the lockfile.** One scoped `python bootstrap/scaffold.py upgrade --target . --finalize tools/board.py` runs in the same commit. `git diff -U0 dev/.cairn/cairn-lock.yml` shows a change to the `"hash"` line of that one record only, and the new hash equals `git show <commit>:tools/board.py | shasum -a 256`. `python bootstrap/verify_integrity.py --target .` lists the same files as at the chunk's parent (18 at `72434d73`) and not `tools/board.py`. *Red when* a record outside the chunk changes, the hash differs, or the list grows.
* **K3 -- no new subprocess, network or dynamic code in the tool.** Pattern A: `import subprocess|subprocess\.|Popen|os\.system|os\.popen|socket|urllib|http\.client|eval\(|exec\(|__import__`. Pattern B: `exec_module|spec_from_file_location|import_module|runpy|(^|[^.A-Za-z_])compile\(` (the last alternative leaves out `re.compile(`, which the tool uses three times). Controls first: A matches `subprocess` in `tools/session.py`; B matches, in `tools/board.py`, exactly the two lines of `_encode` that load the terminal encoder (`spec_from_file_location` and `exec_module`) and no other; the unqualified `compile\(` would match three more, which shows why the qualifier is there. After the chunk, A prints nothing on `tools/board.py` and B prints exactly those two lines, both inside `_encode`. If a docstring trips either, reword the docstring, not the pattern. *Red when* A matches, or B's lines are not exactly those two.
* **K4 -- the standing gates.** `test_security_lint.py` and `test_security_check.py` pass (the Bandit gate scans `templates/skills/_lib/board.py`) and the finding set for the file is the same as at the parent, or each new finding is dispositioned in the commit body. *Red when* a new finding is unaccounted for.
* **K5 -- neutrality stays zero.** `python scripts/quality_gate.py --sub neutrality` is run at the chunk's parent and at its commit; the `fail=` figure is unchanged (0 at `72434d73`) and no FAIL line names a file the chunk edited. If the baseline is not zero when the chunk starts, FAIL lines are compared by file, token and line text (line numbers move) and none may be new. Control: the same command on a scratch copy of the chunk's main edited file with one denylisted name planted reads one more FAIL. *Red when* a FAIL line is new, or the control does not fire.
* **K6 -- red before the code.** Run the chunk's new nodes at its parent, in a throwaway `git worktree` of the parent with only the new test file (and, for C3-C5, any fixture it needs) copied in. Each fails for the reason the commit body names (the missing behaviour, or for C3-C5 the missing guide or line), not on an import error or a slip in the test. The commit body names the parent SHA and each failure. *Red when* a node passes at the parent, except the golden node of C1, which must pass at the parent (its non-vacuity is a mutation, below).
* **K7 -- prose gates.** For every document the chunk edits or creates, `python scripts/claim_check.py <file>` and `python scripts/check_cairn.py` are clean; for anything under `docs/`, `python scripts/link_check.py` is clean too; for `docs/tool-usage.md`, `python scripts/verify_counts.py docs/tool-usage.md` still reads `1 ok, 0 failed`. *Red when* any reports a finding the parent did not. The commit also drops from this plan's `Proposed paths:` list each path that now resolves, as the template says, and `claim_check.py` on the plan stays clean.

### C1 -- The shared reader refuses links, and says so

Files: `tools/board.py`, `templates/skills/_lib/board.py`, `dev/.cairn/cairn-lock.yml` (one record), `bootstrap/tests/test_board_json_contract.py` (created here). Not frozen. Checks: K0-K7.

* **The rule, stated once (D4).** Every path component strictly below the resolved root, from `dev` down to the leaf, and `dev/PLANNING.md`, is examined with `is_symlink()` before any call that follows links (`is_dir`, `is_file`, `exists`, `glob`, `read_text`). One function does it and gives one of three answers: a link (skipped and named), a regular file or real folder (read), or anything else (a failure, D6). It is called by the artifact reader, which the plain board, `--archive` and `--maintainer` share, and by the `dev/PLANNING.md` read. The root is resolved first and the rule never looks above it. *Red when* a call that follows links precedes the check on any path.
* **The terminal board is pinned before it changes.** `TestTerminalBoardIsUnchanged` compares the output of four modes (the plain board, `--archive`, `--maintainer` and `--maintainer --archive`) with golden text committed in the test, captured by running C1's **parent** `board.py` on the same trees. The node passes at the parent and at C1. The main tree holds every shape the terminal modes handle:
  * headers: every field; leading spaces on header lines; a repeated `**Status**:` line; a `##notaheading` line inside a header block; an artifact with no header lines;
  * files: an archived plan, and an archived plan carrying a Waiting line; `_template.md` and `_notes.md` side by side;
  * statuses: `awaiting-decision`; `awaiting-decision` with a note after it; `awaiting-decision-x` (the board lists it: the lookahead excludes only letters, digits and underscore); and `awaiting-decisions`, `awaiting-decision_x`, `awaiting-decision2` (it does not);
  * Waiting lines: blank; `**Waiting on Maintainer **:` with a space before the closing bold (read: the field name is stripped); the marker in lower case (not read); a 60-character text;
  * fences: a plan that says `MAINTAINER-ONLY`; a plan that says only `MAINTAINER-GATED`; a proposal that says `MAINTAINER-GATED`;
  * roadmap rows: the plain, indented, sub-bullet and dash-bullet forms; the marker in lower case; a tab after the bullet; a double bullet; a mention inside a sentence; and a form feed and U+2028 ahead of a marked row.

  Two more small trees: one with no `dev/PLANNING.md`, one where it is a folder. *Red when* any byte differs on any tree.
* **The golden test can fail, for each of twelve plausible accidents.** Each of these one-line breaks of `tools/board.py`, made in a scratch worktree, is run against the golden node and against the existing `test_replacement_tools.py` and reported killed, survived or equivalent, beside an unmutated control run: (1) the lookahead in `_AWAITING_DECISION_RE` changed so `awaiting-decision-x` stops listing; (2) the lookahead dropped, so `awaiting-decisions` lists; (3) a repeated header field read first-wins; (4) a `##x` line ending the header early; (5) header lines read unstripped; (6) the field name unstripped; (7) the roadmap marker name unstripped; (8) the marker matched without case; (9) `split("\n")` for `splitlines()`; (10) `is_file()` widened to `exists()` on `dev/PLANNING.md`; (11) the 48-character cut moved; (12) the `_` skip narrowed to `_template.md`. A tab or a double bullet before the marker is equivalent (the reader strips after removing the bullet) and is reported so, shown by the behaviour test through the real entry point. The two footer rewordings (the plain-mode footer; the `board: not listed` line) stay as cheap checks. *Red when* a mutant is reported survived without a measured reason.
* **The links trees, red at the parent.** `TestSymlinkedSourcesAreNotRead` builds one tree per case: a plan that is a link to a file outside `dev/`; `dev/proposals` as a link to a folder outside `dev/`; `dev/PLANNING.md` as a link to a file outside; `dev` itself linked; `dev/plans/archive` linked, run with `--archive`; a dangling folder link (`dev/plans`); a folder linked to itself; a dangling `dev/PLANNING.md`; a leaf linked to itself; a link to a file inside `dev/`. At the parent each is read, silently dropped or crashes (the measured results in *Found while planning*), so the node fails there for those reasons. *Red when* the node passes at the parent.
* **After C1 none is read, in all four modes.** No row, no entry and no roadmap row comes from a link; each of the ten is named once, in the skip line, by the highest linked component, and a linked folder skips everything beneath it. A linked or dangling `dev/PLANNING.md`, or one under a linked `dev`, is reported as skipped and `--maintainer` does not also call it "missing"; a truly absent file still says so, unchanged. *Red when* any is read, silently dropped, named twice, or called "missing".
* **The rule does not reach too far.** A root reached through a linked parent folder, and `--root` given as a link, are read normally with no skip line. *Red when* either empties the board. Mutant: also test the folders above the root.
* **The skip is said, and only when it happens.** Each skipped path appears once on a line `board: skipped (symbolic link, not read): <path>` (repo-relative, passed through the shared encoder; a path holding an escape byte prints it escaped). A tree with no links prints no such line, so the golden node holds. *Red when* a skip is silent, is named twice, prints a raw control byte, or a no-link tree gains a line.
* **Entries that are not what they should be fail loudly and never hang (D6).** A folder named `x.md` in `dev/plans`, `dev/plans` itself as a regular file, and a named pipe `x.md` (made with `os.mkfifo` and run in a subprocess under a timeout, so a hang fails the test and not the suite; where `os.mkfifo` is missing the node is skipped with its reason and the Boundary B record disposes of the skip), each make the plain board and `--maintainer` print one line on standard error naming the path (through the encoder) and return 1, instead of a traceback or a hang. `dev/PLANNING.md` as a folder keeps today's reading (not read, "missing"), which the golden tree pins. *Red when* the board hangs, prints a traceback, or reads past the entry. Mutant: read the leaf before the `lstat` check.
* **The board loads only its own encoder.** `TestBoardLoadsOnlyItsOwnEncoder` runs each mode with `--root` on a tree holding a planted `tools/session.py` that writes a marker file when executed; no marker appears (control: loading the planted file directly writes it). Mutant: load the encoder from the root. *Red when* a marker appears.
* **One check, called from every reader.** Mutations, each in a scratch worktree, each of which must turn a named case red: delete the call in the artifact reader; test the leaf, `dev/proposals` and `dev/plans` but not `dev` or `archive`; keep `if not base.is_dir(): continue` ahead of the link check; delete the call in the `dev/PLANNING.md` read. *Red when* any mutant survives.
* **The tool says what it now does.** The module docstring gains one sentence: a symbolic link is never read and is named in the output. No other docstring or help change in this chunk (C2 owns them). *Red when* the sentence is absent.
* **The existing tests still pass unedited.** `bootstrap/tests/test_replacement_tools.py` passes, and `git diff --stat` for C1 does not list it. *Red when* it is listed.

### C2 -- The data form

Files: `tools/board.py`, twin, `dev/.cairn/cairn-lock.yml` (one record), the test file, `bootstrap/tests/fixtures/board_json_v1_baseline.json` (created here). Checks: K0-K7. Boundary A also runs the manifest diff.

* **The document is the contract table, and the baseline can catch a break.** The fixture commits every key with its JSON type: the six top-level keys, the twelve record keys, the two roadmap keys; a nullable key is typed `["string", "null"]`. `TestSchemaOneBaselineHolds` runs the board on a tree with every field written and on a tree with every field absent, and requires each baseline key present with its type in both (subset semantics: a new key passes this node on its own). Booleans are told from integers (`bool` is checked before `int`). *Red when* a key is missing, renamed or retyped. Mutation, scripted over the **set of baseline keys read from the fixture** (not the diff): for each key in turn, delete it from the emitted document in a scratch copy; every one must turn the node red.
* **Emitted keys equal the baseline keys at this commit.** Recorded in the commit body by a script (the guide-listing rule that allows additions lands in C3, when a guide exists to list them). *Red when* the sets differ.
* **Header lines are read by one function (D5).** The plain board, `--maintainer` and `--json` all read header lines through `_header_fields`, and `--json` builds no second reader; absent versus blank comes from looking a name up in the dict that function returns. Mutant: change `_header_fields` alone (a repeated field read first-wins): the plain board, `--maintainer` and `--json` outputs all turn red. *Red when* any of the three stays green.
* **No fact can be forged from inside a file.** `TestRecordFactsComeFromWhereTheFileSits`: one artifact whose header carries `**Kind**: proposal`, `**Id**: forged`, `**Path**: javascript:alert(1)`, `**Archived**: yes`, `**Schema**: cairn-board/2`, `**Title**: forged`, `**Includes archive**: true`, an `**Assurance path**:` line, and two `**Status**:` lines. Required: the record's keys are exactly the twelve; `kind`, `id`, `path` and `archived` come from the location; `title` comes from the `# ` line; the document's `schema` is `cairn-board/1` and `includes_archive` follows the flag; the repeated Status gives the last value, which is what `--maintainer` reads. Mutant: build the record by copying every header field in under a snake_case name. *Red when* any forged value reaches the output.
* **Each value comes from where the table says.** For a scratch artifact written with every header line, a title and a body, `kind`, `id`, `path` (repo-relative, `/`), `archived`, `title`, `in_brief`, `status`, `review`, `plan_review`, `opened`, `source_proposal` and `waiting_on_maintainer` equal what was written, whitespace-trimmed and not escaped. A `**Field**:` line below the first `##` heading, or a `# ` line below it, is not read. The title is the first `# ` line above the first `##` heading. *Red when* a value comes from below the first heading or is altered.
* **Absent is null; a present blank is kept (D2).** A missing line gives `null`; a line with nothing after the colon gives the empty string; `title` and `in_brief` never stand in for each other. A `**Waiting on Maintainer**:` line with no text gives `""`, not `null`. *Red when* an absent line gives `""`, or a blank line gives `null`. Mutations: emit `""` for an absent field; emit `null` for a blank Waiting line (C4's recipe node repeats the second).
* **A file with no header lines is listed (D3).** It appears with every header-derived key `null` and its title read, and the plain board still omits it. *Red when* it is dropped from the data or appears on the plain board.
* **Archives, and the unique key (D10).** Without `--archive`, no record has `archived: true` and `includes_archive` is false; with it, archived records appear with `archived: true` and `includes_archive` is true. A live file and an archived file of the same name give two records with different `path`, none dropped. *Red when* an archived record appears without the flag, the flag does not move, or the two records share a `path`.
* **Roadmap rows come from the same function `--maintainer` uses (D5).** `roadmap_waits` for a tree with the rows used in C1's golden tree equals, in line numbers, the roadmap entries `--maintainer` prints; a mention of the marker in a sentence or in backticks is not a row; a row with no text has `text` `""`; a form feed or U+2028 ahead of a row gives the same `line` in both (Python's count, D14). A missing `dev/PLANNING.md` gives `roadmap_read: false` and `roadmap_waits: []`; a present file with no rows gives `true` and `[]`; a linked file gives `false`, and the path is in `skipped_symlinks`. Mutations: change the row grammar in the shared function only (both the `--maintainer` and `--json` nodes go red); keep a second copy of the grammar in the JSON path (a node that changes the first copy and compares must go red). *Red when* the two disagree on any row, or a missing file reads as an empty list with `roadmap_read` true.
* **`skipped_symlinks`.** On each of C1's ten links trees it lists exactly the paths C1 reports, sorted, and it is `[]` otherwise. *Red when* it differs from the terminal footer's list on any of them.
* **Same files, same bytes (D10).** Two runs on one tree give equal bytes; the same artifacts copied to a second scratch root give equal bytes (no machine path, timestamp or commit id); the output is ASCII; keys are sorted at every level; `schema` is present on a tree with no `dev/` folder, alongside `artifacts: []` and `roadmap_read: false`. A title holding a non-ASCII letter is escaped in the output and equal after `json.loads`. Mutations: unsorted keys; `ensure_ascii=False`. *Red when* any of these differs.
* **A failure writes nothing to standard output (D6).** A non-UTF-8 artifact, a non-UTF-8 `dev/PLANNING.md`, a folder named `x.md` and a named pipe `x.md` (under a timeout) each give an empty standard output, exit 1, and one standard-error line naming the path through `ascii()`. A one-line comment beside the `ascii()` call says it is used instead of the terminal encoder so that `--json` loads no other file. Mutation: print the first records before the failure. *Red when* any standard output appears, the exit is 0, or the comment is absent. `--json` with `--maintainer` exits 2 with an empty standard output; `--json` with `--archive` and with `--root` works. Mutation: accept `--json --maintainer`.
* **No derived value, no fence key.** No emitted key (at any level) contains `fence`, `holder` or `maintainer_waits`. The fence warning stays in the terminal `--maintainer` view only (the Decision). *Red when* such a key appears. Mutation: add a `fences_without_wait` key.
* **The plain board and `--maintainer` are unchanged.** The golden node of C1 passes with C2's refactor of the roadmap reader; the existing `test_replacement_tools.py` passes unedited. *Red when* either fails.
* **The tool describes itself truly.** The set of places that say what the board reads, taken from the tree (`git grep -n -i "header block\|header fields\|nothing else" -- tools templates/skills/_lib docs doctrine templates/core .agents README.md`), is listed in the commit body with each hit marked edited or still true and why. Edited here: the module docstring (it names the title line, `--json` printing what authors wrote and deriving no value, and the roadmap rows), the parser description, and the help text of `--archive` and `--maintainer` wherever `--json` changes what they say. Unchanged and still true: the plain-mode footer `Derived from header blocks; the artifact is authoritative.`, which stays byte for byte because plain mode still prints header fields only. `python tools/board.py --help` no longer says the board reads header blocks only. *Red when* the old claim stays in the docstring or help, or the plain footer changes.
* **The help cites the guide.** `--help` ends with this paragraph (exact wording; whitespace may wrap):

```
JSON form: --json prints the board as data (schema cairn-board/1).
Field reference and worked example: Cairn's own cairn/docs/build-a-board-view.md
(in the repository you adopted from, not in this tree).
```

  The existence of the cited path is C3's test, because the guide does not exist yet. *Red when* the paragraph is absent, names `docs/` as if it were in the adopter's tree, or the `--help` text names a vendor.
* **Install contract unchanged.** `python bootstrap/scaffold.py --manifest` before and after C2 differ by nothing (`diff` exits 0), and no line names `build-a-board-view`. *Red when* the diff is non-empty.
* **Mutation ledger for C2** is recorded in the commit body (see *Verification*); every mutant above is killed.

### C3 -- The guide's contract half

Files: `docs/build-a-board-view.md` (created), `docs/tool-usage.md`, the test file. Not frozen. Checks: K0, K5-K7. Descriptive layer: the guide describes the tool and how to extend it and prescribes nothing cross-cutting.

* **It opens in plain words.** The first `##` section after the title is prose: no table and no fenced block, and it says in plain terms what a view is, that Cairn ships none, and that a page built here is regenerated and never hand-kept. It defines "JSON" and "view" in their first sentence each. *Red when* the first section holds a table or a code fence, or either term is undefined.
* **The guide's tables and the output agree, both ways.** Under the exact headings `### Top-level keys`, `### Artifact records` and `### Roadmap waits`, the first column of each table holds the backticked key and the second its type. `TestGuideAndOutputAgree` requires the key set in each table to equal the emitted key set on a full tree, and the type column to equal the baseline fixture's types. `TestSchemaOneBaselineHolds` gains the rule that an emitted key outside the baseline must be listed in the guide. *Red when* a key is documented and not emitted, emitted and not documented, or typed differently. Mutation: rename `status` to `state` in the board and the guide together (the baseline node goes red; this is the case the proposal's S2 names).
* **The promise is written down, all seven.** The section `## What will not change` carries seven numbered statements matching Revision 1's: only adds within `cairn-board/1`; a break is `cairn-board/2`, announced in `CHANGELOG.md`; consumers read `schema`, refuse other versions and ignore keys they do not know; absent is `null` and a present blank is the empty string (D2) and strings are not escaped for any output; the same files give the same bytes under one producer version, row order is not promised, `path` is the unique key, and `(kind, id)` is unique among live records only (an archived file can share an `id` with a live one: D10); a failure writes nothing to standard output and exits nonzero, so a script that regenerates a page must not overwrite it; and what is not promised (the terminal layout, that an optional field is present, any meaning of free text, and any bound on a value's length). The field table says `line` is Python's count (D14). *Red when* a statement is missing. The standing phrase counts over the section, each at least 1: `ignore keys`, `cairn-board/2`, `CHANGELOG.md`, `live records only`, `must not overwrite`, `length`. `TestOutputIsDeterministic` carries the node that a live and an archived file of one name give two records with different `path`.
* **The lookup, its precedence and its caution.** Under `### The lookup`, a table of status words against holders copies `doctrine/lifecycle.md`'s two diagrams. The section says the key is the first word of `status`, matched exactly (real headers read `archived -- C1-C9 all landed`); a declared wait overrides the status word, so a record with a non-null `waiting_on_maintainer` groups under the Maintainer whatever its status says; the lookup is the doctrine's table, not a check that a status is current or true; and "none named" is not "nobody needed". `TestGuideLookupMatchesLifecycle` reads the node labels of both diagrams (D11) and requires: every status word in either diagram is a row of the guide's table with the holder its label gives; the table's last row, "anything else, including the retired words `proposed`, `reviewed` and `revised`", gives "none named"; no other row names a word that is in neither diagram; `archived -- C1-C9` matches by its first word; an unknown or retired status gives "none named" and keeps the raw status. The test records the labels it read in its failure message. *Red when* any holder differs. Mutation: change one table row (`awaiting-decision` to author) and the test goes red; the test checks the table against the lifecycle document, not against the code it supports. This node is the guard named in *Scope delta*.
* **What the data supports, and does not.** The section `## What the data can and cannot show` says "needs you", "in flight by holder", "queued" (`accepted`, `ready-to-implement`) and "done" are derivable, and that **"blocked" and "an agent is working right now" are not** and why; that roadmap rows other than those declaring a wait are not in the data, and that asking for them is the revival condition; and that the fence warning is not in the data and lives in the terminal view (`python tools/board.py --maintainer`). It says three things about trust. A view is a reading aid, never an approval record, because a contributor who can edit a header can put any status there. `accepted`, `archived` and a file under `archive/` say what a file claims or where it sits, **not that a Decision was recorded, by whom, or that a review ran**; those are in the artifact's `## Decision` section and its commit. And a non-empty `skipped_symlinks`, or `roadmap_read` false, means the data is incomplete and a view must show it. Standing phrase counts, each at least 1: `never an approval record`, `not that a Decision`, `skipped_symlinks`. One-shot: `not derivable`, `reading aid`, `--maintainer`. *Red when* a standing phrase is missing. `TestFenceStaysInTheTerminalView` requires that the guide's only mentions of a fence are pointers to the terminal view and that no fenced code block in the guide computes one.
* **Reaching and running it.** The section `## Reaching it and running it` says: adopters do not receive `docs/`; the guide is read in Cairn's published documentation; `board.py --help` cites it. It says the board itself arrived after Cairn 0.3.0 and `--json` after that, so `tools/board.py` may be absent, or may answer `--json` with exit 2 and "unrecognized arguments"; either means an older install, and `bootstrap/UPGRADE.md` is the upgrade path. Both claims are checked from the tree and the result is recorded in C3's commit body, not as a test node (a copy of the repository without tags would fail one): `git ls-tree v0.3.0` has no `tools/board.py` (the instrument can fire: the same command on `HEAD` finds it). *Red when* the section claims `--json` is in 0.3.0, omits the "board absent" case, or does not name `bootstrap/UPGRADE.md`.
* **The help citation resolves; the guide is not installed.** `TestHelpCitesTheGuide`: the `--help` paragraph contains the token `cairn/docs/build-a-board-view.md` and the words "not in this tree", and the token resolves the way `test_cairn_prefix_links.py` resolves a `cairn/` token (strip the prefix, the path exists under Cairn's root). `TestGuideIsNotInstalled`: no destination in the install manifest names the guide. *Red when* either fails.
* **`docs/tool-usage.md` is true.** The board's entry names `--json` and links the guide, its description says the board reads header blocks and the title line, and that `--maintainer` also reads `dev/PLANNING.md` rows, and keeps its statement that it makes no judgments. The entry is re-read at edit time because `review-stance-and-lenses` changes a phrase in the same paragraph. `python scripts/verify_counts.py docs/tool-usage.md` still passes. *Red when* the entry still says the board reads the header block only.
* **No vendor, no doctrine.** The guide names no AI vendor or product and no hosting service from the neutrality denylist (K5); the page the Maintainer uses today is called, if at all, "a shared web page with live status". `git diff --stat` for C3 lists no `doctrine/` path and not `AGENTS.md`. *Red when* either occurs.

### C4 -- The guide's example and recipes

Files: `docs/build-a-board-view.md`, the test file. Not frozen. Checks: K0, K5-K7. Three fenced Python blocks carry a second word on their opening line as a tag: `python view-example`, `python finished-recipe`, `python intent-recipe`. Each tag occurs once. Each block is plain Python that compiles, keeps its work in functions, and runs its `main` only under `if __name__ == "__main__"`, so a test can load its functions without running it.

* **The recipe: what waits on the Maintainer (the Decision's change).** The guide's section `### What waits on the Maintainer` states the rule in plain words (an artifact counts when it is live and its status starts with `awaiting-decision` not followed by a letter, digit or underscore, or when its `waiting_on_maintainer` is not null; a roadmap row counts when it is in `roadmap_waits`; the result also says when the roadmap was not read and lists every skipped path), names the function `waiting_on_maintainer` in the worked example as the recipe, and shows its three-line use. The function is held **once**, in `view-example`; there is no second copy to keep in step. It returns the entries and a list of caveats (the roadmap was not read; each skipped path). `TestWaitsRecipeAgreesWithMaintainerView` loads it from the example block, applies it to `board.py --json` output, and compares the result with `board.py --maintainer` over each of these trees in turn:
  * every status word of the lifecycle bare, and with ` -- note`, `: note` and `, note` after it;
  * `awaiting-decision-x` (listed: the lookahead excludes only letters, digits and underscore) and `awaiting-decisions`, `awaiting-decision_x`, `awaiting-decision2` (not listed);
  * Waiting lines: blank; `**Waiting on Maintainer **:` (read, the field name is stripped); the marker in lower case (not read); one written below the first `##` (not read); a repeated Waiting line; a repeated `**Status**:` line; a header line with leading spaces;
  * files: a header-less file; a file with no Status line; `_template.md` and `_notes.md`; a plan at `implementing` with a wait; a proposal both at `awaiting-decision` and carrying a wait (one entry, reason `awaiting-decision`, the wait's text); an archived artifact carrying a wait, with and without `--archive` (never listed);
  * roadmap rows in all four forms, a mention that is not a marker, a blank row, and a missing `dev/PLANNING.md` (the recipe says the roadmap was not read, as `--maintainer`'s footer does);
  * C1's links trees, including `dev/plans` as a link and a dangling `dev/PLANNING.md`.

  The comparison is on `(kind, artifact, reason)` always, with roadmap entries named `dev/PLANNING.md:<line>`; on text wherever `--maintainer`'s display is lossless (ASCII, under 47 characters); and on the caveats against `--maintainer`'s skip lines and its not-read line. *Red when* the two differ on any tree. Mutations: compare the status exactly (`== "awaiting-decision"`) so a note drops the entry; treat a blank wait as absent; list archived rows; drop the roadmap half; drop the skip list from the caveats; drop `awaiting-decision-x`.
* **The page example.** `TestViewExample` loads `view-example` and builds a page on a scratch tree inside a scratch git repository holding a copy of `tools/board.py`. It requires:
  * groups in the order Maintainer, author, reviewer, implementer, none named, each with a count; the raw `status` printed beside each row; the label `in_brief` or, when null or blank, the title;
  * the **Maintainer group equals `--maintainer`'s artifact lines** on the status-with-note trees and the roadmap rows (the members are compared, not only the function); a plan at `implementing` carrying a wait is grouped under the Maintainer (the declared wait overrides the status word); the roadmap rows are in the Maintainer group;
  * a header-less file and a file with no Status line: the page is still written (exit 0) and shows each row in "none named" with its status shown as unknown;
  * a title holding `<script>alert("x")</script>` and `'` appears only escaped (`&lt;script&gt;`, `&quot;`, `&#x27;`), never raw; a title holding an escape byte and a right-to-left override appears as visible `U+001B` and `U+202E`, and neither raw character is in the file (D7); a title holding U+3164 appears raw, which is the limit the guide states; a label of 1,000 characters is cut to the stated length on one line;
  * the footer holds the commit id from `git rev-parse HEAD`, says that advisories (plans that mention a fence without declaring a wait) are not shown, names `python tools/board.py --maintainer`, and says "n of m live rows carry an In brief line" with the right numbers;
  * **what the board skipped reaches the page**: on C1's links tree, and on a tree whose `dev/plans` is a link, the footer names each skipped path (through the same escape and `U+XXXX` step) and says the page is incomplete; when `roadmap_read` is false the page says the roadmap was not read.

  *Red when* any of these fails. Mutations: remove `html.escape`; use `quote=False`; remove the control-character step; drop the precedence; omit the stamp; drop the footer's advisory sentence; drop the skipped-paths footer line; build the Maintainer group from the example's own status lookup instead of from the recipe's rule; index `status` without a null guard.
* **A failure never overwrites the page (Revision 1, promise 6).** With an existing page file, make the board fail (a non-UTF-8 artifact), and separately make `git rev-parse` fail; in both the example exits nonzero and the existing page's bytes are unchanged, and with no existing page none is created. Mutation: write the page before the board finishes. *Red when* the page changes.
* **The example's two subprocesses.** An analysis of the block's syntax tree finds exactly two subprocess calls: the board, and `git rev-parse HEAD`; each takes a list, never `shell=True`; the board's first element is `sys.executable` and no element is the bare string `python`. *Red when* the count differs, a shell is used, or `python` is looked up on `PATH`.
* **The lookup in the example matches the lifecycle.** `TestGuideLookupMatchesLifecycle` gains a node that reads the example's mapping and requires it equal the guide's table and the lifecycle's labels. Mutation: change one entry in the example's mapping. *Red when* it differs.
* **The example is short enough to read.** Its line count is recorded in the commit body. It holds the lookup, the groups, the waits function, the escaping, the stamp, the footer and the single write, and is expected to fall between 75 and 110 lines (the proposal said about 50 before the waits recipe, roadmap rows and skip report were added). *Red when* it exceeds 110 after the share figure (D7) has been dropped; then the page-rendering helpers move to a second tagged block and the waits function stays where it is.
* **The finished-plans recipe.** `TestFinishedPlansRecipe` builds a scratch git repository with three plans archived on different dates, one proposal archived, and one plan edited after archiving; both the author date and the committer date are set in the test, and the recipe reports the **author date**, which the guide names. It returns plans only, each with its archive date, newest first, one per plan. The guide says it covers plans only because a proposal archives at plan-open or at a Decision, a different event. The command is also run on this tree and the count of archived plan files equals the count of `A` rows (54 and 54 at `72434d73`). *Red when* a proposal appears, an edit counts as an archive, or the order is wrong. Mutation: include proposals.
* **The intent-join recipe.** `TestIntentJoinRecipe` feeds canned `cairn-intent-list/1` output (shape read from `tools/_intent/cli.py`: an object with `schema` and a `claims` list whose records carry `id`, `agent`, `ts`, `action`, `stem` and `files`, with `stem` the empty string when the claim has none) and a canned board document: a record whose `stem` names an artifact is attached to that artifact as a hint; a record with an empty `stem`, and one whose `stem` names nothing on the board, are listed as unattached and never attached by guessing; a document whose `schema` is not `cairn-intent-list/1` is refused; an empty list gives no hints. The canned shape is checked against the real one: the node runs `python tools/intent.py --log-path <scratch log> claim --agent test --files x --action y` once with `--stem` and once without, then `python tools/intent.py --log-path <scratch log> list --format json`, and requires the keys of the canned records to equal the real records' keys and the empty-string `stem` to appear for the claim made without one. The guide labels the join a hint and says why: the intent log is gitignored and local to one working tree, a dead session's claim reads "working" forever, and the intent tool belongs to a team-gated module the board does not depend on. *Red when* a record with an empty `stem` is attached, or another schema is accepted. Mutation: attach by file overlap.
* **Keeping a page honest.** The section names the triggers: a person running the script (for example as a session-end step) or a post-commit hook the adopter installs; the scaffold never writes `.git/hooks`; with neither, the page is a snapshot and the stamped commit says so. It says: regenerate, never edit by hand; to fix a wrong row, fix the artifact's header and regenerate; never overwrite the page on failure; and that the stamp is `HEAD` while the page reads the working tree (D8). **It warns about the hook:** a hook runs the board and the script of **whatever commit is checked out**, so a branch from someone else runs its own code on your next commit; install the hook only where you trust `tools/`, or point it at a board and script kept outside the working tree. Standing phrase count: `whatever commit is checked out`, at least 1; one-shot: `post-commit hook`, `never writes`, `snapshot`, `regenerate`, `working tree`. *Red when* the standing phrase is missing.
* **The AI-agent note.** One short paragraph says a reader can hand this guide and the board's output to an AI agent and ask for a richer page, to be regenerated rather than hand-edited. It names no vendor or product (K5). *Red when* a name appears.
* **Smoke checks, recorded.** `python tools/board.py --json | python -m json.tool` exits 0 on the live tree; the example is run on the live tree and writes a page whose group counts are recorded; `python tools/board.py --maintainer` and the recipe agree on the live tree.

### M -- Read the page (MAINTAINER-ONLY)

This chunk is the proposal's success criterion and the only way to know the page is useful: a person is the only check. It is fenced because only the Maintainer can answer, and it is not a per-commit approval. It sits after C4 because the page needs only the finished board, guide and example; the summary-line prompt (C5) changes what authors write later, and the page already falls back to the title.

* **The agent's part.** Run the guide's example on the live tree at the commit after C4, save the page outside the repository, and put its path and the question (see *Run order and commits*) in the Waiting line. Record the page's group counts and the share of live rows that carry an In brief line (2 of 6 at `72434d73`, so most rows show their titles). *Red when* the page is not produced from the guide's own block unedited.
* **The answer is recorded verbatim** in *Implementation verification*, with the commit the page was built from. The plan does not archive without it. C5, C6 and code review do not wait for it.

### C5 -- The summary-line prompt

Files: the four templates listed under *Touched*, the test file. Not frozen. Checks: K0, K5-K7. Re-read each file at edit time (`git log -3 -- <file>`); by the Maintainer's order the earlier plans have landed or reached code review, and K0 shows that no unfinished edit of theirs is in the working tree.

* **The set is read from the tree.** `git ls-files | grep -E '(proposals|plans)/_template.md$'` lists exactly the four files (control: the same listing without the filter shows `dev/strategy/_template.md`, which is not a proposal or plan template and is not edited). *Red when* a fifth appears or one of the four is skipped.
* **Each gains one header line and one prompt.** Below the rule, after `**Opened**:`: `**In brief**: {{one plain sentence: what changes and why it matters}}`, exactly one occurrence. Above the rule, a paragraph of at most eight lines, in the preamble area, that says: write one plain sentence a scientist outside the project could follow; keep it on one physical line, because the board reads that line only; `python tools/board.py --json` prints it as `in_brief` and a view shows it in place of the title; a longer `## In brief` section below the header is separate and is not read by the board; and leave no placeholder in a finished artifact, because the board prints whatever the line holds. *Red when* a file has zero or two header lines, or the paragraph is longer than eight lines.
* **The board reads the line from each template.** `TestTemplatesAskForTheLineTheBoardReads` takes each of the four files from the rule onward, replaces every `{{...}}` placeholder with fixed text, sets the In brief line to a known sentence, writes the result as a plan (or proposal) in a scratch tree, runs `--json`, and requires `in_brief` equal to the sentence, for all four. *Red when* any of the four differs. Mutation, once per file (four mutants): rename the line to `In-brief` in that file only; the node must go red naming that file.
* **A copied template lists nothing as waiting.** The same four scratch artifacts have `waiting_on_maintainer` `null` and no entry in `--maintainer`'s list, so the new line does not repeat the trap the Waiting-line preamble explains. *Red when* a copied template lists as waiting.
* **Additions only.** For each file, `git diff -U0 <parent> -- <file>` shows no removed line and two added hunks (the paragraph, the header line). *Red when* a line is removed or a third hunk appears.
* **The existing pins pass.** The tests that read these templates, found by searching `bootstrap/tests` for each file's name and for any phrase from a cell they pin (at edit time, so tests added by earlier plans are included): at least `test_scope_reduction_trap.py`, `test_scaffold.py`, `test_documentation_plan_module.py`, `test_claim_check_module.py` and `test_quickstart_sequence.py`, plus the template-reading tests the two earlier plans add. All pass. *Red when* one fails that did not at the parent.
* **No lockfile churn.** `dev/plans/_template.md` and `dev/proposals/_template.md` stay in the 18-file list and are not finalized; the count equals the parent's. *Red when* the count grows or a finalize touches either record.

### C6 -- Boundary B and the record

* **The record is complete.** `## Implementation verification -- <agent> -- <date>` carries every field *Verification* lists: the node IDs of the new test file as `pytest --collect-only -q` prints them, the neutrality figures before and after, the AST comparison, the manifest diff, the mutation ledger with a control run, the old-versus-new comparison of the terminal board, the recipe counts, the example's line count, a run of the new test file from a working directory other than the repository root, and the Maintainer's answer to M when it has come. *Red when* a field is absent or an ID differs from the collection.
* **The old-versus-new comparison.** In a throwaway worktree at the tested commit, put C1's parent version of `board.py` (`git show <C1 parent>:tools/board.py`) beside the new one and run both with `--root` on the live tree and on the C1 golden tree (no links): the plain board, `--archive` and `--maintainer` outputs are equal byte for byte (`cmp`). *Red when* any differs.
* **The not-touched list is shown.** `git diff --stat <base>..<tip> -- bootstrap/_scaffold bootstrap/scaffold.py doctrine AGENTS.md templates/core/AGENTS.md tools/session.py bootstrap/UPGRADE.md bootstrap/tests/test_replacement_tools.py bootstrap/tests/fixtures/gate_manifest.json` is empty. *Red when* it lists a path.
* **Twins and records, finally.** `cmp` of the board pair exits 0; the `tools/board.py` record's hash equals the template's at the tip; `python bootstrap/verify_integrity.py --target .` lists the files the parent of C1 listed.
* **Status moves** to `awaiting-code-review` in that commit.

## Scope delta

**Scope delta**: degraded -- the proposal's own declaration, as the Maintainer allowed at the Decision ("The Scope delta is allowed as revised"). This plan removes nothing further from the accepted scope; the entries below are carried so each is dispositioned before archive. The baseline is the proposal as accepted: Revision 1 with the Decision's changes.

Against the opening text, three units left the contract. Specifying `status_holder` needed a doctrine decision nobody had made, and specifying the wait keys needed code that did not exist; the Maintainer's allowance, quoted from the Decision block and its scribe's note, covers all three:

> "accept both as descried"

* **`status_holder` in the board's data** (and the opening's terminal column). The outcome "a view can group by who acts next" is delivered by the guide's tested lookup (C3, C4). **disposition**: guard (`bootstrap/tests/test_board_json_contract.py::TestGuideLookupMatchesLifecycle`). The terminal column is moot and is wontfix.
* **`maintainer_waits` in the data.** The Decision changed the revised text, which had deferred it: "For the board proposal, I'd put the what waits on my in the recipe, actually instead of deferring it." and "Yes, now" for the roadmap rows. The outcome "a view can list what waits on the Maintainer" is delivered by the recipe, over `waiting_on_maintainer` and `roadmap_waits` (C2, C4). **disposition**: guard (`bootstrap/tests/test_board_json_contract.py::TestWaitsRecipeAgreesWithMaintainerView`).
* **`fences_without_wait`.** A body-text heuristic whose membership cannot be promised; the Decision: "Terminal view only". **disposition**: wontfix, for that reason; the terminal `--maintainer` footer carries it and the example's footer points to it.

Every accepted outcome maps to a chunk:

| Accepted outcome | Chunk |
|---|---|
| `--json` and the document, with `--archive` adding archived artifacts; `--json` with `--maintainer` a usage error | C2 |
| `title`, `in_brief` and `waiting_on_maintainer` reads; no derived value | C2 |
| Roadmap rows that declare a wait in the `/1` data now (Decision) | C2 |
| The promise (seven statements) and the baseline that can catch a break | C2 (fixture and node), C3 (the statements) |
| A symlinked artifact skipped, in both modes (the rule's full reach is D4) | C1 |
| The four places that say the board reads headers only, and the symlink rule's scope | C1, C2, C3 |
| `--help` cites the guide; the guide read in Cairn's docs, not copied into installs | C2, C3 |
| The guide: fields, promise, lookup with precedence, what the data supports | C3 |
| The worked example with the stamp and escaping | C4 |
| "What waits on the Maintainer" as a recipe (Decision) | C4 |
| Finished plans by date, and the intent join, as tested recipes | C4 |
| When a page regenerates; keeping it honest; the AI-agent note | C4 |
| The `**In brief**:` prompt in the proposal and plan templates now (Decision) | C5 |
| The fence warning in the terminal view only (Decision) | C2, C3, C4 (no key, no recipe) |
| `docs/tool-usage.md` gains `--json`, a link and a corrected description | C3 |
| The scoped lockfile finalize | C1, C2 |
| The reading of the page as a success criterion | M |
| The Evidence plan's tests and smoke checks; Boundary A additions; Boundary B full | C1-C4, C6 |
| The mutations the preflight names (S2) | the *Verification* ledger |
| Sequencing: the first chunk starts from a tree holding `72254d0e` | *Sequence* |

Several things differ from the text in mechanism, none in outcome, and the Maintainer's allowance is not assumed for any of them: the link rule reaches folders, `dev`, `archive` and the roadmap file, covers broken and looping links, refuses non-regular entries, and is reported (D4, D6); the data carries `roadmap_read` and `skipped_symlinks` as the shape of the Decision's roadmap rows and of the reporting D4 needs (D1); a present blank line is the empty string (D2); `path`, not `(kind, id)`, is the unique key, which corrects a statement of fact in Revision 1's fifth promise (D10); and the page reports what the board skipped and the share of live rows with a summary line (D7). Each is a closure of an accepted outcome, listed here so a reviewer can overrule it. No outcome is dropped.

## Verification

**Boundary A (iteration, scoped).** Each chunk runs the tests that own the files it touches, plus its standing gates: the K checks above, `python scripts/check_cairn.py` and `python scripts/claim_check.py <file>` for each edited document, and `python bootstrap/verify_integrity.py --target .` after a finalize. The tests, found by searching `bootstrap/tests` for each touched file's name and, for the templates, for the pinned phrases (all in `bootstrap/tests/`):

| Chunk | Tests |
|---|---|
| C1, C2 | `test_board_json_contract.py` (the chunk's new nodes), `test_replacement_tools.py` (unedited), `test_notice_install.py` (twin byte identity and SPDX header), `test_security_lint.py`, `test_security_check.py`, `test_skills_self_heal.py`, `test_skills_upgrade.py`, `test_verify_integrity.py` (the lockfile reader), `test_cairn_prefix_links.py` |
| C3 | `test_board_json_contract.py` (guide, lookup, help, not-installed nodes), `test_cairn_prefix_links.py`, `test_doc_governance.py`, `test_check_cairn_content.py`, `test_check_cairn_counts.py`, `test_link_check_exclusions.py`, `test_quality_gate_neutrality.py` |
| C4 | `test_board_json_contract.py` (the example and recipe nodes), `test_intents_tool.py` (run because the recipe depends on the tool's JSON form; the new node also checks the canned shape against the real one) |
| C5 | `test_board_json_contract.py` (template nodes), `test_scope_reduction_trap.py`, `test_scaffold.py`, `test_documentation_plan_module.py`, `test_claim_check_module.py`, `test_quickstart_sequence.py`, and every test that names a template path or pins a template phrase, searched again at edit time |

This mapping is not a confident bound: dozens of test files drive a scaffold install, which renders the shipped templates, and `tools/board.py` is a verbatim installed tool. So Boundary B is the real check.

**The mutation ledger (the implementer's, recorded in the commit body of the chunk that owns each mutant; Boundary C may repeat it).** Each mutant is one deliberate break, made in a separate copy and run against the chunk's tests, with an unmutated control run beside it. Report each as killed (some test fails), survived (all pass), or equivalent (no behaviour change, shown by a behaviour test through the real entry point); anything not shown equivalent by measurement is a survivor. The set, with the set-wide ones taken from the tree:

| Mutant | Killer | Chunk |
|---|---|---|
| the twelve one-line breaks of `tools/board.py` listed under C1, and the two footer rewordings | the golden node, with `test_replacement_tools.py` beside it; each reported killed, survived or equivalent | C1 |
| delete the link check in the artifact reader; test the leaf, `dev/proposals` and `dev/plans` but not `dev` or `archive`; keep `if not base.is_dir(): continue` ahead of the link check; delete it in the `dev/PLANNING.md` read; also test the folders above the root | the ten links trees and the reach-limit case | C1 |
| read an artifact leaf before the `lstat` check | the folder-named-`x.md` and pipe cases | C1 |
| load the terminal encoder from the `--root` tree | `TestBoardLoadsOnlyItsOwnEncoder` | C1 |
| for each key of the baseline fixture, delete it from the emitted document | `TestSchemaOneBaselineHolds` | C2 |
| change `_header_fields` alone (a repeated field read first-wins) | the plain board, `--maintainer` and `--json` outputs | C2 |
| build the record by copying every header field in under a snake_case name | `TestRecordFactsComeFromWhereTheFileSits` | C2 |
| rename `status` to `state` in the board and the guide together | the baseline node | C2, repeated at C3 |
| emit `""` for an absent field; emit `null` for a blank Waiting line | the absent-is-null node; the recipe node | C2, C4 |
| unsorted keys; non-ASCII output; archived rows without `--archive`; a live and an archived file of one name given one `path` | the determinism and archive nodes | C2 |
| print part of the document before a failure; accept `--json --maintainer` | the failure and usage nodes | C2 |
| change the row grammar in the shared roadmap function only; keep a second copy in the JSON path | the roadmap-equals-`--maintainer` nodes | C2 |
| add a `fences_without_wait` key | the no-fence-key node and the guide-agrees node | C2, C3 |
| change one row of the guide's lookup table | `TestGuideLookupMatchesLifecycle` | C3 |
| remove the help paragraph | `TestHelpCitesTheGuide` | C3 |
| change one entry of the example's mapping | the example-mapping node | C4 |
| in the example: remove `html.escape`; use `quote=False`; remove the control-character step; drop the precedence; omit the stamp; write the page before the board finishes; drop the skipped-paths footer line; drop the advisory sentence; build the Maintainer group from its own status lookup; index `status` without a null guard | `TestViewExample` and the failure node | C4 |
| in the waits function: compare the status exactly; treat a blank wait as absent; list archived rows; drop the roadmap half; drop the skip list from the caveats; drop `awaiting-decision-x` | `TestWaitsRecipeAgreesWithMaintainerView` | C4 |
| include proposals in the finished-plans recipe; attach an intent record by file overlap, or one with an empty `stem` | the recipe nodes | C4 |
| rename the line to `In-brief` in each of the four templates, one at a time | `TestTemplatesAskForTheLineTheBoardReads` | C5 |

Every one is expected killed, except C1's tab and double-bullet mutants, which are expected equivalent and must be shown so by a behaviour test through the real entry point. A survivor is a finding, not noise.

**Boundary B mode**: full. The refusal rules in `AGENTS.md` settle it:

1. **A tool every adopter runs changes, and its record is touched.** `tools/board.py` is a verbatim installed file; its lockfile record is reconciled twice; `test_security_lint.py` scans it. Uncertainty resolves to full.
2. **Four shipped templates change.** The two `templates/core/` files are rendered into every install, and dozens of tests drive an install. No mapping bounds that confidently.
3. **The gate manifest's pinned collection grows** and two new files join the frozen patterns, which touches the gate-manifest contract surface.
4. **The plan declares a security obligation** (`Internal + Internal Security Review`): a file-handling rule and a published output other programs read.
5. **The accepted text expects full.**

**How Boundary B runs.** After the last implementation commit (C5), against a clean unchanged commit, under the canonical interpreter (`/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.x). Run it from a separate `git worktree` at the tested commit, which shares refs (so the gate anchor is present) and keeps other sessions' uncommitted files out of the count:

```
CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
python scripts/quality_gate.py --sub neutrality --sub redundancy
```

then `python scripts/check_cairn.py`, and `python scripts/claim_check.py` and `python scripts/link_check.py` on each edited document. The record is appended as `## Implementation verification -- <agent> -- YYYY-MM-DD` with the template's fields: **Boundary B mode**, **Tested commit**, **Reviewed range**, **Interpreter/runtime**, **Pre-run state** and **Post-run state**, a command table with Command, Exit, Outcomes and Elapsed, **Non-pass disposition**, **Plan-specific acceptance commands** and **Known omissions**.

**Plan-specific acceptance at Boundary B.**

* The neutrality leg exits 0 with `fail=0`; both figures are recorded and equal the parent's.
* The two AST nodes of `test_ast_attest.py` fail at the base for other work. The verify output is derived at the tested commit's parent and at the tested commit and shown equal (4 CHANGED symbols at `72434d73`); no `bootstrap/_scaffold` byte changed. If the Maintainer has re-anchored meanwhile, both are clean and equal.
* `python bootstrap/scaffold.py --manifest` at the plan's base and at the tested commit differ by nothing.
* `python bootstrap/verify_integrity.py --target .` lists the files the base listed.
* `python tools/board.py --json | python -m json.tool` exits 0 on the live tree; the example's page is built from it.
* The new test file is run once from a working directory other than the repository root, and passes.
* The old-versus-new comparison of the terminal board (C6) and the mutation ledger with control runs.
* `git diff --stat` over the range shows no existing frozen file edited; the only paths matching the frozen patterns are the two new files.

**Expected non-pass.** Only the two AST nodes above, each disposed of rather than treated as noise. `test_gate_manifest.py` has no expected failure; changed frozen bytes would not redden it, and none change. Any other skip, xfail, xpass or failure is a finding.

**Boundary C** is the code reviewer's, after Boundary B. The points worth attacking:

* **The set of text sources.** List from the tree every path the board opens (`read_text`, `glob`, `is_dir`, `is_file`, `open`) and show each is preceded by the `lstat` check or is the encoder load; try a link at each level (a leaf, a folder at each depth, `dev/` itself, `archive/`, `dev/PLANNING.md`), a broken link, a link to itself and a link to a file inside `dev/`; and try the cases that must stay readable (a root reached through a linked parent, `--root` given as a link).
* **Pathological entries.** A folder or a named pipe called `x.md`, a file of a very large size (accepted, S5), and an entry that changes type between the check and the read.
* **Absent versus blank.** Build a header that mixes a blank Waiting line, a missing one, and one written below the first `##`; confirm the data, `--maintainer` and the recipe agree.
* **The recipe against `--maintainer`.** Find a status or row shape the table of trees misses. Try a status whose first word differs from the board's pattern, a status with leading whitespace, tabs or a non-breaking space, a duplicated `**Status**:` line, and a Waiting line whose text holds `|`.
* **The output's promises.** Run twice from different directories and roots; diff. Feed a title holding every character class (escape, bidi override, NUL, a lone surrogate written as an escape) and show the document stays valid ASCII JSON.
* **The example as a reader copies it.** Read it cold: does it run from a fresh checkout with only the standard library? What does the page show for an artifact whose title is empty, whose `in_brief` is only spaces, or whose status is hostile?
* **The baseline.** Is any key in the output that the baseline does not name, and is the guide's type column the baseline's?
* **The frozen pair.** Confirm the test and the fixture are the only frozen-pattern paths in the range, and that no later commit edits either after the last one a re-anchor might cover.
* **The templates, for every member.** List the four from the tree, and in a separate copy break the line in each.
* **The terminal board.** Rerun the old-versus-new comparison on a tree the author did not build.

### Security preflight, re-answered where the chunking changes an answer

* **S1 -- who supplied it?** Every value comes from artifact files and `dev/PLANNING.md`, which any contributor can edit, and from the file names. Nothing is derived, so the board makes no claim about whose move it is and authenticates nothing. The guide says a view is a reading aid and never an approval record, and that a status word is not evidence of a Decision. The link rule (C1) is the control on *which files* may supply text: measured today, a leaf link, a folder link, a linked `dev` or `archive` and a linked roadmap file are all followed, and broken or looping links vanish silently or crash the board; after C1 every component from `dev` to the leaf is checked by `lstat` before anything follows a link, and each skip is visible in the terminal, the data and the page.
* **S2 -- can it fail?** Each control has a mutant that turns a named node red (the ledger): the link check at four call sites and at the reach limit, the baseline per key, the one header reader, forged header names, absent-versus-blank, the failure path, the usage error, the shared roadmap reader, the encoder load, `html.escape`, `quote` and the control-character step in the example, the skipped-paths footer, the recipe's status rule, and the four templates. The golden node's strength is shown by twelve plausible accidents, not by two footer rewordings. The lookup test checks the guide against the lifecycle document, not against the code.
* **S3 -- what fires it, over what?** `python -m pytest bootstrap/tests/test_board_json_contract.py` and the Boundary B full run, both started by a person; Cairn has no CI and no hook runs them. The example's regeneration trigger is a person running the script (for example as a session-end step) or a post-commit hook an adopter installs; the guide says so and says the stamp is the only sign the trigger did not fire. Opened and read: the trigger for the neutrality leg is the second Boundary B command, also a person.
* **S4 -- which way does it break?** An absent line is `null`, a failure writes nothing, an unknown schema makes a consumer refuse, an older board refuses `--json` with exit 2, a link is skipped and said and never followed, and an entry that is not a regular file fails loudly and never hangs. The hazards are human: reading "none named" as "nothing to do" (the guide says it is not), and reading a short list as an empty one (`roadmap_read`, the skip list and the page footer exist for that).
* **S5 -- who still wins?**
  * **A contributor who can edit a header** can put misleading, well-formed text on the board: claim `archived`, omit a Waiting line, or put markup or a direction override in a title. The board leaves strings raw (the terminal encoder would turn `A | B` into `A \x7c B`, wrong for data), so the duty falls on the page-builder. That class is closed **by enumeration** in the guide and **by construction only in the example**: `html.escape` plus the `U+XXXX` step.
  * **An adopter's own page-builder** that forgets to escape is not covered, and cannot be.
  * **Someone who edits the baseline and the code together** defeats the baseline test until the next re-anchor; from then on the fixture is frozen and the edit is a hold at the ceremony. Only review reads that diff before then.
  * **A link swapped in after the check.** The check is `lstat` before the read, so a local attacker racing the process could win. The threat the rule answers is a *committed* link, which exists before any check, so a race is out of scope; it is recorded, not closed, and D15 records why the open-flag hardening is not adopted.
  * **The example's subprocess.** The example runs two fixed-argument subprocesses, never through a shell. An adopter who wires it to a hook adds a subprocess to their own tree; the guide says so.
  * **A second reader of the same files.** The recipe and `--maintainer` are two readers of one rule; the equality test is what keeps them one, and a new status shape outside its table would not be seen.
  * **A very large committed file** is read whole, as today, and accepted: it shows itself in the clone, and the tool only reads.
  * **The hook.** A post-commit hook runs whatever board and script the checked-out commit carries. The guide says so and says where to install it (C4); an adopter who ignores that has chosen to run a branch's code on their next commit.
  * **Invisible fillers and length.** The example shows control and format characters and cuts long labels; fillers outside category C pass raw and the guide says so (D7). Promise 7 says no bound on a value's length is promised.
  * **A forged name.** A header line named like one of the board's own facts cannot reach a record: C2's forged-name node pins it.
  * **A skipped folder on an adopter's tree.** An adopter who keeps `dev/` as a link will find, after upgrading, that the board reads nothing and says so. The `CHANGELOG.md` entry says it (see *Dispositions*), so the skip line is not their first notice.

## Dispositions

*Filled at archive-preparation.* Known now:

* **The archive commit writes this plan's `CHANGELOG.md` entry** (the changelog-at-archive rule). It states: `--json` and the contract `cairn-board/1` with its promise, and that a break is `cairn-board/2` announced in this file; the roadmap rows and the link rule with its report; the guide in Cairn's docs and not installed; the `**In brief**:` prompt in the four templates; that the terminal board is unchanged on a tree with no links; and, in one sentence, that **an adopter who keeps `dev/` or a folder under it as a symbolic link will find after upgrading that the board reads nothing from it and prints a skip line**. It points to this plan and the guide.
* **`status_holder`**: `guard`, naming `bootstrap/tests/test_board_json_contract.py::TestGuideLookupMatchesLifecycle`. The terminal column is `wontfix` (moot).
* **`maintainer_waits`**: `guard`, naming `bootstrap/tests/test_board_json_contract.py::TestWaitsRecipeAgreesWithMaintainerView`. It is no longer deferred.
* **`fences_without_wait`**: `wontfix`, with the Decision's "Terminal view only" and the reason that its membership cannot be promised.
* **The re-anchor** row on `dev/PLANNING.md` gets the node IDs of the new test file at archive, and the sentence that both new files must be final before the ceremony. This plan carries no Waiting line at archive: the open wait, the re-anchor, is declared on its marked board row.
* **Roadmap rows without a wait marker** are not in the data. That is the proposal's recorded decision, not a follow-up. Its live home is the guide's "what the data can and cannot show" (C3), which states the revival condition: the Maintainer asks for roadmap items on a view, once the wait marker has had use. It is not a board row, because nothing is owed.
* **The proposal's "Signals the change is wrong".**
  * *A consumer needs a field we left out, and adding it means renaming or retyping one*: `guard`, `TestSchemaOneBaselineHolds`.
  * *Authors rarely write the summary line*: the page footer reports the live share, so the signal is read on the page the Maintainer already opens; `guard`, the footer node of `TestViewExample`. The starting figure is 2 of 6 live artifacts at `72434d73`. If under half carry the line 30 days after C5 lands, the prompt did not work; whoever opens the page sees it. No board row, because the trigger is a person opening the page, said honestly.
  * *The stamp on the page is older than `HEAD` when opened*: `wontfix`. It is a judgment read by a person, and no mechanism fires the script; the guide names the triggers and the stamp, which is the only sign. Nothing is owed and nothing reaches an adopter beyond the guide's words.
  * *The page is still hand-edited beside the generated one*, and *requests for an `--html` flag*: `wontfix`. They are judgments the guide answers in words; no mechanism observes them.
  * *Two views carry different lookups, or one disagrees with `doctrine/lifecycle.md`*: `guard`, `TestGuideLookupMatchesLifecycle`.
* **A reading that asks for more.** If the Maintainer's answer at M asks for a field the data lacks, that is a new additive key and a deviation request, not a silent addition.
* **Open-flag hardening of the leaf read** (`O_NOFOLLOW`, `O_NONBLOCK`, `fstat`): `wontfix`, for the reason in D15. Nothing reaches an adopter.
* Any `defer` that arises is put to the Maintainer as **one batch** at archive-preparation, with the Waiting line, and needs the Decision's words quoted verbatim. None is known now.

## Plan review -- Claude Opus 5.5 (Internal Security Review) -- 2026-10-18

```
Reviewed commit: 10ae64280fbf31bae111077118d421728d5bd0ac
Target: the whole plan, read for security: C1's link rule, C2's data form and failure path, C3's promise and trust statements, C4's example, recipes and hook advice, the terminal and data encoders, pathological input, and the lockfile and frozen-file handling; checked against the proposal's F10 and its preflight S1-S5
Prior findings: none of this tier on the plan; the proposal's F10 is read for whether the plan answers it
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Model**: claude-opus-5-5

Distance: a fresh session of the author's agent type. I wrote neither the
proposal, its review, nor this plan. This pass runs beside the ordinary Internal
pass and does not repeat its scope-and-simplicity job.

### In plain terms

The plan's design is safe, and it is the simplest safe design I can see:
refusing every link (rather than working out where a link points) is simpler
and stricter. Two gaps in how that rule is tested need closing before
implementation.

* **What already holds, measured.** The terminal board already shows hostile
  characters safely: escape sequences, terminal-title tricks and
  direction-reversing characters all come out as visible codes. The planned data
  form will be plain printable text whatever a file holds. The example page's
  escaping stops the dangerous characters. All three reasons the proposal's
  review added this Security Review (F10) are answered.
* **Blocking 1 (BB-SR1).** A link that points nowhere, or at itself, looks to
  the board like "no folder here", so the board says nothing. The plan's tests
  only build links that point at something real, so they would pass a version
  that still drops these silently. They also never link `dev/` itself or an
  archive folder.
* **Blocking 2 (BB-SR2).** After C1 the terminal will say what it skipped, and
  the data will list it. But the page you will read, and the "what waits on
  you" recipe, do not have to show it. One link would give you a page that says
  nothing needs you while the terminal says the board read nothing.
* **Medium.** No test feeds a header line that pretends to be one of the
  board's own facts, such as `**Archived**: yes` (BB-SR3). The guide's suggested
  post-commit hook would run another person's copy of the board whenever you
  commit on their branch (BB-SR4).
* **Low.** BB-SR5 to BB-SR10: where the board loads its one other file from,
  a key the guide calls unique that is not, folders and pipes named like files,
  invisible characters and very long values on the page, roadmap line numbers,
  and one sentence about status words and Decisions.

None needs a new mechanism or a Maintainer decision. Each fix is a test case, a
mutant, or a sentence inside an accepted outcome.

### F10: why this pass exists, and whether the plan answers it

F10 (`dev/proposals/archive/2026-10-18-claude-board-as-basis.md:632`) raised
three points. The preflight described a file-handling rule and an attacker who
survives it, yet the plan review was declared "no security surface". S2 named
no mutant for the symlink rule or for "failure prints nothing". And the example
found `python` on `PATH`. The plan answers all three: the declaration (plan
line 5), the link-check mutants at three call sites (lines 247 and 394), the
failure mutant (lines 264 and 399), and `sys.executable` with no bare `python`
(line 301).

### What I measured

All probes ran at `10ae6428` in a detached worktree in a fresh scratch folder,
with `python3.13 -I`, against scratch trees passed through `--root`.

| Probe | Today's board |
|---|---|
| a plan linked to a file outside `dev/`; `dev/proposals` linked to a folder outside; `dev/PLANNING.md` linked to a file outside | all three read, in the plain board and `--maintainer` (agrees with the plan's *Found while planning*) |
| `dev` itself linked | read |
| `dev/plans/archive` linked, with `--archive` | read |
| a leaf link to itself | the whole board fails with a traceback, exit 1 |
| `dev/plans` linked to itself | "0 row(s)", no mention of anything |
| `dev/plans` and `dev/PLANNING.md` as dangling links | every plan silently absent; the roadmap file called "missing" |
| a folder named `x.md` | the whole board fails (`IsADirectoryError`), exit 1 |
| a named pipe `fifo.md` (git cannot store one) | hangs; killed by the 3-second timeout |
| ESC colour codes, a terminal-title sequence, BEL, U+202E, `\|` and `\` in Status and Waiting lines; ESC in a file name | all escaped; no raw control byte and no U+202E in standard output (control: the same check on the source file finds five control bytes and U+202E) |
| a form feed and U+2028 ahead of a marked roadmap row | `--maintainer` says line 6; `grep -n` says line 4 |
| a `--root` tree holding a planted `tools/session.py` that writes a marker file | not executed (control: loading the planted file directly writes the marker) |
| `json.dumps(..., ensure_ascii=True)` over U+0000-U+00FF, U+202E, U+2028, a lone surrogate and a tag character | printable ASCII and newlines only; round-trips through `json.loads` |
| the plan's D7 rule, modelled: `html.escape`, then category C shown as `U+XXXX` | ESC, U+202E, U+2066, U+200F, U+FEFF, U+00AD, NUL, a lone surrogate and U+E0041 shown as codes; `"><img src=x onerror=...>` escaped; U+3164, U+115F, U+034F, U+FE0F and U+E0100 pass through raw |

Lockfile: both finalize precedents (`2ea3f869`, `72254d0e`) change the `"hash"`
line of one record and leave `base_hash`, which is what K2 expects. The
`tools/board.py` record's hash (`67f705c6...`) equals both copies today.

### Findings

**[BB-SR1] (blocking) The link rule's tests would pass a version that still
drops a broken or looping link without a word, and they never link `dev/` or an
archive folder.**

* **Evidence.** `tools/board.py:104`, `:107` and `:153` ask `is_dir()` and
  `is_file()`, which follow links, before anything is read. Measured above: a
  folder linked to itself gives "0 row(s)" with no mention; a dangling
  `dev/plans` link drops every plan silently; a dangling `dev/PLANNING.md` is
  called "missing". C1's links tree (plan line 244) holds a leaf link, a
  `dev/proposals` link and a `dev/PLANNING.md` link, all to targets that exist,
  plus a link inside `dev/`. Its mutants (line 247) kill "check the leaf only",
  but two others survive every C1 node: "check `dev/proposals`, `dev/plans` and
  the leaf, but not `dev` or `archive`", and "keep `if not base.is_dir():
  continue` ahead of the link check". Each leaves a link unreported, which D4
  (line 155) names as the failure: "A skip nobody can see reads as an empty
  board."
* **Recommended fix.**
  * State the rule as: every path component strictly below the resolved root,
    from `dev` down to the leaf, is examined with `is_symlink()` (an `lstat`)
    before any call that follows links (`is_dir`, `is_file`, `exists`, `glob`,
    `read_text`).
  * Add to `TestSymlinkedSourcesAreNotRead`: `dev` itself linked;
    `dev/plans/archive` linked, run with `--archive`; a dangling folder link; a
    folder linked to itself; a dangling `dev/PLANNING.md`. Each is named once,
    in the skip line and in `skipped_symlinks`; `roadmap_read` is false; and
    `--maintainer` does not call a linked or dangling roadmap file, or one under
    a linked `dev`, "missing".
  * Add one case that keeps the rule from reaching too far: a root reached
    through a linked parent folder, and `--root` given as a link, read normally.
    `main()` resolves the root today (`tools/board.py:213`), which is correct.
    An implementation that also tested folders above the root would empty the
    board for anyone whose home folder sits on a linked volume, and the cheapest
    repair an adopter would find is deleting the check.
  * Add the two surviving mutants to the ledger row at line 394.

**[BB-SR2] (blocking) What the board skipped reaches the data but never the
page or the recipe.**

* **Evidence.** `TestViewExample` (plan line 299) requires the page to say so
  when `roadmap_read` is false, but says nothing about `skipped_symlinks`.
  `TestWaitsRecipeAgreesWithMaintainerView` (line 298) compares the C1 links
  tree on `(kind, artifact, reason)`, where both sides list nothing, and never
  compares the skip report. The guide's "What the data can and cannot show"
  (line 288) has no sentence about it. The plan's own S4 (line 458) says the
  skip list exists so that "a short list" is not read "as an empty one", but
  nothing that reaches the Maintainer uses it. The case is not only hostile: an
  adopter who keeps `dev/` on a synced folder through a link gets an empty page.
* **Recommended fix.**
  * `TestViewExample`: on the C1 links tree, and on a tree whose `dev/plans` is
    a link, the page footer names each skipped path (through the same
    `html.escape` and `U+XXXX` step) and says the page is incomplete. Mutant:
    drop that footer line.
  * The waits recipe returns the skip list, and its node compares it with
    `--maintainer`'s skip lines.
  * "What the data can and cannot show" says a non-empty `skipped_symlinks`
    means the data is incomplete and a view must show it. Phrase count:
    `skipped_symlinks`, at least 1.

**[BB-SR3] (medium) No test feeds a header line named like one of the board's
own facts.**

* **Plain.** Four values in each record come from where the file sits (`kind`,
  `id`, `path`, `archived`), not from what an author wrote, and a page-builder
  will trust them more than free text. If the code ever copied header lines into
  the record by name, a file could write `**Archived**: yes` or
  `**Path**: javascript:alert(1)` over them. The plan's table does not do this,
  but no planned test would notice if the code did.
* **Evidence.** The contract table (plan lines 73-82) gives each key one source.
  The value test (line 257) and `TestGuideAndOutputAgree` (line 285) use a tree
  "with every field written", meaning the contract's own lines, and on that tree
  a by-name copy emits exactly the same keys. The header pattern accepts any
  name of letters, spaces, `/` and `-` (`tools/board.py:42`). Revision 1 calls
  `path` "a link target"
  (`dev/proposals/archive/2026-10-18-claude-board-as-basis.md:817`).
* **Recommended fix.** One node in C2: a header carrying `**Kind**: proposal`,
  `**Id**: forged`, `**Path**: javascript:alert(1)`, `**Archived**: yes`,
  `**Schema**: cairn-board/2`, `**Title**: forged`, `**Includes archive**:
  true`, a non-contract `**Assurance path**:` line, and two `**Status**:` lines.
  Required: the record's keys are exactly the twelve; `kind`, `id`, `path` and
  `archived` come from the location; `title` comes from the `# ` line; `schema`
  is `cairn-board/1`; the repeated Status gives the value `--maintainer` uses
  (the last, `tools/board.py:96`). Mutant: build the record by copying every
  header field in under a snake_case name.

**[BB-SR4] (medium) The guide's suggested post-commit hook runs whatever board a
checked-out branch carries.**

* **Plain.** A hook runs on every commit, and the example runs
  `tools/board.py` from the working tree. Check out someone else's branch to
  review it, commit your review, and the hook runs their copy of the board, and
  of the script too if it lives in the tree. Without the hook, committing a
  review runs nothing of theirs.
* **Evidence.** "Keeping a page honest" (plan line 306) names the hook as a
  trigger; its phrase counts are `post-commit hook`, `never writes`,
  `snapshot`, `regenerate` and `working tree`. S5 (line 464) says only that the
  adopter "adds a subprocess to their own tree". The example's command is
  `[sys.executable, "tools/board.py", "--json"]`
  (`dev/proposals/archive/2026-10-18-claude-board-as-basis.md:895`), a path
  inside the working tree. Hooks in `.git/hooks` serve every worktree of a
  repository. Session-start also runs the checked-out board
  (`.agents/skills/session-start/SKILL.md:38`), but a person or agent chooses
  that run; a hook fires on a commit made for another reason.
* **Recommended fix.** The section says that a hook runs the board and the
  script of whatever commit is checked out, so a branch from someone else runs
  its own code on your next commit; install the hook only where you trust
  `tools/`, or point it at a board and script kept outside the working tree.
  Phrase count: `whatever commit is checked out`, at least 1.

**[BB-SR5] (low) The "no dynamic code" check cannot see the board's one dynamic
load, and nothing pins where that load comes from.**

* **Plain.** The board already runs one other file: it loads the terminal
  encoder from its own `tools/session.py`. Today that is always the tool's own
  copy, never the copy inside a tree named by `--root` (measured). That is the
  property that matters: the other way, reading a stranger's tree would run the
  stranger's code. K3 would not notice the change.
* **Evidence.** `tools/board.py:73-76` (`spec_from_file_location`,
  `exec_module`, the path from `_repo_root()`). K3's pattern (plan line 233)
  holds `exec\(`, which does not match `exec_module(`, and its control fires on
  `subprocess` in `tools/session.py`. That proves the pattern can match one
  word, not that it can see the dynamic-load class K3 claims to check. Probe
  above: the planted `tools/session.py` under `--root` was not run; loaded
  directly, it wrote the marker.
* **Recommended fix.** Add `exec_module|spec_from_file_location|import_module|runpy|compile\(`
  to K3 and require exactly the two known lines in `_encode` (a count, not
  "nothing"). Add a C1 node that runs each mode with `--root` on a tree holding
  a planted `tools/session.py` that writes a marker, and requires no marker.
  Mutant: load the encoder from `root`.

**[BB-SR6] (low) The promise names a key that is not unique.**

* **Plain.** The guide will tell page-builders to key records on `kind` and
  `id`. With `--archive`, a live file and an archived file can share a name, and
  a page keyed that way keeps one and drops the other. For proposals the
  archived one comes second in the output and wins, so a stray archive copy of
  a proposal awaiting your decision would show it as archived.
* **Evidence.** Promise 5 (plan line 286;
  `dev/proposals/archive/2026-10-18-claude-board-as-basis.md:861`). `id` is the
  file name without `.md` (line 76). Output is ordered by `path` (D10, line
  161), and a live proposal's path (`dev/proposals/` then a date) sorts before
  an archived one's (`dev/proposals/archive/`), because a digit sorts before
  `a`.
  No such pair exists at `10ae6428` (checked over both folders with `comm`; the
  listings held 6 live and 54 archived plans, so the instrument ran), so this
  is about a future copy-instead-of-move or a hostile file.
* **Recommended fix.** The guide says `path` is the unique key, and that
  `(kind, id)` is unique among live records only. One node: a live and an
  archived file of the same name give two records with different `path`. This
  corrects a statement of fact in the promise; it removes no outcome.

**[BB-SR7] (low) Folders and pipes named like files, and huge files, have no
criterion.**

* **Plain.** A folder named `x.md/`, which git can store, makes the whole board
  fail today. A named pipe called `x.md`, which git cannot store but a local
  person or an unpacked archive can make, makes it hang. Session-start runs the
  board, so a hang stalls a session. The plan does not say what happens to
  either after it.
* **Evidence.** The probes above. D6 (line 157) covers "an unreadable or
  non-UTF-8 source", and its nodes (line 264) test non-UTF-8 only. The board
  reads each file whole (`tools/board.py:113`) and never recurses: it globs at a
  fixed depth (`tools/board.py:106-108`), so a deep tree is not a case. Link
  loops are BB-SR1.
* **Recommended fix.** In the one check function, the same `lstat` that finds a
  link also requires a regular file for a leaf and a real folder for a folder.
  Anything else is skipped and named like a link (or, if the plan prefers, is a
  D6 failure). Add a folder-named-`x.md` case to C1 and C2, and a pipe case run
  under a timeout. Record in S5 that a very large committed file is read whole,
  as today, and is accepted: it shows itself in the clone, and the tool only
  reads. Optional and not required: opening the leaf with
  `getattr(os, "O_NOFOLLOW", 0)` and `O_NONBLOCK`, then checking `fstat`
  (precedent `tools/_intent/record_io.py:465`), closes the leaf half of the
  race S5 records at no cost.

**[BB-SR8] (low) The example's escaping leaves invisible characters and
unbounded length.**

* **Plain.** The page example makes control and direction-reversing characters
  visible, which is the dangerous class. It leaves invisible "filler"
  characters that the repository's own terminal encoder treats as unsafe, so a
  row can look blank or look like another row. And a value of any length goes
  into the page: the terminal cuts at 48 characters, the data does not.
* **Evidence.** The modelled D7 rule (line 158) above: U+3164, U+115F, U+034F,
  U+FE0F and U+E0100 pass raw, and `tools/session.py:113-139` lists each as
  unsafe. Promise 7 (line 286) is silent on length.
* **Recommended fix.** Default: one sentence in the guide stating the limit
  (invisible fillers are shown raw), with `TestViewExample` feeding U+3164 so the
  stated behaviour is pinned. Copying `encode_display`'s range table into the
  example would make a second table to keep in step, so I do not recommend it.
  Add "any bound on a value's length" to promise 7's list of what is not
  promised, and have the example cut long labels (one line). Add `"` and `'` to
  the `<script>` title case, with a `quote=False` mutant, so attribute escaping
  is pinned too.

**[BB-SR9] (low) `line` counts line breaks the way Python does, not the way an
editor does.**

* **Plain.** The roadmap line number in the data can point a reader at the
  wrong line, because the board treats some invisible characters as line breaks
  that editors and `grep` do not.
* **Evidence.** `tools/board.py:155` uses `splitlines()`, which also breaks on
  form feed, U+2028 and others. Probe: `--maintainer` says line 6, `grep -n`
  says line 4. D5 makes `--json` equal `--maintainer`, and the contract says
  `line` is "the 1-based line of `dev/PLANNING.md`" (line 86).
* **Recommended fix.** Either count `\n` lines in the shared reader (dropping a
  trailing `\r`) and add a case with a form feed and U+2028 ahead of a row, or
  keep the count and say in the guide's field table that it is Python's line
  count. The first changes `--maintainer`'s number only on trees holding those
  characters, which the golden tree does not. The plan should say which it
  chooses.

**[BB-SR10] (low) The guide should say plainly that a status word is not
evidence of a Decision.**

* **Plain.** The guide lists "done" among what the data can show. A page that
  shows `accepted` or `archived` repeats what a file says, and anyone who can
  edit the file can write it. "Never an approval record" is right, but it is not
  tied to the words a reader most wants to trust.
* **Evidence.** Line 288's derivable list and its phrase counts; promise 7's
  "any meaning of free text".
* **Recommended fix.** One sentence in "What the data can and cannot show":
  `accepted`, `archived` and a file under `archive/` say what a file claims or
  where it sits, not that a Decision was recorded, by whom, or that a review
  ran; those are in the artifact's `## Decision` section and its commit. Phrase
  count: `not that a Decision`, at least 1.

### Answers to the five questions

1. **Link handling.** As written, the rule is closed for leaf files,
   `dev/proposals` and `dev/PLANNING.md`, in both modes. It is not yet
   demonstrably closed for `dev`, `archive`, or broken and looping links
   (BB-SR1). The board builds no path from file content: it reads only glob
   results under fixed folders, plus `dev/PLANNING.md`
   (`tools/board.py:100-113`, `:152-155`). As planned, the example and recipes
   open no path taken from the data (the intent join matches `stem` as text), so
   a `..` has nowhere to enter. A linked parent above the root is rightly
   outside the rule, because the root is resolved first; BB-SR1 asks for a test
   that keeps it so. Hard links are not a gap: git records content, not hard
   links, so a cloned tree cannot carry one, and making one needs local write
   access to the tree, where the text could simply be written. **The race
   disposition is sound.** The rule answers a committed link, which exists
   before any check. Winning the race needs local write access during the run,
   and the tool only reads.
2. **Terminal and output injection.** The terminal modes are safe now and stay
   on the one encoder: every cell goes through `encode_display`
   (`tools/board.py:65-85`), the new skip line must as well (line 246), and the
   probe found no raw control or direction byte. The `--json` failure line uses
   Python's `ascii()`, which emits printable ASCII only. It is not a second
   escape table. A one-line comment saying why it does not use the encoder (so
   `--json` loads no other file) would stop a later reader "fixing" it. File
   content cannot break the JSON, and a person running `--json` in a terminal
   sees only printable ASCII (probe). A forged field is untested (BB-SR3), and
   an over-long value passes unbounded (BB-SR8). The page example's `U+XXXX`
   claim holds for every control and direction character I tried, but not for
   invisible fillers (BB-SR8).
3. **Pathological input.** Deep trees are not a case. Link loops are covered
   once BB-SR1 lands. Folders and pipes named like files need a criterion, and
   huge files are an accepted risk to write down (BB-SR7).
4. **The data contract as a trust surface.** The planned statements are the
   right ones: "reading aid", "never an approval record", "not a check that a
   status is current or true", "none named is not nobody needed", and no
   meaning of free text promised. The gaps: skips do not reach a view
   (BB-SR2), the unique key is mis-stated (BB-SR6), and status words are not
   tied to Decisions (BB-SR10).
5. **Frozen files and the lockfile.** The install contract is kept honest. K2
   matches both precedents: only the `"hash"` line of one record moves, and
   `base_hash` stays. The later-edit rule, the twin check, the manifest diff
   and the not-installed test cover the rest, and both new frozen files must be
   final before the ceremony, as the plan says. One sentence is owed to the
   archive's `CHANGELOG.md` entry: an adopter who keeps `dev/` as a link will
   find, after upgrading, that the board reads nothing and prints a skip line.
   The entry should say so, so that the skip line is not their first notice.

### Verdict

**REVISE.** BB-SR1 and BB-SR2 block. They concern the plan's one safety rule
and the one place its report would reach the Maintainer, and in both the
planned tests would pass an implementation that drops content without a word.
Both fixes are test cases, mutants and a sentence, inside accepted outcomes
(the symlinked-artifact rule and the worked example). BB-SR3 to BB-SR10 can be
answered in the same revision. No question for the Maintainer. Status moves to
`revising-plan`.

### What I did not cover

* I did not build `--json` or the example. Every claim about them is read from
  the plan; the escaping and JSON behaviour were modelled in a few lines of
  Python.
* A file name holding bytes that are not UTF-8: APFS refuses such names, so I
  could not make one. Python on Linux carries them as lone surrogates. The
  modelled JSON stays valid ASCII, and the example's category-C step shows them,
  but I did not run that on Linux.
* Windows: whether a committed link arrives as a link or as a small text file
  depends on git's `core.symlinks`. I reasoned about it and did not test it.
  Junctions cannot come from git.
* A link to `/dev/zero`: not run, because it would exhaust this machine's
  memory. The link rule closes it like any other link.
* I did not run the test suite, Bandit, the neutrality gate or
  `verify_integrity.py`.
* I did not read the ordinary Internal pass, which was being written at the same
  time, or check the scope mapping beyond what the security questions needed.
* I did not test D11's reading of `doctrine/lifecycle.md` against hostile
  labels. That file is Maintainer-controlled doctrine, not contributor input.

## Plan review -- Claude Sonnet 5.5 (Internal) -- 2026-10-18

```
Reviewed commit: 10ae64280fbf31bae111077118d421728d5bd0ac
Target: the whole plan as committed (header through Dispositions), read against the accepted proposal's Decision block and scribe's note, Revision 1, and the archived maintainer-attention plan it builds on; checked against the code in tools/board.py and against the open plans that share its files
Prior findings: none of this tier
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Model**: claude-sonnet-5-5

Distance: a fresh session. I wrote neither the proposal nor this plan. This pass
does the scope-and-simplicity job and leaves the security job to the Internal
Security Review (committed at `2e9cf490`). I formed my findings and ran my measurements
before reading that pass, then read it only to avoid duplicate ids; where a
finding overlaps it, I point at it instead of repeating it. All writing
experiments ran in a detached worktree of `10ae6428` in a fresh scratch folder,
under Python 3.13.13, and the worktree is removed.

### In plain terms

**The plan delivers everything the Decision accepted, and drops nothing.** I
traced every Decision bullet and every Revision 1 outcome to a chunk and found
no one removed, narrowed or reworded away. The four additions the author
flagged (D2, D3, D4, D7) are closures of accepted outcomes with two small
exceptions I name below, and none needs the Maintainer's word. There is no
simpler design that still meets the accepted floor.

The plan needs a revision before it is implemented, not because the design is
wrong but because several of its tests are weaker than they read:

* **The "terminal board unchanged" test (BB-PR1).** Built from the shapes the
  plan lists, it let 12 of 33 plausible accidental changes through, even with
  the existing board tests beside it. About a dozen more named shapes close all
  12.
* **The "what waits on you" check (BB-PR2, BB-PR3, BB-PR4).** It compares a
  function with `--maintainer`, but the page the Maintainer will read is never
  compared, a file with no header would crash the example, and the header
  shapes that could make the two differ are not in the test trees.
* **When you get to read the page (BB-PR5).** The plan holds your reading,
  which is the proposal's success test, behind three other plans for no reason
  in the work itself.

None of this needs a Maintainer decision. Each fix is a test shape, a sentence
or a re-ordering inside the accepted outcomes.

### Answers to the two foundational questions

**1. Does the plan deliver what the Decision accepted, all of it?** Yes.

| Decision or Revision 1 item | Where the plan delivers it | Verdict |
|---|---|---|
| "what waits on the Maintainer" is a recipe, not a deferral | C4 recipe and `TestWaitsRecipeAgreesWithMaintainerView` | delivered; the page-level equality is thin (BB-PR4) |
| roadmap rows that declare a wait are in the `/1` data now | C2 `roadmap_waits`, one shared row reader (D5) | delivered |
| the `**In brief**:` prompt in the proposal and plan templates now | C5, all four files | delivered, but timed behind other plans (BB-PR5) |
| the fence warning stays in the terminal view only | no key in C2, `TestFenceStaysInTheTerminalView` in C3 | delivered |
| the guide is read in Cairn's docs, cited by `--help`, not installed | C2 help paragraph, C3 `TestHelpCitesTheGuide` and `TestGuideIsNotInstalled` | delivered |
| the lookup lives in the guide, tested against `doctrine/lifecycle.md` | C3, C4 `TestGuideLookupMatchesLifecycle` | delivered |
| the Scope delta as revised | *Scope delta* section | delivered; dispositions are guards that execute |
| Revision 1: `--json`, the promise, the baseline, the symlink rule, the four "reads headers only" places, the stamped example, finished-plans and intent recipes, triggers, AI-agent note, Boundary B full, the scoped finalize | C1 to C6 | delivered; I walked the plan's own mapping table (lines 351-372) against Revision 1 and found no gap |
| Revision 1's success test: you read a page and can say what needs you and what is in flight | chunk M | delivered, but see BB-PR5 on when |

**Rulings on the four flagged additions.** The author asked review to overrule
any of these; I do not.

* **D2 (a present blank line is `""`, an absent line is `null`): a closure.**
  Revision 1 says "absent is `null`, never `""`". A line that is there with
  nothing after the colon is not absent. The Decision requires the recipe to
  match `--maintainer`, and `--maintainer` lists a blanked Waiting line on
  purpose (`tools/board.py:144`, pinned by
  `test_maintainer_lists_exactly_what_authors_declared`). D2 is the only
  reading that satisfies both. The guide should say it in two plain sentences.
* **D3 (a file with no header is a record with every header key `null`): a
  closure.** Revision 1 says `--json` prints "every proposal and plan". The
  closure has a consequence the plan never tests (BB-PR3).
* **D4 (the link rule reaches folders and `dev/PLANNING.md`, and skips are
  reported): the reach is a closure, the report is a small addition.** Revision
  1's own S1 says the rule closes the case where a link lets an outside file
  supply text. A rule that stopped at the leaf would not close it for a linked
  folder, and not for the roadmap rows the Decision added to the data.
  `is_symlink()` on each component below the resolved root is enough against a
  *committed* link, because git stores a link as a link. The report is a new
  terminal line and a new published key (`skipped_symlinks`) that no accepted
  text names. It is additive and cannot be wrong later without a `/2`, and
  silent skipping reads as an empty board, so I keep it. The Security pass
  (BB-SR2) also wants it on the page. It should be named where the Maintainer
  reads (BB-PR6).
* **D7 (the example shows control and format characters as `U+XXXX`, and its
  footer says "n of m live rows carry an In brief line"): the first is a
  closure, the second is a small addition.** S5 names the direction-override
  class, and the example is where it is closed by construction. The footer
  figure is Revision 1's 30-day signal kept alive after the Decision turned
  the prompt on. Keep it only if the example stays within its line cap
  (BB-PR7); it is the first thing to drop.
* **D1 (`roadmap_read`): a closure.** `--maintainer` says when the roadmap
  file is missing; the data needs the same flag or an empty list reads as
  "nothing waits". Like `skipped_symlinks`, it is a published key the
  proposal's tables do not list (BB-PR6).

**2. Is there a simpler path to the same outcome?** No simpler design meets the
accepted floor. Every candidate I tried loses an accepted outcome: scraping the
terminal table was rejected in the proposal; shipping a view is ruled out by the
Maintainer; importing `board.py` as a module has no contract; leaving the new
keys out saves two keys and costs the Maintainer the visibility the plan exists
for. Four trims cost nothing:

* Move the reading (M) ahead of C5 (BB-PR5). It removes the longest wait in
  the plan and nothing else.
* Keep the waits function once, inside the example, instead of a standalone
  recipe plus an unchanged copy guarded by a syntax-tree equality test
  (BB-PR7).
* Cut the guide's phrase-count tests to the ones that pin a promise
  (BB-PR8). They freeze into a test file at the next re-anchor.
* The footer figure (D7) is optional.

### What I measured

| Probe | Result |
|---|---|
| The golden test, built from the shapes `C1` lists (plan line 243), then 33 one-line breaks of `tools/board.py` copied into a scratch tree, each run through the plain board, `--archive` and `--maintainer` | 13 of 33 break the golden output. The existing `test_replacement_tools.py` catches 15 by itself. Together they catch 19, 2 breaks change no behaviour (tab and double-bullet row handling, because the code already strips after removing the bullet), and **12 survive both**. A tree with about two dozen added shapes kills all 12 (seven with the first group, five with the last five; BB-PR1). |
| The same 12 against 28 historical `dev/` trees from this repository (every 50th commit that touched them) | only the 48-character cut dies; the other 11 survive, so real history cannot stand in for hand-built shapes |
| The plan's two non-vacuity mutants (reword the footer, drop the `board: not listed` line) | both die under any byte comparison, so they show the node compares bytes, not that the tree holds the shapes |
| `frozen_files` in `bootstrap/tests/fixtures/gate_manifest.json` (183 keys) against the live glob in `bootstrap/tests/_gate_manifest.py:339-366` (184, one new file from another plan) | none of the existing files the plan edits is frozen. Control: `bootstrap/tests/test_replacement_tools.py` is in both. The two new files (the test and the fixture) were simulated and both match the live glob, so both freeze at the next re-anchor, as the plan says. |
| `bootstrap/tests/_ast_attest.py verify` against the engine, with the known-new file | 4 CHANGED symbols (`_cmd_adopt_module`, `cmd_upgrade`, `main` in `cli.py`, `seed_gitignore`), the same four the plan names |
| `python bootstrap/verify_integrity.py --target .` | 18 violations, the list the plan quotes; both `tools/board.py` copies hash to `67f705c6...` and the record is verbatim |
| The board follows links today: a plan linked from outside `dev/`, `dev/proposals` linked to an outside folder, `dev/PLANNING.md` linked to an outside file | all three read in the plain board and in `--maintainer` |
| The four templates | `git ls-files` finds exactly four, and `dev/proposals/_template.md` and `dev/plans/_template.md` differ from their `templates/core/` copies, so none is a twin |
| `git ls-tree v0.3.0` against `10ae6428` for `tools/board.py` | absent at the tag, present at the commit |
| `git log --diff-filter=A --name-status -- dev/plans/archive` | 54 add rows for 54 archived plan files, 54 distinct paths. Author and committer dates fall on the same day for all 2427 commits here. |
| The `In brief` share | 2 of 6 live at `72434d73`, 2 of 6 at `10ae6428` |
| D11's reading of the two diagrams in `doctrine/lifecycle.md` (lines 132-141 and 227-239), run as written | 14 status words, and the holders match the guide's planned table; `awaiting-code-review` maps to reviewer only because of the order rule |
| The K3 pattern against `tools/session.py` and `tools/board.py` | fires on the first, silent on the second, as the plan says |

D11 is robust enough. Its failure is loud, not silent: a reworded label turns
the test red. `review-stance-and-lenses` C4 rewrites other sentences of
`doctrine/lifecycle.md` (the "wrong satisfier" paragraph and its search for
"external" and "independen" hits, `dev/plans/review-stance-and-lenses.md` lines
970-993 and 1749-1762) and no diagram label contains those words. The one
cost: a fix to the *heuristic* after the ceremony is an edit to a frozen test;
a fix to the guide's table is not.

### Findings

**[BB-PR1] (medium) The golden test pins the trees the plan lists, and twelve
plausible accidental changes would still pass it.**

* **Plain.** "Unchanged" can only be shown on the trees you try. The plan's
  question 6 asks whether the golden test is real evidence. It is real for the
  layout of the plain board and for several `--maintainer` shapes. It does not
  see a change to the exact rules that decide which status, line or file counts,
  and those are the lines C1 and C2 are about to move.
* **Evidence.** Plan line 243 lists the shapes. Measured as above, the 12
  survivors, each a one-line change to `tools/board.py`: the `awaiting-decision`
  lookahead changed so `awaiting-decision-x` stops listing, or dropped so
  `awaiting-decisions` starts (line 55); a repeated field read first-wins
  instead of last-wins (line 96); a `##x` line ending the header early (line
  92); header lines read unstripped (line 94) or with the field name
  unstripped (line 96); the roadmap marker name unstripped or matched without
  case (line 158); `split("\n")` for `splitlines()` (line 155);
  `is_file()` widened to `exists()` (line 153); the 48-character cut moved
  (line 83); and the `_` skip narrowed to `_template.md` (line 111). C1 moves
  the `_` skip and the `is_dir`/`is_file` calls, and C2 moves the roadmap
  reader and may extend `_header_fields`.
* **Recommended fix.**
  * Add these shapes to the golden tree, and name them in the criterion: the
    status `awaiting-decision-x` (the board lists it) and `awaiting-decisions`
    (it does not); a repeated `**Status**:` line; a `##notaheading` line inside
    a header block; header lines with leading spaces; `**Waiting on Maintainer
    **:` with a space before the closing bold; the marker in lower case in the
    header and in a roadmap row; a 60-character Waiting text; `_notes.md`
    beside `_template.md`; a proposal that mentions `MAINTAINER-GATED`, and a
    plan that mentions only that word; an archived plan carrying a Waiting
    line; a tree with no `dev/PLANNING.md` and one where it is a folder; a
    form feed ahead of a roadmap row (the Security pass, BB-SR9, decides which
    number is right).
  * Run `--maintainer --archive` as a fourth mode.
  * Replace the two footer mutants as the non-vacuity evidence with the 12
    above, or with whichever of them the author can still kill, reported as
    killed, survived or equivalent (the tab and double-bullet row mutants are
    equivalent: `tools/board.py:157` strips after removing the bullet).
  * Keep the C6 old-versus-new comparison on the live tree. It adds a tree the
    author did not build, though real history alone is not enough: 28 sampled
    historical trees killed one of the 12.

**[BB-PR2] (medium) D5 shares the roadmap reader but not the header reader, so
the recipe-versus-`--maintainer` trees cannot see a header difference.**

* **Plain.** The plan's headline test is that the "what waits on you" recipe
  agrees with `--maintainer` "over every shape". Both read the same header
  lines through one function today (`tools/board.py:88-97`, called at lines
  119 and 143). `--json` needs `null` for an absent line, and the terminal
  row builder turns absent into `""` (line 124), so C2 will write a second
  reader for the 11 header keys. Nothing says it must call `_header_fields`.
* **Evidence.** D5 (plan line 156) unifies the roadmap reader only. C2's
  mutation list (line 261) copies the roadmap grammar, not the header grammar.
  C4's trees (line 298) hold no repeated field, no indented header line, no
  `**Waiting on Maintainer **:`, no Waiting line under the first `##`, no
  header-less file, no file without a Status line, and no `_`-prefixed file.
  A JSON reader that is first-wins, or that skips indented lines, passes every
  node as written. The Security pass asks for a forged-name and
  repeated-Status node on the data side (BB-SR3); this is the recipe side of
  the same hole. The plan also calls `awaiting-decision-x` a look-alike (line
  298); the board lists it (the lookahead at line 55 excludes only letters,
  digits and underscore), so the guide's "first word" wording and the test must
  not treat it as not listed. `awaiting-decisions`, `awaiting-decision_x` and
  `awaiting-decision2` are the ones that do not list.
* **Recommended fix.** In C2, require that `--json`, `--maintainer` and the
  plain board read header lines through one function, and add the mutant
  "change that function alone" (all three outputs go red). In C4, add the
  shapes above to the recipe trees and compare `(kind, artifact, reason)`. Fix
  the look-alike wording.

**[BB-PR3] (medium) D3 creates all-`null` records, and no test feeds one to the
recipe or the page.**

* **Plain.** D3 lists a file with no header lines as a record whose status,
  waiting line and every other header key are `null`. A stray `.md` in
  `dev/plans/` or `dev/proposals/` is enough, and the terminal board hides such
  files today. A recipe that matches a pattern against `null`, or an example
  that escapes `null`, fails on the first one. The plan's failure rule then
  keeps the last good page, so the page stops updating and the only sign is its
  older stamp.
* **Evidence.** D3 (line 154) and C2 (line 259) test the data. C4's recipe trees
  (line 298) and `TestViewExample` (line 299) build no header-less file and no
  header with no Status line. Python's `re.match(pattern, None)` raises
  `TypeError`, and `html.escape(None)` raises `AttributeError`. No header-less
  file exists in the live tree today (checked), so the first one would be an
  adopter's. In this tree none of the 138 artifacts, archives included, is
  header-less or lacks a Status line (checked; control: a bare title gives an
  empty header).
* **Recommended fix.** Add both shapes to `TestWaitsRecipeAgreesWithMaintainerView`
  (neither is listed by `--maintainer`, so neither is listed by the recipe) and
  to `TestViewExample` (the page exits 0 and shows the row in "none named" with
  the status shown as unknown). Mutant: the example indexes `status` without a
  null guard. If the author prefers, omit header-less files from `--json` as
  the terminal does; that is simpler, and the null case still arises from a
  header with no Status line, so the tests are owed either way.

**[BB-PR4] (medium) The page's Maintainer group is never compared with
`--maintainer`; only the standalone function is.**

* **Plain.** The proposal's success test is that the page's "needs you" entries
  equal what `--maintainer` lists. The plan tests the recipe function against
  `--maintainer` on many trees, and tests that the example *contains* an
  unchanged copy of the function. Nothing requires the example to *use* it
  for the Maintainer group.
* **Evidence.** The proposal's Evidence section ("its artifact entries in
  'needs you' equal the artifact lines `board.py --maintainer` lists"). Plan
  line 299 asks for one case (an `implementing` plan carrying a wait lands under
  the Maintainer) and a syntax-tree equality of the two function bodies; its
  mutation list has "drop the precedence" and no "group by a different rule".
  The only page-level comparison is the live-tree smoke check (line 308).
* **Recommended fix.** In `TestViewExample`, parse the page's Maintainer group
  and compare its members to `--maintainer`'s artifact lines on at least the
  status-with-note trees and the roadmap rows. Mutant: the example builds the
  Maintainer group from its own status lookup instead of the recipe.

**[BB-PR5] (medium) Your reading of the page, and the whole plan's finish, wait
on three other plans that have nothing to do with the work.**

* **Plain.** The plan's reason for going before `model-mapping-install-path` is
  "it has a user waiting": the hand-kept page goes stale several times a day.
  Then its own order holds your reading of the page behind `neutrality-and-upgrade-slots`
  (implementing), `independent-scientific-check` and `review-stance-and-lenses`
  (both ready to implement, the second with eight chunks). None is near code
  review.
* **Evidence.** C5's gate (plan line 188) is "the three plans ahead have
  archived or reached code review". M follows C5 (line 189), and D13 (line 164)
  says that is because "the page needs the finished board and guide". The page
  needs C1 to C4. The `**In brief**:` prompt changes what authors write later,
  not the page; the page already falls back to the title (line 299). C1 to
  C4 touch none of the three plans' files except disjoint lockfile records and
  one paragraph of `docs/tool-usage.md`. The "three come before this one"
  order is also not settled: `dev/plans/independent-scientific-check.md` lines
  339-341 put the combined plan last, and `dev/plans/review-stance-and-lenses.md`
  line 330 and `dev/plans/neutrality-and-upgrade-slots.md` line 151 put it
  third. The real hazard behind C5's gate is a shared working tree: `git commit
  <path>` commits the whole file, so another agent's unfinished edit to the same
  template would ride in under C5's message. That is checkable directly.
* **Recommended fix.** (1) Move M to follow C4. (2) Replace C5's gate with a
  file-level one: C5 starts when `git status --short` shows none of the four
  templates modified and `python tools/intent.py list` shows no live claim on
  them; it re-reads them as it already says. (3) Say in *Sequencing* that the
  order of the three plans is the Maintainer's and unsettled between the plans'
  own texts, and that C1 to C4 do not depend on it. I agree with the
  recommendation to go before `model-mapping-install-path`: this plan edits no
  engine file and adds no AST symbol, and the files the two share are
  housekeeping plus the one pinned `--maintainer` output.

**[BB-PR6] (low) The text the Maintainer reads does not say the contract grows
by two keys and the page by one figure.**

* **Plain.** The proposal's tables listed three top-level keys. The plan ships
  six, and a key in a published contract is the one thing that cannot be taken
  back inside `/1` (the proposal's own Rationale calls removal the one-way
  door).
* **Evidence.** *In brief* (plan lines 17-37) says the board "names what it
  skipped" but never mentions `roadmap_read` or `skipped_symlinks`, and does
  not mention the footer figure. The author's own sentence at line 374 says
  the Maintainer's allowance "is not assumed for any of them".
* **Recommended fix.** One plain sentence in *In brief*: "The data carries two
  fields you did not see in the proposal, one saying whether the roadmap file
  was read and one listing links the board skipped; the page footer also
  reports how many live items carry a summary line. Each only adds, and none
  can be removed later without a new version." The Security pass notes the
  `CHANGELOG.md` entry must also warn an adopter who keeps `dev/` as a link;
  keep that one.

**[BB-PR7] (low) The example will probably exceed its 80-line cap, and the
waits function exists twice.**

* **Evidence.** I drafted the example with everything C4 requires (the lookup,
  groups, the declared-wait precedence, roadmap rows, `html.escape` plus the
  `U+XXXX` step, the stamp, the advisory sentence, the share figure, the
  not-read message, a single write at the end) and it ran to 73 lines before
  adding the recipe function, which adds about 14. The proposal said "about 50".
  The plan's fallback (line 303) splits the waits group into its own block, and
  C4 then guards two copies of the function with a syntax-tree equality test
  (line 299). The two-subprocess test (line 301) also assumes two literal call
  sites with literal argument lists, which fixes the example's shape.
* **Recommended fix.** Hold the waits function once, in the example, tag that
  block, and have the recipe section link to it. That removes the copy test,
  the 14 duplicated lines and the cap problem. If the author wants the
  standalone recipe for copy-paste, say so and accept the copy test. Drop the
  D7 footer figure first if the example is still long.

**[BB-PR8] (low) Prose pins and host-dependent nodes will freeze into one test
file.**

* **Plain.** The plan's question 5 asks whether freezing the fixture makes a
  needed fix too costly. For the baseline fixture, no: a change to it should
  be a hold. The cost is in the test file, where many nodes pin guide wording
  or depend on the machine, because each later edit to a frozen test is a
  re-anchor only the Maintainer can run.
* **Evidence.** C3 and C4 carry 14 phrase-count checks as written (lines 286-288,
  306: `ignore keys`, `must not overwrite`, `reading aid`, `post-commit hook`,
  `snapshot` and so on). A rewording that keeps the promise turns one red. The
  finished-plans and intent nodes (lines 304-305) create commits, set dates and
  spawn the intent tool, so they depend on git configuration and the
  environment. The v0.3.0 claim (line 289) is "checked from the tree" with
  `git ls-tree v0.3.0`, which fails in a copy that has no tags.
* **Recommended fix.** Keep the structural nodes (tables against output, lookup
  against the lifecycle, help citation resolves, tagged blocks run) and keep
  phrase counts only for the promise statements and the safety sentences; the
  rest is review's job. Scratch repositories use `-c user.name=... -c
  user.email=... -c commit.gpgsign=false` and `GIT_CONFIG_GLOBAL` set to the null
  device, as `bootstrap/tests/test_portable_security_sweeps.py` does. Record the
  `v0.3.0` check in the C3 commit body, not as a node (a skip is a Boundary B
  finding). Name the date the finished-plans recipe reports (author date) and
  set both dates in the test. Run the new file once from another working
  directory before the ceremony.

### Verdict

**REVISE.** BB-PR1 to BB-PR5 are medium; BB-PR6 to BB-PR8 are low. All eight
are answered in the plan's cells without a new mechanism and without the
Maintainer. No accepted outcome is dropped, and none of the flagged additions
needs the Maintainer's word. The Security pass's two blocking findings
(BB-SR1, BB-SR2) stand independently of mine. Status was already
`revising-plan` when I appended, so I left it.

### What I did not cover

* I did not build `--json`, the guide or the example. The 73-line figure is a
  draft I wrote, not the plan's code, and I did not run it.
* I did not review security. I read the Security pass after my findings were
  formed, only to avoid duplicate ids.
* I did not run the full suite, Bandit, `check_cairn.py`, `link_check.py` or the
  neutrality gate. I re-derived the frozen-file, AST, lockfile and archive-date
  figures only.
* I did not read the proposal's External review (`fe0d093c`) in full. I relied on
  the Response, Revision 1 and the Decision, which bind.
* I did not check the other plans beyond the shared-file rows and the lines they
  say about this plan and about `doctrine/lifecycle.md`. `model-mapping-install-path`
  is an uncommitted draft; I did not review it.
* I did not test D11's reading against rewording of the diagram labels, only
  against the labels at `10ae6428` and the text of the plan that edits the file.
* I did not rule on the wording of the *Dispositions* pre-statement. It uses
  `accept` for two watch items that nothing fixes, where the template defines
  `accept` as "fixed in scope"; archive-preparation reads it.
* I did not confirm that "dozens" of tests drive a scaffold install, which is
  the plan's reason for running the full suite. The full run is mandatory here
  anyway (a contract surface and a trust-ceremony surface are touched).

## Response to plan review -- Claude Sonnet 5.5 (author) -- 2026-10-18

This answers the Internal Security Review (`2e9cf490`, BB-SR1 to BB-SR10) and the Internal pass (`98c2cb2b`, BB-PR1 to BB-PR8), both read at `10ae6428`. Neither review section is edited. The plan answers in its cells, as the template says: each row below points at the cell it changed, and no cell is restated here.

**In plain terms.** I accept all eighteen. Nothing the Decision accepted is removed or narrowed; accepted scope stays a floor. Two findings are accepted in a modified form, and I say why in the table: the strengthened code-pattern check (BB-SR5) leaves out `re.compile(`, which a literal reading would trip on; and an entry that is not a link but is not a regular file either (BB-SR7) fails loudly instead of being skipped, which keeps `skipped_symlinks` honest as a list of links. One suggestion is declined with a reason (the optional open-flag hardening in BB-SR7). Two items come from the coordinator, not from the reviews: the build order is the Maintainer's (BB-PR5), and the golden and link tests carry the missing shapes and mutants (BB-SR1 with BB-PR1).

| Finding | Disposition | Cell changed |
|---|---|---|
| **BB-SR1** (blocking) link tests would pass a version that drops broken or looping links silently, and never link `dev` or `archive` | accept | *Plan decisions* D4 (the rule stated once: every component below the resolved root checked by `lstat` before anything follows a link) and D6; *C1*: "The rule, stated once", "The links trees" (ten cases: leaf, `dev/proposals`, `dev/PLANNING.md`, `dev`, `archive` under `--archive`, dangling folder, folder linked to itself, dangling roadmap file, leaf linked to itself, link to a file inside `dev/`), "After C1 none is read", "The rule does not reach too far" (linked parent, `--root` as a link), "One check, called from every reader" (the two surviving mutants added); *Verification* mutation ledger |
| **BB-SR2** (blocking) what the board skipped never reaches the page or the recipe | accept | *C4*: the waits function returns caveats (roadmap not read; each skipped path) and its node compares them with `--maintainer`'s skip lines; `TestViewExample` requires the footer to name each skipped path and say the page is incomplete, with a mutant that drops it; *C3*: "What the data supports" says a non-empty `skipped_symlinks` means incomplete data (standing phrase `skipped_symlinks`); *In brief* item 4; *D4* |
| **BB-SR3** a header line named like a board fact is never tested | accept | *C2*: new bullet "No fact can be forged from inside a file" (`TestRecordFactsComeFromWhereTheFileSits`, the full forged header from the review, with the snake_case-copy mutant); *Verification* ledger |
| **BB-SR4** the suggested post-commit hook runs whatever board a checked-out branch carries | accept | *C4*: "Keeping a page honest" gains the warning and the standing phrase `whatever commit is checked out`; *Security preflight* S5 (the hook bullet) |
| **BB-SR5** "no dynamic code" cannot see the board's one dynamic load, and nothing pins where it loads from | accept, modified | *Acceptance criteria* K3: a second pattern for the dynamic-load words, and a count (exactly the two `_encode` lines) in place of "nothing"; *C1*: `TestBoardLoadsOnlyItsOwnEncoder` (planted `tools/session.py` under `--root`, with the load-from-root mutant); *C2*: the comment beside `ascii()` (D6). **Modified:** the review's `compile\(` alternative matches the three `re.compile(` lines in `tools/board.py` (measured), so the pattern excludes a leading `re.`; the unqualified form is kept as a control to show why. *Found while planning* records it |
| **BB-SR6** the promise names a key that is not unique | accept | *Contract table* (`id` row); *D10*; *C2* "Archives, and the unique key" (a live and an archived file of one name give two records with different `path`); *C3* promise bullet (`path` is the unique key, `(kind, id)` is unique among live records only; standing phrase `live records only`). This corrects a statement of fact in Revision 1's fifth promise and removes no outcome |
| **BB-SR7** folders and pipes named like files, and huge files, have no criterion | accept, modified; the optional hardening declined | *D6*: the same `lstat` that finds a link refuses a non-regular leaf, or a non-folder in the path, before any open, so a pipe cannot hang the board; *C1* "Entries that are not what they should be fail loudly and never hang" (folder `x.md`, `dev/plans` as a file, a pipe under a timeout); *C2* failure bullet; *S5* (a very large committed file is read whole and accepted). **Modified:** such an entry is a failure (the review's stated alternative), not a skip, so `skipped_symlinks` stays a list of links; `dev/PLANNING.md` keeps today's "not a file, so missing" reading, which the golden test pins. **Declined:** the `O_NOFOLLOW`/`O_NONBLOCK` open, as the review marks it optional: it adds a second reader to a verbatim installed tool for a race the plan records as out of scope (*D15*, *Dispositions*, `wontfix`) |
| **BB-SR8** the example leaves invisible fillers and unbounded length | accept; copying the encoder's range table not adopted, as the review recommends | *D7*; *C3* promise bullet ("any bound on a value's length"; standing phrase `length`); *C4* `TestViewExample`: U+3164 shown raw and pinned, a 1,000-character label cut to one line, `"` and `'` in the `<script>` case with the `quote=False` mutant; *S5* (invisible fillers and length) |
| **BB-SR9** `line` counts line breaks as Python does, not as an editor does | accept, second option: keep the count and say so | *Contract table* (`line` row); *D14* (why: choosing the other count would change `--maintainer`'s number and the accepted text says the terminal board does not change); *C2* roadmap bullet (a form feed and U+2028 ahead of a row give the same `line` in both); *C1* golden tree holds that shape; *Found while planning* |
| **BB-SR10** the guide should say a status word is not evidence of a Decision | accept | *C3*: "What the data supports, and does not" (the sentence, standing phrase `not that a Decision`) |
| **BB-PR1** the golden test lets twelve plausible accidents through | accept | *C1*: "The terminal board is pinned before it changes" (all the listed shapes, four modes including `--maintainer --archive`, and the two small trees for a missing and a folder `dev/PLANNING.md`) and "The golden test can fail, for each of twelve plausible accidents" (each of the twelve reported killed, survived or equivalent, with the tab and double-bullet mutants stated equivalent); *C6* keeps the old-versus-new comparison on the live tree; *Verification* ledger first row |
| **BB-PR2** D5 shares the roadmap reader but not the header reader | accept | *D5* and *C2* "Header lines are read by one function" (with the change-it-alone mutant); *C4* recipe trees gain the repeated field, indented header line, spaced `**Waiting on Maintainer **:`, Waiting line below the first `##`, header-less, no-Status and `_`-prefixed files; the look-alike wording is corrected in *C1* and *C4* (`awaiting-decision-x` is listed; `awaiting-decisions`, `awaiting-decision_x` and `awaiting-decision2` are not) |
| **BB-PR3** D3's all-`null` records are never fed to the recipe or the page | accept; D3 kept | *C4*: the recipe trees and `TestViewExample` include a header-less file and a file with no Status line (page still written, row in "none named", status shown as unknown); mutant: index `status` without a null guard |
| **BB-PR4** the page's Maintainer group is never compared with `--maintainer` | accept | *C4* `TestViewExample`: the Maintainer group's members equal `--maintainer`'s artifact lines on the note and roadmap trees; mutant: build the group from the example's own lookup |
| **BB-PR5** the reading of the page waits on three other plans for no reason in the work | accept, with the Maintainer's order and the coordinator's calls | *Sequencing with the other plans*: the build order is stated as the Maintainer's (neutrality, independent check, review-stance, this plan, model-mapping, stewardship), and the recommendation against model-mapping is replaced by "it follows this plan"; *Sequence*: M moves after C4, C1's gate adds "`review-stance-and-lenses` has reached `awaiting-code-review` or later", C5's gate becomes the file-level guard; *Run order*: the sequential rule and its reason (interleaved commits make each plan's Boundary B and code-review ranges ambiguous); *K0* (clean `git status` and no live claim, since all agents share one agent id); *D13*; *M* |
| **BB-PR6** the text the Maintainer reads does not say the contract grows by two keys and the page by one figure | accept | *In brief*: new paragraph "Two fields and one figure beyond the proposal's tables"; *Dispositions*: the `CHANGELOG.md` entry also warns an adopter who keeps `dev/` as a link |
| **BB-PR7** the example will exceed its cap and the waits function exists twice | accept | *C4*: the function is held once, in `view-example`; the recipe section names it and states the rule; three tagged blocks, not four; the syntax-tree copy test is gone; the cap is 110 lines with the share figure the first thing to drop (*D7*) |
| **BB-PR8** prose pins and host-dependent nodes will freeze into one test file | accept | *Reading these criteria*: phrase counts are one-shot except ten named promise and safety phrases; scratch repositories isolate git configuration; *C3*: the `v0.3.0` check goes in the commit body, not a node; *C4*: the finished-plans recipe reports the author date and the test sets both dates; *C6* and *Boundary B*: the new test file is run once from another working directory |

**Also changed, not from a numbered finding.** In *Dispositions* the two watch items that nothing fixes (a stale stamp; a hand-edited page or `--html` requests) were marked `accept`, which the template defines as "fixed in scope"; the Internal pass flagged the wording. They are now `wontfix`, each with its rationale. *Sequencing with the other plans* no longer carries statuses that go stale; they are read at each chunk's start. The header Status is `ready-to-implement`. There is no second round of plan review.

## Implementation verification -- Claude Opus 5.5 -- 2026-10-19

**Boundary B mode**: bounded (scoped under the `12be58d9` certifying-run rule; full suite deferred to the Maintainer's next certifying run)
**Certified by**: pending
**Tested commit**: `47bfece22690913bb309934fcd13d05b806c29c0`
**Reviewed range**: `a6306e00..47bfece2` (commits `a6306e00`, `94fd8cc7`, `f1b61e46`, `b332e727`, `b2a17203`, `47bfece2`)
**Interpreter/runtime**: Python 3.13.12 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`), pytest 8.4.2, macOS (`PYTHONDONTWRITEBYTECODE=1`, detached `git worktree` at `47bfece2`)
**Pre-run state**: clean (`git status --short` empty in the detached `git worktree`)
**Post-run state**: clean (`git status --short` empty in the detached `git worktree`)

**Touched surfaces and why the scoped run covers them (pending the certifying run)**:

* `tools/board.py` and `templates/skills/_lib/board.py` (C1, C2), plus one scoped lockfile hash update (`dev/.cairn/cairn-lock.yml`). Covered by `bootstrap/tests/test_board_json_contract.py` (25 nodes), `bootstrap/tests/test_replacement_tools.py` (unedited), `bootstrap/tests/test_notice_install.py`, `bootstrap/tests/test_security_lint.py`, `bootstrap/tests/test_security_check.py`, `bootstrap/tests/test_skills_self_heal.py`, `bootstrap/tests/test_skills_upgrade.py`, `bootstrap/tests/test_verify_integrity.py`, and `bootstrap/tests/test_cairn_prefix_links.py`.
* `bootstrap/tests/fixtures/board_json_v1_baseline.json` (C2) and `docs/build-a-board-view.md` + `docs/tool-usage.md` (C3, C4). Covered by `bootstrap/tests/test_board_json_contract.py`, `bootstrap/tests/test_cairn_prefix_links.py`, `bootstrap/tests/test_doc_governance.py`, `bootstrap/tests/test_check_cairn_content.py`, `bootstrap/tests/test_check_cairn_counts.py`, `bootstrap/tests/test_link_check_exclusions.py`, `bootstrap/tests/test_quality_gate_neutrality.py`, and `bootstrap/tests/test_intents_tool.py`.
* `dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md`, `dev/plans/_template.md`, `templates/core/dev/plans/_template.md` (C5). Covered by `bootstrap/tests/test_board_json_contract.py` (`TestTemplatesAskForTheLineTheBoardReads`) and all 15 template-reading test files found across `bootstrap/tests/` (`test_scope_reduction_trap.py`, `test_scaffold.py`, `test_documentation_plan_module.py`, `test_claim_check_module.py`, `test_quickstart_sequence.py`, `test_review_stance_in_shipped_files.py`, `test_certifying_run_rule.py`, `test_scientific_check_guidance_ships.py`, `test_core_dev_folders.py`, `test_incident_trackers_module.py`, `test_install_module.py`, `test_session_routines.py`, `test_trigger_evaluation_action.py`, `test_verification_boundaries.py`, plus `test_doc_governance.py`). Because `tools/board.py` is a verbatim installed tool, the four templates are rendered by scaffold installs, and two new frozen-pattern files (`bootstrap/tests/test_board_json_contract.py`, `bootstrap/tests/fixtures/board_json_v1_baseline.json`) join the 0.4 re-anchor batch, the full-suite requirement is satisfied by the next Maintainer certifying run (`**Certified by**: pending`) per `AGENTS.md` (`12be58d9`).

| Command | Exit | Outcomes | Elapsed |
|---|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q --quality-gate-shuffle-seed=0` over the 29 mapped test files (`test_board_json_contract.py`, `test_replacement_tools.py`, `test_notice_install.py`, `test_security_lint.py`, `test_security_check.py`, `test_skills_self_heal.py`, `test_skills_upgrade.py`, `test_verify_integrity.py`, `test_cairn_prefix_links.py`, `test_doc_governance.py`, `test_check_cairn_content.py`, `test_check_cairn_counts.py`, `test_link_check_exclusions.py`, `test_quality_gate_neutrality.py`, `test_intents_tool.py`, `test_scope_reduction_trap.py`, `test_scaffold.py`, `test_documentation_plan_module.py`, `test_claim_check_module.py`, `test_quickstart_sequence.py`, `test_review_stance_in_shipped_files.py`, `test_certifying_run_rule.py`, `test_scientific_check_guidance_ships.py`, `test_core_dev_folders.py`, `test_incident_trackers_module.py`, `test_install_module.py`, `test_session_routines.py`, `test_trigger_evaluation_action.py`, `test_verification_boundaries.py`) | 0 | 2,843 passed, 0 failed, 0 skipped, 3 warnings | 59.37s |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | `[neutrality] fail=0 info=56` (unchanged from `a6306e00` baseline `fail=0 info=56`); `[redundancy] fail=0 info=0` | 1.20s |
| `python scripts/link_check.py docs/build-a-board-view.md docs/tool-usage.md dev/proposals/_template.md templates/core/dev/proposals/_template.md dev/plans/_template.md templates/core/dev/plans/_template.md` | 0 | `OK -- 6 Markdown file(s) scanned; no issues` | 0.12s |
| `python scripts/claim_check.py <each of the 6 edited docs and dev/plans/board-as-basis.md>` | 0 | `OK, no claim-check flags` on all 7 files | 0.35s |
| `python scripts/verify_counts.py docs/tool-usage.md` | 0 | `1 ok, 0 failed, 0 skipped` (`claim_check_watch_file_lines = 1704`) | 0.08s |
| `cd /tmp && PYTHONDONTWRITEBYTECODE=1 python -m pytest -q <worktree>/bootstrap/tests/test_board_json_contract.py` | 0 | 25 passed in 1.65s (non-repo working directory) | 2.08s |

**Non-pass disposition**:

* Zero skips, zero xfails, zero xpasses, and zero failures in the 29-file scoped Boundary B pytest run (`2,843 passed`).
* `bootstrap/tests/test_ast_attest.py` (probed separately at `a6306e00` and `47bfece2`): `2 failed, 28 passed` identically at both commits for earlier work (`neutrality-and-upgrade-slots` / `independent-scientific-check` / `review-stance-and-lenses`) awaiting the single combined 0.4 re-anchor ceremony. Zero bytes under `bootstrap/_scaffold/` or `bootstrap/scaffold.py` changed in this plan.

**Collected node IDs of `bootstrap/tests/test_board_json_contract.py` (`pytest --collect-only -q`, 25 nodes)**:

1. `bootstrap/tests/test_board_json_contract.py::TestTerminalBoardIsUnchanged::test_terminal_modes_match_parent_golden_output`
2. `bootstrap/tests/test_board_json_contract.py::TestSymlinkedSourcesAreNotRead::test_symlinked_sources_are_skipped_and_named_in_all_modes`
3. `bootstrap/tests/test_board_json_contract.py::TestSymlinkedSourcesAreNotRead::test_symlinked_root_or_parent_above_root_is_read_normally`
4. `bootstrap/tests/test_board_json_contract.py::TestSymlinkedSourcesAreNotRead::test_non_regular_entries_fail_loudly_without_hanging`
5. `bootstrap/tests/test_board_json_contract.py::TestBoardLoadsOnlyItsOwnEncoder::test_planted_session_module_under_root_is_never_executed`
6. `bootstrap/tests/test_board_json_contract.py::TestSchemaOneBaselineHolds::test_schema_one_baseline_keys_and_types_hold`
7. `bootstrap/tests/test_board_json_contract.py::TestRecordFactsComeFromWhereTheFileSits::test_header_lines_cannot_forge_location_or_schema_fields`
8. `bootstrap/tests/test_board_json_contract.py::TestRecordFactsComeFromWhereTheFileSits::test_all_record_values_and_absent_vs_blank_and_headerless_files`
9. `bootstrap/tests/test_board_json_contract.py::TestOutputIsDeterministic::test_archives_unique_path_key_and_deterministic_ascii_json`
10. `bootstrap/tests/test_board_json_contract.py::TestRoadmapWaitsAndSkippedSymlinksInJson::test_roadmap_waits_match_maintainer_and_share_one_reader`
11. `bootstrap/tests/test_board_json_contract.py::TestRoadmapWaitsAndSkippedSymlinksInJson::test_json_failures_and_usage_errors_write_nothing_to_stdout`
12. `bootstrap/tests/test_board_json_contract.py::TestGuideAndOutputAgree::test_guide_opening_section_is_plain_prose_and_defines_terms`
13. `bootstrap/tests/test_board_json_contract.py::TestGuideAndOutputAgree::test_guide_field_tables_and_standing_phrases_match_output_and_baseline`
14. `bootstrap/tests/test_board_json_contract.py::TestGuideLookupMatchesLifecycle::test_guide_lookup_table_matches_lifecycle_diagrams`
15. `bootstrap/tests/test_board_json_contract.py::TestGuideLookupMatchesLifecycle::test_view_example_lookup_matches_guide_table_and_lifecycle`
16. `bootstrap/tests/test_board_json_contract.py::TestFenceStaysInTheTerminalView::test_fence_mentions_only_point_to_terminal_view_and_no_code_block_computes_one`
17. `bootstrap/tests/test_board_json_contract.py::TestHelpCitesTheGuide::test_help_cites_cairn_guide_path_and_token_resolves`
18. `bootstrap/tests/test_board_json_contract.py::TestGuideIsNotInstalled::test_guide_is_absent_from_scaffold_manifest`
19. `bootstrap/tests/test_board_json_contract.py::TestWaitsRecipeAgreesWithMaintainerView::test_waits_recipe_matches_maintainer_view_across_all_shapes`
20. `bootstrap/tests/test_board_json_contract.py::TestViewExample::test_view_example_structure_lookup_and_ast`
21. `bootstrap/tests/test_board_json_contract.py::TestViewExample::test_view_example_renders_groups_escaping_footer_and_preserves_page_on_failure`
22. `bootstrap/tests/test_board_json_contract.py::TestFinishedPlansRecipe::test_finished_plans_recipe_uses_author_date_and_excludes_proposals_and_edits`
23. `bootstrap/tests/test_board_json_contract.py::TestIntentJoinRecipe::test_intent_join_matches_by_stem_only_and_canned_shape_matches_real_tool`
24. `bootstrap/tests/test_board_json_contract.py::TestTemplatesAskForTheLineTheBoardReads::test_proposal_templates_carry_in_brief_below_the_rule`
25. `bootstrap/tests/test_board_json_contract.py::TestTemplatesAskForTheLineTheBoardReads::test_plan_templates_carry_in_brief_below_the_rule_and_keep_waiting_above_it`

**Plan-specific acceptance commands**:

* **Old-versus-new comparison of the terminal board**: `git show a6306e00:tools/board.py` placed beside `tools/board.py` at `47bfece2` and run across all four terminal modes (`plain`, `--archive`, `--maintainer`, `--maintainer --archive`) on both the live tree and C1's golden tree: byte-identical (`cmp` exits 0 on all runs).
* **Not-touched list**: `git diff-tree --no-commit-id --name-only -r <commit> -- bootstrap/_scaffold bootstrap/scaffold.py doctrine AGENTS.md templates/core/AGENTS.md tools/session.py bootstrap/UPGRADE.md bootstrap/tests/test_replacement_tools.py bootstrap/tests/fixtures/gate_manifest.json` across all commits of this plan (`a6306e00`, `94fd8cc7`, `f1b61e46`, `b332e727`, `b2a17203`, `47bfece2`): empty. No existing frozen file was edited; the only paths matching frozen patterns are the two new files (`bootstrap/tests/test_board_json_contract.py`, `bootstrap/tests/fixtures/board_json_v1_baseline.json`).
* **Manifest diff**: `python bootstrap/scaffold.py --manifest` at `a6306e00` and `47bfece2` are byte-identical (78 lines; zero occurrences of `build-a-board-view`).
* **Twins and lockfile**: `cmp tools/board.py templates/skills/_lib/board.py` exits 0; `dev/.cairn/cairn-lock.yml` record for `tools/board.py` equals `sha256:203c5919db24aa195e5cf9a1fdd30c52be4a3d2cd2b7d03c27118df6dd1bfa34`; `python bootstrap/verify_integrity.py --target .` lists the same 18 modified files as at `a6306e00` and does not list `tools/board.py`.
* **Worked example (`view-example`) and recipe counts at `47bfece2`**:
  * `view-example` tagged block length: `101` lines (within the 110-line cap).
  * `waiting_on_maintainer(doc)` on the live tree at `47bfece2`: 2 declared roadmap items (`dev/PLANNING.md:454`, `dev/PLANNING.md:794`), 0 caveats (`roadmap_read: true`, `skipped_symlinks: []`).
  * `finished_plans(root)` on the live tree at `47bfece2`: `55` archived plans (`55 == 55` committed files under `dev/plans/archive/`).
  * Generated page saved at `/tmp/cairn-board-view.html` from commit `47bfece22690913bb309934fcd13d05b806c29c0`: group counts `Maintainer (2)`, `author (0)`, `reviewer (1)`, `implementer (2)`, `none named (3)`; footer reports `1 of 6 live rows carry an In brief line.`
  * **Chunk M reading**: awaiting Maintainer response (`**Waiting on Maintainer**: read the generated board page` set in the header; `/tmp/cairn-board-view.html` generated from `47bfece22690913bb309934fcd13d05b806c29c0`).

**Mutation ledger summary (81 mutants across C1–C5, each run in a detached `git worktree` beside an unmutated `rc=0` control run)**:

* **C1 (23 mutants — 21 killed, 2 measured equivalent)**:
  * Golden-tree breaks `M1`–`M12` + two footer rewordings (`M13`, `M14`): all 14 killed (`rc=1`) by `TestTerminalBoardIsUnchanged` (and `M13` also by `test_replacement_tools.py`).
  * Equivalence checks `E1` (tab after bullet before marker) and `E2` (double bullet before marker): both measured equivalent (`rc=0`) through the real entry point because `_waiting` strips whitespace and leading `-*` after removing the outer bullet.
  * Link/regular-file/encoder breaks `M15`–`M21` (drop artifact link check; check only leaf/`dev/proposals`/`dev/plans` skipping `dev` and `archive`; `if not base.is_dir(): continue` before link check; drop `dev/PLANNING.md` link check; check parent folders above `--root`; read leaf before `lstat`; load encoder from `--root`): all 7 killed (`rc=1`) by `TestSymlinkedSourcesAreNotRead` and `TestBoardLoadsOnlyItsOwnEncoder`.
* **C2 (33 mutants — 33 killed)**:
  * Baseline key deletions (`M-BL-1`..`M-BL-20`, all 6 top-level keys, 12 artifact record keys, 2 roadmap_waits keys): all 20 killed (`rc=1`) by `TestSchemaOneBaselineHolds`.
  * Functional breaks `M-C2-1`..`M-C2-13` (`_header_fields` first-wins; copy raw snake_case header keys; rename `status` to `state` in code + guide; emit `""` for absent header; emit `null` for blank Waiting line; `sort_keys=False`; `ensure_ascii=False`; include archive without `--archive`; key by `id` instead of `path`; print partial stdout before failure; accept `--json --maintainer`; alter `_roadmap_waits` grammar; add `fences_without_wait` key): all 13 killed (`rc=1`).
* **C3 (3 mutants — 3 killed)**:
  * `M-C3-1` (change `revising` holder in guide table to `reviewer`): killed (`rc=1`) by `TestGuideLookupMatchesLifecycle`.
  * `M-C3-2` (remove `--help` JSON guide paragraph): killed (`rc=1`) by `TestHelpCitesTheGuide`.
  * `M-C3-3` (add `fences_without_wait` to guide table): killed (`rc=1`) by `TestGuideAndOutputAgree`.
* **C4 (18 mutants — 18 killed)**:
  * `M-C4-1`..`M-C4-10` in `view-example` (change lookup entry; remove `html.escape`; `quote=False`; remove category-C control step; drop precedence; omit commit stamp; write output before board finishes; drop skipped-paths footer; drop fence advisory sentence; build Maintainer group from `HOLDER_BY_STATUS` instead of `waiting_on_maintainer`; drop null guard on `status`): all 10 killed (`rc=1`) by `TestGuideLookupMatchesLifecycle` and `TestViewExample`.
  * `M-C4-11`..`M-C4-15` in `waiting_on_maintainer` (exact status match; treat blank wait as absent; list archived rows; drop roadmap half; drop skip caveats; drop `awaiting-decision-x`): all 5 killed (`rc=1`) by `TestWaitsRecipeAgreesWithMaintainerView`.
  * `M-C4-16`..`M-C4-18` in `finished-recipe` and `intent-recipe` (include `dev/proposals/archive`; join intents by file overlap; match empty `stem`): all 3 killed (`rc=1`) by `TestFinishedPlansRecipe` and `TestIntentJoinRecipe`.
* **C5 (4 mutants — 4 killed)**:
  * `M-C5-1`..`M-C5-4` (rename `**In brief**:` to `**In-brief**:` in `dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md`, `dev/plans/_template.md`, and `templates/core/dev/plans/_template.md`, one at a time): all 4 killed (`rc=1`) by `TestTemplatesAskForTheLineTheBoardReads`, each failure naming the mutated template file.

**Known omissions**:

* Full-suite execution (`CAIRN_FULL_SUITE=1`) is omitted per `AGENTS.md` (`12be58d9`) and explicit Maintainer instruction; `**Certified by**: pending` awaits the Maintainer's next certifying run.
* Chunk M's Maintainer reading of `/tmp/cairn-board-view.html` is open (`**Waiting on Maintainer**: read the generated board page`); per *Sequence*, C6 and code review proceed while archive waits on the Maintainer's answer.

