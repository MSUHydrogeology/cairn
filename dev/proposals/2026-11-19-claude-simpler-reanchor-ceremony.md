# Let the re-anchor pass a long history, and shrink the Maintainer's part

**Author**: Claude Sonnet 5.5
**Status**: revising
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

## Review -- Claude Sonnet 5.5 (usual reviewer) -- 2026-11-20

```
Reviewed commit: 8b5ed6400c4d963790506e31b7ee24113bbbb10c
```

**Tier**: usual
**Findings**: raised (one blocking)
**Verdict**: REVISE

**Elapsed**: about 12 minutes
**Tokens**: unknown

The proposal tries to let the next signing pass a history in which Cairn rewrote its own lock many times, and to let an agent find setup errors before the Maintainer starts. The aim is sound.

**Foundations**

1. **Should this happen as framed?** Yes. `check_stop_records` runs unconditionally (`release/repin.py:2559`, called at 3003), and I counted 29 lock commits in the range -- `git log --oneline e5b7fd0a..6620faa5 -- dev/.cairn/cairn-lock.yml`.
2. **Best alternative?** Doing nothing leaves the anchor on the old layout. Routing each rewrite through the apply prompts is worse. Checking the end state is the better design -- Rationale; `repin.py:1574` (only `apply-reviewed-pin` writes records).
3. **What would show it wrong?** A pinned file one byte off the reader's digest that still passes, or a `--check-only` exit 0 followed by a refusal before the first prompt -- promises (b), (c).

**Findings**

1. **Blocking.** Part 2 contradicts itself. The first prompt is the pasted launcher digest (`repin.py:2890`), which comes before the stop-record check (3003). The key probe (`key_checks`, 3004) comes before the two scans and the report binding (3014-3045). So "every check before the key probe" leaves out the scans and report, and "reaches its first prompt" says nothing about them. Replace the first two sentences of Part 2 with: "`ceremony --check-only` makes every check the real run makes except the key probe (`key_checks`, which reads the key file) and the typed answers: the record and its digests, the values file's checkout equal to the trusted checkout, that checkout at the record commit, the report binding, the dispositions and both scans. It computes the launcher digest itself and compares it with the record. It exits 0 only if the real run would reach its last prompt before signing."
2. Non-blocking. "Not checked" can be answered by reading: line 3003 is unconditional, so an ordinary ceremony refuses 29 lock rewrites too, and promise (d) keeps that. Say so, so the Maintainer knows the ordinary path stays unusable here.
3. Non-blocking. "Independent reader", "candidate" and "pinned" are not defined; the Decision summary needs one plain line each.
4. Non-blocking. The card is well aimed, but the proposal never says the Maintainer's hash comparison is among three named digests; list them.

**Not covered**: no test, ceremony or repin run; I did not judge the Security questions (end-state check against the per-commit check, key exposure, the five preflight answers), which the next pass owns. Line 3353 cited for `--first-run` is the `if`; the refusal is on 3354.

## Review -- Claude Opus 5.5 (Security reviewer) -- 2026-11-20

```
Reviewed commit: 4eaf26f62d6c6d50e7c52b8efca02f5a33a029de
```

**Tier**: Security Review
**Findings**: raised (two blocking)
**Verdict**: REVISE

**Elapsed**: about 25 minutes
**Tokens**: unknown

The proposal wants one deliberate approval of the final pinned files in place of dozens of per-commit ones. That aim is right; the mechanism drops the approval.

**Foundations**

1. **Should this happen as framed?** The goal, yes; Part 1 as written, no -- finding 1; `release/repin.py:2559-2609`.
2. **Best alternative?** Show the net change of the three files from the old anchor to the candidate at one prompt -- `render_changes`, `repin.py:1082`.
3. **What would show it wrong?** A transition test where an agent commit rewrites one AST baseline key: it must be displayed before signing.

**Findings**

1. **Blocking.** The digest check is almost a no-op: the record commit may change only the record and must sit on the read commit (`repin.py:2819-2827`), so the reader's digests already equal the candidate's files. The verifier does not hash the AST baseline (`tests/_gate_manifest.py:86-91`); stop records are the ceremony's only sight of it. Here four fixture commits would be signed unseen; the runbook's threat is honest agent mistakes (`REANCHOR_RUNBOOK.md:5`). Add to Part 1, after its second sentence: "Before the Summary 2 prompt the driver shows each pinned file's net change from the old anchor to the candidate, key by key, old paths mapped to new; that `yes` covers it, and the reader records reading that change." Replace S2's second clause with "promise (b) catches a change after the reader's record; new promise (e), a fixture change before it is displayed, covers the rest." Replace S5 with: "An honest agent rewrite of a pinned file is no longer stopped per commit; the net change is shown once instead."
2. **Blocking.** Replace Part 2's second and third sentences, superseding the usual review's wording, which would need stage 1's report (`repin.py:3036-3044`): "It stops before `key_checks` (line 3004): it runs no `ssh-keygen` or `ssh-add` against the private key, never starts stage 1 and checks no package or report. It writes nothing the real run reads, and the real run remakes every check."
3. Non-blocking. Transition is measured, not chosen (`repin.py:2993-2997`), so the ordinary ceremony stays unchanged; but the relaxation covers every future transition. Say so.
4. Non-blocking. Check-only runs the candidate's `reanchor.sh` validate as the agent (`repin.py:2948-2957`): no new authority, but say so. S1, S3, S4 hold.

**Not covered**: no runs; the launcher template and `reanchor_ceremony.py` read only where `repin.py` calls them; layout context setup (`repin.py:2480-2515`) skimmed.
