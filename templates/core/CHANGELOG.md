# Changelog — {{project_name}}

Written in [Cairn Plain Language 1.0](dev/agent_collaboration.md).

Use this file to describe releases for people who use your project. Write new
work under **Unreleased**. At release, move those notes under the new version
and date, then open a fresh **Unreleased** section.

Group a change under **Major changes** if users would notice it or need to act.
Put a security fix or removal there too. Put other changes under **Minor
changes**. Start each entry with one type, in this order: **Added**,
**Changed**, **Deprecated**, **Removed**, **Fixed** or **Security**, followed
by ` — ` and a short description. Use plain language and link to useful detail
when it helps.

If this project already has a changelog, you can keep its history unchanged.
You may optionally adapt it to this format if you choose. To start fresh,
first save the old file at a safe, separate path, then remove it from the
project root before installing this one. Keep the saved history.

On an upgrade, a root `CHANGELOG.md` that is not yet tracked by Cairn blocks
the new template. Run `upgrade --stage`, review the `.ours` and `.theirs`
copies, then use the displayed `--adopt-collisions` command from the target
Cairn tree, without `--to`, to keep your existing file unchanged as a tracked
fork. Re-stage and review before applying. If you chose to adapt your history,
review the changed bytes before adopting them. To start fresh, first save the
old file separately, remove it from the root, then re-stage and review the new
template. A file tracked under another source, a link, a folder or another
ineligible path needs manual resolution; collision adoption does not apply.

## Unreleased

### Major changes

### Minor changes
