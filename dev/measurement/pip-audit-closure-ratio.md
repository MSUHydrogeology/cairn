# The pip-audit closure ratio, and the tripwire that keeps it meaningful

**What this file is.** The durable record behind the `python-security` module's
**reachability annotation** — the `in-closure` / `out-of-closure` / `unknown`
label the dependency leg puts on each vulnerable distribution. It carries four
things: the field measurement an adopter supplied, the same ratio measured here,
the threshold that keeps the annotation worth having, and how often the walk has
to answer `unknown`.

**Why it is a gate, not a document.** The threshold in §3 is read out of *this
file* by `test_closure_stays_a_bounded_fraction_of_the_discoverable_set` in
[`bootstrap/tests/test_security_stack.py`](../../bootstrap/tests/test_security_stack.py),
so the number here is the only copy and the test cannot drift from it. **Cairn
has no CI**: that node runs when a person types
`CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests`. Nothing runs it
automatically.

**Why the annotation needs a ratio at all.** The leg audits the Python
distributions discoverable in the environment, which is the right question for a
self-audit tripwire and is not narrowed by any of this. But on a conda
scientific stack the environment is several times the project's own dependency
closure, so a correct report can carry a hundred-plus findings of which a
handful are the project's. The label is what makes that report triageable. It
only works while the closure it is computed against is meaningfully *smaller*
than the environment — a closure that has re-inflated to most of the
environment partitions nothing and the axis is dead weight. §3 is the tripwire
for exactly that.

## 1. The adopter's field measurement

Reported on
[issue #6](https://github.com/MSUHydrogeology/cairn-scientist-ai-teams/issues/6),
measured by the adopter on a scientific Python library in a conda environment.
**Recorded exactly as reported**, and attributed to them, so field evidence
built by hand does not evaporate into a closed issue.

| | count |
|---|---:|
| distributions discoverable in the environment | 299 |
| in the adopter's declared dependency closure | 93 |
| outside the adopter's scope | 212 (71%) |
| vulnerabilities reported over the ambient environment | 144 across 21 packages |
| reachable from a declared runtime dependency | 27 across 2 packages |

Both reachable findings were transitive and one patch release behind
(`flopy → matplotlib → pillow`, `rasterio → click`).

**The partition does not close, and this record does not close it.** 93 + 212 =
**305** against a stated discoverable total of **299** — a gap of **6**. It is
not rounding: `212/299` is 71% and `93/299` is 31%, and the two shares sum to
102%. No third bucket is stated that would absorb the difference, and neither
the report nor the proposal that carried it says which figure moves.

These are someone else's numbers. Adjusting one of them so the table adds up
would hand a reporter their own field data back silently corrected, which is a
worse failure than a visible gap — so the figures stand as reported and the
discrepancy is stated here rather than smoothed away. Asking the reporter which
figure moves is a question for the issue, not an answer this record supplies.

## 2. The same ratio, measured here

Measured with the walk this record governs
([`resolve_declared_closure`](../../templates/modules/team-gated/run_security_audit.py)),
`as_of 2026-08-31`.

* **Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — Python
  3.13.13 (conda-forge), Cairn's canonical interpreter.
* **Discoverable set**: **299** distributions
  (`installed_distribution_names()`, the same enumeration the annotation's
  denominator uses).
* **Root**: `modflow_tools` — a scientific package installed in this
  environment, chosen because it is the shape the adopter reported on rather
  than a tooling package with a trivial closure.

| root | closure | share of the discoverable set |
|---|---:|---:|
| `modflow_tools` | 53 | 17.7% |
| `jupyterlab` | 89 | 29.8% |
| `hvplot` | 40 | 13.4% |
| `sphinx` | 24 | 8.0% |
| `flopy` | 15 | 5.0% |
| `rasterio` | 9 | 3.0% |
| `pytest` | 9 | 3.0% |

Across **303** top-level names in this environment that resolve to exactly one
distribution, the **largest** closure any root produced was **89 of 299
(29.8%)** and the median was **2**. The adopter's 93/299 (31%) sits just above
the top of that range, which is the agreement worth recording: the ratio they
measured by hand is the ratio this walk produces on a comparable environment.

## 3. The closure-size tripwire threshold

**Tripwire threshold**: `closure <= 50% of the discoverable set`

**Why 50, measured on both sides rather than picked.** The number has to sit
above every legitimate closure and below the failure it is watching for, and
both bounds were measured on this environment on 2026-08-31:

* **Above the legitimate range.** The largest correct closure observed over 303
  real roots is 29.8%. Fifty per cent leaves a factor of about 1.7 in headroom,
  so a project genuinely larger than anything here does not trip the wire
  merely for being large.
* **Below the failure mode.** The failure this watches for is an extras-gated
  edge being followed — the policy an earlier revision of the design proposed
  and which was withdrawn. Re-running the same roots with extras included:

  | root | default closure | extras-inclusive closure |
  |---|---:|---:|
  | `modflow_tools` | 53 (17.7%) | 234 (78.3%) |
  | `jupyterlab` | 89 (29.8%) | 214 (71.6%) |
  | `flopy` | 15 (5.0%) | 225 (75.3%) |
  | `rasterio` | 9 (3.0%) | 217 (72.6%) |
  | `sphinx` | 24 (8.0%) | 214 (71.6%) |
  | `pytest` | 9 (3.0%) | 214 (71.6%) |

  Every extras-inclusive closure lands at **71.6% or above**. Fifty per cent is
  therefore below the *smallest* observed failure and above the *largest*
  observed success, with a wide gap on each side rather than a number tuned to
  one case.

**What a breach means.** Not that the walk crashed — it will not — but that the
closure has stopped being a *subset* worth partitioning against. At 78% of the
environment, `out-of-closure` labels a fifth of the report and the reader is
back to triaging by hand. That is why the threshold is a tripwire on the *axis
being useful*, not a correctness gate: nothing about the audited set, the
findings or the exit code changes when it trips.

## 4. How often the answer is `unknown`

The design tolerates an approximate walk because every failure direction lands
on `unknown` and `unknown` gates nothing. The open question was whether
`unknown` would become the *common* case, at which point the axis stops
carrying information. Measured rather than assumed, same environment, same
date:

| observation | count |
|---|---:|
| top-level package names (excluding data-directory keys) | 309 |
| …resolving to exactly one distribution | 303 |
| …ambiguous, so the whole closure is `unknown` | 6 |
| single-distribution roots returning a whole-closure `unknown` | **0** |
| single-distribution roots returning a non-empty partial `unknown` set | **0** |

The six ambiguous names are `PyObjCTest`, `PyObjCTools`, `git`, `google`,
`sphinxcontrib` and `stevedore` — namespace packages several distributions
contribute to, which is a real limitation for a project whose own top-level
name is one of those, and no limitation at all for a project whose is not.

So on this environment `unknown` is **not** the common case: every unambiguous
root partitioned cleanly, and no distribution anywhere landed in a partial
`unknown` set. That is one environment on one date, which is why this is
recorded as an observation with a denominator rather than as a property.

## Re-measuring

Every figure above is dated because they all move: install a package and the
discoverable set changes, and the closures with it. Re-measure when the
threshold is questioned, when the environment changes materially, or when the
adopter supplies a second field measurement — and add a dated section rather
than editing one, so the trend stays visible.
