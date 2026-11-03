# Changelog — {{project_name}}

Written in [Cairn Plain Language 1.0](dev/agent_collaboration.md).

Use this file to describe releases for people who use your project. Write new
work under **Unreleased**. At release, move those notes under the new version
and date, then open a fresh **Unreleased** section.

This is project-owned living state. Cairn tracks it for upgrades but does not
hash-attest its content, so ordinary release-note edits need no re-pinning.
Review its changes through Git; executable and governing Cairn files retain
their integrity checks.

Group a change under **Major changes** if users would notice it or need to act.
Put a security fix or removal there too. Put other changes under **Minor
changes**. Start each entry with one type, in this order: **Added**,
**Changed**, **Deprecated**, **Removed**, **Fixed** or **Security**. Give a
major change a short title of two to five plain words after its type, in one
bold run, then the description: `**Added: Export to CSV.** Results can now be
saved as a spreadsheet.` A minor change has no title: its type, then ` — ` and
a short description. Use plain language and link to useful detail when it
helps.

If this project already has a changelog, you can keep its history unchanged.
You may optionally adapt it to this format if you choose. To start fresh,
first save the old file at a safe, separate path, then remove it from the
project root before installing this one. Keep the saved history.

On an upgrade, a root `CHANGELOG.md` that is not yet tracked by Cairn blocks
the new template. Run `upgrade --stage`, review the `.ours` and `.theirs`
copies, then use the displayed `--adopt-collisions` command from the target
Cairn tree, without `--to`, to keep your existing file unchanged as a tracked
fork. Re-stage and review before applying. If you chose to adapt your history,
edit it, then run `upgrade --stage` again. Review the new `.ours` and `.theirs`
copies and use the newly displayed `--adopt-collisions` command. Its digest is
bound to the staged bytes, so the earlier command is refused after an edit. To
start fresh, first save the old file separately, remove it from the root, then
re-stage and review the new template. A file tracked under another source, a
link, a folder or another ineligible path needs manual resolution; collision
adoption does not apply.

## Unreleased

### Major changes

### Minor changes
