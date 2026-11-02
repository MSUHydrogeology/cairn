# issue-capture — forge-specific reference starters

The `issue-capture` module works with any issue tracker. It defines four
types of reports — Bug, Gap, Friction, and Wish — and when to review them,
without requiring a particular hosting service. This directory provides
starter files for GitLab and GitHub so adopters can use the guidance without
building forms from the field lists.

* `.gitlab/` — issue templates (GitLab's web UI auto-discovers
  `issue_templates/`) + a `labels.yml` manifest applied by a bootstrap
  script.
* `.github/` — `ISSUE_TEMPLATE/` markdown forms (YAML frontmatter
  carries the labels) + a `labels.yml` for `gh label` / a label-sync
  action.

**These are starters, not rules.** Copy the directory for your hosting
service into your repository root. Then add any project-specific routing
labels to `labels.yml` (for example, `domain::<area>` or `legacy`). The
starter labels are the minimum assumed by the triage guidance.
