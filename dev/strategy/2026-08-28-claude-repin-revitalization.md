# Re-pinning, revitalized — one approval loop the Maintainer can actually run

**Author**: Claude (Strategy)
**Model**: Fable 5
**Date**: 2026-08-28
**Status**: open (working-agent input from the sweep/ceremony session folded
in 2026-08-28 — it corrected this note's state, replaced one of its three
human acts, and supplied four design constraints and four hidden hazards)
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
artifacts cover those commits; that the A and B derivations are
independent, complete-preimage, and freshly computed; that writes are
atomic, contained, and read back.

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
2. **The typed confirmation** — an *authorization act, explicitly not an
   authentication claim* (Codex item 3, as amended by the working agent:
   under one human, one machine, one OS user, a tool can authenticate
   nobody, and the honest fix is deleting the claim, not strengthening the
   check).
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
  digest they computed independently; atomic contained writes with
  read-back; no `--authorize`, no non-interactive path to the human act.

The Codex redesign requirements are inherited **as triaged by the working
agent, not verbatim**: items (1) and (5) without reservation — the closed
JSON-native plan binding exact input *and* output bytes (the fix to the
whole projection class), and public-path tests for every reproduced failure
*including controls proving a guard has not become refuse-all* (the
discipline this repo failed three times in one session). Item (3) amended —
typed confirmation as authorization, the authentication claim deleted. Item
(2) — fresh-process re-derivation from separately verified checker bytes —
**discarded as written**: it is the two-parser design again, it defends a
line the same-user posture already concedes, and it costs a second
implementation of everything. The AST runbook's complete-set guard is
preserved; git errors fail closed. The tool joins the protected set, so the
previous pin covers the tool that moves the next one.

Four constraints from the working agent's attack on this note's first
draft, adopted as design rules:

* **Sign the complete preimage; demote the protected set from attested to
  derived-and-linted.** A signed commit kills the projection class because
  the tree hash covers every byte — but sign the whole tree and every prose
  commit becomes an authority act; sign a subset and the projection is
  reinvented. The resolution: the *signature* binds the whole tree, and the
  manifest survives as a **check** (a lint that says which files decide),
  never as the authority. Left implicit, the manifest quietly survives as
  authority and nothing improves.
* **Classify before showing.** A diff of 362 commits is not comprehensible
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

**2. Two tiers, not four ceremonies.** *Re-pin* (routine): gate manifest,
AST baseline, lockfile — the three-act loop above, no key ceremony, the
approval recorded as a signed ordinary Maintainer commit. *Re-anchor* (the
root moves): keeps the two-stage key ceremony — the key boundary is real —
but rides the same tool for all pre-work, and its human step becomes the
same three acts plus the key. The routine path must be cheap enough that
the baseline re-anchor after an ordinary `_scaffold/` change is minutes,
not a supervised afternoon.

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

**The gate anchor is no longer stopped.** The Maintainer, in the working
agent's session, verbatim: *"We don't need to re-review everything. I bless
the security of this session for re-anchoring. Let's go ahead with the
ceremony."* That ceremony is executing there. **`correct_pinned_digests.py`
alone stays refused**; routine corrections continue by hand under their
runbooks until the successor lands.

The working agent is building **`scripts/reanchor_drive.py`** on exactly
this note's principle — the machine does the arithmetic, the closure prints
three ways so the transition is visible at a glance, a free read-only
rehearsal runs before any key or package is spent, and the human is asked
exactly two questions: *does this report describe what you intend to bless?*
and *is the key loaded?* It is under adversarial review now. It is the
concrete tier-*anchor* instance of this strategy; the routine-tier `repin`
tool builds on the same skeleton rather than beside it.

Four things the stopped period was hiding, now written down (working
agent's inventory):

* **A vulnerable pre-fix launcher sits on this machine** —
  `~/Downloads/cairn-m2-codex-round2-20260819/reanchor-launcher.sh`, with no
  `unset` hardening. A future session that "just runs the ceremony" runs the
  injection hole; today it would refuse only by the *luck* of a stale
  binding, not by a control. It should be deleted — the Maintainer's file,
  the Maintainer's delete.
* **The out-of-band independence control cannot be executed by anyone
  here.** The runbook has the launcher and packet produced by an External
  review and delivered out of band so the candidate's preparer is not its
  attester — but this posture has one party. A written control nobody can
  perform is worse than none, because it reads as verified. The redesign is
  a **one-party ceremony, honestly**: delete the claim, keep the review.
* **The friction is packaging, not verification.** The read-only checks
  pass — with the three changed closure members admitted as a transition,
  the gate itself refuses nothing. What made the ceremony heavy was
  assembling a matching packet and launcher: logistics. That is where the
  tooling effort goes first.
* **RA-16 (key handling) is the only step no code can enforce** — the
  runbook's own text, and the strongest argument for this whole direction.

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
