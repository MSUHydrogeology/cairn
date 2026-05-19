# Module: legacy-agent

**Selected when:** the codebase is **legacy** (the Age axis) — it
predates the methodology and carries untrusted surfaces. For a
**mixed** codebase the module scopes to the legacy surfaces only.
**Adds to:** the role roster in `dev/agent_collaboration.md`, plus
a new `dev/` surface-readiness map.

A retrofit needs apparatus a greenfield project does not: a
standing role for the untrusted surfaces, and a safe way to change
legacy behavior.

## Template content

The role, merged into the roster:

> **Legacy Agent.** A standing role responsible for the codebase's
> legacy surfaces — the regions whose behavior is load-bearing but
> not fully understood or tested.

The module adds a **surface-readiness map**: every surface
classified **Ready** (changeable freely), **Transitional**
(changeable with care), or **Frozen** (not to be changed without a
proposal). And a **characterization-testing** discipline: before
changing legacy behavior, pin the *current* behavior with tests,
so the change is visible against a known baseline. Relocated
legacy material goes to an **attic** directory rather than being
deleted outright.

Greenfield surfaces in a mixed codebase do not carry this
apparatus — they follow the kernel's absorbed-test path.
