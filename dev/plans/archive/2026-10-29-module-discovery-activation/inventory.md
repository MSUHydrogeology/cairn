# Module first-use inventory

This is the implementation design inventory. Every entry point is an installed
`dev/modules/<module>.md` unless another path is named. The implementation
must check the shipped text and actual installed paths before using these tasks;
a missing or inapplicable instruction is a failed criterion, not permission to
invent a command. Each row's output is the expected first-use result.

| Module | First action and expected result |
|---|---|
| reflections | Read the module and `dev/reflections/README.md`; record one session reflection using its guidance. Result: a local reflection. |
| claim-check | Use the module's installed claim checker on an existing document. Result: its path and line claims checked. |
| incident-trackers | Use `dev/modules/incident_log_template.md` to create a tracker for a relevant incident class. Result: a project tracker. |
| documentation-plan | Tailor `docs/DOCUMENTATION_PLAN.md` to project documentation. Result: a project-specific placement map. |
| dual-review | Read the module and choose a staffing approach for a Maintainer-called read if one occurs. Result: a documented staffing choice, without requiring a new read. |
| domain-agents | Read the module and identify one domain and its proposed agent boundary. Result: a candidate role boundary. |
| legacy-agent | Read the module and identify an inherited-system area where its guidance applies. Result: a candidate legacy-agent focus. |
| dual-language-tests | Read the module and identify one behavior requiring cross-language coverage. Result: a candidate test mapping. |
| coordination-tiers | Read the module and use `tools/intent.py --help` to identify the claim workflow. Result: the team's first coordination procedure. |
| security-review | Read the module and identify a project trust boundary and a candidate review trigger. Result: a boundary and trigger for Maintainer consideration. |
| issue-capture | Read the module and choose how to record one friction or gap. Result: a capture route; do not create an external issue without authorization. |
| model-selection | Fill `dev/.cairn/model-selection-mapping.yml` with the team's actual model assignments and run `python scripts/check_model_selection.py`. Result: a checked mapping. |
| testing-discipline | Read the module and map one changed behavior to a test. Result: a test ownership example. |
| doc-drift-prevention | Read the module and run `python scripts/link_check.py` on the installed documentation according to its usage. Result: a link report. |
| examples-gallery | Read the module and identify one example and its owning source. Result: a candidate gallery entry. |
| content-security | Read the module and its scanner usage before scanning a chosen local input. Result: a content-scan report; findings need human judgment. |
| python-security | Read the module and configure the required Python package before using its audit. Result: a configured audit input; network access remains opt-in. |
| portable-security-sweeps | Read the module and configure the policy and required local adapter before running a sweep. Result: a configured offline sweep. |
| api-access-security | Read the module and fill dev/.cairn/api-access-policy.json for an authorized target before running its check. Result: an authorized policy, without automatic network access. |
| web-hosting-security | Read the module and fill dev/.cairn/web-hosting-policy.json for an authorized target before running its check. Result: an authorized policy, without automatic network access. |
| architecture-review | Read the module and use dev/architecture_review.md to choose a legacy, new or mixed-system review approach. Result: an adapted rubric; expansion of the rubric remains outside this plan. |
| security-verification | Read the module and inspect the installed dispatcher and its initially empty capability registry. Result: understand which, if any, checks are admitted; no check is assumed. |
