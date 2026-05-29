# Tool usage — worked examples

Cairn ships a few small, standard-library scripts. The doctrine says *that*
they exist; this doc shows *how to run them and what to do with the output* —
the concrete moment, not the abstract capability. Each tool is a **discipline
aid, not a gate**: it shifts the cheap, mechanical part of a habit left, ahead
of review.

Install paths below are the adopter-side defaults; substitute your own if your
profile placed them elsewhere. Tools marked *(team-gated)* install only when
their module is selected.

## claim_check — verify path / line / count claims

**What it does.** Scans a Markdown proposal/plan/doc and hard-flags broken
repo paths and out-of-bounds line citations, and soft-flags absolute count
claims. Run it at write-time and before committing a deliberation artifact.

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
... -- 1 soft flag(s) (must resolve or consciously accept):
  ...:7: [count] count claim `937 tests` -- compute it live or cite a delta
```

**What to do.** Fix a hard flag before committing (a real broken path, or a
forward-reference you must *mark* with a `Proposed/Untracked/External-repo
paths:` line). For a soft count flag, either recompute it live, cite a delta,
or — if it is a deliberate point-in-time snapshot — accept it with a
`<!-- claim-check-allow-count: 937 tests -->` directive.

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
optimize. Regenerate it rather than quoting a stale figure from memory (that is
exactly the count-claim `claim_check` soft-flags).

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
