# Re-pinning, revitalized — one approval loop the Maintainer can actually run

**Author**: Claude (Strategy)
**Model**: Fable 5
**Date**: 2026-08-28
**Status**: open (working-agent input folded 2026-08-28; Codex External
strategy review at `9450676` — verdict REVISE BEFORE PROMOTION, five
findings, all accepted — folded in and removed 2026-08-28 per the template;
the review text lives at commit `65045a6`)
**Type**: design-exploration
**Surfaces this feeds**: a deliberate-lane proposal (trust-ceremony surface —
Security Review required, External floor at the proposal);
`bootstrap/REANCHOR_RUNBOOK.md` and `bootstrap/AST_BASELINE_RUNBOOK.md`;
the successor to the blocked `scripts/correct_pinned_digests.py`; the
security strategy's [REL-1]/[REL-3]/[TRU-5] rows

## The design input, verbatim

The Maintainer, mid-ceremony, 2026-08-27 (recorded as a security finding in
the security strategy's Live residual register):

> "this whole ceremony thing is really just me doing what you tell me to do.
> It's a mess, and I've asked for it to be fully scripted multiple times but
> that hasn't been delivered. I'm happy to compare two different sets of
> checksums or something, but I don't have the qualifications or time to do
> anything more."

And 2026-08-28, commissioning this note: re-anchoring and re-pinning must
become *"much more user-friendly... keeping it secure but also actually
something I can do."*

The register already names the honest fork: **(a)** drive the human step down
to what the operator can genuinely do, with everything else committed as
tested tooling; or **(b)** admit the human leg is a formality and stop
claiming operator judgment as a control. This note is the design for (a).

## What is broken, from the record — not re-argued

* **The human leg is a relay, not a control.** The agent in the room composes
  the instructions; the Maintainer executes them. The runbook's forbidden
  shape — the implementer blessing its own verifier — reached through a
  human. The correction scripts were written from scratch **three times**
  (`c3d5bd9`, `77d2b3b`, `d283589`-era); nothing accumulates; the Maintainer
  has a standing dependency on whichever agent is present.
* **The committed runner failed review, fundamentally.** Codex External
  Security Review: BLOCK, seven findings, two CRITICAL, each reproduced —
  the plan digest bound a *projection*, so two materially different trees
  digested identically and `apply` wrote unauthorized values; provenance by
  pickaxe showed the Maintainer the wrong commit subjects at the moment of
  authorization; `--authorize` let any process perform the purported human
  act. The review's close is a redesign, not a patch. The runner refuses on
  entry.
* **The ceremony's own apparatus is attack surface.** The env-injection
  lived in the ceremony's *values reader*, and its disclosure print showed
  the injected value under "nothing below was discovered" — the one moment
  of real oversight, handed a false statement. Fixing it voided the
  authority-closure clearance, so the ceremony is deadlocked on re-reviewing
  apparatus. The instantiated launcher is bound to its reviewed template by
  nothing, and performs 9 of the registry's 19 steps.
* **Four pinning systems, four dialects.** Gate anchor (two-stage key
  ceremony, 615-line runbook), gate manifest re-pin, AST baseline re-anchor
  (182-line runbook), lockfile reconciliation. The routine ones redden on
  ordinary work (every `bootstrap/_scaffold/` change owes a baseline
  re-anchor), so the heavy dialect keeps getting exercised by hand, by
  scratch script, on the surfaces where mistakes matter most.

## The reframe — one approval loop

All four systems are the same loop wearing different costumes:

> A **protected set** of files changes only through reviewed work. Drift
> accumulates between pins. A **Maintainer approval** moves the pin to the
> current, reviewed state.

The strategy is to build that loop **once**, honestly divided between what
machines verify and what the human attests.

**What the machine attests** (committed, tested, itself in the protected
set): what changed since the last pin, byte-exactly; which commits changed
it, derived from file history — never pickaxe; which reviewed lifecycle
artifacts cover those commits; and one **immutable transaction object**
(Codex RPR-1's resolution, chosen over fresh-process re-derivation as the
simpler coherent design): every input bound — the signed commit's tree,
plus every non-tree influence named explicitly — and the exact output
bytes, rendered once as the thing the Maintainer reads, with **no later
live or candidate read**, applied only through exact-preimage
compare-and-swap with atomic, contained, read-back writes. The earlier
A/B-independence claim is deleted, not weakened: the transaction object
replaces it.

**What the Maintainer attests** — corrected by the working agent's triage of
the 19 registry steps, which found exactly **one judgment in the whole
ceremony**: RA-14, *read the report; does it describe what you intend to
bless?* The first draft of this note kept "compare the digest against one
you computed yourself" as a human act; the working agent showed that is
**fiction on one machine** — a human running `shasum` and a program running
`shasum` are the same act under the same OS user, and in practice the
Maintainer was handed a digest to paste. So the human leg is:

1. **The judgment (RA-14, promoted to the center).** Read the classified
   report — every changed file traced to a reviewed record, each change
   marked as touching code that **decides** or content that is merely
   **pinned** — and answer one question: *does this describe what I intend
   to bless?* Checking that reviews exist and the intent matches is a
   judgment a non-specialist genuinely can make; re-auditing the reviewed
   changes is not, and the ceremony must stop pretending to ask for it.
   **The semantic assurance comes from the lifecycle reviews that landed
   the changes; the ceremony proves linkage, never repeats them.**
2. **The typed confirmation — named honestly as a confirmation and intent
   record**, not authentication and not an enforceable authorization
   boundary (Codex RPR-3): under one OS user a tool can authenticate
   nobody, and the honest fix is deleting that claim. The *enforceable*
   boundary during a root move is **capability separation — the dedicated
   ceremony key**: Maintainer-only unlock, absent while candidate code
   runs. The ordinary signing key, which agents commit with, supplies no
   such boundary and is never described as one. The landed form (the
   ceremony driver, 2026-08-28, after its adversarial review caught the
   tool comparing its own arithmetic against itself): the confirmation
   value is computed **twice, by two different programs**, both shown,
   disagreement refuses — described in the tool's own text as exactly what
   it is: two programs on one machine, not a second party.
3. **The key (RA-16)** — the one step in the entire registry no code can
   enforce, which the runbook itself calls the real fence. That it is the
   *only* such step is the runbook's own argument for this whole strategy:
   everything else is arithmetic a script does faster and more reliably.

Everything around these three goes silent. The steps whose only function is
servicing the apparatus (RA-01, RA-03, RA-08, RA-15 per the working agent's
triage) are deleted from the Maintainer's attention, not explained better —
"I am doing nothing of use" was literally accurate for them.

## The shape of the build

**1. One committed tool** (working name `repin`), successor to the blocked
runner and the thrice-rewritten scratch scripts. Three verbs:

* `status` — the drift report: per changed protected file, a one-line what,
  the commits (by file history), and the reviewed artifact covering each.
  An uncovered change renders as a refusal-grade warning, not a footnote.
* `package` — the reviewable bundle and its digest, computed fresh.
* `apply` — exact-preimage compare-and-swap after the Maintainer types the
  confirmation value from the rendered transaction (their intent record);
  atomic contained writes with read-back; no `--authorize`, no
  non-interactive path to the human act.

One rule for every check the tool makes, from a shape that recurred twice
in one day (a lockfile reconciliation, then the ceremony packet): **measure
over the declared set, never the present one.** A packet with zero member
rows must refuse, not vacuously match — and each such check gets a
zero-member control test proving it can.

The Codex redesign requirements are inherited **as triaged by the working
agent, not verbatim**: items (1) and (5) without reservation — the closed
JSON-native plan binding exact input *and* output bytes (the fix to the
whole projection class), and public-path tests for every reproduced failure
*including controls proving a guard has not become refuse-all* (the
discipline this repo failed three times in one session). Item (3) amended —
typed confirmation renamed to what it is, with the dedicated key as the
real boundary (above). Item (2)'s **property is kept; its mechanism is
replaced**: the working agent's "second parser" equivalence was false
(Codex RPR-1 — fresh execution of *one* implementation is not a second
grammar, and `sys.modules` staleness is a real defect the BLOCK
reproduced), but rather than re-running derivations in sterile processes,
this design delivers the same guarantee through the immutable transaction
object — bind once, render that object, never read live again. Cutting the
launcher's second values *parser* is a separate, compatible win. The AST
runbook's complete-set guard is preserved; git errors fail closed. The tool
joins the protected set, so the previous pin covers the tool that moves the
next one.

Four constraints from the working agent's attack on this note's first
draft, adopted as design rules:

* **Sign the whole tracked tree; name every other influence; keep the
  protected-set rule as *policy* under prior-trusted control.** A signed
  commit binds parent and complete tracked tree, which kills the
  demonstrated projection defect — but only for tracked state (Codex
  RPR-2): untracked and ignored inputs (the interpreter binding lives in
  one), host executables, and any live read after the signed object was
  shown are part of the preimage whenever they influence a result, so the
  transaction names them explicitly. And calling the manifest a lint does
  not make it non-authoritative — the rule that says which files *decide*
  is policy authority; it is **derived from the prior trusted state, and a
  change to the rule itself is separately authorized**, never smuggled
  through an ordinary re-pin. A signature authenticates a key holder, not
  the process that requested the signature; the design says so.
* **Classify before showing.** A diff of 365 commits (measured at the
  reviewed commit) is not comprehensible
  because it is a diff; it is comprehensible only behind a classification
  the machinery already knows and never presents: does this change touch
  code that **decides**, or content that is merely **pinned**? A strategy
  that ships "show a diff" without "classify first" ships the old opacity
  in a new costume.
* **Cut the second parser — worth more than any single hardening.** One
  values grammar has two implementations (the launcher's own reader, needed
  before it can trust the artifact's), bound by a parity test; the
  env-injection appeared in *both* because they are one design, and had to
  be fixed twice; three registry steps exist only to service the split; and
  the shared defect landed in the operator's one moment of real oversight
  (the disclosure print). This, not the injection alone, is the
  economy-of-mechanism evidence.
* **Fix the asymmetric failure modes before consolidating.** The four
  systems pin at four granularities, and the gate manifest fails loudly on
  deletion but *silently on modification* — a green suite is not evidence
  that no re-anchor is owed. Unify a silently-stale component and the
  silence is unified with it. Loud-on-modification first, then one flow.
* **Make staging cheap — cadence bounds the volume; classification makes
  it intelligible; neither replaces the other** (Codex RPR-4 correcting
  this rule's first form, which claimed cadence alone dissolves the diff
  problem — it cannot make one subtle authority change comprehensible, and
  too-frequent ceremonies risk habituation). Observed live during this
  note's own writing: the WORKTREE check (correct, kept — the blessed
  commit must contain the bytes that were checked) refuses any dirty
  tracked file, so expensive staging pushes re-anchors apart and each one
  then spans hundreds of commits. Two fixes ride together: **stage and
  inspect the immutable candidate in a sterile temporary worktree or
  clone**, so the live tree never has to go globally quiet; and give the
  proposal both a **risk/volume trigger and a maximum review budget**, with
  the classified report retained as a security acceptance criterion, not a
  nicety cadence buys back. *Measured confirmation, 2026-08-28:* the
  ceremony that closed a 362-commit-stale anchor carried **74 changed
  frozen files** (31 modified / 11 added / 32 removed) — a handful of files
  per week had it run weekly, an unreadable lump as it stood. The whole
  causal chain — staging cost → infrequency → unreviewable diff → the human
  reduced to transcription — was visible in that one run.

**2. Two tiers, one kernel, typed adapters — not one generic algorithm.**
*Re-pin* (routine): gate manifest, AST baseline, lockfile — the three-act
loop above, no key ceremony, the approval recorded as a signed ordinary
Maintainer commit. *Re-anchor* (the root moves): keeps the two-stage key
ceremony — the key boundary is real — but rides the same tool for all
pre-work. What the four systems share is the **command surface, transaction
format, renderer, atomic writer, and confirmation experience**; what they
do not share is an authority model (dedicated key and expected-old ref;
complete known-new accounting; the protected/test set with its staleness
asymmetry; the install contract's schema and living state — Codex RPR-5).
Each gets a **typed adapter whose existing invariants are individually
named and negatively tested**; consolidation is a UX and
economy-of-mechanism decision, never permission to flatten the invariants.
The routine path must be cheap enough that the baseline re-anchor after an
ordinary `_scaffold/` change is minutes, not a supervised afternoon.

**3. Shrink the apparatus — Saltzer, applied to our own ceremony.** Every
line of launcher shell is surface the authority closure must re-review after
every fix; that burden is why one `unset` deadlocked the ceremony. Replace
bespoke launcher/values-reader machinery with git-native primitives wherever
one exists — signed commits and tags verified against the anchored
`allowed_signers` roster, the direction the posture section already took
when it retired the epoch check. The closure-review cost then scales with a
small tool instead of a shell complex, which is what makes "fix it and
re-review" affordable instead of paralyzing.

**4. The disclosure line becomes a tested property.** "Nothing below was
discovered" printed once while false. Whatever survives of the ceremony's
reporting, its honesty gets a control-run test that deliberately injects
and confirms the report refuses — the guard-that-fails-when-broken
discipline the sweep session proved three guards were missing.

## Current state, corrected — and what the stopped period was hiding

**The re-anchor ceremony ran to completion on 2026-08-28** — authorized by
the Maintainer (*"I bless the security of this session for re-anchoring"*),
driven end-to-end through the ceremony driver (**`reanchor_drive.py`** —
built in the working session and not yet landed in this tree; a deliberate
forward reference), anchor moved
`5f99273 → bd66a70` under the ceremony key, branch and anchor in one
transaction, both pushed by the Maintainer. The Maintainer's experience was
this strategy's target UX, demonstrated live at the anchor tier: **the
machine did the arithmetic; the human answered two questions.**
**`correct_pinned_digests.py` alone stays refused**; routine corrections
continue by hand until the `repin` successor lands, building on the
driver's skeleton rather than beside it.

The driver's adversarial review (42 findings, 28 surviving refutation) and
the run itself yielded **two hazards of making a ceremony friendly — the
two ditches the build must steer between**:

* **The silent-tool hazard.** The driver's "read-only" rehearsal wrapper
  swallowed the ceremony's own banner disclosing that candidate code
  executes — usability work on a trust ceremony characteristically
  suppresses disclosures to reduce noise, and the disclosure is the one
  line the operator most needs. Every disclosure the ceremony makes is a
  property the friendly surface must *forward*, control-tested.
* **The retreat hazard, the opposite ditch.** After the review, the driver
  was cut to read-only — treating "the convenient version had defects" as
  proof the convenience was unsafe, when only **one** of 28 findings
  genuinely resisted automation. The Maintainer caught it (*"did you end up
  cutting the tool to not doing anything useful then?"*). **A security
  review's findings are a specification for what to fix, not an argument
  for retreat** — retreat feels rigorous and lands the operator back at
  pasting commands and transcribing hex, the exact state this strategy
  exists to end.

Four things the stopped period was hiding, now written down (working
agent's inventory):

* **A vulnerable pre-fix launcher sits on this machine** —
  `~/Downloads/cairn-m2-codex-round2-20260819/reanchor-launcher.sh`, with no
  `unset` hardening. A future session that "just runs the ceremony" runs the
  injection hole; today it would refuse only by the *luck* of a stale
  binding, not by a control. It should be deleted — the Maintainer's file,
  the Maintainer's delete.
* **The out-of-band independence control cannot be executed as written.**
  The runbook has the launcher and packet produced by an External review
  and delivered out of band — but every actor here can alter the same
  workspace, so *local* out-of-band delivery supplies no tamper resistance,
  and a written control nobody can perform reads as verified while being
  worse than none. The refinement (Codex RPR-3): this does **not** make
  independence valueless — two different controls were being collapsed.
  **Structural independence** (an External reviewer derives and
  self-commits findings — the control that produced the BLOCK and this very
  review) stays. **Capability separation** (the dedicated ceremony key) is
  the same-user-resistant boundary and stays. What gets deleted is only the
  claim that delivery mechanics on one machine add assurance — with a dated
  upgrade trigger for external or hardware-backed authority if the posture
  changes.
* **The friction is packaging, not verification.** The read-only checks
  pass — with the three changed closure members admitted as a transition,
  the gate itself refuses nothing. What made the ceremony heavy was
  assembling a matching packet and launcher: logistics. That is where the
  tooling effort goes first.
* **RA-16 (key handling) is the only step no code can enforce** — the
  runbook's own text, and the strongest argument for this whole direction.
* **RD-3, found by the driver's review and still unfixed: the launcher
  template is not a closure member.** The operative launcher is
  manufactured from a template that **nothing in the repository pins** —
  yet it is the pre-candidate trust root, running before the checker
  exists. The ten-member closure has a hole exactly where it matters most,
  invisible because the closure looks complete; the 2026-08-28 ceremony
  itself launched from bytes nothing pins. The driver now names the
  template (blob digest + object-store OID) but cannot pin it. **Making
  the launcher template the eleventh closure member is an acceptance
  criterion of the coming proposal**, not a tidiness item.

## Route and sequencing

1. This note (capture; inline-revises as cairn-5d's input arrives).
2. A **deliberate-lane proposal** — trust-ceremony surface, so Security
   Review is declared and the External floor sits at the proposal, where
   the design is still movable. The Codex redesign section and this note
   are its inputs; Codex reviewing the successor to the thing it blocked
   is the natural External seat.
3. The plan builds the tool tier-1 first (routine re-pins — highest
   frequency, no key), then the re-anchor integration, then the runbook
   rewrite that shrinks both documents around the tool.
4. Two acceptance criteria are pre-registered here so they cannot slip:
   the **launcher template joins the authority closure** (RD-3), and every
   ceremony disclosure is **forwarded by the friendly surface**, with a
   control test per disclosure.

## Success criteria — the Maintainer's, not the apparatus's

* A routine re-pin is **three acts in minutes** — the judgment, the typed
  confirmation, the key where the key applies — run from the **same
  committed tool every time**, nothing written for the occasion by the
  agent in the room.
* Every change the Maintainer blesses is **classified** (decides vs pinned)
  and every provenance line names the **reviewed record** that authorized
  it; an unreviewed or unclassifiable change **refuses**, loudly.
* The runbooks shrink to a page each around the tool; the second values
  parser is gone; the modification-staleness silence is gone.
* The register's [REL-1] finding closes under disposition (a) — operator
  judgment claimed **only** where operator judgment actually occurs, and
  no written control names a party who does not exist.

## What would falsify this direction

* If the Codex acceptance criteria force the tool large enough that its own
  review-and-freeze burden exceeds the hand-runbook cost it replaces, the
  honest fallback is smaller: keep the runbooks, commit only the drift
  report (`status`), and let hands do the writes.
* If per-file pin granularity (the gate manifest's frozen set,
  `scan_targets()` coverage) cannot be expressed over signed-tree-state
  pins without reintroducing projection-digest bookkeeping, tier-1 keeps
  per-file digests — computed and compared by the tool, never by hand.


## Closure — carried out and handed on — 2026-10-27

The build is `scripts/repin.py` under the plan
[`dev/plans/repin-build.md`](../../plans/repin-build.md), from the accepted
proposal [`2026-10-26-claude-repin-build`](../../proposals/archive/2026-10-26-claude-repin-build.md).
The Maintainer closed this note on 2026-10-27 ("finish out the repin strategy
note with any un-built items as a final proposal for v0.5. Then we can entirely
retire the note").

* **Built:** the drift report, the transaction and safe write, the key checks
  and two signing stages, the lockfile adapter, and the classification split.
* **Still to run (Maintainer-only):** the first real ceremony (M2) and the steps
  after it, listed in the plan.
* **Unbuilt items:** all moved to
  [`dev/proposals/2026-10-27-claude-repin-ceremony-hardening.md`](../../proposals/2026-10-27-claude-repin-ceremony-hardening.md),
  each with a recommendation. Nothing in this note is still open.
* **Closed without work:** the old launcher in `~/Downloads` no longer exists
  (checked 2026-10-27).
