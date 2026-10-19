# UPGRADE.md — folding new Cairn doctrine into a customized tree

Cairn keeps evolving. An adopting team that bootstrapped months ago is
frozen at the version they installed — unless they can pull new doctrine
forward **without losing their local customizations**. This is that path:
a **token- and slot-aware 3-way merge** that folds upstream changes into
your tree, preserves your filled `cairn:slot` bodies and tunings, and
surfaces genuine "local optimization vs. new doctrine" conflicts for
review instead of silently clobbering or skipping them.

The upgrade is **never an auto-overwrite**. It stages a review surface;
you (or your agent) review, resolve any conflicts, and apply — and the
applied upgrade is itself a tracked change in your repo that goes through
your own review lifecycle.

## Moving to one review at every stage

Cairn now ships one review stance and its nine-question evidence sweep in
`dev/agent_collaboration.md`, with the governing pointer in `AGENTS.md`.
Adding a second agent type to the team roster does not call an outside read;
only the Maintainer can ask for one on a named piece of work. The upgrade
merges these words with your own, so inspect both conflicted and cleanly
merged files before applying. A clean merge can preserve local language from
the former two-kind review system, including a claim that a second agent
always needs higher capability; Cairn does not flag those sentences. Search
the files you actually have for the old role and tier words, for example:

```
grep -n -i -E 'internal|external|tier' AGENTS.md dev/agent_collaboration.md
```

Treat hits as prompts to read, not instructions to replace every use of the
words: also inspect `dev/collaboration_agreement.md` if your project has one;
`External read` remains the name of a Maintainer-called read. In the
two adopter rehearsals, one project's `AGENTS.md` had a one-line conflict:
keep its local doctrine-gating bullet and the new upstream sentence above it.
That project's loop document needed the shipped sweep plus its domain probes,
without a second ledger or clean-pass rule. The other project's collaboration
agreement was entirely local text and conflicted as a whole; keep that local
file. These
are examples of what to inspect, not automatic resolutions for your tree.
The module-body-coverage probe now lists 11 unmatched old heading names for
`dual-review` (8 before this change); the three added names moved under other
headings rather than losing their rules.

## The two on-disk artifacts the install leaves

Installing (or upgrading) writes two **tracked** artifacts into your
target's `dev/`:

* **`dev/.cairn/cairn-lock.yml`** — a machine lockfile (the *upgrade ancestor* +
  the install-side provenance record). It pins the Cairn version + commit,
  the resolved profile, the module roster, and **per file**: source,
  destination, the `verbatim` flag, the content hash as written, and the
  substituted token values. It is **tool-owned: regenerate-only — do not
  hand-edit.** (It is JSON-encoded, which is valid YAML, so it round-trips
  without any YAML library.)
* **`dev/.cairn/base/`** — a cache of the **raw** upstream templates for
  the mergeable `.md` files, exactly as they stood when installed. This is
  the merge's *base*, so the upgrade works under any distribution mode
  (git clone, release tarball, copied tree) — it never needs Cairn's git
  history. It is tracked and hidden; the lockfile lists every cached path
  + hash so it stays auditable. Verbatim scripts are **not** cached (they
  use a hash policy, below), which keeps the cache to just the mergeable
  set.

## The workflow

```
python bootstrap/scaffold.py upgrade --target <repo> --plan     # 1. inspect
python bootstrap/scaffold.py upgrade --target <repo> --stage    # 2. stage
#    ... review dev/.cairn-upgrade/, resolve any conflict markers ...
python bootstrap/scaffold.py upgrade --target <repo> --apply    # 3. apply
python bootstrap/verify_integrity.py --target <repo>            # 4. verify
```

* **`--plan`** is **strictly read-only**: it classifies every tracked file
  (clean / conflict / slot-removed / review-only / verbatim-* /
  up-to-date), lists new modules available since install (opt-in only) and
  modules removed upstream, and prints any flags. It writes **nothing**.
* **`--stage`** writes the merged/updated results into the **ephemeral**
  `dev/.cairn-upgrade/` staging directory (auto-seeded into your
  `.gitignore`) along with stage metadata. Originals are untouched.
  Open the staged files, resolve any `<<<<<<< ours … >>>>>>> theirs`
  conflict markers by hand.

  **What's in the staging directory** — review and edit only the first:
  * `files/` — **the merged result** (your customizations + the upstream
    changes). This is what you review, resolve conflicts in, and apply.
  * `review-only/` — for each **review-only** file (a customized file with
    no recoverable base — e.g. an `--init-lock` migrated tree — or a tracked
    file missing on disk), the upstream version (`<dst>.theirs`) alongside
    your current copy (`<dst>.ours`, omitted when the file is missing) so you
    can merge the change **by hand** into the original. These never merge
    automatically and `--apply` never swaps them; they record the work you
    still owe.
  * `new-base/` — the upstream templates that will become the **next
    base-cache** after `--apply`. Reference only; do **not** edit these.
  * `stage-metadata.json` — the stage record `--apply` checks against the
    safety contract. Machine-owned; do not edit.
* **`--apply`** swaps the resolved staged files into place and cleans the
  staging directory — but only under a **safety contract**: the stage must
  have been produced from the current lockfile (same tokens + roster), the
  originals must be unchanged since `--stage`, **no conflict markers
  may remain**, and **no review-only file may be left unreconciled**. A tree
  with markers, or with outstanding review-only files, is never applied —
  only a resolved tree advances the lockfile.

  **The completion gate.** An upgrade is **not complete** until every
  review-only / customized file has been reconciled against the new upstream.
  `--apply` enforces this: it **fail-closes** (mirroring the conflict-marker
  gate) when review-only files remain, so a `--stage` → `--apply` cannot
  silently advance the lockfile to the new version while your customized
  doctrine never landed. Once you have merged each `review-only/` pair into
  its original by hand, re-run `--apply --ack-review-only` to acknowledge them
  and apply. (Without that flag the gate holds — there is no way to advance
  the version past an unreconciled customized file by accident.)

  After applying, re-run a clean install (or `--stage`) to refresh the
  lockfile + base cache to the new version.

* **`verify_integrity` (step 4)** checks the tree you now have against the
  lockfile: it recomputes each recorded file's SHA-256 and exits non-zero on
  a mismatch. **Only a person following these steps runs it.** `--apply` does
  not call it and Cairn has no CI that does, so if you skip the step nothing
  notices. Run it from the Cairn folder you upgraded with, and point
  `--target` at your project.
* **The slot note.** After it has fixed its result and printed its report,
  `verify_integrity` prints a short advisory to stderr, every line starting
  `slot note:` (it does not run when the lockfile is missing, unparseable or
  records no files). It lists the slots in your project that still hold the
  placeholder text Cairn shipped (a *slot* is a section of a file that your
  project fills in), and it always includes a coverage line saying how many
  files it could check and why it could not check the rest. A note with no
  slots listed, plus its coverage line, means *none found among what it could
  check*, never *none exist*. The note never changes the result
  `verify_integrity` returns, and it reports state, not obligation: it does
  not say a slot is required. The note always writes to stderr. If whatever
  reads stderr has already gone away (`grep -q` and `head` do this), the note
  stops writing and the exit code is unchanged.
* **Known gap.** A placeholder that an upgrade rewords reads as filled: the
  note compares your slot with the base copy recorded for it, and after an
  upgrade the base copy holds the new wording while your slot still holds
  the old.

`--to <ref>` upgrades to a specific Cairn git ref **only when your Cairn
source is a git checkout** carrying that ref; a packaged release (tarball
/ zip) can upgrade only to the currently-running Cairn tree.

## Recording an edit you made

After you fill a slot, or otherwise edit a file Cairn installed,
`verify_integrity` reports that file as `modified (hash mismatch)`: the
lockfile still holds the hash of the file as Cairn wrote it. That is
expected. Recording the edit is how you tell the lockfile that the new bytes
are the ones you meant. **Recording attests the whole file, not only your
slot**, so read before you record.

1. **Read the whole file first.** Open the file inside your project, under
   the `--target` you passed -- not the same-named file in the Cairn folder
   you ran the check from. Make sure your own fill is in what you read; if
   it is not, you are reading the wrong copy. `verify_integrity` keeps only a hash
   of each file, so nothing it prints can show you what changed: you are the
   check. Confirm that the only change is yours.
2. **Know what reading can and cannot catch.** Reading finds a line you know
   is not yours, such as an instruction to download and run a script. It does
   not reliably find a small rewording of text Cairn itself shipped, because
   the check keeps no copy of that text to compare against. Comparing with a
   copy you trust is an aid, never proof.
3. **`git log -p -- <path>` is supplementary.** It shows committed history
   only, never uncommitted edits, so it cannot stand in for reading the file
   as it is now.
4. **Then record the file:** `python bootstrap/scaffold.py upgrade --target
   <repo> --finalize <path>`. This records the whole file, not only your
   slot. The scoped form (with a path) also skips the dirty-tree guard that a
   bare `--finalize` applies, so it records whatever is on disk at that
   moment. Commit the lockfile afterwards.

This section describes the command. It does not claim that any command shows
you what changed.

## How the merge protects your customizations

* **Slots are adopter-owned.** Content between `cairn:slot NAME` and
  `cairn:end NAME` is yours. Before merging, the tool copies your slot
  bodies into the base and upstream versions so all three agree inside the
  slot — the surrounding doctrine merges, your slot body is preserved
  verbatim, and you never get a spurious conflict inside a slot. A slot
  **added** upstream arrives with its placeholder for you to fill; a slot
  **removed** upstream whose body you had filled is **flagged** (not
  silently orphaned).
* **Tokens re-substitute.** The base is reconstructed by substituting your
  recorded token values into the cached raw template, so token sites don't
  conflict. A **new** upstream token with no recorded value is surfaced as
  *needs a value*.
* **Verbatim scripts use a hash check, not a text merge.** A shipped
  reference script (`claim_check.py`, `intent.py`, `lifecycle_metrics.py`,
  `lifecycle.py`, `link_check.py`, `sync_doc_snippets.py`) is meant to be
  byte-for-byte. If yours is unmodified it updates to the new upstream; if
  you forked it, the upgrade **flags it and does not clobber** — a forked
  tool may break against new doctrine, so that is a real decision for you to
  make.
* **A linked `.gitignore` is refused, wherever it points.** Install, `--stage`,
  `--apply` and `--adopt-module` append ignore entries to `.gitignore`, and
  appending through a link would change the file behind it. If your
  `.gitignore` is a link (to a file outside the project, or to one inside it),
  each of them stops before writing anything and tells you to replace the link
  with a regular file, then re-run. `--plan` writes nothing and is not
  affected. The rule is the same for every link on purpose, so a shared
  `.gitignore` kept by link has to become a real file first.
* **A linked `dev/` folder is refused too.** The same rule covers the empty
  `dev/` folders the install creates (`dev/` itself and each folder under it,
  such as `dev/plans` or `dev/rules`). If any of them is a link, the install
  stops before creating a single folder, at either end of the link, with a
  `ScaffoldSecurityError` traceback and exit 1. That refusal prints no
  remedy line: replace the link with a real folder, then re-run.
* **The session helper refuses links and unsafe table rows.** `tools/session.py`
  (`session-start`, `session-end`) never writes through a link or outside the
  project. If `dev/`, `dev/reflections` or `dev/.cairn` is a link, `session-end`
  stops with exit 1 and a one-line note that names the link and says to replace
  it with a real folder; the full handoff refuses before it prunes anything, and
  `tools/prune_reflections.py` refuses the same way (exit 2). On a machine that
  cannot make links, the copy fallback also stops, with a note, if `.gitignore`
  is a link or is read-only (add the line yourself, or make the file writable);
  `session-start` carries on. A row in `.agents/skills/_data/vendor_targets.yml`
  must name a folder called `skills`, inside another folder, outside `.git` and
  `dev/.cairn`, using letters, digits, dots, dashes and underscores only; any
  other row is skipped with a warning that names the rule. The installer's own
  check of a row is looser (any relative path without `..`), so a row the
  installer accepts can still be skipped here; that mismatch is known and the
  installer is unchanged.
* **A committed interpreter binding is not used.** `dev/.cairn/local-env.json`
  belongs to one machine and is meant to be ignored by git. If git tracks it, or
  it sits behind a link, or git cannot be asked, `session-start` and
  `session-end` do not run the program it names: they use the current
  interpreter, say so on stderr, and name the fix. The fix is `git rm
  dev/.cairn/local-env.json` (which deletes the file too), add it to
  `.gitignore`, commit, then re-run the install to write a binding for this
  machine. Checking out a branch that tracks the file replaces your own ignored
  binding without a word; this check is what notices.
* **The lifecycle skills participate exactly like `core/`.** The canonical
  `.agents/skills/*/SKILL.md` files ride the token-/slot-aware 3-way merge
  (base cache + provenance), and `tools/session.py` follows the verbatim
  hash policy above. The gitignored vendor fan-out copies (where symlinks
  are unavailable) are **regenerated** from the canonical source on upgrade. A
  copy you edited in place is **moved aside** to `<file>.diverged.bak` (your
  edit is kept there) and regenerated, with a warning — the canonical
  `.agents/skills/` source is the one to edit. The install and the upgrade
  **refuse, and write nothing**, if a copy's name (or its `.diverged.bak` name)
  is a link or sits under one, is a folder, or has a file where a folder must
  go. The message names the path relative to the project; remove or move that
  item, then run `python tools/session.py session-start` (or install again). An
  `upgrade --apply` that meets this still finishes the upgrade and prints the
  refusal as a warning, because running the upgrade again does not redo the
  fan-out. (The bullet above is the *already-tracked* case; if your lockfile
  predates the skills, see the next section — they are acquired, not skipped.)

## New core-like files (and skills) added upstream

`core/` files and the lifecycle skills install **unconditionally** — they are
not opt-in modules. When Cairn adds a file to that tier *after* you installed
(the lifecycle skills are the first such case — an adopter who bootstrapped
before they existed), `upgrade` **brings it in** rather than silently omitting
it. `--plan` / `--stage` list these under **`new core/skills (added)`**, and
`--apply`:

* writes the file (a mergeable `SKILL.md` is token-substituted + base-cached
  like any `core/` doc; a verbatim CLI such as `tools/session.py` is
  hash-tracked),
* **records it in the lockfile** so the next upgrade tracks it, and
* fans the skills out to your in-use vendor read-paths (e.g. `.claude/skills`)
  and seeds their `.gitignore` entries — exactly as a fresh install does.

Detection keys on the **source template**, not the destination, so a file you
installed under a renamed destination (the vendor wrapper `VENDOR.md` →
`CLAUDE.md`) is recognized as already-present and never re-added. Only the
unconditional core/skills tier auto-adds; **new modules stay opt-in** (listed
under "new modules available (opt-in)", adopted deliberately — see below).

## Adopting a hand-placed module

A module is **opt-in**, so it is never auto-added on upgrade. If you hand-placed
a module's files (or filled its forkable template) without recording it in the
lockfile, adopt it explicitly:

```
python bootstrap/scaffold.py upgrade --target <repo> --adopt-module <name>
```

This records each of the module's files in the lockfile (`src` / `dst` /
`verbatim` / on-disk `hash`; a mergeable file also gets a `base_cache` of the
raw upstream template + `base_hash`) and adds `<name>` to the roster, so the
module **3-way-merges on later upgrades** instead of staying an untracked fork.
It records your **on-disk** content as the hash (a filled forkable stays your
content; the base cache is the raw template, so the fill reads as a local
modification, not a fork). A spec whose `dst` is missing is installed from the
template first. Adoption fails closed on an unknown module name and is a no-op
if the module is already recorded. (`init` would also record it, but its
lockfile writer fail-closes on a customized tree — `--adopt-module` is the path
for an existing adopter.)

## Migrating a tree installed before upgrade support

If you bootstrapped before this capability existed, or copied the kernel
in by hand, your tree has no lockfile. Create one:

```
python bootstrap/scaffold.py upgrade --target <repo> --init-lock
```

This synthesizes `dev/.cairn/cairn-lock.yml` from your on-disk content and your
fidelity manifest's `cairn_commit`. **Important limitation:** the fidelity
manifest records token *names*, not the *values* substituted at install,
so for token-substituted files the install-time base **cannot** be
reconstructed. Those files are marked *unrecoverable-base* and upgrade as
a **review-only diff** (you compare and merge by hand) — never a pretended
3-way merge. Verbatim scripts are hash-tracked normally. A re-install does
not recover a clean base: over an existing tree it skips every file already
there and writes no lockfile (unless every file still matches a clean install),
and `--force` overwrites what you wrote. Keep the migrated lockfile and merge
the review-only diffs — `upgrade --stage` writes both versions side by side.

## Migrating your plan-review records to the gated schema

The plan-review gate used to clear on the **presence** of a section whose
heading began `Plan review`. It now reads the **record**: a bare
`## Plan review` container, an `### Plan review` at H3, an undated pass and a
`## Plan reviewers` heading all cleared before and none of them clears now.
The rules are in `doctrine/plans.md` > *The record schema*; this section is
what you have to do about it.

**Behaviour and policy ship together.** A verbatim manifest source — the
session kernel (`templates/skills/_lib/session.py`, installed as
`tools/session.py`) is the current example — arrives in the same pass as the
doctrine it backs, so there is no window in which your tree carries one and not
the other.

**What a pass must now carry.** A conforming pass is a heading

```
## Plan review -- <reviewer> -- YYYY-MM-DD
```

at **H2** (an appended record nests under the file's *last* H2, so H2 is the
only level the append-only lifecycle can actually produce), with **two
attestation lines inside its body**, one line each, full-line anchored:

```
**Tier**: <Internal|External>
**Findings**: <none|raised>
```

Those are the two new field names, and there is **no default for either**: a
value outside the vocabulary, an absent field, and a field written twice are all
violations — the last one even when the two occurrences agree. The tier is read
from the `**Tier**:` line and **from nowhere else**: not from the reviewer's
name, not from a `(<role>)` parenthetical, not from any agent registry. A human
reviewer declares `**Tier**: External` in the same line-shape an agent does.

**The date must be a real date.** It is parsed strictly, not shape-matched, so
`2026-99-99`, `2026-02-30` and `0000-00-00` are each a `malformed date`
violation while `2028-02-29` is accepted.

**The required tier is read from the first parenthesised group only** of your
plan header's `**Plan review**:` line: `required(...)`, with `*`, `_` and
backticks stripped, the first alphabetic word taken and case-folded, and
`internal` or `external` required. Text after the closing paren is ignored, and
text after the first word *inside* the group is a lens annotation — so
`required(**Internal**, security lens)` and
`required(Internal + Internal Security Review)` both resolve to `internal`.
Negations fail closed: `required(not External)` is a violation, not an External
requirement.

**The legacy exemption is a fixed enumeration of pre-existing records — not a
dated grace period, and not an epoch.** Records that predate the schema are
exempt from the attestation rules by *membership in a generated manifest* keyed
by plan stem, with an occurrence count per heading. There is **no cutoff date
and no epoch constant to look up**: nothing in the gate compares a heading's
date to anything, so writing an older date buys you nothing, and re-appending a
heading byte-identical to an admitted one is refused as occurrence
`count + 1`. If you read an upgrade note or a doctrine passage that names a
review-schema epoch, it is describing a design that was refused on review and
removed.

**What that means for your tree.** Cairn's manifest enumerates *Cairn's* old
records, not yours, so **every** review-required plan in your tree is judged by
the full schema from the moment you upgrade. The consequence: a plan already
past `open` whose review predates the schema will be reported. Append-only
forbids editing that landed review, so the repair is a **new** conforming pass
appended to the plan (a re-read, by whoever performs it, with the two
attestation lines) — not a rewrite of the old one. If instead you want your own
pre-existing records enumerated the way Cairn's are, that is a code change to a
committed constant in your installed checker, and it shows up as a code diff in
review; it is deliberately not something a plan file can ask for.

**What the gate does not do.** It checks that a record is *conformant*. It
cannot establish that the declared review happened, that the named reviewer
performed it, or that the declared tier is true — it attests that a tier was
**declared**. It is a conformance backstop, and the structural independence
itself stays a human judgement.

## The lockfile and the fidelity manifest

The lockfile is the **machine authority** for what is installed (files,
modules, tokens, hashes). The human **fidelity manifest**
(under `dev/.cairn/`, see `fidelity-check.md`) is the audit *narrative*; it
**cites** the lockfile's version/commit rather than re-listing the
inventory. `upgrade` warns if the manifest's citation is stale. Keep the
two one-way: regenerate the lockfile with the tool; update the manifest's
citation by hand.

## Adding a lockfile field without bumping the schema

The lockfile's top-level fields today: `schema`, `cairn_version`,
`cairn_commit`, `source_repository`, `source_licenses`, `profile`,
`modules`, `optional_templates`, `tokens`, `files`, plus the
writer-varying `migrated` (present only on a lockfile synthesized by
`upgrade --init-lock`).

**The rule.** An additive **optional** top-level field does not bump
`schema` — readers must use `.get()` with a default and tolerate
unknown keys. A removal, rename, or change of meaning of an existing
field does bump `schema`, and a bump is the point a reader-side
validator becomes mandatory. `migrated` is the existing precedent this
rule codifies, not a new invention: it is absent from every fresh
install, written only by `upgrade --init-lock`, and has coexisted with
`schema: 1` since it shipped.

**Why `dev/.cairn/profile.yml` takes the opposite disposition.** The lockfile
tolerates an unknown key because it *carries* a `schema` field: a reader can
tell "a field I do not know" from "a file written by a newer engine". The
profile refuses one, because until now it carried no version signal at all —
so an unknown key there was indistinguishable from a typo, and a typo silently
dropped whatever it was meant to set. The profile's newly-reserved `schema:`
key is what buys the lockfile's tolerance later; it does not buy it today
(see `bootstrap/BOOTSTRAP.md` Appendix B, "Schema rules").

**`source_repository` / `source_licenses` are declared, not
attested.** Both are read from the source tree's `CITATION.cff` at
install/upgrade time — `source_repository` from its `repository-code:`
line, `source_licenses` from its `license:` block — and are
**derived** readings of that file (the parser filters as it reads; it
is not a byte-for-byte copy), not attestations of checkout origin or
installed-file licensing. A fork with a stale or false `CITATION.cff`
produces a stale or false declaration; the fields' authority is
exactly that of the file they were derived from, no more. **Signed,
name-bound release tags** (from `v0.4.0` onward), the observed
`cairn_commit`, and the per-file hashes remain the lockfile's actual
origin/integrity controls (see [`PROVENANCE.md`](PROVENANCE.md)'s
"Controls" section, and its bootstrap procedure for how to check the
tag). The second branch of that control — an unsigned release commit
vouched for by author metadata and by branch protection — was
**retired**: a git author field is free text, branch protection is
invisible from a clone, and neither is something an adopter can run.

## The forked-facade advisory, and what each note means

Some tools Cairn installs are **facades**: a thin launcher (`tools/intent.py`)
over an engine package beside it (`tools/_intent/`). If you edit the launcher
but keep the engine, you run an un-maintained fork of the launcher while the
maintained engine sits dormant, and upstream engine fixes never take effect.
`verify_integrity` and `upgrade` both surface that as a **NOTE**. It is
**advisory only**: it never blocks, never mutates, and never changes an exit
code — a genuinely forked facade still passes `verify_integrity`.

**The comparison bytes come from the caller, not from your tree.** For a record
the advisory examines, the verdict is decided by reading two files and comparing
them: the installed file under your tree, and the upstream template in the
**Cairn checkout you ran the command from**. When that comparison cannot be
made, the note is **kept** and marked `UNCONFIRMED` — never dropped. Once a
record is examined, nothing it says about itself — not `hash`, not `base_hash`,
not its `src` — can stand in for that comparison or make a difference go away:
the **only** thing that drops a note is the two reads coming out
byte-identical. (The one lockfile field that can *silence* a note already
raised is `fork_acknowledged`, and only at verify time — see the end of this
section.) That is why the note prints the root and version it compared against
(**R1**): the operator can see whose bytes decided it. What it does *not*
establish is that the checkout is authentic; see
[`PROVENANCE.md`](PROVENANCE.md) for the controls that do.

**What your lockfile still decides is *which* records get examined.** The
advisory only looks at a record that is marked `verbatim`, names a `.py`
destination with an engine package installed beside it, and carries **both** a
`hash` and a `base_hash` that *differ* — the install-time "this file changed
since we wrote it" signal. A record that omits either hash, or records the two
as equal, or drops its `verbatim` mark, is never examined at all, so a fork
hidden that way produces no note. That is a **known limitation of the
advisory**, stated rather than discovered: it is what "advisory" means here.
Closing it would mean not keeping an install-time baseline in the lockfile,
which is a separate change. So read the absence of a note as *"nothing was
flagged among the records the advisory examined"*, never as *"every installed
facade matches upstream"*. Cairn ships no check that makes the stronger
statement today: `verify_integrity`'s hash attestation compares your files
against the hashes **your own lockfile** records, which is a different claim
again.

Three shapes of note:

* **`is forked from upstream`** — the two reads disagreed. The note names the
  templates root and Cairn version it compared against. This is the one that
  means what it says.
* **`UNCONFIRMED`** — the difference is measured against the **install-time
  baseline in the lockfile**, and could not be checked against upstream. The
  note says why. `base_hash` ratchets forward on every `--finalize`, so an
  unconfirmed difference is *not* evidence of an upstream fork; treat it as
  "not checked", not as "forked". You will see it when: `upgrade --to <ref>` is
  used, because that ref's templates are not materialized on disk (**R3**); the
  destination is absent from the trusted install manifest, so no upstream
  template names it (**R4**); or a file on either side is missing, unreadable,
  or fails a containment check.
* **`source-version skew`** — an extra line on a note that already exists,
  saying the comparison used a different Cairn version than the one your tree
  records installing from. It is an annotation; it never creates a note.

A fourth line may be appended to a note that already exists: your record's own
`src` does not name the upstream template the trusted manifest names, so the
recorded `src` was ignored (**R9**). Like the skew line, it annotates a finding
rather than creating one — a relabelled `src` whose on-disk bytes actually match
upstream produces no note at all.

To silence a deliberate long-term fork at verify time, set
`"fork_acknowledged": true` on its lockfile record. `upgrade` re-surfaces it
regardless: an upgrade is the active decision point.

## A note on secrets

Cairn templates must **not** introduce secret-bearing substitution tokens
— the lockfile records token values into a tracked file, so a secret would
leak. The lockfile writer refuses obvious secret-like token names
(`password`, `secret`, `token`, `key`, …) unless explicitly allow-listed.
See `SAFETY.md`.
