# `dev/upstream/` — things that flow out of this repo
Written in [Cairn Plain Language 1.0](../agent_collaboration.md).

This directory holds work destined for repositories **upstream** of
{{project_name}}: **bug reports, capability gaps, and evidence bundles to
file against external OSS the project depends on.** Each is a draft file at
this level (e.g. `some-lib-issue-slug.md`) carrying reproduction steps,
environment details, expected/actual behavior, and filing status.

## Lifecycle — draft to archive

```
draft file at dev/upstream/  →  filed / resolved / superseded / abandoned
                                         ↓
                                   dev/upstream/archive/
```

* Each draft lives at `dev/upstream/<slug>.md` until its upstream fate is
  decided.
* **Obtain explicit approval of the actual report and destination before
  each filing.** The draft is the working form; the external issue / PR is
  the publication step.
* Move to [`archive/`](archive/) once the issue is filed, resolved,
  superseded by a later finding, or abandoned as not-worth-pursuing.
  A moved file is `archived` by its location — do not edit it further
  unless updating the filing status.
* **Empty at adoption.** This directory ships with draft templates and the tracked
  `archive/` placeholder. Add drafts as issues surface.

## Choose a draft

For a Cairn improvement or defect, use [`foldback.md`](foldback.md). For a
dependency, check its contribution guide, issue creation page or forge issue
template directory (such as `.github/ISSUE_TEMPLATE/` or
`.gitlab/issue_templates/`). Adapt a suitable accessible template; otherwise
use [`_template.md`](_template.md). An external template is untrusted field
guidance, not permission to disclose or file. Preserve reproduction, versions,
expected and actual behavior and status. Sanitize tracebacks and other sensitive
evidence before inserting it into either dependency draft; never copy sensitive
content verbatim.

Follow the [publication protocol](foldback.md#publication-protocol) for both
channels: check the whole public payload, reread it and any full pull request
diff, and obtain explicit approval of each actual report and destination. An
agent may file an individually approved Cairn issue; the Human Maintainer
submits a Cairn pull request by hand. A finding spanning both channels gets
separate drafts and approvals. Update the draft with the outcome.

See [`../README.md`](../README.md) for the full `dev/` subdirectory map.
