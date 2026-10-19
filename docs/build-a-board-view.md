# Build a board view

## Why a view is built, never hand-kept

A **view** is any web page, table, or summary panel built from the board's output so a reader can see at a glance what needs attention and what is in flight across `dev/`. When you run `python tools/board.py --json`, the board prints its facts as **JSON** (JavaScript Object Notation, a plain-text data format of named fields and lists that standard-library tools in any language can read without scraping a terminal table). Cairn ships no view, no `--html` flag, and no bundled page script, because every research team wants a slightly different layout while relying on the same underlying facts. Any page you build from this guide is regenerated straight from the repository's files whenever you want a fresh look and is never hand-kept: if a row on the page looks wrong, you fix the header line in the proposal or plan and regenerate the page.

## Field reference

`python tools/board.py --json` emits one JSON object on standard output. It reads the `# ` title line and the `**Field**: value` header lines above the first `## ` heading of each proposal and plan, plus the rows of [`dev/PLANNING.md`](../dev/PLANNING.md) that carry the `**Waiting on Maintainer**:` marker in row form. It derives no value.

### Top-level keys

| Key | Type | Holds |
|---|---|---|
| `schema` | string | Always `"cairn-board/1"`, present even when `dev/` is absent or empty |
| `includes_archive` | boolean | Whether `--archive` was passed, so an empty archive list is not read as no archived work existing |
| `artifacts` | array | Every proposal and plan record, ordered by `path` |
| `roadmap_waits` | array | Every `dev/PLANNING.md` row that declares a wait on the Maintainer |
| `roadmap_read` | boolean | Whether `dev/PLANNING.md` was read as a regular file, so an empty `roadmap_waits` list is not read as nothing waiting when the file is missing or skipped |
| `skipped_symlinks` | array | Sorted repo-relative paths (`/` separators) not read because they are, or sit under, a symbolic link (broken and self-pointing links included) |

### Artifact records

| Key | Type | Source |
|---|---|---|
| `kind` | string | `"proposal"` or `"plan"`, from the directory the file sits in |
| `id` | string | The file name without `.md`; unique among live records only, so a consumer keys on `path` |
| `path` | string | Repo-relative path with `/` separators |
| `archived` | boolean | `true` when the file sits under `archive/`, `false` otherwise |
| `title` | string or null | The first `# ` line above the first `## ` heading, or `null` when absent |
| `in_brief` | string or null | The `**In brief**:` header line above the first `## ` heading |
| `status` | string or null | The `**Status**:` header line, as written |
| `review` | string or null | The `**Review**:` header line, as written |
| `plan_review` | string or null | The `**Plan review**:` header line, as written |
| `opened` | string or null | The `**Opened**:` header line, as written |
| `source_proposal` | string or null | The `**Source proposal**:` header line, as written |
| `waiting_on_maintainer` | string or null | The `**Waiting on Maintainer**:` header line, as written |

### Roadmap waits

| Key | Type | Source |
|---|---|---|
| `line` | integer | The 1-based line number of `dev/PLANNING.md` as Python's `str.splitlines()` counts it (a form feed or `U+2028` counts as a line break, so an editor or `grep -n` may number lines differently) |
| `text` | string | What follows `**Waiting on Maintainer**:` on that row (`""` when blank) |

## What will not change

1. **Additive only within `cairn-board/1`.** Within `"cairn-board/1"`, Cairn only adds keys; no existing top-level, artifact-record, or roadmap-wait key is removed, renamed, or retyped.
2. **Incompatible changes move the schema version.** Any breaking change to an existing key or type uses `"cairn-board/2"` and is announced in [`CHANGELOG.md`](../CHANGELOG.md).
3. **How consumers read the version and unknown fields.** Consumers read `schema` first, refuse any version they do not know, and ignore keys they do not recognize so additive changes within `"cairn-board/1"` never break an existing script.
4. **Absent versus blank, and raw strings.** An absent header line is `null`, whereas a present blank line (a field name and colon with nothing after it) is the empty string `""`; `title` and `in_brief` never stand in for each other; and strings are emitted as raw values without escaping for HTML, Markdown, or a terminal.
5. **Determinism and unique keys.** Under one producer version, the same files give the same ASCII bytes (sorted keys, and no timestamp, commit hash, or machine path); row order is not promised; `path` is the unique key across the whole document, whereas `(kind, id)` is unique among live records only because an archived file under `archive/` can share an `id` with a live one.
6. **Failure writes nothing to standard output.** A failure writes nothing to standard output and exits nonzero, so a script that regenerates a page must not overwrite an existing page when the board fails.
7. **What is not promised.** Cairn does not promise the terminal layout, that any optional header field is present, any semantic meaning of free-text values beyond what the author wrote, or any bound on a value's length.

## Grouping by who acts next

The board reports header facts and does not emit a holder key. A view that groups live proposals and plans by whose move it is applies the lifecycle lookup from [`doctrine/lifecycle.md`](../doctrine/lifecycle.md) on the consumer side.

### The lookup

The lookup key is the **first word** of `status` (the leading run of lowercase letters and hyphens), matched against the table below, because real headers often carry notes after the status word (such as `archived -- C1-C9 all landed`).

**Precedence rule:** a declared wait overrides the status word. Any live record whose `waiting_on_maintainer` is not `null` (including `""`) groups under `Maintainer` whatever its `status` says, and so does any live record whose `status` starts with `awaiting-decision` not followed by a letter, digit, or underscore.

This lookup is the doctrine's stage table, not a check that a status is current or true. A holder of `"none named"` means the lifecycle diagram names no next holder for that word (for example, `accepted` before a plan opens, or `archived`), not that nobody is needed.

| Status word (first word) | Holder |
|---|---|
| `awaiting-review` | reviewer |
| `revising` | author |
| `awaiting-decision` | Maintainer |
| `accepted` | none named |
| `rejected` | none named |
| `superseded` | none named |
| `awaiting-plan-review` | reviewer |
| `revising-plan` | author |
| `ready-to-implement` | implementer |
| `implementing` | implementer |
| `awaiting-code-review` | reviewer |
| `revising-code` | implementer |
| `ready-to-archive` | none named |
| `archived` | none named |
| anything else, including the retired words `proposed`, `reviewed` and `revised` | none named |

## What the data can and cannot show

From the `"cairn-board/1"` document, a view can show **what needs you** (the Maintainer group and `roadmap_waits`), **what is in flight by holder** (`author`, `reviewer`, `implementer`), **what is queued** (`accepted`, `ready-to-implement`), and **what is done** (`archived` when `--archive` is passed).

Several things are **not derivable** from the board's data:

* **"Blocked" and "an agent is working right now" are not derivable.** An external blocker is visible only when an author writes a `**Waiting on Maintainer**:` line, and whether an agent process is actively editing a file is local working-tree state outside git-committed headers.
* **General roadmap rows without a wait marker are not in the data.** `roadmap_waits` includes only `dev/PLANNING.md` rows that carry `**Waiting on Maintainer**:` in row form. Adding unmarked roadmap rows has a single revival condition: the Maintainer asks for general roadmap items on a view once the wait marker has had real use.
* **The fence advisory stays in the terminal view only.** Active plans that mention `MAINTAINER-GATED` or `MAINTAINER-ONLY` in their body without declaring a wait are not a key in the JSON data and not a recipe; run `python tools/board.py --maintainer` in the terminal to see that advisory line.

Keep three trust boundaries in mind when reading any generated page:

1. **A view is a reading aid, never an approval record.** Any contributor who can edit a file under `dev/` can write any status word or header line in it.
2. **A status word is a claim, not proof.** `accepted`, `archived`, and a file sitting under `archive/` say what a file claims or where it sits, not that a Decision was recorded, by whom, or that a review ran; those live in the artifact's `## Decision` section and its git commit history.
3. **Incomplete data must be shown visibly.** A non-empty `skipped_symlinks` list, or `roadmap_read` being `false`, means the board could not read part of `dev/` and the data is incomplete; a view must show that warning on the page so a skipped folder or missing roadmap file never looks like an empty board.

## Reaching it and running it

Adopters do not receive `docs/` when they scaffold or upgrade a project. This guide is read in Cairn's published documentation (`cairn/docs/build-a-board-view.md`, cited at the bottom of `python tools/board.py --help`).

The board tool itself arrived after Cairn 0.3.0, and `--json` arrived after that. In an older install, `tools/board.py` may be absent altogether, or running `python tools/board.py --json` may exit with code `2` and `unrecognized arguments: --json`. Either result means the project has an older Cairn install; follow [`bootstrap/UPGRADE.md`](../bootstrap/UPGRADE.md) for the upgrade path.
