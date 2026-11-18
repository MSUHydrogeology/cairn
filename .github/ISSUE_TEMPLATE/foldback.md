---
name: Fold-back from a deployment
about: A Cairn-portable improvement surfaced from a deployment
title: '[Fold-back from <deployment>] <short description>'
labels: ['foldback']
assignees: []
---

<!-- Follow the shared protocol in dev/upstream/foldback.md. An agent may
     file this issue only after the Human Maintainer approves this actual issue
     and its destination. -->

## Source deployment

<!-- The deployment repository this fold-back originated from.
     Include enough context that a Cairn maintainer can locate the
     proving artifacts: repo name, the relevant proposal/plan stem(s),
     and the commit range that demonstrates the candidate. -->

## Candidate description

<!-- One paragraph: what is the generalizable improvement?  Frame it
     in vendor-neutral, deployment-shape-neutral terms (Cairn's R-G
     vendor-neutrality discipline applies).  Avoid project-specific
     terminology unless explicitly cross-referenced under the
     export-safety affirmation below. -->

## Generalizability test

<!-- The harvest-doctrine question: would a differently-shaped team
     hit the same need?  One paragraph of evidence.  Deployment-local
     quirks (the deployment's own tools, naming, science) do NOT fold
     back -- only what crosses the generalizability bar belongs here. -->

## Proven by

<!-- Cite the deployment commits / archived proposal / archived plan
     that demonstrate the candidate works in practice.  This is the
     evidence the foldback rides on. -->

* Commit(s):
* Archived proposal:
* Archived plan:

## Suggested disposition

<!-- Where this candidate should land in Cairn.  Check one: -->

- [ ] **Cairn proposal** -- this candidate warrants a full Cairn proposal-lifecycle pass
- [ ] **Cairn methodology sharpening** -- a `cairn/docs/methodology/` edit captures it
- [ ] **Cairn templates / module update** -- a `cairn/templates/modules/` change carries it
- [ ] **Other (described below)**

## Export-safety affirmation

Follow the shared protocol in `dev/upstream/foldback.md` before filing.

- [ ] I checked the complete body and attachments for unpublished data or hints,
  proprietary project or customer detail, and credentials, and reread them
  after writing.
- [ ] The Human Maintainer approved this actual issue and its destination.
