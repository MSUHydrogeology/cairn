# Plan: Repair the 0.7.0 adopter defects

**Source proposal**: dev/proposals/2026-11-16-claude-adopter-defects-0-7-0.md
**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`, Medium), plan author
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: Fix the small faults adopters hit upgrading to Cairn 0.7.0, most of them on Windows, and prove the Windows ones on Windows.

## Build summary

After this plan an upgrade on Windows no longer shows dozens of review-only files with no explanation. The report says when a file differs only in line endings, treats a file equal to its recorded release as an update, fills the empty flag text, and names a slot whose upstream placeholder changed. `session-start` stops printing stray carriage-return escapes and finds a lowercase `handoff` commit. The link check stops reporting an absent optional file, loses a hidden character, and refuses Windows network and drive targets before touching the disk. Installed module documents pass the claims check outside Cairn's tree, two shipped texts are corrected, and the Windows hook failure gets a named reason code and a real commit run on Windows.

## Source proposal

The accepted proposal (Decision 2026-11-16, standard tier with Security Review) adopts its recommended default on Decisions 1 to 7 and 9 and on item 8, and requires the Windows checks to work on Windows. This plan carries out those outcomes and adds none.

## Scope

Seven chunks edit: the link check and its shipped twin; the upgrade engine (`bootstrap/_scaffold/upgrade.py`, `bootstrap/_scaffold/merge.py`); the session reader and its byte copy; the safe Git reader, its twin and their 23 hash pins; `bootstrap/UPGRADE.md`, 11 shipped module documents and the shipped rules README; the session-end skill. An eighth chunk is the Windows evidence. Engine, reader, Git reader and shipped templates are protected: they take the Security plan review and the Maintainer's re-anchor afterwards (a separate board wait, never a chunk).

**Left alone or held (non-work):**
- 64.1b: `\x5c` for a backslash is the deliberate, reversible escape.
- 91.2: the two symlink tests are not in this tree; held until located.
- 91.2b and 91.1: same cause as 63.2; the Git attributes file is its own light proposal.
- Folding line endings before hashing (Decision 1) and `--finalize` writing `base_hash` (Decision 2): rejected, nothing changes what a hash means.
- Moving doctrine out of slot placeholders (Decision 3): larger, not proposed.
- A committed symbolic link to a network path (item 8): not included. It needs a committed link plus `core.symlinks` on Windows, a text check cannot see it, and a fix is new behavior. The reviewer may disagree.
- Cairn's own `dev/modules/` copies of the 11 documents (they follow by module refresh) and `scripts/check_cairn.py` (Cairn-only).
- CHANGELOG entries, `dev/PLANNING.md`, issue closing and archiving the proposal: the coordinator, at closeout, never implementers.

**Reuse.** Reused: `_sha256_hex`, `_well_formed_sha256`, `_theirs_bytes` and the `_behind_by_n` hex test (`bootstrap/_scaffold/lockfile.py`); the session reader's existing `\r\n` fold in `_git`; the fixtures in `test_upgrade_added_slots.py`. Searched `PureWindowsPath` over `scripts/`, `tools/`, `bootstrap/_scaffold/` (no hits, so the drive test is new) and `replace(b"\r\n"` in `bootstrap/_scaffold/` (one hit, the edit check, a different question).

### Documentation / doctrine surface

Descriptive and shipped-template layers only. No governing-layer change.

## Sequence

Estimate 12 to 16 low-tier agent-hours, 1 to 2 elapsed days. Uncertain: the Windows hook cause (C8), and other sessions' open edits.

**Every chunk.** A Low-tier implementer, high-risk chunks included (`AGENTS.md`); name the model at spawn. Claim the exact paths first. Read `git status` and `git log -5` for each file when the chunk starts: another session's uncommitted edit to the same file stops you; never commit it. Write the failing test, run it, see the stated failure, then change. Edit the shipped file, `cp` it over its installed copy, `cmp`. Prose by exact replacement. Run only the named test files with `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest`, plus the prose gates for prose (`claim_check`, `link_check`, `sync_doc_snippets --check`, `quality_gate --sub neutrality`). One commit per chunk, explicit paths. If the code differs from what the chunk says, stop and report; decide nothing. No push.

**Landing order.** These accepted light proposals edit files this plan edits: the hook installer (`scripts/link_check.py`, `tools/_intent/hooks.py`), claims warn-only (`tools/_intent/conflict.py`, `bootstrap/tests/test_intents_tool.py`, the incident and coordination module documents), release route (`bootstrap/_scaffold/install.py`, `bootstrap/PROVENANCE.md`, possibly `bootstrap/UPGRADE.md`), Windows route checks (`bootstrap/tests/security/test_git_read_routes.py`). Each gate below waits for its owner's commit.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Link check: 65.1, 65.2, item 8 | plan reviews; hook installer landed | twin pair, 3 tests |
| C2 | Upgrade: line-ending reason on saved ancestors (63.2) | plan reviews | `upgrade.py`, 2 tests |
| C3 | Upgrade: verbatim files, 63.2, 63.3, 66.1 | C2 | `upgrade.py`, 5 tests |
| C4 | Upgrade: changed slot placeholder (63.4) | C3 | `merge.py`, `upgrade.py`, 4 tests |
| C5 | Session reader and skill: 64.1, 64.2, 64.2b | plan reviews | reader pair, skill pair, 3 tests |
| C6 | Prose: `UPGRADE.md`, 11 module documents, rules README | C3, claims and release-route landed | 14 documents, 1 test |
| C7 | Git reader reason code (63.1) and the 24-site re-pin; scoped lock finalize | C1 to C6 committed, claims landed | helper pair, pins, 2 tests |
| C8 | Windows run on `cairn-windows` | C7 and Windows route checks landed | record only |

C1, the chain C2 to C4, and C5 touch disjoint files and may run in parallel. C7 is the last frozen-file edit before the Maintainer's ceremony. If C8 finds the hook still failing, the fix returns the plan to `revising-plan` (Plan change) and ends with the C7 pin step again. This plan reaches `ready-to-archive` before the repository-layout move starts (`dev/proposals/2026-11-09-claude-repository-layout.md`).

**Red until the re-anchor** (expected, not pass criteria). `bootstrap/tests/test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package` after C2 to C4 and C7 (any `bootstrap/_scaffold/` edit, pin lines included). The gate manifest after C1, C5 and C7, for each frozen file edited (the link-check pair, `scripts/*.py` pin lines, roster tests); `python scripts/repin.py status` names what is owed. One ceremony covers all of it, because every frozen edit sits in C1 to C7. Pin-consistency and each chunk's named tests stay green.

Length: the body runs about 1,150 words against the 1,000 target, and C3 and C6 pass 150, because a Low-tier executor needs exact files, strings and test names.

## Acceptance criteria

**C1 (`templates/modules/team-gated/link_check.py`, copy to `scripts/link_check.py`).** Tests first: `test_doc_drift_tools.py` (TestLinkCheck), `test_content_scan.py` (`TestSourceCarriesNoRawInvisibles`), `integration/test_link_check_exclusions.py`. (65.1) A tree with no `dev/.cairn/scanner-check-allow.json` prints nothing to stderr from `check_tree`; a present, invalid file still prints; `load_scanner_config` is unchanged (guard `config.present and config.diagnostic`). (65.2) No `scripts/*.py`, `tools/*.py` or `templates/**/*.py` holds a Unicode Cf character (measured: only line 201 of both copies); in the comment above `_BALANCED_CODE_SPAN_RE`, replace the two backtick pairs around the character, ahead of `opener of 2`, with `an `. (Item 8) Before the `path_part.startswith('/')` branch, a target not starting with `/` whose `PureWindowsPath(...).drive` is non-empty gets one `link` flag, "link target is a network or drive path and is not checked", is never exempted by `link-check-allow`, and `Path.resolve` never receives it (spy on `Path.resolve`; targets `\\host\share\x.md`, `\/host/share/x.md`, `\\?\UNC\host\s\x`, `C:\x.md`, `C:x.md`). `/x.md`, `//host/share/x.md` and `../c.md` behave as before. Copies identical.

**C2 (`upgrade.py`).** WHEN a saved ancestor's digest matches `base_hash` only after `\r\n` becomes `\n`, `upgrade --plan` lists it review-only with `saved ancestor differs only in line endings (core.autocrlf?); see UPGRADE.md (review-only diff)` (keeping today's `file missing on disk; ` prefix); every other mismatch keeps `saved ancestor is missing or invalid (review-only diff)`. A new helper runs only after the raw-byte digest check fails; nothing is folded before hashing; the file stays review-only. Tests in `test_upgrade.py` (TestUpgradeModes): a CRLF ancestor, and an altered-ancestor control. Also green: `test_upgrade_lockfile_path_containment.py`, `test_upgrade_refuses_hostile_project_data.py`.

**C3 (`upgrade.py`, verbatim branch of `_compute_upgrade`).** A verbatim file whose digest equals lockfile `hash` and whose bytes equal the template at the lockfile's `cairn_commit` becomes `verbatim-update`, even with a stale `base_hash`. The commit passes `re.fullmatch(r"[0-9a-f]{4,40}", ...)` before Git sees it, then `_theirs_bytes`; any failure (non-git source, Git below 2.45) leaves `verbatim-locally-modified`. A remaining `verbatim-locally-modified` carries one of two exact details, the first when `\r\n` folding matches the baseline `classify_verbatim` used: `differs only in line endings (core.autocrlf?); see UPGRADE.md`, or `differs from the install baseline in the lockfile and from the new upstream copy. To keep your version, leave it (record it with upgrade --finalize <path>); to take upstream, copy the upstream file over it, then run --stage and --apply.` Tests (`test_upgrade.py`, calling `_compute_upgrade` as the fork test does; skip below Git 2.45): stale-base update (a scratch directory with `git init` holding `templates/` copied from `CAIRN_ROOT`, committed once; the project installed from `CAIRN_ROOT`; one verbatim template then changed in the scratch working tree; the lock record set to `cairn_commit` = the scratch commit, `hash` = the project copy's digest, `base_hash` = another digest); forked file still flagged with detail (extend `test_finalize_preserves_verbatim_fork_detection`); CRLF script flagged, never updated; hostile `cairn_commit` `--output=<marker>` creates no file (in `test_upgrade_refuses_hostile_project_data.py`; removing the hex test makes it fail). Also green: `test_skills_upgrade.py`.

**C4 (`merge.py`, `upgrade.py`).** `MergeResult` gains a defaulted `changed` field and `FilePlan` a defaulted `changed_slots`. WHEN a slot is in the saved ancestor, the new template and the adopter's file, its raw body differs between ancestor and template, and the adopter's body is non-empty and differs from the ancestor body with tokens filled, `--plan` and `--stage` print `  [changed slot placeholder] <file>: <names> -- upstream changed this placeholder; your filled text is kept. Compare it with the new upstream text.` after the `[new slot]` lines, with `[new slot]`'s cap (10 names, 80 characters, `(and N more)`, shared helper) and `ascii()` escaping. No line for an unfilled, empty or unchanged slot. Merged text and statuses are byte-identical. Tests in `test_upgrade_added_slots.py`: changed and filled, unfilled, unchanged, cap; the file's existing nodes stay green.

**C5 (`templates/skills/_lib/session.py` to `tools/session.py`; `templates/skills/session-end/SKILL.md` to `.agents/skills/session-end/SKILL.md`).** (64.1) In `_encode_child_output`, `\r\n` becomes `\n` before the split; a lone CR, including one before a CR-LF pair, still prints `\x0d`. Amend the two pinned assertions in `test_session_binding_gate_and_printing_hold.py` (`\x0dbare\x0d\nlast` to `\x0dbare\nlast`; `error\x0d\nnext\x9b` to `error\nnext\x9b`) and add lone-CR and CR-LF-pair cases through the real child-tool path (fold-all mutant fails the lone-CR case). (64.2) `git log` gains `--regexp-ignore-case`; `test_session_routines.py` gains a lowercase `handoff:` case and a mid-subject control; the fallback note keeps `no '<marker>' commit found`, adds "any letter case", names `--handoff-marker`, and drops "likely a freshly-bootstrapped repo". (64.2b) Both skill copies gain, after the reflection paragraph: "The handoff commit message starts with the marker `Handoff`, in any letter case; `session-start` lists the commits after the last one. A project with another marker passes `--handoff-marker`." Copies identical. Also green: `test_session_start_drain_rules.py`.

**C6 (prose).** `bootstrap/UPGRADE.md`: under the workflow command block, three lines (`--stage` collision: `upgrade --adopt-collisions`, see "New core-like files (and skills) added upstream"; review-only files: merge by hand from `dev/.cairn-upgrade/review-only/`, then `--apply --ack-review-only`; an in-place edit: `upgrade --finalize <path>`, see "Recording an edit you made"); after the paragraph on hashing the saved ancestor, "If `--plan` lists files that differ only in line endings, Git converted the saved ancestors when it checked your project out (`core.autocrlf`). Re-clone with `git clone -c core.autocrlf=false` and run `--plan` again; do not edit `dev/.cairn/base/`."; in the forked-facade section replace "`base_hash` ratchets forward on every `--finalize`, so an unconfirmed difference" with "`--finalize` advances `hash` and keeps `base_hash` for a verbatim file, so an unconfirmed difference". In `templates/modules/` only, each module document that exits 1 from `claim_check.py` in a scratch `high-rigor-legacy` install (measured: 11 documents, 22 paths) gets first line `<!-- claim-check-allow: <the exact unresolved paths, no wildcard> -->`; a new test in `test_claim_check_module.py` installs that preset and asserts exit 0 for every `dev/modules/*.md` (it fails first: 11 exit 1). `templates/core/dev/rules/README.md` and `dev/rules/README.md`: replace "Cairn never templates them" with "Cairn never templates the files in it; `RULES.md` is seeded once, and upgrade merges preserve your edits to it."

**C7 (`templates/skills/_lib/git_read.py` to `tools/git_read.py`).** The Windows worker's failure reply carries `reason`, one of five fixed codes by stage: `worker-request-invalid` (read, size, JSON, keys), `worker-source-mismatch` (digest), `worker-load-failed` (compile or exec), `worker-run-failed`, `worker-reply-failed`; never exception text. The parent copies it through `_worker_reason`, which accepts only that set and otherwise returns `worker-incomplete`. Tests in `bootstrap/tests/security/test_git_read.py`, any OS: run `_WINDOWS_BOOTSTRAP` under `-I -c` on five inputs (not JSON; wrong digest; source that raises when loaded; `_windows_worker_run` that raises; one that returns `None`) and check each reason, exit 2, and an exception marker absent from output; a `_worker_reason` test. **Pin step:** compute the new digest; replace the old in every file `git grep -l` finds (measured 23 plus `dev/.cairn/cairn-lock.yml`); no old digest remains; a throwaway script (not committed) confirms every `_GIT_READ_SHA256` equals the helper's digest. Commit; then one scoped `python bootstrap/scaffold.py upgrade --finalize --target /Users/kendal30/Code/cairn --cairn-root /Users/kendal30/Code/cairn <paths>` naming each self-installed copy changed by C1 to C7 (changed paths that are a `dst` in `dev/.cairn/cairn-lock.yml`), and commit the lock alone.

**C8 (Windows).** On `cairn-windows` (x64 `lhm` interpreter, fresh folder from `git archive`, commands as in `dev/measurement/windows-native-rerun-2026-11-13.md`), record commit, interpreter, commands, results and elapsed in an `## Implementation` entry here. (a) Every new or changed node of C1 to C7 passes; a failure elsewhere in those files is compared with the same node at the pre-plan commit on the VM. (b) 63.2: a project cloned with `git -c core.autocrlf=true clone` shows the line-ending reasons under `upgrade --plan`; with `core.autocrlf=false` it shows none. (c) 64.1: `session-start` over an active intent prints no `\x0d`. (d) 63.1: in the unpacked tree after `git init`, `git add .`, one commit and `python tools/intent.py install-precommit`, a real `git commit` of one staged file exits 0 with no `worker-` reason in its output; otherwise record the reason code and open the Plan change. (e) Item 8's nodes pass; no check opens a network connection.

**Security answers (only where chunking matters).** S1: link target, lockfile `cairn_commit`, child output and worker reason are untrusted and each passes a text check, hex test, escape or fixed set before use. S2: new failing cases are in C1, C3, C5 and C7, each with a one-line mutant. S3: the named pytest homes, `upgrade --plan`, `session-start`. S4: every fallback lands on flagged, review-only or refused. S5: a committed link to a network path still wins (non-work). The Security plan review also assesses the conceded executable-folder check in `tools/git_read.py` (Decision 7); this plan changes no code there.

## Scope delta

**Scope delta**: preserved.

## Verification

Promises and entry points: `check_tree` stderr, the link refusal and the Cf scan (C1); `upgrade --plan` and `--stage` output (C2 to C4); `session-start` output (C5); `claim_check.py` over an installed tree (C6); the worker reply and `_worker_reason` (C7); real Windows runs (C8). Each chunk runs only its named files, the existing homes of the changed code or text, where its new tests go; `python tools/test_tiers.py for <paths>` is the ceiling. After C7 the coordinator runs that selector over the joined changed paths once on the clean tree and records omissions; no whole suite. Code review after C8: ordinary and Security, over the joined range. The Maintainer's re-anchor is a standalone board wait with its own evidence; AST and gate-manifest results stay unpassed until it, and do not block archive.

## Plan review -- Claude Sonnet 5.5 (Plan Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: 33a9f5a611cfe8b9663d569161544e16ca8853e4
```

**Obligation**: Clear that each chunk C1 to C8 can be run by a Low-tier implementer with no design left to them, that the plan delivers every outcome the accepted Decision adopted (none lost, none added), and that its order, ownership and ceremony statements are true. This Internal pass does not clear the Internal Security Review.
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 14 minutes (12:43 to 12:57 EST)
**Tokens**: unknown

Strongest case: one chain of small, test-first repairs with exact strings is the cheapest route to a working Windows upgrade, and C1, C2, C4, C5, C6 and C8 are specified well enough for a Low-tier implementer.

**Foundations**

1. **Should this happen as framed?** Yes. Every outcome of Decisions 1 to 7, 9 and item 8 has a chunk, and the three tree contradictions stay inside the Decision (finding 3). -- `dev/proposals/2026-11-16-claude-adopter-defects-0-7-0.md`, Decision block
2. **Best alternative.** Forward the worker's inner failure reason (already a fixed string) instead of five stage codes, and learn the real Windows cause first with a scratch probe that is never committed, so there is one 24-file re-pin, not two. -- `tools/git_read.py:1515`
3. **What would show it wrong.** A C7 test that makes the real `_windows_worker_run` fail inside and still gets `worker-incomplete`. -- `tools/git_read.py:1135-1160`

1. **Blocking, C7 (returned to author: missing design).** The five stage codes cannot see the likely Windows failure. `_windows_worker_run` ends in `except BaseException: return ReadResult("failed", None, b"")` (`tools/git_read.py:1515`) and the bootstrap copies only `state`, `returncode` and `stdout` (lines 1152-1155), so a failure inside the run still reaches the parent as `worker-incomplete`; only a monkeypatched test reaches `worker-run-failed`. Missing decision: does the bootstrap forward a returned failed result's inner `reason` (and which fixed set the parent then accepts), or map any `state != completed` to `worker-run-failed`? Closes with: that sentence in C7 and a test through the real `_windows_worker_run`. From reading, not run.
2. **Blocking, C3 (returned to author: test cannot fail as specified).** Measured in a scratch copy: `_theirs_bytes` given `--output=<path>` raises and creates no file even with no hex test, because `_resolve_commit_oid` already passes `--end-of-options` (`bootstrap/_scaffold/lockfile.py:289-292`); a non-hex name such as `HEAD` is resolved and read. So "removing the hex test makes it fail" is false. Missing: the distinguishing assertion (a spy that `_theirs_bytes` is not called for `HEAD` and `--output=...`) and the exceptions caught around it (`ScaffoldSecurityError`, `bootstrap/_scaffold/upgrade.py:353`; "any failure" invites a bare `except`). The scratch-repo recipe itself ran as written.
3. **Non-blocking, the three tree contradictions stay inside the Decision; no Maintainer allowance.** (i) 11 module documents, 22 flags: measured with `claim_check.py` on a `high-rigor-legacy` install; an install of all 22 modules flags the same 11, and a first-line directive clears each in a scratch copy. The Decision's outcome is "installed documents pass"; "six" was marked not checked. (ii) The second assertion is `bootstrap/tests/test_session_binding_gate_and_printing_hold.py:457`: same fold, same Decision 9. (iii) 24 files hold the digest (`git grep -l`), the direct result of editing the pinned reader that Decision 7 adopts. Add "six became eleven" to the Scope delta line.
4. **Non-blocking, order and ceremony.** Order is true and safe: the hook installer is still uncommitted in the tree; claims warn-only and release-route are in (`dc6e4ffb`, `b2cd93f4`). C7's gate omits the hook installer though C7 re-pins the `scripts/sync_doc_snippets.py` pair it edits. The red list is wrong: C2 to C4 edit three frozen test files (`bootstrap/tests/test_upgrade.py`, `bootstrap/tests/test_upgrade_added_slots.py`, `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py`), so the gate manifest also holds after C2 to C4.
5. **Non-blocking, C8 and exact text.** C8(b) names no source project; (e) "no check opens a network connection" has no method (the spy nodes passing is what is measurable). Each other Windows claim has a run. Give exact strings for the C5 fallback note and C6's three `bootstrap/UPGRADE.md` lines; the sentence C6 replaces breaks across lines 800-801; "22 paths" is 22 flags; C6 edits Cairn's own `dev/rules/README.md`, which Decision 6 does not name (keep or drop); C7 hand-edits the lock and then finalizes it (leave it to the finalize).

Security, one line, not assessed: C3 (project-supplied `cairn_commit` toward Git), C7 (new worker-reply field) and C1 (new refusal) touch trust inputs; the Security Review owns them.

**Does any rule weaken or disappear?** No, beyond the Decision: a CR directly before LF is no longer escaped (C5), the 11 documents exempt only their named unresolved paths (C6), and a false `--finalize` sentence is corrected.

**Coverage**: Did not run any test, the Windows VM or `repin.py`. My scratch probes (a C3 recipe copy, the hex-test question, `claim_check.py` over installed documents) are my measurements, not the implementer's. About 780 words with headers, over the 300 target: findings 1 to 3 carry measured evidence the author needs, and findings 4 and 5 batch small fixes in one place.

## Plan review -- Claude Opus (Security Reviewer, High) -- 2026-11-16

```
Reviewed commit: 09f94350b1d28a0afd14e0d0b6aad7f76aaf2164
```

**Obligation**: Decide whether any chunk adds, widens or leaves open a trust boundary, and state the security requirements C1 to C8 must carry so a Low-tier implementer cannot weaken an existing protection. Security Review pass 1 of at most 2.
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 4 minutes (12:57 to 13:01 EST)
**Tokens**: unknown

Strongest case: every chunk fails closed or only adds a message, so the plan's security work reduces to one text check (C1) and one closed set (C7).

**Foundations**

1. **Should this happen as framed?** Yes, except that C1's rule leaves a route open (finding 1). -- `scripts/link_check.py:751-752`; `PureWindowsPath` probe in a scratch folder
2. **Best alternative.** C1: test the drive of the text actually joined. C7: forward the worker's own fixed reason through a literal set checked on both sides. -- `tools/git_read.py:1152-1158`, `1416-1418`
3. **What would show it wrong.** A C1 test in which `/\\host\share\x.md` reaches `Path.resolve`, or a C7 reply carrying `reason: "\x1b[2J"` that reaches the `ReadResult`. -- the planned test homes

1. **Blocking, C1.** The attacker is anyone who writes Markdown into a tree a Windows user checks; they control the target. The rule tests only targets not starting with `/`, but line 752 joins `root / path_part.lstrip('/')`. Measured with `PureWindowsPath`: `/\\host\share\x.md` and `/\/host/share/x.md` both join to `\\host\share\x.md`; `/Z:x.md` joins to drive `Z:` (possibly a mapped share). Closes with: refuse when `PureWindowsPath(t).drive` is non-empty, where `t` is `path_part.lstrip('/')` for a `/`-led target and `path_part` otherwise (so `//host/share/x.md` stays under the root), before the `link-check-allow` lookup. The test adds those three targets, a refused target listed in `link-check-allow`, and the spy on `Path.resolve`. A committed link to a share is not a link-check boundary (every reader in that checkout follows it); the plan's exclusion is acceptable.
2. **Blocking, C7: the constraints any fix to the Internal review's finding 1 must meet.** The reason is a label only; every caller already refuses on any failed state (`scripts/run_portable_security_sweeps.py:700-705`, `tools/meter.py:4853-4860`). Required: (a) the set is a literal `frozenset` in `git_read.py`; `_worker_reason` returns a value only when `isinstance(value, str) and value in` that set, else `worker-incomplete`, so no pattern match, no `str(exc)` and no exception type name; (b) inside `_windows_worker_run`, a `GitReadError` whose message is in the set returns it as `reason` (all 115 raises are literals today), anything else returns `worker-run-failed`; (c) the bootstrap adds `"reason"` to its reply only from `result.reason`, through `json.dumps` (ASCII); its own `except` writes fixed bytes; (d) the parent reads `reason` only when `state != "completed"`, keeps `stdout` empty, and ignores `reason` on a completed reply. Forwarding the inner reason this way keeps the set closed; the five stage codes alone are closed but blind. Tests: a reply whose `reason` is an escape sequence, a code with a trailing newline, a Windows path, a 10,000-character string, a non-string, or a plausible code outside the set gives `worker-incomplete`; a completed reply with a `reason` returns no reason; a real `_windows_worker_run` with an invalid request returns `worker-request-invalid` on any OS (`_worker_job` does nothing off Windows, `tools/git_read.py:694`).
3. **Non-blocking, the 24 pins.** A missed site fails closed: the loader raises `git-read-binding-failed` (`scripts/link_check.py:171`). The only way this fails open is an implementer "fixing" a binding failure by editing a loader. Required: compute the digest from the final committed helper bytes, after the last `git_read.py` edit; the diff at each site changes only the 64-character literal and touches no loader line (stop and report otherwise); the throwaway check covers all three names (`_GIT_READ_SHA256`, `_GIT_SHA256` in the `exact_replace.py` and `prose_diff.py` copies, and `SAFE_GIT_SOURCE_SHA256` in both `meter.py` copies). As written, it names only the first and would skip six sites.
4. **Non-blocking, C3.** No new capability: a crafted `base_hash` equal to the file's digest already gives `verbatim-update` (`bootstrap/_scaffold/upgrade.py:858-859`). The read is bounded to Cairn's own source repository and to `templates/` (`_contained_lockfile_path`, line 347). Required: catch exactly `ScaffoldSecurityError` around `_theirs_bytes` (it wraps the Git failures, lines 351-366); `None` stays locally modified; compare raw bytes. A test that can fail: `cairn_commit: HEAD` in the scratch repository where the template at `HEAD` equals the project file must stay `verbatim-locally-modified`; without the hex test it becomes `verbatim-update`. Keep `--output=` as a regression check that no file is created.
5. **Non-blocking, C2 and C3 line-ending texts.** These texts are diagnostics only. The test asserts the kind, that `ancestor_evidence["checked_base_hash"]` is the raw-byte digest, and that `--stage` writes no merge. A mutant that folds line endings before hashing must fail it.
6. **Non-blocking, C5.** The only change is `value.replace("\r\n", "\n")` before the split. Add `a\r\r\nb` (prints `\x0d`) and `\x85` and ` ` cases, which must stay escaped; a `splitlines()` mutant fails them.

C6 widens nothing: the directive takes specific literal paths, suppresses only flags for unresolved paths, and is scoped to one document (`scripts/claim_check.py:146-158`); the claim check is a drift heuristic, not a security control. Decision 7's executable-folder concession needs a local writer on Git's parent folder, who can already replace Git: not a threat in Cairn's model.

**Coverage**: Ran one `PureWindowsPath` probe; read the cited lines. Did not run tests or the VM, and did not review C4, C6's prose, C8's method or the AST and gate ceremony. About 900 words, over the 300 target: eight chunks, and the C7 constraints must be exact for a Low-tier implementer.
