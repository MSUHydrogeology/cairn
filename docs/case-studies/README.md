# Case studies

Two research-software projects that use Cairn day to day, told from their own
decision records: what the projects are, how Cairn is set up in each, moments
where the method caught a scientific mistake or recorded a domain decision,
and what it cost.

| Case study | The project | Why it is a useful example |
| --- | --- | --- |
| [LHM](lhm.md) | An 18-year-old surface-water and groundwater model: a MATLAB core with few tests, a Python frontend, and a partial port between them | The heaviest setup: old code, two languages, several agents |
| [modflow_tools](modflow_tools.md) | A Python toolkit for building, reviewing and calibrating MODFLOW groundwater models | Built with AI agents from the start; where Cairn was first worked out |

**Read them as accounts of use, not as proof.** Both projects have the same
maintainer as Cairn, so neither is an independent adoption, and no controlled
comparison exists. What they show is the kind of mistake the method catches,
the kind of decision it records, and where its overhead shows.

## Rules for this folder

* **The project's maintainer approves the content** before a case study is
  added or changed here, and the approval is recorded in a commit
  (`bootstrap/SAFETY.md`, Rule 3). Both of these were approved by Anthony
  Kendall, who maintains both projects.
* **Methodology only.** No scientific results, calibration data, source code
  or embargoed material. The projects' own repositories hold their working
  detail.
* **Tool names are allowed here.** A case study may name the AI tools a
  project really used, because it reports what happened. Everywhere else,
  Cairn's guidance names no vendor.

## A historical file

[`modflow_tools-fidelity-manifest.yml`](modflow_tools-fidelity-manifest.yml)
is a machine-readable snapshot of modflow_tools' setup in May 2026, kept as a
worked example of the format described in
[`../bootstrap/fidelity-check.md`](../bootstrap/fidelity-check.md). It lists
modules and files that have since been removed, and does not describe the
project today.

## Adding a case study

A third case study is most useful if it sits somewhere these two do not: a
small new project, a team of several people, or a single agent. To propose
one, open an issue on Cairn's tracker describing the project, how Cairn is
set up there, and two or three moments from its record. The project's
maintainer must approve the text before it is added. A contributed case
study is licensed like the rest of Cairn's prose, under CC BY 4.0
([`../LICENSE-CC-BY.md`](../LICENSE-CC-BY.md)).
