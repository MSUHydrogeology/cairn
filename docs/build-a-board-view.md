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


## Worked example: a regenerated HTML board page

The script below uses only the Python standard library. It runs `tools/board.py --json` and `git rev-parse HEAD`, groups live items in the order `Maintainer`, `author`, `reviewer`, `implementer`, `none named` with counts, prints the raw `status` beside each row, uses `in_brief` (or `title` when `in_brief` is null or empty) as the label, and writes the page only after both commands succeed.

Every free-text string is flattened to one line, truncated to 120 characters, passed through `html.escape(..., quote=True)`, and then scanned so any Unicode control or format character (category starting with `C`, such as `U+001B` or `U+202E`) is shown as a visible `U+XXXX` code. Invisible filler characters outside category `C` (`U+3164`, `U+115F`, `U+034F`, `U+FE0F`, `U+E0100`) pass through raw.

```python view-example
import html, json, re, subprocess, sys, unicodedata
from pathlib import Path

HOLDER_BY_STATUS = {
    "awaiting-review": "reviewer",
    "revising": "author",
    "awaiting-decision": "Maintainer",
    "accepted": "none named",
    "rejected": "none named",
    "superseded": "none named",
    "awaiting-plan-review": "reviewer",
    "revising-plan": "author",
    "ready-to-implement": "implementer",
    "implementing": "implementer",
    "awaiting-code-review": "reviewer",
    "revising-code": "implementer",
    "ready-to-archive": "none named",
    "archived": "none named",
}
GROUPS = ("Maintainer", "author", "reviewer", "implementer", "none named")
_DECISION_RE = re.compile(r"^awaiting-decision(?![A-Za-z0-9_])")
_FIRST_WORD_RE = re.compile(r"^[a-z-]+")
_KIND_ORDER = {"proposal": 0, "plan": 1}


def _clean(value: object, limit: int = 120) -> str:
    one_line = " ".join(str(value or "").splitlines())
    if len(one_line) > limit:
        one_line = one_line[: limit - 1] + "\u2026"
    escaped = html.escape(one_line, quote=True)
    return "".join(
        f"U+{ord(ch):04X}" if unicodedata.category(ch).startswith("C") else ch
        for ch in escaped
    )


def waiting_on_maintainer(doc: dict) -> tuple[list[tuple[str, str, str, str]], list[str]]:
    if doc.get("schema") != "cairn-board/1":
        raise ValueError(f"Unsupported schema: {doc.get('schema')!r}")
    entries: list[tuple[str, str, str, str]] = []
    live = sorted(
        (a for a in doc["artifacts"] if not a["archived"]),
        key=lambda a: (_KIND_ORDER.get(a["kind"], 9), a["id"]),
    )
    for art in live:
        status = art.get("status") or ""
        wait = art.get("waiting_on_maintainer")
        decision = bool(_DECISION_RE.match(status))
        if decision or wait is not None:
            reason = "awaiting-decision" if decision else "declared"
            entries.append((art["kind"], art["id"], reason, wait or ""))
    for row in doc["roadmap_waits"]:
        entries.append(("roadmap", f"dev/PLANNING.md:{row['line']}", "declared", row["text"]))
    caveats = [] if doc["roadmap_read"] else ["dev/PLANNING.md was not read"]
    caveats.extend(f"skipped (symbolic link, not read): {rel}" for rel in doc["skipped_symlinks"])
    return entries, caveats


def render_page(doc: dict, commit: str) -> str:
    waits, _ = waiting_on_maintainer(doc)
    maint_keys = {(k, art) for k, art, _, _ in waits if k != "roadmap"}
    grouped: dict[str, list[str]] = {g: [] for g in GROUPS}
    live = sorted(
        (a for a in doc["artifacts"] if not a["archived"]),
        key=lambda a: (_KIND_ORDER.get(a["kind"], 9), a["id"]),
    )
    for art in live:
        label = _clean(art.get("in_brief") or art.get("title") or art["id"])
        raw_status = _clean(art.get("status") or "status unknown")
        if (art["kind"], art["id"]) in maint_keys:
            holder = "Maintainer"
        else:
            m = _FIRST_WORD_RE.match(art.get("status") or "")
            mapped = HOLDER_BY_STATUS.get(m.group(0) if m else "", "none named")
            holder = "none named" if mapped == "Maintainer" else mapped
        grouped[holder].append(f"<li><code>{_clean(art['id'])}</code> ({raw_status}) &mdash; {label}</li>")
    for k, target, reason, text in waits:
        if k == "roadmap":
            grouped["Maintainer"].append(f"<li><code>{_clean(target)}</code> ({_clean(reason)}) &mdash; {_clean(text)}</li>")
    sections = [f"<section><h2>{g} ({len(grouped[g])})</h2><ul>{''.join(grouped[g])}</ul></section>" for g in GROUPS]
    brief_n = sum(1 for a in live if a.get("in_brief"))
    foot = [
        f"<p>Built from commit <code>{_clean(commit.strip())}</code> (working tree).</p>",
        f"<p>{brief_n} of {len(live)} live rows carry an In brief line.</p>",
        "<p>Advisories for plans with a fence and no declared wait are not shown; run <code>python tools/board.py --maintainer</code>.</p>",
    ]
    if not doc["roadmap_read"]:
        foot.append("<p>Page incomplete: dev/PLANNING.md was not read.</p>")
    if doc["skipped_symlinks"]:
        foot.append(f"<p>Page incomplete: skipped symbolic links: {', '.join(_clean(s) for s in doc['skipped_symlinks'])}</p>")
    return f"<!doctype html><meta charset='utf-8'><title>Cairn Board</title>{''.join(sections)}<footer>{''.join(foot)}</footer>\n"


def build_view(out_path: Path) -> None:
    board_proc = subprocess.run([sys.executable, "tools/board.py", "--json"], capture_output=True, text=True, check=True)
    git_proc = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
    out_path.write_text(render_page(json.loads(board_proc.stdout), git_proc.stdout), encoding="utf-8")


if __name__ == "__main__":
    build_view(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("board-view.html"))
```

## Recipes

### What waits on the Maintainer

An item waits on the Maintainer when it is a live (`not archived`) proposal or plan whose `status` starts with `awaiting-decision` not followed by a letter, digit, or underscore (`^awaiting-decision(?![A-Za-z0-9_])`), or whose `waiting_on_maintainer` is not `null` (a blank line is `""` and still counts as declared); or when it is a marked row in `roadmap_waits`. The result also reports when `dev/PLANNING.md` was not read (`roadmap_read` is `false`) and lists every skipped path in `skipped_symlinks`.

The function `waiting_on_maintainer(doc)` in `view-example` above implements that exact rule once so the page and any standalone script stay in step:

```python
doc = json.loads(subprocess.check_output([sys.executable, "tools/board.py", "--json"], text=True))
entries, caveats = waiting_on_maintainer(doc)
```

### Plans finished by date

This recipe lists archived plans from git history, reporting the **author date** (`%ad`) of the commit that added each file under `dev/plans/archive/`, newest first, one entry per plan. It covers plans only, because a proposal archives when its plan opens or at a Decision, which is a different lifecycle event.

```python finished-recipe
from pathlib import Path
import subprocess


def finished_plans(repo_root: Path = Path(".")) -> list[tuple[str, str]]:
    proc = subprocess.run(
        [
            "git",
            "-C",
            str(repo_root),
            "log",
            "--diff-filter=A",
            "--format=__DATE__%ad",
            "--date=short",
            "--name-only",
            "--",
            "dev/plans/archive",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    seen: dict[str, str] = {}
    cur_date = ""
    for raw in proc.stdout.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("__DATE__"):
            cur_date = line.removeprefix("__DATE__")
        elif line.startswith("dev/plans/archive/") and line.endswith(".md"):
            stem = Path(line).stem
            if not stem.startswith("_") and stem not in seen:
                seen[stem] = cur_date
    return sorted(seen.items(), key=lambda item: (item[1], item[0]), reverse=True)


if __name__ == "__main__":
    for plan_id, archived_on in finished_plans():
        print(f"{archived_on}  {plan_id}")
```

### Joining active work-intent claims (a hint only)

If your project uses the optional `work-intent` module (`tools/intent.py`), you can join `python tools/intent.py list --format json` (`schema` `"cairn-intent-list/1"`) with the board's JSON output by matching each claim's `stem` to a live artifact's `id`. Claims with an empty `stem`, or a `stem` that matches no live artifact on the board, stay in an unattached list and are never attached by guessing from file paths.

Treat this join as a **hint only**: the intent log is gitignored and local to one working tree, a terminated session's claim continues to read as active until it expires or is cleared, and the intent tool belongs to a team-gated module that `tools/board.py` does not depend on.

```python intent-recipe
import json
import subprocess
import sys


def join_intents(
    board_doc: dict, intent_doc: dict
) -> tuple[dict[str, list[dict]], list[dict]]:
    if board_doc.get("schema") != "cairn-board/1":
        raise ValueError(f"Unsupported board schema: {board_doc.get('schema')!r}")
    if intent_doc.get("schema") != "cairn-intent-list/1":
        raise ValueError(f"Unsupported intent schema: {intent_doc.get('schema')!r}")
    live_ids = {
        art["id"] for art in board_doc.get("artifacts", []) if not art.get("archived")
    }
    attached: dict[str, list[dict]] = {}
    unattached: list[dict] = []
    for claim in intent_doc.get("claims", []):
        stem = claim.get("stem") or ""
        if stem and stem in live_ids:
            attached.setdefault(stem, []).append(claim)
        else:
            unattached.append(claim)
    return attached, unattached


if __name__ == "__main__":
    b_out = subprocess.run(
        [sys.executable, "tools/board.py", "--json"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    i_out = subprocess.run(
        [sys.executable, "tools/intent.py", "list", "--format", "json"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    by_id, other = join_intents(json.loads(b_out), json.loads(i_out))
    print(json.dumps({"attached": by_id, "unattached": other}, indent=2, sort_keys=True))
```

## Keeping a page honest

A generated page updates only when something runs the script: a person running it directly (for example as a session-end step) or a local `post-commit hook` that the adopter installs. Cairn's scaffold `never writes` `.git/hooks`. With neither trigger in place, the file on disk is a point-in-time `snapshot`, and the commit hash in its footer says which `HEAD` was checked out when it was built.

Always `regenerate` the page from the repository's files and never edit the HTML by hand. If a row on the page is wrong, fix the header line in the proposal or plan (or the row in `dev/PLANNING.md`) and regenerate. Because the script runs both subprocesses before opening the output file, a failure exits nonzero and never overwrites the previous page. Remember that the footer stamp comes from `git rev-parse HEAD` while `tools/board.py` reads the `working tree`, so an uncommitted edit to a header line will appear under the current `HEAD` stamp.

**Hook safety warning:** a `post-commit hook` runs the board tool and view script of `whatever commit is checked out` when a commit finishes. Checking out a branch from someone else and making a commit will execute that branch's copy of `tools/board.py` (and of the view script, if it lives inside the repository). Install a hook only in repositories where you trust `tools/`, or point the hook at a copy of the board and view script kept outside the working tree.

## Handing this guide to an AI agent

If you want a richer layout—such as filtering by date, custom styling, or a multi-panel dashboard—hand this guide and the output of `python tools/board.py --json` to an AI coding agent and ask it to write a generator script for your team, keeping the rule that the page is regenerated from `cairn-board/1` data rather than edited by hand.
