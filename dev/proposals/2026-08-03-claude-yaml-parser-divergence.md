<!-- cairn-internal-ref-allow: doctrine/runtime-contract.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# Two YAML parsers, chosen by accident — the profile loader behaves differently depending on what happens to be installed

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: proposed
**Touches**: `bootstrap/_scaffold/config.py` (`_yaml_load`, `_minimal_yaml_parse`,
`load_config`), its exports in `bootstrap/_scaffold/__init__.py`, and the
`bootstrap/tests/` coverage for profile loading
**Deliberately not touched**: the profile YAML *schema* itself, the lockfile
emitter (`_emit_lock_yaml`), and the YAML *quoting* helpers (`_yaml_dq`,
`_yaml_sq`) — those are emitters, not parsers, and carry no divergence
**Related**: `gate-reanchor-preflight` (archived 2026-08-03) — this is the same
finding class its six review rounds kept producing, on a different surface
**Plan review**: `required(**External**, security lens)` — the scaffold / merge
engine is a named high-risk surface in `AGENTS.md` (it parses untrusted module
and profile files and writes into a target tree), so this clears the Security
Review trigger

## Context

`bootstrap/_scaffold/config.py:33-43` selects a YAML parser at import time:

```python
try:
    import yaml as _yaml
    def _yaml_load(text): return _yaml.safe_load(text)
except ImportError:
    def _yaml_load(text): return _minimal_yaml_parse(text)
```

So the profile loader runs **one of two different parsers depending on whether
PyYAML happens to be importable**. That is not a fallback in the usual sense —
both paths are live, and nothing records which one ran.

The distribution of who gets which is the wrong way round. Cairn's whole
runtime contract is that **adopters take zero dependencies**
(`bootstrap/DEPENDENCY_BUDGET.md`), so the typical adopter running the bootstrap
gets `_minimal_yaml_parse`. Cairn's own canonical environment has PyYAML 6.0.3
installed, so its tests and gates exercise `safe_load`. The
`except ImportError` branch even carries `# pragma: no cover`.

**The path most adopters take is the path Cairn least exercises.**

## Evidence

Nine realistic profile inputs, both parsers, same input:

| Input | `yaml.safe_load` | `_minimal_yaml_parse` |
|---|---|---|
| `project_name: cairn  # the name` | `{'project_name': 'cairn'}` | `{'project_name': 'cairn  # the name'}` |
| `modules: [claim-check, reflections]` | list of 2 | the **string** `'[claim-check, reflections]'` |
| `profile:\n  size: small\n  tier: two` | nested mapping | `{'profile': []}` — **data silently dropped** |
| `strict: true` | `True` | `'true'` |
| `strict: false` | `False` | `'false'` — a **truthy** string |
| `test_command: null` | `None` | `'null'` |
| `depth: 3` | `3` | `'3'` |
| `- claim-check\n- reflections` | a list | `{}` |
| tab-indented list | **raises `ScannerError`** | accepted |
| empty document | `None` | `{}` |

**9 of 9 diverge.** Two matter beyond tidiness.

### Finding 1 — a validation guard that does not fire on the adopter path

`load_config` (`config.py:147-156`) guards the contract that a profile must be a
top-level mapping:

```python
if not isinstance(cfg, dict):
    raise ValueError(f"{config_path}: expected a YAML mapping at the top level, ...")
```

Under PyYAML that guard fires. Under the minimal parser it **cannot**, because
`_minimal_yaml_parse` returns a `dict` unconditionally — including `{}` for
input it did not understand at all. Executed both ways:

```
top-level sequence   PyYAML   -> refused (expected a YAML mapping at the top)
top-level sequence   minimal  -> ACCEPTED
empty file           PyYAML   -> refused (expected a YAML mapping at the top)
empty file           minimal  -> ACCEPTED
```

A malformed or hostile profile that Cairn's own environment rejects is accepted
on the adopter path — as an **empty config**, which then silently takes every
default. The install proceeds. This is a control that is present and not
reached, which is precisely the finding the `gate-reanchor-preflight` reviews
produced four times running.

### Finding 2 — token values carry unparsed text into the generated tree

`project_name` is a substituted token (`KNOWN_TOKENS`, `config.py:50-63`) written
into files in the adopter's tree. On the minimal path its value retains a
trailing YAML comment, so `project_name: cairn  # the name` substitutes
`cairn  # the name`. Content the adopter believed was a comment becomes content.

### Latent, not live

`false` parsing to the truthy string `'false'` would invert a boolean setting.
No current config key is consumed as a boolean — grepped, none found — so this
is a hazard of the shape, not a present defect. Recorded so a future boolean key
is not added into it.

## Proposal

**Make the parse deterministic, and make the subset boundary explicit.**

1. **One parser, always.** Drop the PyYAML branch and always use the in-tree
   parser. Behaviour must not depend on what happens to be installed in the
   environment; that dependence is the defect, and removing the branch removes
   the whole differential rather than trying to keep two implementations in
   agreement forever. This also aligns the loader with the stdlib-only runtime
   contract instead of quietly preferring a dependency when present.

2. **Fail closed at the subset boundary.** `_minimal_yaml_parse` documents itself
   as covering "the subset scaffold.py needs". It should *refuse* input outside
   that subset rather than silently returning a different value: nested
   mappings, inline `[...]`/`{...}` collections, tab indentation, and a
   non-mapping top level should raise, not degrade. A parser that cannot
   represent the input must say so.

3. **Move the mapping guard where both paths reach it**, so the `load_config`
   contract is enforced by the parser's own return contract rather than by an
   `isinstance` check one implementation can never fail.

4. **Differential tests as the regression.** Property-based tests (Hypothesis)
   over generated profile documents, asserting the in-tree parser agrees with
   `yaml.safe_load` on the supported subset and refuses outside it. PyYAML and
   Hypothesis are **test-only** here — the same standing as `pytest` and
   `vermin` in `bootstrap/DEPENDENCY_BUDGET.md`, not a new shipped exception,
   because the shipped code would no longer import PyYAML at all.

**Alternative considered — keep both parsers and make them agree.** Rejected as
the primary direction: it preserves a differential surface permanently and makes
correctness depend on tests that must anticipate every input, rather than on
there being one implementation. Worth revisiting only if dropping PyYAML breaks
a real adopter profile, which the subset rules should surface.

### Documentation / doctrine surface

No doctrine change. The stdlib-only runtime contract
(`doctrine/runtime-contract.md`, `bootstrap/DEPENDENCY_BUDGET.md`) is *applied*
here, not amended — this proposal removes a quiet exception to it rather than
adding one. `bootstrap/BOOTSTRAP.md` Appendix A documents the profile format and
should gain an explicit statement of the supported subset, since that subset
becomes an enforced boundary rather than an informal one.

## Known implementation cost

`bootstrap/_scaffold/*.py` is pinned by the AST attestation baseline
(`bootstrap/tests/test_ast_attest.py`). Changing `config.py` requires re-anchoring
that baseline per `bootstrap/REANCHOR_RUNBOOK.md`; it does not auto-update, and
the suite fails until it is re-anchored. Flagged here so the cost is priced at
Decision rather than discovered mid-implementation.

`config.py` is **not** in `_gate_manifest._frozen_files()` (the globs reach
`bootstrap/*.py` non-recursively, not `bootstrap/_scaffold/`), so this does not
require a gate re-anchor — only the AST baseline.

## Risks and residuals

* **Adopter profiles relying on PyYAML-only syntax would begin to refuse.** That
  is the intended behaviour change, but it is a behaviour change: an adopter
  whose profile used a nested mapping got silent data loss before and gets an
  error after. Better, and still worth a changelog note.
* **The in-tree parser becomes the only implementation**, so its own bugs have
  no second opinion. The differential tests against PyYAML are what substitute
  for that, and they only run in a dev environment where PyYAML is installed.
* This proposal does **not** audit the emitters (`_emit_lock_yaml`, `_yaml_dq`,
  `_yaml_sq`). Round-tripping emitted YAML through the stricter parser is a
  reasonable follow-up and is not claimed here.
