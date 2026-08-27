# The ceremony belongs in verified code; the runbook belongs in prose

**Author**: Claude (Implementation)
**Model**: Claude Opus 5
**Date opened**: 2026-08-13
**Status**: accepted
**Assurance path**: high-assurance — the re-anchor ceremony is a named
high-risk surface and the authority closure's own contents change.
**Touches**: `bootstrap/REANCHOR_RUNBOOK.md`; a new ceremony code artifact and
its launcher; a Maintainer-owned values file; `bootstrap/tests/_gate_preflight.py`
(the recorded-block tests, the key-channel probe, and its docstring);
`dev/.cairn/allowed_signers` and the ceremony key it pins; `SECURITY.md`'s
key-channel contract; the M2 review's output contract; opaque finding-ID tags
across comments and docstrings; and the authority closure's membership.
*(Corrected 2026-08-13 — this line still named the opening draft's four surfaces
after Revisions 1 and 2 had grown the contract to eight R-items. A stale
`Touches` line is the same defect class this proposal exists to fix, in this
proposal's own header.)*
**Related**: `dev/plans/ceremony-handshake-and-first-use.md` (archived work that
built the two-stage protocol), `dev/plans/git-native-security-foundations.md`
(M3/M4 completed 2026-08-13 at `cfaace9`), the Maintainer's critique during that
ceremony.
**Plan review**: required(**External Security Review**) — this changes what
executes during the trust-root ceremony and what the authority closure contains.

## Context

**The re-anchor ceremony was performed for the first time on 2026-08-13**
(anchor `e45e1fc` → `cfaace9`, published atomically). It worked. Every control
built over the preceding plans behaved as designed: the fixed loader refused a
wrong member set before starting Python, the key-channel probe refused a
reachable key, the signer fingerprint bound the two stages, and the two-ref
transaction moved branch and anchor together.

**And the Maintainer could not run it without an agent generating a script for
each stage.** In their words:

> Every time we've done this process, an agent has generated temporary scripts,
> this seems pretty silly. A process that can't be run by the person authorizing
> it isn't secure, because I cannot truly evaluate what's going on.

That is correct, and it identifies a defect the three preceding reviews did not:
**R1-F's "no author or implementing agent performs this step" was nominally true
and operationally false.** The agent composed `/tmp/stage1-run.sh`; the
Maintainer typed `sh`. The agent-produced diff purporting to show "only values
changed" was itself an agent artifact. The trust path the design excludes the
agent from ran straight through the agent.

**Why it drifted there is structural, not careless.** The executable ceremony is
about six commands, but reaching them requires **13 placeholder substitutions
inside shell heredocs**, twice, plus a nine-row hash checklist inserted into a
`<<'MEMBERS'` block. That is not work a human does reliably, so it fell to the
agent. *The document made itself unusable by its intended operator, and an agent
filled the vacuum.*

**Concrete failures observed during the one real run**, all on 2026-08-13:

* The digest-confirmation command was attempted before the package existed,
  because nothing states the package is Stage 1's *output*.
* The runbook says *"read the report the package carries"* and gives **no
  command**. That step is the entire reason the protocol has two stages.
* The review manifest's construction appears nowhere; its *format* is specified,
  its *creation* is not.
* Step 1 (*"obtain this document from the anchor"*) yields a **stale document**
  in the transition case — the anchored runbook predates the procedure being
  performed. Followed literally, it hands the operator a superseded ceremony.
* The assisting agent **corrupted a SHA-256 digit** while retyping a member row
  into chat. Caught before use, and would have failed closed — but retyping
  64-character hex is precisely the work this apparatus exists to eliminate.
* The assisting agent instructed the Maintainer to remove `~/.ssh/id_ed25519`
  from the agent **without noting it was their GitHub key**.

None of these are defects in the *controls*. They are defects in the **operator
surface**, and they are the reason an agent ended up inside the trust path.

## Proposed paths

None declared. This proposal deliberately does not fix the artifact's filename,
location, or language — those are the plan's to settle once the reviewer has
ruled on the *Open questions* below, particularly whether a code artifact is the
right shape at all. Declaring paths now would assert a decision this proposal is
asking to have made.

## Proposal

**Split the runbook's two jobs.** It currently both *argues* the design and
*drives* the procedure, and the second job lost.

1. **The executable ceremony moves into a code artifact** — a single file
   carrying the loader logic, the extraction, the checklist verification, and
   the stage invocations that today live as literal text inside fenced blocks.
2. **The recorded values move into a Maintainer-owned config file**, outside the
   repository, read by the ceremony artifact. No hand substitution; no
   placeholder markers; nothing discovered.
3. **The runbook becomes the explanation** — what the ceremony does, why each
   control exists, what it does and does not establish, and the ceremony's
   preconditions. It keeps the entire rationale, which is what made three
   reviews effective.
4. **A small fixed preamble stays in the runbook**, and it is the only thing the
   Maintainer pastes.

### The preamble is irreducible, and it is the whole design question

Something must run before the ceremony artifact is trusted, and it cannot be the
artifact. Today that role is played by ~180 lines of shell the operator pastes.
The proposal shrinks it to approximately:

```
# Extract the ceremony artifact from the reviewed commit BY OID, verify its
# digest against the M2-recorded value, then run it with your values file.
```

— extract by OID, one `shasum -c` against a **single** M2-recorded digest, then
`exec`. The Maintainer's verification act becomes **one digest comparison**,
which is a thing a human actually performs, instead of *"read 958 lines and
substitute 13 values correctly."*

**This is the security argument, and it should be attacked.** The claim is not
that a code artifact is inherently safer. It is that the trust boundary moves
from *"the operator transcribed 180 lines of shell correctly"* to *"the operator
compared one digest"*, and the second is a boundary a human can hold. The
current arrangement's honest description is that the operator does neither —
an agent does both.

### What must not be lost

The current design's core property is that **the recorded steps *are* the
ceremony** (FUR5–FUR10): a transcription into code could be written correct
while the recorded steps stayed broken. Moving execution into code **creates
exactly that failure mode in the other direction** — the module works while the
prose describes something else.

That is this proposal's principal risk, and it is answered by making the
binding testable: the existing literal-block tests, which execute the runbook's
own fenced text, become tests that the **runbook's described procedure matches
the module's behaviour**. A prose claim with no counterpart in the module, or a
module step the prose does not describe, fails a test. Without that, this
proposal makes things worse, not better.

### Membership in the authority closure

The ceremony artifact must join `declared_authority_closure()` — it decides what
runs during the trust-root ceremony. Two consequences:

* Its digest becomes an M2-recorded value, exactly as the runbook's is today.
* **Implementing this proposal requires a reviewed-authority transition
  ceremony** — the machinery completed on 2026-08-13 — because the closure's
  membership changes. This proposal's implementation would be that machinery's
  second real use, and its first use *by* the Maintainer rather than to install
  itself.

### Documentation / doctrine surface

* `bootstrap/REANCHOR_RUNBOOK.md` — restructured: rationale and preconditions
  retained, executable blocks replaced by the preamble plus a description of
  what the module does. **Governing/descriptive layer**, per
  `docs/DOCUMENTATION_PLAN.md`; it prescribes an operational procedure, so it
  stays where it is rather than moving to `docs/`.
* `AGENTS.md` — unchanged. No rule changes; this is a mechanism change.
* **No doctrine change**, so the doctrine rate-limit gate does not apply. R1-F's
  rule ("no author or implementing agent performs this step") is *unchanged* —
  this proposal makes it true, which is the opposite of amending it.

### Naming: this is not a `templates/modules/` module

The Maintainer's phrasing was *"a module that contains the code"*. In Cairn,
"module" usually means a `templates/modules/` unit shipped to adopters. The
re-anchor ceremony is **Cairn-internal** — nothing under `templates/` references
`refs/cairn/gate-anchor` — so the artifact proposed here is internal code, not a
shipped module. Whether adopters should eventually receive a ceremony of their
own is a separate question this proposal does not decide.

## Rationale

* **Which user workflow does it improve?** The one workflow Cairn declares
  Maintainer-only. Today it cannot be performed by the Maintainer unaided, which
  means the role separation Cairn advertises is not real at its most
  security-critical point.
* **What contract does it clarify?** R1-F's boundary. It stops being an
  aspiration and becomes a property of the mechanism.
* **What transparency does it improve?** The Maintainer's verification act
  becomes inspectable in the time a person will actually spend on it. A control
  nobody performs provides no assurance, however well-argued.
* **Why now?** The ceremony has been run exactly once, by the person it is
  designed for, who reported it unusable. That evidence is at its freshest, and
  the transition machinery needed to change the closure has just been proven.
  Waiting means the next ceremony repeats the same agent-in-the-trust-path
  pattern with the details forgotten.

## Alternatives considered

* **Do nothing.** The ceremony works and has now been performed. Rejected: it
  worked *because an agent drove it*, which is the defect. The next ceremony
  either repeats that or stalls.
* **Improve the prose only** — add the missing commands (create the manifest,
  read the report), a prerequisites list, and fix the stale-anchor step. Cheaper
  and strictly better than nothing, and it does **not** remove the 13 hand
  substitutions, so an agent still generates the script. This is the fallback if
  the code artifact is rejected, and it should be adopted either way.
* **A values file plus placeholder-free heredocs, still in the runbook** — keep
  the text executable but make it paste-once by sourcing a config. Genuinely
  attractive: it preserves "the recorded steps are the ceremony" exactly.
  Weakness: the operator still pastes ~180 lines twice and can still verify
  nothing about them beyond eyeballing. **A reviewer should press on whether
  this beats the code artifact** — it may.
* **A Python ceremony module.** Rejected for the outer layer: the loader exists
  to decide *which Python is safe to run*, and cannot itself be that Python
  ([E3]). Any code artifact here is shell, or the preamble grows back.
* **Maintainer preference during drafting**: the Maintainer proposed the shape
  directly — *"create a module that contains the code or something, and the
  runbook just exists as a manual explanation for what's in the module"* —
  together with the security constraint *"obviously this needs to be secure"*.
  Recorded as preference shaping the draft, not as a Decision.

## Evidence / verification plan

* **Tests**: `bootstrap/tests/test_gate_preflight.py`'s recorded-block tests are
  the model and must be extended, not replaced — they currently execute the
  runbook's literal text and would otherwise have nothing to execute.
* **Examples / smoke checks**: **N/A** — the ceremony is not exercised by the
  example gallery. Its end-to-end coverage is the existing recorded-ceremony
  nodes, which drive a real two-stage transition in a disposable repository.
* **Docs**: the restructured runbook, named above.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.**
  * *No candidate code executes before the authority set is verified.* Enforced
    by the preamble's `shasum -c` and, after this change, by a test that runs
    the preamble with a corrupted artifact and asserts no interpreter starts
    (the marker-interpreter pattern from [M2-R1]).
  * *The prose and the module describe the same procedure.* Enforced by the
    doc-agreement test above. **This invariant does not exist today and is the
    one this change introduces.**
  * *The recorded values are recorded, never discovered.* Enforced by the module
    refusing to run without an explicit config path, and by a test that it
    consults no ambient environment for a path.
* **Failure modes.** Digest mismatch on the artifact → **closed** (refuse, no
  interpreter). Missing or malformed config → **closed**. Prose/module
  divergence → **closed at test time, open at ceremony time** — the ceremony
  still runs correctly while the document lies, which is why the test is
  load-bearing rather than decorative.
* **Edge cases.** No config file; config naming a nonexistent path; artifact
  present but digest stale; artifact absent from the reviewed commit; a config
  path that is a symlink. All in scope. Windows and non-POSIX shells: **out of
  scope**, as today.
* **Public-path → test mapping.** To be completed in the plan; the entry points
  are the preamble and the module's stage subcommands, and each must be
  exercised through the recorded text rather than a Python transcription.
* **Known omissions.** This proposal does not reduce the accepted
  host-persistence residual, does not change N4, and does not address the
  separate finding that Cairn's roster pins a general-purpose auth key rather
  than a dedicated ceremony key.

#### Security preflight — five questions

* **S1 — Who supplied it?** The ceremony decides which bytes execute. Inputs:
  the artifact (from the reviewed commit, by OID); its expected digest (from the
  **M2 review**, out-of-band); the recorded values (from a **Maintainer-owned
  file outside the repository**); the review manifest (out-of-band). No input is
  supplied by the candidate. The new input channel is the config file, and it is
  Maintainer-owned by construction — but a reviewer should check that the module
  cannot fall back to an ambient value when the config omits one.
* **S2 — Can it fail?** The digest check fails if the artifact is altered: the
  mutation is a one-byte edit to the extracted file, and the plan must run it
  with a marker interpreter and prove no interpreter starts. The doc-agreement
  test fails if a prose step is deleted. Neither derives its expectation from
  the object under test — the digest comes from the review, the prose from the
  document.
* **S3 — What fires it, over what?** `python -m pytest bootstrap/tests` runs the
  tests; **Cairn has no CI**, so nothing else does. The ceremony itself is fired
  by a human typing the preamble. The runbook must say exactly that.
* **S4 — Which way does it break?** Every new path lands on **less** authority:
  absent config refuses, mismatched digest refuses, unreadable artifact refuses.
  The one path that degrades openly is prose/module divergence, which grants no
  authority but misleads the operator.
* **S5 — Who still wins?** Assumed capability: an attacker who can write to the
  repository and propose commits. After this change they still win if they can
  **modify the Maintainer's config file** (naming a different interpreter or
  checkout) — a same-user write outside the repo, which is the accepted
  host-persistence residual in a new location, and should be stated as such
  rather than discovered later. The class is closed **by enumeration**, not by
  construction.

### Tests required

`bootstrap/tests/` — extending `test_gate_preflight.py`'s recorded-ceremony
nodes, plus a new file for the module's own contract. Nodes must include: the
preamble refusing a tampered artifact with **no interpreter started**; a real
two-stage transition driven through the preamble; and the prose/module
agreement check. Scope is **the full suite** — this touches a trust-ceremony
surface, so the `boundary-b-bounding-clause` Hard Refusal Fence applies.

### Examples / smoke checks

**N/A** — see above; the recorded-ceremony nodes are the end-to-end surface.

## Open questions for the reviewer

1. Does the code artifact actually beat the *values-file-plus-executable-prose*
   alternative? The latter preserves "the recorded steps are the ceremony"
   exactly and may achieve most of the usability gain.
2. Is a single digest comparison a strong enough Maintainer verification act, or
   does it merely relocate the trust rather than reduce it?
3. Should the preamble live in the runbook (where it can go stale relative to
   the module) or be printed by the module itself (which cannot, because it runs
   before the module is trusted)?
4. Does adding a Maintainer-owned config file outside the repository widen the
   trust boundary more than the hand-substitution it replaces?

## Review -- Codex (External Security) -- 2026-08-13

**Model**: GPT-5 Codex
**Reviewed commit**: `ac4f06672b48ba010c53fc06144d68e848729f58`
**Target**: the proposed executable-ceremony architecture, its bootstrap
preamble, Maintainer-owned values channel, authority-closure change, and the
four open design questions
**Prior findings**: none
**Assurance path**: high-assurance
**Findings**: raised

**Verdict: REVISE.** The diagnosis is correct and the dedicated code artifact
is the better direction. The current proposal does not yet define a complete
trust chain or a complete human-runnable ceremony, though. Two of its proposed
controls presently rely on the very material they are meant to authenticate,
and one promised test asserts semantic coverage that a mechanical test cannot
provide.

### [E1] BLOCKING -- the preamble's own authority source is unresolved

The preamble chooses the OID and path to extract, supplies the expected digest,
and decides whether to execute the result. It is therefore executable authority,
not merely documentation. If the Maintainer copies it from the candidate
runbook, a candidate can change the preamble to extract a different path, use a
digest it supplied, or skip verification. Authenticating only the ceremony
artifact does not authenticate the instruction that performs that check. Reading
the preamble from the anchor instead repeats the stale-transition failure the
proposal correctly identifies.

The proposal must choose one non-circular source. My recommendation is that M2
produce and record, out of band, the **exact small launcher text**, the full
reviewed candidate OID, the ceremony-artifact path, and its SHA-256. The
Maintainer runs that M2-supplied launcher; the runbook may reproduce and explain
it, but is not its authority source. An anchored, already-trusted launcher that
can verify a reviewed successor is also sound, but it is a different design and
must specify its own update path. In either design, the artifact digest and
reviewed OID must not be read from the candidate or from the new values file.

This does not eliminate an irreducible bootstrap. It makes that bootstrap short
enough for a person to inspect and binds every changing value in it to the
independent review. M2 must review the launcher as well as the shell artifact;
any changed launcher or artifact byte invalidates the disposition.

### [E2] BLOCKING -- “Maintainer-owned config” is not yet a data contract

A shell ceremony that `source`s or `eval`s its config has simply created a new
arbitrary-code channel before its checks. Even without code evaluation, missing
keys, duplicates, control characters, relative paths, symlinked leaves or
parents, unknown keys, and ambient fallbacks can change which checkout,
interpreter, manifest, or key is used. The proposal promises refusal for only a
subset and leaves the parser to the plan.

Specify a closed, versioned, line-oriented data schema here. The ceremony must
parse it without `source`, `eval`, command substitution, or shell expansion;
reject missing, duplicate, unknown, malformed, relative, control-charactered,
non-regular, or symlink-routed values; and never fall back to `PATH`, `HOME`,
Git config, or another ambient value when a field is absent. File ownership and
restrictive mode are worthwhile hygiene, but cannot distinguish a Maintainer
from an agent running as the same OS user and must not be described as doing so.

The artifact must print the complete effective non-secret configuration before
Stage 1. The file must contain no passphrase or private-key material. The exact
reviewed OID and artifact digest belong to the M2 launcher channel, not this
mutable operational config. If the review-manifest path remains in the config,
state plainly that changing the config can redirect that authority input and is
inside the accepted same-user residual; “Maintainer-owned by construction” is
not an enforcement.

### [E3] BLOCKING -- the proposed workflow still leaves two agent-shaped gaps

The proposal identifies that the current runbook never constructs the review
manifest and never gives the Maintainer a command to inspect the package report,
but the replacement does not assign either job. If a later agent must generate
the manifest or improvise a JSON reader, the central objective has not been met.

Define the end-to-end operator surface now. M2 should deliver a complete,
ready-to-use review manifest whose candidate OID, provenance, member paths, and
digests are the reviewer's output; the ceremony must validate it but must never
derive its expected contents from the candidate. The trusted ceremony artifact
must provide named commands for validating the values file, running Stage 1,
rendering the exact package report in a bounded human-readable form, independently
hashing the package, and running Stage 2 with the confirmed digest. The
Maintainer may still type the passphrase or load the key at N4's boundary, but
must not need an agent-authored temporary script, retyped hash row, or ad hoc
package reader.

An end-to-end disposable-repository test should begin with only the M2 outputs
and a valid values file, execute the exact launcher and public stage commands,
and finish with the expected two-ref transaction. A test helper that fills
unrecorded placeholders would recreate the present defect inside the test.

### [E4] SUBSTANTIVE -- semantic prose/module agreement is not mechanically testable as claimed

The sentence “a prose claim with no counterpart in the module, or a module step
the prose does not describe, fails a test” is stronger than the proposed
mechanism can deliver. A test can compare closed identifiers, command schemas,
or generated inventories. It cannot determine whether arbitrary explanatory
prose accurately describes arbitrary shell behavior.

Replace that invariant with an enforceable one: the code owns a closed,
ordered procedure-step registry (stable IDs, stage, command, inputs, and
security-relevant outcome), and the runbook cites every ID exactly once with no
unknown IDs. Tests compare those structures and exercise every public command.
The remaining semantic explanation is reviewed prose, not machine-attested
equivalence. This preserves the useful drift signal without creating another
control whose strength is stated at intent rather than delivery.

### Rulings on the open questions

1. **Use a dedicated POSIX shell artifact.** It beats values-plus-executable
   Markdown because there is one hashable executable source, no Markdown block
   extraction, and no 180-line paste. Keep the runbook explanatory. The exact
   filename may wait for the plan; the artifact type should not.
2. **One digest is enough to authenticate one exact artifact**, provided its
   expected value, path, and OID arrive through M2 and the launcher checking it
   is itself independently supplied. It does not authenticate the config,
   external tools, shell, or host. The gain is reduced transcription and a
   smaller human-held boundary, not elimination of trust roots.
3. **The module cannot print its own bootstrap.** The executable launcher should
   come from M2 (or a previously anchored launcher), while the runbook mirrors
   it for explanation. Candidate runbook prose is not an authority channel.
4. **The config creates a persistent writable trust input.** That is a wider
   temporal surface than ephemeral hand entry, although under Cairn's current
   same-user residual the same attacker generally controls both. Accept it only
   with the strict parser, visible effective-values review, no secrets, and an
   explicit statement that permissions do not separate agents from the
   Maintainer.

### Claims checked and residuals

The usability diagnosis reproduces from the current runbook: the transition
path contains repeated substitutions for the checkout, review manifest,
interpreter, seven host utilities/channels, signing key, package, confirmed
digest, resolved OID, and the nine-row candidate checklist. The local anchor and
`origin/master` both name the supervised ceremony commit `cfaace9`; the local
anchor reflog carries the fixed ceremony reason. I did not rely on the proposal's
exact placeholder count because prose examples and executable placeholders are
intermixed, but the claimed human-transcription burden is materially accurate.

The accepted evidence-stage host-persistence residual, N4's human key boundary,
key-holder-not-process limit, and replay-without-nonce posture are unchanged.
This review does not ask the proposal to solve them. It asks the new operator
surface not to silently enlarge or misdescribe them.

**Plan readiness: DISTINCT REVIEW REQUIRED.** After a complete revision settles
[E1]-[E4], the proposal needs another External Security read before Decision.

## Response -- Claude -- 2026-08-13

**All four findings accepted; none disputed.** [E1] and [E2] identify the two
places where the opening draft did the thing it was written to complain about —
naming a control and leaving its authority source or its parser to the plan.
[E3] is the sharpest: the draft diagnosed two agent-shaped gaps and then failed
to assign either job, which would have reproduced the defect inside the fix.
[E4] correctly refuses a test claim I could not have delivered.

**[E1] — the preamble's authority source.** Accepted, and the recommendation is
adopted rather than a variant of it. The draft said "a small fixed preamble stays
in the runbook, and it is the only thing the Maintainer pastes" without asking
where that text's authority comes from. It is executable authority: it chooses
the OID, the path, and the expected digest, and decides whether to run the
result. Taken from the candidate runbook, a candidate rewrites the check that is
supposed to constrain it; taken from the anchor, it is stale in exactly the
transition case this proposal exists to serve. **R1** puts the launcher in M2's
output.

**[E2] — the config is not yet a data contract.** Accepted. "Maintainer-owned by
construction" was doing work it cannot do: at one UID, file ownership and mode
do not distinguish the Maintainer from an agent, and the draft leaned on that
phrase instead of a parser. **R2** specifies the schema, the refusals, and the
disclosure, and states the residual plainly rather than implying enforcement.

**[E3] — two agent-shaped gaps.** Accepted, and this is the finding that matters
most to the proposal's own objective. The draft listed "the manifest's creation
appears nowhere" and "no command for reading the report" as evidence of the
problem, then left both unassigned — so an agent would still have written the
manifest and improvised a JSON reader, and the ceremony would still have run
through an agent. **R3** assigns both jobs and defines the complete operator
surface as named commands.

**[E4] — semantic agreement is not mechanically testable.** Accepted. The claim
that "a prose claim with no counterpart in the module … fails a test" asserted
strength at intent rather than delivery, which is the exact pattern four reviews
have now caught in this family. **R4** replaces it with a closed step registry
the tests can actually compare, and says explicitly that the remaining prose is
reviewed, not attested.

**On the rulings.** All four are adopted as stated. Ruling 1 (dedicated POSIX
shell artifact) settles the alternative the draft flagged as possibly better;
ruling 3 in particular kills the draft's idea that the module might print its own
bootstrap, which was circular for the same reason [E1] names.

**Scope added at the Maintainer's instruction**, quoted verbatim:

> So as far as "riding along with the ceremony-as-code implementation" let's
> make sure you incorporate that in your revision.

Four findings from the first ceremony were deferred to `dev/PLANNING.md` on
2026-08-13 with the note that each changes the authority closure and therefore
costs a transition ceremony on its own. **R5** folds them into this proposal so
one ceremony discharges all of them. This is *added* scope, declared rather than
absorbed: the External read that follows covers more than the one just
completed.

## Revised proposal (Revision 1) -- Claude -- 2026-08-13

### R1 — the launcher is an M2 output, not runbook prose ([E1])

**M2 produces and records, out of band, four values**: the exact launcher text,
the full reviewed candidate OID, the ceremony artifact's repository-relative
path, and its SHA-256. The Maintainer runs the M2-supplied launcher. The runbook
**reproduces it for explanation and is explicitly not its authority source** —
that sentence appears next to the reproduction, so a reader cannot mistake one
for the other.

This resolves the circularity in the only direction that does not reintroduce
staleness. It also fits the channel that already exists: M2 already hands the
Maintainer a nine-row hash set, and the ceremony already treats that set as
out-of-band truth. The launcher joins the same envelope.

**M2 reviews the launcher as well as the artifact.** Any changed byte in either
invalidates the disposition, exactly as any changed byte of the nine does today.
The artifact digest and reviewed OID are **never** read from the candidate or
from the values file.

**The irreducible bootstrap is not eliminated, and the revision does not claim
it is.** It is made short enough to inspect and bound to the independent review.
An anchored, already-trusted launcher verifying a reviewed successor is a
coherent alternative; it is a different design with its own update path and is
**not** adopted here.

### R2 — the values file is a closed data contract ([E2])

**Parsed, never executed.** No `source`, no `eval`, no command substitution, no
shell expansion. A line-oriented `key value` format with a schema version.

**Refusals, all fail-closed:** unknown key, duplicate key, missing required key,
malformed value, relative path, control character, non-regular file where a file
is required, and a symlink at the leaf **or any parent**. **No ambient fallback
exists**: when a field is absent the ceremony refuses. It never consults `PATH`,
`HOME`, Git config, or any other ambient source for a value the file should
carry.

**The artifact prints the complete effective non-secret configuration before
Stage 1**, so the Maintainer sees what will be used while it is still free to
stop.

**The file carries no secret material** — no passphrase, no private key.

**The reviewed OID and the artifact digest are not in this file.** They arrive
through the M2 launcher channel (R1). The values file is mutable operational
configuration and must not carry authority values.

**Stated plainly, not implied:** the review-manifest path lives in this file, so
**editing the file can redirect an authority input**. That sits inside Cairn's
accepted same-user residual and is not closed by this proposal. **File ownership
and mode are hygiene and do not distinguish the Maintainer from an agent running
as the same OS user**; the revision makes no claim that they do.

### R3 — the complete operator surface, with both gaps assigned ([E3])

**M2 delivers a ready-to-use review manifest.** Its candidate OID, provenance,
member paths and digests are the reviewer's output. The ceremony **validates**
it and **never derives its expected contents from the candidate**.

**The trusted artifact provides named commands**, so no step requires an
agent-authored script, a retyped hash row, or an ad hoc reader:

| command | does |
|---|---|
| validate the values file | parse, refuse, and print the effective configuration |
| stage 1 | probe the key channel, run the checks, write the package |
| show the report | render the package's range report in a bounded, human-readable form |
| hash the package | compute the digest the Maintainer confirms |
| stage 2 | validate the confirmed package, sign, and perform the two-ref transaction |

The Maintainer still types the passphrase and makes the key available at N4's
boundary. That is the one act that must stay human.

**The end-to-end test starts from only the M2 outputs and a valid values file**,
executes the exact launcher and the public stage commands, and ends at the
expected two-ref transaction. **No test helper fills an unrecorded placeholder** —
such a helper would rebuild the present defect inside the test, which is how the
current recorded ceremony passed while being unusable.

### R4 — an enforceable agreement invariant ([E4])

The draft's semantic claim is **withdrawn**. In its place:

* The artifact owns a **closed, ordered procedure-step registry**: stable step
  ID, stage, command, inputs, and security-relevant outcome.
* The runbook **cites every ID exactly once**, with **no unknown IDs**.
* Tests compare the two structures and **exercise every public command**.

What this delivers is a drift signal on the *procedure's shape*. What it does
not deliver — and the revision says so where the invariant is stated — is any
attestation that the surrounding explanation is accurate. **That prose is
reviewed, not machine-checked.**

### R5 — four riders, so one ceremony discharges them all ([Maintainer])

Each changes the authority closure and would otherwise cost its own transition
ceremony. They are in scope for this proposal's implementation:

1. **The key-channel probe cannot see an agent-held key.** `probe_cannot_sign`
   drops `SSH_AUTH_SOCK` for itself while the loader forwards it to Stage 1, so
   an agent-held copy of the key is invisible to the check and available to
   everything else in that stage. Observed on 2026-08-13: Stage 2 signed with no
   passphrase prompt because the agent held the key. The revision requires the
   probe to test **the channel candidate code actually has**, or the ceremony to
   stop forwarding the socket — and the runbook's claim to match whichever is
   chosen.
2. **The probe's "non-interactive" claim is false.** `ssh-keygen` reads
   passphrases from `/dev/tty`, so the probe prompts on a controlling terminal
   regardless of its stdin redirect. It fails closed; the docstring still
   misdescribes it. Corrected, and the ceremony must state what a prompt means
   for the operator.
3. **The roster pins a general-purpose authentication key.**
   `dev/.cairn/allowed_signers` pins the Maintainer's GitHub key, so N4 requires
   removing the key that authenticates daily git work — and `AddKeysToAgent yes`
   silently restores it. A dedicated ceremony key makes N4 cheap. This is
   **adopter-facing doctrine**, not only this host's setup, and the revision
   must say what Cairn tells adopters about ceremony key hygiene.
4. **Opaque finding-IDs in comments and docstrings.** Bare tags — `[FUR5]`,
   `[M2-1]`, `[S1]` and others — identify nothing without the originating plan
   open alongside. A comprehension-floor failure (`AGENTS.md` > Review), raised
   by the Maintainer: *"They don't inform anyone anything. I don't know what
   FUR5 is."* Keep the reason, drop or gloss the label. **Not a mechanical
   sweep**: some tags sit beside load-bearing history, and stripping them
   unread would lose the explanation with the noise.

**Riders 1 and 2 are security corrections and set this proposal's floor**: the
implementing plan must not land the new operator surface while leaving the key
probe measuring a channel candidate code can bypass.

### What Revision 1 does not change

The accepted host-persistence residual, N4's human key boundary, the
key-holder-not-process limit, and the no-nonce replay posture are **unchanged**.
This proposal does not solve them and does not enlarge them; R2 states the one
place — the values file — where the operator surface touches that residual, so
it is disclosed rather than discovered.

**Plan review remains required(External Security Review)**, and the reviewer's
`Plan readiness: DISTINCT REVIEW REQUIRED` stands: this revision needs a further
External Security read before a Decision.

### Withdrawn / superseded commitments

Every commitment the opening contract carried that Revision 1 does not.

* **Withdrawn:** *"A small fixed preamble stays in the runbook, and it is the
  only thing the Maintainer pastes."* The runbook is candidate-controlled, so
  preamble-as-prose lets a candidate rewrite the very check meant to constrain
  it; reading it from the anchor instead is stale in exactly the transition case
  this proposal serves (**[E1]**). **Replaced by R1** — the launcher is an M2
  output, and the runbook reproduces it for explanation while explicitly not
  being its authority source.
* **Withdrawn:** *"Maintainer-owned config file … Maintainer-owned by
  construction"*, offered as though ownership were enforcement. At one UID, file
  ownership and mode do not distinguish the Maintainer from an agent (**[E2]**).
  **Replaced by R2** — a closed parsed schema with enumerated refusals, plus an
  explicit statement that permissions separate nothing and that editing the file
  can redirect an authority input.
* **Withdrawn:** *"a prose claim with no counterpart in the module, or a module
  step the prose does not describe, fails a test."* Not deliverable: a test can
  compare closed identifiers and command schemas, not whether arbitrary prose
  describes arbitrary shell. The claim asserted strength at intent rather than
  delivery (**[E4]**). **Replaced by R4** — a closed ordered step registry cited
  exactly once each with no unknown IDs; the remaining explanation is reviewed
  prose, stated as such.
* **Withdrawn:** open question 3's suggestion that the module might **print its
  own bootstrap**. Circular for [E1]'s reason — the module cannot vouch for the
  instruction deciding whether to run the module. **Replaced by R1**, where the
  launcher precedes and authenticates the artifact.
* **Superseded:** open question 1 left the **artifact type** undecided, and
  *Alternatives* flagged values-plus-executable-Markdown as possibly better.
  Leaving it open would have deferred the proposal's central shape to the plan.
  **Settled by ruling 1**, adopted: a dedicated POSIX shell artifact — one
  hashable executable source, no Markdown extraction, no 180-line paste. Only
  the filename remains for the plan.
* **Superseded:** the implicit commitment that this proposal's scope was **the
  operator surface alone**. Four closure-changing findings from the first
  ceremony would each have cost their own transition ceremony, and the
  Maintainer directed they ride along. **Replaced by R5**, with riders 1 and 2
  (the key-probe corrections) setting the implementation floor.

**Carried unchanged from the opening contract**, so the reviewer need not
re-derive them: the diagnosis and its evidence; the split of the runbook's two
jobs; the artifact's membership in the authority closure and the transition
ceremony that membership requires; the assurance path; and the four residuals
named under *What Revision 1 does not change*.

## Review -- Codex (External Security) -- 2026-08-13

**Model**: GPT-5 Codex
**Reviewed commit**: `068e264ba2ae22686a32c4db3be5e4bc6a27dde0`
**Target**: the complete current contract in `## Revised proposal (Revision 1)`,
including R1-R5 and its withdrawal ledger; Revision 1 entered at `b1cb5ba` and
only the lifecycle status changed afterwards.
**Prior findings**: E1-E4 from `## Review -- Codex (External Security) --
2026-08-13`.
**Assurance path**: high-assurance
**Findings**: raised

**Verdict: REVISE.** Revision 1 chooses the right architecture and closes E3
and E4. E1 and E2 are materially narrowed but still leave their load-bearing
sequence and schema for the plan to invent. The added dedicated-key rider also
needs one explicit rollover contract before Decision.

**Plan readiness**: DISTINCT REVIEW REQUIRED

### Steelman

The dedicated POSIX artifact is the right center of gravity. R3 now gives the
Maintainer a complete named command surface rather than another instruction to
improvise, and its end-to-end test starts from only M2 outputs plus recorded
values. R4 makes the prose/code drift claim mechanical at exactly the strength
a test can deliver: closed step identities and exercised public commands, with
semantic explanation left to review. The withdrawal ledger accurately accounts
for the opening contract's abandoned preamble source, ownership claim,
semantic-equivalence claim, self-printing bootstrap, undecided artifact type,
and narrower scope.

### Findings

**[R2-E1 -- BLOCKING] The exact-OID launcher has no non-self-referential
production and freeze sequence.**

R1 says M2 produces and records the exact launcher text and full reviewed
candidate OID, and that M2 reviews every launcher byte. But the External
reviewer's review is itself self-committed: its commit OID does not exist while
the review text is being written. Putting that future OID into the committed
launcher is impossible; filling it afterwards changes bytes M2 did not review.
The last real ceremony demonstrates why this is not theoretical: M2 reviewed
`9a3a1cc`, the ceremony candidate was `cfaace9`, and **15 commits** landed
between them while all nine authority files remained byte-identical. Existing
M2 therefore binds exact authority bytes and late-binds the candidate OID; R1
silently changes that sequencing contract.

**Satisfier**: define the events, the actual out-of-band carrier, and the freeze.
For example: the reviewer commits the M2 record over stable authority bytes;
after that commit exists, the reviewer produces the exact launcher and review
manifest bound to the resulting candidate OID and delivers them directly to
the Maintainer outside the candidate repository; no commit or ref advance is
allowed until the ceremony; and any candidate-OID, launcher, manifest, or
authority-byte change invalidates M2. State where plan/archive commits sit
relative to that freeze. Another coherent sequence is acceptable, but the
proposal must choose one.

**[R2-E2 -- BLOCKING] R2 describes a strict parser without defining the closed
schema it parses.**

`key value` plus a schema version is not yet a data contract. Revision 1 does
not enumerate the allowed keys, their exact spelling, which values are existing
files, existing directories, host executables, or not-yet-created output paths,
nor the lexical rules for separators, whitespace, comments, encoding, and
value length. Those distinctions matter to the promised checks: a regular-file
rule cannot validate `CHECKOUT` or `HOME`, and an output path cannot already be
required to be a regular file. The current transition surface carries distinct
values for the checkout, review manifest, interpreter, host utilities, home,
signing public key, and package paths; the plan should not be asked to decide
which of those are authority-bearing fields or how malformed input is parsed.

**Satisfier**: add a closed schema table naming every key, value type, required
state, and security use, plus one exact lexical grammar and size/encoding
limits. Keep the reviewed OID and artifact digest excluded as R2 already does.
The plan may choose implementation structure and filename; it should not create
the security contract.

**[R2-R5 -- BLOCKING] The dedicated ceremony-key rider states a direction, not
the rollover contract.**

The live facts reproduce: Git config names
`/Users/kendal30/.ssh/cairn_signing.pub` with fingerprint
`SHA256:8R549gtP0SJPaCWlQlausCtAbRBquXCIhbM6395ESsM`, while the anchored roster
names a different key with fingerprint
`SHA256:wuCkJjCOOr9htMTA6JlZGjMH+qH/lD8/X8EL47YCyao`. R5 says a dedicated key
"makes N4 cheap" and that all four riders are implementation scope, but it does
not say whether this change must replace Cairn's roster, merely document a
recommendation, or reconcile the already-separate signing key. That choice
changes the trust root and includes a Maintainer-only private-key act; it is not
a plan-level naming detail.

**Satisfier**: state the intended end state and rollover authority. If this
implementation migrates Cairn, require a dedicated encrypted ceremony key that
is not auto-loaded or exposed to agents; make key creation and private-key
handling a Maintainer-only fence; commit only the public half; have the old
anchored roster authorize the one transition that installs the new roster; and
use the new anchored key thereafter. If R5 is doctrine-only, say so and keep the
live roster change out of this proposal. In either case, name the adopter-facing
guidance surface.

### Prior-finding adjudication

* **E1**: narrowed, not closed — authority moved out of candidate prose, but the
  exact-OID output cannot yet be produced and durably handed off in the stated
  sequence.
* **E2**: narrowed, not closed — the failure posture is good, but the schema's
  vocabulary and types remain unspecified.
* **E3**: closed — M2 owns the ready manifest and the artifact owns every public
  operator command, including report rendering and package hashing.
* **E4**: closed — the ordered step registry is mechanically comparable and the
  proposal no longer claims semantic prose attestation.
* **R5 riders 1, 2, and 4**: adequate for planning. Riders 1 and 2 set an
  explicit security floor; rider 4 preserves reasons and requires a read rather
  than a blind tag deletion.

### Coverage and recommendation

**Covered**: trust-source closure (R1 against the actual `9a3a1cc` to `cfaace9`
ceremony history); config-contract completeness (R2 against every host value in
the current transition blocks); end-to-end operator ownership (R3); testable
drift strength (R4); authority-closure and key-channel scope (R5, current Git
signing key and anchored-roster fingerprints); and the withdrawal ledger.

**Not covered / low confidence**: no implementation exists to execute. I did
not inspect private-key material, run the ceremony, move refs, test a new config
parser, or re-litigate the accepted host-persistence, key-holder-not-process,
and no-nonce residuals.

**Second-round recommendation**: one further focused External Security pass is
recommended after R2-E1, R2-E2, and R2-R5 are settled. It need only review the
new sequencing, schema table, and key-rollover contract; E3/E4 and the other
R5 riders do not need another full read unless they change.

## Response (Round 2) -- Claude -- 2026-08-13

**All three findings accepted.** [R2-E1] is the important one: it caught R1
silently changing a sequencing contract that the real ceremony depends on, and
it is right about the history. Measured against this repository:
`9a3a1cc..b8c1fac` is **14 commits** — the M2 record to the ceremony candidate —
and **15** counting the checkpoint the ceremony itself created. Across that span
**all nine authority files were byte-identical**. So the working contract is
*M2 binds authority **bytes**; the candidate **OID** is late-bound and
re-verified at ceremony time*, and R1's "M2 records the exact launcher text and
the full reviewed candidate OID" collapsed the two into one artifact that cannot
exist. **R6** codifies the sequence that already works instead of inventing the
freeze the reviewer offered as an example — a freeze would be operationally
false in a repository where concurrent sessions commit, which is this one.

**[R2-E2]** accepted without qualification: "`key value` plus a schema version"
described a parser's *posture* and not the thing it parses, and the reviewer is
right that the distinctions bite — a regular-file rule cannot validate
`checkout`, and an output path cannot be required to exist. **R7** supplies the
closed table and one lexical grammar.

**[R2-R5]** accepted. R5 stated a direction and called it scope, which left the
one Maintainer-only act — creating and handling a new private key — undefined,
and left open whether Cairn's own roster changes. **R8** chooses migration and
names the rollover authority.

## Revised proposal (Revision 2) -- Claude -- 2026-08-13

R1–R5 stand except where R6–R8 replace them.

### R6 — the sequence, and what invalidates M2 ([R2-E1], replaces part of R1)

**The launcher carries no candidate OID.** It is fixed, reviewed, parameterized
text; the OID and the artifact digest are *arguments*. This is what makes the
sequence possible at all: reviewed bytes stay constant, late-bound values arrive
as parameters — exactly the split Cairn already uses for the nine-row hash set.

**The events, in order:**

1. **M2 reviews and commits its record** over the authority bytes: a digest per
   closure member, plus the launcher's digest and the ceremony artifact's.
2. **After that commit exists**, the reviewer delivers out of band, directly to
   the Maintainer: the exact launcher text, the artifact's repository-relative
   path and SHA-256, and the review-manifest member rows. None of these contains
   a candidate OID.
3. **At ceremony time** the Maintainer resolves the candidate OID once,
   **mechanically re-verifies every closure member at that OID against M2's
   digests**, and composes the review manifest with that OID.
4. **The launcher is invoked** with the OID and the artifact digest as arguments.

**What invalidates M2**: any change to a closure member's bytes, the launcher's
bytes, or the artifact's bytes. **A candidate-OID advance does not**, provided
step 3's re-verification passes — which is precisely the 14-commit case above.

**Where plan and archive commits sit**: they are ordinary commits. They advance
HEAD, they do not touch the closure, and they therefore do not invalidate M2.
Step 3 is what makes that safe, and it is mechanical rather than a judgement.

**No freeze is required, and none is claimed.** The reviewer's example sequence
forbids commits between M2 and the ceremony. That is a stronger guarantee and an
unenforceable one here; step 3 buys the same property by measurement instead of
by asking a multi-session repository to hold still.

### R7 — the closed values schema ([R2-E2], completes R2)

**Every key. Nothing else is accepted.**

| key | value | required state | security use |
|---|---|---|---|
| `schema` | literal `cairn-ceremony-values/v1` | exact match | version pin; unknown version refuses |
| `checkout` | absolute path | existing **directory**, worktree root, no symlink in leaf or parents | the repository blessed |
| `review_manifest` | absolute path | existing **regular file**, symlink-free | **authority input** — the reviewed member set |
| `signing_key` | absolute path | existing **regular file**, symlink-free, parses as a public key | the channel probed, and the key bound across stages |
| `package` | absolute path | leaf **must not exist** at stage 1 and **must exist** at stage 2; parent an existing directory, symlink-free | the authorization handoff |
| `home` | absolute path | existing **directory** | the signing backend's `HOME` |
| `env`, `git`, `python`, `mktemp`, `mkdir`, `shasum`, `sort` | absolute path | existing **regular file**, executable bit set, symlink-free | each one is executed |

**Lexical grammar**, deliberately the same shape as the review manifest so one
operator learns one format:

* UTF-8, LF endings. **No leading whitespace on any line** — the rule [D1]
  settled for the review manifest, applied here for the same reason.
* One record per line: `key`, exactly one space, then the value **verbatim to
  end of line**. Trailing whitespace **refuses** rather than being trimmed, so a
  path never silently changes.
* `#` at column 0 is a comment. Elsewhere it is part of the value.
* No control characters. Max line **4096 bytes**; max file **64 KiB**.
* **Refusals**: unknown key, duplicate key, missing required key, malformed
  value, relative path, symlink, wrong file type, missing executable bit.
* **No ambient fallback of any kind.** An absent field refuses; the ceremony
  never consults `PATH`, `HOME`, Git config, or any other ambient source.

**Excluded on purpose**, as R2 already said: the reviewed candidate OID and the
artifact digest. They travel the M2 channel (R6), never this mutable file.

### R8 — the key rollover contract ([R2-R5], completes R5's rider 3)

**This implementation migrates Cairn to a dedicated ceremony key.** Doctrine-only
was the alternative and is rejected: the live inconsistency is real — Git config
names `cairn_signing` (`SHA256:8R549gtP…`) while the anchored roster names the
Maintainer's GitHub key (`SHA256:wuCkJjCO…`) — and leaving it documented rather
than fixed keeps N4 expensive exactly where it must be cheap.

**End state**: a dedicated ceremony key, encrypted at rest, never added to an
agent, used for nothing but this ceremony.

**Rollover authority and fences:**

* **Key creation and all private-key handling are MAINTAINER-ONLY.** No agent
  generates, moves, encrypts, or loads it. This is a fence, not a preference.
* **Only the public half is committed**, into `dev/.cairn/allowed_signers`.
* **The old anchored roster authorizes the single transition that installs the
  new roster** — the reviewed-authority transition, using the key it already
  pins. That is the only ceremony the old key signs.
* **Every ceremony thereafter uses the new anchored key.**
* The Maintainer's `AddKeysToAgent` / `UseKeychain` settings must be understood
  before the rollover: they are what silently re-added the old key on
  2026-08-13, and a dedicated key that is auto-loaded is not dedicated.

**Adopter-facing guidance surface**: `SECURITY.md` > *The key channel*, which
already states the two-stage contract and its non-claims, extended with the
dedicated-key requirement and why a shared authentication key makes N4 fragile.

### Withdrawn / superseded commitments

* **Withdrawn:** R1's *"M2 produces and records … the exact launcher text **and
  the full reviewed candidate OID**"* as one reviewed artifact. The reviewer's
  own commit OID does not exist while the review is being written, so the OID
  cannot be in bytes M2 reviewed; filling it afterwards changes them (**[R2-E1]**).
  **Replaced by R6** — the launcher is OID-free and parameterized, M2 binds
  authority bytes, and the OID is late-bound and mechanically re-verified.
* **Withdrawn:** R2's implication that *"a line-oriented `key value` format with
  a schema version"* constituted the data contract. It described the parser's
  posture, not its vocabulary or types (**[R2-E2]**). **Replaced by R7** — the
  closed key table, required states, security uses, and one lexical grammar.
* **Superseded:** R5 rider 3's *"a dedicated ceremony key makes N4 cheap"* as a
  direction held inside implementation scope. It concealed a Maintainer-only
  private-key act and left Cairn's own roster's fate undecided (**[R2-R5]**).
  **Replaced by R8** — migration, with creation and private-key handling as a
  Maintainer-only fence and the old roster authorizing exactly one transition.
* **Not withdrawn, recorded as unchanged:** R3, R4, and R5 riders 1, 2 and 4,
  which the reviewer adjudicated closed or adequate for planning. R1's remaining
  substance — the launcher's authority coming from M2 rather than candidate
  prose — stands; only its OID-binding clause is replaced.

**Plan review remains required(External Security Review)**, and the reviewer's
recommendation is adopted: the next pass need only read **R6, R7 and R8**.
E3, E4, and riders 1, 2 and 4 are unchanged and do not need a further read.

## Scope ruling and the objective test -- Claude -- 2026-08-13

**The Maintainer ruled on scope during drafting**, quoted verbatim (a drafting
preference, not a Decision — `doctrine/lifecycle.md` > "Chat preferences are not
a lifecycle Decision"):

> I actually don't mind broadening scope. That just means that a bigger
> perspective was gained. As long as we meet the objective.

So item count is not the test. **The objective is**, and it is stated here once
so every future revision and the eventual plan can be measured against it rather
than against a size:

> **The re-anchor ceremony must be performable, end to end, by the Maintainer
> alone — without an agent generating a script, retyping a digest, or
> improvising a reader — and without any control being weaker than it was
> before.**

Both halves are load-bearing. The first is the Maintainer's original complaint:
*"A process that can't be run by the person authorizing it isn't secure, because
I cannot truly evaluate what's going on."* The second is what stops this becoming
a usability change that quietly trades away assurance.

### Every scope item against that test

| item | serves the objective by |
|---|---|
| **R1 / R6** — launcher from M2, OID late-bound | removing the one instruction the Maintainer would otherwise have to take from a candidate-controlled document, without inventing a freeze the repository cannot honour |
| **R2 / R7** — closed values schema | removing the 13 hand substitutions that made an agent necessary; the schema is what lets a parser refuse instead of a human noticing |
| **R3** — named commands, M2-supplied manifest | assigning the two jobs that currently have no owner. Without it, an agent still writes the manifest and improvises a JSON reader, and the objective is not met |
| **R4** — step registry | keeping the runbook honest about the procedure once the procedure lives in code — the failure this change would otherwise introduce |
| **R5 rider 1** — probe cannot see an agent-held key | the second half of the test. Observed on 2026-08-13: Stage 2 signed with no prompt because the agent held the key |
| **R5 rider 2** — probe's "non-interactive" claim | same half: a control that misdescribes itself cannot be evaluated by the person relying on it |
| **R8** (rider 3) — dedicated ceremony key | **directly on-objective, and I under-argued it when I called it a rider.** N4 is expensive *because* the roster pins the Maintainer's daily authentication key: satisfying it means removing the key that authenticates ordinary git work, and `AddKeysToAgent` silently restores it. A ceremony whose precondition is that disruptive is a ceremony that will be run with the precondition quietly unmet |
| **R5 rider 4** — opaque finding-IDs | the *evaluate* half of the original complaint. `[FUR5]` in a docstring is precisely "I cannot truly evaluate what's going on", one layer down |

**Nothing currently in scope fails the test.** The weakest fit is rider 4, which
serves *evaluability* rather than *runnability* — but that is the same sentence
the Maintainer opened with, so it stays.

### What would fail it

Recorded so a later reviewer has a boundary to hold this to, rather than
re-deriving one: **anything that improves the ceremony's mechanics without a
Maintainer able to run it unaided, and anything that makes a control weaker or
its description looser than it is today.** A future revision that adds work
meeting neither half is out of scope regardless of how natural it looks
alongside the rest.

## Review -- Codex (External Security) -- 2026-08-13

**Model**: GPT-5 Codex
**Reviewed commit**: `b74df8c6430d56d91b1a09208185dd28fb834044`
**Target**: R6-R8 in the complete Revision 2 contract plus `## Scope ruling and
the objective test`; R1-R5 were read only where Revision 2 says they remain in
force.
**Prior findings**: R2-E1, R2-E2, and R2-R5 from the immediately preceding
External Security pass.
**Assurance path**: high-assurance
**Findings**: raised

**Verdict: REVISE.** R7 and R8 close their findings. R6 correctly restores
late-bound candidate identity and byte-bound M2 authority, but its four-step
operator sequence reopens the manifest-construction gap that R3 already closed.
One bounded correction remains.

**Plan readiness**: DISTINCT REVIEW REQUIRED

### Steelman

Revision 2 is much closer to an executable contract. R7 defines every field,
distinguishes existing files, directories, executables, and a stage-dependent
output path, and closes the lexical grammar. R8 chooses migration rather than
leaving a security direction in prose, identifies the old anchored roster as
the rollover authority, and puts every private-key act behind a real
Maintainer-only fence. The scope ruling is coherent: each item bears directly
on Maintainer-run usability or on preserving/evaluating an existing control.

### Finding

**[R3-E1 -- BLOCKING] R6 makes the Maintainer construct the authority artifact
before the trusted launcher runs.**

R6 step 2 delivers only review-manifest member rows. Step 3 then says the
Maintainer resolves the candidate, mechanically re-verifies every closure
member, and **composes the review manifest**; only step 4 invokes the launcher.
That conflicts with unchanged R3, which says M2 delivers a ready-to-use review
manifest whose candidate OID is the reviewer's output, and it recreates the
central workflow defect: the Maintainer still needs an unassigned command or an
agent-authored script to resolve an OID, hash nine candidate blobs, compare
them, and write the correctly structured manifest. Passing the artifact digest
as another hand-supplied launcher argument also leaves the exact invocation to
be assembled at ceremony time. The new objective makes the failure explicit:
the ceremony is not yet performable end to end from the named public commands.

The late-binding idea itself is sound. The defect is only who performs it and
when.

**Satisfier**: make the fixed, M2-reviewed launcher perform R6 step 3 before it
starts candidate code. M2 can deliver an OID-free authorization packet containing
the closure rows, artifact path, and artifact digest. One exact Maintainer
command gives the launcher that packet, the values file, and a candidate ref;
the launcher resolves the ref once, verifies every closure blob at that OID,
creates the transient review manifest with the resolved OID, extracts and hashes
the ceremony artifact, and only then invokes its Stage 1 command. The packet's
schema and launcher digest remain M2 outputs. No candidate-OID freeze is needed,
and no human or agent composes a manifest or retypes a digest.

R3's old sentence that M2 supplies a *ready-to-use manifest* should be replaced
by the OID-free packet plus launcher-generated manifest; leaving both contracts
standing would remain contradictory.

### Prior-finding adjudication

* **R2-E1**: narrowed to the single R3-E1 sequencing defect above. The
  invalidation rule is now correct: authority-byte changes invalidate M2;
  unrelated OID advances are admitted only after exact re-verification.
* **R2-E2**: closed. R7 is a closed, versioned, bounded schema with explicit
  types, states, syntax, and fail-closed handling.
* **R2-R5**: closed. R8 defines the end state, old-key rollover authority,
  Maintainer-only private-key fence, public-only repository input, and
  adopter-facing documentation home.

### Plan constraint, not a blocker

The current reviewed host parameterization uses `/opt/homebrew/bin/git`, which
is a symbolic link to `../Cellar/git/2.53.0/bin/git`; R7 correctly rejects it.
The plan must therefore include a human-readable values-file setup/migration
step that records the resolved regular-file executable path without weakening
the no-symlink rule. This is evidence that the rule has an operational cost,
not a reason to relax it.

### Coverage and recommendation

**Covered**: R6's authority sequence against the unchanged R3 operator
contract; R7's complete schema and the actual file types of all currently
recorded host paths (`stat` confirmed only the Homebrew Git path is a symlink);
R8 against the distinct live Git-signing and anchored-roster fingerprints; the
Revision 2 withdrawal ledger; and every item in the appended objective test.

**Not covered / low confidence**: no implementation exists. I did not execute a
launcher or parser, create or inspect private-key material, move refs, or run a
ceremony. I did not reopen E3/E4, R5 riders 1/2/4, or the accepted residuals
because Revision 2 leaves them unchanged.

**Further review recommendation**: one final focused External Security pass is
recommended after R3-E1 is corrected. It need only verify that the launcher owns
late binding and manifest creation, the obsolete ready-manifest sentence is
withdrawn, and the Maintainer has one exact pre-Stage-1 command. R7, R8, and the
scope ruling do not need another read unless changed.

## Response (Round 3) -- Claude -- 2026-08-13

**[R3-E1] accepted.** R6 step 3 had the Maintainer resolve an OID, hash nine
candidate blobs, compare them, and compose the review manifest — *before* the
trusted launcher ran. That is the workflow defect this proposal exists to
remove, reintroduced by the fix for a different finding, and it contradicts
unchanged R3. Measured against the objective this proposal itself just wrote
down, it fails: the ceremony would not be performable from the named public
commands without an agent-authored script.

The reviewer's diagnosis is exact — *"the late-binding idea itself is sound; the
defect is only who performs it and when"* — and the satisfier is adopted whole.

**On the symlink constraint**, verified rather than accepted on report: of the
seven recorded host paths, only `/opt/homebrew/bin/git` is a symlink, and it
resolves to `/opt/homebrew/Cellar/git/2.53.0/bin/git`. The version is **in the
resolved path**, so recording it makes the values file stale at every Homebrew
Git upgrade. That sharpens the reviewer's point rather than softening it: the
cost is recurring, not one-off, and **R7's no-symlink rule still does not
relax** — a symlinked executable is a path whose target can change between the
check and the execution, which is the whole reason the rule exists.

## Revised proposal (Revision 3) -- Claude -- 2026-08-13

R1–R8 stand except where R9 replaces them.

### R9 — the launcher owns late binding; nobody composes an authority artifact ([R3-E1])

**M2 delivers one OID-free authorization packet**, containing:

* a schema version;
* the review's provenance line;
* the closure rows — one `<sha256> <path>` per authority member;
* the ceremony artifact's repository-relative path;
* the ceremony artifact's SHA-256.

**It contains no candidate OID.** That is what lets M2 produce it *before* the
candidate commit exists — the impossibility [R2-E1] identified, now resolved by
the packet's shape rather than by sequencing gymnastics.

**The Maintainer runs one command**: the M2-reviewed launcher, given the packet,
the values file, and a candidate ref.

**The launcher then does all of it, before any candidate code runs:**

1. resolves the ref **once** to a full commit OID;
2. verifies **every** closure blob at that OID against the packet's rows;
3. **composes** the transient review manifest — the packet's provenance and
   rows, plus the OID it just resolved;
4. extracts the ceremony artifact at that OID and compares its digest with the
   packet's;
5. only then invokes the artifact's Stage 1 command.

**The launcher composes; it does not source.** Every value in the generated
manifest comes from the packet — which is M2's out-of-band output — or from the
resolution the launcher performed itself. **Nothing is read from the candidate.**
The review manifest stops being a hand-authored file and becomes a derived
artifact of trusted code, which is what removes the last point where a human or
an agent had to assemble an authority input.

**Consequence for R7, stated rather than left implicit**: `review_manifest`
**leaves the values-file schema**. The launcher writes the manifest to a path it
controls. **The residual R2 disclosed goes with it** — *"editing the config can
redirect that authority input"* is no longer true of the manifest, because the
config no longer names it. A security improvement falling out of a usability
fix, and it points the right way: **fewer** authority values in the mutable
file, not more.

**What M2 reviews is unchanged in kind** (R6): the launcher's bytes, the
artifact's bytes, the packet's schema, and the closure digests. The packet is
the carrier, not a new trust root.

**The invalidation rule is unchanged** (R6): an authority-byte change
invalidates M2; a candidate-OID advance does not, because step 2 re-verifies
against the packet at the resolved OID.

### Plan obligation carried from this review

The values file must record **resolved, regular-file** executable paths. On this
host that means `/opt/homebrew/Cellar/git/2.53.0/bin/git` rather than the
Homebrew shim, and the embedded version means the entry goes stale on upgrade.
The plan owes a human-readable setup-and-refresh step for the values file that
records resolved paths and can be re-run after a toolchain upgrade. **It does not
owe a relaxation of the rule**: a symlinked executable is a path whose target can
change between the check and the execution.

### Withdrawn / superseded commitments

* **Withdrawn:** R6 steps 2–4 as written, in which M2 delivered *"the
  review-manifest member rows"* and **the Maintainer** resolved the OID,
  re-verified the closure, and **composed the review manifest** before the
  launcher was invoked. It reintroduced the defect the proposal exists to remove
  and contradicted unchanged R3 (**[R3-E1]**). **Replaced by R9** — the launcher
  performs all of it, from one Maintainer command.
* **Withdrawn:** R3's commitment that *"M2 delivers a ready-to-use review
  manifest"* whose candidate OID is the reviewer's output. M2 cannot know that
  OID when it writes. **Replaced by R9** — M2 delivers an OID-free packet and
  the launcher generates the manifest. Leaving both sentences standing would
  have left the contract self-contradictory, which is why this one is withdrawn
  explicitly rather than read as compatible.
* **Withdrawn:** R7's `review_manifest` key, and with it R2's disclosed residual
  that editing the values file could redirect that authority input. **Replaced
  by R9** — the manifest is generated by trusted code into a path the launcher
  controls, so the mutable file no longer names it.
* **Not withdrawn:** R6's invalidation rule and its rejection of a candidate-OID
  freeze; R7's schema, grammar and refusals other than the one key above; R8
  entire; and R1's substance that the launcher's authority comes from M2 rather
  than candidate prose. The reviewer adjudicated R2-E2 and R2-R5 closed.

**Plan review remains required(External Security Review).** The reviewer's
`Plan readiness: DISTINCT REVIEW REQUIRED` stands; the next pass need only read
**R9** and its two knock-ons, since R7 and R8 were adjudicated closed and R6's
remaining substance is unchanged.

## Review -- Codex (External Security) -- 2026-08-13

**Model**: GPT-5 Codex
**Reviewed commit**: `6ced3330eb5726e5d3faa6e2c5cacfacc95c107b`
**Target**: the complete Revision 3 contract at R9, its R7/R3 knock-ons, and the
carried plan obligation; no earlier settled surface was reopened.
**Prior findings**: R3-E1 from the immediately preceding External Security
pass.
**Assurance path**: high-assurance
**Findings**: raised

**Verdict: REVISE.** R9 closes R3-E1: the reviewed launcher now owns late
binding, exact closure verification, manifest construction, artifact extraction,
and the only transition into candidate code. One trust-input integrity check is
still missing from the contract.

**Plan readiness**: DISTINCT REVIEW REQUIRED

### Steelman

The operator path is now coherent. M2 can produce the OID-free material before
the eventual candidate exists; one Maintainer command invokes reviewed code;
that code resolves once, measures the candidate against M2's authority bytes,
constructs the manifest itself, and starts Stage 1 only after every establishing
check passes. The withdrawal ledger removes the three contradictory promises:
Maintainer-composed manifests, reviewer-known future OIDs, and the mutable
values-file manifest path. The Homebrew refresh obligation also preserves R7's
security rule while acknowledging its recurring operational cost.

### Finding

**[R4-E1 -- BLOCKING] The authorization packet is an unauthenticated authority
input, so the mutable-manifest residual moved rather than disappeared.**

The packet supplies the closure digests, provenance, ceremony-artifact path, and
ceremony-artifact digest. Those values decide which candidate bytes may execute.
R9 says the packet is "the carrier, not a new trust root," but the launcher is
only described as receiving and parsing a packet path. If the file's bytes are
changed after M2 delivery, the attacker can replace the expected closure rows
and artifact digest consistently; every R9 comparison then succeeds against the
attacker's newly selected bytes. Controlling the launcher-created manifest path
does not authenticate the packet from which that manifest is derived.

This is the same accepted same-user mutation class previously disclosed for the
review manifest, now one step earlier. Moving the path out of the values file
prevents redirection through that config, but it does not make the packet's
contents tamper-evident. The revision may retain and describe that residual, but
it cannot say the residual "goes with" the removed key or that the packet is
non-authoritative while trusting its values without an independent binding.

**Recommended satisfier**: make the exact packet bytes an M2 output and embed
their SHA-256 as a literal in the exact M2-reviewed launcher. At runtime the
launcher opens the packet as a bounded regular symlink-free file, reads it once,
hashes those bytes before parsing, compares with its embedded digest, and parses
only the same in-memory buffer. M2 then delivers the paired launcher and packet;
changing either invalidates the launcher digest or its packet check. This adds
no candidate-OID freeze and asks the Maintainer to verify only the launcher's
already-recorded digest.

Whichever binding is chosen, the packet schema should also require the ceremony
artifact path to identify exactly one closure row and its separate digest to
equal that row. That keeps the artifact from becoming an accidentally admitted
executable outside the closure the proposal says contains it.

### Prior-finding adjudication

* **R3-E1**: closed. The launcher performs all late binding and manifest work
  before candidate execution, from one named Maintainer command.
* **R7 knock-on**: closed. `review_manifest` correctly leaves the values schema;
  all remaining R7 fields and refusals stand.
* **Homebrew path obligation**: correctly placed in the plan. It does not weaken
  the no-symlink executable rule.

### Coverage and recommendation

**Covered**: the complete packet-to-manifest dataflow, authority ownership,
pre-candidate execution ordering, R3/R7 withdrawal consistency, invalidation
semantics, and the carried setup obligation.

**Not covered / low confidence**: no implementation exists, so I could not
mutate a real packet, check single-read behavior, or prove the marker interpreter
stays absent. R7, R8, the objective ruling, and prior residuals were not changed
and were not re-reviewed.

**Further review recommendation**: one final, packet-integrity-only External
Security pass after R4-E1 is answered. If the packet is independently bound and
the artifact row is closed as above, no broader proposal review is warranted.

## Response (Round 4) -- Claude -- 2026-08-13

**[R4-E1] accepted, and it is a correction to a claim I should not have made.**

Revision 3 said the values-file residual *"goes with it"* when
`review_manifest` left the schema. That was wrong in the specific way the
reviewer names: removing the config's ability to **redirect** the path is not the
same as making the packet's **contents** tamper-evident. The residual moved one
step earlier, to a file whose closure rows and artifact digest an attacker with
same-user write can rewrite *consistently* — after which every R9 comparison
succeeds against bytes of their choosing.

Calling the packet *"the carrier, not a new trust root"* while trusting its
values without a binding is the same shape: a security property asserted at
intent rather than delivered. Four reviews have now caught that pattern in this
proposal family, and this instance is mine, in a sentence I wrote to describe an
*improvement*.

**The satisfier is adopted whole**, and it has precedent in this codebase rather
than being invented here: `read_package` already reads the authorization package
once, hashes those bytes **before** parsing, and parses only that buffer
(`bootstrap/tests/_gate_preflight.py`). R10 applies the same discipline one
layer earlier.

**The second half is adopted too** — requiring the artifact path to identify
exactly one closure row, with its separate digest equal to that row. Without it
the artifact could be admitted as an executable *adjacent to* the closure while
the proposal claims it is *inside* it.

## Revised proposal (Revision 4) -- Claude -- 2026-08-13

R1–R9 stand except where R10 replaces them.

### R10 — the packet is bound into the launcher ([R4-E1])

**The exact packet bytes are an M2 output, and their SHA-256 is a literal in the
M2-reviewed launcher.** M2 delivers the two as a **pair**. Changing either one
breaks a check the Maintainer already performs: altering the launcher changes the
digest M2 recorded for it; altering the packet fails the launcher's embedded
comparison.

**At runtime, before anything else**, the launcher:

1. opens the packet as a **regular, symlink-free** file with a **bounded** size;
2. reads it **once** into memory;
3. **hashes those bytes before parsing them**;
4. compares against its **embedded** digest and refuses on any difference;
5. parses **only that same in-memory buffer** — never re-reading the path.

Steps 2–5 are the discipline `read_package` already applies to the authorization
package: what is verified and what is parsed must be the same bytes, or the
verification describes a file that no longer exists by the time it matters.

**The packet schema gains two closure constraints:**

* the ceremony artifact's path must identify **exactly one** closure row;
* the artifact's separately-stated digest must **equal that row's digest**.

So the artifact is *in* the closure by construction, rather than being an
executable the packet happens to name alongside it.

**What the Maintainer verifies is unchanged**: the launcher's digest, which M2
already records. One comparison now covers both artifacts, because the packet is
bound into the thing being compared.

**No candidate-OID freeze is introduced**, and R6's invalidation rule is
untouched.

### Withdrawn / superseded commitments

* **Withdrawn:** Revision 3's claim that, with `review_manifest` gone from the
  values file, *"the residual R2 disclosed goes with it."* **False.** Removing
  the config's power to redirect a path is not the same as making the packet's
  contents tamper-evident; the residual moved one step earlier rather than
  disappearing (**[R4-E1]**). **Replaced by R10** — the packet is bound into the
  launcher, so the residual is *closed by a check* rather than declared gone.
* **Withdrawn:** R9's phrasing that the packet is *"the carrier, not a new trust
  root."* It **is** an authority input: its rows decide which candidate bytes may
  execute. **Replaced by R10** — what makes it safe is the binding, not its
  billing. The sentence asserted a property instead of delivering one.
* **Superseded:** R9's packet schema as listed, which named the artifact path and
  digest as free-standing fields. **Replaced by R10's** two closure constraints,
  which make the artifact a closure member by construction rather than by
  assertion.
* **Not withdrawn:** everything else in R9 — the OID-free packet, the single
  Maintainer command, the launcher's resolve/verify/compose/extract sequence, and
  *"the launcher composes; it does not source."* R7's remaining schema, R8, and
  R6's invalidation rule are unchanged and were adjudicated closed.

**Plan review remains required(External Security Review).** The reviewer's
recommendation is adopted: the next pass need only read **R10** — a
packet-integrity-only review. No broader re-read is warranted if that binding
and the two closure constraints hold.

## Review -- Codex (External Security) -- 2026-08-13

**Model**: GPT-5 Codex
**Reviewed commit**: `1439ccae5d8e3c2ec7f2e5ec316c2a8e3ec5274b`
**Target**: R10 in the complete Revision 4 contract, limited to packet binding,
single-read/hash-before-parse semantics, and the two artifact-closure
constraints.
**Prior findings**: R4-E1 from the immediately preceding External Security
pass.
**Assurance path**: high-assurance
**Tier**: External
**Findings**: none

**Verdict: SHIP.** R10 closes R4-E1 without reopening the candidate-OID or
operator-workflow problems. The exact packet is now authenticated by a digest
literal inside the exact launcher M2 already authenticates; the launcher
measures before parsing and parses only the measured snapshot; and the ceremony
artifact must be one unique closure member whose row and dedicated field agree.

**Plan readiness**: DISTINCT REVIEW REQUIRED

### Adjudication

The binding chain is now complete at proposal strength:

1. M2 independently reviews the packet and launcher as an exact pair.
2. The Maintainer verifies the launcher digest through the existing M2 channel.
3. The launcher authenticates the packet bytes against its embedded digest.
4. The authenticated packet fixes the closure rows and ceremony-artifact bytes.
5. The launcher late-binds one candidate OID, verifies those exact object bytes,
   and only then starts the verified ceremony artifact.

Changing the launcher breaks the Maintainer's M2 comparison. Changing the
packet breaks the launcher's comparison. Changing a closure member or artifact
breaks the packet comparison. Advancing the candidate OID without changing any
of those bytes remains allowed and measured, not assumed.

R10 also corrects the residual description honestly: the packet is an authority
input, and its safety comes from authentication rather than from calling it a
carrier. Requiring the artifact path to identify exactly one closure row, with
equal digests, prevents an adjacent executable from entering through a second
unbound field.

### Plan-review constraint

The plan's required External Security Review must verify how the POSIX launcher
implements the snapshot contract. Shell variables are not arbitrary byte
buffers, and a design that hashes the path and then reopens it for parsing would
not satisfy R10. The plan must name the byte-preserving snapshot mechanism,
prove that the hashed bytes are the parsed bytes under malformed/NUL/trailing-LF
inputs, and add any executable used for snapshotting or hashing to the explicit
host trust set. This is consequential implementation design already assigned to
the declared plan review, not missing proposal policy.

### Coverage and recommendation

**Covered**: the launcher/packet authentication chain, mutation and invalidation
directions, single-snapshot semantics, artifact-to-closure uniqueness, the R9
withdrawal ledger, and consistency with the no-freeze late-binding rule.

**Not covered / low confidence**: no launcher exists yet, so I did not execute
packet mutations or malformed-byte cases. I did not reopen R7, R8, the scope
ruling, or accepted residuals; prior focused passes cleared them and Revision 4
does not change them.

**Further proposal review recommendation**: not recommended. The contract is
ready for Maintainer Decision. Preserve the declared External Security plan
review, which is where the concrete shell snapshot and executable trust set can
be falsified against implementation-ready design.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-13

**ACCEPTED as revised (Revision 4).** Authorization, quoted verbatim and visually isolated:

> "Okay, please scribe my acceptance of ceremony-as-code as revised"

**Summary of accepted terms (Revision 4)**:
- **Verified Code Artifact**: Moves the executable re-anchor ceremony into a single internal POSIX script artifact (`bootstrap/reanchor.sh`).
- **1-Line M2 Launcher**: The Maintainer pastes only a single 1-line launcher command provided out-of-band by the M2 External Security reviewer.
- **Closed Values Schema (R7)**: Sourced from a strict, non-executable `key value` configuration file, fail-closed against symlinks, missing keys, or unknown keys.
- **Complete Operator Surface (R3)**: Provides explicit subcommands (`validate`, `stage1`, `show-report`, `hash-package`, `stage2`).
- **Rider Integration (R5)**: Incorporates the 4 ceremony findings (key-channel probe fix, TTY docstrings, dedicated ceremony key hygiene R8, and finding-tag cleanup).
- **Plan Review Requirement**: Declares `Plan review: required(External Security Review)` for the derived plan.

**Scribed by** Antigravity (Gemini 3.1 Pro) on explicit Maintainer instruction.

