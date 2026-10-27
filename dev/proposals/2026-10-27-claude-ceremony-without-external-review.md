# Let a fresh local agent read the re-anchor ceremony's code, and ask the Maintainer only for what he can do

**Author**: Claude Sonnet 5.5 (Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-27
**In brief**: The re-anchor ceremony says an outside security review must read its launcher, which the Maintainer cannot arrange, so this proposes a one-time interim authorization for the 0.5 cut (a fresh agent builds and a second fresh agent reads, he compares digests and signs) and then a rewrite after the cut that makes a fresh local agent plus automated scanners the standard reader, with a short human yes/no check before signing.

**Lane**: deliberate (a trust-ceremony surface). **Assurance path**: `high-assurance`.

## Context

**Conclusion first.** The ceremony cannot be run as written, because it asks for something the Maintainer has said he cannot supply. The 0.5 cut needs one hand ceremony first. I recommend an interim for that one ceremony, then a rewrite after the cut. Below it is plain what that costs in assurance.

The Maintainer, in chat on 2026-10-27, on the ceremony:

> "We cannot require an External Security review. The runbook must be updated. The reality is that I do not, nor do most scientists-as-coders, have the expertise to provide the 'you do this by hand' that you are asking. That is why we are making this process more automated. I can confirm that 1=1, and simple things. I can provide a signing key. But I cannot do anything that requires checking lots of code against itself. That has to be a local agent, and we have to have a system that trusts it to be correct, provided certain conditions are met and that we are developing in a trusted environment. I like having a human in the loop before things get signed off for a release, but that human really should be providing a pro-forma check that the tests evaluate for dangerous or malicious additions."

And on the 0.5-cut route, the same day (his answer to the planning session's question):

> "Interim for this ceremony, rewrite after (Recommended)"

**Terms.** The *anchor* (`refs/cairn/gate-anchor`) is a signed marker of which version of the test gate to trust. *Re-anchoring* moves it, and only the Maintainer's *ceremony key* (a signing key that does nothing else) can do that. The *authority closure* is the 11 files that decide what the ceremony runs (`EXPECTED_PATHS`, `bootstrap/reanchor-launcher.template.sh:53-64`). The *launcher* is the short shell program, made from that template, that checks everything before any new code runs. The *packet* is a list of those 11 files' digests. A *digest* is a fingerprint of a file's bytes (SHA-256): two equal digests mean the same bytes.

**What the ceremony demands today (read, not run).**

* The launcher and packet "come from" an External Security review, and the Maintainer verifies the launcher's digest "against the review's record" (`bootstrap/REANCHOR_RUNBOOK.md:36`, `:48`, `:282-286`; `bootstrap/reanchor-launcher.template.sh:5-9`, `:18-21`; `scripts/repin.py:965-970`, which prints "Paste the launcher digest from the review's record"). `doctrine/dual-review.md:85-91` calls this the one standing call: the Maintainer chooses the reader each time and records it with `**Called by**`.
* The Maintainer is told to exercise judgement at the report (`REANCHOR_RUNBOOK.md:89-93`, `[RA-14]` at `:157`; `scripts/reanchor_ceremony.py:588`, `:625`).
* First use "is gated on a focused External security review of the exact checker bytes" and the Maintainer is told to "review the exact verifier bytes" and compute six modules' hashes (`REANCHOR_RUNBOOK.md:372-390`), then hand-run manifest, commit and `update-ref` steps (`:392-436`), after a long sterile `git` command that is "irreducibly the operator's to know" (`:203-225`, `:224`). Phase 4 has more hand ref steps (`:457-538`). **Not established:** whether Phases 0 and 4 are still the live path now that the launcher exists. The plan must check.
* No program in the tree builds a packet or fills the launcher's slot. Only a test helper does (`bootstrap/tests/test_repin_ceremony.py:79-91`; `git grep` for `cairn-authorization-packet` finds only consumers).

**Measured today (Python 3.13.13, commit `40c92fd0`).**

* `python scripts/repin.py status` stops: `_gate_manifest.py` at HEAD differs from the anchor's entry. So the hand ceremony comes first (`dev/PLANNING.md`, "The 0.5 cut").
* The anchor is `6f29519d`; HEAD is 402 commits on and 273 files changed. **The closure itself changed in 4 of its 11 files, 35 lines added and 17 removed** (`git diff --stat` over the 11 paths). That is small enough for an agent to read in full.
* **The existing scanners do not read the closure.** `scan_targets()` in `bootstrap/security_check.py:682` returns 66 files (so it can match) and none of the 11 closure files is among them: `bootstrap/tests/` is excluded on purpose, and the shell and Markdown members are not Python. The Bandit gate (`bootstrap/tests/test_security_lint.py`) and `scripts/quality_gate.py` (sub-gates: order-independence, neutrality, redundancy) therefore say nothing about the files that matter most here. The differential oracle lists the gate files as sensitive (`bootstrap/tests/_oracle_activation.py:34-47`) but compares engine behaviour, not ceremony code. **Any "scanners looked for dangerous additions" claim about the closure would be empty today.**
* Not checked: how the old External review was commissioned in practice beyond what the runbook and the archived hardening plan say.

## Proposal

### The Maintainer's part: exactly what he said he can do

1. Confirm that two digests are equal (launcher; package; the commit id; his key's fingerprint).
2. Run a few printed commands and read a plain-language report.
3. Supply the signing key (RA-16; still the one fence no code enforces: `REANCHOR_RUNBOOK.md:51`, `SECURITY.md:193-231`).
4. Give a short pro-forma yes or no (below).

**Steps that ask for more than that**, to be removed or handed to an agent: the External-review sourcing (`REANCHOR_RUNBOOK.md:36`, `:48`, `:282`; template `:5-9`, `:18-21`, `:577`); "exercise judgement" at the report (`:89-93`, `:157`; driver `:588`); "review the exact verifier bytes" and compute hashes "yourself... independently of the tool" (`:372-390`); the sterile acquisition command (`:203-225`); the hand-run steps 2 to 4 and Phase 4 (`:392-436`, `:457-538`) if still live; `SECURITY.md:167` ("confirms the package's digest independently") and `:234` ("the Maintainer reviews the preflight result").

### What a local agent does instead

A *fresh-session agent* is one started new, with no memory of writing the change. It (1) builds the packet and fills the launcher's one slot; (2) reads the closure diff in full (it is 52 changed lines today); (3) runs the scanners and tests that exist and a fixed list of commands that search the closure diff for dangerous additions (the plan holds the list, not this proposal); and (4) writes a committed review record. **Two agents must not be the same session:** the builder and the reader. **Neither may be a session that wrote any commit in the range being blessed.** That is the forbidden "implementer blesses its own verifier" (`REANCHOR_RUNBOOK.md:11-15`).

### Conditions the system trusts the agent under

Each is checkable by a printed line the Maintainer reads, or a test. Two are statements, and I say which.

* **C1, trusted machine.** His own checkout, values file outside the repository, nobody else with write access (the posture at `REANCHOR_RUNBOOK.md:339-368`). *A statement:* nothing can prove a machine is trusted. The ceremony prints host, user and checkout path; he answers yes.
* **C2, fresh and distinct sessions.** The record names the builder, the reader, the models, and says neither wrote a commit in the range. *A statement:* git cannot show it (every agent commit carries his git identity; trailers name only a model). The next reviewer and he check the line.
* **C3, record committed before signing, bound to the bytes.** The record is a committed file that states the packet digest, the launcher digest, the candidate commit and the 11 members' digests. Test: the closure's digests at the candidate equal the record's; a record that is missing or older than a closure change is refused.
* **C4, the named list.** The report must show, each as a count and the names: new executable files (new `.sh` or `.py`, new executable bit); added lines that start a process, touch the network or write a file; **every change to the gate's own files** (the 11 members, the gate manifest, the AST baseline, the oracle's sensitive list); and every scanner finding. Any non-zero count is explained in the record in plain words.
* **C5, the instrument can fail.** Each scan is shown catching a planted bad line in a scratch copy (a control) before its "none found" is believed. Because the Bandit gate reads none of the 11 files, the record must say which members were read only by the agent.
* **C6, the key stays out.** No agent loads or handles the ceremony key. This is today's two-stage split and dedicated key (`SECURITY.md:148-231`); it is unchanged.

### The human's pro-forma check

A short page, written plainly, ends the ceremony's reading. **Equalities, he compares:** (E1) the launcher's digest printed by the tool equals the digest in the committed record and in the reader's chat hand-off; (E2) the commit id printed equals the one `git rev-parse HEAD` shows him; (E3) the two package digests (the ceremony's and `shasum`) agree; (E4) the key fingerprint printed equals `ssh-keygen -lf` of his own key; and the two `SAME` commands from the hardening plan's C7 print `SAME`. **Yes or no:** (Y1) is the record present, committed, and written by a session that is not the author? (Y2) are the gate-file changes listed the ones this release was meant to make (the plan names them)? (Y3) is every count in the C4 list zero, or explained? (Y4) did every scanner and test pass, or is each failure named in an earlier allowance? (Y5) is this his own machine with the key unloaded until now? **What a yes means:** the numbers on the page match what he asked for and a fresh agent says in writing nothing dangerous was added. It does **not** mean he audited code. Any no stops the ceremony; nothing is signed.

### Options for the 0.5 cut

* **(a) Interim for this ceremony only, rewrite after the cut. Recommended; the Maintainer's stated choice.** For this ceremony only: the packet and launcher are built by a fresh-session agent that wrote none of the change; a second fresh-session security reviewer reads them and the 4-file closure diff and runs the scanners; the reader's record is committed before he signs; his only parts are the digest comparisons, the C7 `SAME` commands and the signing. **No runbook, launcher or doctrine text changes first**, so no closure member changes and no extra transition is owed. His authority is the Decision block below: it names the reader (as `doctrine/dual-review.md:85-91` already lets him) and says in plain words that the reader is a same-vendor fresh session, not an outside one. **Cost:** this one ceremony is blessed under text that still says "External", by a Decision that overrides it once; the reader has the same blind spots as the builder; the rewrite's text edits touch closure members, so they need another hand transition (`scripts/repin.py:1027-1029` refuses closure changes), which can ride with the next transition that is owed anyway.
* **(b) Rewrite first, then the ceremony.** This proposal goes through its plan; the text and the record format land, then one ceremony. **Cost:** the cut waits on a proposal, plan, plan review and code review; the earlier plan's order rule means every closure edit lands before the ceremony. **Gain:** one ceremony, under the final text.
* **(c) Rewrite the text only, defer the report tool.** Same as (b) with no new code. **Cost:** the "tests evaluate" half stays an agent's grep plus the existing scanners; same delay as (b).
* **(d) Wait for an outside reader, or do nothing.** The Maintainer has said he cannot arrange one; the cut stays blocked. Listed only because "do nothing" must be priced.

**Why (a):** it is the only option that moves the cut now, it keeps every machine check and the key fence, and the closure diff is small enough that a fresh agent's full read is real. Its extra hand transition later is paid only if nothing else needs one first.

### The rewrite after the cut (the normal process; (a)'s second half)

A mechanical report verb, built as tested code and itself pinned, produces the C4 list and prints the pro-forma page; the ceremony refuses without a committed record that matches the closure digests (C3). Text changes, with where each lands (none is edited by this proposal):

| File | Change | Note |
|---|---|---|
| `bootstrap/REANCHOR_RUNBOOK.md` | "External Security review" (`:36`, `:48`, `:282`, `:372`) becomes the builder and fresh reader; the judgement wording (`:89-93`) becomes the pro-forma page; Phase 0 step 1 and the sterile command become an agent step | closure member |
| `bootstrap/reanchor-launcher.template.sh` | comments only (`:5-9`, `:18-21`, `:577`); `EXPECTED_PATHS` untouched | closure member |
| `bootstrap/reanchor.sh` | comments only, if any say "review produced"; the citation of a retired review record (`:175`) stays | closure member |
| `scripts/reanchor_ceremony.py` | `:163`, `:588`, `:743` text | keyed, listed by `repin`; edits must be deletion-only if the earlier row for it still stands |
| `scripts/repin.py` | `:965` prompt text | needs its own code review before `--first-run` |
| `doctrine/dual-review.md` | `:85-91`, the standing call, rewritten to the new reader | doctrine rate-limit gate: the Maintainer's words above are the Decision input |
| `bootstrap/SAFETY.md`, `SECURITY.md` | `SAFETY.md:657-658` ("instantiated by review"); `SECURITY.md:167`, `:234`, `:237` | not closure members |

Left as they are: the printed and docstring uses of "external review" in `bootstrap/tests/_gate_preflight.py` (e.g. `:1010`, `:2801`). Editing that closure member and listed file buys wording only and forces its own transition.

## Deferred runbook items

The Maintainer asked whether the queued runbook items should be done now. The earlier hardening proposal deferred them (`dev/proposals/archive/2026-10-27-claude-repin-ceremony-hardening.md:32`, `:34`, `:354`; queued rows `dev/PLANNING.md:503-507`). Each is a closure edit, so under (a) none can precede the ceremony. My recommendations, each with a default:

* **D, shrink the 622-line runbook to a page: do it inside the rewrite.** Most of its length is the hand steps (Phase 0 `:197-449`, Phase 4 `:453-538`) that this proposal removes anyway, so doing it separately would edit the file twice. One transition. Default: yes. If not: the runbook keeps its dead steps until a later transition.
* **C, cut the launcher's second values reader: stay deferred, after the rewrite.** It is a launcher redesign (the launcher must read the values file before it can trust anything), and it needs its own design and a Security Review that can read the launcher (`:32`). Folding it in would put an undesigned mechanism into the one file the interim ceremony relies on. Default: defer. If not: the rewrite waits on a design nobody has written.
* **I, the checker's messages the launcher does not print: probably superseded, keep the trigger.** The plain-language page prints the counts and names the Maintainer needs, so a refusal he cannot read matters less. Its trigger (a refusal his screen did not explain) stays. Default: defer. If not: a launcher-against-checker read becomes part of this Security Review.
* **"Classify before showing" (which changed files DECIDE versus are merely PINNED, `dev/strategy/archive/2026-08-28-claude-repin-revitalization.md:187-195`): it is the pro-forma page; fold it into the report verb.** What I verified in code: `repin` already prints "N of 11 authority files differ" and names them (`scripts/repin.py:415-431`) and the commits behind each changed file (`:377-412`); the stage-1 report sorts every changed path into five classes from the gate manifest's own policy, with unclassified paths listed in full (`bootstrap/tests/_gate_preflight.py:1138-1145`, `:1203-1222`). **Not present:** a decides-versus-pinned split (no match for it in `scripts/repin.py`, `reanchor.sh`, the checker or the driver; the `_classify` at `repin.py:343` sorts AST symbols and is unrelated), the added-line scan, and the executable-file list. So C4 is partly built; the report verb adds the missing three. Default: yes.

## Rationale

The Maintainer has already said what he can do, and the 2026-08-27 finding says a control that names a party who does not exist is worse than none (`dev/strategy/2026-08-05-codex-security-strategy.md`, [REL-1], read through the commit message of `45e10d2c`). The runbook already concedes that handing a file over on one machine adds no assurance of its own (`REANCHOR_RUNBOOK.md:445-449`). What an outside reader added was a different reader, not the handover. This proposal keeps what a single machine can enforce and states honestly that it lost the different reader.

## Alternatives considered

(b), (c) and (d) above. A fourth: trust the Maintainer's "yes" alone with no record. It loses the C3 binding, so a stale or swapped file could be blessed by an honest yes. Rejected.

## Documentation / doctrine surface

Doctrine: `doctrine/dual-review.md` (governing layer; rate-limit gate noted). Closure members and descriptive prose in `bootstrap/` and the root. Nothing under (a) edits any file. The table above is the rewrite's surface.

## Evidence / verification plan

For (a): the builder's and reader's commits exist and the record is committed before signing; the `SAME` commands print `SAME`; stage 1 and 2 refusals are the existing ones. For the rewrite (plan owns the mapping, full suite only at a certifying run): tests that refuse a missing or stale record, that show each scanner catching a planted line, and that the report prints each C4 count including zeros.

**Security preflight.** S1 (who supplied it): the packet, launcher and record are supplied by agents on the same machine; the Maintainer supplies the key and the equalities. S2 (can it fail): the digest equalities can fail on any changed byte; **the record's own digest and "fresh session" lines cannot be checked by a machine** and I say so. S3 (what fires it): a person running the ceremony; no job observes it. S4 (which way it breaks): a missing record must refuse, never pass. S5 (who still wins): a compromised development machine or a poisoned input that fools both agents; see below.

## Assurance, honestly

**Still stopped:** accident; a careless or confused agent; a closure change slipping in unreported (the packet pins all 11 digests and the launcher measures a transition itself, `reanchor-launcher.template.sh:571-612`); candidate code running while the key is loaded; a stale or wrongly signed anchor; any agent moving the anchor alone, since only his key can.

**No longer stopped:** a malicious change written by a compromised session or a poisoned input, in files only agents read, that a same-vendor fresh agent also misses or is steered past. The old design put an outside reader in that gap; this one does not. The Maintainer's yes is now backed by a report from the same machine, and he cannot judge it. Plain words: the key still decides whether the anchor moves, but what he is told when he turns it is no longer cross-checked from outside.

**Signals this is wrong:** the record's digest and the printed one disagree for a reason no one can explain; a planted bad line is not caught; the reader's record lists nothing that the closure diff shows; a later outside read finds a dangerous change that the fresh reader passed; the report's zeros turn out to come from an instrument that could not match.

## Scope delta

**Scope delta**: degraded. The baseline outcome "an External reader reads the launcher" is replaced, not kept. **disposition**: guard. It stays available as the Maintainer's call under `doctrine/dual-review.md`; only the standing requirement goes. Specifying the replacement (above) was preferred to cutting.

## Questions for the Maintainer

1. **Accept (a) as the Decision for this ceremony, with the reader being a fresh same-vendor session?** Default: yes. If not: the cut stays blocked.
2. **Must the builder and the reader differ in model, not only session?** Default: no, session only (the record names the models). If yes: we lose time finding a second model and gain a little more distance.
3. **Do you want the reader's launcher digest also stated in chat (E1)?** Default: yes; it costs nothing. Without it the record is the only copy and sits in the same workspace as the launcher.
4. **After the cut, may the rewrite (with the runbook shrink, item D, and the report verb, with C and I left deferred as above) wait for the next transition that is owed anyway?** Default: yes. If not: one extra hand ceremony just for text.
5. **Until the report tool exists, is the agent's grep list plus existing scanners enough for the "tests evaluate" half?** Default: yes for the 4-file diff, with the gap stated in each record. If not: the report tool is built before the cut (option (b) or (c)).
6. **Should the interim's reader also be asked whether Phases 0 and 4 are still live?** Default: yes, as a finding in its record. If not: the unused steps stay in the runbook until the rewrite.

## Decision -- (the Maintainer's, not yet made)

Left empty for the Decision block. If (a) is accepted, its authorization is quoted here verbatim, with the reader named.

## Revision 1 -- Claude Sonnet 5.5 (author) -- 2026-10-27 -- the complete current contract

**This revision supersedes everything above and is the whole contract.** No review of the first text was committed. The Maintainer then changed his route, in chat, 2026-10-27:

> "Please go ahead and do all of it now, I changed my mind. The re-anchoring is such an ongoing issue that we just need to tackle it. Period."

**Conclusion first.** Build all of it now, before the 0.5 cut, as one change set that one hand ceremony pins: a ceremony the Maintainer can actually run (equalities, simple checks, his key, a pro-forma yes), a fresh local agent as the standing reader, a plain-language report made by a tested tool, a shorter runbook, one values reader instead of two, and the old hand path deleted. **The cost to the cut is time**: the cut now waits behind a proposal review, a plan with two reviews, five code chunks and their code and security reviews, a certifying run, and then the ceremony. I have not measured how long that is. The nearest precedent is the hardening change (6 commits, proposal to code review in one day, `dev/plans/archive/repin-ceremony-hardening.md`); this is larger, and the launcher change is the slow part. I assume days, not hours.

### What is true today (read or measured, Python 3.13.13, HEAD `e6c2688b`)

* **Measured.** `python scripts/repin.py status` stops: `_gate_manifest.py` differs from the anchor. The anchor `6f29519d` is about 400 commits back; 4 of the 11 closure files changed (35 lines added, 17 removed); the anchor is unsigned (`dev/PLANNING.md:440-448`).
* **Measured.** The External-review requirement is prose, two comments and one prompt, not a code gate: `REANCHOR_RUNBOOK.md:36`, `:48`, `:282`, `:372-390`; template `:5-9`, `:18-21`, `:577`; the prompt at `scripts/repin.py:965-970` compares a pasted digest with the launcher's own SHA-256. Nothing needs relaxing; the text and the prompt change. (A second session measured the same.)
* **Measured.** `scan_targets()` (`bootstrap/security_check.py:682`) returns 66 files and none of the 11 closure members. Running Bandit on the 7 Python members gives 54 findings, all LOW (27 `B603`, 20 `B607`, 7 `B404`; no MEDIUM or HIGH), so adding them to the gate passes today and would catch an added `eval` or `shell=True`. It would **not** catch a new, ordinary subprocess call (LOW, not blocking), nor anything in the shell and Markdown members.
* **Read, not run.** `repin` already prints which closure files differ (`scripts/repin.py:415-431`) and the commits behind each; the stage-1 report sorts paths into five gate-policy classes (`bootstrap/tests/_gate_preflight.py:1138-1145`, `:1203-1222`). Not present anywhere I searched: a decides-versus-pinned split, an added-line scan, an executable-file list.
* **Read.** The driver has an undefined name in an error path (`template`, `scripts/reanchor_ceremony.py:176`, should be `TEMPLATE_REL`), a stale docstring (`:163`, "NOT itself a closure member", false since the launcher template joined), and the "delivered out of band" print (`:743`). `repin ceremony` refuses any closure change (`scripts/repin.py:1027-1029`).
* **Read, not reproduced.** The queued report that the ceremony's test collection inherits the caller's environment (`dev/PLANNING.md:452-460`): `gather_evidence` in the checker copies `os.environ` minus only `PYTHONPATH` and `PYTHONHOME` and runs the candidate's manifest producer with `-E -s` (`bootstrap/tests/_gate_preflight.py:1461-1472`). `-E` ignores `PYTHON*` variables, not `PYTEST_ADDOPTS`, so the reported drop of 9 of 4,650 tests with exit 0 is plausible from the code. The row names the driver, `reanchor.sh` and the template; the code that builds the environment is in the checker, a closure member.
* **Not checked.** Whether Phases 0 and 4 of the runbook (`:197-449`, `:453-538`) are still a live path; chunk 7 must settle it before it deletes them.

### The Maintainer's part (unchanged from his words)

He confirms equalities, runs a few printed commands, reads a plain page, supplies the ceremony key, and gives a pro-forma yes. The steps that ask more are removed or handed to an agent: External sourcing, "exercise judgement" at the report (`REANCHOR_RUNBOOK.md:89-93`, `:157`; driver `:588`), reviewing verifier bytes and hand-hashing six modules (`:372-390`), the sterile acquisition command (`:203-225`), hand-run steps 2 to 4 and Phase 4 if live (`:392-436`, `:457-538`), `SECURITY.md:167` and `:234`.

### The local agent, and what it is trusted under

Two fresh-session agents, distinct from each other and from every author of the range: a **builder** (packet, launcher with its one slot filled) and a **reader** (reads the closure diff in full, runs the scanners, writes a committed record). Neither implemented the change.

* **C1 trusted machine** (a statement; the page prints host, user, checkout path; he answers).
* **C2 fresh and distinct sessions** (a statement; git cannot show it, since every agent commit carries his git identity; the record names sessions and models).
* **C3 record committed before signing and bound to bytes** (test: the record's packet, launcher and 12 member digests equal those in hand; a missing or older record refuses).
* **C4 the named list**, from the report tool: new executable files; added lines that start a process, touch the network or write a file; every change to the gate's own files; every scanner finding; non-zero counts explained in plain words.
* **C5 the instrument can fail**: each pattern and scanner is shown catching a planted bad line in a scratch copy before its "none" is believed; the record says which members only an agent read (the shell and Markdown ones).
* **C6 the key stays out of every agent** (the two-stage split and dedicated key, `SECURITY.md:148-231`, unchanged).

### The pro-forma page

Printed by the report tool during the ceremony. **He compares:** E1 the launcher digest printed equals the one in the committed record and in the reader's chat hand-off; E2 the commit id equals his `git rev-parse HEAD`; E3 the two package digests agree; E4 the key fingerprint equals `ssh-keygen -lf` of his key; E5 the two `SAME` commands print `SAME`. **He answers:** Y1 the record exists, is committed, and is by a session that is not an author; Y2 the gate-file changes listed are the ones the plan said this release makes; Y3 every C4 count is zero or explained; Y4 every scanner and the certifying run passed, or each failure is named in an earlier allowance; Y5 this is his own machine and the key is not loaded yet. **A yes means** the numbers match what he asked for and a fresh agent says in writing nothing dangerous was added; **not** that he audited code. A no stops everything. His yes is a typed act bound to the page he read (the plan picks the mechanism; one candidate is typing the page's digest into stage 2); a yes bound to no page is refused.

### Chunks, in order

Proposed paths:
* `scripts/closure_report.py`
* `bootstrap/tests/test_closure_report.py`

1. **Scanner coverage (code, small).** `scan_targets()` gains the 7 Python closure members, with a test that every Python closure member is scanned and a planted-line control. `security_check.py` is on the oracle's sensitive roster, so his authorization names it.
2. **The report tool (code, new).** `scripts/closure_report.py` with its tests in `bootstrap/tests/test_closure_report.py`, read-only, reading git objects only and never importing or running candidate code. It prints the C4 list and the page, with *decides* = the closure members and the files the ceremony imports, *pinned* = other frozen files (using the checker's own path classes, not a second definition), *other* = the rest; the added-line scan over a fixed pattern list; the executable-file list. **It becomes the twelfth closure member**, or nothing pins the tool that tells him what he is blessing: the template's `EXPECTED_PATHS`, the checker's declared closure and the three retyped lists (11 to 12) change, as the template's own addition did.
3. **One values reader (code, the launcher).** The launcher stays the only parser, as it must (it reads values before it can trust anything). It gains three modes (`validate`, `show-report`, `hash-package`) that verify and extract exactly as now, then run the artifact with the parsed values passed as fixed arguments; the artifact's own parser and the parity test are deleted, and `repin` and the report call the launcher modes. **Constraints:** the pre-candidate set of six executables (`bootstrap/SAFETY.md:654-700`) must not grow; no new grammar. **Falsifier:** if a mode needs a seventh executable or any parse beyond today's grammar, stop and keep two readers. This is my design, not a reviewed one; the Security Review attacks it. The driver's `values_field` (`:146`) stays; it reads fields without validating and says so.
4. **The launcher check by the tool (code, A2).** `repin ceremony` reads the template from the anchor's signed tree, fills the slot with the packet's digest and refuses unless the launcher in hand is byte-equal; its Summary 2 includes the page; the `:965` prompt text changes. It cannot act in the first ceremony (the anchor holds the old template), so E5 covers that one.
5. **Driver cleanup (code, deletions and fixes).** Delete `drive()` and `--run`, `scripts/correct_pinned_digests.py` (421 lines) and its test; fix `:163`, `:176`, `:743`. This lifts the earlier plan's fence on that edit (Q1) and its deletion-only check cannot hold (the print and the undefined name are not deletions), so the code review reads the whole driver diff instead.
6. **The evidence environment (code, reproduction first).** First a test that sets `PYTEST_ADDOPTS` to deselect tests, runs `gather_evidence` on a scratch tree, and shows the collected set shrinking while the exit status stays 0; if it does not reproduce, the chunk records that and stops. Then the fix: build the producer's environment from a short allowlist rather than subtracting two names (an unlisted variable then means absent, the safe side), and, if a committed pre-compiled file is shown to load, run with `-B` and refuse one in the raw tree. The reproduction also decides whether the second half of the report is real. It edits the checker, so it joins the single transition.
7. **Prose last.** The runbook to one page around the tool (D: roughly the launcher command, the page, the key, the push, and the first-ceremony authorization); template and artifact comments; `doctrine/dual-review.md:85-91`; `bootstrap/SAFETY.md:657-658`; `SECURITY.md:167`, `:234`, `:237`; the record format and where the record lives (the plan decides; not in the retired reviews folder). Deliberately untouched: `_gate_preflight.py` wording that says "external review" (`:1010`, `:2801`), unless a chunk already edits that file.

Then: one code review of chunks 1 to 7 together; **a Security Review that reads** the launcher in full, `reanchor.sh` in full, `closure_report.py` in full, the checker's changed hunks (including `gather_evidence`'s environment), `repin`'s A2 hunk, the driver diff, the `security_check.py` hunk, and the runbook page as the thing he is told to do; a certifying run; the builder and reader; then the ceremony. Chunks 1 to 6 are code; 7 is prose.

### The first ceremony: the bootstrap problem

No reviewed launcher built by the new process exists before the new process does, and the anchor still holds the old text and the old closure, so the first ceremony is a transition that no tool of the new design can run (`repin` refuses at boot; A2 has no anchored template). **How it is authorized:** his Decision on this proposal, quoted verbatim there, says the first ceremony runs under the new text before that text is anchored, with a builder and a reader as above, the record committed first, his only parts E1 to E5, Y1 to Y5 and the key, and the sensitive-roster entries named (`bootstrap/security_check.py` and `bootstrap/tests/_gate_manifest.py`). **What he does by hand, once:** the commands the launcher's stage 1 prints (launcher, show-report, hash-package, stage 2 with his digest), the `SAME` commands, `git verify-commit refs/cairn/gate-anchor`, and the push; nothing else. Then M2, M1, R6a and the cut's own re-anchor through `repin`, as `dev/PLANNING.md` lists.

### Items he asked about, with a recommendation each

* **I (checker messages the launcher does not print): superseded by the page; keep its trigger.** Default: yes.
* **E (stale-pin warning at session start): do not build.** It adds subprocess use to the interpreter trust root (`templates/skills/_lib/session.py`) and may touch session-routine doctrine; cheap ceremonies make the silence matter less. Default: no. Lost: staleness stays visible only on demand.
* **Unsigned anchor (`dev/PLANNING.md:440-448`): close it by this ceremony.** Stage 2 signs the new anchor, so `AGENTS.md`'s "signature on the commit it names" becomes true; no text edit. Default: yes. If stage 2 does not sign, the sentence is corrected instead.

### Assurance, honestly

**Still stopped:** accident; a careless or confused agent; a closure change slipping in unreported (the packet pins 12 digests; the launcher measures a transition, `template:570-612`); candidate code running while the key is loaded; a stale or wrongly signed anchor; any agent moving the anchor alone, because only his key can. **No longer stopped:** a malicious change from a compromised session or poisoned input that a same-vendor fresh agent and the pattern list both miss. The old design put an outside reader there. The key still decides whether the anchor moves; what he is told when he turns it is no longer cross-checked from outside. New here: the report tool is unanchored code at the first ceremony (read by two fresh agents, not signed), and the pattern list is by enumeration, so it ages.
**Signals this is wrong:** a planted bad line the report misses; a record digest and a printed one disagreeing without explanation; the launcher growing a seventh executable; a later outside read finding a dangerous change the reader passed; zeros from an instrument that could not match.

### Scope delta

**Scope delta**: degraded, one unit: the standing External reader is replaced by the fresh local reader. **disposition**: guard (it stays the Maintainer's call under `doctrine/dual-review.md`; only the standing requirement goes). Every outcome in his words and in the second brief is in. E is not built and I is superseded (recorded above, with defaults); each carries **disposition**: wontfix for E, accept for I.

**Assurance path**: `high-assurance`. **Review**: usual + Security Review. **Plan review**: required(Internal + Internal Security Review). **Status**: awaiting-review.

### Questions for the Maintainer

1. **Lift the plan's MAINTAINER-ONLY fence on the driver cleanup's edit** (agents write it; the ceremony stays yours)? Default: yes. If not: the cleanup waits for you to write it, and the old driver path stays through the first ceremony.
2. **Authorize the first ceremony under the new, not-yet-anchored text**, in your own words at the Decision, naming the two sensitive-roster entries? Default: yes. If not: there is no way to run the first transition.
3. **Make the report tool a twelfth closure member?** Default: yes. If not: it is unpinned and a later edit could change what the page says.
4. **Build the one-reader launcher change (chunk 3) in this batch?** Default: yes, with its falsifier. If not: two readers and a parity test remain, and the Security Review has a smaller launcher to read.
5. **Build the session-start stale-pin warning (E)?** Default: no.
6. **Is a same-vendor fresh reader acceptable as the standing reader, with the record stating that plainly?** Default: yes. If you want a different model as reader, we gain a little distance and lose the ability to run a ceremony on a day that model is unavailable.

### Withdrawn / superseded commitments

* The interim route (a), and options (b) to (d) as written: withdrawn by the Maintainer's words above; everything is built now.
* "No runbook, launcher or doctrine text changes first": superseded; the text and closure members change first so one transition pins them.
* "Template `EXPECTED_PATHS` untouched": superseded; it gains the report tool.
* The deferral of D, C and I; the report verb "after the cut": superseded; D and C are in, I is superseded by the page.
* "Rewrite as a later transition" and the options table: superseded by the chunks above.
