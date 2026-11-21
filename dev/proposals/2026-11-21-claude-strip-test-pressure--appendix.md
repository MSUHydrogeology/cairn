# Appendix: what became of each sentence

This is the appendix of `dev/proposals/2026-11-21-claude-strip-test-pressure.md`. It records, for every row of the reader's inventory in the files that were edited, what the row became: `kept` under section C, `rule A`, `rewritten`, `removed`, or `undecided`. The row numbers are the inventory's. Five agents made the edits, one group of files each, on 2026-11-21; their tables follow as they wrote them. Rows in the security modules, the protected-surfaces rule and the testing module were not edited and are not listed.

## After the five groups

Strategy made three more edits for consistency, by exact replacement (commit `169fc9dc`):

- Both copies of the collaboration file: the sentence that gave a review the verdict `WIDER RUN REQUIRED` now says that a review names a changed behaviour that has no check at all.
- `docs/methodology/plans.md`, rows 357 and 358: the passage that told agents to split a run at the test runner's file limit is replaced by two sentences: do not split a selection to get under the limit, and never use the full-suite override outside certification.
- `docs/methodology/plans.md`: the heading sentence that called Boundary B "joined evidence for an arc" now calls it the whole suite at certification.

Answers Strategy gave to the groups' questions: row 29 was rewritten to ask for direct evidence; the "joined integration run" became the certification run; rows 158 and 514 were kept, because a question about whether tests are worth their runtime pushes the number of tests down; row 498 was left as it is, with the testing module, by the Maintainer's word.


## Group G1

### Rows G1 (entry files)

Paired rows: own tree row / shipped row. Same outcome for both unless stated.

| row | file:line | kind | outcome | new words / clause kept under |
|---|---|---|---|---|
| 1 / 662 | session-end SKILL:70 (both trees) | run-tests | rewritten | list now "(doc builds, changelog cadence, foldback capture)" |
| 2 / 663 | session-end SKILL:88 | run-tests | removed | smoke-command sentence removed (file states no rule on tests) |
| 3 / 664 | session-end SKILL:90 | not-run-ledger | removed | removed with row 2 |
| 4 / 665 | session-end SKILL:91 | other | kept | C: certification and plan-named requirement runs stand |
| 5 / 666 | session-end SKILL:96 | evidence-as-runs | removed | smoke example paragraph removed |
| extra | session-end SKILL:93 (both) | neighbour | rewritten | "a smoke result does not replace them..." clause cut; sentence ends "existing schedule." (the smoke result no longer exists) |
| 6 / 667 | session-start SKILL:180 | add-test | rewritten | "(i) a test or a direct check reproduces it"; "all three conditions" became "both conditions" (extra fix) |
| 7 / 668 | session-start SKILL:181 | run-tests | removed | condition (iii) removed |
| 8 / 669 | session-start SKILL:184 | add-test | rewritten | code, and a test only where none covers it, with no proposal. |
| 9 / 670 | session-start SKILL:188 | other | kept | not about tests: the proposal as the record |
| 10 / 671 | session-start SKILL:206 | evidence-as-runs | kept | not about runs: commit-body record, no test named |
| 11 / 672 | session-start SKILL:212 | other | kept | C: a red test from a Maintainer-only step is never committed (failing check not weakened) |
| 12 / 673 | session-start SKILL:226 | add-test | rewritten | show the fault yourself (a new test only where none covers it) from a promise the repository makes |
| 13 / 674 | session-start SKILL:232 | other | kept | C: a failing check you cannot explain stops work |
| 14 / 675 | session-start SKILL:233 | not-run-ledger | rewritten | End with the books: commits (ids), items parked, what was not checked, "nothing pushed" (disposition 6) |
| 15 / 424 | AGENTS.md:19 | other | kept | C: unmet checks go to the Maintainer (declined blocking finding) |
| 16 / 425 | AGENTS.md:36 | reviewer-asks | kept | C: says what was not covered; unsupported assertion does not clear a review |
| 17 / 426 | AGENTS.md:36 | not-run-ledger | kept | C: saying plainly what was not checked |
| 18 / 427 | AGENTS.md:51 | not-run-ledger | kept | C: saying plainly what was not checked |
| 19 / 428 | AGENTS.md:69 | other | kept | pointer to "Verification"; not a request for a test |
| 20 / 429 | AGENTS.md:71 | select-by-file | rewritten | Run the fewest tests that show a change is right, once; prose takes the prose gates. The whole suite runs at certification. |
| extra | AGENTS.md:71 (both) | follow-on | removed | the tier-tool sentence and the "pass the reviewed range" sentence, as the brief said |
| 21 / 430 | AGENTS.md:73 | run-tests | kept | C: tells an agent to run a check tool (claim check) |
| 22 / 431 | AGENTS.md:73 | other | kept | C: keeps named checks honest |
| 23 / 432 | AGENTS.md:73 | control | kept | C: known-positive case for a search that finds nothing |
| 24 | RULES.md:9 | select-by-file | rewritten | Run the fewest tests that show a change is right, once; for prose, the prose gates (pointer and certifying-run sentence unchanged) |
| 25 | RULES.md:22 | other | kept | not about tests: routing table row |
| 224 | conventions.md:33 | add-test | kept | C: names meaningful refusals as what to test |
| 225 | custom_session_routines.md:36 | run-tests | removed | whole smoke-selection paragraph and code block |
| 226 | custom_session_routines.md:43 | evidence-as-runs | removed | removed with row 225 |
| 227 | custom_session_routines.md:46 | not-run-ledger | removed | removed with row 225 |
| 228 | custom_session_routines.md:50 | other | kept | C: certification and plan-named requirement runs stand |
| 229-235 | development-environment.md:12,58,62,100,143,157,175 | machine facts | kept | not about asking for tests: machine setup facts and interpreter notes |
| 238 | working-agreements.md:29 | not-run-ledger | kept | C: saying plainly what was not checked |
| 239 | working-agreements.md:33 | add-test | kept | the Maintainer's own quoted rule; agrees with the new rule |
| 240 | working-agreements.md:34 | select-by-file | rewritten | "...scan the test files for six-word runs from the old text. Delete them." (tail about running a few tests removed) |
| 241 | working-agreements.md:35 | control | kept | disposition 5: existing controls stay |

Undecided: none.

### Totals after edits (measured)

- `cat AGENTS.md CLAUDE.md RULES.md | wc -w` = 1577 (limit 2000)
- `cat templates/core/AGENTS.md templates/core/VENDOR.md templates/core/RULES.md | wc -w` = 1478 (limit 1500)

### Words before -> after

AGENTS.md 1051 -> 1034; templates/core/AGENTS.md 1262 -> 1243; RULES.md 230 -> 232;
custom_session_routines.md 413 -> 323; working-agreements.md 945 -> 932;
session-start SKILL (each copy) 2333 -> 2336; session-end SKILL (each copy) 1047 -> 943.
conventions.md and development-environment.md unchanged.

## Group G2

### rows-G2 (dev/agent_collaboration.md rows 26-78; template twin rows 435-491 follow the same outcome)

| Row | File:line | Kind | Outcome | New words / clause kept |
|---|---|---|---|---|
| 26 | dev:64 | reviewer-asks | kept | not about tests; says what closes a finding |
| 27 | dev:77 | reviewer-asks | kept | not about tests (skepticism toward a clean pass) |
| 28 | dev:81 | reviewer-asks | kept | saying plainly what was not checked |
| 29 | dev:84 | reviewer-asks | rewritten | "A claim about how the code will behave needs direct evidence: something that would fail if the claim were wrong was read, run or checked;" (coordinator's answer) |
| 30 | dev:85 | reviewer-asks | rewritten | "Check the failing path through the public entry point" |
| 31 | dev:88 | control | kept | known-positive case for a pass by finding nothing |
| 32 | dev:92 | reviewer-asks | rewritten | "Every finding names what closes it: exact words, code, a guard, doc..." |
| 33 | dev:98 | not-run-ledger | kept | saying plainly what was not checked |
| 34 | dev:104 | evidence-as-runs | kept | says what remains uncertain |
| 35 | dev:105 | control | kept | eases pressure; no test asked |
| 36 | dev:106 | control | rewritten | new security check "is shown once to refuse one planted bad input, with the command and result recorded" (disp 5); existing controls kept |
| 37 | dev:108 | control | kept | check of a model result; existing controls |
| 38 | dev:115 | evidence-as-runs | kept | unsupported assertion does not clear a review |
| 39 | dev:140 | not-run-ledger | kept | saying plainly what was not checked |
| 40 | dev:193 | not-run-ledger | kept | saying plainly what was not checked |
| 41 | dev:281 | not-run-ledger | kept | saying plainly what was not checked |
| 42 | dev:281 | reviewer-asks | removed | Question 3 forward-test sentence (disp 3) |
| 43 | dev:283 | reviewer-asks | rewritten | disp 3 exact words: closed by exact words or code; failing test only when words cannot show the fault |
| 44 | dev:283 | before-after-hosts | rewritten | implementer runs it once, unchanged, after the fix; changed test is a decline; Security Review not bound |
| 45 | dev:283 | add-test | kept | names a test as a guard |
| 46 | dev:283 | run-tests | rewritten | "A passing test is not proof that a fix is right. No second read of the fix follows, except after a failed joined integration run." |
| 47 | dev:287 | reviewer-asks | kept | review rules on new refusals; existing refusals kept |
| 48 | dev:291 | add-test | kept | defines a cheap follow-up; asks no test |
| 49 | dev:301 | run-tests | kept | already reruns only the affected check; within rule A |
| 50 | dev:321 | other | kept | plan-finish rule; asks no run |
| 51 | dev:343 | run-tests | kept | tells an agent to run a check tool |
| 52 | dev:345 | run-tests | kept | check tools; a figure counts only if true |
| 53 | dev:348 | add-test | rewritten | "with a test only if no existing test would have caught the fault" (disp 2) |
| 54 | dev:351 | add-test | rewritten | `-- test <path::node> or none --` |
| 55 | dev:357 | evidence-as-runs | kept | commit-body length rule; verification need not be a run |
| 56 | dev:363 | run-tests | rewritten | "stays required at certification, including slow or scientific runs" |
| 57 | dev:365 | add-test | rule A | rule A, in the proposal's words, plus its two following sentences |
| 58 | dev:365 | add-test | kept | names tests as guards; one check per security class |
| 59 | dev:365 | run-tests | rule A | developmental-test run sentence replaced by rule A |
| 60 | dev:365 | add-test | kept | limits tests; no new ask |
| 61 | dev:365 | control | kept | eases pressure |
| 62 | dev:365 | add-test | kept | scientific benchmark guidance; the testing module is held |
| 63 | dev:365 | select-by-file | rule A | selection by files replaced by rule A |
| 64 | dev:365 | other | removed | "Agents select routinely, reviewers challenge..." goes with selection |
| 65 | dev:367 | run-tests | removed | joined integration selection (disp 1) |
| 66 | dev:367 | not-run-ledger | rewritten | "Before arc completion or release, one line says what was not checked." |
| 67 | dev:367 | run-tests | removed | reuse results / rerun interactions |
| 68 | dev:367 | run-tests | kept | a failing check stays work; not weakened |
| 69 | dev:367 | run-tests | removed | tied to the removed selection |
| 70 | dev:369 | run-tests | kept | describes a boundary; asks no run |
| 71 | dev:369 | reviewer-asks | rewritten | "closed by the review's exact words or code, or its failing test where words cannot show the fault" |
| 72 | dev:372 | evidence-as-runs | kept | cost record; asks no run |
| 73 | dev:380 | select-by-file | rewritten | "runs the claim, link, snippet and neutrality gates." (tests that read the file dropped) |
| 74 | dev:380 | select-by-file | removed | search for readers and byte pins |
| 75 | dev:380 | run-tests | removed | suite-run sentence; rule A governs |
| 76 | dev:380 | evidence-as-runs | kept | a figure given must be true and attributable |
| 77 | dev:411 | run-tests | removed | fast smoke sentence |
| 78 | dev:411 | other | kept | slow tests at release / required by plan or security requirement |
| 435-491 | template | same | same as the dev twin | template twin of each row above, same outcome |
| 443 | tmpl:116 | not-run-ledger | kept | reading aid does not downgrade a required tier |
| 447 | tmpl:123 | control | kept | preserves security checks |
| 467 | tmpl:368 | not-run-ledger | kept | certification record (certification kept) |
| 482 | tmpl:374 | run-tests | removed | fragment of the joined-integration sentence (with 477) |
| extra | dev:411 / tmpl | | rewritten | "Change checks and joined Boundary B remain due on their schedules." (smoke clause dropped; it named the removed smoke run) |

Extra rows (coordinator's answer 2, both copies): added "Boundary B is the whole suite at certification, before a release is cut." after "Boundary A is scoped iteration."; "failed joined integration run" -> "failed certification run" (row 46 sentence); "joined Boundary B" -> "Boundary B" (two places: retries, goodnight); "one joined integration run" -> "one certification run" (Plans and records). No sentence left that makes no sense.

Not touched (note): the template-only sentence "A whole suite runs only when a project requirement calls for it, and a reviewer never runs one" (no row); rule A governs where it differs.

Words before / after (wc -w): dev/agent_collaboration.md 5562 / 5569; templates/core/dev/agent_collaboration.md 5595 / 5602.

## Group G3

### Rows G3

| row | file:line | kind | outcome | new words / clause |
|---|---|---|---|---|
| 153 | dev/plans/_template.md:114 | reviewer-asks | kept | kept: not about tests |
| 154 | dev/plans/_template.md:116 | reviewer-asks | rewritten | the input or case that breaks it, and what was tried |
| 155 | dev/plans/_template.md:124 | reviewer-asks | rewritten | each ending in the file, line, reasoning or direct check that backs it (disp 4) |
| 156 | dev/plans/_template.md:126 | reviewer-asks | rewritten | Question 3 names what would show it wrong even when there are no findings (disp 3) |
| 157 | dev/plans/_template.md:128 | reviewer-asks | kept | C: unsupported assertion does not clear a review; gaps named |
| 158 | dev/plans/_template.md:133 | reviewer-asks | kept | kept by the Maintainer's answer: it pushes the number of tests down, not test pressure |
| 159 | dev/plans/_template.md:178 | evidence-as-runs | rewritten | Point to what was read or checked directly and state the result (disp 4) |
| 160 | dev/plans/_template.md:257 | other | kept | kept: not about tests |
| 161 | dev/plans/_template.md:267 | other | kept | C: failing or missing checks stay open work |
| 162 | dev/plans/_template.md:277 | evidence-as-runs | kept | kept: not about tests |
| 163 | dev/plans/_template.md:284 | add-test | rewritten | Add a test only for a behavior that no existing test covers, and then one (disp 2) |
| 164 | dev/plans/_template.md:290 | control | kept | C: existing negative controls and security checks |
| 165 | dev/plans/_template.md:312 | run-tests | kept | C: run the prose-integrity gate (check tool) |
| 166 | dev/plans/_template.md:315 | run-tests | kept | C: run the link check (check tool) |
| 167 | dev/plans/_template.md:349 | select-by-file | rewritten | name promises and entry points; the rule on tests is in agent_collaboration > Verification |
| 168 | dev/plans/_template.md:351 | run-tests | removed | selection, reuse and widening rules removed (B1) |
| 169 | dev/plans/_template.md:352 | run-tests | removed | selection, reuse and widening rules removed (B1) |
| 170 | dev/plans/_template.md:354 | control | removed | selection, reuse and widening rules removed (B1) |
| 171 | dev/plans/_template.md:355 | add-test | kept | C: names a test as a guard |
| 172 | dev/plans/_template.md:356 | evidence-as-runs | rewritten | Forward behavior needs evidence before completion: read, reasoned or checked directly; a run is not required (disp 4) |
| 173 | dev/plans/_template.md:358 | not-run-ledger | kept | C: failed required evidence keeps work open |
| 174 | dev/plans/_template.md:359 | control | kept | C: security checks, independent scientific checks, controls |
| 175 | dev/plans/_template.md:365 | select-by-file | removed | test selector run and range removed (B1) |
| 176 | dev/plans/_template.md:367 | run-tests | kept | C: run the prose gate (check tool) |
| 177 | dev/plans/_template.md:368 | select-by-file | removed | test selector run and range removed (B1) |
| 178 | dev/plans/_template.md:388 | not-run-ledger | kept | kept: not about tests |
| 179 | dev/plans/_template.md:388 | not-run-ledger | rewritten | Say in one line what was not checked; tests not run need no list and no home (disp 6) |
| 180 | dev/plans/_template.md:388 | not-run-ledger | kept | Home rule for remaining work; not about tests |
| 181 | dev/plans/_template.md:388 | not-run-ledger | kept | C: the Maintainer's word on deferrals |
| 182 | dev/plans/_template.md:389 | add-test | kept | C: names a test as a guard |
| 183 | dev/plans/_template.md:423 | reviewer-asks | rewritten | each ending in the file, line, reasoning or direct check that backs it (disp 4) |
| 184 | dev/plans/_template.md:441 | not-run-ledger | rewritten | Report what was read and checked directly and any unresolved or unmeasured cases concisely |
| 185 | dev/plans/_template.md:450 | reviewer-asks | rewritten | closes with exact words or code, or a failing test only when words cannot show the fault (disp 3) |
| 186 | dev/plans/_template.md:458 | reviewer-asks | rewritten | each ending in the file, line, reasoning or direct check that backs it (disp 4) |
| 187 | dev/plans/_template.md:461 | reviewer-asks | kept | kept: not about tests |
| 188 | dev/plans/_template.md:463 | reviewer-asks | rewritten | the input or case that breaks it, and what was tried |
| 189 | dev/plans/_template.md:468 | reviewer-asks | kept | C: keeps existing checks |
| 190 | dev/plans/_template.md:472 | reviewer-asks | removed | Bounding verdict and WIDER RUN REQUIRED removed (disp 3) |
| 191 | dev/proposals/_template.md:82 | reviewer-asks | rewritten | each ending in the file, line, reasoning or direct check that backs it (disp 4) |
| 192 | dev/proposals/_template.md:84 | reviewer-asks | rewritten | Question 3 names what would show it wrong even when there are no findings (disp 3) |
| 193 | dev/proposals/_template.md:86 | reviewer-asks | kept | C: unsupported assertion does not clear a review; gaps named |
| 194 | dev/proposals/_template.md:128 | evidence-as-runs | rewritten | Point to what was read or checked directly and state the result (disp 4) |
| 195 | dev/proposals/_template.md:163 | evidence-as-runs | kept | C: a claim of failure needs evidence |
| 196 | dev/proposals/_template.md:173 | other | kept | C: keeps accepted checks; failed checks stay work |
| 197 | dev/proposals/_template.md:179 | other | kept | C: keeps accepted checks; failed checks stay work |
| 198 | dev/proposals/_template.md:208 | evidence-as-runs | kept | heading, not pressure |
| 199 | dev/proposals/_template.md:210 | evidence-as-runs | rewritten | what was read, reasoned or checked directly. Name what would falsify it (disp 4) |
| 200 | dev/proposals/_template.md:213 | add-test | kept | section heading kept; its text is rewritten (row 201) |
| 201 | dev/proposals/_template.md:215 | add-test | rewritten | Propose a test only for a behavior no existing test covers, and then one; points to the rule on tests (disp 2) |
| 202 | dev/proposals/_template.md:225 | select-by-file | rewritten | The full suite is a separate tree-certification run (C); routing by file removed |
| 203 | dev/proposals/_template.md:232 | select-by-file | removed | test-home mapping, tracing and widening removed (B1); disp 2 is stated once above |
| 204 | dev/proposals/_template.md:235 | select-by-file | removed | test-home mapping, tracing and widening removed (B1); disp 2 is stated once above |
| 205 | dev/proposals/_template.md:238 | add-test | removed | test-home mapping, tracing and widening removed (B1); disp 2 is stated once above |
| 206 | dev/proposals/_template.md:239 | other | rewritten | Speed alone does not establish affected coverage |
| 207 | dev/proposals/_template.md:241 | select-by-file | removed | bounded/wide coverage rules removed (B1) |
| 208 | dev/proposals/_template.md:243 | not-run-ledger | kept | C: no claim of covered without evidence; unmet checks stay open |
| 209 | dev/proposals/_template.md:246 | other | kept | C: names check tools |
| 210 | dev/proposals/_template.md:249 | select-by-file | rewritten | routine test choice is the agent's |
| 211 | dev/proposals/_template.md:256 | run-tests | kept | slot describing where the project's checks live |
| 212 | dev/proposals/_template.md:258 | run-tests | rewritten | gallery described; clause that a change runs them removed (B1) |
| 213 | dev/proposals/_template.md:262 | run-tests | kept | slot description of commands, no demand |
| 214 | dev/proposals/_template.md:265 | run-tests | kept | C: check tool |
| 215 | dev/proposals/_template.md:292 | control | kept | C: kept whole (security preflight / independent scientific check) |
| 216 | dev/proposals/_template.md:297 | evidence-as-runs | kept | C: kept whole (security preflight / independent scientific check) |
| 217 | dev/proposals/_template.md:340 | control | kept | C: kept whole (security preflight / independent scientific check) |
| 218 | dev/proposals/_template.md:342 | control | kept | C: kept whole (security preflight / independent scientific check) |
| 219 | dev/proposals/_template.md:351 | reviewer-asks | kept | C: kept whole (security preflight / independent scientific check) |
| 220 | dev/proposals/_template.md:437 | reviewer-asks | rewritten | each ending in the file, line, reasoning or direct check that backs it (disp 4) |
| 221 | dev/proposals/_template.md:447 | reviewer-asks | kept | kept: not about tests |
| 222 | dev/proposals/_template.md:478 | evidence-as-runs | rewritten | Record what was read, reasoned or checked directly, the revision, commands run and one line on what was not checked (disp 4, 6) |
| 223 | dev/proposals/_template.md:480 | not-run-ledger | kept | C: results cited with their limits |
| 509 | templates/core/dev/plans/_template.md:116 | reviewer-asks | kept | kept: not about tests |
| 510 | templates/core/dev/plans/_template.md:118 | reviewer-asks | rewritten | the input or case that breaks it, and what was tried |
| 511 | templates/core/dev/plans/_template.md:126 | reviewer-asks | rewritten | each ending in the file, line, reasoning or direct check that backs it (disp 4) |
| 512 | templates/core/dev/plans/_template.md:128 | reviewer-asks | rewritten | Question 3 names what would show it wrong even when there are no findings (disp 3) |
| 513 | templates/core/dev/plans/_template.md:130 | reviewer-asks | kept | C: unsupported assertion does not clear a review; gaps named |
| 514 | templates/core/dev/plans/_template.md:135 | reviewer-asks | kept | kept by the Maintainer's answer: it pushes the number of tests down, not test pressure |
| 515 | templates/core/dev/plans/_template.md:259 | other | kept | kept: not about tests |
| 516 | templates/core/dev/plans/_template.md:269 | other | kept | kept: not about tests |
| 517 | templates/core/dev/plans/_template.md:279 | evidence-as-runs | kept | kept: not about tests |
| 518 | templates/core/dev/plans/_template.md:286 | add-test | rewritten | Add a test only for a behavior that no existing test covers, and then one (disp 2) |
| 519 | templates/core/dev/plans/_template.md:292 | control | kept | C: existing negative controls and security checks |
| 520 | templates/core/dev/plans/_template.md:309 | run-tests | kept | describes the project's doc tooling to fill in; not a demand |
| 521 | templates/core/dev/plans/_template.md:343 | select-by-file | rewritten | name promises and entry points; the rule on tests is in agent_collaboration > Verification |
| 522 | templates/core/dev/plans/_template.md:345 | run-tests | removed | selection, reuse, widening, test-selector rules removed (B1) |
| 523 | templates/core/dev/plans/_template.md:346 | run-tests | removed | selection, reuse, widening, test-selector rules removed (B1) |
| 524 | templates/core/dev/plans/_template.md:348 | control | removed | selection, reuse, widening, test-selector rules removed (B1) |
| 525 | templates/core/dev/plans/_template.md:349 | add-test | kept | C: names a test as a guard |
| 526 | templates/core/dev/plans/_template.md:350 | evidence-as-runs | rewritten | Forward behavior needs evidence before completion: read, reasoned or checked directly; a run is not required (disp 4) |
| 527 | templates/core/dev/plans/_template.md:352 | not-run-ledger | kept | C: failed required evidence keeps work open |
| 528 | templates/core/dev/plans/_template.md:353 | control | kept | C: security checks, independent scientific checks, controls |
| 529 | templates/core/dev/plans/_template.md:359 | select-by-file | removed | selection, reuse, widening, test-selector rules removed (B1) |
| 530 | templates/core/dev/plans/_template.md:361 | run-tests | kept | C: run the prose gate (check tool) |
| 531 | templates/core/dev/plans/_template.md:368 | evidence-as-runs | kept | C: tree certification is kept |
| 532 | templates/core/dev/plans/_template.md:388 | not-run-ledger | kept | kept: not about tests |
| 533 | templates/core/dev/plans/_template.md:388 | not-run-ledger | rewritten | Say in one line what was not checked; tests not run need no list and no home (disp 6) |
| 534 | templates/core/dev/plans/_template.md:388 | not-run-ledger | kept | kept: not about tests |
| 535 | templates/core/dev/plans/_template.md:388 | not-run-ledger | kept | C: the Maintainer's word on deferrals |
| 536 | templates/core/dev/plans/_template.md:389 | add-test | kept | C: names a test as a guard |
| 537 | templates/core/dev/plans/_template.md:423 | reviewer-asks | rewritten | each ending in the file, line, reasoning or direct check that backs it (disp 4) |
| 538 | templates/core/dev/plans/_template.md:428 | reviewer-asks | kept | kept: not about tests |
| 539 | templates/core/dev/plans/_template.md:441 | not-run-ledger | rewritten | Report what was read and checked directly and any unresolved or unmeasured cases concisely |
| 540 | templates/core/dev/plans/_template.md:450 | reviewer-asks | rewritten | closes with exact words or code, or a failing test only when words cannot show the fault (disp 3) |
| 541 | templates/core/dev/plans/_template.md:458 | reviewer-asks | rewritten | each ending in the file, line, reasoning or direct check that backs it (disp 4) |
| 542 | templates/core/dev/plans/_template.md:461 | reviewer-asks | kept | kept: not about tests |
| 543 | templates/core/dev/plans/_template.md:468 | reviewer-asks | removed | Bounding paragraph removed; the test-removal question is kept (C: keeps existing checks) |
| 544 | templates/core/dev/plans/_template.md:472 | reviewer-asks | removed | Bounding verdict and WIDER RUN REQUIRED removed (disp 3) |
| 545 | templates/core/dev/proposals/_template.md:65 | reviewer-asks | rewritten | each ending in the file, line, reasoning or direct check that backs it (disp 4) |
| 546 | templates/core/dev/proposals/_template.md:67 | reviewer-asks | rewritten | Question 3 names what would show it wrong even when there are no findings (disp 3) |
| 547 | templates/core/dev/proposals/_template.md:69 | reviewer-asks | kept | C: unsupported assertion does not clear a review; gaps named |
| 548 | templates/core/dev/proposals/_template.md:146 | evidence-as-runs | kept | C: a claim of failure needs evidence |
| 549 | templates/core/dev/proposals/_template.md:156 | other | kept | C: keeps accepted checks; failed checks stay work |
| 550 | templates/core/dev/proposals/_template.md:162 | other | kept | C: keeps accepted checks; failed checks stay work |
| 551 | templates/core/dev/proposals/_template.md:191 | evidence-as-runs | rewritten | what was read, reasoned or checked directly; heading kept (disp 4) |
| 552 | templates/core/dev/proposals/_template.md:193 | evidence-as-runs | rewritten | what was read, reasoned or checked directly; heading kept (disp 4) |
| 553 | templates/core/dev/proposals/_template.md:196 | add-test | rewritten | Propose a test only for a behavior no existing test covers, and then one; points to the rule on tests (disp 2) |
| 554 | templates/core/dev/proposals/_template.md:196 | add-test | kept | section heading kept; its text is rewritten |
| 555 | templates/core/dev/proposals/_template.md:198 | add-test | rewritten | Propose a test only for a behavior no existing test covers, and then one; points to the rule on tests (disp 2) |
| 556 | templates/core/dev/proposals/_template.md:203 | select-by-file | rewritten | (Name the project's test homes. Speed alone does not establish affected coverage. ...); mapping and bounded/wide removed (B1) |
| 557 | templates/core/dev/proposals/_template.md:211 | run-tests | kept | slot describing where the project's checks live |
| 558 | templates/core/dev/proposals/_template.md:239 | control | kept | C: kept whole (security preflight / independent scientific check) |
| 559 | templates/core/dev/proposals/_template.md:244 | evidence-as-runs | kept | C: kept whole (security preflight / independent scientific check) |
| 560 | templates/core/dev/proposals/_template.md:287 | control | kept | C: kept whole (security preflight / independent scientific check) |
| 561 | templates/core/dev/proposals/_template.md:289 | control | kept | C: kept whole (security preflight / independent scientific check) |
| 562 | templates/core/dev/proposals/_template.md:298 | reviewer-asks | kept | C: kept whole (security preflight / independent scientific check) |
| 563 | templates/core/dev/proposals/_template.md:367 | reviewer-asks | rewritten | each ending in the file, line, reasoning or direct check that backs it (disp 4) |
| 564 | templates/core/dev/proposals/_template.md:377 | reviewer-asks | kept | kept: not about tests |
| 565 | templates/core/dev/proposals/_template.md:408 | evidence-as-runs | rewritten | Record what was read, reasoned or checked directly, the revision, commands run and one line on what was not checked (disp 4, 6) |
| 566 | templates/core/dev/proposals/_template.md:410 | not-run-ledger | kept | C: results cited with their limits |
| X1 | both plan templates, Verification | extra | removed | "Group equivalent paths." had no selection left to group |
| X2 | both plan templates, verification-commands slot | extra | removed | "This is the iteration scope; do not widen it by judgment." and "The selector claims no unknown dependencies." lost their subject |
| X3 | dev/proposals/_template.md, tests-tier slot | extra | removed | "The plan owns the reviewed change-specific mapping, not a permanent fast set." lost its subject |

Word counts (before -> after):
- dev/plans/_template.md 3955 -> 3850
- templates/core/dev/plans/_template.md 3967 -> 3871
- dev/proposals/_template.md 3928 -> 3803
- templates/core/dev/proposals/_template.md 3446 -> 3422
- total 15296 -> 14946

## Group G4

### Rows for group G4 (published method)

Outcome counts are on the 182 inventory rows; extra rows X1-X10 follow.

| row | file and line | kind | outcome | new words, or clause of C |
|---|---|---|---|---|
| 242 | docs/methodology/dual-review.md:22 | reviewer-asks | rewritten | for code review this states what was checked directly and its outcome concisely |
| 243 | docs/methodology/dual-review.md:30 | reviewer-asks | kept | C: claim of checked only when true; a bare 'checked' is incomplete; say what was not checked |
| 244 | docs/methodology/dual-review.md:33 | reviewer-asks | rewritten | Question 3 names what would show it wrong even when there are no findings. |
| 245 | docs/methodology/dual-review.md:34 | reviewer-asks | kept | C: claim of checked only when true; a bare 'checked' is incomplete; say what was not checked |
| 246 | docs/methodology/dual-review.md:44 | reviewer-asks | kept | C: claim of checked only when true; a bare 'checked' is incomplete; say what was not checked |
| 247 | docs/methodology/dual-review.md:46 | reviewer-asks | kept | C: claim of checked only when true; a bare 'checked' is incomplete; say what was not checked |
| 248 | docs/methodology/dual-review.md:150 | reviewer-asks | rewritten | check the real call chain and real config |
| 249 | docs/methodology/dual-review.md:176 | run-tests | kept | C: not a pressure sentence (plainly not about tests) |
| 250 | docs/methodology/dual-review.md:181 | evidence-as-runs | kept | C: claim of checked only when true; a bare 'checked' is incomplete; say what was not checked |
| 251 | docs/methodology/dual-review.md:200 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 252 | docs/methodology/dual-review.md:206 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 253 | docs/methodology/dual-review.md:224 | reviewer-asks | kept | C: not a pressure sentence (plainly not about tests) |
| 254 | docs/methodology/dual-review.md:232 | other | kept | C: send unresolved blocking findings to the Maintainer |
| 255 | docs/methodology/dual-review.md:243 | reviewer-asks | rewritten | closes by exact words or code, or by the reviewer's failing test where words cannot show the fault |
| 256 | docs/methodology/dual-review.md:334 | reviewer-asks | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 257 | docs/methodology/dual-review.md:335 | reviewer-asks | rewritten | then checks directly the changed public paths, negative or edge cases, cross-surface assumptions |
| 258 | docs/methodology/dual-review.md:337 | reviewer-asks | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 259 | docs/methodology/dual-review.md:339 | reviewer-asks | rewritten | Where a changed behavior has no test at all, a review may name one. |
| 260 | docs/methodology/dual-review.md:341 | run-tests | rewritten | A fix after a failed certification run that changes more than the failing test returns to the same reviewer |
| 261 | docs/methodology/dual-review.md:344 | select-by-file | removed | sentence and its paragraph removed (scoped test mapping; Bounding verdict WIDER RUN REQUIRED; six record-replacement triggers) |
| 262 | docs/methodology/dual-review.md:348 | reviewer-asks | removed | sentence and its paragraph removed (scoped test mapping; Bounding verdict WIDER RUN REQUIRED; six record-replacement triggers) |
| 263 | docs/methodology/dual-review.md:363 | control | kept | C: keeps existing controls, negative controls, known-positive case; new security check shown once |
| 264 | docs/methodology/dual-review.md:365 | evidence-as-runs | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 265 | docs/methodology/dual-review.md:366 | control | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 266 | docs/methodology/dual-review.md:367 | control | kept | C: keeps existing controls, negative controls, known-positive case; new security check shown once |
| 267 | docs/methodology/dual-review.md:368 | evidence-as-runs | rewritten | Claims about forward behavior need a direct check, one run included |
| 268 | docs/methodology/dual-review.md:370 | not-run-ledger | kept | C: claim of checked only when true; a bare 'checked' is incomplete; say what was not checked |
| 269 | docs/methodology/dual-review.md:379 | reviewer-asks | removed | sentence and its paragraph removed (scoped test mapping; Bounding verdict WIDER RUN REQUIRED; six record-replacement triggers) |
| 270 | docs/methodology/dual-review.md:385 | evidence-as-runs | rewritten | records changed promises, the evidence for them, and omissions |
| 271 | docs/methodology/dual-review.md:391 | run-tests | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 272 | docs/methodology/dual-review.md:397 | run-tests | removed | sentence and its paragraph removed (scoped test mapping; Bounding verdict WIDER RUN REQUIRED; six record-replacement triggers) |
| 273 | docs/methodology/dual-review.md:400 | run-tests | removed | sentence and its paragraph removed (scoped test mapping; Bounding verdict WIDER RUN REQUIRED; six record-replacement triggers) |
| 274 | docs/methodology/dual-review.md:401 | run-tests | removed | sentence and its paragraph removed (scoped test mapping; Bounding verdict WIDER RUN REQUIRED; six record-replacement triggers) |
| 275 | docs/methodology/dual-review.md:402 | not-run-ledger | removed | sentence and its paragraph removed (scoped test mapping; Bounding verdict WIDER RUN REQUIRED; six record-replacement triggers) |
| 276 | docs/methodology/dual-review.md:403 | run-tests | removed | sentence and its paragraph removed (scoped test mapping; Bounding verdict WIDER RUN REQUIRED; six record-replacement triggers) |
| 277 | docs/methodology/dual-review.md:405 | run-tests | removed | sentence and its paragraph removed (scoped test mapping; Bounding verdict WIDER RUN REQUIRED; six record-replacement triggers) |
| 278 | docs/methodology/dual-review.md:407 | reviewer-asks | removed | sentence and its paragraph removed (scoped test mapping; Bounding verdict WIDER RUN REQUIRED; six record-replacement triggers) |
| 279 | docs/methodology/dual-review.md:409 | run-tests | removed | sentence and its paragraph removed (scoped test mapping; Bounding verdict WIDER RUN REQUIRED; six record-replacement triggers) |
| 280 | docs/methodology/dual-review.md:421 | reviewer-asks | kept | C: not a pressure sentence (plainly not about tests) |
| 281 | docs/methodology/dual-review.md:449 | reviewer-asks | kept | C: claims checked against the tree directly; committed evidence allowed |
| 282 | docs/methodology/dual-review.md:451 | evidence-as-runs | kept | C: claims checked against the tree directly; committed evidence allowed |
| 283 | docs/methodology/dual-review.md:453 | evidence-as-runs | rewritten | forward behavior needs a direct check, one run included. |
| 284 | docs/methodology/dual-review.md:456 | reviewer-asks | rewritten | Production path checked; the public entry point is checked through |
| 285 | docs/methodology/dual-review.md:470 | control | kept | C: keeps existing controls, negative controls, known-positive case; new security check shown once |
| 286 | docs/methodology/dual-review.md:481 | reviewer-asks | rewritten | every finding states the exact words, code, guard / doc / scope-cut / explicit wontfix that would close it |
| 287 | docs/methodology/dual-review.md:503 | reviewer-asks | kept | C: claim of checked only when true; a bare 'checked' is incomplete; say what was not checked |
| 288 | docs/methodology/dual-review.md:508 | reviewer-asks | kept | C: claim of checked only when true; a bare 'checked' is incomplete; say what was not checked |
| 289 | docs/methodology/dual-review.md:515 | reviewer-asks | kept | C: claim of checked only when true; a bare 'checked' is incomplete; say what was not checked |
| 290 | docs/methodology/dual-review.md:524 | reviewer-asks | rewritten | does the landed check actually reach the public path today? |
| 291 | docs/methodology/dual-review.md:527 | not-run-ledger | kept | C: claim of checked only when true; a bare 'checked' is incomplete; say what was not checked |
| 292 | docs/methodology/dual-review.md:532 | reviewer-asks | kept | C: names a test as a guard / says plainly what was not checked / not a pressure sentence |
| 293 | docs/methodology/dual-review.md:666 | not-run-ledger | kept | C: claim of checked only when true; a bare 'checked' is incomplete; say what was not checked |
| 294 | docs/methodology/dual-review.md:669 | not-run-ledger | kept | C: claim of checked only when true; a bare 'checked' is incomplete; say what was not checked |
| 295 | docs/methodology/dual-review.md:670 | not-run-ledger | kept | C: claim of checked only when true; a bare 'checked' is incomplete; say what was not checked |
| 296 | docs/methodology/dual-review.md:703 | run-tests | rewritten | Include: what shipped, where, the reviewer's deliverable, and procedural constraints |
| 297 | docs/methodology/dual-review.md:734 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 298 | docs/methodology/dual-review.md:756 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 299 | docs/methodology/dual-review.md:759 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 300 | docs/methodology/dual-review.md:762 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 301 | docs/methodology/lifecycle.md:51 | add-test | rewritten | a defect repair: both of (i) a failing-test reproduction, (ii) restores intended behavior with no contract change |
| 302 | docs/methodology/lifecycle.md:59 | add-test | rewritten | code (and a test only where no existing test would have caught the fault), no proposal and no code review |
| 303 | docs/methodology/lifecycle.md:93 | evidence-as-runs | kept | C: cost record, not a test ask |
| 304 | docs/methodology/lifecycle.md:117 | select-by-file | rewritten | the agent chooses its checks under the rule on tests (dev/agent_collaboration.md > Verification); the row's own first sentence kept |
| 305 | docs/methodology/lifecycle.md:293 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 306 | docs/methodology/lifecycle.md:305 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 307 | docs/methodology/lifecycle.md:391 | run-tests | kept | C: sentence tells an agent to run a check tool (check_cairn) |
| 308 | docs/methodology/lifecycle.md:595 | add-test | kept | C: names a test as a guard |
| 309 | docs/methodology/lifecycle.md:633 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 310 | docs/methodology/plans.md:93 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 311 | docs/methodology/plans.md:101 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 312 | docs/methodology/plans.md:253 | add-test | rewritten | two conditions in lifecycle.md (a failing-test reproduction; restores intended behaviour with no contract change) |
| 313 | docs/methodology/plans.md:262 | evidence-as-runs | rewritten | Each plan records the evidence for its changed promises ... completes its required checks, reviews and dispositions |
| 314 | docs/methodology/plans.md:266 | evidence-as-runs | rewritten | its accepted proposal records the evidence for its changed promises and applicable reused evidence |
| 315 | docs/methodology/plans.md:363 | other | kept | not pressure: record format, certification, check tool, or description of an existing guard |
| 316 | docs/methodology/plans.md:370 | select-by-file | rule A | Run the fewest tests that show the change is right, once ... More than this needs the Maintainer's word. (full rule A, once, plus the two governing sentences) |
| 317 | docs/methodology/plans.md:373 | run-tests | rule A | Run the fewest tests that show the change is right, once ... More than this needs the Maintainer's word. (full rule A, once, plus the two governing sentences) |
| 318 | docs/methodology/plans.md:374 | run-tests | kept | C: check tool: standing prose gates stay |
| 319 | docs/methodology/plans.md:375 | select-by-file | removed | sentence removed; rule A governs (or no list and no home needed) |
| 320 | docs/methodology/plans.md:377 | not-run-ledger | kept | C: unknown dependencies are not claimed as covered |
| 321 | docs/methodology/plans.md:378 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 322 | docs/methodology/plans.md:383 | select-by-file | removed | sentence removed; rule A governs (or no list and no home needed) |
| 323 | docs/methodology/plans.md:386 | add-test | kept | C: names a test as a guard / says plainly what was not checked / not a pressure sentence |
| 324 | docs/methodology/plans.md:391 | evidence-as-runs | kept | C: names a test as a guard / says plainly what was not checked / not a pressure sentence |
| 325 | docs/methodology/plans.md:396 | select-by-file | rewritten | then records the changed caller-visible promises and affected components and consumers in the implementation record |
| 326 | docs/methodology/plans.md:399 | select-by-file | removed | sentence removed; rule A governs (or no list and no home needed) |
| 327 | docs/methodology/plans.md:400 | run-tests | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 328 | docs/methodology/plans.md:401 | reviewer-asks | rewritten | claims about forward behavior need a direct check, one run included |
| 329 | docs/methodology/plans.md:402 | evidence-as-runs | rewritten | claims about forward behavior need a direct check, one run included |
| 330 | docs/methodology/plans.md:403 | control | kept | C: keeps existing controls, negative controls, known-positive case; new security check shown once |
| 331 | docs/methodology/plans.md:404 | control | kept | C: keeps existing controls, negative controls, known-positive case; new security check shown once |
| 332 | docs/methodology/plans.md:405 | control | kept | C: keeps existing controls, negative controls, known-positive case; new security check shown once |
| 333 | docs/methodology/plans.md:406 | control | kept | C: keeps existing controls, negative controls, known-positive case; new security check shown once |
| 334 | docs/methodology/plans.md:408 | select-by-file | removed | sentence removed; rule A governs (or no list and no home needed) |
| 335 | docs/methodology/plans.md:409 | select-by-file | removed | sentence removed; rule A governs (or no list and no home needed) |
| 336 | docs/methodology/plans.md:414 | other | rewritten | Agents make this routine choice; independent review challenges the selection |
| 337 | docs/methodology/plans.md:416 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 338 | docs/methodology/plans.md:419 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 339 | docs/methodology/plans.md:421 | run-tests | rewritten | The arc owner records the joined evidence after connected plans finish, or earlier at a named critical shared boundary. |
| 340 | docs/methodology/plans.md:423 | not-run-ledger | rewritten | records the evidence for the final combined revision and, in one line, what was not checked |
| 341 | docs/methodology/plans.md:425 | run-tests | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 342 | docs/methodology/plans.md:427 | run-tests | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 343 | docs/methodology/plans.md:428 | run-tests | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 344 | docs/methodology/plans.md:431 | run-tests | removed | sentence removed; rule A governs (or no list and no home needed) |
| 345 | docs/methodology/plans.md:432 | run-tests | rewritten | At integration or release boundaries, name applicable safety, security, scientific, and release checks |
| 346 | docs/methodology/plans.md:438 | not-run-ledger | kept | not pressure: record format, certification, check tool, or description of an existing guard |
| 347 | docs/methodology/plans.md:449 | run-tests | rewritten | A configured suite member remains required at certification |
| 348 | docs/methodology/plans.md:455 | run-tests | kept | not pressure: record format, certification, check tool, or description of an existing guard |
| 349 | docs/methodology/plans.md:457 | evidence-as-runs | rewritten | The record of such work is the gates run. |
| 350 | docs/methodology/plans.md:468 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 351 | docs/methodology/plans.md:470 | run-tests | rewritten | owner records the joined evidence, unless a named critical shared boundary calls for it earlier |
| 352 | docs/methodology/plans.md:472 | not-run-ledger | rewritten | record the evidence for the final combined revision and, in one line, what was not checked |
| 353 | docs/methodology/plans.md:474 | run-tests | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 354 | docs/methodology/plans.md:477 | run-tests | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 355 | docs/methodology/plans.md:480 | run-tests | kept | C: names a test as a guard / says plainly what was not checked / not a pressure sentence |
| 356 | docs/methodology/plans.md:482 | other | kept | C: names a test as a guard / says plainly what was not checked / not a pressure sentence |
| 357 | docs/methodology/plans.md:485 | run-tests | undecided | tied to the test runner's 40-file limit, which the proposal leaves to the next proposal; left as it is |
| 358 | docs/methodology/plans.md:489 | not-run-ledger | undecided | tied to the test runner's 40-file limit, which the proposal leaves to the next proposal; left as it is |
| 359 | docs/methodology/plans.md:492 | reviewer-asks | removed | paragraph removed (Bounding verdict and wider-run duty; six record-replacement triggers) |
| 360 | docs/methodology/plans.md:496 | run-tests | removed | paragraph removed (Bounding verdict and wider-run duty; six record-replacement triggers) |
| 361 | docs/methodology/plans.md:499 | evidence-as-runs | rewritten | records its changed caller-visible promises, the evidence for them, results and omissions |
| 362 | docs/methodology/plans.md:502 | evidence-as-runs | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 363 | docs/methodology/plans.md:504 | reviewer-asks | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 364 | docs/methodology/plans.md:508 | run-tests | rewritten | Joined evidence does not repeat unchanged behavior solely to bind every result to one revision identifier. |
| 365 | docs/methodology/plans.md:517 | evidence-as-runs | kept | not pressure: record format, certification, check tool, or description of an existing guard |
| 366 | docs/methodology/plans.md:518 | evidence-as-runs | rewritten | <what was read, reasoned or checked directly, any test run once, and results; reused source and limits> |
| 367 | docs/methodology/plans.md:519 | evidence-as-runs | kept | not pressure: record format, certification, check tool, or description of an existing guard |
| 368 | docs/methodology/plans.md:520 | evidence-as-runs | rewritten | **Interpreter/runtime**: <path and version, if a test was run> |
| 369 | docs/methodology/plans.md:522 | evidence-as-runs | kept | not pressure: record format, certification, check tool, or description of an existing guard |
| 370 | docs/methodology/plans.md:524 | evidence-as-runs | rewritten | <tests run once, standing gates, and acceptance commands> |
| 371 | docs/methodology/plans.md:526 | not-run-ledger | kept | not pressure: record format, certification, check tool, or description of an existing guard |
| 372 | docs/methodology/plans.md:527 | evidence-as-runs | kept | not pressure: record format, certification, check tool, or description of an existing guard |
| 373 | docs/methodology/plans.md:528 | not-run-ledger | rewritten | **Known omissions**: <one line: what was not checked> |
| 374 | docs/methodology/plans.md:529 | evidence-as-runs | kept | C: cost record, not a test ask |
| 375 | docs/methodology/plans.md:535 | evidence-as-runs | kept | C: cost record, not a test ask |
| 376 | docs/methodology/plans.md:543 | evidence-as-runs | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 377 | docs/methodology/plans.md:554 | evidence-as-runs | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 378 | docs/methodology/plans.md:557 | run-tests | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 379 | docs/methodology/plans.md:559 | run-tests | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 380 | docs/methodology/plans.md:561 | run-tests | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 381 | docs/methodology/plans.md:572 | reviewer-asks | rewritten | Code review reads the iteration evidence and checks directly what could falsify the change. |
| 382 | docs/methodology/plans.md:573 | reviewer-asks | rewritten | A review finding names the missing behavior; where a changed behavior has no test at all, it may name one. |
| 383 | docs/methodology/plans.md:575 | run-tests | rewritten | A fix after a failed certification run that changes more than the failing test returns to the same reviewer |
| 384 | docs/methodology/plans.md:577 | run-tests | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 385 | docs/methodology/plans.md:581 | run-tests | removed | paragraph removed (Bounding verdict and wider-run duty; six record-replacement triggers) |
| 386 | docs/methodology/plans.md:584 | run-tests | removed | paragraph removed (Bounding verdict and wider-run duty; six record-replacement triggers) |
| 387 | docs/methodology/plans.md:585 | run-tests | removed | paragraph removed (Bounding verdict and wider-run duty; six record-replacement triggers) |
| 388 | docs/methodology/plans.md:586 | not-run-ledger | removed | paragraph removed (Bounding verdict and wider-run duty; six record-replacement triggers) |
| 389 | docs/methodology/plans.md:587 | run-tests | removed | paragraph removed (Bounding verdict and wider-run duty; six record-replacement triggers) |
| 390 | docs/methodology/plans.md:589 | run-tests | removed | paragraph removed (Bounding verdict and wider-run duty; six record-replacement triggers) |
| 391 | docs/methodology/plans.md:591 | reviewer-asks | removed | paragraph removed (Bounding verdict and wider-run duty; six record-replacement triggers) |
| 392 | docs/methodology/plans.md:593 | run-tests | removed | paragraph removed (Bounding verdict and wider-run duty; six record-replacement triggers) |
| 393 | docs/methodology/plans.md:611 | add-test | rewritten | What docs, examples, or checks show the change is right? |
| 394 | docs/methodology/plans.md:672 | reviewer-asks | rewritten | its test, if any, and the stated fence |
| 395 | docs/methodology/plans.md:941 | add-test | kept | C: names a test as a guard / says plainly what was not checked / not a pressure sentence |
| 396 | docs/methodology/plans.md:944 | add-test | rewritten | needs at most a test that fits existing test files |
| 397 | docs/methodology/plans.md:950 | other | kept | not pressure: limits or reuses runs, keeps reviewer off suites, or says a failing check stays open (C: failing check not weakened) |
| 398 | docs/methodology/plans.md:954 | evidence-as-runs | rewritten | The reviewer points to what was read or checked directly, committed evidence or adequate static calculations |
| 399 | docs/methodology/plans.md:957 | control | kept | C: keeps existing controls, negative controls, known-positive case; new security check shown once |
| 400 | docs/methodology/plans.md:958 | control | kept | C: keeps existing controls, negative controls, known-positive case; new security check shown once |
| 401 | docs/methodology/plans.md:961 | not-run-ledger | kept | C: names a test as a guard / says plainly what was not checked / not a pressure sentence |
| 402 | docs/methodology/plans.md:1037 | add-test | kept | C: names a test as a guard / says plainly what was not checked / not a pressure sentence |
| 403 | docs/methodology/plans.md:1049 | not-run-ledger | kept | C: names a test as a guard / says plainly what was not checked / not a pressure sentence |
| 404 | docs/methodology/plans.md:1052 | not-run-ledger | kept | C: names a test as a guard / says plainly what was not checked / not a pressure sentence |
| 405 | docs/methodology/plans.md:1054 | not-run-ledger | rewritten | Evidence not shipped: one line: what was not checked in this plan. Checks not made wait for certification. |
| 406 | docs/methodology/plans.md:1056 | not-run-ledger | removed | sentence removed; rule A governs (or no list and no home needed) |
| 407 | docs/methodology/proposals.md:34 | evidence-as-runs | kept | not pressure: record format, certification, check tool, or description of an existing guard |
| 408 | docs/methodology/proposals.md:134 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 409 | docs/methodology/proposals.md:138 | other | kept | C: not a pressure sentence (plainly not about tests) |
| 410 | docs/methodology/proposals.md:168 | add-test | rewritten | a one-line bug with a reproduction |
| 411 | docs/methodology/proposals.md:173 | evidence-as-runs | kept | not pressure: record format, certification, check tool, or description of an existing guard |
| 412 | docs/methodology/proposals.md:330 | evidence-as-runs | kept | not pressure: record format, certification, check tool, or description of an existing guard |
| 413 | docs/methodology/proposals.md:406 | add-test | kept | C: names a test as a guard |
| 414 | docs/methodology/proposals.md:503 | add-test | kept | C: names a test as a guard |
| 415 | docs/methodology/rationale.md:445 | add-test | rewritten | required prompts in the proposal template, each answered in a line |
| 416 | docs/methodology/roles.md:43 | add-test | rewritten | plan: the code, the docs, and a test only where none covers the change. |
| 417 | docs/methodology/roles.md:242 | run-tests | kept | C: not a pressure sentence (plainly not about tests) |
| 418 | docs/methodology/roles.md:249 | run-tests | kept | C: not a pressure sentence (plainly not about tests) |
| 419 | docs/methodology/runtime-contract.md:190 | run-tests | kept | not pressure: record format, certification, check tool, or description of an existing guard |
| 420 | docs/methodology/runtime-contract.md:197 | run-tests | kept | not pressure: record format, certification, check tool, or description of an existing guard |
| 421 | docs/methodology/session-routines.md:100 | run-tests | rewritten | additionally scrubs the roadmap boards, verifies the docs and changelog, rewrites the next session's starting plan (smoke run removed) |
| 422 | docs/methodology/session-routines.md:105 | not-run-ledger | removed | smoke-command record paragraph removed; Reflection-only participants acquire no test obligation. kept |
| 423 | docs/methodology/session-routines.md:113 | other | kept | C: whole suite at certification: slow tests due at release |
| X1 | plans.md ~372 | extra | removed | Cairn's own command (tier_inventory) and the AGENTS.md range sentence: made false by rule A |
| X2 | plans.md ~267 | extra | rewritten | the arc owner records the joined evidence (was: joined integration selection) |
| X3 | dual-review.md ~344-350 | extra | removed | 'Routine selection remains with the agent applying these defaults ... Existing project requirements remain in force.': went with row 261 |
| X4 | dual-review.md ~452-455 | extra | rewritten | mapping: test or guard -> guard; exact words, code or doc -> accept; 'none of these' (was: none of the five) |
| X5 | lifecycle.md ~117 | extra | rewritten | 'agent maps affected behavior to existing checks and consumers ... review challenges that mapping' became 'chooses its checks under the rule on tests; review reads that choice' |
| X6 | proposals.md 178, 335 | extra | rewritten | 'the lifecycle's three conditions' -> 'two conditions' (row 301 dropped condition iii) |
| X7 | session-routines.md ~105-111 | extra | removed | rest of the smoke paragraph (no command configured, example) removed with row 422 |
| X8 | session-routines.md ~113-117 | extra | rewritten | 'a goodnight smoke' -> 'goodnight'; project's 'concrete command' -> 'close-out steps'; Cairn's local selection sentence removed |
| X9 | plans.md ~1058 | extra | rewritten | 'turning deferred evidence into shipped' -> 'turning evidence that did not ship into shipped' |
| X10 | plans.md / dual-review.md after the trigger lists | extra | removed | 'These triggers require evidence ...' and 'The fifth trigger ...' paragraphs, with the lists |

Counts: kept 100, removed 29, rewritten 49, rule A 2, undecided 2; total 182

Notes:
- Undecided 357, 358: the split rule for a selection above the runner's file limit; the limit is the next proposal.
- Differs from G3 (collaboration file): its 'Verification' still holds the Bounding verdict WIDER RUN REQUIRED; rows 269, 359 and 360 removed it here under disposition 3. Strategy may want G3 to follow.
- Rule A appears once, in plans.md (Boundary A), and in no other file of this group.

Word counts before / after (wc -w):
- dual-review.md 7320 / 7080
- plans.md 8383 / 8148
- lifecycle.md 6175 / 6172
- proposals.md 4600 / 4599
- rationale.md 4639 / 4636
- roles.md 2267 / 2274
- runtime-contract.md 1898 / 1898
- session-routines.md 3688 / 3592
- total 38970 / 38399

## Group G5

### Rows G5 (commit eb013165)

Rows 79-84, 87-97, 433-434, 492-508, 567-579, 588-593, 596-612 = 72 rows. Kept 61, rule A 0, rewritten 10, removed 0, undecided 1.

| Row | File:line | Kind | Outcome | New words / clause |
|---|---|---|---|---|
| 79,569 | claim-check:15 (both) | run-tests | kept | not about tests (verify-before-asserting) |
| 80,570 | claim-check:55 | run-tests | kept | direct check of a claim; claim-check tool module |
| 81,571 | claim-check:83 | run-tests | kept | not about tests (counts of files/lines) |
| 82,572 | claim-check:93 | run-tests | kept | direct check of a claim |
| 83,573 | claim-check:104 | run-tests | kept | direct check of a claim |
| 84,574 | claim-check:123 | run-tests | kept | tells an agent to run a check tool |
| 87,596 | doc-drift-prevention:204/205 | run-tests | kept | runs the link check tool |
| 88,597 | doc-drift-prevention:206/207 | add-test | kept | not pressure; says where tests may live |
| 89,601 | examples-gallery:33 | run-tests | kept | names a test as a guard (broken example fails the build) |
| 90,602 | issue-capture:64 | add-test | rewritten | "fixes it with review, and a test only where no existing test covers it" |
| 91,603 | issue-capture:69 | add-test | rewritten | "lands, with a test only where no existing test covers it" |
| 92,612 | model-selection:176 | run-tests | kept | check run by a person; not test pressure |
| 93 | dev-tour:37 | evidence-as-runs | kept | not about tests |
| 94 | dev-tour:89 | add-test | rewritten | "any test it needs, where no existing test covers it" (template copy edited too) |
| 95 | dev-tour:91 | other | kept | not about tests |
| 96 | dev-tour:106 | run-tests | rewritten | "runs the applicable prose checks before recording the result" (prose checks kept; integration selection removed; template copy too) |
| 97 | dev-tour:108 | run-tests | kept | prose checks still apply |
| 433 | PLANNING:98 | other | kept | not about tests |
| 434 | PLANNING:143 | add-test | kept | names a test as a guard |
| 492-495 | method-background:9-14 | add-test/reviewer-asks | kept | description of the problem; not a demand |
| 496-497 | method-background:20,39 | add-test/control | kept | what a good test of the science is |
| 498 | method-background:46 | control | undecided | "Observe it fail before fixing behavior" sits in the background of the testing module, held for the Maintainer; proposal does not settle it |
| 499-503 | method-background:60-82 | other/add-test | kept | what a good test is; tier check is a check |
| 504 | method-background:151 | not-run-ledger | kept | says plainly what was not checked |
| 505 | method-background:185 | evidence-as-runs | kept | direct check, no run required |
| 506-507 | method-background:196-197 | evidence/control | kept | keeps an existing control |
| 508 | method-background:227 | control | kept | check of a model result against the world |
| 567-568 | strategy/_template:137,139 | evidence-as-runs | kept | not about tests |
| 575 | documentation_plan_template:188 | evidence-as-runs | kept | heading; not about tests |
| 576 | documentation_plan_template:196 | run-tests | kept | direct check of a figure, not a test |
| 577-578 | documentation_plan_template:211,217 | other | kept | not about tests |
| 579 | documentation_plan_template:301 | run-tests | rewritten | example now: "Commit only explicit paths; complete required security checks" |
| 588 | architecture-review:43 | control | rewritten | "add a narrow check ... shown once to refuse one dangerous example" |
| 589-590,593 | architecture-review:48; template:37,142 | add-test | kept | name tests as guards |
| 591 | architecture_review_template:86 | control | kept | check of helpers; extra edit on the next sentence (below) |
| 592 | architecture_review_template:122 | other | kept | not pressure |
| 598 | dual-language-tests:22 | add-test | kept | describes the test architecture of science code |
| 599 | dual-language-tests:27 | add-test | rewritten | "documented surface, with a test only where no existing test covers it" |
| 600 | dual-language-tests:59 | other | kept | verification command, a check |
| 604-605 | bug forms | evidence-as-runs | kept | steps to reproduce, not test pressure |
| 606-610 | legacy-agent:22-65 | add-test/other | kept | what a ready surface is; guards and check command |
| 611 | legacy-agent:77 | add-test | rewritten | "pin the current behavior with a test where no existing test does" |
| 607-610 | see above | | kept | |
| extra | architecture_review_template:86-87 | control | rewritten | "A narrow drift check is shown once to refuse one dangerous example" (keeps 588 true) |
| extra | templates/onboarding/dev-tour.md | twin | rewritten | same two edits as dev-tour, copies identical |

Not touched: doc-drift-prevention and claim-check twins differ and stay as they were; examples-gallery, model-selection pair identical.

Words before/after (wc -w, all my files incl. both dev-tour copies and both bug forms): 25441 -> 25478 (added "only where no existing test covers it" clauses outweigh removals).
