# Authorization, second re-anchor ceremony (the AST pin) (to be committed after the ceremony)

Given in chat by the Maintainer, 2026-10-28. The text below was drafted by the planning session and put to the Maintainer, who answered with the words quoted at the end.

> I authorize moving the gate anchor to candidate 5267f3639d6ce5a86db4c7d32e0d23d034d1e7d6 (package sha256 f1c350a7e77e7715e53c4ba21868ec98d090381ee9a0e7364fcb9531f72f1611). I am relying on the agents' work and the scripted comparisons: the AST correction script and its two readers, the packet from `repin packet`, and the reader's record. I have not checked the code myself. The change pins the AST attestation baseline after the 0.5 changes: four reviewed deletions of onboarding constants removed by `fa86e2cb`, 21 changed symbols, and the known-new manifest (23 added, 7 rekeyed, 4 dropped). I know: there is no full test run at this commit (I waived it); the two AST tests now pass; all commits are unsigned; and the pinned-files manifest reads HOLD until this ceremony signs it.

The Maintainer's reply, verbatim, after `compare.sh` printed ALL COMPARISONS PASSED:

> "Yes on the authorizations."

Note: `compare.sh`'s process look listed one orphaned `/bin/sh` from an earlier agent test run (a `test_values_file_state_fifo` temp folder, parent pid 1, running 18 hours, blocked on a FIFO), not a stage 1 process. The planning session stopped it with `kill` before stage 2.
