"""Unused-def whitelist for the ``quality_gate.py`` R6 detector.

Lists symbol names that the stdlib AST-based unreferenced-def
detector should NOT flag, even when no static reference is visible
in the scanned tree.  Two categories:

1. **Argparse callback functions** -- ``_cmd_*`` (or equivalently
   named) functions registered via ``set_defaults(func=...)`` or a
   subparser ``set_defaults``.  Static analysis sees them as
   defined-but-never-called because the dispatch happens through a
   runtime function reference, not a source-visible call.

2. **Standard `__main__` / `__init__` entry points** -- e.g.
   ``main`` invoked under ``if __name__ == "__main__"``.  The static
   walker treats the body of an ``if __name__`` guard conservatively,
   but allowlisting these by name is the cleaner contract.

This file is **imported** (not exec'd) by ``quality_gate.py``; keeping
it as a plain Python frozenset keeps the contract type-stable and
easy to extend.

To add a name:

* Static-dispatch helpers like argparse subcommand callbacks belong
  here.
* Genuinely unreferenced code does NOT -- delete it instead, that's
  the whole point of the R6 gate.

If R6's false-positive rate climbs as the Cairn toolchain grows,
add per-symbol comments explaining why each entry is on the list.
"""
from __future__ import annotations

#: Symbol names whose definitions should not trigger an
#: unreferenced-def finding even when the AST walker sees no static
#: reference.  Match is on the unqualified name (function or class
#: defn name), not the fully-qualified path.
WHITELIST: frozenset[str] = frozenset({
    # Argparse subcommand callbacks in tools/intent.py and the
    # scaffold / upgrade CLI surface.  Dispatched via
    # ``set_defaults(func=...)`` -> ``args.func(args)``.
    "_cmd_claim",
    "_cmd_release",
    "_cmd_list",
    "_cmd_install_hook",
    "_cmd_install_precommit",
    "_cmd_hooks_status",
    "_cmd_precommit_check",
    "_cmd_install",
    "_cmd_upgrade",
    "_cmd_init_lock",
    # Standard Python entry points.
    "main",
    # Pytest fixtures, hook implementations, and parametrized helper
    # names that conftest plugins / pytest discovers by attribute name.
    "pytest_collection_modifyitems",
    "pytest_addoption",
    # Public-API exports in shipped modules.  Adopter code calls
    # these by name; static analysis from inside Cairn's own tree
    # sees no reference because the call site is in the adopter
    # tree, not Cairn.
    "iter_log",  # templates/modules/team-gated/intent.py -- public
                 # iterator over the intent log for adopter tooling.
    "check_text",  # templates/modules/default-on/claim_check.py --
                   # public API for adopters wanting to scan
                   # pre-loaded text without a file path; Cairn's own
                   # callers prefer check_file (which delegates to
                   # check_text via _scan).
    # Dataclass / NamedTuple field "constructors" -- when a NamedTuple
    # is declared and unpacked elsewhere, the type itself may appear
    # unreferenced in some scans.  Keep the door open.
})
