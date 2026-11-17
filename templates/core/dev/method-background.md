# Cairn method background

Loaded rules remain authoritative.

## Testing-discipline background

### Module: testing-discipline

Cairn requires a change to **absorb its tests** (the lifecycle's
implement-with-tests step), but does not, on its own, say *how the test
suite is organized* or *how large it should grow*. Without a scheme, "add
a test" lands wherever, tiers blur, and every change adds tests while none
are removed. AI agents make this worse: writing a test costs them little,
and a reviewer more often asks for a missing test than questions an extra
one. This module gives the suite a shape, a way to choose tests, and a
budget.

The guidance below is a practical summary, not a complete testing curriculum.

> **Worked contrast: a pin and a promise.** Before, a change-specific test
> might freeze an internal detail of the water-budget example:
>
> ```python
> import water_budget
>
> def test_flux_order_is_stable():
>     assert water_budget._FLUX_COLUMNS == (
>         "precip_mm", "et_mm", "runoff_mm", "recharge_mm")
> ```
>
> That test fails on a harmless refactor. After, use the promise-shaped
> `examples/scientific-minimal/test_water_budget.py`: its module docstring
> states the mass-balance promise, and tests check `compute_residual`, input
> preservation, the writer round trip and the public `main` result. Its
> independent synthetic row checks P=100, ET=30, runoff=20, recharge=40 and
> dS=10 mm; closure alone is not treated as proof that the inputs were
> preserved. The example has no private reach in `scripts/test_coupling.py`.

> **Worked useful/vacuous/broken contrast.** For a synthetic monthly row,
> predeclare P=100, ET=30, runoff=20 and recharge=40 mm; the stated balance
> gives dS=10 mm. A producer fault that changes output P to 110 and dS to 20
> still balances at residual 0, so closure alone is vacuous evidence of input
> preservation. An independent check of P=100 and dS=10 rejects the altered
> row. This checks row preservation only, not physical validity. In ordinary
> code, a truthiness check on `greet("Ada")` passes when the name is ignored;
> `greet("Ada") == "Hello, Ada!"` fails and exposes the fault. Observe it fail
> before fixing behavior; fix the behavior, not the expected value.

optional architecture review is available, not required for every change.

### Module: testing-discipline — continued

**test-tier scheme** rather than an undifferentiated `tests/` pile. Broadly
applicable; team-gated so a preset (`governance presets`) turns it on for the
profiles that warrant it rather than every adoption paying for it by default.

A tier communicates broad scope; the test name and assertions show its specific
behavior.

A test's tier is determined by where it lives (its directory, or a per-tier
configuration that maps file names to tiers), applied automatically -- authors do
not hand-tag each test, and a check fails when a test has no tier, so the scheme
cannot rot.

(valid and malformed input; dry and saturated cell; laminar and turbulent flow)

(zero, empty, one, the threshold, a sign change)

More examples inside a regime rarely find new faults.

(conservation, symmetry, a round trip (`load(save(x)) == x`), a known limit)

A golden output is a change detector: it fails on every harmless change and says
nothing about whether the result is right.

The removed optional detail was: “sample or generate varied cases to probe a
stated invariant.”

The contract-test sentence ended: “changes -- the change then has to be
deliberate.”

Scope and cost are separate: choose a tier by what a test covers, and record its
runtime on its own.

The removed sentence ending was: “in, so the suite's shape stays legible as it
grows.”


## Collaboration guide background

### The deliberation and decision process

**The deliberation and decision process.** `AGENTS.md` carries the
operational rules — how to make a correct change and operate safely. This
file carries the roles, the review loop, and the coordination doctrine that
explain *why* those rules take the shape they do.

### The AI surface is bimodal

**The AI surface is bimodal.** These roles are filled by **agent-side AI** — a
model acting as a named participant, with a role, a record, and accountability
for what it signs. That is a different thing from AI used as a tool inside the
work, and conflating the two is how "an agent reviewed it" comes to mean less
than it should.

### The scope-reduction trap

Narrowing is
the path of least resistance in review — it costs the reviewer nothing,
reads as prudence, and can never be shown wrong, because the wider
version is never built.

### Coordination space

That is
what makes the method model-agnostic: sessions coordinate through the record,
not through shared memory, so a project can mix or swap AI vendors without
changing anything.


## Collaboration guide background (continued)

### Author relation

its author, who is typically the stronger party on the software.

### Review record

It is asynchronous and commit-mediated: not a conversation that
leaves no record.

### Steelman first

A review that opens with
findings reads as a verdict, and an author defends rather than thinks.

### Review confidence

a reviewer who reads to confirm that the change works will find that
it does.

### Review sweep examples

("exists / works / is available / is atomic / fails closed")

(empty /
   None / zero / single / N≫1 / mismatched units or CRS)

### Coverage gap

A covered-only line manufactures false comfort.

### Decision choices

A menu of five options with no recommendation moves
the work to the Maintainer rather than unblocking it.

### Durable handoff

A tool's
private memory is not shared with another agent type or with a human reviewer.

### Session reflection

a lesson that stays only in
a reflection is a lesson that expires.
