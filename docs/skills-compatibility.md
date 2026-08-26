# Skills compatibility matrix

<!-- GENERATED from templates/skills/_data/vendor_targets.yml by
     bootstrap.scaffold.render_compatibility_matrix; hand edits are
     replaced on the next render.  Levels are CLAIMED-pending-fixture
     (II3): a target is `native-tested` only once a fixture proves
     install + invoke on it. -->

| Target | Tier | Format | Install/invoke level | Auto-suppress |
|--------|------|--------|----------------------|---------------|
| agents-native | alias | skill-md | native-claimed-unverified | declared-flag |
| antigravity | alias | skill-md | native-claimed-unverified | cli-backstop-only |
| claude-code | symlink | skill-md | native-claimed-unverified | declared-flag |
| codex | alias | skill-md | native-claimed-unverified | cli-backstop-only |
| cursor | alias | skill-md | native-claimed-unverified | cli-backstop-only |
| github-copilot | alias | skill-md | native-claimed-unverified | cli-backstop-only |
| windsurf | alias | skill-md | native-claimed-unverified | cli-backstop-only |

## Runtime self-heal

A **symlink**-tier target's read-path is fanned out from the canonical
`.agents/skills/` source at install time. It is *also* re-ensured at
**session-start** by the session kernel (`tools/session.py
session-start`), so an adopter established by lockfile-copy -- or whose
symlink-tier harness was not present at install -- self-heals on first
run instead of silently having no skills in that harness. The self-heal
is idempotent and carries the installer's writer-safety contract:
path-containment, a copy fallback where symlinks are unavailable (with a
`.gitignore` seed), and a refuse-or-quarantine guard that never clobbers
a divergent existing target. **alias**-tier targets read `.agents/skills/`
directly and need no fan-out (nothing is emitted for them).
