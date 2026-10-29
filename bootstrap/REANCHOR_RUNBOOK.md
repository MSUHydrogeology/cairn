# Supervised re-anchor runbook (differential-oracle gate)

> **Maintainer-only.** Agents prepare the packet and read the change; **you** inspect the script's bound comparisons, make the recorded decisions and sign. No agent signs, loads your key or pushes. The page ends at the marker; below it is reference, except Phase 5, the push, which is the last step and is yours.

**What your yes protects.** Against honest agent mistakes: the anchor moves only to the commit a fresh reader read. It does **not** protect against code running as you, such as a malicious local agent or the candidate's own tests; stage 1 can fool the script's comparisons and leave files that stage 2 loads while you type the key's passphrase. The driver watches the launcher, values file and Python executable; it does not contain code or protect Python's library folder or your other tools.

### Trust-boundary state

The current signed anchor retains the broad frozen policy. The dormant-roster and active-checker bridges are separate reviewed ceremonies, each with its own candidate, packet, reader record, E5/E7 checks and Maintainer authorization; neither authorizes the other. See the reference section for details.

After installation, signed P supplies the roster; named security/trust tests are protected and ordinary changes remain notes. The launcher does not run the prior-manifest verifier; the separate maintained verifier command below performs full collection. Candidate code can influence both.

### Prerequisites
Have the builder's instantiated launcher and authorization packet, a ceremony key kept out of agents, and a values file with real executable paths. The driver requires the reader-record commit at `HEAD`; its checks refuse stale or mismatched values.

### Run the maintained verifier and ceremony

Use the maintained `repin prepare-verifier` and `repin verify-candidate` commands described in the reference section below. The preparer defaults to installed P and committed C, takes the independently trusted signer fingerprint, prepares the hashes and clean target, and does not act as authority. The independent reader checks P provenance and the exact P/C bytes before collection.

The verifier runs P's full `_gate_manifest.py verify` with `-I -E -s`, an empty environment, immutable P for both anchor and trusted refs, `--require-anchor`, and no `--no-collect`. It requires your `YES` confirmation that the signing key is away. Candidate code executes during collection; these checks do not contain that code or establish host isolation.

A HOLD remains a HOLD. The command lists every exact protected HOLD and ordinary note. A human may record a bounded `proceed`, `stop` or `defer` disposition with a reason; a fresh full run refuses if P, C, report, collection or displayed items change. That record does not clear the HOLD or authorize signing; the existing ceremony's human approval remains required. New or unexplained HOLDs stop unless the Maintainer decides under the existing ceremony. The launcher does not run this verifier automatically.

After the independent reader has verified the packet and committed its record
alone at the read tip, use the maintained driver. It performs the packet,
record, launcher-template, values, roster, anchor, package and report checks;
shows the Y1–Y5 summary; repeats watched-file and key checks before stage 2;
signs once; and verifies the new signature against the packet's roster. It
stops on any mismatch. Do not `ssh-add` the key; the signer asks for its
passphrase. Do not invoke the launcher by hand or reproduce E/R/H/K
comparisons in shell. The driver does not push.

For an ordinary ceremony:

```sh
python scripts/repin.py ceremony --values <values-file> --ceremony-dir <ceremony-folder>
```

For a reviewed authority transition, first prepare its packet with
`transition-packet` and reader inputs with `prepare-reader` as described below.
After the reader's record-only commit, run the same driver with the independent
fingerprint of the prior signer:

```sh
python scripts/repin.py ceremony --transition --expected-fingerprint <SHA256:...> \
  --values <values-file> --ceremony-dir <ceremony-folder>
```

The transition mode authenticates the old anchor with the old roster and uses
the candidate roster for the new signature. It does not install a baseline or
move any real ref during testing. Publishing both refs atomically is a separate
Maintainer action after the ceremony. Nothing in this page calls
`_gate_reanchor.py promote`.
<!-- end of page -->

<!-- `dev/.cairn/trusted-activation.yml` and `dev/.cairn/promotion-authorization.yml`
     are Maintainer-supplied trust-root configs, absent unless the supervised
     re-anchor flow creates them.  Their claim-check exemption moved to
     dev/.cairn/claim-check-allow.json on 2026-08-27; this note names them so a
     reader still learns why the paths do not resolve. -->

## Prior verifier preparation

The short Stage 1 procedure uses these maintained entry points. Run preparation from the committed candidate checkout, with a new evidence-folder path whose parent already exists. The script verifies its own bytes equal `scripts/repin.py` at C, authenticates P's signed commit against the independently supplied fingerprint, and reads P's manifest and tool dependencies as raw objects. The prior manifest's allowed-signers file is verification input, never the sole trust root. The reader independently checks the expected signer source, P's signature and reachability, all emitted hashes, and the C target before collection.

```sh
python scripts/repin.py prepare-verifier \
  --trusted-repo <trusted-checkout> \
  --evidence-dir <new-evidence-folder> \
  --expected-fingerprint <independently-trusted-SHA256-fingerprint>
```

P defaults to `refs/cairn/gate-anchor`; C defaults to committed `HEAD`. The command creates a no-hardlink scratch clone at C and checks every tracked worktree byte against the raw C object, refusing symlinks, submodules, changed HEAD or a dirty tree. It extracts `_gate_manifest.py`, `_gate_preflight.py`, the manifest and the verifier/scanner dependency closure from P. It prints P, C, signer, preparer, verifier, observer and manifest digests. The preparer is candidate code under review, not authenticated authority.

The independent reader verifies the displayed P signer fingerprint against an independent trust source, confirms that fingerprint matches the verified signed commit, checks the P manifest and every extracted dependency against raw P objects, and checks the scratch target against exact C. Stop on any disagreement. Then run:

```sh
python scripts/repin.py verify-candidate \
  --evidence-dir <prepared-evidence-folder> \
  --expected-fingerprint <same-independently-trusted-SHA256-fingerprint> \
  --operator-confirms-key-away
```

This invokes P's `_gate_manifest.py` verifier through a small observer stored in the evidence folder. The observer's exact source hash is separate from the P tool hash and is part of the report binding; the independent reader checks it. The observer imports no candidate helper, calls P's original `_collect` once with the same target, records its returned node IDs and skip/xfail IDs, and returns that result unchanged. It writes a nonce-bound capture exclusively. Missing, malformed, duplicate, repeated or mismatched data refuses. The command checks the report's collection deltas against the captured collection and binds P, C, verifier, manifest, observer, report, collection, HOLDs and ordinary notes.

Before collection, the helper prints its command and asks you to type `YES` confirming the signing key is away. It invokes Python `-I -E -s` with `HOME=/nonexistent`, `PATH=/usr/bin:/bin`, and `LC_ALL=C`; P receives the verified external trusted repository, its full commit ID as both `--anchor-ref` and `--trusted-ref`, `--require-anchor`, and no `--no-collect`. The verifier process and target are rechecked after collection. Candidate tests can execute code on this machine and can influence the process; the helper does not claim containment.

If the P verifier returns a HOLD, the first run writes a `verifier-dispositions-<nonce>.json` template with every exact HOLD. Fill every row with `proceed`, `stop` or `defer` and a specific reason. Then rerun the full command with `--dispositions <that-file>`. Identical P/C/report/collection evidence can reuse the disposition; changed report, collection, tool bytes or items require fresh review. A complete disposition record records a human choice but does not clear the verifier's HOLD, waive it automatically or authorize signing. The Maintainer's later ceremony approval still controls. A verifier error, missing collection, malformed capture, failed raw-byte check, new unexplained HOLD or changed evidence is a stop.

## Preparing reusable inputs

The builder can prepare the values file and a fresh package path with
`python scripts/repin.py prepare-values --output <new-values-file> --signing-key <public-key> --home <home> --ceremony-dir <outside-checkout-directory>`. The command prints the values-file digest. The independent reader checks every path and digest; the launcher validates the file before use. After a tool upgrade a recorded executable path goes stale, and that is not a malfunction: prepare and check fresh values. No secret is written.

For an ordinary ceremony, `python scripts/repin.py packet --ceremony-dir <directory>` prepares the packet and launcher. `python scripts/repin.py prepare-reader --ceremony-dir <directory> --output <new-reader-inputs-file> --expected-fingerprint <independently-trusted-SHA256-fingerprint>` prepares the candidate and member hashes for the independent reader. These inputs are not a review or an authorization. The reader verifies the underlying objects and records their review at the read commit before the Maintainer acts.

When an AST pin is owed, run `python scripts/repin.py package --ceremony-dir <directory>` at the read commit before the reader writes their record. For a reviewed missing symbol, add `--delete-symbol <exact-baseline-key>` for each missing key; omitted or extra keys refuse. Prepare reader inputs after the package so they include its digest. Once the independent reader has verified and committed the record alone on that read commit, `python scripts/repin.py apply-reviewed-pin --ceremony-dir <directory>` checks the binding, asks the Maintainer before writing, and stops with an exact-path commit instruction. It does not commit. Run `python scripts/repin.py commit-reviewed-pin --ceremony-dir <directory>` and approve the exact paths to make that commit. Then prepare fresh ceremony evidence for the new candidate.

These commands prepare inputs; the `ceremony --transition` command above carries the reviewed changed-authority sequence through the same maintained checks and signature verification. It authenticates the prior anchor using its old roster and still requires the independent reader and Maintainer decisions.

## The first ceremony

The first ceremony has no anchored E7 scan. Prepare and review its packet and
reader record, then run:

```sh
python scripts/repin.py ceremony --first-run --reviewed-commit <reviewed-commit> --values <values-file> --ceremony-dir <ceremony-folder>
```

The driver states the checks it cannot establish and asks for the Maintainer's
decision; it does not waive an unreviewed change.

## Packet format

`repin packet` writes the packet and launcher. The packet uses schema
`cairn-authorization-packet/v1`, a provenance field, the artifact
`bootstrap/reanchor.sh`, its `artifact_sha256`, and one `member` digest per
closure file. The launcher contains the packet's SHA-256 in its one
`@PACKET_SHA256@` slot. The packet carries no candidate id; the reader record
binds the exact candidate.

## What each comparison protects, and what it does not

| Check | It protects | It does not |
|---|---|---|
| E1, R3 | you run the launcher and packet the reader recorded | that the reader read well |
| E2 | the commit you sign is the commit the report describes | that the commit is safe |
| E3 | the package you confirm is the bytes the report described | that the package is harmless |
| E4 | your key is in the packet-pinned candidate roster | that the roster change itself was safe |
| E5, R1 to R4 | the answers come from git objects read before stage 1 starts the candidate's tests, with no replace entry, hook or filter, not from repository state those tests could have written; the launcher is the reviewed template with one slot filled; the record is the one commit on what was read and names this packet, launcher and these files | that the template is safe; what the reader wrote in the record; code already running as you |
| E6 | the programs run before any candidate byte are the ones you named | the bytes of those programs: a tool you own can be replaced; and `--scan-digest` (E7) runs the anchor's checker with `/usr/bin/git` from `PATH`, not the git your values file names |
| E7 | the digest the report prints is the one the anchor's own checker computes over this range, started by the launcher from raw objects before candidate code and compared before signing | that the hits listed in the report are the scan behind that digest (it binds the digest only, and the report's line saying who made the scan is the report's own claim); a change that matches no scan pattern; test files and pytest settings, which stage 1 runs and the scan does not read; the first ceremony, which has no anchored scan |
| H | the values file and the Python are the bytes they were before stage 1 | Python's library folder, your other tools, or a change made and undone between the two hashes; nor a process stage 1 left running, which could change either file after the second hash, because `repin` only checks the hash and cannot stop it |
| K | no agent, the login session's included, holds your key when you run stage 1 and stage 2 | an agent started in between |
| V | the new anchor carries a good signature by a key the roster lists | that the key was yours alone: you compare its fingerprint with E4 |
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
| RA-17 | stage 2 validates the package against your digest and re-verifies its own bytes; it starts no candidate test, but files stage 1 left on this machine can still be loaded (see H) |
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
