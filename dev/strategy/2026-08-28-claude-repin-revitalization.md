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
* **Make staging cheap, because the infrequency and the opacity are the
  same problem.** Observed live during this note's own writing: the
  ceremony's WORKTREE check (correct — the blessed commit must contain the
  bytes that were checked) refuses any dirty tracked file, so the ceremony
  needs a globally quiet repository. Expensive staging pushes re-anchors
  apart; each one then covers hundreds of commits; and an enormous diff is
  exactly what no classification can make comprehensible. The causality
  runs staging-cost → infrequency → opacity, so cadence is a *design goal*,
  not a nicety: **a re-anchor cheap enough to run weekly largely dissolves
  the diff problem on its own.** Keep the WORKTREE check; shrink everything
  around it until quiet-repository moments are easy to find.

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

## Review -- Codex (External) -- 2026-08-28

> **Temporary strategy review.** Fold accepted substance into the note inline,
> then remove this section as `dev/strategy/_template.md` requires.

**Reviewed commit**: `9450676340b02b724cd20e626515c0679bdd52a3`
**Role**: External strategy reviewer
**Target**: the strategy note at the named commit, before proposal promotion
**Verdict**: **REVISE BEFORE PROMOTION**

### Steelman

The direction is worth pursuing. The present ceremony asks a solo Maintainer to
perform arithmetic and packaging through instructions assembled by an agent,
then describes some of that relay as independent human assurance. A same-account
terminal prompt cannot establish who typed, and re-running `shasum` under the
same account supplies no independent trust root. Deleting those claims is more
secure than preserving a control that cannot be performed. A Git commit also
offers a much stronger state-binding primitive than the blocked runner's small
JSON projection: its signature covers the commit object, whose tree and parent
identify exact repository states. Finally, cheaper ceremonies would reduce the
amount a person must inspect at once.

The note should become a proposal after it separates those sound observations
from three stronger conclusions that do not yet follow.

### Findings

1. **[RPR-1] HIGH -- discarding fresh-process derivation is based on a false
   equivalence, and contradicts the note's own machine contract.**

   The rejected redesign item is not a second parser or a second implementation.
   It is the same derivation executed from separately verified checker bytes in
   a fresh process. The blocked runner demonstrated why that matters:
   `config.py` changed between A and B, but the second derivation reused the
   first import from `sys.modules` and produced the same digest. Same OS user is
   relevant to identity and containment; it does not concede stale module state,
   candidate-code execution, or a checker/input substitution.

   The note still promises that A and B are "independent" and "freshly
   computed" at lines 80-82, while lines 137-140 discard the only named
   mechanism that supplies that property. Lines 126-128 also retain the claim
   that the Maintainer computed a digest independently after lines 88-91 call
   that act fiction.

   The proposal should choose one coherent design. Either run one implementation
   twice in fresh, sterile processes from pinned bytes, or replace A/B entirely
   with one immutable transaction object: bind every input and exact output,
   render that object, perform no later live or candidate read, and apply it only
   through exact-preimage compare-and-swap. The latter can be simpler, but then
   the note must delete the A/B independence claim rather than claim it was
   retained. Removing the launcher's second values parser is compatible with
   either choice; process freshness does not require a second grammar.

2. **[RPR-2] HIGH -- whole-tree signing closes the demonstrated projection only
   under a narrower contract than "complete preimage," and the manifest remains
   policy authority.**

   A signed Git commit binds its parent and complete tracked tree. That prevents
   the blocked runner's exact failure -- carrying an undigested kept record into
   a different output tree -- if the authorized operation consumes only those
   immutable objects. It does not, by itself, bind untracked or ignored inputs,
   host executables and configuration, interpreter state, candidate code run to
   derive collection evidence, filesystem path/symlink identity, or any live
   read performed after the signed object was shown. Those are all part of the
   preimage when they influence a result.

   Nor does calling the protected-set manifest a lint make it non-authoritative.
   The rule that says which files "decide," which drift refuses, and when the
   rule itself may change is policy authority even if it is no longer the
   cryptographic authenticity root. The safe form is to derive that rule from
   the prior trusted state and separately authorize any rule transition. A
   subset signature is not automatically the old projection defect: it is safe
   when the prior trusted rule proves that the subset exactly equals the
   operation's complete read/write footprint. Whole-tree signing is a useful
   conservative alternative, not a proof that selection has disappeared.

   Before promotion, define the signed transaction precisely: operation and
   schema; input parent/commit and tree; output commit and tree; exact target
   paths with old/new object identities; checker/tool identity; the classified
   report or its digest; expected-old ref; and every non-tree input that can
   influence derivation. Verification must use a pinned principal and must end
   in an expected-old compare-and-swap. The proposal should say explicitly that
   signing authenticates a key holder, not the process that requested the
   signature.

3. **[RPR-3] HIGH -- deleting false authentication is right; deleting every
   independence claim, and calling a typed token authorization, is not.**

   The note correctly concludes that a TTY and a same-account checksum do not
   authenticate the Maintainer. It should delete the current runbook's claim
   that local out-of-band delivery supplies tamper resistance when every actor
   can alter the same workspace. But two different controls are being collapsed:

   * structural independence -- an External reviewer derives and self-commits
     findings or exact hashes, which can catch design and implementation error;
   * capability separation -- a key, account, device, or external channel that
     the executing agent cannot use, which can resist same-user substitution.

   Cairn has the first and should keep it. The dedicated ceremony key may supply
   the second during re-anchor only if the Maintainer alone can unlock it and it
   is absent while candidate code runs. The ordinary signing key does not supply
   it under the recorded posture in which agents commit with that key.

   A typed digest without an authenticated principal is a confirmation and an
   intent record, not an enforceable authorization boundary. Use that honest
   name. State separately that the current trusted-contributor, solo-machine
   posture accepts same-user substitution; name the dedicated key as the actual
   re-anchor capability; and leave a dated upgrade trigger for an external or
   hardware-backed authority if the threat model changes. "Delete the false
   claim" is sustained. "One party makes independence valueless" is not.

4. **[RPR-4] MEDIUM -- cadence reduces volume but cannot replace semantic
   presentation, and a shared dirty worktree need not govern cadence.**

   The claimed 362-commit range does not reproduce at the reviewed commit:
   `git rev-list --count refs/cairn/gate-anchor..9450676` returns **365**. More
   importantly, weekly cadence does not make one subtle authority change
   comprehensible, while a well-classified report can make a longer mechanical
   range tractable. Frequency and presentation are complementary controls:
   cadence bounds volume; classification, provenance, exact old/new state, and
   consequence rendering make the bounded material intelligible. Too-frequent
   ceremonies also risk habituation.

   Keep cheap cadence as an operational goal, but do not say it dissolves the
   diff problem on its own. Give the future proposal both a risk/volume trigger
   and a maximum review budget, with the report design retained as a security
   acceptance criterion. Also test the simpler architectural answer to the
   global-quiet-tree problem: prepare and inspect an immutable candidate in a
   sterile temporary worktree or clone. The live-worktree refusal is sound, but
   it need not force every concurrent session to become quiet.

5. **[RPR-5] MEDIUM -- one user loop should not erase four different source
   invariants.**

   The gate anchor, gate manifest, AST baseline, and install lockfile can share
   a command surface, transaction format, renderer, atomic writer, and
   confirmation experience. They do not share an authority model. The gate
   anchor moves a trust root under a dedicated key and expected-old ref; the AST
   baseline requires complete known-new accounting; the gate manifest defines a
   protected/test set and has asymmetric stale-state behavior; the lockfile is
   the install contract and has schema and living-state rules. The proposal
   should specify a small common kernel plus typed adapters whose existing
   invariants are individually named and negatively tested. "One tool" is a UX
   and economy-of-mechanism decision, not permission to reduce them to one
   generic protected-set algorithm.

### Central adjudication

* **Delete same-account authentication and local out-of-band tamper-resistance
  claims:** **YES**, while retaining structurally independent review and the
  dedicated-key boundary.
* **Discard redesign item 2 as a second parser:** **NO**. Either preserve fresh
  execution of one implementation or replace A/B with a fully specified
  immutable transaction; the present text does neither consistently.
* **Whole-tree signature plus manifest lint kills the projection class:**
  **CONDITIONALLY** for tracked Git state, once the complete influence set and
  prior-trusted policy rule are explicit. It is not yet a complete-preimage
  design.
* **Cadence makes diffs comprehensible:** **NO as stated**. Cadence is volume
  control; semantic presentation remains the comprehension control.

### Coverage

**Examined and exercised:** the exact strategy bytes at `9450676`; the complete
2026-08-27 External Security Review and its reproduced CPD-1 through CPD-8
record; `bootstrap/REANCHOR_RUNBOOK.md` including RA-01 through RA-19, the
out-of-band launcher/packet contract, same-user residual, signing posture, and
first-use bootstrap; [REL-1] in the live security strategy; the registered step
output from `sh bootstrap/reanchor.sh steps`; current anchor identity and commit
count; and the commit history that introduced the note's four design rules and
cadence rule. The runbook's 615 lines, AST runbook's 182 lines, and 19 registered
acts reproduce.

**Not examined:** `scripts/reanchor_drive.py` is untracked at the reviewed
commit and remains uncommitted in the working tree. I did not treat claims about
its three-way report, rehearsal, questions, or adversarial review as evidence.
I did not run a re-pin, re-anchor, signing operation, full suite, or destructive
probe, and I did not review the future proposal or an implementation of the
proposed transaction format.
