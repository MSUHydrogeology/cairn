# Install, customize and upgrade in a disposable copy

This exercise installs the real v0.7.0 scaffold and upgrades to a local current
Cairn checkout. It needs Python 3.11+, Git, a local Cairn checkout containing
v0.7.0 tag object `49dfa217102545d44e57190a48941cabcec422c3` (commit
`2f9fda2ba410077e2523547b8ef3c055257ea61d`), and a current checkout
containing that history and the layout migration. No network or agent account
is needed. Run from the current Cairn repository root. Use a new temporary
folder; never point these commands at a real project. The target is an exercise,
not a verified release installation; see [upgrade guidance](../../install/UPGRADE.md)
for release verification and real project review.

```bash
WORK=$(mktemp -d)
git clone --no-hardlinks --quiet . "$WORK/old"
git -C "$WORK/old" checkout --quiet 2f9fda2ba410077e2523547b8ef3c055257ea61d
git clone --no-hardlinks --quiet . "$WORK/current"
mkdir "$WORK/project"
cp -R examples/scientific-minimal/. "$WORK/project/"
printf 'project_name: Water budget\ntest_command: pytest\npreset: solo-greenfield\n' > "$WORK/profile.yml"
python "$WORK/old/bootstrap/scaffold.py" --config "$WORK/profile.yml" --target "$WORK/project" --cairn-root "$WORK/old" --allow-dev --non-interactive
```

The old checkout must retain its Git history: a plain exported archive gives an
unknown ancestor and cannot prove the layout migration. The scaffold generates
managed tools and a lockfile; the sample's code, data and illustrative records
are project-owned. `AGENTS.md` is managed: its `dst` record in
`dev/.cairn/cairn-lock.yml` names its cached base and installed hash. Fill its
`project-conventions` slot with a project-owned instruction:

```bash
python - "$WORK/project/AGENTS.md" <<'PY'
from pathlib import Path
import sys
path = Path(sys.argv[1])
text = path.read_text()
start = text.index('<!-- cairn:slot project-conventions -->')
end = text.index('<!-- cairn:end project-conventions -->', start)
path.write_text(text[:start] + '<!-- cairn:slot project-conventions -->\nUse millimetres per month for water-budget inputs.\n' + text[end:])
PY
```

The layout migration comes first. Read the proposed moves and stage output;
copy the printed receipt into the apply command (the receipt is specific to
this project). Review the staged layout receipt before applying it.

```bash
python "$WORK/current/install/scaffold.py" upgrade --target "$WORK/project" --plan
python "$WORK/current/install/scaffold.py" upgrade --target "$WORK/project" --stage
# Replace RECEIPT with the digest printed by the preceding command.
python "$WORK/current/install/scaffold.py" upgrade --target "$WORK/project" --apply --migration-receipt RECEIPT
```

Now stage the ordinary upgrade and review the actual managed file before
applying it. The `diff` may exit 1 because the file changed; inspect it. The
custom sentence must be present in the staged file and again after apply.

```bash
python "$WORK/current/install/scaffold.py" upgrade --target "$WORK/project" --stage
diff -u "$WORK/project/AGENTS.md" "$WORK/project/dev/.cairn-upgrade/files/AGENTS.md" || true
grep -n 'Use millimetres per month' "$WORK/project/dev/.cairn-upgrade/files/AGENTS.md"
python "$WORK/current/install/scaffold.py" upgrade --target "$WORK/project" --apply
grep -n 'Use millimetres per month' "$WORK/project/AGENTS.md"
```

The stage reports `AGENTS.md` as locally modified and merged cleanly. If it
reports a conflict, stop and resolve it before apply using the upgrade guide.
This exercise does not claim a release trust check or back up a real project.
