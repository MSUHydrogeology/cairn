# Supervised re-anchor runbook (differential-oracle gate)

> **Maintainer-only.** Agents build the packet and read the change; **you**
> compare, answer and sign. No agent signs, loads your key or pushes. The page
> ends at the marker line; below it is reference, except Phase 5, the push, which
> is the last step and is yours.

**What your comparisons prove.** The anchor moves only to the commit you name,
signed by your key, and nothing changed between what the reader read and what
you sign. They do **not** prove the change is safe: a harmful change that the
reader and the scanners both miss would pass. Handing you a file on the machine
you sign on adds no assurance; the comparisons do. Run all commands from your
checkout.

### Prerequisites
The instantiated launcher and the authorization packet (from the builder), your
values file, your ceremony key (in no agent), and the candidate ref `$CAND`: the
reader's record, `dev/ceremony-record.md`, is its tip commit. `$REV` is the
record's `read-commit` line, the commit the reader read.

### 1. Your values file, once
Copy `bootstrap/reanchor-values.example` outside the repository and fill it in.
It names each tool by its real file, never a link; a toolchain upgrade breaks
it. That goes stale, and that is not a malfunction: the refusal is correct, so
fix the path and run `--validate`.

### 2. Stage 1, with no key
```
sh <launcher> <packet> <values> $CAND --validate
sh <launcher> <packet> <values> $CAND
sh <launcher> <packet> <values> $CAND --show-report
```
Read the page `--show-report` prints, then answer its five yes/no questions
(Y1 to Y5); any no stops here.

### 3. Compare, then sign
Each command's result must equal what is said. Any difference: stop.
```
# E1  equals `launcher-sha256` in the record and the reader's hand-off
shasum -a 256 <launcher>
# E2  equals the page's candidate id
git rev-parse HEAD
# E3  equals the page's package sha256
sh <launcher> <packet> <values> $CAND --hash-package
# E4  your key's fingerprint is on the page's roster list
ssh-keygen -lf <key.pub>
# E5  both print SAME
git diff --quiet $REV $CAND -- bootstrap/reanchor-launcher.template.sh && echo SAME || echo DIFFERENT
git show $CAND:bootstrap/reanchor-launcher.template.sh | sed "s/@PACKET_SHA256@/$(shasum -a 256 <packet> | cut -c1-64)/" | cmp - <launcher> && echo SAME || echo DIFFERENT
# E6  equals the page's path for that tool, for every tool in your values file
readlink -f "$(command -v <tool>)"
# E7  second and later ceremonies only: equals the page's scan digest
E=$(mktemp -d) && git archive refs/cairn/gate-anchor bootstrap | tar -x -C "$E" && <python> -E -s "$E/bootstrap/tests/_gate_preflight.py" scan-digest --repo <checkout>
# R1  the record sits directly on what was read: prints $REV
git rev-parse HEAD^
# R2  prints only dev/ceremony-record.md
git diff --name-only HEAD^ HEAD
# R3  equals `packet-sha256` in the record
shasum -a 256 <packet>
# R4  prints SAME
diff <(grep '^member ' dev/ceremony-record.md | sort) <(grep '^member ' <packet> | sort) && echo SAME || echo DIFFERENT
```
Just before stage 2, repeat E1 and E6, and check `ssh-add -l` does **not** list
your key. Then run stage 2 with no key socket in its environment; the signer
asks for the key's passphrase once. Do not `ssh-add` the key. Pass the digest
from E3:
```
env -i HOME=<home> PATH=/usr/bin:/bin TERM="$TERM" LANG=C /bin/sh <launcher> <packet> <values> $CAND --stage2 <digest>
```
Then publish both refs in one atomic push (Phase 5, below).

### The first ceremony
The anchor still holds the old text, so no tool of this design can run it and
E7 has no anchored scan: it rests on the builder, the reader and the record,
and the page and record say so. You authorize it in your own words, naming
`bootstrap/_scaffold/`, `bootstrap/security_check.py`,
`bootstrap/tests/_gate_manifest.py`, and the dropped test nodes by count and
commit, and you name the known manifest and AST failures as the Y4 allowance.
Nothing in this page calls `_gate_reanchor.py promote`; it stays callable.
<!-- end of page -->

<!-- `dev/.cairn/trusted-activation.yml` and `dev/.cairn/promotion-authorization.yml`
     are Maintainer-supplied trust-root configs, absent unless the supervised
     re-anchor flow creates them.  Their claim-check exemption moved to
     dev/.cairn/claim-check-allow.json on 2026-08-27; this note names them so a
     reader still learns why the paths do not resolve. -->

## What each comparison protects, and what it does not

| Check | It protects | It does not |
|---|---|---|
| E1, R3 | you run the launcher and packet the reader recorded | that the reader read well |
| E2 | the commit you sign is the commit on the page | that the commit is safe |
| E3 | the package you confirm is the bytes the page described | that the package is harmless |
| E4 | your key is one the anchored roster lists | which key a later roster adds |
| E5 | the launcher is the reviewed template with one slot filled | that the template is safe |
| E6 | the programs run before any candidate byte are the ones you named | the bytes of those programs: a tool you own can be replaced |
| E7 | the digest the page prints is the one the anchor's own code computes over this range | that the hits listed on the page are the scan behind that digest (it binds the digest only, and the page's line saying who made the scan is the report's own claim); a change that matches no scan pattern; the first ceremony, which has no anchored scan |
| R1 to R4 | the record is the one commit on what was read, and names this packet, launcher and these files | what the reader wrote in it |
| Y1 to Y5 | your own judgement | Y1 is a statement of the reader's; you cannot check it |

Delivering a file to the machine you sign on adds no assurance of its own. The
reader is a fresh session of the same vendor as the builder, which each record
states; the scanners are a fixed pattern list and age.

## The steps the tools cite

`sh bootstrap/reanchor.sh steps` prints the closed, ordered registry of the
ceremony's steps. **The IDs below are that registry's**, cited here so the two
cannot drift apart: a step in the code and not in this document, or the
reverse, fails a test.

What this buys is a drift signal on the procedure's *shape*. It attests nothing
about whether the prose around each citation is accurate — that is reviewed, not
machine-checked, and this sentence is here so the presence of a check is not
mistaken for the stronger claim.

| ID | what it establishes |
|---|---|
| RA-01 | the launcher alone reads your values file, under a closed grammar |
| RA-02 | the packet on disk is the one bound into the launcher |
| RA-03 | the packet is re-hashed in memory; it detects a rewrite between reads, it does not prevent one |
| RA-04 | the packet names exactly the closure fixed in the launcher |
| RA-05 | the ceremony artifact is a closure member: one row, its digest, the path the launcher starts |
| RA-06 | the candidate ref is resolved once, to a full object id |
| RA-07 | every closure blob at that id matches its reviewed digest |
| RA-08 | the extracted artifact is hashed again, separately |
| RA-09 | the launcher composes the review manifest from the packet; nothing is read from the candidate |
| RA-10 | **the first candidate byte runs**, and only because its digest matched |
| RA-11 | the effective configuration prints, while you can still stop |
| RA-12 | the key channel is probed; if a passphrase prompt appears here, decline it |
| RA-13 | the read-only checks run and the package is written; no key, no ref moves |
| RA-14 | you read the page (`--show-report`) |
| RA-15 | you hash the package yourself (`--hash-package`) |
| RA-16 | the key stays in no agent (the **N4** precondition); you make the pre-signing checks |
| RA-17 | stage 2 validates the package against your digest and re-verifies its own bytes; no candidate code runs |
| RA-18 | the checkpoint is signed and branch and anchor move in one transaction |
| RA-19 | the two refs are published in one atomic push |

**"Where does the review manifest come from?"** The launcher composes it. It is
not a file you write, and it is not a file the builder hands you: every value in
it comes from the packet or from the candidate id the launcher resolved itself.

**"How do I read the report?"** Run the launcher with `--show-report`. A
confirmed digest over an unread report authorizes something you have not seen;
this is the step at which you exercise judgement rather than check arithmetic.

## Phase 0 — the trust root, transitions and the dated posture

### Phase 0 transition mode — measured, never chosen

A **transition** is a ceremony that carries a change to the authority closure
itself: the checker, the roster, the runbook, the ceremony artifact. A
**steady-state** re-anchor carries none.

**You do not select between them, and there is no flag.** The launcher compares
every closure member at the anchor against the resolved candidate, and a single
difference makes it a transition. That is deliberate: an operator who picks the
mode can pick wrong in the unsafe direction, and declaring "steady state" over a
real closure change is precisely the substitution the reviewed-transition path
exists to prevent.

**What a transition additionally requires** is a reviewed member set — which is
what the authorization packet is. The launcher composes the review manifest from
it and hands both the manifest and the resolved OID to the stage commands; in
steady state it passes neither, because there is nothing to carry.

**If the checker refuses saying the closure is identical**, this ceremony is not
a transition and does not need one. Re-run without expecting a closure change:
the launcher will detect steady state by itself.

This section used to hold a second loader block for the transition case,
alongside an instruction to "replace the final command" of the steady-state one.
That instruction produced a live failure — the edited block still extracted from
`refs/cairn/gate-anchor`, so stage 1 ran the candidate's checker and stage 2 ran
the old one. One launcher removes the class.

### The dated posture, and what ends it

The trusted-contributor threat model is scoped to **Cairn's own trust root,
single-maintainer, as of 2026-08-03** — not a standing assumption. One trigger is
mechanical: `apply` refuses to construct a checkpoint unless the commit it builds
verifies against the **anchored** roster (`dev/.cairn/allowed_signers`) under a
pinned verifier.

**This used to say something stronger, and the weaker statement is the accurate
one.** The earlier text claimed `apply` refuses if any commit at or after a
*signing epoch* is unsigned or signed by an unpinned key. That per-commit range
check was retired (plan `git-native-security-foundations`, Chunk B): the epoch
constant lived in the checker's own bytes inside the tree being blessed, so a
candidate could move it to grandfather its own commits, and it refused the
ordinary unsigned-agent-commit workflow, which meant operators disabled it.
Authorization is now the Maintainer's signature on a checkpoint binding the
range-report digest. Signature counts over the range survive as **diagnostics**
in the report and in `check`'s output — never as a verdict.

**Two triggers are not mechanical, and live here because nothing can observe
them:**

1. **The ceremony is run on a checkout the Maintainer does not solely control.**
2. **An adopter takes this mechanism** (it is Cairn-internal today; nothing under
   `bootstrap/tests/` is installed).

On either, revisit the posture before blessing. The named upgrade paths are OS
containment for the evidence stage, external anchoring via `_gate_manifest.py
verify --trusted-repo` (already supported, merely unused here), and a single-use
nonce for replay.

**Dated 2026-10-27.** Handing a file to the Maintainer on the machine the
ceremony runs on adds no assurance of its own; the assurance is the reader's review and
the comparisons you make. Revisit this section if the ceremony gains an external
or hardware-backed authority. Nothing observes that: no job fires this, and
only a person remembering it does.

---

## Phase 5 — publish, in one atomic push (M4)

**The Maintainer's step, and no one else's.** `AGENTS.md` makes pushing always
the Maintainer's; here the push is additionally *part of the authorization
ceremony*, because an anchor nobody else can fetch has authorized nothing. No
reviewer and no implementing agent pushes to `origin` on the Maintainer's
behalf.

**Step 1 — one push, both refs, explicit refspecs.**

```
<maintainer-recorded-git> -C <absolute-path-of-the-checkout-to-bless> \
    push --atomic origin \
        refs/heads/<branch>:refs/heads/<branch> \
        refs/cairn/gate-anchor:refs/cairn/gate-anchor
```

* **`--atomic`** — the branch and the anchor are *one* fact. Without it git
  publishes each ref it can and reports partial success, which leaves the remote
  carrying a moved branch whose anchor still names the previous trust root. Every
  fetcher then verifies new code against an anchor that never blessed it, and
  nothing on the remote records that the pair was ever meant to be one update.
* **Explicit refspecs.** Not `--all`, not `--mirror`, and not whatever
  `push.default` resolves to: the ceremony names the two refs it publishes, so
  the set is read off this page rather than out of a config file the ceremony
  does not control.

**Step 2 — there is no two-push fallback.** If the atomic push is rejected,
**stop and report incomplete publication.** Do not re-push ref-by-ref, do not
push the branch "to at least get the code up", and do not `--force`. A rejection
means the remote's state is not what this ceremony assumed, and the two-push
recovery reproduces by hand exactly the split state `--atomic` exists to
prevent. Diagnose the rejection against the remote's current refs, then re-run
the ceremony from the point the diagnosis indicates.

**Step 3 — verify against the remote, by reading it back.** The push's own exit
status says the client believed it succeeded. Resolve both refs on the remote
and record the object ids in the audit trail:

```
<maintainer-recorded-git> -C <absolute-path-of-the-checkout-to-bless> \
    ls-remote origin refs/heads/<branch> refs/cairn/gate-anchor
```

Exactly two lines, both naming `N`. One line, or two that disagree, is
incomplete publication under step 2 — not a partial success to be topped up.

**Fresh clones need an explicit fetch refspec for the anchor.** `git clone`
fetches `refs/heads/*` and `refs/tags/*`; `refs/cairn/*` is in neither, so a
clone that looks complete has no anchor at all and the gate has nothing to
verify against:

```
git clone <remote-url> <dir>
git -C <dir> fetch origin '+refs/cairn/gate-anchor:refs/cairn/gate-anchor'
```

**Receiving the anchor proves availability, not authenticity.** The fetch says
the remote had a ref by that name; it says nothing about who put it there. What
makes the anchor trustworthy is the signature on the object it names, verified
against the anchored roster — the same check the ceremony ran before publishing.
A fetched anchor is verified, never assumed.

---

## Audit trail

Each ceremony leaves: the record (`dev/ceremony-record.md`, committed on the
commit the reader read), the candidate commit, the resulting new anchor, and the
two **remote** object ids read back in Phase 5 step 3. The expected-old CAS is the
single-use authority — the ref's own history is the replay ledger.

**The reflogs are a diagnostic, not part of this ledger.** The anchor carries a
fixed ceremony reason (`_gate_preflight._CEREMONY_REFLOG_REASON`), which is what
makes a mis-set anchor recoverable — the prior value is written down somewhere.
But a reflog is local and mutable: whoever can write a ref can write its reflog,
so it is never tamper evidence and never authentication. No decision predicate
in the ceremony reads reflog content, and none may.
