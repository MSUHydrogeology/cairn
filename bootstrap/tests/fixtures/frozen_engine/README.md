# Frozen pre-split engine snapshot (scaffold-split 0A.3 / P2#5)

`scaffold_frozen.py` is a **byte-for-byte copy of `bootstrap/scaffold.py` as it
stood before any subsystem extraction** — the behavioral reference for the
differential-oracle harness (`bootstrap/tests/_oracle.py`). The oracle runs both
this frozen engine and the current (in-progress-split) engine against identical
fixture adopter trees and byte-compares the deterministic output; a diff means
an extraction commit changed behavior.

It is a self-contained, stdlib-only module (imports: `argparse`, `re`, `sys`,
`dataclasses`, `pathlib`, `typing`, optional `yaml`) with a `__main__` guard, so
it runs standalone as a subprocess with `--cairn-root` pointing at the live
Cairn tree (templates are read from there, not from this file's location).

## Re-pin protocol

Capture at **Stage 0A** (now — `scaffold.py` is still the intact pre-split
monolith) and **re-pin at the end of Stage 0B**, after the monolith has moved
intact into `bootstrap/_scaffold/` (pure motion, AST-attested). From 0B onward
the current engine is the launcher+package; this frozen copy stays the fixed
pre-split reference for Stages 1–8. To re-pin:

```
cp bootstrap/scaffold.py \
   bootstrap/tests/fixtures/frozen_engine/scaffold_frozen.py   # pre-0B
# or, post-0B, freeze the assembled engine's public entry equivalently.
```

Do **not** re-pin mid-extraction — that would erase the very baseline the oracle
exists to defend.
