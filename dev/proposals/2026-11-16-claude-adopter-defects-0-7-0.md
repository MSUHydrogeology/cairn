# Fix what adopters hit in 0.7.0: sort 17 items into plain repairs and decisions

**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Status**: awaiting-review
**Waiting on Maintainer**: release draft for review
**Review**: usual + Security Review
**Proposed tier**: standard — the plain repairs touch the upgrade engine and the safe-Git reader, and the decisions change shipped output (the Maintainer sets the tier)
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: Adopters upgrading to Cairn 0.7.0 (most on Windows) hit 17 small faults in six issues; this sorts which ones are plain repairs and which need a design decision, and proposes the designs.

## Decision summary

Seventeen items came from issues #63, #64, #65, #66, #78 and #91 (parts 1 and 2). Eight need no Decision: three are plain repairs (a failing test, then restore the promised behavior, no contract change), three are left as is or held, and two are prose edits. Nine change an output, a default or the installed file set, so this proposal asks for a Decision on each design. The largest are the upgrade's handling of Windows line endings and of a stale recorded baseline hash, which together make a 0.7.0 upgrade on Windows look like 39 review-only files. Cost: one standard plan, Security Review of the protected files, and a Maintainer re-anchor after the engine edits.

## Context

The rule is `docs/methodology/lifecycle.md` item 1 (the "Deliberate" lane, its defect-repair carve-out), with the cheap-fix limits in `dev/agent_collaboration.md` > "Working tree and commits". A repair needs no proposal only if (i) a failing test reproduces it, (ii) it restores documented or intended behavior with no contract change, and (iii) the surface's own tests run. The cheap-fix text also bars a high-risk surface, so protected files cannot use the one-line commit form.

Protected (`dev/rules/protected-surfaces.md`): `bootstrap/_scaffold/upgrade.py` and `lockfile.py`; `tools/session.py` with its byte-copy `templates/skills/_lib/session.py` (the interpreter-binding reader); `tools/git_read.py` (safe Git reader) with its twin. Shipped templates are also protected. Each protected edit takes Security Review and the Maintainer's re-anchor; AST baseline coverage: not checked.

Read at `3ec301a9`; every Windows behavior below is **not reproduced here** (macOS). Shipped twins were confirmed byte-identical with `diff -q`.

## Proposal

**Plain repairs (no Decision).** Each needs the failing test first, in the named existing home.

| # | Defect and cause | File | First failing test |
|---|---|---|---|
| 64.1 | `\x0d` after each intents line: `_encode_child_output` splits on `\n` only, then escapes the leftover `\r` (`tools/session.py:236`). Fold `\r\n` to `\n` first; a lone `\r` stays escaped. | session.py and its twin | feed `a\r\nb\r\n` and a lone `\r`: `test_session_routines.py` |
| 65.1 | Absent optional file reported "missing": `load_scanner_config` sets a diagnostic for absence (`scripts/link_check.py:314`) and `check_tree` prints it (line 918). The module says the file is optional. Print only when present and invalid. | link_check.py and its twin | empty tree, no stderr: `test_doc_drift_tools.py` |
| 65.2 | U+200B in a comment at line 201, column 44, both copies (confirmed by scan). Replace with words. | link_check.py and its twin | no format-control character in shipped `.py`: `test_content_scan.py` |
| 64.1b | Backslash shown as `\x5c` is the deliberate, reversible escape. Leave it; no change. | none | none |
| 91.2 | Symlink tests fail without the Windows privilege. The two named tests are not in this tree (`git grep` finds none). Owner and file: not located; hold until found. | not located | skip with reason when `symlink_to` raises |
| 91.2b | `git-read-binding-failed` on four tests: cause not investigated by the reporter or here; out of scope. | none | none |

**Documentation edits (no failing test possible; prose gates apply).** 66.2: add three lines under the command block in `bootstrap/UPGRADE.md` naming the collision, review-only and `--finalize` branches. 64.2b: say in the session-end skill that the handoff subject starts with `Handoff`. Both only complete existing guidance.

**Decisions (the sort's main value).** Each item changes output, a default, or the installed set.

1. **Line endings (63.2).** Cause: `_compute_upgrade` hashes the raw bytes of the saved ancestor (`upgrade.py`, near line 878) and Git's CRLF checkout changes them. Options: normalize before hashing (changes what a lockfile hash means; the lockfile schema is protected) or print a diagnostic only. **Recommend diagnostic only**: when folding CRLF makes the hash match, the review-only reason says "differs only in line endings (core.autocrlf?)", with the LF-clone route in `UPGRADE.md`. The edit check already folds CRLF (`upgrade.py:3035`), so there is precedent.
2. **Stale base hash (63.3, 66.1).** Cause: `--finalize` advances `hash` and deliberately keeps `base_hash` (`upgrade.py:2858`; its docstring says so), while `UPGRADE.md:800` says `base_hash` "ratchets forward on every `--finalize`", which is false for verbatim files. `classify_verbatim` (`lockfile.py:467`) then calls a file equal to the old template "locally-modified", and `_compute_upgrade` gives it an empty detail (66.1). Options: finalize also writes `base_hash` (alters recorded provenance), or classify at plan time (read-only). **Recommend plan time**: if the file's bytes equal its lockfile `hash` and the template at the recorded `cairn_commit`, treat it as an update. Fill the flag text: what differs, whether it equals upstream, and the two actions. Fix the `UPGRADE.md:800` sentence. Whether the recorded commit is always readable from a release checkout: not checked.
3. **Changed slot placeholder (63.4).** Cause: `_transplant_slots` (`merge.py:119`) replaces both base and theirs with the adopter's slot, so a changed upstream placeholder never reaches the merge; the `added` list covers new slots only. **Recommend** a `[changed slot placeholder] <file>: <slot>` line when old and new placeholders differ and the adopter's slot is filled. Moving doctrine out of placeholders is a larger, separate change; not proposed.
4. **Claim check in installed modules (63.5).** Cause: `claim_check` reads `claim-check-allow.json` (`claim_check.py:1075`); `link_check` reads a different file with a different shape (`scanner-check-allow.json`, `link_check.py:222`). Options: one shared source (new contract), treat `docs/methodology/` as external in adopter trees (new behavior), or add the existing in-file `claim-check-allow` directive to the six shipped module documents. **Recommend the directive**: no new file, no new contract. Whether it clears all flags: not checked.
5. **Handoff marker (64.2).** Cause: `git log --grep=^Handoff` is case-sensitive (`session.py:1623`). **Recommend** `--regexp-ignore-case` plus a fallback note that names the marker and `--handoff-marker`, replacing "likely a freshly-bootstrapped repo".
6. **`RULES.md` header (78).** The shipped `dev/rules/README.md` says Cairn "never templates" the rule files; `RULES.md` is seeded and tracked (`UPGRADE.md:618`). **Recommend** the header say that: files in `dev/rules/` are never templated; `RULES.md` is seeded once and its edits are preserved by upgrade merges.
7. **Windows hook (63.1) and Git attributes (91.1).** The hook cause is unknown: the worker's blanket `except BaseException` returns a bare failed reply, so the caller reports `worker-incomplete` (`git_read.py:1157`, `1418`). **Recommend** now only a fixed-set reason code in that reply (never exception text), then a Windows run to find the cause. Real-hook Windows test: no Windows runner is known to me. A shipped `.gitattributes` adds an installed file, so per the board it takes its own lane: a separate light proposal, written after this one is decided.

**Order.** This lands before the repository layout (`dev/proposals/2026-11-09-claude-repository-layout.md`) moves these files, because its migration relies on upgrade preserving local copies, and items 63.2 and 63.3 would turn that migration into review-only files. Fixing first also means each test is written once, against current paths. This is reasoning, not a measurement.

## Rationale

Windows is an equal partner (Maintainer, 2026-11-10, quoted on the board: "We want full windows support--it is an equal partner."), and adopters hit these now. A diagnostic is preferred to changing what a hash or lockfile means: least continuing burden.

## Alternatives considered

Treat all 17 as plain repairs: rejected; nine change output or the installed set. Do nothing: every Windows upgrade stays a hand merge.

## Documentation / doctrine surface

`bootstrap/UPGRADE.md`, the shipped `dev/rules/README.md` header and six module documents (descriptive and shipped-template layers); no governing-layer change.

## Evidence / verification plan

Each repair names its failing test; each decision gets one promise test through its real entry point (`upgrade --plan`, `session-start`, `claim_check`), run via `python tools/test_tiers.py for <paths>`. Windows behavior stays unverified until a Windows run. Falsified if a CRLF fixture still shows review-only without the new reason.

#### Security preflight

Questions S1 to S5: the protected edits (reader, engine, safe-Git reply) need them answered in the plan; not answered here.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Assurance path

Usual review, then Security Review on the protected edits; a standard plan with Internal and Internal Security Review; Maintainer re-anchor after engine edits; the 91.1 proposal separately.
