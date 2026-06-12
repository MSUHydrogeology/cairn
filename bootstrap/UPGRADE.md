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

`--to <ref>` upgrades to a specific Cairn git ref **only when your Cairn
source is a git checkout** carrying that ref; a packaged release (tarball
/ zip) can upgrade only to the currently-running Cairn tree.

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
* **The lifecycle skills participate exactly like `core/`.** The canonical
  `.agents/skills/*/SKILL.md` files ride the token-/slot-aware 3-way merge
  (base cache + provenance), and `tools/lifecycle.py` follows the verbatim
  hash policy above. The gitignored vendor fan-out copies (where symlinks
  are unavailable) are **regenerated** from the canonical source on upgrade,
  with a divergence guard that **warns rather than clobbers** a copy you
  edited in place — the canonical `.agents/skills/` source is the one to
  edit. (The bullet above is the *already-tracked* case; if your lockfile
  predates the skills, see the next section — they are acquired, not skipped.)

## New core-like files (and skills) added upstream

`core/` files and the lifecycle skills install **unconditionally** — they are
not opt-in modules. When Cairn adds a file to that tier *after* you installed
(the lifecycle skills are the first such case — an adopter who bootstrapped
before they existed), `upgrade` **brings it in** rather than silently omitting
it. `--plan` / `--stage` list these under **`new core/skills (added)`**, and
`--apply`:

* writes the file (a mergeable `SKILL.md` is token-substituted + base-cached
  like any `core/` doc; a verbatim CLI such as `tools/lifecycle.py` is
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

If you bootstrapped before this capability existed, your tree has no
lockfile. Create one:

```
python bootstrap/scaffold.py upgrade --target <repo> --init-lock
```

This synthesizes `dev/.cairn/cairn-lock.yml` from your on-disk content and your
fidelity manifest's `cairn_commit`. **Important limitation:** the fidelity
manifest records token *names*, not the *values* substituted at install,
so for token-substituted files the install-time base **cannot** be
reconstructed. Those files are marked *unrecoverable-base* and upgrade as
a **review-only diff** (you compare and merge by hand) — never a pretended
3-way merge. Verbatim scripts are hash-tracked normally. For clean 3-way
merges on those files, re-install from an upgrade-capable Cairn so a full
lockfile + base cache is written.

## The lockfile and the fidelity manifest

The lockfile is the **machine authority** for what is installed (files,
modules, tokens, hashes). The human **fidelity manifest**
(under `dev/.cairn/`, see `fidelity-check.md`) is the audit *narrative*; it
**cites** the lockfile's version/commit rather than re-listing the
inventory. `upgrade` warns if the manifest's citation is stale. Keep the
two one-way: regenerate the lockfile with the tool; update the manifest's
citation by hand.

## A note on secrets

Cairn templates must **not** introduce secret-bearing substitution tokens
— the lockfile records token values into a tracked file, so a secret would
leak. The lockfile writer refuses obvious secret-like token names
(`password`, `secret`, `token`, `key`, …) unless explicitly allow-listed.
See `SAFETY.md`.
