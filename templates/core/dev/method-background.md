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
