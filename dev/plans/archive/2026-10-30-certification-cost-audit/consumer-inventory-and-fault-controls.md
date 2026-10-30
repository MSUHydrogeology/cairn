# Consumer inventory and installed-copy fault controls

Implementation: `e270902db03f54a5936269c198ccd706434dd5c4`.
Final checked tree: `6fc4d9eaddf4dc5082022665097f6c4e5fe40bd4`.

## Fixture consumers

`installs` is defined in `bootstrap/tests/test_review_sweep_ships.py`. Its four consumers are:

| Test | Installed-tree behavior |
|---|---|
| `test_installed_loop_document_carries_the_obligation` | Reads installed `dev/agent_collaboration.md`. |
| `test_installed_agents_md_carries_the_pointer` | Reads installed `AGENTS.md`. |
| `test_an_install_without_the_sweep_is_reported` | Reads the installed sweep, then removes it from a local string. |
| `test_an_install_leaves_no_placeholder_the_engine_cannot_fill` | Reads installed text files only. |

No consumer mutates an installed tree or requires a fresh install. The fixture invokes the real `bootstrap/scaffold.py` CLI once per globbed profile and creates a separate temporary target for each: `collaborative-team`, `high-rigor-legacy`, and `solo-greenfield`.

## Fault matrix

The unmutated control passed all 391 nodes with both shuffle seeds. Each fault was injected into the fixture's fresh installed copy immediately before its existing installed-content assertion node ran. Every mutant produced the expected assertion failure.

| Profile | Fault | Existing node | Result |
|---|---|---|---|
| `collaborative-team` | Delete lens 4 | `test_installed_loop_document_carries_the_obligation[lens-4-silent-failure-fail-closed-collaborative-team]` | Killed |
| `collaborative-team` | Delete matched wrapped pointer phrase | `test_installed_agents_md_carries_the_pointer[pointer-says-the-answers-rest-on-nine-standing-lenses-collaborative-team]` | Killed |
| `collaborative-team` | Add `{{unknown_token}}` | `test_an_install_leaves_no_placeholder_the_engine_cannot_fill[collaborative-team]` | Killed |
| `high-rigor-legacy` | Delete lens 4 | `test_installed_loop_document_carries_the_obligation[lens-4-silent-failure-fail-closed-high-rigor-legacy]` | Killed |
| `high-rigor-legacy` | Delete matched wrapped pointer phrase | `test_installed_agents_md_carries_the_pointer[pointer-says-the-answers-rest-on-nine-standing-lenses-high-rigor-legacy]` | Killed |
| `high-rigor-legacy` | Add `{{unknown_token}}` | `test_an_install_leaves_no_placeholder_the_engine_cannot_fill[high-rigor-legacy]` | Killed |
| `solo-greenfield` | Delete lens 4 | `test_installed_loop_document_carries_the_obligation[lens-4-silent-failure-fail-closed-solo-greenfield]` | Killed |
| `solo-greenfield` | Delete matched wrapped pointer phrase | `test_installed_agents_md_carries_the_pointer[pointer-says-the-answers-rest-on-nine-standing-lenses-solo-greenfield]` | Killed |
| `solo-greenfield` | Add `{{unknown_token}}` | `test_an_install_leaves_no_placeholder_the_engine_cannot_fill[solo-greenfield]` | Killed |

**Control / mutation summary**: total 9, killed 9, survivors 0, measured equivalents 0. The initial historical pointer probe survived because its pattern did not match a line-wrapped phrase; the accepted proposal's `fault-controls.txt` records that correction. My first temporary hook had the same matching mistake and stopped before mutating; it is excluded from the mutant count. The corrected hook matched the installed text and all nine existing nodes rejected their mutant.
