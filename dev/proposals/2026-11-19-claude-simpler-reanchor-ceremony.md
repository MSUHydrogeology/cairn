# Let the re-anchor pass a long history, and shrink the Maintainer's part

**Author**: Claude Sonnet 5.5
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — it changes what the signing ceremony accepts.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-19
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/certifying-runs.md, dev/rules/working-agreements.md
**In brief**: Fix the re-anchor so it can pass a repository whose history changed the install lock and the AST baseline, and cut the Maintainer's part to checking hashes and typing a passphrase.

## Decision summary

On 2026-11-19 the Maintainer started the v0.8 re-anchor, the signed step that moves the trusted gate anchor to the new file layout. It stopped three times before signing. The third stop cannot be fixed by preparation: the ceremony requires a "stop record" for every commit since the old anchor that changed the install lock or the AST baseline files, and this release has 33 such commits and no records. The first two stops were agent-side setup errors. The Maintainer released v0.8 without the re-anchor, because the shipped files do not change; the re-anchor moves to v0.9.

Proposed, for v0.9, before the next re-anchor:

1. In transition mode, replace the per-commit history check with a check that the three pinned files at the reviewed candidate have the digests the independent reader recorded.
2. Add `ceremony --check-only`, an agent-run mode that makes every check the ceremony makes before it touches the key, so setup errors show before the Maintainer starts.
3. Put a one-page card at the top of the runbook: what to have ready, what to check, what to type.

Cost: part 1 narrows what a transition ceremony checks. It examines the end state, not each step of the history. That needs a Security Review.

## Context

Measured on 2026-11-19.

- `check_stop_records` (`release/repin.py:2559`) runs without condition (line 3003). The range `e5b7fd0a..6620faa5` has 33 commits that change `dev/.cairn/cairn-lock.yml` (29, routine scoped finalizes) or the AST fixtures (4). Only `apply-reviewed-pin` writes stop records, and none exist. `--transition` cannot be combined with `--first-run`, the one switch that turns the refusal into a warning (line 3353).
- The layout plan left the check untouched. No test and no reader exercised a history with such commits.
- The two earlier stops: the trusted checkout was one commit behind the reader's record, and `prepare-values` named the Maintainer's checkout, not the trusted one. Neither shows until the ceremony reads them.
- The signing stage receives only `HOME`, `PATH`, `TERM` and `LANG` (`release/repin.py:3069`), so `SSH_ASKPASS` never reaches it and the passphrase is asked in the terminal. The runbook does not say so. Its Maintainer tasks (confirm the fingerprint, compare hashes, type the passphrase) are scattered through a long document.

Not checked: whether the ordinary ceremony refuses routine lock updates the same way.

## Proposal

**Part 1.** In transition mode only, the reader's record also lists the digest of each pinned output (the two AST fixtures and the lock) at the candidate, computed from raw Git objects. The driver compares them with the candidate's blobs and refuses on a difference, a missing line or a duplicate. It no longer walks the history for stop records. The ordinary ceremony is unchanged.

**Part 2.** `ceremony --check-only` runs every check before the key probe: the record and its digests, the values file's checkout equal to the trusted checkout, that checkout at the record commit, the report binding, the dispositions and both scans. It prompts for nothing, writes only inside the ceremony folder, and exits 0 only if the real run would reach its first prompt. The agent runs it; the Maintainer's command is printed only after it passes.

**Part 3.** The runbook card lists what the agent hands over (the command, the fingerprint source, the three digests to compare, where each digest is printed), what the Maintainer checks, and what the Maintainer types (`YES` at each prompt, the passphrase in the terminal). It says not to run the launcher by hand and not to use `SSH_ASKPASS` for this ceremony, and names where the graphical prompt does apply (`dev/rules/development-environment.md`). The long reference stays below it.

Outcome: the next re-anchor needs no `repin.py` edit and no reading beyond the card. Prerequisite: a Decision and a plan. Release: v0.9.

## Rationale

The check exists so that an unreviewed change to a pinned file is not blessed. What is blessed is the final state. Cairn's own workflow rewrites the lock after most changes (29 times in this release), so a per-commit rule passes only if each rewrite goes through the Maintainer's apply prompts, which turns one deliberate approval into dozens. Comparing the end state with digests an independent reader computed keeps the part that matters.

## Alternatives considered

- **Write stop records after the fact.** It fakes the Maintainer's approval. Rejected.
- **Route every lock update through `apply-reviewed-pin`.** Dozens of prompts per cut, for files that change by design.
- **`--first-run` for a transition.** It turns every history finding into a display and is meant for unsigned anchors.
- **Do nothing.** No release that moves the layout could be re-anchored, and the anchor stays on the old layout, as v0.8 shipped.

## Documentation / doctrine surface

`release/REANCHOR_RUNBOOK.md` (the card and the notes on askpass and the trusted checkout), `release/repin.py`, and a pointer in `dev/rules/development-environment.md`. No shipped adopter text changes.

## Evidence / verification plan

Test homes: `tests/test_repin.py`, `tests/test_repin_ceremony.py`, `tests/test_reanchor_driver_disclosures.py`. Entry point: `repin ceremony --transition`. Promises: (a) a history with routine lock commits and a matching end state passes; (b) a pinned file one byte off the reader's digest, or a missing digest line, refuses; (c) `--check-only` refuses a stale trusted checkout, a values file naming the wrong checkout and a wrong report digest (the three faults of 2026-11-19), and never prompts or reads the key; (d) the ordinary ceremony still refuses an unrecorded pin commit. `python tests/check_cairn.py` covers the runbook. No full suite until the cut.

### Security preflight

- **S1.** The digests come from the reader's committed record, written by a fresh reader from raw objects. The candidate supplies the blobs under judgment, not the digests.
- **S2.** Change one byte of a pinned file at the candidate and the ceremony refuses; promise (b) shows it.
- **S3.** `repin ceremony --transition` fires it, over exactly three paths.
- **S4.** A missing, duplicate or malformed digest line refuses, which is less authority.
- **S5.** An attacker who can commit to the branch commits a bad pinned file early and restores it before the candidate: no longer caught, and nothing shipped is affected. The class is closed by enumeration of three paths, not by construction.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A candidate whose pinned file differs from the reader's digest passes; `--check-only` exits 0 and the real run then refuses on a check made before the key; or the ordinary ceremony stops refusing unrecorded pin commits.

## Scope delta

**Scope delta**: preserved. This is the opening proposal; nothing accepted is removed.

## Assurance path

**Assurance path**: high-assurance. The change alters what the signing ceremony accepts. Obtain the usual review and a Security Review before the rule changes.
