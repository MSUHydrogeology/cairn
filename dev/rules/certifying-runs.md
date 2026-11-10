# Certifying runs

Cairn's rule for the full-suite certifying run. Routed from `RULES.md`. The text below moved from `AGENTS.md` on 2026-11-10 unchanged.

Do not run a full-tree certifying suite for ordinary implementation. The
authorized certifying run is the pair on a clean committed tree under Python
3.13.x: `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests
--quality-gate-shuffle-seed=0`, then `python scripts/quality_gate.py --sub
neutrality --sub redundancy`. It is run only before a push when required,
before re-anchor, before a release cut, or when the Maintainer asks. It
certifies every change at or before that commit for bisect. The reviewer never
runs the full suite. Never set
`CAIRN_FULL_SUITE=1` for another reason.
