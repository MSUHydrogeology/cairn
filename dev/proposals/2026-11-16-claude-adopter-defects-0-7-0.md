# Fix what adopters hit in 0.7.0: sort 17 items into plain repairs and decisions

**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: standard — the plain repairs touch the upgrade engine and the safe-Git reader, and the decisions change shipped output (the Maintainer sets the tier)
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: Adopters upgrading to Cairn 0.7.0 (most on Windows) hit 17 small faults in six issues; this sorts which ones are plain repairs and which need a design decision, and proposes the designs.

## Decision summary

Seventeen items came from issues #63, #64, #65, #66, #78 and #91 (parts 1 and 2). Eight need no Decision: three are plain repairs (a failing test, then restore the promised behavior, no contract change), three are left as is or held, and two are prose edits. Nine change an output, a default or the installed file set, so this proposal asks for a Decision on each design. The largest are the upgrade's handling of Windows line endings and of a stale recorded baseline hash, which together make a 0.7.0 upgrade on Windows look like 39 review-only files. Cost: one standard plan, Security Review of the protected files, and a Maintainer re-anchor after the engine edits. An eighteenth item, a possible network-path exposure in the link check, was added on 2026-11-16 (Proposal, item 8).

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
8. **Link check and network paths (added 2026-11-16; Maintainer: "Add the possible security defect, yes.").** Found by reading while issue #89 was checked for the heavy-tier proposal; not run on Windows. For a relative link target, `scripts/link_check.py` and its shipped twin resolve the path and test that it exists before the repository-root containment check, and nothing refuses a Windows network path first. A link in an untrusted Markdown file could therefore make the check contact a network share on Windows. **Recommend** a plain repair once a Windows test reproduces it: refuse a target that is absolute, drive-qualified or a network path before any filesystem call, and run the containment check before the existence check. If the Windows test does not reproduce it, record that and close the item. This proposal's Security Review covers it.

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

## Review -- Claude Sonnet 5.5 (ordinary Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: dae317c8e839ce14cf97b36b7039c68ea314ac79
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 7 minutes (11:54 to 12:01 EST)
**Tokens**: unknown

The strongest case: a one-developer project accepts the sort once, fixes the cheap Windows faults with a test each, and spends design effort only where an output or a hash's meaning changes.

**Foundations**

1. **Should this happen as framed?** Yes, with one relabel: the cited lines hold, but 64.1 is not a plain repair. -- `bootstrap/tests/test_session_binding_gate_and_printing_hold.py:424-429`
2. **Best alternative.** Split plain repairs from engine decisions; it buys little, since every item sits on a protected or shipped file. -- `dev/rules/protected-surfaces.md` lines 5-12
3. **What would show it wrong.** Folding `\r\n` with that pinned test unchanged and green; run it first. If it must change, 64.1 is a Decision. -- same file, line 457

1. **Blocking.** 64.1 fails rule (ii), "no contract change": an existing test pins `bare\r\nlast` as `\x0dbare\x0d\nlast`, and the named home `test_session_routines.py` holds no such test. Closes with: move 64.1 to the Decisions and name the test to amend.
2. **Non-blocking.** Item 8's order (containment before existence) breaks `test_link_allow_directive_exempts_listed_target` (`test_link_check_exclusions.py:459`), and refusing "absolute" targets drops the `/`-rooted form (`link_check.py:752`). Narrower: refuse only drive or network-path targets before `.resolve()` (line 756). The draft states honestly that it was found by reading, not run.
3. **Non-blocking.** 91.2b is probably the line-ending cause, not out of scope: `link_check.py:89` pins the sha256 of the LF bytes of `git_read.py` (the pin equals the LF digest; a CRLF copy differs). From reading, not run. Tie it to 63.2 and 91.1.
4. **Non-blocking.** "No Windows runner is known to me" is wrong: `cairn-windows` exists (`dev/rules/development-environment.md:32`). Only it can confirm 63.1, 63.2, 91.2b, item 8 and the Windows emission in 64.1; name it in the plan. Its system `core.autocrlf` is `false` (checked), so reproduce with `-c core.autocrlf=true`.
5. **Non-blocking.** 64.2b's wording depends on Decision 5 (and has two copies); item 6's quoted sentence is in `templates/core/dev/rules/README.md:5`, not the `RULES.md` header; Decision 1 omits the 31 verbatim flags in #63.2; the tier line misplaces which edits touch the engine.

**Audience / rule loss:** One rule may weaken: 64.1 narrows the child-output escape (finding 1); Security Review should read it. Items 4 and 6 lose none.

**Coverage:** Checked lines: `session.py:236,1623`; `link_check.py:201,222,314,918`; `upgrade.py` 878, 2858, 3035; `lockfile.py:467`; `merge.py:119`; `claim_check.py:1075`; `git_read.py:1157,1418`; `UPGRADE.md:618,800`; twins by `diff -q`. Not checked: any Windows behavior (one read-only VM `git config`), `cairn_commit` readability, whether Decision 4's directive clears every flag, the AST baseline, the Security Review questions. No tests run. Over target (about 370 words): five findings carry evidence the author needs.

## Security Review -- Claude Opus (Security Reviewer, High) -- 2026-11-16

```
Reviewed commit: 04921fc918bfe27535c8d2aecb1c6e6f39645ae0
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 12 minutes (11:52 to 12:04 EST)
**Tokens**: unknown

Obligation: decide whether these repairs and designs add, widen or leave open a trust boundary.

Steelman: every repair fails closed or only adds a message, so the one open boundary is item 8, which already exists.

**Foundations**

1. **Should this happen as framed?** Yes; item 8 is real from the code. A target such as `\/host/share/x.md` or `\\?\UNC\host\s\x` passes `_LINK_RE` and does not start with `/`. On Windows, `md.parent / path_part` becomes a network path, and `.resolve()` and `.exists()` then touch it. -- `scripts/link_check.py:754-758` (regex at line 188); pure-path join checked with `PureWindowsPath`
2. **Best alternative.** Check the path by its text before any filesystem call: refuse a non-`/` target whose `PureWindowsPath(...).drive` is non-empty, on every OS, and keep the existence-then-containment order. -- `link_check.py:752-768`
3. **What would show it wrong.** A unit test feeding those targets that still reaches `.resolve()` on any OS. -- the planned `test_link_check_exclusions.py` test

1. **Blocking.** The attacker is anyone who writes Markdown into a tree that a Windows user checks. They control the link target, and the harm is an outbound SMB connection, which can send the user's NTLM credential hash. The draft says to "close the item" if a Windows run does not reproduce it. A network or VM setup can fail to reproduce it while the code path stays open. Closes with: a cross-platform unit test of the path's text as the failing test, with no dependence on a Windows run.
2. **Non-blocking.** Decision 2 reads the template at the lockfile's `cairn_commit`, which is project-supplied. Closes with: the plan reuses the full-match hex gate before any Git argument. -- `bootstrap/_scaffold/SECURITY_MUTATIONS.md:121`
3. **Non-blocking.** A committed symlink to a network path would still be followed by `.resolve()`. Git for Windows creates symlinks only with `core.symlinks` set. Closes with: the plan says whether this is in scope.

Pins (point b): about 20 modules pin the LF bytes of `git_read.py`. A CRLF checkout raises `git-read-binding-failed`, so it fails safe (`link_check.py:170`). A `.gitattributes` `eol=lf` restores those bytes and changes no pin. The fix must not fold CRLF before hashing. Item 64.1 folds only a CR that comes before an LF, which cannot overwrite a line; a lone CR stays escaped. No item makes a project-supplied program run.

**Coverage:** Not run on `cairn-windows` (Windows SMB behavior is assumed, not measured). No tests run. Not reviewed: Decisions 3 to 6 beyond reading, and the reason-code values for item 7. About 380 words; finding 1 needs the attacker and the input stated.
