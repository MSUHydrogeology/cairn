<!-- claim-check-allow: scripts/foldback_export_scan.py, scripts/foldback_suggest.py -->
<!-- Both paths refer to the adopter-install location -- the
     foldback_export_scan + foldback_suggest modules verbatim-install
     into `<target>/scripts/` (parallel to claim_check + lifecycle_metrics).
     The doctrine cites them by adopter-install path because that is the
     invocation context the protocol asks the adopter for.  From
     Cairn's own checkout these paths do not resolve (the source-of-truth
     templates live at `templates/modules/default-on/`); exempted so the
     adopter-facing cite stays correct. -->

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
default install puts it under the deployment's `dev/.cairn/`) — listing
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
* `filed → <issue-#>` — a Cairn issue has been filed (via the
  active-surfacing protocol below); the candidate is now in
  Cairn's triage / discussion surface, **not yet accepted into a
  tracked proposal**. Transient pre-acceptance state.
* `pr → <pr-#>` — a Cairn PR has been opened (active-surfacing
  protocol with deployment-side working code to contribute);
  same pre-acceptance position as `filed`.
* `scoped → <proposal/milestone>` — a tracked Cairn proposal has taken
  it over. (A `filed` or `pr` row transitions to `scoped` only when
  a Cairn-side maintainer Decision creates the tracked surface.)
* `synced` — shipped into Cairn (transient; the row then moves to the
  already-synced record or is deleted).
* `dropped` — decided not to port, with a one-line reason.

A row carrying an optional `deferred-until <ISO-date | condition>`
field is snoozed: the active-surfacing protocol skips that row until
the date elapses (the maintainer evaluates the condition string at
surfacing time -- the string is a memo, not machine-parsed).

**Migration rule** — existing ledger entries using older vocabulary
(without `filed` / `pr` / `deferred-until`) remain valid. The new
states are **additive**; the surfacing protocol only modifies the row
it files, never rewriting other rows. An adopter with an existing
ledger does not need to retroactively re-status rows when this
doctrine update lands. Tooling that reads the ledger (e.g.
`foldback_suggest.py`) handles both vocabularies gracefully — only
`candidate` status surfaces, regardless of which other states are
present.

### Removal rule

A row is deleted once its change is `synced` **and** the archived Cairn
proposal carries the durable record; a `dropped` row is deleted with its
reason captured in the commit. **A `filed` or `pr` row remains in the
open-candidate set** until it transitions to `scoped`, `synced`, or
`dropped` — it is a pre-acceptance pending state, not a sync. The
*open-candidate* set is the ledger's load-bearing content; the
already-synced record is a terse cadence log, so it never becomes a
second, less-governed roadmap.

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

## Active surfacing — from capture to suggested filing

**Active surfacing is the bridge between capture and sync.** The
capture cadence (above) reliably records candidates; the harvest
cadence and the maintainer judge when to *open a sync*. Between those,
a candidate sits in the ledger — *captured but unfiled*. The active-
surfacing step closes that gap: each `candidate`-status row is, at
standing cadence, surfaced to the deployment maintainer with concrete
filing options — file as a Cairn issue (for a well-shaped idea that
wants Cairn-side discussion), draft as a Cairn PR (for an idea the
deployment is ready to ship), defer (with a `deferred-until` value),
or drop.

**Why this is part of Cairn's methodology, not just adopter
convenience.** Cairn improves through community contribution. The
dominant barrier to OSS contribution in the literature is the
**"where do I start?"** friction Steinmacher et al. 2016 documented
(FLOSScoach, ICSE 2016); the Nakakoji et al. 2002 onion model
("Evolution patterns of open-source software systems and communities,"
IWPSE 2002) names the outer-to-inner transition — passive user /
deployment maintainer → active contributor — as the bottleneck. An
agent that has *already read the deployment's ledger entries* is a
personalized in-context FLOSScoach. The active-surfacing step is
therefore not a UX nicety; it is the mechanism by which Cairn builds
its own contributor pipeline through every deployment that adopts it.

**Trigger — standing**: at goodnight, the foldback-capture step
extends into a foldback-surfacing step (see `session-routines.md` +
the `fold-back-ledger` module's merge). The goodnight owner reviews
each open `candidate`-status row that is not currently snoozed via
`deferred-until`, and applies a **grace-period judgment** -- the
default convention is seven days (floors very-fresh candidates
against churn); the maintainer reads each row's Source field for its
captured date and decides per-row whether to surface or skip.  The
grace period is intentionally a **maintainer judgment**, not a
machine-enforced gate: ledger rows do not currently carry a
structured `captured: <ISO-date>` field, and adding one would be a
separate schema-and-doctrine arc.  The current ledger schema records
the capture date inline within the Source field; the maintainer
reads it at surfacing time.

**Trigger — on-demand**: a deployment-installed helper
(`scripts/foldback_suggest.py`, if the deployment installs Cairn's
optional helper module) lists all open candidates with their detail
entries, callable any time the maintainer wants to review the funnel
state.  The helper is a `candidate`-status + `deferred-until` filter
only -- it does not enforce the grace-period judgment (see above);
the maintainer applies that judgment by reading each surfaced row's
Source field.

### Protocol

The agent reads the row's detail entry and walks the maintainer
through six steps:

1. **Recap**: state the candidate, why it is generalizable, and
   cite the deployment commit(s) that prove it.
2. **Choose a filing path**: issue (most common; discussion-shape),
   PR (when the deployment has working code to contribute), defer
   (record a `deferred-until` ISO date or condition string), or
   drop (with one-line reason).
3. **Compose**: for issue / PR, the agent drafts the body from the
   row + the Cairn issue / PR template; the maintainer reviews +
   edits.
4. **Scrub** — *fail-closed machine gate*. The agent writes the
   drafted body to a local **gitignored** temp file (working
   convention: `dev/.cairn/.foldback-draft-<timestamp>.md`), then
   invokes the export-scrub scanner:

       python scripts/foldback_export_scan.py <draft-path>

   The scanner exits 0 clean or non-zero with per-finding output.
   **Non-zero exit fails closed** — the maintainer dispositions the
   findings (edit the draft to resolve; mark a documented false
   positive in the draft; or abort the filing).  The agent does not
   negotiate the gate.  In addition, the agent asks the maintainer
   to explicitly **affirm the two manual-only no-export classes**
   (unpublished data hints; proprietary domain detail in long-form
   prose) — the affirmation is recorded in the issue/PR template's
   signed checkbox.
5. **Submit**: the maintainer submits the issue / PR **by hand** via
   `gh issue create --body-file <draft.md>` (or the GitHub UI).
   **The agent does not submit autonomously.** Bright-line: only the
   maintainer crosses the export boundary.
6. **Record**: on submission, the row's status flips from `candidate`
   to `filed → <cairn-issue-#>` or `pr → <cairn-pr-#>`. Existing
   lifecycle handles the rest (the row stays in the open-candidate
   set until a Cairn-side Decision transitions it to `scoped`,
   `synced`, or `dropped`).

### Anti-patterns

* **Filing every `candidate` automatically** — the maintainer judges
  per-row; surfacing is the *prompt*, not the action.
* **Bypassing the scrub gate at the agent's discretion** — the gate
  is unconditional and fail-closed; the agent does not negotiate it,
  and the maintainer's disposition of a finding is documented in the
  draft body, not silent.
* **Aggregating multiple candidates into one filing** — one filing
  per candidate (a Cairn maintainer reviews one idea at a time).
* **The agent submitting the filing directly** — only the maintainer
  submits.  This is the structural guard on the export boundary.
* **Surfacing a snoozed row** — rows with a `deferred-until` value
  in the future are skipped until the deferral expires.

## The export boundary — scrub before anything goes up

A fold-back ledger is a **cross-repository export surface**: content
flows from a deployment's own repository — which may be private or
proprietary — *up* to public Cairn. That makes it a privacy surface, and
the same rule applies as to any coordination artifact (`coordination.md`
> "Privacy"). **The no-export class enumeration is structured into
two tiers** — machine-gated (regex-detectable) + manual-affirmation
(human-judgment), matching the actual structure of the boundary:

**Machine-gated classes (5; detected by `scripts/foldback_export_scan.py`,
fail-closed during the active-surfacing scrub step)**:

* **Credentials / secrets** — assignment-pattern detectable
  (`password = ...`, `api_key = ...`, `secret = ...`, `token = ...`).
* **Private filesystem paths** — `/Users/<name>/`, `/home/<name>/`,
  `C:\Users\<name>\`, `/private/`, `/var/folders/`, and similar
  user-scoped absolute paths.
* **IP addresses (deployment-internal AND remote-repo)** — IPv4 +
  IPv6, with an RFC 5737 documentation-IP allowlist (192.0.2.0/24,
  198.51.100.0/24, 203.0.113.0/24) so doc examples don't trigger.
  Both deployment-internal IPs *and* IPs the deployment's remote
  repo would expose qualify.
* **Internal hostnames** — `.local`, `.internal`, `.lan`, plus
  RFC 1918 ranges covered via the IP detector.
* **Adopter-configurable proprietary tokens** — a deployment-side
  allowlist file enumerating project codenames, client names, and
  domain-specific terms the adopter does not want exported.

**Manual-affirmation classes (2; maintainer-signed in the issue/PR
template's affirmation field)**:

* **Unpublished data hints** — long-form prose context that no
  regex can reliably distinguish from generic phrasing (e.g.,
  "the client's marina sediment data" versus generic "sediment
  data").
* **Proprietary domain detail** — descriptive prose about
  client / project specifics that the deployment maintainer
  recognizes as private but a scanner cannot.

Two controls:

* The ledger template carries a prominent **`[SECURITY WARNING]`** stating
  the no-leak rule, so the constraint is visible at the point of capture.
* Before any ledger item becomes a public Cairn issue / PR / proposal,
  **two gates fire together**: the machine-gated scrub (above) runs
  fail-closed against the drafted body, AND the maintainer signs the
  manual-affirmation field. The export boundary is where both gates
  bite, not local capture; an item captured locally is scrubbed before
  it crosses to public Cairn.

## Adaptation

The mechanism is part of every deployment by default (the
`fold-back-ledger` module is default-on), because the improvement loop is
the methodology's whole premise. A solo, single-deployment adopter that
will never fold doctrine back up may omit the module (the documented
opt-out) — but the cost of keeping it is one mostly-empty file and a
cheap nightly glance, and the payoff is that a generalizable improvement
is never silently lost.
