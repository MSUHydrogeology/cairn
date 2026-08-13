# The ceremony belongs in verified code; the runbook belongs in prose

**Author**: Claude (Implementation)
**Model**: Claude Opus 5
**Date opened**: 2026-08-13
**Status**: proposed
**Assurance path**: high-assurance — the re-anchor ceremony is a named
high-risk surface and the authority closure's own contents change.
**Touches**: `bootstrap/REANCHOR_RUNBOOK.md`, a new ceremony code artifact,
`bootstrap/tests/_gate_preflight.py`'s recorded-block tests, the authority
closure membership.
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
