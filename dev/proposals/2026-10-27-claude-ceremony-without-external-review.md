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
