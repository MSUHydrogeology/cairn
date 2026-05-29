# issue-capture — forge-specific reference starters

The `issue-capture` module's doctrine is **tracker-agnostic** (it
names the friction taxonomy — Bug / Gap / Friction / Wish — and the
triage cadence, not a forge). This directory ships **concrete
starters** for the two common forges so an adopter doesn't have to
invent the shape from the field lists.

* `.gitlab/` — issue templates (GitLab's web UI auto-discovers
  `issue_templates/`) + a `labels.yml` manifest applied by a bootstrap
  script.
* `.github/` — `ISSUE_TEMPLATE/` markdown forms (YAML frontmatter
  carries the labels) + a `labels.yml` for `gh label` / a label-sync
  action.

**These are starters, not doctrine.** Copy the tree for your forge into
your repo root, then extend `labels.yml` with project-specific routing
labels (e.g. a `domain::<area>` set to route to your domain agents, or
a `legacy` marker). The standing set here is the minimum the triage
doctrine assumes.
