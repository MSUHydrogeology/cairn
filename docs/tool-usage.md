# Tool usage — worked examples

Cairn ships a few small, standard-library scripts. The doctrine says *that*
they exist; this doc shows *how to run them and what to do with the output* —
the concrete moment, not the abstract capability. Each tool is a **discipline
aid, not a gate**: it shifts the cheap, mechanical part of a habit left, ahead
of review.

Install paths below are the adopter-side defaults; substitute your own if your
profile placed them elsewhere. Tools marked *(team-gated)* install only when
their module is selected.

## claim_check — verify path / line claims

**What it does.** Scans a Markdown proposal/plan/doc and hard-flags broken
repo paths and out-of-bounds line citations. Run it at write-time and before
committing a deliberation artifact. (The category-D count soft-flag was
retired 2026-06-05 — 0 catches across the instance log; numeric drift is now
governed by the three-kind precision / `as_of` discipline and a code-side
registry verifier, not a write-time nag.)

```bash
python scripts/claim_check.py dev/proposals/2026-06-01-me-new-thing.md
```

A clean file:

```
claim_check: dev/proposals/2026-06-01-me-new-thing.md -- OK, no claim-check flags.
```

A file with problems (exit code 1):

```
claim_check: ... -- 1 hard flag(s):
  ...:42: [path] cited path does not resolve: `frontend/helpre/util.py`
```

**What to do.** Fix a hard flag before committing (a real broken path, or a
forward-reference you must *mark* with a `Proposed/Untracked/External-repo
paths:` line, or — for a single cross-document citation — a document-scoped
`<!-- claim-check-allow: <glob> -->` directive).

## scripts/verify_counts.py — re-measure registered live-invariant counts *(Cairn-maintainer-only)*

**What it does.** The **live-invariant** leg of the three-kind numeric-claim
discipline. When `claim_check` retired its category-D count soft-flag, the
*decision-irrelevant* and *snapshot* kinds were handled by doctrine (approximate;
date) — but a count cited as **present fact** and prone to drift (a headline
file size re-quoted across docs as it changes) is registered in a code-side
registry (`scripts/measurements.py`) and re-measured here. **Not installed into
adopters** (not in `_CORE_MAPPINGS`); it dogfoods on Cairn's own docs.

A doc annotates the number with `<!-- verify: <key> -->` **immediately after the
number it verifies** (RR1 — the verifier reads the number directly preceding the
annotation on that line; for a `Snapshot`, put the `as_of` date before the number
or after the annotation, not between them). The annotation carries **only a
registry key** — never a path, never a command — so there is no document-supplied
path and no shell surface (every measurement is root-contained; `git` runs
`shell=False`).

```bash
python scripts/verify_counts.py docs/tool-usage.md
```

Two kinds dispatch from the registry: an **`Invariant`** is re-measured today and
the annotated number compared to it (a mismatch is **drift**); a **`Snapshot`** is
**never re-measured** — only its value-equality and the presence of the ISO
`as_of` date on the line are checked (re-running would erase the evidence the
snapshot is). An `Invariant` whose `root` is an **absent** sibling checkout
degrades to a **visible** `SKIPPED (root absent: …)` (a distinct non-clean exit
status), never a silent pass; an **unregistered** key is **refused**.

Worked example (the number and its annotation share one physical line, per RR1):

> Cairn's `claim_check` watch file is currently 837 lines `<!-- verify: claim_check_watch_file_lines -->`.

The count-soft-flag retirement shrank it from ~876; `verify_counts` re-measures it
and flags that line if the two ever diverge.

**What to do.** Keep the registry **small** (soft cap ~10 keys) and each
measurement cheap (a bounded stdlib scan or `git log` range) — there is no cache
by design. If the verifier ever runs slowly or the registry churns more than the
docs drift, that is the **curation-tax kill-signal**: shrink or freeze the
registry, do not accelerate it. Most numbers are decision-irrelevant — approximate
them; reserve a registered invariant for the few that are cited as live fact and
genuinely drift.

## tools/intent.py — claim work before editing *(team-gated: coordination-tiers)*

**What it does.** On a concurrent team, you claim a set of files before
editing them so a second agent sees the claim and coordinates rather than
colliding. The post-commit hook auto-releases your claim.

```bash
python tools/intent.py claim --files frontend/prep/soils.py tests/test_soils.py \
    --action "fix soil-temp fold-in"
# ... edit, commit (the post-commit hook releases the claim) ...
python tools/intent.py status          # what is claimed right now, by whom
```

First-session setup (opt-in; the scaffold never mutates `.git/hooks`):

```bash
python tools/intent.py install-hook        # post-commit auto-release
python tools/intent.py install-precommit   # pre-commit work-intent check (warn-only)
python tools/intent.py hooks-status        # confirm both are installed
```

**What to do.** If a pre-commit warning says a staged path has no active
claim, either claim it or proceed deliberately — the check is warn-only, not a
gate. If `status` shows a path held by another session, coordinate before
editing it.

## tools/lifecycle_metrics.py — measure the deliberation loop *(default-on)*

**What it does.** Derives per-proposal / per-plan lifecycle metrics — review
rounds, revision counts, finding tallies — from the `dev/` tree. The report is
a derived artifact, regenerable at any commit.

```bash
python tools/lifecycle_metrics.py proposals --format md   # Markdown table to stdout
python tools/lifecycle_metrics.py proposals --out metrics.csv
```

**What to do.** Read it as a health signal, not a target: a proposal that took
many review rounds is a candidate for a retrospective, not a number to
optimize. Regenerate it rather than quoting a stale figure from memory (exactly
the numeric-drift the three-kind precision / `as_of` discipline guards against).

## scripts/link_check.py — check cross-references resolve *(team-gated: doc-drift-prevention)*

**What it does.** Resolves the Markdown links across your tracked docs and
reports the ones that do not.

```bash
python scripts/link_check.py                 # whole tracked tree
python scripts/link_check.py docs/guide.md   # specific files
python scripts/link_check.py --check-external # also probe http(s) links
```

**What to do.** Fix a broken internal link before committing the doc change
that introduced it; treat it as the link sibling of a `claim_check` path flag.
External-link probing is opt-in (slower, network-dependent) — run it at
release-prep, not every edit.

## See also

* The role-dispatch heuristics — `doctrine/roles.md` > "When to dispatch which
  role".
* The verify-before-asserting discipline these tools serve —
  `doctrine/rationale.md` and the `claim-check` module.
