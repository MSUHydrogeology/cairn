# Human team — solo ↔ multi-human

The **human team** axis is how many people are on the project, and
in what roles. It drives how Decision authority is handled and what
human-review patterns apply. It is independent of every codebase
axis and of the agent-team axis: a solo human may run several
agents; a multi-human team may run one.

## Scoring rubric

* **Contributor count.** How many humans make changes — one, a
  handful, many?
* **Roles.** Is there a PI, are there students, are there outside
  contributors — and who, today, is accountable for the project's
  scientific direction?
* **Current review practice.** Does the team already do human code
  review, or has review been informal?

## Positions

### Solo

One human, who is by definition the Maintainer. Decision authority
is unambiguous. There is no human-to-human review; the review
tiers are filled by the agent team and the Maintainer
(`../doctrine/dual-review.md`).

### Multi-human

* **One designated Maintainer.** Even with several humans, exactly
  one holds final Decision authority (`../doctrine/roles.md`).
  Cairn's v1 does not split Decision rights — a multi-human team
  *elects* its Maintainer rather than deciding by committee.
* **Human review patterns.** Other humans — a PI, senior
  contributors — can fill the External-review tier, and human
  review of agent-authored work is available where the team wants
  it.
* **Optional `CONTRIBUTING.md`.** A multi-human team (the
  `small-multi` / `large-multi` axis values) gets the optional
  human-facing `CONTRIBUTING.md` — the GitLab/GitHub-surfaced
  contributor entry that points back to `AGENTS.md` for the shared
  rules (it does not duplicate them). The scaffold installs it for
  these positions and records it under `optional_templates:` in the
  fidelity manifest so the gate is auditable
  (`../bootstrap/fidelity-check.md`). A solo project ships no
  `CONTRIBUTING.md`.
* A multi-human-team review module — shared decision rights, a
  formal human-review rotation — is a **named follow-up**, picked
  up only if multi-human adoption shows demand beyond the "elect
  one Maintainer" guidance.
