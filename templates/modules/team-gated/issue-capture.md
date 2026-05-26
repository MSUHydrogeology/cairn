# Module: issue-capture

**Selected when:** the team **uses an issue tracker** to capture
gaps and friction — the surface the User Agent role (`roles.md`)
writes to. A team that tracks nothing, or tracks only in the
deliberation record, does not need it; a team with a tracker gets a
standing capture discipline so friction becomes a recorded issue
rather than a lost remark.
**Adds to:** the role roster note for the User Agent in
`dev/agent_collaboration.md`, plus tracker-agnostic issue templates
in the adopting repository.

The User Agent "captures friction as issues," but without a capture
surface that is just an instruction. This module supplies the
surface — issue structures, a capture-vs-fix rule, and a fallback
for when the tracker is unreachable — **without naming a specific
tracker.**

## Template content

### Issue structures (tracker-agnostic)

Three structures cover the capture surface. They are field lists,
not a specific tracker's form — an adopter maps them onto whatever
tracker they run:

* **Bug report** — what was observed vs. expected; the exact
  reproduction steps; the system context (OS, versions, data
  inputs); the affected surface; severity.
* **Feature request** — the user-seat need; the workflow it would
  unblock; the rough shape of a solution (not a design); who asked.
* **Friction note** — a smaller-than-a-bug observation: something
  that was confusing, slow, or surprising during real use. The
  User Agent's most common output; cheap to file, valuable in
  aggregate.

Labels are the project's classification axes (area, severity, kind)
— **labels-as-axes**, mapped to the tracker's label system by the
adopter.

### Capture vs. fix inline

A standing rule keeps the channel useful: **capture friction as an
issue rather than fixing it inline mid-session**, unless the fix is
trivial and in-scope for the current work. Inline fixes to
unrelated friction scatter the work and escape review; an issue
preserves the signal for triage on its own cadence. The exception
is the genuinely one-line, on-path fix.

The rule binds the User Agent's **debug-from-the-user's-seat** mode
especially (`roles.md` > User Agent): reproducing and diagnosing a
failure from real use is the User Agent's job, but the *fix* — once it
exceeds a trivial, in-scope correction — is captured and routed to the
surface's owning implementer, not landed mid-diagnosis. A diagnosis is
a strong issue (reproduction + root cause); it is not a licence to
re-decide the owning surface's design.

### Tracker-unavailable fallback

When the issue tracker is unreachable (auth, network, an outage),
capture does not stop: the agent records the would-be issues in a
local scratch surface — each with its reproduction, context, and
proposed labels — so they can be filed when the tracker returns or
surfaced to the Maintainer for manual filing. A captured-but-unfiled
issue is recoverable; an uncaptured one is lost.
