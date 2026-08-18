# Monitoring activation record

**Immutable.** This file is written once and never edited. The monitoring
window's start is not stored here — it is *derived* from Git as the author date
of the commit that first introduced these exact bytes, so the record cannot
move its own start date. Editing it in place is refused: `pilot-report` compares
the tracked bytes against the working-tree bytes and stops rather than derive a
window from a record that changed after the fact.

What activation does and does not mean, restated here because the distinction is
easy to lose: it opens a window for **collecting evidence** about the review
allocation. It does **not** switch that allocation on — the allocation has been
in force since 2026-08-11 — and an absent or inactive window is absence of
evidence, never a signal that the policy is off.

The window closes at six distinct plan stems reaching `ready-to-archive`, or 60
calendar days from the derived activation date, whichever comes first. At that
boundary the Maintainer's Decision is `retain | revise | retire`.

```cairn-pilot-activation
schema: cairn-pilot-activation/1
machinery_sha: 089a9dba39b935bb77b0e447454d6ff6eb52bd2f
machinery_record_path: dev/plans/archive/review-efficient-lifecycle.md
machinery_record_section: Implementation verification -- Claude (Implementation) -- 2026-08-13 (B2)
```

`machinery_sha` names the reviewed commit whose machinery this window measures,
and it is falsifiable rather than decorative: the named record and section are
read **at the enabling commit**, and activation refuses unless that section
actually attests this commit. The section named above is the Boundary B2
verification — 4276 passed on a clean tree, with the gate re-anchor `cfaace9` ->
`089a9db` verified at zero frozen drift.
