# The fold-back ledger — how a deployment improves Cairn

Cairn is extracted from a reference instance, but improvement is not
one-directional. A *deployment* — any team running the Cairn methodology
— accretes operating doctrine of its own: a failure mode it hardened
against, a coordination rule it sharpened, a review pattern that earned
its keep. Some of that is **generalizable** — it would help any
differently-shaped team — and should flow *back up* into Cairn so every
adopter gets the proven version. The **fold-back ledger** is the standing
mechanism that carries it.

This is the deployment-side **push**. It complements the framework-side
**pull** — the reference-instance doctrine harvest (`rationale.md` > "The
reference-instance doctrine harvest"), where Cairn periodically diffs a
mature deployment against core. The harvest is run by the framework on a
cadence; the ledger is maintained by the deployment, continuously. The
two feed the same destination — a Cairn proposal — and the ledger is the
harvest's recording surface as well.

## The ledger artifact

A deployment keeps a fold-back ledger — a single tracked file (the
default install puts it under the deployment's `dev/upstream/`) — listing
candidates bound for Cairn. A candidate is a generalizable improvement
noticed *here* that should be ported *up*. The ledger is the holding pen
between the moment a candidate is noticed and the moment a Cairn proposal
picks it up; without one home, candidates rot scattered across the
roadmap or are lost at session handoff.

**What belongs**: generalizable doctrine or a net-new Cairn-side
improvement. The test — borrowed from the harvest — is *would a
differently-shaped team hit the same need?* Deployment-local quirks (a
project's own tools, naming, science) do **not** fold back.

## Lifecycle

Each candidate moves through four states:

1. **Capture.** When work surfaces something Cairn-portable, add a row
   (and a short detail entry). Status `candidate`. Capture is cheap and
   continuous — the nightly goodnight foldback-check (below) is when it
   reliably happens.
2. **Queue.** When a sync is agreed (the framework's cadence, or a
   maintainer call), the chosen candidates flip to `queued`.
3. **Sync.** A Cairn proposal ships the change. The finding is
   *deliberated* through Cairn's own lifecycle — the ledger feeds the
   lifecycle, it does not bypass it.
4. **Record.** On ship, the row moves to an "already-synced" record (or
   is deleted once the archived Cairn proposal carries the durable
   record).

### Status vocabulary

* `candidate` — captured; not yet committed to a sync.
* `queued` — selected for the next sync.
* `scoped → <proposal/milestone>` — a tracked Cairn proposal has taken
  it over.
* `synced` — shipped into Cairn (transient; the row then moves to the
  already-synced record or is deleted).
* `dropped` — decided not to port, with a one-line reason.

### Removal rule

A row is deleted once its change is `synced` **and** the archived Cairn
proposal carries the durable record; a `dropped` row is deleted with its
reason captured in the commit. The *open-candidate* set is the ledger's
load-bearing content; the already-synced record is a terse cadence log,
so it never becomes a second, less-governed roadmap.

## Capture cadence — the nightly goodnight check

Capture is a **standing step in the goodnight routine**
(`session-routines.md`): every goodnight, the deployment scans the
session-day's doctrine activity for Cairn-portable candidates and
captures each in the ledger. Capturing never lapses — a portable rule
proven today should not reach tomorrow uncaptured. An **empty capture is
success** (mirroring the harvest's "an empty sweep is success"); never
manufacture marginal candidates to justify the step. Whether to *open a
sync* is the separate, judgment-gated decision the harvest cadence
governs — capture is standing, the sync is judged.

## The export boundary — scrub before anything goes up

A fold-back ledger is a **cross-repository export surface**: content
flows from a deployment's own repository — which may be private or
proprietary — *up* to public Cairn. That makes it a privacy surface, and
the same rule applies as to any coordination artifact (`coordination.md`
> "Privacy"): **ledger candidates carry no secrets, credentials, internal
hostnames or IP addresses, local machine paths, or proprietary domain
detail.** Two controls:

* The ledger template carries a prominent **`[SECURITY WARNING]`** stating
  the no-leak rule, so the constraint is visible at the point of capture.
* Before any ledger item becomes a public Cairn proposal, the
  **Maintainer confirms** no private coordinate leaks — a
  scrub-and-verify gate at the upstream-submission step. The
  export boundary is where the gate bites, not local capture; an item
  captured locally is scrubbed before it crosses to public Cairn.

## Adaptation

The mechanism is part of every deployment by default (the
`fold-back-ledger` module is default-on), because the improvement loop is
the methodology's whole premise. A solo, single-deployment adopter that
will never fold doctrine back up may omit the module (the documented
opt-out) — but the cost of keeping it is one mostly-empty file and a
cheap nightly glance, and the payoff is that a generalizable improvement
is never silently lost.
