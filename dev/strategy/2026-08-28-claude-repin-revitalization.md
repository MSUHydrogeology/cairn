# Re-pinning, revitalized — one approval loop the Maintainer can actually run

**Author**: Claude (Strategy)
**Model**: Fable 5
**Date**: 2026-08-28
**Status**: open (cairn-5d's working-agent input requested 2026-08-28; folds
in on arrival)
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

**What the Maintainer attests** — three acts, one breath: *I read the
provenance panel and every changed file traced to a reviewed record; I
compared the digest the tool showed against one I computed myself; I chose
this moment to move the pin.* Digest comparison is what signature
verification reduces to for every operator on earth — the register says so —
and checking that *reviews exist* is a judgment a non-specialist genuinely
can make. Re-auditing the reviewed changes is not, and the redesigned
ceremony must stop pretending to ask for it: **the semantic assurance comes
from the lifecycle reviews that landed the changes, and the ceremony's job
is to prove linkage to them, not to repeat them.** That is what makes the
human leg real instead of a relay: the operator attests exactly what they
verified, nothing more, and the claim matches the act.

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

The Codex redesign requirements are inherited **verbatim as acceptance
criteria**: closed JSON-native plan binding exact input *and* output bytes;
re-derivation in a fresh process from verified checker bytes; the AST
runbook's complete-set guard preserved; git errors fail closed rather than
collapsing to "untracked". The tool joins the protected set, so the previous
pin covers the tool that moves the next one.

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

## What stays true while this is built

Both stops stand: the gate-anchor ceremony does not run, and
`correct_pinned_digests.py` stays refused. Corrections continue by hand
under their runbooks — slower and honest. The three changed closure files
are not re-reviewed under the *current* apparatus unless a ceremony is
genuinely needed before the redesign lands; paying closure-review cost on
machinery this note proposes to replace is the wrong spend, and that call is
the Maintainer's.

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

* A routine re-pin is **three acts in minutes**, describable in one breath,
  run from the **same committed tool every time** — nothing written for the
  occasion by the agent in the room.
* Every digest the Maintainer confirms is one they **computed
  independently**; every provenance line names the **reviewed record** that
  authorized the change; an unreviewed change **refuses**, loudly.
* The runbooks shrink to a page each around the tool.
* The register's [REL-1] finding closes under disposition (a) — operator
  judgment claimed **only** where operator judgment actually occurs.

## What would falsify this direction

* If the Codex acceptance criteria force the tool large enough that its own
  review-and-freeze burden exceeds the hand-runbook cost it replaces, the
  honest fallback is smaller: keep the runbooks, commit only the drift
  report (`status`), and let hands do the writes.
* If per-file pin granularity (the gate manifest's frozen set,
  `scan_targets()` coverage) cannot be expressed over signed-tree-state
  pins without reintroducing projection-digest bookkeeping, tier-1 keeps
  per-file digests — computed and compared by the tool, never by hand.
