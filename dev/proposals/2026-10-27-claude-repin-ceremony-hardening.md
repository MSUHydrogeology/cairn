# Finish the re-anchor ceremony work the repin build left out

**Author**: Claude (Strategy)
**Status**: revising
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-27
**In brief**: List everything in the 2026-08-28 repin strategy note that `repin` did not build, say which items are worth building for 0.5, which can wait and which to drop, and let the Maintainer decide each one.

## Context

**The repin build delivered the routine half.** `scripts/repin.py` (status, package, ceremony) and its tests are built and code-reviewed. The plan `dev/plans/repin-build.md` is at `ready-to-archive`. It waits on the Maintainer-only steps M2, M1, R6a, R6b and M3, which `dev/PLANNING.md` lists for the 0.5 cut. This proposal does not touch them.

**The strategy note, `dev/strategy/archive/2026-08-28-claude-repin-revitalization.md`, asked for more than that build.** The accepted build proposal (`dev/proposals/archive/2026-10-26-claude-repin-build.md`) listed what it left out in its Scope delta and sent each item to "a later proposal". This is that proposal. After it opens, the note is retired, so nothing is lost: every unbuilt item is named below with its source.

**What I checked on 2026-10-27 (Python 3.13, commit `4206505e`):**

* The authority closure still has ten members (`declared_authority_closure()` in `bootstrap/tests/_gate_preflight.py`). The launcher template `bootstrap/reanchor-launcher.template.sh` is not one of them. The operative launcher is made from it before the checker runs, so nothing pins its bytes.
* The launcher keeps its own values reader (`read_values`, `bootstrap/reanchor-launcher.template.sh:151`; the comment at line 140 calls it "deliberately a second one"). The driver has another (`values_field`, `scripts/reanchor_ceremony.py:146`). `scripts/repin.py:952` calls the driver's.
* `bootstrap/REANCHOR_RUNBOOK.md` is 615 lines and still lists the steps whose only job is to service the second reader (RA-01, RA-03, RA-08, RA-15).
* The old launcher in `~/Downloads` is gone (`ls` fails on `~/Downloads/cairn-m2-codex-round2-20260819/`). That note item is closed; it needs no work.
* Nothing runs `python scripts/repin.py status` unprompted. A frozen file can go stale without a red test; `AGENTS.md` says so under "Operational pitfalls".

## Proposal

Seven items. Each has my recommendation; the Maintainer decides each (Q1 to Q7 below). I recommend building A and B for 0.5, and deferring or dropping the rest.

**A. Pin the launcher template as the eleventh closure member.** Source: the note's pre-registered acceptance criterion ("not a tidiness item"). Build: add `bootstrap/reanchor-launcher.template.sh` to the closure list, so the anchor's signature covers its bytes, and test that a changed template refuses. Closure change is a transition ceremony (`bootstrap/REANCHOR_RUNBOOK.md`), so it rides the 0.5 re-anchor. **Recommend: build for 0.5.** It is the one item the note called a security criterion, and the hole is real: the code that runs before the checker exists is pinned by nothing.

**B. Forward every ceremony disclosure, with a control test per disclosure.** Source: the note's second pre-registered criterion. The tools `repin` calls already do this. The driver (`scripts/reanchor_ceremony.py`) does not wrap `repin`, so its disclosures are untested. Build: list each line the driver prints that tells the reader something about trust (for example, that candidate code runs), and add one test per line that fails when the line is removed. **Recommend: build for 0.5**, small, and it closes the failure the note opened with ("nothing below was discovered", printed once while false).

**C. Cut the launcher's second values reader.** Source: the note's economy-of-mechanism argument. Two readers for one grammar had the same injection hole and had to be fixed twice. Cutting it removes four runbook steps and one parity test, but the launcher reads the values before it can trust anything, so the replacement must be a different mechanism, not a call into the artifact. I have not designed that mechanism. **Recommend: defer.** It needs its own design and a Security Review that can read the launcher, and A should land first so the launcher is pinned while it is being redesigned.

**D. Shrink `bootstrap/REANCHOR_RUNBOOK.md` to a page around the tool.** Source: the note's success criterion "the runbooks shrink to a page each". Only the AST runbook is cut by the build (R6a). This runbook is a closure member, so any edit is itself a closure change, and C removes steps from it. **Recommend: defer, and do it with C** so the closure is re-pinned once.

**E. Run `status` automatically.** Source: the note's "the modification-staleness silence is gone" and its risk or volume trigger. Today the silence is visible on demand only. Build options: have the `session-start` orientation print `repin status` when the last pin is older than a set number of protected-path commits; or add a line to the goodnight routine. **Recommend: build only the session-start line, and only if the Maintainer still wants a trigger.** It is a warning only: Cairn's tools warn rather than block unless a real safety property is at stake. The threshold is a number I would pick without evidence; Q5 asks for one.

**F. Key-tier integration: signed-tree binding, a dedicated ceremony key, a typed confirmation at the anchor tier.** Source: the note's section on what the Maintainer attests. The build's Decision recorded one key for releases and the anchor as a departure, and accepted the same-user limit. **Recommend: drop**, unless the Maintainer wants to reopen that Decision. Nothing new has been found since. I list it so the retirement of the note does not hide a choice.

**G. A sterile temporary worktree for staging.** Source: the note's rule "make staging cheap". The build cut it because the dirty-tree refusal had not blocked anyone. **Recommend: drop**, with the earlier trigger kept: revisit if the refusal blocks the Maintainer twice. The record of that trigger is this proposal.

**Not in this proposal.** The Maintainer-only steps M1 to M3 and R6, which `dev/plans/repin-build.md` owns. The two inherited gaps the build's Security Review put on the board (an unsigned anchor commit, inherited `PYTEST_*` variables); they are on `dev/PLANNING.md`.

## Rationale

The note ended up in three parts: what the build did, what it sent to a later proposal, and what the note itself said was wrong. This proposal takes the second part and gives each item a plain choice, so the Maintainer can retire the note without wondering what it still held. I recommend only A and B because they are the two criteria the note pre-registered as security criteria. The rest are either design work that depends on A (C, D), a warning that needs a number (E), or a choice the Maintainer already made (F, G).

**What doing nothing costs.** A stays open: the launcher runs before the checker, pinned by nothing, and a future session that edits the template changes the ceremony's first moments with no signal. B stays open: the driver's disclosures can be deleted in a refactor and no test notices.

## Alternatives considered

* **One proposal per item.** Seven proposals for seven small choices costs the Maintainer seven decisions and seven reviews. One proposal with a question per item costs one review and one sitting.
* **Leave the items in the note.** A settled note that still holds open work is read as done. The unbuilt items need a home that has a lifecycle.
* **Build A to G together.** C and D redesign a trust root and would be built before A pins it. Order matters more than speed here.

## Documentation / doctrine surface

No rule text changes. A edits a closure list in `bootstrap/tests/_gate_preflight.py` (a frozen file) and `bootstrap/REANCHOR_RUNBOOK.md` states the list; B adds tests under `bootstrap/tests/`; E, if built, edits the `session-start` skill and its template twin. These land in the descriptive layer and the code. `dev/PLANNING.md` carries the board row, which the planning session owns.

## Evidence / verification plan

* **A.** A test that changes the template's bytes in a scratch repository and checks the closure check refuses; control: unchanged bytes pass. The closure count reads eleven (`declared_authority_closure()`).
* **B.** For each disclosure line, a test that removes the line and expects the test to fail. A list of the lines is part of the plan. The control is the unmodified driver passing.
* **E, if built.** A test that the orientation prints the line when the last pin is older than the threshold and prints nothing when it is not.
* **Falsifier.** If the plan for A finds that pinning the template forces the launcher's reader (C) to change first, A stops and goes back to the Maintainer. That would show the order I recommend is wrong.

## Signals the change is wrong

* The re-anchor after A takes longer than the Maintainer's report of the last one, because the closure change adds a re-review of the launcher. That would show A is a bigger ceremony than it looks.
* A disclosure test for B fails only on a rewording and never on a removal. That would show the tests pin text, not the disclosure.

## Scope delta

**Scope delta**: preserved. This is the opening version. Items C to G are not recommended for 0.5; the Maintainer's answer to each question is what dispositions them, and the Decision records it.

## Assurance path

**Assurance path**: high-assurance

A and C change the authority closure and the launcher, which are trust roots of the re-anchor ceremony; B edits a ceremony driver. All are high-risk surfaces under `AGENTS.md`, so the Security Review is declared and the plan carries one.

## Questions for the Maintainer

Each has a recommended default. A "yes" to the default is enough.

* **Q1. Build A (launcher template joins the closure) for 0.5?** Default: yes. It rides the 0.5 re-anchor.
* **Q2. Build B (one control test per ceremony disclosure) for 0.5?** Default: yes.
* **Q3. Defer C (cut the second values reader) to a later proposal after A lands?** Default: yes.
* **Q4. Defer D (shrink the re-anchor runbook) and do it with C?** Default: yes.
* **Q5. Build E (a warning at session start when a pin is stale)? If so, after how many protected-path commits since the last pin?** Default: no. If yes, the earlier ceremony ran at 362 commits stale and 74 changed files, and the build proposal measured 5 commits since the last pin; I would pick 25, but I have no evidence for it.
* **Q6. Drop F (dedicated ceremony key and anchor-tier confirmation)?** Default: yes, the earlier Decision stands.
* **Q7. Drop G (sterile worktree), keeping the "blocks twice" trigger?** Default: yes.

## Review -- Claude Sonnet 5.5 (Internal, fresh session) -- 2026-10-27

```
Reviewed commit: e9bf23de (proposal text); tree checked at a0f31a8e
Target: the whole proposal, read against scripts/repin.py, scripts/reanchor_ceremony.py, bootstrap/REANCHOR_RUNBOOK.md, dev/PLANNING.md and dev/plans/repin-build.md
Prior findings: none
Assurance path: high-assurance (not contested)
```

**Conclusion.** The seven-item split is sound and the drops (F, G) and the closed item are right. Two blocking findings: A's cost to the 0.5 cut is not stated (so Q1 cannot be answered), and B is not yet described precisely enough to plan. Everything else is non-blocking.

### Foundations

1. **Should it exist as framed, doing nothing included?** Yes, with changes. Doing nothing leaves the note's two pre-registered criteria open, and the note is retired (dev/strategy/archive/2026-08-28-claude-repin-revitalization.md:346-349). But A and B are not equally urgent or equally priced (B1, B2). Backing: scripts/reanchor_ceremony.py:156-169 (template read, pinned by nothing); no test names the driver's rehearsal banner (grep of bootstrap/tests/test_*.py for "rehearse"/"READ THIS BEFORE" finds none).
2. **Strongest alternative.** Build A as an advisory instead: have the driver and `repin package` print the template's digest at the anchor next to the candidate's and flag a difference. No closure change, no transition ceremony, no new packet. Cost: the anchor's signature does not cover the template as a listed member, so the packet does not bind it. Backing: the driver already prints the candidate's template digest (scripts/reanchor_ceremony.py:211-214) and reads blobs at the anchor (:231).
3. **What would make me withdraw.** If the plan finds that A makes M3 a first-ever by-hand transition needing a new packet and launcher review that cannot land before the cut, A moves after the cut. Backing: bootstrap/REANCHOR_RUNBOOK.md:311-326 (a closure change is a transition and needs a reviewed member set), repin.py:1027 (`repin ceremony` refuses any closure difference).

### Findings

**B1 (blocking). A's effect on the cut is unstated.** "Rides the 0.5 re-anchor" does not say which one. Measured from the tree: A edits `_gate_preflight.py` (closure list), the launcher template (its fixed list at EXPECTED_PATHS must name itself; test_gate_preflight.py:4119-4131 compares the two), and the closure-arity test (:4094, 10 to 11). `_gate_preflight.py` is byte-compared by `repin` (bootstrap/tests/test_repin.py:40), so `repin ceremony` refuses after A until a ceremony anchors it. A therefore turns M3 (dev/PLANNING.md:250-252) from a steady-state by-hand ceremony into the first transition by hand: a reviewed eleven-member packet and a launcher rebuilt from the changed template (runbook :36-48). Order is also forced: A cannot land before M2 (its reviewed commit is 5670dda9) or it makes M2 refuse, the same trap plan B1 caught for R6b. The proposal's "ceremony lengthens" signal (Signals) is the only cost it names, and it is not weighed against the 0.5 cut or "plain, short". *Fix:* add a short "What A does to the cut" paragraph: sequence (after M2, before M3), what M3 becomes, what the packet and the gate-manifest list gain, and one more Q1 option: build A after the cut, with what that loses (template unpinned for one release). Keep the default, but let the Maintainer see the price.

**B2 (blocking). B is not described precisely enough to plan, and its size is asserted.** (a) R6b deletes `drive()` and `--run` (dev/plans/repin-build.md:108; driver lines 546-680, 81 of the file's 176 `say`/`head` lines). B should be written against the post-R6b driver or it tests code about to go; the proposal does not mention R6b. (b) `repin` calls the driver only for `compare`, `check_packet_pair`, `values_field` (scripts/repin.py:980-985); it does not call `rehearse`. `repin` already carries one control test per stage-one and summary disclosure, including "EXECUTES CANDIDATE CODE" (test_repin_ceremony.py:777-810). So the failure the note opened with is already covered on the `repin` path, and "the driver's disclosures are untested" is true (measured) only for what the driver prints on its own path. (c) The note's criterion was "forwarded by the friendly surface"; B quietly changes it to "driver prints are tested". Say so. *Fix:* list the surviving disclosure lines now (a cheap grep, with the count), say whether the standalone driver stays an operator path after R6b, and if it does not, ask whether B shrinks to `compare`'s transition note. Replace "small" with that count.

**N1. Say precisely what A buys.** "Pinned by nothing" is true of the repository, but the launcher cannot verify its own bytes (the operative file differs from the template by one filled slot, runbook :282-283), and its digest is already compared by the Maintainer (:48). What A adds is that a template change since the signed anchor is a visible closure difference and a transition, and that a candidate whose template differs from the reviewed one is refused through the packet row. Also, the "changed template refuses" test is mostly already generic: per-member loops exist (test_gate_preflight.py:1782, :2623). The new tests are membership, arity and the template-lists-itself check. Size A on that.

**N2. Frozen-surface cost of B and A is not named.** New and edited files under `bootstrap/tests/` are frozen by glob (bootstrap/tests/_gate_manifest.py:354-355), so B owes a gate-manifest entry at the cut as well (AGENTS.md, "frozen-file edit owes the gate-manifest ceremony"). The Documentation section names a frozen file for A only.

**N3. E touches a named high-risk surface and maybe doctrine.** `session-start` runs through `templates/skills/_lib/session.py` (self-hosted `tools/session.py`), which owns the interpreter trust root; running `repin status` from it is new subprocess use, a Security Review trigger (AGENTS.md, local interpreter binding). The Assurance path lists A, B and C only. A new orientation line may also change `doctrine/session-routines.md`, contradicting "No rule text changes". If E stays at default no, a one-line note suffices.

**N4. Questions: say what is lost.** Q1 and Q2 have the doing-nothing cost in Rationale but not beside the question. Q3 and Q4 should say that deferring keeps two parsers of one grammar (the injection hole was fixed twice) and the 615-line runbook for now. Q5's 362-commit and 74-file figures match the note (:221); the threshold of 25 is, as stated, unevidenced, which is honest.

**N5. Scope delta wording.** "Preserved" sits beside "C to G not recommended". Nothing accepted is removed here, so say "none against accepted scope; the note's items are dispositioned by Q3-Q7". The build proposal's own review caught the same word used loosely.

### Checked and sound
Ten closure members (`_gate_preflight.py:600-625`; arity test test_gate_preflight.py:4094). Template is not a member (grep of the list: no match). `~/Downloads/cairn-m2-codex-round2-20260819` does not exist (`ls` fails), so that item is closed. The launcher's second reader exists (template:151) and RA-01, RA-03, RA-08, RA-15 are real runbook steps (runbook:113-158). `claim_check.py`: no flags. The instrument can match: the same grep finds `reanchor.sh` in test_reanchor.py.

**Coverage line.** I did not read the launcher template beyond its fixed list, the 81 driver print sites individually, `_gate_preflight.py` beyond the closure function, or `reanchor.sh`. I did not check whether the 5670dda9 reviewed commit constrains A's landing beyond what M2's text says, nor the lockfile or AST ceremonies. No Security Review was done or cleared. I ran no tests, no tool, no re-anchor. Blocking: 2 (B1, B2); non-blocking: 5 (N1-N5).

## Review -- Claude Sonnet 5.5 (usual, fresh session) -- 2026-10-27

```
Reviewed commit: e949eec3 (the proposal as it stands after the first Internal review); tree checked at 03b31d55
Target: the whole proposal, against the source note, the build proposal's Scope delta, dev/plans/repin-build.md and the tree
Prior findings: the first Internal review above (B1, B2, N1-N5). I do not repeat them; I say where I agree and where a premise is wrong.
Assurance path: high-assurance (not contested)
```

**Tier**: usual (the Security Review is a separate pass by another reviewer; not done and not cleared here). **Verdict**: REVISE. **Findings**: 2 blocking (R1, R2), 3 non-blocking (R3-R5).

**Conclusion.** Every fact in Context is true except one (R3), and building A and B for 0.5 and deferring C and D is sound. Two things must change before the Decision. The proposal says every unbuilt item is named, and at least three are not (R1). And the first review's cost of A rests on a premise the tree contradicts: M3 is already a closure transition (R2).

### Foundations

1. **Should it exist as framed, doing nothing included?** Yes. The note is retired on the claim "Nothing in this note is still open" (note :391-393), so an incomplete list loses items for good. Backing: R1; the build's Scope delta (build proposal :1240-1255) compared item by item.
2. **Strongest alternative.** Do A together with C and D as one closure change after 0.5. It saves a second hand transition on the same launcher (R4). It costs one release with the template unpinned, which the Maintainer's by-hand digest comparison (runbook :48) partly covers. Backing: `git diff 6f29519d HEAD -- bootstrap/tests/_gate_manifest.py` (R2) and runbook :48.
3. **What would show it wrong.** A's marginal cost (a rebuilt launcher and one more reviewed member) turning out larger than the Maintainer's report of the last ceremony; or the omitted items (R1) needing a decision the proposal already made by silence. Backing: proposal Signals section; the note's out-of-band passage (:304-316).

### Check 1: unbuilt items in the note against A-G

Matched: RD-3 template (A), disclosure criterion (B), second parser (C), runbooks shrink (D), staleness silence and risk trigger (E), dedicated key and typed confirmation (F), sterile worktree (G), `~/Downloads` launcher (closed, `ls` fails), the signed tree and double hash (build accepted, build :1244). Built, not unbuilt: classification, transaction, protected-set rule, lockfile adapter, zero-member rule (build :1258). Not matched:

**R1 (blocking). Four items are dropped silently.**
(a) The note says to **delete the claim** that out-of-band delivery on one machine adds assurance, and add a dated upgrade trigger (note :304-316). The runbook still makes the claim (`bootstrap/REANCHOR_RUNBOOK.md` :27, :48, :283, :377, :401, :438). It is a closure member, so it belongs with D, and a written control naming a party who does not exist is the note's own definition of worse than none.
(b) The build's Scope delta keeps "not for the checker's internal messages the launcher does not print" (build :1246). B covers only "each line the driver prints".
(c) The note's success criterion that REL-1 closes under disposition (a) (note :362-364). I could not find the register row (grep of `dev/` finds REL-1 only in the note, the build and one reflection), so I cannot say whether it is open.
(d) "The previous pin covers the tool that moves the next one" (build :1247) is closed only by M2. Say that in one line so the retirement hides nothing.
*Fix:* add (a)-(d) as rows, each with a recommendation and a question or a "closed by X" line. Drop the "every unbuilt item is named" claim until they are in.

### Check 2: the facts in Context (measured, Python 3.13.13)

True: `declared_authority_closure()` returns 10 members and the template is not one; `read_values` is at template :151 and the "deliberately a second one" comment at :140; `values_field` at `scripts/reanchor_ceremony.py:146`; `scripts/repin.py:952` calls `rc.values_field`; the runbook is 615 lines; the `~/Downloads` directory is gone; commit `4206505e` exists and is an ancestor of HEAD. Not true as written: R3.

**R2 (blocking). M3 is already a closure transition, so A is cheaper than the first review said.** `bootstrap/tests/_gate_manifest.py` is a closure member, and it differs from the anchor `6f29519d` by two deleted lines (commit `fa86e2cb`, `git diff 6f29519d HEAD`). So `repin ceremony` will refuse the closure difference and M3 is by hand either way (repin.py:1027; PLANNING :250-252). A's marginal cost is then an eleventh packet row and a launcher rebuilt from a template that lists itself, not "the first transition". The Response to the first review's B1 should be written from this. Second, and outside this proposal, read from code and not run: `boot()` byte-compares the 10 `LISTED` files at HEAD with the anchor's entries on every verb, `_gate_manifest.py` is one of them (scripts/repin.py:62-67, :290-295), so M2 as planned (`--first-run --reviewed-commit 5670dda9`) looks like it refuses at today's HEAD. Someone should run `python scripts/repin.py status` and tell the plan owner before the Maintainer's steps start.

### Check 3 and 4: recommendations and Scope delta

Build A and B: sound, with R2 correcting A's price and the first review's B2 on B. Measured for B: `repin` calls four driver functions, not `rehearse` (grep of `rc.` in repin.py: `compare`, `check_packet_pair`, `packet_artifact_digest`, `values_field`). After R6b the driver's `main` stays as a read-only preflight (reanchor_ceremony.py:681-760, 172 `say`/`head` lines by my grep). B is small only if written against that remainder. Defer C and D: sound, and PLANNING :476-479 now carries the rows (03b31d55). Drop F and G: sound; G's trigger is on the board. E at default no: sound.

**R3 (non-blocking). "Four steps serve the second reader" is overstated.** Context :20 and C say RA-01, RA-03, RA-08, RA-15 exist only to service it. The runbook text says that of RA-01 only (:113-118). RA-03 and RA-08 are re-hash checks (:119, :134). RA-15 is the digest the Maintainer computes, which the build restored on purpose (build Rev. 3, "six steps including the digest comparison"). The note itself says "three" at :198 and lists four at :128. *Fix:* "one to four, counted in C's design".

**R4 (non-blocking). A first, then C and D, costs two hand transitions on the same launcher.** A pins bytes that C will change, and C and D are closure edits too. This is acceptable, because a pin in the meantime is worth something, but the Q3 and Q4 text should say that two transitions, not one, is the price.

**R5 (non-blocking). Scope delta wording.** "Preserved" is literally true (the note's items are not accepted scope) but reads as "nothing is lost". With R1 fixed, say "none against accepted scope; the note's items are dispositioned by Q1-Q7 and R1's rows". The first review's N5 says the same.

### Falsification ledger

| Probe | Result |
|---|---|
| Re-run `declared_authority_closure()` | 10, template absent; matches the proposal |
| Open each cited line (template :140, :151; driver :146; repin :952) | all four say what the proposal says |
| `git diff 6f29519d HEAD` over all 10 members plus the template | one differs (`_gate_manifest.py`); R2 |
| Grep runbook for "out-of-band" | at least six live uses; R1(a) |
| Grep tests for driver disclosure strings | none named for `rehearse`; repin's own are at test_repin_ceremony.py:777-810 |
| Instrument can match | the same grep finds the repin disclosures, so an empty result for `rehearse` is real |

**Coverage line.** I did not run `repin status` or any test, so R2's M2 refusal is read from code, not shown. I did not read the launcher past :138-160, the 172 driver print sites one by one, the security strategy (REL-1 state), `reanchor.sh`, or the plan's chunk text beyond R6b and M2. I did not check the 25-commit threshold, nor the lockfile and AST ceremonies. No Security Review was done or cleared. A second author claim (`claude-d8d22f62`, "Response and Revision 1") was open on this file when I claimed it; this review reads e949eec3, not that Response. Blocking: 2; non-blocking: 3.
