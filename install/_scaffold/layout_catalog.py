"""Reviewed installer ownership across the repository-layout transition.

Rows are (owner, old source, old destination, verbatim, new source, new
destination), with sources relative to the Cairn repository root. A row is
an allowlist, not proof that it existed at a particular revision. Historical
membership and regular-blob evidence must be established separately from the
exact trusted revision. Project lock and profile data cannot add rows.
"""

LAYOUT_INSTALLS = (
    ('skills', 'templates/skills/_data/vendor_targets.yml', '.agents/skills/_data/vendor_targets.yml', True, 'templates/skills/_data/vendor_targets.yml', '.agents/skills/_data/vendor_targets.yml'),
    ('skills', 'templates/skills/session-end/SKILL.md', '.agents/skills/session-end/SKILL.md', False, 'templates/skills/session-end/SKILL.md', '.agents/skills/session-end/SKILL.md'),
    ('skills', 'templates/skills/session-start/SKILL.md', '.agents/skills/session-start/SKILL.md', False, 'templates/skills/session-start/SKILL.md', '.agents/skills/session-start/SKILL.md'),
    ('skills', 'templates/core/gitattributes.txt', '.gitattributes', True, 'templates/core/gitattributes.txt', '.gitattributes'),
    ('core', 'templates/core/AGENTS.md', 'AGENTS.md', False, 'templates/core/AGENTS.md', 'AGENTS.md'),
    ('core', 'templates/core/CHANGELOG.md', 'CHANGELOG.md', False, 'templates/core/CHANGELOG.md', 'CHANGELOG.md'),
    ('optional:human_team', 'templates/optional/CONTRIBUTING.md', 'CONTRIBUTING.md', False, 'templates/optional/CONTRIBUTING.md', 'CONTRIBUTING.md'),
    ('core', 'templates/core/NOTICE.md', 'NOTICE.md', False, 'templates/core/NOTICE.md', 'NOTICE.md'),
    ('core', 'templates/core/RULES.md', 'RULES.md', False, 'templates/core/RULES.md', 'RULES.md'),
    ('core', 'templates/core/VENDOR.md', 'VENDOR.md', False, 'templates/core/VENDOR.md', 'VENDOR.md'),
    ('module:api-access-security', 'templates/modules/team-gated/api_access_policy_stub.json', 'dev/.cairn/api-access-policy.json', False, 'templates/modules/team-gated/api_access_policy_stub.json', 'dev/.cairn/api-access-policy.json'),
    ('module:model-selection', 'templates/modules/team-gated/model_selection_mapping_stub.yml', 'dev/.cairn/model-selection-mapping.yml', False, 'templates/modules/team-gated/model_selection_mapping_stub.yml', 'dev/.cairn/model-selection-mapping.yml'),
    ('module:documentation-plan', 'templates/modules/default-on/scanner-check-allow.json', 'dev/.cairn/scanner-check-allow.json', False, 'templates/modules/default-on/scanner-check-allow.json', 'dev/.cairn/scanner-check-allow.json'),
    ('module:web-hosting-security', 'templates/modules/team-gated/web_hosting_policy_stub.json', 'dev/.cairn/web-hosting-policy.json', False, 'templates/modules/team-gated/web_hosting_policy_stub.json', 'dev/.cairn/web-hosting-policy.json'),
    ('core', 'templates/core/dev/PLANNING.md', 'dev/PLANNING.md', False, 'templates/core/dev/PLANNING.md', 'dev/PLANNING.md'),
    ('core', 'templates/core/dev/README.md', 'dev/README.md', False, 'templates/core/dev/README.md', 'dev/README.md'),
    ('core', 'templates/core/dev/agent_collaboration.md', 'dev/agent_collaboration.md', False, 'templates/core/dev/agent_collaboration.md', 'dev/agent_collaboration.md'),
    ('module:architecture-review', 'templates/modules/team-gated/architecture_review_template.md', 'dev/architecture_review.md', False, 'templates/modules/team-gated/architecture_review_template.md', 'dev/architecture_review.md'),
    ('core', 'templates/core/dev/measurement/README.md', 'dev/measurement/README.md', False, 'templates/core/dev/measurement/README.md', 'dev/measurement/README.md'),
    ('module:incident-trackers', 'templates/modules/default-on/measurement-archive/.gitkeep', 'dev/measurement/archive/.gitkeep', True, 'templates/modules/default-on/measurement-archive/.gitkeep', 'dev/measurement/archive/.gitkeep'),
    ('core', 'templates/core/dev/method-background.md', 'dev/method-background.md', False, 'templates/core/dev/method-background.md', 'dev/method-background.md'),
    ('core', 'templates/core/dev/modules/README.md', 'dev/modules/README.md', False, 'templates/core/dev/modules/README.md', 'dev/modules/README.md'),
    ('module:api-access-security', 'templates/modules/team-gated/api-access-security.md', 'dev/modules/api-access-security.md', False, 'templates/modules/team-gated/api-access-security.md', 'dev/modules/api-access-security.md'),
    ('module:architecture-review', 'templates/modules/team-gated/architecture-review.md', 'dev/modules/architecture-review.md', False, 'templates/modules/team-gated/architecture-review.md', 'dev/modules/architecture-review.md'),
    ('module:claim-check', 'templates/modules/default-on/claim-check.md', 'dev/modules/claim-check.md', False, 'templates/modules/default-on/claim-check.md', 'dev/modules/claim-check.md'),
    ('module:content-security', 'templates/modules/team-gated/content-security.md', 'dev/modules/content-security.md', False, 'templates/modules/team-gated/content-security.md', 'dev/modules/content-security.md'),
    ('module:coordination-tiers', 'templates/modules/team-gated/coordination-tiers.md', 'dev/modules/coordination-tiers.md', False, 'templates/modules/team-gated/coordination-tiers.md', 'dev/modules/coordination-tiers.md'),
    ('module:doc-drift-prevention', 'templates/modules/team-gated/doc-drift-prevention.md', 'dev/modules/doc-drift-prevention.md', False, 'templates/modules/team-gated/doc-drift-prevention.md', 'dev/modules/doc-drift-prevention.md'),
    ('module:documentation-plan', 'templates/modules/default-on/documentation-plan.md', 'dev/modules/documentation-plan.md', False, 'templates/modules/default-on/documentation-plan.md', 'dev/modules/documentation-plan.md'),
    ('module:domain-agents', 'templates/modules/team-gated/domain-agents.md', 'dev/modules/domain-agents.md', False, 'templates/modules/team-gated/domain-agents.md', 'dev/modules/domain-agents.md'),
    ('module:dual-language-tests', 'templates/modules/team-gated/dual-language-tests.md', 'dev/modules/dual-language-tests.md', False, 'templates/modules/team-gated/dual-language-tests.md', 'dev/modules/dual-language-tests.md'),
    ('module:dual-review', 'templates/modules/team-gated/dual-review.md', 'dev/modules/dual-review.md', False, 'templates/modules/team-gated/dual-review.md', 'dev/modules/dual-review.md'),
    ('module:examples-gallery', 'templates/modules/team-gated/examples-gallery.md', 'dev/modules/examples-gallery.md', False, 'templates/modules/team-gated/examples-gallery.md', 'dev/modules/examples-gallery.md'),
    ('module:incident-trackers', 'templates/modules/default-on/incident-trackers.md', 'dev/modules/incident-trackers.md', False, 'templates/modules/default-on/incident-trackers.md', 'dev/modules/incident-trackers.md'),
    ('module:incident-trackers', 'templates/modules/default-on/incident_log_template.md', 'dev/modules/incident_log_template.md', False, 'templates/modules/default-on/incident_log_template.md', 'dev/modules/incident_log_template.md'),
    ('module:issue-capture', 'templates/modules/team-gated/issue-capture.md', 'dev/modules/issue-capture.md', False, 'templates/modules/team-gated/issue-capture.md', 'dev/modules/issue-capture.md'),
    ('module:legacy-agent', 'templates/modules/team-gated/legacy-agent.md', 'dev/modules/legacy-agent.md', False, 'templates/modules/team-gated/legacy-agent.md', 'dev/modules/legacy-agent.md'),
    ('module:model-selection', 'templates/modules/team-gated/model-selection.md', 'dev/modules/model-selection.md', False, 'templates/modules/team-gated/model-selection.md', 'dev/modules/model-selection.md'),
    ('module:portable-security-sweeps', 'templates/modules/team-gated/portable-security-sweeps.md', 'dev/modules/portable-security-sweeps.md', False, 'templates/modules/team-gated/portable-security-sweeps.md', 'dev/modules/portable-security-sweeps.md'),
    ('module:python-security', 'templates/modules/team-gated/python-security.md', 'dev/modules/python-security.md', False, 'templates/modules/team-gated/python-security.md', 'dev/modules/python-security.md'),
    ('module:reflections', 'templates/modules/default-on/reflections.md', 'dev/modules/reflections.md', False, 'templates/modules/default-on/reflections.md', 'dev/modules/reflections.md'),
    ('module:security-review', 'templates/modules/team-gated/security-review.md', 'dev/modules/security-review.md', False, 'templates/modules/team-gated/security-review.md', 'dev/modules/security-review.md'),
    ('module:security-verification', 'templates/modules/default-on/security-verification.md', 'dev/modules/security-verification.md', False, 'templates/modules/default-on/security-verification.md', 'dev/modules/security-verification.md'),
    ('module:testing-discipline', 'templates/modules/team-gated/testing-discipline.md', 'dev/modules/testing-discipline.md', False, 'templates/modules/team-gated/testing-discipline.md', 'dev/modules/testing-discipline.md'),
    ('module:web-hosting-security', 'templates/modules/team-gated/web-hosting-security.md', 'dev/modules/web-hosting-security.md', False, 'templates/modules/team-gated/web-hosting-security.md', 'dev/modules/web-hosting-security.md'),
    ('core', 'templates/core/dev/plans/_template.md', 'dev/plans/_template.md', False, 'templates/core/dev/plans/_template.md', 'dev/plans/_template.md'),
    ('core', 'templates/core/dev/proposals/_template.md', 'dev/proposals/_template.md', False, 'templates/core/dev/proposals/_template.md', 'dev/proposals/_template.md'),
    ('module:reflections', 'templates/modules/default-on/reflections-README.md', 'dev/reflections/README.md', True, 'templates/modules/default-on/reflections-README.md', 'dev/reflections/README.md'),
    ('core', 'templates/core/dev/rules/README.md', 'dev/rules/README.md', False, 'templates/core/dev/rules/README.md', 'dev/rules/README.md'),
    ('core', 'templates/core/dev/strategy/README.md', 'dev/strategy/README.md', False, 'templates/core/dev/strategy/README.md', 'dev/strategy/README.md'),
    ('core', 'templates/core/dev/strategy/_template.md', 'dev/strategy/_template.md', False, 'templates/core/dev/strategy/_template.md', 'dev/strategy/_template.md'),
    ('core', 'templates/core/dev/upstream/README.md', 'dev/upstream/README.md', False, 'templates/core/dev/upstream/README.md', 'dev/upstream/README.md'),
    ('core', 'templates/core/dev/upstream/_template.md', 'dev/upstream/_template.md', False, 'templates/core/dev/upstream/_template.md', 'dev/upstream/_template.md'),
    ('core', 'templates/core/dev/upstream/archive/.gitkeep', 'dev/upstream/archive/.gitkeep', False, 'templates/core/dev/upstream/archive/.gitkeep', 'dev/upstream/archive/.gitkeep'),
    ('module:documentation-plan', 'templates/modules/default-on/documentation_plan_template.md', 'docs/DOCUMENTATION_PLAN.md', False, 'templates/modules/default-on/documentation_plan_template.md', 'docs/DOCUMENTATION_PLAN.md'),
    ('module:api-access-security', 'templates/modules/team-gated/_security_net/__init__.py', 'scripts/_api_access_security/__init__.py', True, 'templates/modules/team-gated/_security_net/__init__.py', 'dev/tools/_api_access_security/__init__.py'),
    ('module:api-access-security', 'templates/modules/team-gated/_security_net/net.py', 'scripts/_api_access_security/net.py', True, 'templates/modules/team-gated/_security_net/net.py', 'dev/tools/_api_access_security/net.py'),
    ('module:api-access-security', 'templates/modules/team-gated/_security_net/policy.py', 'scripts/_api_access_security/policy.py', True, 'templates/modules/team-gated/_security_net/policy.py', 'dev/tools/_api_access_security/policy.py'),
    ('module:api-access-security', 'templates/modules/team-gated/_security_net/report.py', 'scripts/_api_access_security/report.py', True, 'templates/modules/team-gated/_security_net/report.py', 'dev/tools/_api_access_security/report.py'),
    ('module:web-hosting-security', 'templates/modules/team-gated/_security_net/__init__.py', 'scripts/_web_hosting_security/__init__.py', True, 'templates/modules/team-gated/_security_net/__init__.py', 'dev/tools/_web_hosting_security/__init__.py'),
    ('module:web-hosting-security', 'templates/modules/team-gated/_security_net/net.py', 'scripts/_web_hosting_security/net.py', True, 'templates/modules/team-gated/_security_net/net.py', 'dev/tools/_web_hosting_security/net.py'),
    ('module:web-hosting-security', 'templates/modules/team-gated/_security_net/policy.py', 'scripts/_web_hosting_security/policy.py', True, 'templates/modules/team-gated/_security_net/policy.py', 'dev/tools/_web_hosting_security/policy.py'),
    ('module:web-hosting-security', 'templates/modules/team-gated/_security_net/report.py', 'scripts/_web_hosting_security/report.py', True, 'templates/modules/team-gated/_security_net/report.py', 'dev/tools/_web_hosting_security/report.py'),
    ('module:api-access-security', 'templates/modules/team-gated/api_access_security.py', 'scripts/api_access_security.py', True, 'templates/modules/team-gated/api_access_security.py', 'dev/tools/api_access_security.py'),
    ('module:issue-capture', 'templates/modules/team-gated/issue-capture/bootstrap_github_labels.py', 'scripts/bootstrap_github_labels.py', True, 'templates/modules/team-gated/issue-capture/bootstrap_github_labels.py', 'dev/tools/bootstrap_github_labels.py'),
    ('module:issue-capture', 'templates/modules/team-gated/issue-capture/bootstrap_gitlab_labels.py', 'scripts/bootstrap_gitlab_labels.py', True, 'templates/modules/team-gated/issue-capture/bootstrap_gitlab_labels.py', 'dev/tools/bootstrap_gitlab_labels.py'),
    ('module:model-selection', 'templates/modules/team-gated/check_model_selection.py', 'scripts/check_model_selection.py', True, 'templates/modules/team-gated/check_model_selection.py', 'dev/tools/check_model_selection.py'),
    ('module:claim-check', 'templates/modules/default-on/claim_check.py', 'scripts/claim_check.py', True, 'templates/modules/default-on/claim_check.py', 'dev/tools/claim_check.py'),
    ('module:content-security', 'templates/modules/team-gated/content_scan.py', 'scripts/content_scan.py', True, 'templates/modules/team-gated/content_scan.py', 'dev/tools/content_scan.py'),
    ('module:content-security', 'templates/modules/team-gated/content_scan_allowlist.txt', 'scripts/content_scan_allowlist.txt', True, 'templates/modules/team-gated/content_scan_allowlist.txt', 'dev/tools/content_scan_allowlist.txt'),
    ('module:content-security', 'templates/modules/team-gated/content_scan_residuals.txt', 'scripts/content_scan_residuals.txt', True, 'templates/modules/team-gated/content_scan_residuals.txt', 'dev/tools/content_scan_residuals.txt'),
    ('module:content-security', 'templates/modules/team-gated/content_scan_roots.txt', 'scripts/content_scan_roots.txt', True, 'templates/modules/team-gated/content_scan_roots.txt', 'dev/tools/content_scan_roots.txt'),
    ('module:content-security', 'templates/modules/team-gated/content_scan_runner.py', 'scripts/content_scan_runner.py', True, 'templates/modules/team-gated/content_scan_runner.py', 'dev/tools/content_scan_runner.py'),
    ('module:content-security', 'templates/modules/team-gated/exact_replace.py', 'scripts/exact_replace.py', True, 'templates/modules/team-gated/exact_replace.py', 'dev/tools/exact_replace.py'),
    ('module:doc-drift-prevention', 'templates/modules/team-gated/link_check.py', 'scripts/link_check.py', True, 'templates/modules/team-gated/link_check.py', 'dev/tools/link_check.py'),
    ('module:portable-security-sweeps', 'templates/modules/team-gated/portable_security_policy.json', 'scripts/portable_security_policy.json', True, 'templates/modules/team-gated/portable_security_policy.json', 'dev/tools/portable_security_policy.json'),
    ('module:content-security', 'templates/modules/team-gated/prose_diff.py', 'scripts/prose_diff.py', True, 'templates/modules/team-gated/prose_diff.py', 'dev/tools/prose_diff.py'),
    ('module:content-security', 'templates/modules/team-gated/prose_roots.txt', 'scripts/prose_roots.txt', True, 'templates/modules/team-gated/prose_roots.txt', 'dev/tools/prose_roots.txt'),
    ('module:portable-security-sweeps', 'templates/modules/team-gated/run_portable_security_sweeps.py', 'scripts/run_portable_security_sweeps.py', True, 'templates/modules/team-gated/run_portable_security_sweeps.py', 'dev/tools/run_portable_security_sweeps.py'),
    ('module:python-security', 'templates/modules/team-gated/run_security_audit.py', 'scripts/run_security_audit.py', True, 'templates/modules/team-gated/run_security_audit.py', 'dev/tools/run_security_audit.py'),
    ('module:security-verification', 'templates/modules/default-on/run_security_verification.py', 'scripts/run_security_verification.py', True, 'templates/modules/default-on/run_security_verification.py', 'dev/tools/run_security_verification.py'),
    ('module:doc-drift-prevention', 'templates/modules/team-gated/sync_doc_snippets.py', 'scripts/sync_doc_snippets.py', True, 'templates/modules/team-gated/sync_doc_snippets.py', 'dev/tools/sync_doc_snippets.py'),
    ('module:testing-discipline', 'templates/modules/team-gated/test_coupling.py', 'scripts/test_coupling.py', True, 'templates/modules/team-gated/test_coupling.py', 'dev/tools/test_coupling.py'),
    ('module:claim-check', 'templates/modules/default-on/verify_stems.py', 'scripts/verify_stems.py', True, 'templates/modules/default-on/verify_stems.py', 'dev/tools/verify_stems.py'),
    ('module:web-hosting-security', 'templates/modules/team-gated/web_hosting_security.py', 'scripts/web_hosting_security.py', True, 'templates/modules/team-gated/web_hosting_security.py', 'dev/tools/web_hosting_security.py'),
    ('module:coordination-tiers', 'templates/modules/team-gated/_intent/__init__.py', 'tools/_intent/__init__.py', True, 'templates/modules/team-gated/_intent/__init__.py', 'dev/tools/_intent/__init__.py'),
    ('module:coordination-tiers', 'templates/modules/team-gated/_intent/cli.py', 'tools/_intent/cli.py', True, 'templates/modules/team-gated/_intent/cli.py', 'dev/tools/_intent/cli.py'),
    ('module:coordination-tiers', 'templates/modules/team-gated/_intent/conflict.py', 'tools/_intent/conflict.py', True, 'templates/modules/team-gated/_intent/conflict.py', 'dev/tools/_intent/conflict.py'),
    ('module:coordination-tiers', 'templates/modules/team-gated/_intent/hooks.py', 'tools/_intent/hooks.py', True, 'templates/modules/team-gated/_intent/hooks.py', 'dev/tools/_intent/hooks.py'),
    ('module:coordination-tiers', 'templates/modules/team-gated/_intent/identity.py', 'tools/_intent/identity.py', True, 'templates/modules/team-gated/_intent/identity.py', 'dev/tools/_intent/identity.py'),
    ('module:coordination-tiers', 'templates/modules/team-gated/_intent/record_io.py', 'tools/_intent/record_io.py', True, 'templates/modules/team-gated/_intent/record_io.py', 'dev/tools/_intent/record_io.py'),
    ('module:coordination-tiers', 'templates/modules/team-gated/_intent/shared.py', 'tools/_intent/shared.py', True, 'templates/modules/team-gated/_intent/shared.py', 'dev/tools/_intent/shared.py'),
    ('skills', 'templates/skills/_lib/board.py', 'tools/board.py', True, 'templates/skills/_lib/board.py', 'dev/tools/board.py'),
    ('module:architecture-review', 'templates/modules/team-gated/code_map.py', 'tools/code_map.py', True, 'templates/modules/team-gated/code_map.py', 'dev/tools/code_map.py'),
    ('module:incident-trackers', 'templates/modules/default-on/evolution_infer.py', 'tools/evolution_infer.py', True, 'templates/modules/default-on/evolution_infer.py', 'dev/tools/evolution_infer.py'),
    ('skills', 'templates/skills/_lib/git_read.py', 'tools/git_read.py', True, 'templates/skills/_lib/git_read.py', 'dev/tools/git_read.py'),
    ('module:coordination-tiers', 'templates/modules/team-gated/intent.py', 'tools/intent.py', True, 'templates/modules/team-gated/intent.py', 'dev/tools/intent.py'),
    ('skills', 'templates/skills/_lib/meter.py', 'tools/meter.py', True, 'templates/skills/_lib/meter.py', 'dev/tools/meter.py'),
    ('module:coordination-tiers', 'templates/modules/team-gated/prune_intents.py', 'tools/prune_intents.py', True, 'templates/modules/team-gated/prune_intents.py', 'dev/tools/prune_intents.py'),
    ('module:reflections', 'templates/modules/default-on/prune_reflections.py', 'tools/prune_reflections.py', True, 'templates/modules/default-on/prune_reflections.py', 'dev/tools/prune_reflections.py'),
    ('skills', 'templates/skills/_lib/pulse.py', 'tools/pulse.py', True, 'templates/skills/_lib/pulse.py', 'dev/tools/pulse.py'),
    ('skills', 'templates/skills/_lib/session.py', 'tools/session.py', True, 'templates/skills/_lib/session.py', 'dev/tools/session.py'),
)

# Existing vendor wrapper aliases are keep-only, never additional move paths.
VENDOR_WRAPPER_ALIASES = ('CLAUDE.md', 'GEMINI.md', 'CODEX.md', 'CURSOR.md', 'COPILOT.md', 'QWEN.md')

# Recorded custom wrapper names are also keep-only; they cannot authorize a move.
RECORDED_WRAPPER_POLICY = "keep-only"
SKILL_FANOUT_ROOTS = (".agents/skills/", ".claude/skills/")

# Write E is outside the regular template lock inventory. Existing copies stay.
ONBOARDING_GUIDES = (
    ('docs/agent-team-onboarding.md', 'templates/onboarding/agent-team-onboarding.md', 'dev/modules/onboarding/agent-team-onboarding.md'),
    ('docs/dev-tour.md', 'templates/onboarding/dev-tour.md', 'dev/modules/onboarding/dev-tour.md'),
)

# Comparison evidence for the unlisted self-hosted code-map copy.
CODE_MAP_V070_COMMIT = "2f9fda2ba410077e2523547b8ef3c055257ea61d"
CODE_MAP_V070_BLOB = "a6c597921b0ec19884201ca15706b30f1784361d"
SELF_HOST_UNLISTED = (("module:architecture-review", "tools/code_map.py"),)

# Cairn source motion, distinct from adopter migration authority. Resolve the
# named overrides and installed destinations first, then ordered prefixes;
# expand against a trusted
# revision's tracked paths, not an adopter's lock or filesystem.
SOURCE_FILE_MOVES = (
    ('bootstrap/security_check.py', 'release/security_check.py'),
    ('bootstrap/requirements-dev.txt', 'tests/requirements-dev.txt'),
    ('bootstrap/AST_BASELINE_RUNBOOK.md', 'release/AST_BASELINE_RUNBOOK.md'),
    ('bootstrap/REANCHOR_RUNBOOK.md', 'release/REANCHOR_RUNBOOK.md'),
    ('bootstrap/reanchor.sh', 'release/reanchor.sh'),
    ('bootstrap/reanchor-launcher.template.sh', 'release/reanchor-launcher.template.sh'),
    ('bootstrap/reanchor-values.example', 'release/reanchor-values.example'),
    ('scripts/repin.py', 'release/repin.py'),
    ('scripts/reanchor_ceremony.py', 'release/reanchor_ceremony.py'),
    ('scripts/check_release_publication.py', 'release/check_release_publication.py'),
    ('scripts/check_release_test_members.py', 'release/check_release_test_members.py'),
    ('templates/codebase-readiness-report.md', 'install/codebase-readiness-report.md'),
    ('docs/agent-team-onboarding.md', 'templates/onboarding/agent-team-onboarding.md'),
    ('docs/dev-tour.md', 'templates/onboarding/dev-tour.md'),
)
SOURCE_PREFIX_MOVES = (
    ('bootstrap/tests/', 'tests/'),
    ('bootstrap/', 'install/'),
    ('templates/phase-0/', 'install/phase-0/'),
    ('dimensions/', 'install/dimensions/'),
    ('on-ramp/', 'install/on-ramp/'),
    ('case-studies/', 'docs/case-studies/'),
    ('scripts/', 'tests/'),
    ('tools/', 'tests/'),
)
