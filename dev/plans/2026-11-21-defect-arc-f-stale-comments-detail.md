# Detail: Defect arc F, the sixteen comment lines

Companion to [the plan](2026-11-21-defect-arc-f-stale-comments.md). It exists
because the table of old and corrected lines is too long for the plan's
opening body; it holds nothing the plan's Scope does not already promise.

Line numbers are from `0.9-dev` on 2026-11-21 (read with a text search and
confirmed with Python's tokenizer, which lists only comment tokens). Each
corrected line replaces the old line in place; indentation is kept. Where a
tool has a shipped copy and Cairn's own copy, the same edit goes into both and
`cmp` must report them identical afterwards. Names come from
`install/_scaffold/layout_catalog.py` and the tree: `bootstrap/` is `install/`
(its old tests folder is now `tests/`), `scripts/` and `tools/` installed files
are `dev/tools/`, and `scripts/quality_gate.py` is `tests/quality_gate.py`.

## Lines to correct (16 lines, 11 copies)

Pair 1, `claim_check.py`, line 1006, in `dev/tools/` and
`templates/modules/default-on/`:

```
old:  # directory path half (``bootstrap/tests::test_x``) is not a valid
new:  # directory path half (``tests/integration::test_x``) is not a valid
```

Pair 2, `content_scan.py`, line 324, in `dev/tools/` and
`templates/modules/team-gated/`:

```
old:  # parsed by scripts/quality_gate.py and must not trip the
new:  # parsed by tests/quality_gate.py and must not trip the
```

Pair 3, `content_scan_runner.py`, line 87 (one line becomes two), in
`dev/tools/` and `templates/modules/team-gated/`. The code below it still has
a branch for an install made before 0.8, so the new text keeps that fact
without naming a retired folder:

```
old:  # the rendered scripts/ and installed tools/ copies use their own parent.
new:  # the installed dev/tools/ copy has its own branch below; a copy
      # installed before 0.8 uses its own parent.
```

Pair 4, `run_portable_security_sweeps.py`, line 184, in `dev/tools/` and
`templates/modules/team-gated/`:

```
old:  # scripts/run_security_audit.py) so an adopter reads one exit vocabulary across
new:  # dev/tools/run_security_audit.py) so an adopter reads one exit vocabulary across
```

Single copy, `install/check_module_body_coverage.py`, line 81:

```
old:  #: The Cairn checkout this script ships in (bootstrap/ -> repo root).
new:  #: The Cairn checkout this script ships in (install/ -> repo root).
```

Single copy, `templates/modules/default-on/run_security_verification.py`
(shipped only; Cairn has no installed twin), five lines:

```
132 old:  #: ``verify()`` in ``bootstrap/verify_integrity.py`` reads the same record
132 new:  #: ``verify()`` in ``install/verify_integrity.py`` reads the same record
142 old:  #: distinct from ``bootstrap/_scaffold/lockfile.py``'s ``_LIVING_STATE_DSTS``
142 new:  #: distinct from ``install/_scaffold/lockfile.py``'s ``_LIVING_STATE_DSTS``
144 old:  #: adopter checkout never has a ``bootstrap/`` directory). Carries exactly the
144 new:  #: adopter checkout never has Cairn's ``install/`` directory). Carries exactly the
153 old:  #: engine-side ``_LIVING_STATE_DSTS`` in ``bootstrap/_scaffold/lockfile.py``
153 new:  #: engine-side ``_LIVING_STATE_DSTS`` in ``install/_scaffold/lockfile.py``
406 old:  # ships as an adopter-tree file with no bootstrap/ engine to import, so this
406 new:  # ships as an adopter-tree file with no install/ engine to import, so this
```

Single copy, `templates/modules/team-gated/api_access_security.py` (shipped
only), two lines:

```
49 old:  #: siblings of this file: the installed layout (``scripts/_api_access_security``,
49 new:  #: siblings of this file: the installed layout (``dev/tools/_api_access_security``,
67 old:  # Parity with bootstrap/scaffold.py's launcher: a real directory inside
67 new:  # Parity with install/scaffold.py's launcher: a real directory inside
```

Count: 2 + 2 + 2 + 2 (pairs 1 to 4, one line per copy) + 1 + 5 + 2 = 16 lines
in 4 x 2 + 3 = 11 copies. This matches the roadmap's count.

## Left alone, with the reason

- `dev/tools/_intent/shared.py` and its twin `templates/modules/team-gated/_intent/shared.py`,
  line 19: "either tools/_intent or dev/tools/_intent". A text search for stale
  folder names in comments also finds it. It is not one of the seven tools
  the roadmap names, and it states both layouts on purpose, because the code on
  the next lines handles both. Left alone.
- Docstrings and string literals in the eleven copies that name an old folder
  (for example `content_scan.py` lines 12 to 38 and 148 to 150,
  `claim_check.py` lines 8 and 256 to 260, the `"<verified tools/git_read.py buffer>"`
  strings, and the `scripts/` fallback in `run_security_verification.py`
  lines 338 and 360). Changing a docstring or a string changes the syntax
  tree, and a string may be read by code or recorded in a baseline. The
  roadmap and plan C already set this boundary. Left alone; the plan does not
  touch any token that is not a `#` comment.
