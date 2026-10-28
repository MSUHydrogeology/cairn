# Authorization, first re-anchor ceremony under the new design (to be committed after the ceremony)

Given in chat by the Maintainer, 2026-10-28. The text below was drafted by the planning session and put to the Maintainer, who answered with the words quoted at the end.

> I authorize moving the gate anchor to candidate 55d31f1e59a95c5185b08cb5242b7c23bd73debc (package sha256 ecb847161a3e5a8d4409905da66f944b0d08b5616cb78fe3c405ceeaa3c2ed28). I am relying on the agents' work and the scripted comparisons: the builder's packet, the reader's record, the code reviews and Security reviews. I have not checked the code myself. I know: there is no full test run at this commit (I waived it); two AST attestation tests fail until the AST baseline is corrected; the manifest check says HOLD (29 modified, 17 missing, 19 new pinned files); all 470 commits are unsigned; and 168 test nodes were dropped (77 by `6e9c068d`, 9 by `fed00f7b`, 82 from eight kept files). The change covers `bootstrap/_scaffold/`, `bootstrap/security_check.py` and `bootstrap/tests/_gate_manifest.py`, among others.

The Maintainer's reply, verbatim:

> "Yes, I authorize it."

Y answers as put to the Maintainer: Y1 (the reader's statement) accepted by this authorization; Y2 and Y3 checked by the planning session against the plan and the record; Y4 is the allowance named above; Y5 the Maintainer's own.
