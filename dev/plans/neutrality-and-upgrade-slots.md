# Plan: neutrality and upgrade slots -- a vendor-name check that reads zero, and a note for slots an upgrade adds

**Source proposal**: `dev/proposals/archive/2026-10-17-claude-neutrality-and-upgrade-slots.md`
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Assurance path**: high-assurance -- inherited from the proposal: the work widens the neutrality checker, adds code to the lockfile reader adopters run before they trust their scripts (`bootstrap/verify_integrity.py`), and edits comments in two security-relevant scripts (the interpreter binding and the content scanner)
**Opened**: 2026-10-18

## In brief

Two of Cairn's checks cannot be trusted today, for opposite reasons. This plan fixes both in twelve small chunks, and writes the one paragraph the Maintainer also accepted for issue #16.

1. **The vendor-name check is always red.** Cairn promises to stay neutral about which AI tool a team uses, so nothing it ships to a project may name an AI vendor or our reference project. `python scripts/quality_gate.py --sub neutrality` enforces that. Every recorded run has been red, and it reports 74 failures today, so a new leak would be invisible, like a smoke alarm that is always ringing. The plan:
   * makes the check slightly stricter: it will also read comment lines, two more file types (`.json`, `.txt`) and four more tool names, which raises the count to 81;
   * rewrites every shipped leak (reviewer credits in comments, the reference project's name) and marks the illustrative mentions in Cairn's own documents, so the check reads **zero** (`fail=0`), without changing what any program does (a script shows each edited program is identical to its parent apart from comments);
   * says plainly what zero covers: no listed name, as a whole word in its normal capitals, in the file types the check reads. It does not cover lower-case or joined spellings, hidden characters, names missing from the list, other file types, or someone hiding a name on purpose.
2. **When an upgrade adds a fill-in section, nothing says so (#8).** A *slot* is a section of a project's file that the project fills in; Cairn's placeholder sits there until it does. The plan adds an advisory note to the install integrity check (`bootstrap/verify_integrity.py`) that lists every slot still holding Cairn's placeholder text. It always says how much it was able to check, so silence means "none found" and never "could not look". It prints no commands, because a Security Review showed that a printed command could lead someone to approve a tampered file. It cannot change the check's pass or fail result. `bootstrap/UPGRADE.md` gains a step and a section on recording an edit you made.
3. **Issue #16's paragraph.** One paragraph in the doc-drift module names the third kind of documentation drift: prose that names a function the code no longer has. The code check #16 also asked for is not built.

**What it costs the Maintainer.** No engine change, so no hand re-anchor of the engine's fingerprint. Fourteen *frozen files* (files whose exact bytes the gate manifest records) change, so the next gate-manifest *re-anchor* (the supervised ceremony only the Maintainer runs) covers them. They join the queued row on `dev/PLANNING.md`, which this plan's opening commit updates. If that ceremony runs before this plan archives, a second pass is owed. Nothing is pushed.

**How we will know it worked.** The neutrality check reads `fail=0` and exits 0, the "green" the gate manifest already expects of it, and a planted leak makes it read 1. Every edited program file is shown identical to its parent apart from comments. A test shows that a bad lockfile entry cannot change the integrity check's verdict. One full test run (Boundary B) is recorded against one clean commit.

Two terms used below. A **twin** is Cairn's own installed copy of a shipped template; for example `tools/session.py` is a byte-identical copy of `templates/skills/_lib/session.py`, and the pair must stay identical. **Boundary A, B and C** are the three verification jobs in `AGENTS.md`: scoped iteration while building, one integration run on a clean commit, and the code reviewer's independent falsification.

## Source proposal

Accepted 2026-10-18 at `f4cff4be`. Revision 4 binds, over Revisions 1-3 as it states: Revision 2 is the last complete contract, Revision 3 replaces parts of it, and Revision 4 replaces parts of Revision 3. The Security Review obligation was cleared at `eca6ca1d`. The Decision accepted every recommended answer:

* **Q1(a) yes.** #16's proposed symbol-drift check is won't-build, under the three-recurrence rule, keeping its revival rule.
* **Q1(b) yes.** #16's one-paragraph half is written in the doc-drift module as a separate small change. It is chunk C11 here (see *Found while planning*).
* **Q2 not now.** `upgrade` does not name the slots it adds in this change. That rides with the next engine change to the upgrade path that already owes a re-anchor, or sooner if an adopter misses an upgrade-added slot. It is a `defer`, recorded in *Dispositions*.

The SR15-closure pass handed two non-blocking findings to the plan: SR17 (C10) and SR18 (already landed, see *Found while planning*).

## Scope

Measured at `fbf664f0`, the HEAD when this plan was written. The plan executes the accepted text; it does not re-argue it.

**Touched.**

| Surface | Files | Chunk |
|---|---|---|
| The checker | `scripts/quality_gate.py`; `bootstrap/tests/test_quality_gate_neutrality.py` | C1 |
| Routing table, session kernel, session-start skill | `templates/skills/_data/vendor_targets.yml`, `templates/skills/_lib/session.py`, `templates/skills/session-start/SKILL.md`; twins `.agents/skills/_data/vendor_targets.yml`, `tools/session.py`, `.agents/skills/session-start/SKILL.md` | C2 |
| Onboarding package and activation helper | `templates/modules/default-on/_onboarding/` (`__init__`, `activation`, `cli`, `security`, `shared`, `triggers`), `templates/modules/default-on/onboarding_activate.py`; twins `scripts/_onboarding/` (the same six) and `scripts/onboarding_activate.py` | C3 |
| Content scanner, intent tool | `templates/modules/team-gated/content_scan.py`, `templates/modules/team-gated/intent.py`; twins `scripts/content_scan.py`, `tools/intent.py` | C4 |
| Shipped Markdown | `templates/modules/default-on/documentation-plan.md`, `documentation_plan_template.md`, `incident-trackers.md`, `incident_log_template.md`; `templates/onboarding/solo-greenfield.md`; `templates/modules/team-gated/api-access-security.md`, `web-hosting-security.md`; twins `dev/modules/documentation-plan.md`, `dev/modules/incident-trackers.md`, `dev/modules/incident_log_template.md` | C5 |
| Cairn-internal prose | `bootstrap/tests/fixtures/skills/README.md`, `docs/DOCUMENTATION_PLAN.md`, `docs/agent-team-onboarding.md`, `doctrine/lifecycle-contract.md`, `doctrine/rationale.md` | C6 |
| The dogfood log | `doctrine/consolidation-review.md` | C7 |
| The install check | `bootstrap/verify_integrity.py`; `bootstrap/tests/test_verify_integrity.py` | C8, C9 |
| The upgrade guide | `bootstrap/UPGRADE.md` | C10 |
| The doc-drift paragraph | `templates/modules/team-gated/doc-drift-prevention.md`; twin `dev/modules/doc-drift-prevention.md` | C11 |
| Cairn's own install record | `dev/.cairn/cairn-lock.yml`, scoped finalize of 12 records | C2-C5 |
| Board and changelog | `dev/PLANNING.md` (the opening commit joins the re-anchor row); `CHANGELOG.md` (the archive commit) | opening, archive |

**Not touched**, each checked by `git diff --stat` over the implementation range (C12): `bootstrap/_scaffold/` and `bootstrap/scaffold.py` (so **no AST impact**), `bootstrap/tests/_gate_manifest.py` and the gate-manifest fixture, `AGENTS.md` and `templates/core/AGENTS.md`, every `doctrine/` file except the two marker edits (C6) and the log (C7), `scripts/check_model_selection.py`.

**Twins.** Sixteen template and twin pairs are edited: the fifteen in chunks C2-C5 (three skills files, seven onboarding files, two scanner and intent files, three Markdown modules) and the doc-drift pair in C11. All sixteen are byte-identical today (measured with `filecmp` and `cmp`). `docs/DOCUMENTATION_PLAN.md` is not a twin: it is Cairn's own customized copy of `templates/modules/default-on/documentation_plan_template.md` and differs from it. Each chunk edits the template, copies it to the twin, and checks the pair with `cmp` in the same commit.

### Frozen files and the AST baseline

**Frozen files: 14.** Read from `bootstrap/tests/fixtures/gate_manifest.json` > `frozen_files` (183 keys) and intersected with every file this plan edits by script. The instrument was checked against a known frozen key (`bootstrap/verify_integrity.py` is reported frozen). The 14:

* `scripts/quality_gate.py`, `bootstrap/tests/test_quality_gate_neutrality.py` (C1);
* `templates/modules/default-on/_onboarding/__init__.py`, `activation.py`, `cli.py`, `security.py`, `shared.py`, `triggers.py` and `scripts/onboarding_activate.py` (C3);
* `templates/modules/team-gated/content_scan.py` and `scripts/content_scan.py` (C4);
* `bootstrap/tests/fixtures/skills/README.md` (C6);
* `bootstrap/verify_integrity.py` and `bootstrap/tests/test_verify_integrity.py` (C8, C9).

Not frozen, though edited: every other file in the table, including `tools/session.py`, `tools/intent.py` and both `session.py` copies. The proposal's "up to 16" was an upper bound; the manifest gives 14. Changed frozen bytes do not redden `test_gate_manifest.py`, which verifies a freshly produced manifest and never diffs the committed fixture, so a green suite is no evidence that the re-anchor is paid. The pinned collection also grows: C1 adds 8 nodes to `test_quality_gate_neutrality.py` (22 pinned, 30 after), and C8-C9 add the nodes of `test_verify_integrity.py` (13 pinned, 19 collected at the base, so the ceremony already sees 6 new nodes there). Both join the re-anchor row already queued on `dev/PLANNING.md` (line 156 at the base). **The re-anchor is the Maintainer's alone** (`bootstrap/REANCHOR_RUNBOOK.md`); an implementing agent must not perform it. The opening commit adds the 14 paths to that row, marked as planned and not yet changed; the archive commit adds the node IDs.

Two ceremony facts for the Maintainer, measured: `bootstrap/verify_integrity.py` is also on the differential oracle's refactor-sensitive roster (`bootstrap/tests/_oracle_activation.py:34-47`), and it already differs from the gate anchor `bd66a70c` (five commits since). So the ceremony's sensitive-path check covers it whether or not this plan runs.

**AST: no change.** No file under `bootstrap/_scaffold/` and not `bootstrap/scaffold.py` is edited, and `bootstrap/verify_integrity.py` keeps its two engine imports (`bootstrap._scaffold.lockfile` and `trusted_upstream`) and adds standard-library imports only. The baseline `bootstrap/tests/fixtures/scaffold_ast_baseline.json` is already not clean at the base, for other work: on a clean extraction of `fbf664f0`, `python bootstrap/tests/_ast_attest.py verify` reports 2 CHANGED symbols (`main` in `bootstrap/_scaffold/cli.py`, `seed_gitignore` in `bootstrap/_scaffold/install.py`) and `test_ast_attest.py` fails 2 of 30 nodes for that reason. The AST re-anchor is Maintainer-only and not this plan's. C12 derives the set again at the tested commit's parent and at the tested commit and requires them equal.

**Lockfile.** Twelve of Cairn's own lockfile records attest edited twins that match their record today, and are scoped-finalized in the commit that edits them (precedent `2ea3f869`): `.agents/skills/_data/vendor_targets.yml`, `tools/session.py`, the six `scripts/_onboarding/` modules, `scripts/onboarding_activate.py`, `tools/intent.py`, `scripts/content_scan.py`, `dev/modules/incident_log_template.md`. Four edited files are already among Cairn's 18 integrity violations and are **left alone**, so the count does not grow: `.agents/skills/session-start/SKILL.md`, `dev/modules/documentation-plan.md`, `dev/modules/incident-trackers.md`, `docs/DOCUMENTATION_PLAN.md`. `dev/modules/doc-drift-prevention.md` (C11) is a fifth, also already among the 18. The 18 at the base (measured with `python bootstrap/verify_integrity.py --target .`): `.agents/skills/session-end/SKILL.md`, `.agents/skills/session-start/SKILL.md`, `AGENTS.md`, `dev/README.md`, `dev/agent_collaboration.md`, `dev/measurement/README.md`, `dev/modules/claim-check.md`, `dev/modules/doc-drift-prevention.md`, `dev/modules/documentation-plan.md`, `dev/modules/incident-trackers.md`, `dev/plans/_template.md`, `dev/proposals/_template.md`, `dev/rules/README.md`, `dev/strategy/_template.md`, `dev/upstream/README.md`, `docs/DOCUMENTATION_PLAN.md`, `scripts/claim_check.py`, `tools/_intent/conflict.py`. The lockfile schema is untouched.

### Found while planning

* **#16 is already closed on GitHub, before its paragraph exists.** A read-only `gh issue view 16` on 2026-10-18 shows `CLOSED`, state reason `COMPLETED`, closed 15:57 UTC. The paragraph is not in `templates/modules/team-gated/doc-drift-prevention.md` at the base. The Decision said "#16 closes when it lands", so the issue is no longer a live home for the work; the plan carries it (C11). The plan makes no GitHub change. Whether the closure reason should read "not planned" is the Maintainer's call.
* **SR18 already landed.** `7c077ddf` (the same minute as the SR15 closure) removed "or its history since install" from the hint and added the assertion `history misses uncommitted edits` to `test_a_filled_customized_slot_is_pointed_at_finalize`. C9 keeps it true; no new work.
* **Marker form.** Markers on their own line would shift every later line of the file. `independent-scientific-check` cites `doctrine/rationale.md:405`, `:414-417` and `:451`, and several archived records cite `doctrine/lifecycle-contract.md` by line. The gate also accepts a marker at the end of the hit line (`<!-- vendor-ok: reason -->`), which it reads as a one-line exemption; I checked this on a scratch tree with the unmodified checker. C6 uses that same-line form wherever the hit is prose, adds no line, and shifts no citation. A hit inside a code fence cannot take a same-line marker without changing the example (`docs/agent-team-onboarding.md:37-38`), so there a block marker wraps the fence; that is the one block wider than its hit lines.
* **The solo-greenfield paragraph is counted by a test.** `test_onboarding_review_tiers.py` requires exactly three paragraphs in `templates/onboarding/solo-greenfield.md` that name both "External" and "tier". The credit at line 92 sits in a paragraph with "External" and no "tier"; rewording it must not add the word "tier" there (C5).
* **A comment citing lines of `verify_integrity.py` is already stale.** `templates/modules/default-on/run_security_verification.py` (line 128) and `bootstrap/tests/test_security_verification.py` (line 944) cite `bootstrap/verify_integrity.py:63-111`, which no longer bounds the record loop. Not widened; flagged so that whoever next edits either comment re-points it.
* **The five comment sites in the checker** sit one line off the proposal's numbers at the base: `scripts/quality_gate.py:197-200`, `:252`, `:434-439`, `:446`, `:454-459`.
* **Rows in the log table quote tokens.** The dogfood log's table lives inside one `vendor-ok` block, so new rows go inside it, before its end marker (C7).

### Plan decisions the proposal left open

The proposal fixes the note's content, not its shape. These are choices this plan makes; plan review may overrule any of them.

* **D1 Where the note speaks.** It prints to stderr, like the fork advisory and the existing hint. Every line it prints begins `slot note:`, so tests can separate the note's lines from the hint's (the SR16 test needs this) and so a person can tell them apart.
* **D2 Names.** The entry point is `_slot_note`, called from `verify()` inside a fence. Its parameters are fixed in C8.
* **D3 When it runs.** On both exits of `verify()` (the OK path and the violations path), after the report and the exit code are fixed. It does not run on the fail-closed early returns (no lockfile, a lockfile with no files).
* **D4 The warning and the pointer** print once per run, when the note lists at least one slot or counts at least one file as failed the integrity check. A run with nothing to act on prints only the coverage line.
* **D5 Not-checked reasons.** A missing `base_cache` is "no base copy"; a `base_cache` that is present but unusable (not a string, a NUL byte, outside `dev/.cairn/base/`, a symlinked part, cannot be opened, not a regular file, over the cap, not UTF-8) is "unreadable"; a base copy whose bytes do not hash to a string `base_hash` is "base hash mismatch"; a non-verbatim record that did not pass the integrity pass is "failed the integrity check"; an unusable `tokens` mapping, installed bytes that are over the cap or not UTF-8, and any per-record exception count as "unreadable". A bad `tokens` mapping must not fall back to "no substitution", because that would make every templated slot read as filled, which is the silent miss the coverage line exists to prevent.
* **D6 The pointer's target.** The note points to `bootstrap/UPGRADE.md` > *Recording an edit you made*. One test (C10) pins that a heading of exactly that name exists, since a code string naming a heading is not a link that `check_cairn.py` resolves.
* **D7 Scope of the check.** "Files in scope" are the non-verbatim records, living-state records included (verbatim ones are scripts that hold no slots).
* **D8 Plan review.** The proposal's header says `required(Internal)`. This plan declares `required(Internal + Internal Security Review)`: `AGENTS.md` asks for it where the surface calls for security treatment, and the Security Review handed build details (SR12, SR17) to the plan.

### Documentation / doctrine surface

| Layer | Files |
|---|---|
| Governing | none; `AGENTS.md` > "Vendor-neutrality" stays true |
| Doctrine | marker-only edits in `doctrine/lifecycle-contract.md` and `doctrine/rationale.md`; log rows in `doctrine/consolidation-review.md` |
| Descriptive | `bootstrap/UPGRADE.md`; `docs/DOCUMENTATION_PLAN.md` (stale lines); `docs/agent-team-onboarding.md` (markers) |
| Module text | `templates/modules/team-gated/doc-drift-prevention.md` and its twin (C11) |
| Deliberation | this plan; `dev/PLANNING.md` (the re-anchor row; at archive, the deferral row) |
| Changelog | one entry, written by the archive commit |

The rate-limit gate (`doctrine/rationale.md` > "Adaptive-doctrine rate-limit gate") is not triggered: the markers change no rule, and `doctrine/consolidation-review.md` prescribes this disposition. The proposal's fallback (leave the 8 doctrine lines unmarked, so the gate reads `fail=8`) is part of the accepted text but would lose the "zero" outcome, so invoking it is a scope reduction and takes the Maintainer's word. Marker reasons are text `templates/modules/team-gated/content_scan.py` skips (its `_CAIRN_MARKER_RE`), so only the injection review of `bootstrap/SAFETY.md` Rule 7 reads them; C6 checks each is short and declarative.

## Sequence

The rows are in run order. All commits go to `master`; nothing is pushed.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **The stricter checker.** `scripts/quality_gate.py` reads whole-line comments in `templates/`, reads `.json` and `.txt` there, and gains four names; its five misdescribing comments are corrected. Eight new nodes. The gate moves from 74 to 81 and only up. | `ready-to-implement` | one commit |
| C2 | **The routing table and the session kernel.** The 9 hits and the 4 new names in `templates/skills/` are reworded (comments, docstrings, one `_doc` string); twins follow; two records are finalized. | C1 | one commit |
| C3 | **The onboarding package.** The 27 hits (26 in the six `_onboarding` modules, 1 in `onboarding_activate.py`) are reworded in comments and docstrings; twins follow; seven records are finalized. | C1 | one commit |
| C4 | **The content scanner and the intent tool.** The 3 hits are reworded; twins follow; two records are finalized. | C1 | one commit |
| C5 | **The shipped Markdown.** 8 hits in five templates, plus the 3 `reviewer=` credits in two security modules, are reworded; three twins follow; one record is finalized. | C1 | one commit |
| C6 | **Cairn's own prose.** The fixture credit and the stale "not self-hosted" lines are reworded; the illustrative mentions in four files are marked with same-line markers. | C1 | one commit |
| C7 | **Zero, and the log.** The gate is run and must read `fail=0`; plants, the superset check and the one-time search are recorded; the pass is logged. | C2-C6 | one commit |
| C8 | **The note's frame.** `verify()` fixes its verdict and prints its report, then calls `_slot_note` inside a fence. The note's reader opens base copies and living-state files safely and prints the coverage line. | `ready-to-implement` | one commit |
| C9 | **The listing.** The note finds slots still holding Cairn's text and prints them, with a warning and a pointer and no commands. | C8 | one commit |
| C10 | **The upgrade guide.** `bootstrap/UPGRADE.md` gains step 4, what the note means, the known gap, and the section *Recording an edit you made*. | C9 | one commit |
| C11 | **#16's paragraph.** One paragraph names prose that cites a symbol the code no longer has. | `ready-to-implement` | one commit |
| C12 | **Boundary B, then the record.** One full run on one clean commit; the result is written down. Status moves to `awaiting-code-review`. | C1-C11 | one commit |
| M | **MAINTAINER-ONLY: the re-anchor.** Runs the gate-manifest ceremony over the changed frozen files and the new nodes. **An implementing agent must not perform it.** The agent's part is the board note at archive. No new ceremony and no Waiting line in this plan: the wait is already declared on the marked board row. | code review cleared | Maintainer |

C8 to C10 do not depend on C1 to C7 and may run first; the order shown is the default. The finalizes in C2-C5 touch `dev/.cairn/cairn-lock.yml`, a file other plans also finalize: each such commit reads the file fresh, names it by path, and checks the lockfile diff before committing (K4).

### Sequencing with the later plans

This plan runs first. The later plans are expected in this order: `independent-scientific-check`, `model-mapping-install-path`, `board-as-basis`, `external-is-a-maintainer-stance`. Their proposals were skimmed for the files they name; where one edits a file this plan also edits, it re-reads the file at edit time and rebases on this plan.

**Everything they ship is held to the stricter checker from C1 on.** Any shipped text they add under `templates/` is scanned in comment lines and in `.json` and `.txt` files, and the names Copilot, Windsurf, Cline and OpenCode now count. After C7 the baseline is zero, so a new failure is theirs.

| File | This plan | Later plan | What to know |
|---|---|---|---|
| `templates/onboarding/solo-greenfield.md` line 92 | C5 rewords the credit | `external-is-a-maintainer-stance` names this exact line (its SR6) | it finds the line already reworded, and compares against zero |
| `doctrine/rationale.md`, `doctrine/lifecycle-contract.md`, `docs/agent-team-onboarding.md`, `bootstrap/tests/fixtures/skills/README.md` | C6: same-line markers, and one reworded credit in the fixture README | `external-is-a-maintainer-stance` edits prose in the first three (its anchor, its examples) | markers sit on hit lines; if it rewrites a marked line it keeps or drops the marker deliberately, and the gate says which |
| `doctrine/rationale.md` | C6: no line added | `independent-scientific-check` cites lines `:405`, `:414-417`, `:451` | no shift from this plan |
| `templates/skills/session-start/SKILL.md` and `.agents/skills/session-start/SKILL.md` | C2: one phrase near line 28 | `external-is-a-maintainer-stance` changes one phrase ("review tier, plan-review tier"); `board-as-basis` cites lines 43-45 but does not edit them | three plans, three different sentences |
| `scripts/_onboarding/triggers.py` and its template | C3: comments and docstrings only | `external-is-a-maintainer-stance` deliberately leaves its credit comments alone | after C3 there are no credits left to leave |
| `bootstrap/UPGRADE.md` | C10: step 4 in "The workflow", a known-gap line, a new section | `external-is-a-maintainer-stance` edits the plan-pass schema rows and stale planner text | different sections |
| `docs/DOCUMENTATION_PLAN.md` | C6: six stale lines | cited as the routing procedure by `independent-scientific-check`, `board-as-basis`, `external-is-a-maintainer-stance` | read, not edited, by them |
| `dev/.cairn/cairn-lock.yml` | C2-C5: 12 records | `model-mapping-install-path` and `board-as-basis` each finalize or edit other records | one file, different records |
| `dev/PLANNING.md`, `CHANGELOG.md` | the opening commit (the re-anchor row); the archive commit | every plan | commit by path, read fresh |
| `templates/skills/_lib/session.py`, `tools/session.py`, `scripts/onboarding_activate.py` | C2, C3: comments only | `model-mapping-install-path` names them as not touched | no overlap in practice |

`bootstrap/tests/test_verify_integrity.py` is named by `board-as-basis` as a test to run, not edited. `review-lenses-for-every-install` was accepted at `fbf664f0`, after the order above was set; it edits `AGENTS.md`, `templates/core/AGENTS.md`, the `agent_collaboration.md` and `dual-review.md` pairs and adds a test, shares none of those with this plan, and runs the neutrality gate like the others (so the stricter checker applies to its shipped text too).

## Acceptance criteria

**Reading these criteria.** Each ends with *Red when*: a change that turns it red. Prose checks use `count(file, section, phrase)`: the number of times a fixed phrase occurs in a section, taken on whitespace-collapsed text. These are one-shot checks the implementer runs and records in the chunk's commit body; no standing test pins new prose unless a criterion says so. Boundary C attacks the prose.

### Checks every rewording chunk repeats (C2-C6)

Each chunk's commit body records the result of the checks that apply to it.

* **K1 -- the gate moves the right way.** Run `python scripts/quality_gate.py --sub neutrality` at the chunk's parent and at its commit. Strip each FAIL line's message tail, sort, and `comm` the two lists. Lines only in the parent are exactly the chunk's hits (the counts below); lines only in the commit are none. *Red when* a FAIL line appears that the parent lacked.
* **K2 -- the comment-only proof**, for every edited `.py` (procedure under *Verification*). (a) The docstring-stripped `ast.dump` of the new file equals the parent's. (b) No added or removed line in the file's diff matches `nosec`, `noqa`, `pragma`, `type:` or an encoding declaration. (c) The instrument fires: a one-character code change in a scratch copy of each edited `.py` makes (a) read DIFFERENT, and a scratch diff with `# noqa` makes (b) print a hit. *Red when* any file reads DIFFERENT, (b) prints a line, or a control does not fire.
* **K3 -- twins.** `cmp` of each template and its twin exits 0, and the pairs the chunk touches are listed in the body. *Red when* either copy was edited alone.
* **K4 -- the lockfile.** For the chunk's attested twins only, one scoped `python bootstrap/scaffold.py upgrade --target . --finalize <path> ...` runs in the same commit. `git diff -U0 dev/.cairn/cairn-lock.yml` shows changes only to the `"hash"` lines of exactly those records. Each advanced `hash` equals the SHA-256 of its template as committed (`git show <commit>:<template> | shasum -a 256`), so a reviewer can confirm it from the commit alone. `python bootstrap/verify_integrity.py --target .` lists the same 18 files as at the base and none of the chunk's finalized files. *Red when* a record outside the chunk changes, a hash differs from the template's, or the 18 grow.
* **K5 -- the reason survives.** For each reworded reviewer credit the commit body names the line and the reason in code terms that the new text keeps, or states that the credit carried none. `modflow_tools` becomes "the reference deployment" or is dropped. *Red when* a credit is deleted along with an explanation a reader needed (the reviewer reads before and after).
* **K6 -- the early substring search.** On the chunk's added lines, a case-insensitive substring search for each of the 20 denylist entries (the 16 existing and the four added) prints the containing word of each hit; the distinct words are read by hand (full form in C7). *Red when* a hit is a name the gate cannot see, such as a joined or lower-case spelling.
* **K7 -- not inside a slot.** For each edited Markdown template, every changed line lies outside every `cairn:slot` to `cairn:end` span (compare `git diff -U0` hunk ranges with the spans from `grep -n`). A change inside a slot body could trigger the reworded-placeholder gap (C9). *Red when* a changed line is inside a slot.

### C1 -- The stricter checker

Frozen: `scripts/quality_gate.py`, `bootstrap/tests/test_quality_gate_neutrality.py`.

* **Eight new nodes, red before the code.** In `test_quality_gate_neutrality.py`, five functions, one parametrized: a vendor name in a whole-line HTML comment in `templates/` fails; in a `.txt` file there fails; in a `.json` file there fails; each of Copilot, Windsurf, Cline and OpenCode in a `templates/` file fails (one function over four names: 4 nodes); a whole-line `vendor-ok` directive in `templates/` that also names a vendor yields two failures, the directive's and the name's. Run them at C1's parent in a throwaway `git worktree` with only the new test file copied in (the tests load `scripts/quality_gate.py` from the tree they sit in); each fails on an assertion, not an import error. The body names the parent SHA. *Red when* a node passes at the parent, or `pytest --collect-only -q` shows other than 8 more nodes (22 before, 30 after).
* **The 22 existing nodes pass unchanged**, and the test file's diff is additions only. *Red when* an existing node is edited.
* **The count moves 74 to 81 and only up (the superset check).** In a throwaway worktree at C1's parent, run the parent's checker and C1's checker over the same tree. Every FAIL line of the old is in the new, and the new has exactly seven more: `templates/modules/team-gated/api-access-security.md:101`, `templates/modules/team-gated/web-hosting-security.md:70` and `:93` (the `reviewer="Claude (Implementation)"` credits), and the four added names on `templates/skills/_data/vendor_targets.yml:2`. Counts: `fail=74 info=21` before, `fail=81 info=21` after. This also shows the four names add nothing outside `templates/`. I prototyped it on a scratch copy of the base: 74 within 81, the same seven. *Red when* an old line is missing, or a new line is outside the seven.
* **Only failures are added.** The diff of `scripts/quality_gate.py` consists of: four names added to `_VENDOR_DENYLIST`; the two-line skip in the `templates/` branch removed (`:278-279`); `.json` and `.txt` added to the `templates` entry only; comment text. The skip in the non-template branch (a directive-only line carries no prose tokens) is untouched, so exemption reasons that name vendors still pass outside `templates/`. The `Last updated` comment above the denylist is advanced and the commit body names why the four were added (the routing table itself lists them). No exemption is added. *Red when* the diff touches the non-template branch's skip or adds any allowance.
* **The five comment sites describe the scan truly** (`:197-200`, `:252`, `:434-439`, `:446`, `:454-459` at the base). Afterwards they say: `templates/` is scanned for tokens, comment lines included, as well as for the directive rule; the file types read there now include `.json` and `.txt`; matching is whole-word and case-sensitive; `bootstrap/tests/` **is** scanned under the `bootstrap` root (`.md` only). `grep -n "only for the directive-forbidden\|Not bootstrap/tests/" scripts/quality_gate.py` prints nothing (the same grep prints both at the parent). *Red when* a sentence still says templates are scanned only for directives.
* **Standing gates.** `python scripts/quality_gate.py --sub redundancy` reads `fail=0`; `test_security_lint.py` (the Bandit gate over `scripts/`) passes. The neutrality gate reads 81 at this commit, and C1's body says why that is expected.

### C2 -- The routing table and the session kernel

Hits at the base: 13 in these three files once C1's four names count (5 on `vendor_targets.yml:2`, 4 added, 3 in `templates/skills/_lib/session.py` at `:215`, `:905`, `:1338`, 1 in `templates/skills/session-start/SKILL.md:28`). Finalize: `.agents/skills/_data/vendor_targets.yml`, `tools/session.py`.

* **K1** with the 13 lines. **K2** for `session.py`. **K3** for three pairs. **K4** for two records.
* **The protected code is identical.** In addition to K2's whole-file result, the `ast.dump` of `_resolve_interpreter`, `encode_display` and every function that executes the path `_resolve_interpreter` returns is equal before and after. These sit outside the three hit lines; the check shows it rather than assuming it. *Red when* any of them differs.
* **The routing table.** `json.load` of the new `templates/skills/_data/vendor_targets.yml` equals the parent's after removing `_doc` from each. The new `_doc` names no harness in prose (the lowercase ids in the rows are untouched), keeps every fact the old one states (canonical source, the tier meanings, the `auto_suppress` levels, that a vendor refresh is a row edit), and the reviewer reads it against the old. Nothing reads `_doc`: `load_vendor_targets` in `bootstrap/_scaffold/install.py` and `_load_vendor_targets` in `tools/session.py` read the rows, shown by reading both, and `test_skills_matrix.py` loads the changed file. *Red when* any non-`_doc` key differs or a fact is lost.
* **The skill.** The `SKILL.md` change is the one phrase near line 28 (and its twin); it points at the routing table instead of naming a harness. `git diff` shows no other line. The skill-contract tests pass.
* **Control for the zero.** Before relying on "no hits", the same search finds the known hit at the parent.

### C3 -- The onboarding package

Hits at the base: 27 (`__init__` 2, `activation` 6, `cli` 4, `security` 5, `shared` 2, `triggers` 7 in the six modules; `onboarding_activate.py:53` 1). Frozen: the six templates and `scripts/onboarding_activate.py`. Finalize seven twins.

* **K1** with the 27 lines. **K2** for seven `.py` files. **K3** for seven pairs. **K4** for seven records.
* **Credits become reasons.** Each credit such as "(Codex P2-5 decision: ...)" or "per Antigravity plan-review P3-1" is replaced by the property the code relies on (for example "the log is tracked and parallel to the deliberation tree", "a distinct exit code so automation can tell the case apart"). `activation.py:179` names `modflow_tools/tools/intent.py` as a precedent; it becomes the intent log's precedent without the project name. *Red when* K5 finds a lost explanation.
* **Behaviour pinned by tests that read these modules passes**: the onboarding and active-surfacing tests listed in *Verification*. `test_ast_attest.py` shows only the 2 failures it shows at the base, and they are not in these files.

### C4 -- The content scanner and the intent tool

Hits at the base: 3 (`templates/modules/team-gated/content_scan.py:329` and `:547`, `templates/modules/team-gated/intent.py:64`). Frozen: `templates/modules/team-gated/content_scan.py` and `scripts/content_scan.py`. Finalize `scripts/content_scan.py` and `tools/intent.py`.

* **K1** with the 3 lines. **K2** for two `.py` files. **K3** for two pairs. **K4** for two records.
* **The scanner's look-alike signs survive.** `content_scan.py:329` is a comment between the string pieces of one regular expression, and `_OHM_SIGNS` holds two look-alike characters that an editor's Unicode normalization would merge. K2(a) catches both, because string constants are part of `ast.dump`. As a direct control: after the edit, `len(set(_OHM_SIGNS))` is 2 when the module is loaded, and the diff has no hunk on the `_OHM_SIGNS` lines. *Red when* either differs.
* **The scanner behaves the same.** `test_content_scan.py` passes, and `python scripts/content_scan.py bootstrap/tests/fixtures/redteam/malicious.txt` prints identical output before and after.

### C5 -- The shipped Markdown

Hits at the base: 8 in five templates (`documentation-plan.md` 4, `documentation_plan_template.md` 1, `incident-trackers.md` 1, `incident_log_template.md` 1, `solo-greenfield.md` 1), and, once C1 counts them, 3 more: the `reviewer=` credits. Finalize `dev/modules/incident_log_template.md` only.

* **K1** with 8 lines, then the 3 credits (the gate counts them from C1). **K3** for three pairs. **K4** for one record. **K5, K6, K7.**
* **The three credits** (`api-access-security.md:101`, `web-hosting-security.md:70` and `:93`) become `reviewer="agent"`, the form `templates/core/NOTICE.md` already uses. The scanner does not read the `reviewer=` value, so nothing is suppressed or revealed: `python scripts/content_scan.py` over the two files prints identical findings before and after (control: the same command on a scratch copy with a planted imperative HTML comment prints a flag). *Red when* the findings differ.
* **`modflow_tools` becomes "the reference deployment" or is dropped** in the five hit lines, without changing a sentence's meaning (K5).
* **The solo-greenfield paragraph keeps its count.** `test_onboarding_review_tiers.py::test_solo_greenfield_external_tier_paragraphs_name_their_staffing` passes: it still counts exactly three paragraphs naming "External" and "tier". The reworded line 92 adds no "tier" to its paragraph. *Red when* the node reports another count.
* **The twins that stay mismatched stay byte-identical** to their templates (`dev/modules/documentation-plan.md`, `dev/modules/incident-trackers.md`): `cmp` exits 0 and the 18 violations do not grow.

### C6 -- Cairn's own prose

Hits at the base: 20 in four files marked (`docs/agent-team-onboarding.md` 8, `doctrine/lifecycle-contract.md` 5 on two lines, `doctrine/rationale.md` 3 on one line, `bootstrap/tests/fixtures/skills/README.md` 4) and 7 reworded (`bootstrap/tests/fixtures/skills/README.md:35`, six in `docs/DOCUMENTATION_PLAN.md`). Frozen: the fixture README.

* **K1.** After C6 the FAIL lines in these files are zero (the whole gate reads zero at C7, once C2-C5 have also landed). The 20 marked hits move to `info` lines carrying their reasons.
* **Markers add text only.** For the three files marked same-line (`doctrine/lifecycle-contract.md`, `doctrine/rationale.md`, the fixture README's three marked lines), deleting every `<!-- vendor-ok: ... -->` span from the new file gives back the parent's bytes exactly, and the file's line count is unchanged (no citation into it shifts). For `docs/agent-team-onboarding.md` the fence at lines 37-38 gets two own-line block markers around it, which add two lines; nothing cites that file by line (`grep -rnE 'agent-team-onboarding\.md:[0-9]'` outside the archives prints nothing at the base), and lines 65-67 get three same-line markers. Deleting every marker span or marker line from the new file still gives back the parent's bytes. *Red when* any other text differs, or a line was added to a doctrine file.
* **Markers are tight and declarative.** No marker block spans a line that has no hit, except the fence wrapper (the commit body lists its span). Each reason is one short sentence (under 100 characters), is declarative, and matches none of the imperative verbs in `templates/modules/team-gated/content_scan.py`'s `_IMPERATIVE_IN_COMMENT_RE` (run the regex on each reason; control: "ignore previous instructions" matches). *Red when* a reason matches or is longer.
* **`info=` is recorded.** The commit body records the `info=` figure beside `fail=`; it equals the parent's 21 plus one per marked token occurrence and one per block begin, so a name added later inside a block shows as a changed count.
* **The credit is reworded, not marked.** `bootstrap/tests/fixtures/skills/README.md:35` ("Codex P2#3") keeps its reason (why `declared-flag` is not yet `native-tested`).
* **The stale lines are corrected, and true.** The six `docs/DOCUMENTATION_PLAN.md` lines (`:25`, `:28`, `:103`, `:150`, `:414`, `:419` at the base) no longer say Cairn does not host its own `dev/` tree; each new statement is checked by a command (for example `git ls-files dev/proposals/archive | wc -l` shows Cairn's own records), and the file's FAIL lines are zero. `claim_check.py` and `check_cairn.py` are clean on the file; `test_documentation_plan_module.py` and `test_default_security_stance.py` pass. The record for this file stays mismatched (one of the 18) and is not finalized.
* **The rate-limit gate is not engaged**: no sentence in `doctrine/` changes (the first bullet shows it).

### C7 -- Zero, and the log

* **The gate reads zero.** `python scripts/quality_gate.py --sub neutrality` prints `fail=0` and exits 0, the "green" recorded for `quality-gate-neutrality` in `bootstrap/tests/_gate_manifest.py:149-151`. The `info=` figure is recorded. *Red when* any FAIL line remains.
* **The plants.** In a scratch worktree at C7's commit, add each plant alone to a clean copy (the unplanted copy reads 0 first, as the control) and record the gate's result: visible prose in a `templates/` file `fail=1`; a whole-line comment there `fail=1`; a `.txt` file there `fail=1`; a `.json` value there `fail=1`; and the named blind spots, each `fail=0`: lower case `claude`; `ClaudeCode`, `GPT4o`, `Claude_Code`; a zero-width character inside a name. *Red when* a "1" row reads 0 or a blind spot reads above 0 (that would mean the claim in this plan is wrong).
* **The one-time search.** Over every added line of `git diff -U0 <base>..<C6>`, search case-insensitively, as a substring, for each of the 20 denylist entries, without using the gate's matcher. For every hit print the containing word and tabulate the distinct words. Read them by hand. Each must be a routing id or a path (`claude-code`, `.claude/skills`, `CLAUDE.md`), a marker reason inside a marker, or an unrelated English word that contains a short name (for example "metadata" for Meta, "decline" for Cline), named as such. A joined, lower-case or odd spelling of a name is a failure. Control: the same search on a scratch line holding `ClaudeCode` shows it. This covers this change's lines only; it is not a standing guarantee. *Red when* a hit is a name in a form the gate cannot see.
* **The pass is logged.** `doctrine/consolidation-review.md` > "Dogfood disposition log" gains rows inside its existing `vendor-ok` block, before the end marker: the checker widened (what, and the 74 to 81); the shipped leaks reworded (counts per class); the illustrative mentions marked; the stale lines corrected; and a row recording the three limits of "zero" and the trigger below. No line is added outside the block, and the gate still reads `fail=0` afterwards. *Red when* the gate reads above 0 after the rows are added.
* **The standing trigger is written down.** The log row states: a Boundary B record after archive that shows a neutrality failure the change under test did not introduce means the commit hook is owed. The trigger is Boundary B's own second command (`AGENTS.md` > "Verification boundaries"), which a person runs; no hook runs the gate today.
* **The twins and the record, finally (SR14).** All 15 pairs edited so far `cmp` clean (the sixteenth, the doc-drift pair, joins in C11); for each of the 12 finalized records the `hash` equals the SHA-256 of its template at the tip; `python bootstrap/verify_integrity.py --target .` lists exactly the 18 files recorded under *Scope*. *Red when* a pair differs, a hash differs, or the list changes.

### C8 -- The note's frame

Frozen: `bootstrap/verify_integrity.py`, `bootstrap/tests/test_verify_integrity.py`. Every node builds its own lockfile, base cache and files in `tmp_path`, and is red at C8's parent for the reason the commit body names (the note does not exist), checked in a throwaway worktree with only the new tests copied in.

* **Order.** `verify()` fixes its exit code and prints its report before calling `_slot_note`; the call is the last thing before the return; the two fail-closed early returns never call it. Tests: a spy in place of `_slot_note` records the captured output at call time and finds the report already there; a second test shows the spy is not called on a missing lockfile and on a lockfile with no files. *Red when* the note is called inside the record loop or before the report.
* **What it receives.** Its parameters are exactly: the target, the accepted non-verbatim records with the bytes the integrity pass already read, the legitimate living-state records, the lockfile's tokens, and an integer count of in-scope records that did not pass. A test reads `inspect.signature(_slot_note)` and finds no parameter named for the violation list, the skipped count, or an exit code. *Red when* a parameter carries any of them.
* **The fence.** An `Exception` or a `SystemExit` raised inside the note prints exactly one line, `slot note: not run (<ExceptionType>)`, naming the type and never the message (messages can carry tree-controlled text), and `verify()` returns the code fixed before the call. `KeyboardInterrupt` is not caught. Tests: spies raising `RuntimeError` with an escape byte in its message, `SystemExit(3)`, and `KeyboardInterrupt` (which propagates). *Red when* the message appears, the code changes, or Ctrl-C is swallowed.
* **The verdict cannot change.** One parametrized test runs `verify()` twice per case, normally and with `_slot_note` replaced by a no-op, and requires equal exit code, equal stdout, and equal stderr once lines beginning `slot note:` are removed. Each case also asserts the hostile value really reaches the note (the record is non-verbatim and accepted, and the coverage line counts it under the expected reason), so the comparison is not vacuous at the parent. The 17 inputs: `base_cache` is not a string; names a directory; names a FIFO (run under a timeout so a blocking open fails the test, not the suite); is a symlink; has a symlinked parent; points outside the target; points outside `dev/.cairn/base/`; holds a NUL byte; the base copy is over the cap; is not UTF-8; `base_hash` does not match; is not a string; `tokens` is not a mapping; has a non-string key; has a non-string value; the installed bytes of a file that passes the integrity check are not UTF-8; are over the cap. *Red when* any case changes the exit code or the report, or is vacuous.
* **The record still fails on its own.** A modified file whose record carries an unsafe `base_cache` still exits 1 with its `modified (hash mismatch)` line. *Red when* it exits 0.
* **The reader (SR12).** One `os.open` per file, with its flags built inside the fenced call by `getattr(os, "O_NOFOLLOW", 0)` and likewise `O_NONBLOCK` and `O_NOCTTY`; no module-level statement names an `os.O_*` flag (a `grep` shows it, and a test deletes the three attributes from `os`, imports the module afresh, and gets the same verdict). `os.fstat` on that descriptor must show a regular file. The read asks for the cap plus one byte (the cap is 256 KiB): a file of exactly the cap is accepted if its hash matches, one byte more is refused. The hash, the UTF-8 decode and the slot parse all use that one bytes object; they never re-read the path. The cap also bounds the installed bytes handed in and the living-state files. Containment: `base_cache` is a `str` without NUL, relative, with no `..`, under `dev/.cairn/base/`, and no component from the target down is a symlink (checked with `os.lstat` per component). *Red when* any of these is absent; the mutation ledger shows each guard is exercised.
* **Buckets.** Every in-scope file lands in exactly one bucket: checked, or one of the four not-checked reasons (D5). A tree with one file per bucket prints the expected counts, and they sum to the in-scope total. *Red when* a file can vanish from the count.
* **Living-state files.** A record whose `dst` is in `_LIVING_STATE_DSTS` is read from disk with the same reader and counted like any other file. A record flagged `living_state: true` outside that set is a violation in the integrity loop already and is counted "failed the integrity check"; it is never read. *Red when* a living-state file is neither read nor counted.
* **The coverage line is always printed when the note runs.** It gives files in scope, files checked, slots checked, slots listed, empty slots awaiting a module, and the files not checked by reason (slot fields read 0 until C9). On a tree with no base copies it still prints, with every file under "no base copy". All names and paths pass through `ascii()`. *Red when* a tree with nothing checkable prints nothing.
* **Imports and tooling.** The engine imports in `bootstrap/verify_integrity.py` are unchanged (`git diff` of the import block adds only standard-library names); `test_scaffold_substrate.py` passes; the Bandit finding set for the file is the same before and after, or each new finding is dispositioned in the record (`test_security_lint.py`).
* **Mutation ledger** (implementer's, recorded in the commit body, each mutant against an unmutated control run): see *Verification*. All C8 mutants are killed.

### C9 -- The listing

* **What is listed.** A slot is listed when its body is unchanged from the base copy's, after whitespace is normalized and the recorded tokens are substituted. Tests: an unfilled slot is listed; a filled one is not; a slot carrying `<!-- cairn:customized -->` inside is not; a slot empty in the base copy is counted "empty: filled when its module is installed", not listed, and gets no advice; a base body with `{{project_name}}` matches an installed body holding the recorded value, and an unknown token is left intact on both sides; a slot present only in the base is not listed; unclosed and unpaired markers list nothing. *Red when* any of these flips.
* **One linear pass.** Slots are found by one pass over the markers using the bounded name pattern of `_MARKER_RE`, on both the base and the installed text. A test (in the style of `test_unclosed_slots_cost_linear_time`) parses a cap-sized text of unclosed openers and a quarter-sized one; the time ratio is under 8 for a 4x size. *Red when* the larger text costs quadratic time.
* **It agrees with the engine.** A test pins the note's marker pass, customized-marker pattern, token pattern, spacing rule and "empty" rule against `_SLOT_RE`, `_SLOT_END_RE`, `_CUSTOMIZED_MARKER_RE`, `_TOKEN_RE`, `_normalize_for_compare` and `_slot_is_empty` in `bootstrap/_scaffold/slotmerge.py` on a table of samples with case and spacing variants (`<!--cairn:slot X-->`, upper case, CRLF, indentation). Where the engine's own routines disagree with each other (`_slot_body_in_text` accepts only the single-space form), the test names the difference rather than choosing silently. *Red when* the note and the engine decide differently on a listed sample.
* **Printable ASCII.** Every character the note prints is printable ASCII or a newline. A slot name and a path holding an escape byte, a newline, a right-to-left mark and a non-ASCII letter appear only as `ascii()` escapes. *Red when* any raw control byte appears (mutant: `str()` instead of `ascii()`).
* **No commands.** For a listed slot, a living-state slot, and a file that failed the integrity check, the note's lines contain none of the words `git` and `python` (matched as whole words, since "legitimate" contains "git") and none of the strings `--finalize`, `scaffold.py` and `$(`. The hash-only warning (this check keeps only a hash, not the text, so it cannot show what changed) and the pointer to `bootstrap/UPGRADE.md` > *Recording an edit you made* appear exactly once per run (D4), after the list, and the warning tells the reader to read the whole file and confirm their edit is the only change. *Red when* a command is printed or the warning repeats.
* **What the lines say.** A listed slot "still holds the text Cairn shipped", says to write the content or `N/A: <reason>`, and, only for keeping Cairn's text on purpose, to add `<!-- cairn:customized -->` inside the slot (never as the way to fill it). A living-state line says to fill it and mentions no recording step. No line says a slot is required or missing: the note reports placeholder state, not obligation; which slots a profile needs is F8 (`dev/PLANNING.md`) and stays separate. *Red when* a line claims an obligation.
* **The loop.** (1) A fresh install lists the `AGENTS.md` slot `project-conventions`. (2) It is filled in the file. (3) `verify()` exits 1, the file is counted under "failed the integrity check", and the slot is no longer listed. (4) The test records the file as `bootstrap/UPGRADE.md` will describe it, `main(["upgrade", "--target", ..., "--finalize", "AGENTS.md"])`. (5) `verify()` exits 0 and the slot is not listed. *Red when* step 4 is removed (the exit stays 1): the way back to a passing check is proved, not printed.
* **A first install with a planted line.** The file has a marked slot filled and a line planted outside it, so it fails the integrity check. The note's lines contain no `--finalize`, no `git diff`, no `git status`; the whole output contains no `git diff`; the coverage line counts the file under "failed the integrity check". The existing hint prints `--finalize AGENTS.md` for this same file by design and is not asserted against. *Red when* a command appears on a note line.
* **Verbatim records are not read.** A verbatim record whose file quotes slot markers in code (as `scripts/_onboarding/triggers.py` does) is neither opened nor counted: a spy on the opener sees no call for it. *Red when* it is opened.
* **The known gap is pinned.** `test_a_placeholder_reworded_by_an_upgrade_reads_as_filled`: when the base copy's placeholder text differs from the placeholder still in the installed file, the slot is not listed. Its docstring says this is a recorded limit, not a guarantee, and C10 records it in the upgrade guide.
* **The hint and the guide agree (SR18).** The hint's text is as `7c077ddf` left it; the assertion `history misses uncommitted edits` in `test_a_filled_customized_slot_is_pointed_at_finalize` still passes; `grep -n "its history since install" bootstrap/verify_integrity.py bootstrap/UPGRADE.md` prints nothing (the same grep prints line 186 of `git show 7c077ddf^:bootstrap/verify_integrity.py`; the phrase "or its history" would not do, because the old source splits it across two string literals). *Red when* the phrase returns.
* **Two real trees.** (a) A fresh `solo-greenfield` install: the note lists the placeholders in the accepted files plus the living-state ones, and the count is checked against an independent count made by a throwaway script over the lockfile; the pristine tree's verdict is 0. (b) Cairn's own tree: `python bootstrap/verify_integrity.py --target .` exits 1 with the same 18 files as before, the note's coverage line reads 0 slots checked, with the files under "no base copy" apart from the two that have one (measured at the base: 35 non-verbatim records, 2 base copies, 1 matching its `base_hash`), and its figures agree with an independent count. *Red when* a figure disagrees.
* **Mutation ledger.** All C9 mutants are killed (see *Verification*).

### C10 -- The upgrade guide

* **Step 4.** The "The workflow" command block in `bootstrap/UPGRADE.md` gains `python bootstrap/verify_integrity.py --target <repo>` as a fourth step after `--apply`, and a bullet says plainly that only a person following the steps runs it; nothing runs it for them (this is the trigger, named honestly because no CI exists).
* **What the note means.** A bullet says it lists slots still holding Cairn's placeholder, that silence plus the coverage line means none found among what was checked, that it never changes the pass or fail result, and that it reports state, not obligation.
* **The known gap.** One sentence: a placeholder that an upgrade rewords reads as filled.
* **The section.** A new `##` heading named exactly `Recording an edit you made`. On whitespace-collapsed text each of these occurs in the section at least once: `the whole file`, `inside your project`, `same-named file`, `your own fill`, `wrong copy`, `keeps only a hash`, `small rewording`, `never proof`, `committed history only`, `uncommitted edits`, `dirty-tree guard`. In prose: read the whole file first, in your project under the `--target` you passed, not the same-named file in the Cairn folder you ran the check from; your own fill must be in what you read, and if it is not you are reading the wrong copy; `verify_integrity` keeps only a hash, so nothing it prints can show what changed; reading finds a line you know is not yours, not a small rewording of Cairn's own text, because the check keeps no copy to compare with; comparing with a copy you trust is an aid, never proof; `git log -p -- <path>` is supplementary and shows committed history only, never uncommitted edits; then record the file with `python bootstrap/scaffold.py upgrade --target <repo> --finalize <path>`, which records the whole file, and whose scoped form skips the dirty-tree guard. The section describes the command and does not claim that any command shows the change. *Red when* a phrase is missing, or the section says a command shows what `--finalize` records.
* **The pointer resolves.** One new node, `test_the_pointer_names_a_heading_that_exists`, asserts that `bootstrap/UPGRADE.md` has a heading named exactly as the note's pointer. It is red at C10's parent and green at C10. *Red when* the heading is renamed.
* **Nothing else moves.** `git diff -U0 bootstrap/UPGRADE.md` shows insertions in "The workflow", the known-gap line and the new section only, plus the code-block edit; `claim_check.py`, `check_cairn.py` and `link_check.py` are clean on the file.

### C11 -- #16's paragraph

* **One paragraph** (at most 8 lines) in `templates/modules/team-gated/doc-drift-prevention.md`, after "The gate catches drift, not absence" in its "Template content" block, and identical in the twin `dev/modules/doc-drift-prevention.md` (`cmp` exits 0; the twin's record stays one of the 18).
* **It names the third category**: prose that names a symbol the code no longer has. It is present, so not absence, and not generated or synced from anything, so not drift from a source; no gate in this module catches it. It states the discipline: when a symbol is removed or renamed, search the docs, README, changelog and docstrings for the old name in the same change; the deliberation record under `dev/` is history and may keep the name; a changelog may name it to say it was removed. It states that no tool ships for this, and the revival rule: promote it to machinery only after three independent recurrences. It names no vendor or project and uses a generic example.
* **No tool, no new file.** `git show --stat` for the commit lists exactly the template and its twin.
* **Gates.** `claim_check.py` and `check_cairn.py` clean on both; the neutrality gate still reads `fail=0`; `test_doc_drift_tools.py`, `test_doc_governance.py`, `test_practice_modules.py`, `test_profiles_smoke.py` and `test_presets.py` pass.
* **The commit body** says that #16 was already closed on GitHub when this landed, and that the commit changes nothing there.

### C12 -- Boundary B and the record

* **The record is complete.** `## Implementation verification -- <agent> -- <date>` carries every field *Verification* lists, includes the node IDs added to `test_quality_gate_neutrality.py` and `test_verify_integrity.py` as `pytest --collect-only -q` prints them, the `fail=` and `info=` figures, the plant table from C7, the mutation ledger, and the AST comparison. *Red when* a field is absent or an ID differs from the collection.
* **The not-touched list is shown.** `git diff --stat <base>..<tip> -- bootstrap/_scaffold bootstrap/scaffold.py` is empty, and the other "Not touched" paths show no change.
* **Status moves** to `awaiting-code-review` in that commit.

### The security findings ledger

Every finding the accepted text took on, with where it is closed or why nothing is owed. Nothing is dropped.

| Finding | What the accepted text requires | Where it is checked |
|---|---|---|
| NU1 | the precedent (zero was reached in May and refilled within hours) and why zero should hold now; a concrete trigger | the CHANGELOG entry (archive) and the C7 log row; the trigger is in *Dispositions* |
| NU2 | a way back to a passing check after filling a slot | superseded by the no-commands revision; the way back is proved by the C9 loop and documented by C10 |
| NU3 | a coverage line, always printed; the reworded-placeholder gap tested or recorded | C8, C9, C10 |
| NU4 | question 1 split: the check closed as won't-build, the sentence half given its own disposition | C11; the issue's state is in *Found while planning* |
| NU5 | the `:446` comment corrected; the twins named | C1; *Scope* |
| SR1 | the stricter checker; the three credits; the one-time search; the plant table; the blind spots named | C1, C5, C7 and the security preflight below |
| SR2 | claims corrected; no remedy for a failing file; the base copy hashed first | C8 (hash gate), C9 (no remedy, no commands); the corrected claims are in the proposal's ledger |
| SR3 | the note is a separate pass after the verdict; every malformed value leaves the verdict alone | C8 |
| SR4 | `base_hash`, containment under `dev/.cairn/base/`, a size cap, escaped names | C8, C9 (`shlex.quote` was withdrawn with the commands) |
| SR5 | the marker only to keep Cairn's text; empty slots not listed | C9 |
| SR6 | no `nosec`, `noqa`, `pragma`, `type:` or encoding line added or removed | K2(b) |
| SR7 | the fixture credit and the stale lines reworded; markers tight and declarative; `info=` recorded | C6 |
| SR8 | the review command | withdrawn by the proposal; no command is printed (C9) |
| SR9 | living-state files read and counted | C8, C9 |
| SR10 | "zero" says whole word and file types; joined spellings named; the substring search; five comment sites; scanning every file declined | C1, C7, the preflight; the decline is kept (the gate walks the filesystem and `templates/` holds untracked `.pyc` files) |
| SR11 | the dropped fallback recorded; the failing-file line points to the guide | C9 (D4, D6), C10 |
| SR12 | the seven build details | C8 (receives, reader, fence, per-record errors, no-op cases), C9 (printable names) |
| SR13 | the superset check; a directive carrying a name fails twice | C1 |
| SR14 | the 12 and the 4; hashes equal the templates'; the 18 unchanged | K4, C7 |
| SR15 | no printed command | C9 |
| SR16 | the planted-line test scoped to the note's lines; the guide leads with reading the whole file | C9, C10 |
| SR17 | which copy to read; the fill must be present; what reading cannot catch | C10; the preflight (S5) |
| SR18 | the hint and the guide disagree about history | landed at `7c077ddf`; guarded in C9 |

## Scope delta

**Scope delta**: preserved. The baseline is the proposal as accepted (Revision 4 binding over 3 and 2, with the Decision's answers), and every outcome maps to a chunk:

| Accepted outcome | Chunk |
|---|---|
| the checker: comment lines, `.json` and `.txt`, four names, five comments corrected, no exemption | C1 |
| the 9 `templates/skills/` hits reworded; `_doc` names no harness | C2 |
| the 38 hits in 14 other shipped templates reworded | C3 (27), C4 (3), C5 (8) |
| the three `reviewer=` credits | C5 |
| the fixture credit and the stale lines reworded | C6 |
| markers for the rest of `docs/`, `doctrine/`, the fixture README | C6 |
| the pass logged; the zero claim stated with its limits | C7 |
| twins changed in the same commit; 12 finalized, 4 left alone | C2-C5, C7 |
| the separate pass after the verdict; what it trusts; the coverage line | C8 |
| what it lists; the remedy with no commands; placeholder state, not obligation | C9 |
| `bootstrap/UPGRADE.md`: step 4, the meaning, the known gap, the new section | C10 |
| the neutrality and install-check tests; the smoke checks (plants, search, comment-only proof, twins, both probes, `check_cairn.py`) | C1, C7, C8, C9, C12 |
| Q1(a): the check half won't-build | recorded in *Found while planning* and *Dispositions* (the issue is already closed) |
| Q1(b): the paragraph | C11 |
| Q2: `upgrade` does not name the slots it adds now | not built; a `defer`, in *Dispositions* |
| SR1-SR18, NU1-NU5 | the ledger above |
| Boundary B full | C12 |

Four things differ from the text in mechanism, none in outcome. Markers are same-line where the hit is prose (the accepted text allows "one line"); C11 is carried here rather than left outside any plan, because the issue that would have held it is closed; the plan-review obligation is stronger than the proposal's header (D8); and the frozen-file count is measured at 14 against an "up to 16" ceiling. No outcome is dropped.

## Verification

**Boundary A (iteration, scoped).** Each chunk runs the tests that own the files it touches, plus its standing gates: `python scripts/check_cairn.py` and `python scripts/claim_check.py <file>` for each edited document, `python scripts/quality_gate.py --sub neutrality` (K1), `python scripts/quality_gate.py --sub redundancy` for scripts, and `python bootstrap/verify_integrity.py --target .` after any finalize (K4). The tests, found by searching `bootstrap/tests` for each touched file's name (all in `bootstrap/tests/`):

| Chunk | Tests |
|---|---|
| C1 | `test_quality_gate_neutrality.py`, `test_quality_gate_cli.py`, `test_quality_gate_redundancy.py`, `test_quality_gate_order_independence.py`, `test_security_lint.py`, `test_gate_manifest.py` |
| C2 | `test_skills_matrix.py`, `test_skills_self_heal.py`, `test_skills_security.py`, `test_skills_install.py`, `test_skills_upgrade.py`, `test_skills_fanout.py`, `test_skills_onboarding.py`, `test_skill_contract.py`, `test_session_kernel.py`, `test_session_failsafe.py`, `test_session_routines.py`, `test_first_session_report.py`, `test_notice_install.py` (twin byte-identity), `test_security_lint.py`, `test_security_check.py`, `test_verify_integrity.py` |
| C3 | `test_onboarding_activation_helper.py`, `test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`, `test_skills_onboarding.py`, `test_active_surfacing_mechanism.py`, `test_active_surfacing_render.py`, `test_trigger_evaluation_action.py`, `test_trigger_evaluation_maturity.py`, `test_deferred_task_store.py`, `test_facade_loader_cleanup.py`, `test_upgrade_side_door_parity.py`, `test_security_leaf.py`, `test_hardening.py`, `test_install_module.py`, `test_module_merge_lockfile.py`, `test_notice_install.py`, `test_ast_attest.py` (the same 2 base failures, no more) |
| C4 | `test_content_scan.py`, `test_security_stack.py`, `test_skills_security.py`, `test_security_verification.py`, `test_default_security_stance.py`, `test_intents_tool.py`, `test_fork_advisory.py`, `test_facade_loader_cleanup.py`, `test_upgrade_module_additions.py`, `test_session_routines.py`, `test_session_failsafe.py`, `test_notice_install.py`, `test_security_lint.py`, `test_verify_integrity.py` |
| C5 | `test_documentation_plan_module.py`, `test_incident_trackers_module.py`, `test_default_security_stance.py`, `test_module_merge_lockfile.py`, `test_evolution_infer.py`, `test_onboarding_review_tiers.py`, `test_presets.py`, `test_profiles_smoke.py`, `test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`, `test_quickstart_sequence.py`, `test_security_verification.py`, `test_security_finding_confidentiality.py`, `test_security_capability_install.py`, `test_api_access_security.py`, `test_web_hosting_security.py` |
| C6 | `test_comprehension_floor.py`, `test_replacement_tools.py`, `test_documentation_plan_module.py`, `test_default_security_stance.py`, `test_doc_governance.py`, `test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`, `test_skills_matrix.py` |
| C7 | `test_quality_gate_*.py` and the gate itself |
| C8, C9 | `test_verify_integrity.py`, `test_fork_advisory.py`, `test_lockfile_module.py`, `test_upgrade_side_door_parity.py`, `test_security_verification.py` (it calls `verify`), `test_scaffold_substrate.py` (import purity of the trust anchors), `test_upgrade.py`, `test_security_lint.py` and `test_security_check.py` (the Bandit gate sees the new code) |
| C10 | `test_verify_integrity.py` (the pointer node); the three prose gates on `bootstrap/UPGRADE.md` |
| C11 | `test_doc_drift_tools.py`, `test_doc_governance.py`, `test_practice_modules.py`, `test_profiles_smoke.py`, `test_presets.py` |

This mapping is not a confident bound: dozens of test files drive a scaffold install, which renders these templates (57 were counted in the `verification-practice` plan). So Boundary B is the real check.

**The comment-only proof (K2).** For each edited `.py`, with `<base>` the chunk's parent:

```python
import ast, subprocess, sys

def stripped_dump(source):
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            first = body[0] if body else None
            if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
                    and isinstance(first.value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.dump(tree)

base, path = sys.argv[1], sys.argv[2]
old = subprocess.run(["git", "show", f"{base}:{path}"], capture_output=True, check=True).stdout.decode()
new = open(path, encoding="utf-8").read()
same = stripped_dump(old) == stripped_dump(new)
print("SAME     " if same else "DIFFERENT", path)
sys.exit(0 if same else 1)
```

Then `git diff -U0 <base> -- <edited .py files> | grep -E '^[+-]' | grep -vE '^(\+\+\+|---)' | grep -nE 'nosec|noqa|pragma|type:|coding[:=]'` must print nothing. I ran the script on a scratch copy of the base: a reworded comment reads SAME, a one-character code change reads DIFFERENT. The interpreter is the canonical one, because `ast.dump` is interpreter-minor sensitive.

**The mutation ledger (C8, C9; the implementer records it, Boundary C may repeat it).** Each mutant is one deliberate break, made in a separate copy and run against the chunk's tests with an unmutated control run beside it. Report each as killed (some test fails), survived (all pass), or equivalent (no behaviour change, shown by a behaviour test through the real entry point). A mutant not shown equivalent by measurement is reported as a survivor. The set: call the note before the report, or inside the record loop; catch `Exception` only (let `SystemExit` through); remove the fence; drop `O_NOFOLLOW`; drop the `fstat` regular-file check; read without the cap; drop the `dev/.cairn/base/` containment; skip the `base_hash` comparison; accept a non-mapping `tokens`; let a per-record exception reach the fence (remove the per-record handler); print with `str()` instead of `ascii()`; print a `--finalize` line; list a slot that carries the customized marker; drop token substitution; read a verbatim record. Every one is expected killed.

**Boundary B mode**: full. The refusal rules in `AGENTS.md` settle it, four ways:

1. **Frozen files change and the pinned collection grows.** Fourteen frozen files change and nodes are added, which touches the gate-manifest contract surface; bounded mode refuses.
2. **Trust-ceremony surfaces are touched.** Vendor-neutrality is a named high-risk surface and this plan changes its checker; `bootstrap/verify_integrity.py` is the lockfile reader adopters run before trusting their scripts; `tools/session.py` is the interpreter binding (comments only); `scripts/content_scan.py` is the content scanner (comments only). Bounded mode refuses.
3. **Ten executable templates (shipped byte for byte) are edited.** Most tests render them. No mapping bounds that confidently, and uncertainty resolves to `full`.
4. **The accepted text says so.**

**How Boundary B runs.** After the last implementation commit (C11), against a clean unchanged commit, under the canonical interpreter (`/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.x). Run it from a separate `git worktree` at the tested commit, which shares refs (so the gate anchor is present) and keeps other sessions' uncommitted files out of the count:

```
CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
python scripts/quality_gate.py --sub neutrality --sub redundancy
```

then `python scripts/check_cairn.py` and `python scripts/claim_check.py` on each edited document. The record is appended as `## Implementation verification -- <agent> -- YYYY-MM-DD` with the template's fields: **Boundary B mode**, **Tested commit**, **Reviewed range**, **Interpreter/runtime**, **Pre-run state** and **Post-run state**, a command table with Command, Exit, Outcomes, Elapsed, **Non-pass disposition**, **Plan-specific acceptance commands**, **Known omissions**.

**Plan-specific acceptance at Boundary B.**

* The neutrality leg exits 0 with `fail=0`; the `info=` figure is recorded.
* The two AST nodes of `test_ast_attest.py` fail at the base for other work. Re-derive the AST verify output at the tested commit's parent and at the tested commit and show them equal; no `_scaffold` byte changed (C12). If the Maintainer has re-anchored in the meantime, both are clean and equal.
* Both probes re-run, as the proposal's smoke checks: install `4ad1c115` (`solo-greenfield`) in a scratch tree, fill all its slots, finalize, upgrade to the tested commit, and run the new `verify_integrity`: the note names exactly the one added slot (`assurance-path-triggers`). Then the partly filled variant (only the three slots `bootstrap/BOOTSTRAP.md` says need the Maintainer's own input filled): the added slot is listed among the others and not singled out; the count is recorded (the proposal's prototype measured 17). That second result is the Q2 limit, recorded and accepted, not a defect. The exact commands go in the record.
* `python bootstrap/verify_integrity.py --target .` lists the 18 files.

**Expected non-pass.** Only the two AST nodes above, each disposed of rather than treated as noise. `test_gate_manifest.py` has no expected failure: changed frozen bytes do not redden it. Any other skip, xfail, xpass or failure is a finding.

**Boundary C** is the code reviewer's, after Boundary B. The points worth attacking:

* **The verdict.** Can any lockfile or file shape change `verify()`'s exit code or the integrity report through the note? Repeat the mutation ledger; add a shape the 17 cases miss.
* **The reader.** Race the path walk against a symlink swap (harmless only because bytes must match `base_hash`; check that the bytes hashed are the bytes parsed). Is any `os.O_*` name reachable at import time?
* **No commands, anywhere.** List the note's print sites from the tree and show none can emit a command or a raw control byte, rather than reading the diff.
* **Every twin.** List the 16 pairs from the tree and, in a separate copy, change one line of code (not a comment) in each edited `.py` template to show K2 notices it.
* **The markers.** Read the placement of each: does a mid-paragraph marker split a list item or a fence? Are the reasons declarative? Did any doctrine file gain a line?
* **The guide, read cold as an adopter.** Can you follow step 4 and the section from `bootstrap/UPGRADE.md` alone? Does the section say which copy to read?
* **The lockfile diff.** Is each finalize commit confined to the `"hash"` lines of its records?
* **The claim "zero".** Do the CHANGELOG text and the log row say what zero does not cover?

### Security preflight, re-answered where the chunking changes an answer

* **S1 -- who supplied it?** Unchanged. Part 1 adds no decision and no exemption. Part 2 decides from installed bytes the integrity pass already matched to the lockfile, a base copy re-checked against `base_hash`, the lockfile's tokens, and the lockfile; all come from the adopter's tree, so steering the note takes a lockfile change that review sees. The note grants nothing and prints nothing to run.
* **S2 -- can it fail?** Both checks can, and the chunking says where it is shown: the gate by the plants (C7) and the superset check (C1); the note by the no-op comparison with its non-vacuity assertion and the mutation ledger (C8, C9).
* **S3 -- what fires it, over what?** Part 1: a person runs the gate at Boundary B and at the gate-manifest ceremony; no hook runs it; it covers the file types in `_NEUTRALITY_FILE_SUFFIXES`, now including `.json` and `.txt` under `templates/`. Part 2: a person runs `verify_integrity`, as step 4 of `bootstrap/UPGRADE.md` says (C10); no CI exists and none is claimed. Both triggers were opened and read in this plan.
* **S4 -- which way does it break?** Every read, type or decode failure becomes a "not checked" count in the coverage line. The exit code is fixed before the note runs and the note cannot reach it. The note prints nothing to run, so no output of it can direct a recording; recording stays the adopter's own act, after reading the whole file.
* **S5 -- who still wins?**
  * **Spellings the gate cannot see**: lower-case and joined spellings, invisible characters, unlisted names, unlisted file types, and anyone hiding a name on purpose. These are closed by enumeration only; the one-time search covers this change's lines only.
  * **A changed lockfile**: anyone who changes the lockfile together with a base copy can steer the note's list. The note grants nothing.
  * **An adopter who records without reading the whole file.**
  * **An adopter who reads but cannot tell.** Reading finds a line one knows is not theirs, such as an instruction to download and run a script. It does not reliably find a small rewording of text Cairn shipped, because the check keeps no copy to compare with. C10 says so and offers comparison with a copy you trust only as an aid, never proof.
  * **The existing hint.** It still prints a `--finalize` command for a modified file with a marked slot, while saying it cannot show what changed. That is shipped behaviour this plan does not change. Since `7c077ddf` it no longer offers history as enough.
  * **Size.** The integrity pass still reads each recorded file whole and uncapped (shipped behaviour); the cap bounds only what the note parses.
  * **A path-walk race** on `base_cache` can happen, harmlessly: only bytes that match `base_hash` go further.

## Dispositions

*Filled at archive-preparation.* Known now:

* **The archive commit writes this plan's `CHANGELOG.md` entry** (applying the changelog-at-archive rule). It states what "zero" covers and what it does not (the three limits from *In brief*), names the note and its limit on a partly filled tree, and names issues #2, #8 and #16's paragraph. Closing #2 and #8 on GitHub is the Maintainer's; the plan does not touch the tracker.
* **Q2 is a `defer`.** `upgrade` itself does not print the slots it adds. It rides with the next engine change to the upgrade path that already owes a re-anchor (it would change at least `merge_file` and `_print_upgrade_report`), or sooner if an adopter misses an upgrade-added slot. The deposit is a board row in `dev/PLANNING.md`, authorized by the Decision's words, quoted verbatim:

  > "Accept A, B, C and D as revised, with every recommended answer, including B’s scope cut and D’s scope delta."

  The row names the trigger: an upgrade-added slot missed on a partly filled tree.
* **The re-anchor row** gets the node IDs of `test_quality_gate_neutrality.py` and `test_verify_integrity.py` at archive (chunk M). This plan carries no Waiting line at archive: the open wait, the re-anchor, is declared on its marked board row.
* **The standing neutrality trigger** (a later Boundary B record that shows a neutrality failure the change under test did not introduce means the commit hook is owed) is homed in the C7 log row and executed by Boundary B's second command; at archive-preparation it is dispositioned `guard` naming that command.
* **The other signals** the proposal named have no executing home today: a reworded comment that lost an explanation (Boundary C reads for it), and the note becoming noise because adopters add `<!-- cairn:customized -->` by reflex or the note names filled slots (no tracker exists). The author proposes, at archive-preparation, one of: a tracker class in an incident tracker, or `wontfix` with the rationale. The noise signal reaches adopters, so it cannot be `wontfix` without the Maintainer.
