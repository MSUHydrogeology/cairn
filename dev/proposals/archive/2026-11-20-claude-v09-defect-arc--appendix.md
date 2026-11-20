# Appendix: per-item table for the v0.9 defect arc

Companion to `2026-11-20-claude-v09-defect-arc.md`. Sources: the open issues read with `gh issue view` on 2026-11-20 and section 1 of the roadmap on the `0.9-dev` branch. "Read" means I read the code or text and did not run it. Protected-surface key: ENG = installer engine (`install/_scaffold/`); SES = the interpreter-binding reader (`session.py` and its byte copy); PYT = shipped Python or functional configuration; SWEEP = portable security sweeps; GATE = gate machinery and protected tests; none = prose or comments only.

| Item | Kind | Resolution | Plan | Host | Protected surface |
|---|---|---|---|---|---|
| #93 prune command is bash-only | adopter friction | add the PowerShell form beside bash, in skill, module, methodology page and shipped twins | A | any | none |
| #97 text names the pre-0.8 layout | defect (docs) | correct the named lines, add `RULES.md` to the commit list | A | any; Windows to run the PowerShell steps | none |
| #97 fixes 2 and 3 (a new quickstart path check; run the PowerShell column as a release step) | feature | not in this arc; no new check, nothing added to the gate | none | any | none |
| #98.4 bare `python` in session-start skill | adopter friction | say what to run when `python` is not found | A | Windows to confirm | none |
| #98.5 prose check fails on a fresh clone | defect | cite the meter export so the checker accepts it; replace the dead `suite-cost.md` link | A | any | none |
| #99.2 UPGRADE.md omits the layout move | adopter friction (docs) | describe it; record that the second move cannot be previewed as a known limit | A | any | none |
| #99.5 stale paths in Cairn- and tool-owned text | defect (docs) | fix at the source in templates and Cairn's own text; generated files are regenerated, never hand-edited | A (comment-only edits in engine and tool files go with B and C) | any | none |
| #95 Windows clone fails the helper hash check | defect | root `.gitattributes`; error names the real cause; line-ending note in UPGRADE.md (plan A) | B | Windows to verify | ENG, config file |
| #99.1 lock keys the dispatcher rejects | defect | default: do not widen the dispatcher; stop writing the keys where it reads; heal upgraded trees | B | any | ENG, PYT (security gate) |
| #99.3 shallow fetch looks like unproved ancestry | adopter friction | its own message | B | any | ENG |
| #99.4 identical files blocked by a stale `base_hash` | defect, unconfirmed | reproduce; fix or close with evidence | B | any (needs a CRLF fixture) | ENG |
| #100 `claim_check_command` token keeps the old path | defect | layout move rewrites it; upgraded trees healed | B | any | ENG |
| #102 no way to retire a deleted wrapper's record | adopter friction | documented route like `RULES.md`; wrappers only | B | any | ENG, trust integrity |
| #98.3 skills not linked; harness folder absent | adopter friction | closing message says what to do | B | Windows to confirm | ENG |
| Move `docs/DOCUMENTATION_PLAN.md` into `dev/` (roadmap section 1, not an issue) | defect | move it, add the upgrade move, update shipped files naming the old path; changes the install manifest | E (after B) | any | ENG, install contract |
| #98.1 README files listed as open work | defect | skip `README.md` | C | any | SES |
| #98.2 backslash printed as `\x5c` | defect | forward slashes on every system; escape policy unchanged | C | Windows to confirm | SES |
| #91 part 2 execute-bit test | defect | fix the Windows test in both `conflict.py` copies; close the four named tests as not Cairn's | C | Windows to verify | PYT |
| #96 meter reports Claude usage UNKNOWN | defect (partly confirmed) | usage-free record types no longer force UNKNOWN; unreadable usage still incomplete; check against real current logs | C | any with Claude logs | PYT |
| #99.6 and #101 Bandit findings and threshold | adopter friction and feature | adopter-set severity threshold, default unchanged; plan finds why an adopter's audit sees Cairn's tools | C | any | PYT (security audit) |
| B3a new files under `tests/` unscanned | test gap | restore the scan | D | any | GATE |
| B3b `test_fork_advisory.py` checks only exit 2 | test gap | restore no word match; if the test must tell one refusal from another, it checks which record the refusal names | D | any | GATE |
| B2a nine older failures in the release-members contract test | test gap | measure on Windows, then repair | D | Windows | GATE |
| B2d no Git-absent test in the secrets sweep | test gap, partly stale | a test exists, shaped for POSIX; measure on Windows, then repair | D | Windows | SWEEP, GATE |
| B2e fifteen older Windows failures of 2026-11-16 | test gap, unconfirmed | measure, then repair what remains | D | Windows | GATE |
| B2b checker rejects Windows `file=` paths | defect (release operator) | accept the paths, or record that the check runs only on the Mac | D | Windows | GATE (release control) |
| Published v0.8.0 tag checked through both release routes (roadmap section 1) | test gap | run both routes in Windows Git Bash | D | Windows | release control |
| History freeze fails on refs that point at trees (roadmap section 1) | defect | default: document freezing from a clean clone; skipping such refs would change a security check and needs review | D | any | release control |
| #91 part 1 `.gitattributes` for adopters | already fixed | close: 0.8 ships it | none | any | none |
| AST baseline correction | already fixed | fixed at `ed893f0d`; the joined run confirms | none | any | GATE |
| #90 repository root by a marker | feature | defer to v0.10 (Decision 2) | none | any | PYT |
| #91 part 3 archive helper | feature | defer to v0.10 (Decision 2) | none | any | PYT |
| #79 smaller entry file | feature | to the tightening proposal (Decision 2) | none | any | none |
| B2c full Windows suite as a release gate | process | belongs to the roadmap row on verifying releases on Linux and Windows | none | Windows | GATE |
| B1 the re-anchor and its ceremony proposal | process | separate proposal, one signing after the joined run | none | Mac (Maintainer) | GATE |
| B4 "bootstrap" wording check | wording check | not restored: it looked for one word in a refusal message (Maintainer, chat, 2026-11-20: "Drop it.") | none | any | GATE |
| Archive of `2026-11-19-codex-native-release-membership.md` | process | after the signing | none | any | none |

Open issues that are not defects, left alone: #19, #34, #67, #75, #81, #82, #83, #84, #92, #94.
