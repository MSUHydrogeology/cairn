# Code review (External) — the issue batch (`4edd7778..5f520a33`) — Claude Opus 5.5 — 2026-10-17

**Obligation**: External code review (falsification), the one code review the
trivial lane's defect-repair carve-out requires (`doctrine/lifecycle.md` >
"Three lanes"), here covering nine commits. Fresh session, not the
implementing session. The implementer is the same agent type, so the distance
here is a fresh context, not a different type.
**Reviewed range**: `5aabfdb3..5f520a33` — the nine commits `4edd7778` through
`5f520a33`, with `5aabfdb3` (`4edd7778^`) used as the "before" tree.
**Interpreter**: Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
`PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`. Platform: darwin. Every
install, mutation and test run used `git archive` extractions of `5f520a33`,
`5aabfdb3` and `1c9d3f51` under the session scratchpad, against throwaway
target trees. In the live checkout I ran only read-only tools (`tools/board.py`,
`tools/evolution_infer.py`, `bootstrap/verify_integrity.py --target .`,
`scripts/check_cairn.py` on one file) and one read-only test node that needs a
git checkout; `git status --short` was unchanged by them.

**Verdict**: REVISE — 2 blocking, 6 non-blocking. No commit needs reverting.

Seven of the nine commits do what they say and close the failure their issue
reported. Two do not close it. **#15:** in the default mode — the one
session-start runs — the rate-limit gate still prints `none` and exits 0 for
trackers shaped like the issue's own; only the `--trackers` mode was fixed.
**#10:** the new `--finalize` hint fires on any file containing the marker
text anywhere, and a shipped default-on file quotes the marker in prose, so in
Cairn's own tree the only file the hint names has no slot at all — exactly what
the commit says the hint must never do. Neither regresses anything: each commit
is better than its parent, and the tests around their callers pass as before.
Both fixes are small and outside the engine package, so neither touches the AST
baseline. One non-blocking item (IB3) sits in `_cmd_adopt_module`, the one
CHANGED engine symbol, and should land before the Maintainer re-anchors.

## Falsification ledger

### `4edd7778` — the board test builds its own tree

| Check | Result |
|---|---|
| Reported failure | **Reproduced and closed.** The live board lists 0 rows today, so the old assertion (rows non-empty) fails on the repository as it stands. The new test reads only its own scratch tree. |
| Can the test fail? | **Yes.** Four mutations of `tools/board.py`, each red: templates no longer skipped; archives always included; `dev/plans` not read; `archived` never set. |
| Collection | Same node ID; 15 passed. |

### `a01f1774` (#11) — the adopt refusal names a remedy

| Check | Result |
|---|---|
| Follow the advice, preset-only install | **Holds.** The refusal (exit 2) names `dev/.cairn/profile.yml`; the install profile copied there plus `python_package: mypkg` adopts (2 files recorded). |
| Follow the advice, Appendix B install (literal `modules:`, no preset, no axes) | **Fails → IB3.** |
| Can the test fail? | **Yes.** Restoring the old message turns it red (the `init-lock` assertion). |
| AST | **As declared.** `bootstrap/tests/test_ast_attest.py` is red on exactly `FunctionDef:_cmd_adopt_module` e94a89ec4083cd40 → 7a8513f314db483a, and green on `5aabfdb3`. Expected. |
| Adopt tests | 14 passed. |

### `32c8be94` (#15) — evolution_infer fails closed and says what was read

| Check | Result |
|---|---|
| A canonical tracker still counts | **Holds.** A canonical-header tracker with two in-window `occurred` rows gives the same finding on both trees; the new one adds a `READ` line. Cairn's own three trackers: same result on both (no findings, nothing fail-closed), plus `READ (3)`. |
| Existing JSON keys | **Unchanged.** `findings`, `fail_closed_trackers`, `threshold` as before; `fail_closed_reasons` and `trackers_read` are added. |
| `tools/session.py` | **Works.** `_run_evolution_infer` (`tools/session.py:1231`) prints the new output as-is. It runs discovery mode, with no arguments. |
| The issue's tracker shape, named with `--trackers` | **Fixed.** Exit 3, with the reason. |
| The issue's tracker shape, discovery mode | **Not fixed → IB1.** |
| Can the tests fail? | **Yes.** All three are red on the old gate. Mutations — drop the missing-column reason; skip named trackers again; read columns by position — each red. Dropping the window reason turns an existing test red (TypeError). One survivor → IB7. |
| Twins and lockfile | Byte-identical twins. The lockfile `hash` equals the file's sha256 (`39e1c643…`) and `base_hash` is untouched, as a scoped finalize should leave it. |

### `e23aad28` (#10, part 1) — verify_integrity points a filled slot at `--finalize`

| Check | Result |
|---|---|
| Follow the hint literally | **Holds.** On a scratch install with a filled, marked `project-conventions` slot, the printed command (run from the Cairn checkout) finalizes 1 path, and verify_integrity then passes. |
| A mismatch without the marker gets no hint | **Holds for a file whose bytes lack the marker** (`VENDOR.md`). |
| An unexplained edit to a file that ships with the marker text | **Gets the hint → IB2.** |
| Can the test fail? | **Yes.** Hint for every mismatch: red. No hint at all: red. |

### `1c9d3f51` (#20, #21) — two template pointers

| Check | Result |
|---|---|
| #20: "the module-merge pass fills only an empty body" | **True.** `resolve_slot_merge` against the shipped template: empty body → `inserted`; blank lines only → `inserted`; an `N/A:` line → `conflict` (deferred to a side file). |
| #20: "the one exception" | **True** within `templates/core/AGENTS.md`. The old N/A instruction survives in the module file it points to → IB5. |
| #21: the new targets exist | **Yes.** `## Session reflections and handoff` (`templates/core/dev/agent_collaboration.md:135`) and the doctrine step (`doctrine/session-routines.md:394`). No live reference to the removed slot remains. |
| Standing gates | **check_cairn red at this commit** (loop fidelity: the doctrine citation dangles in an adopter tree). Repaired by `90236088`; see Seen, not raised. |

### `90236088` — the `cairn-internal-ref` marker

| Check | Result |
|---|---|
| The marker is the form the gate reads | **Yes.** The inline `cairn-internal-ref:` form matches `_INTERNAL_REF_INLINE_RE` in `scripts/check_cairn.py`. check_cairn over the three changed files: 1 issue at `1c9d3f51`, OK at `5f520a33`. |

### `12c865c1` (#22, #29) — claim_check

| Check | Result |
|---|---|
| The issues' reproducers | **Closed.** #29's RST file through the CLI: OK on the old checker, 1 hard flag on the new. #22: an archived strategy note resolves; a missing one still flags. |
| `.md` behaviour through check_cairn | **Unchanged apart from the intended effect.** check_cairn (`--no-content-scan`) over all 328 `.md` files of the HEAD tree, once with the old claim_check and once with the new: the new one removes 13 flags — every one a citation of an archived strategy note — and adds none. |
| link_check | **Untouched.** It has its own `scannable_lines` and reads `*.md` only. |
| One fence rule for registry and scan | **True in the code** (`scripts/claim_check.py:1268` feeds both walks). **No test pins it → IB7.** |
| `_LIFECYCLE_DOC_RE` | **Untouched.** The one walk left on the default (`parse_header_status`) runs only for proposal and plan `.md` files, so it never sees an `.rst`. |
| Can the tests fail? | **Yes.** Both behaviour tests red on the old checker; keeping fences in the scan turns the RST test red. |
| Pinned line count | `scripts/claim_check.py` is 1704 lines; check_cairn OK on `docs/tool-usage.md`. |

### `12d363ec` (#26) — the board's disposition copy

| Check | Result |
|---|---|
| The named source exists and governs the four dispositions | **Yes** (`templates/core/dev/plans/_template.md:204`). |
| It carries everything the board copy restates | **No → IB6.** |

### `5f520a33` (#23 Finding A) — the session-start skill

| Check | Result |
|---|---|
| The columns it now names | **True.** `_FIELDS` in `tools/board.py` is Status, Review, Plan review, Opened, Source proposal; rows carry kind and artifact; templates and archives are excluded by default; the footer says the view is derived. The dropped "header names the `HEAD`" claim was false — the board prints no HEAD. Checked against `tools/board.py --archive` on the live tree (123 rows). |
| The same claim elsewhere | **Survives in the canonical doctrine → IB4.** |

### Callers, across the batch

17 test files — claim_check, check_cairn, link_check, loop fidelity,
evolution_infer, incident-trackers, the session kernel and routines, skills
install and matrix, verify_integrity, the board, the default security stance,
slot merge, upgrade: **347 passed, 1 failed** on `5f520a33`; **339 passed, the
same 1 failed** on `5aabfdb3`. The difference is the 8 new nodes (IB8). The one
failure needs a git checkout (`git ls-files`) and passes in the live checkout.

## Findings

### [IB1] blocking (for closing #15; the commit stands) — the default mode still reports a silent zero for the issue's own trackers

**What.** Discovery mode still skips, without a word, any file that has no
`## Incidents` heading (`tools/evolution_infer.py:319`). The new `READ` block
prints only when something was read (`tools/evolution_infer.py:361`). The
issue's two trackers have no such heading. The issue shows it: the old gate,
pointed at one of them with `--trackers`, returned an empty fail-closed list,
and the old gate fails closed on a missing window line whenever the heading is
present. The issue says that window line is missing too.

**Evidence.** I rebuilt the issue's two tables, with no heading and no window
line, under a scratch `dev/measurement/`:
`| Date | Event class | Brief | Recovery / outcome |` and
`| Date | Type | File | Commit(s) | Note |`. In the default mode the old and new
gates print byte-identical human output — `RATE-LIMIT SUGGESTIONS: none.` —
and exit 0. Through `_run_evolution_infer`, as session-start calls it, the
result is the same. The JSON differs only by `"fail_closed_reasons": {}` and
`"trackers_read": []`. Named with `--trackers`, the new gate exits 3 with a
reason, so that half is fixed.

That default run is the issue's first measured command, and it is the command
session-start runs. So the adopter still sees a clean `none` and reads it as
health. The commit message is accurate: its fail-closed bullet says "for a
tracker named with --trackers". But the issue's direction (2), "say what is
being read", is not met for a file the gate passes over.

**Fix.** Keep exit 0 in discovery, which
`bootstrap/tests/test_evolution_infer.py:191` pins, and say what was skipped:
- one `SKIPPED` line per discovered file with no `## Incidents` table;
- a `trackers_skipped` JSON key;
- an explicit "no incident tracker found under dev/measurement/" when nothing was read.

Add a test with the issue's shape in discovery mode. This touches
`tools/evolution_infer.py`, so it needs another scoped `--finalize`. It does not
touch the engine package.

### [IB2] blocking — the `--finalize` hint matches the marker text anywhere, and a shipped file quotes it

**What.** `verify_integrity` puts a file in the hint when the raw bytes
`<!-- cairn:customized -->` appear anywhere in it
(`bootstrap/verify_integrity.py:48`, `bootstrap/verify_integrity.py:117`). The
default-on module `templates/modules/default-on/documentation-plan.md:148`
quotes the marker in prose. So every installed
`dev/modules/documentation-plan.md` carries it from the start, with no slot
involved.

**Evidence.** In Cairn's own tree, `verify_integrity --target .` names exactly
one file in the hint: `dev/modules/documentation-plan.md`. That file has no
`cairn:slot` at all; the marker appears once, in prose, at
`dev/modules/documentation-plan.md:148`. On a scratch install I appended an
unrelated line to that file. verify_integrity said it is "usually a slot you
filled on purpose" and printed the `--finalize` command for it.

The commit says the tool "never invites blessing an unexplained change". The
code comment says that suggesting `--finalize` for any other mismatch "would
invite an adopter to bless a change nobody can explain". That is what happens
here, on a trust check. The test cannot see it: its fixture appends the marker
to the end of `AGENTS.md`, outside any slot, so it pins "marker anywhere" rather
than "a slot was filled".

**Fix.** Use the engine's notion of a customized slot: the marker inside a
`cairn:slot` body, matched the way `bootstrap/_scaffold/slotmerge.py:88` matches
it (`<!--\s*cairn:customized\s*-->`, case-insensitive). Inline the pattern if
the narrowed trust-anchor imports should stay narrow. This also closes the
opposite gap: today a marker written `<!--cairn:customized-->`, which the merge
honours, gets no hint.

Change the test to fill a real slot, and add a control: an edit to
`dev/modules/documentation-plan.md` gets no hint. The fix stays in
`bootstrap/verify_integrity.py`, so the AST baseline is not affected.

### [IB3] non-blocking (timing: before the AST re-anchor) — the #11 remedy fails for an install profile with no axes

**What.** The new message says to add the token to `dev/.cairn/profile.yml`,
"the profile you installed with". The resolver uses that file only when all six
axes resolve. Otherwise it warns and seeds nothing
(`bootstrap/_scaffold/upgrade.py:268`). The Appendix B example profile
(`bootstrap/BOOTSTRAP.md:701`) has a literal `modules:` list, no preset and no
axes, and it installs cleanly.

**Evidence.** I installed with that profile and tried to adopt
`python-security`:
1. The adopt is refused, as it should be.
2. I copied the install profile to `dev/.cairn/profile.yml` and added `python_package: mypkg`.
3. The adopt is refused again, now with `[warn] … missing axis(es): age, size, complexity, language, human_team, agent_team … (upgrade --init-lock shows the required shape)` (`bootstrap/_scaffold/upgrade.py:285`).
4. `--init-lock` on that tree answers "already exists; nothing to migrate" (`bootstrap/_scaffold/upgrade.py:1187`).

So the adopter is sent back to the same no-op this commit removed, one step
later. Adding the six axes makes the adopt succeed.

**Fix.** Make the message ask for a complete profile: a `preset:` or all six
axes, plus the token. The message lives in `_cmd_adopt_module`, the one CHANGED
symbol, so land this before the re-anchor and the baseline moves once. The
warning's own `--init-lock` pointer predates this batch, and changing it would
change a second symbol (`_resolve_current_profile`).

### [IB4] non-blocking — #23 Finding A's false column list survives in the doctrine the skill defers to

`doctrine/session-routines.md:52` to `:55` still promises six things the board
does not report: owner role, work-intent, review obligation, evidence, what
blocks it, and row validity. It also promises a header that names `HEAD`. The
skill calls that file its canonical doctrine. So the skill and its source now
disagree, and an agent reading the doctrine is set up for the misreading the
commit itself names: an absent column read as "nothing blocks".

The commit records Finding B as not done, but says nothing about this.
**Fix:** make the same descriptive correction in that paragraph, or note on #23
that Finding A is closed in the skill only.

### [IB5] non-blocking — #20's N/A instruction survives one hop away

`templates/modules/default-on/security-verification.md:46` still says that if
the module is not installed, "replace this section with `N/A:
security-verification not installed`. An unfilled slot is a review finding."
Cairn's copy at `dev/modules/security-verification.md` says the same. "This
section" is the text that merges into the slot, and the corrected AGENTS.md
guidance sends the reader to this file.

The reach is limited: in an adopter tree the file exists only when the module is
installed. **Fix:** drop the sentence, or point it at the AGENTS.md guidance.

### [IB6] non-blocking — the board names a source that lacks part of what the board restates

The board's restated `accept` bullet carries the scope-cut / scope-reduction
rule (`templates/core/dev/PLANNING.md:107` onward), and the commit notes that
`test_scope_reduction_trap` pins that rule on the board. The section the board
now says to cite instead, `dev/plans/_template.md` > *Dispositions*, does not
contain that rule. It lives in the same template's `## Scope delta`
(`templates/core/dev/plans/_template.md:110`) and in `doctrine/lifecycle.md:559`.

Separately, the named section points its own *why* at `doctrine/plans.md` >
"Archive precondition" (`templates/core/dev/plans/_template.md:232`).
`doctrine/plans.md` has no such section; `doctrine/plans.md:920` itself points
to `doctrine/lifecycle.md`. So the board (lifecycle.md) and the source it names
(plans.md) disagree about where the why lives, and the source is the one that is
wrong. That pointer predates this batch, but this commit now sends citers to it.

**Fix:** name *Dispositions* and *Scope delta* in the board line, and point the
template at `doctrine/lifecycle.md`.

### [IB7] non-blocking — two claims no test pins

| Mutation | Outcome |
|---|---|
| claim_check: the registry parse keeps Markdown fences on `.rst` while the scan drops them | survives (77 passed). Measured effect: a `Proposed path:` declaration between two tilde underlines is lost, and the declared path, cited later, hard-flags. The commit's "the two walks cannot disagree" holds in the code, not in a test. |
| evolution_infer: the `READ` line's `occurred_in_window` count ignores the cutoff | survives (14 passed). No test has an out-of-window `occurred` row, so the count the new summary prints is unchecked. |

**Fix:** add one `.rst` test with a declaration between underlines, and add one
out-of-window row to `test_columns_are_read_by_name_not_position`.

### [IB8] non-blocking — eight new pinned-collection nodes are missing from the re-anchor row

`--collect-only`, diffed between `5aabfdb3` and `5f520a33`: four frozen test
files gain 8 nodes and lose none. `test_upgrade.py` gains 1,
`test_evolution_infer.py` 3, `test_verify_integrity.py` 1, and
`test_claim_check_module.py` 3. The queued re-anchor row lists the node changes
the ceremony should expect (`dev/PLANNING.md:182`), and this batch adds to them
without saying so. The changed frozen-file hashes are covered, because that row
says to derive the set from the manifest at ceremony time. The collection is
not. **Fix:** name the 8 at the row's next serialization point, or in the AST
re-anchor commit's body.

## Seen, not raised

* **`1c9d3f51` landed with check_cairn red.** Its verification names
  claim_check and link_check, not check_cairn. `90236088` repaired it one second
  later, so the range ends green. Boundary A asks for the standing gates of
  every touched surface.
* **`e23aad28`'s test figure.** The body says `test_verify_integrity 15
  passed`; the file collects 14, at that commit and at HEAD. A figure slip, and
  a commit body cannot be corrected.
* **The install accepts an angle-bracket placeholder token.** A profile with
  `python_package: "<my package>"` installs `python-security` with that value:
  the install-time `missing_required_tokens` does not test the `<...>` form, as
  `_adopt_token_unfilled`'s docstring already records. This predates the batch.
  It never reaches the adopt refusal, because a filled token selects the module
  at install.
* **incident-trackers' "Merged into" text has no `cairn:merge-target`.** Nothing
  merges it mechanically, so the new "Adds to" is a citation. That is the
  option #21 proposed. The issue's own open question (was the slot retired or
  lost?) remains open.
* **`_slot_is_empty`'s docstring** says comments do not count as content, but
  the code (`body.strip() == ""`) counts them. The new AGENTS.md prose
  ("anything written between the markers") matches the code, so it is correct.
* **A line citation drifted by four lines.**
  `templates/modules/default-on/run_security_verification.py:128` cites
  `bootstrap/verify_integrity.py:63-111` for the record loop, which now spans
  roughly lines 67 to 118. It still lands in the right function.
* **The board's AST sentence** ("separate and current", `dev/PLANNING.md:186`)
  has been false since `a01f1774` and stays false until the Maintainer
  re-anchors. This is expected.

**Disposition**: revise with follow-up commits, not reverts. Fix IB1 and IB2
before #15 and #10 close. Land IB3 in `_cmd_adopt_module` before the AST
re-anchor, so the baseline moves once. IB4 through IB8 can ride any later
commit.

## Response -- Claude Opus 5.5 (implementer) -- 2026-10-17

All eight findings accepted and fixed as follow-up commits. Nothing was
reverted. Each fix that changes behaviour landed with a test that was red
before it.

| Finding | Disposition | Commit |
|---|---|---|
| IB1 (blocking) | **accept.** Discovery lists every file it skipped (`SKIPPED`, and `trackers_skipped` in JSON). A run that read no tracker says "the gate evaluated nothing" instead of a bare `none`. Discovery still exits 0. The new tests use the issue's own table shape. | `2ea3f869` |
| IB2 (blocking) | **accept.** The hint requires the marker inside a `cairn:slot` body, in any spacing or case the merge engine accepts. The test fills a real slot with the compact marker; the control quotes the marker in prose outside any slot. `verify_integrity --target .` no longer names `dev/modules/documentation-plan.md`. | `70e87171` |
| IB3 | **accept, before the re-anchor.** The refusal names both complete shapes (a `preset:` line, or all six axes, listed from `_AXES`). The new test installs from a literal module list and follows the message to a successful adopt. | `29a4d1da` |
| IB4 | **accept.** The doctrine paragraph now names the columns the board prints, matching the skill. | `1695967e` |
| IB5 | **accept.** Both copies of the module say to leave the slot body empty. | `1695967e` |
| IB6 | **accept, both parts.** The board names *Scope delta* beside *Dispositions*. The plan template's "why" points at `doctrine/lifecycle.md`. | `1695967e` |
| IB7 | **accept, both parts.** The out-of-window row went in with IB1. The `.rst` declaration test is in `995291f6`. | `2ea3f869`, `995291f6` |
| IB8 | **accept.** The queued re-anchor row lists all 13 nodes the batch adds, by file and name. | `1695967e` |

**Seen, not raised:**
- **`_slot_is_empty`'s docstring: fixed** in `995291f6`.
- **The board's AST sentence: corrected** in `1695967e`. It now says one more re-anchor is owed.
- **`1c9d3f51` landing with check_cairn red: accepted as a process slip.** check_cairn now runs on every touched prose file before commit.
- **The `e23aad28` figure: acknowledged.** A commit body cannot be corrected.
- **incident-trackers' citation: as #21 proposed.** No change.

Two items are recorded on the board rather than fixed in this batch:
- **The install accepts an angle-bracket placeholder.** Fixing it changes what `missing_required_tokens` accepts on every install path. It is a defect repair in its own right, so it gets its own failing test and its own code review, not a ride on this batch's.
- **The drifted line citation in `run_security_verification.py:128`.** The dispatcher is a Security-Review surface, so a comment-only edit is not worth a Security Review. It is fixed at the next change to that file.

**Outside the findings.** `ef1b833d` removes the team-gated dual-review module's stale "a different agent type" requirement for contract-touching code review. Doctrine and AGENTS.md had already dropped it. The verification-practice proposal's author found it while checking citations.

**AST.** Two symbols are now CHANGED: `_cmd_adopt_module` (IB3) and `_slot_is_empty` (docstring only). Both go in the one pending Maintainer re-anchor. Nothing else in the engine package moved.

**Second round.** Not requested. The follow-ups answer findings and introduce no new surface. The one exception is `ef1b833d`, which is prose only and reverses a stale rule to match doctrine. Boundary B, the full suite, runs after the re-anchor and before the push.
