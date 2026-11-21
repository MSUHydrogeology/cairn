# Custom session routines

## Session start

At an attended, explicitly requested session-start, offer the opt-in Meter only
when `dev/tools/meter.py` is installed, no enabled consent config exists, and no
remembered refusal appears in this routine. Show the exact provider-log roots
and project paths proposed for consent, the private ledger at
`~/.cairn/meter/ledger.json`, each sanitized project export path, and that
recurring work and cost depend on the selected logs and are unmeasured. Ask
before creating the consent file. The offer does not run a refresh or read
provider logs. Unattended starts make no offer, private-source read or config
write.

If the person declines, remember that choice only if they ask: add a
non-private instruction here to reoffer only on request. If they do not ask to
remember it, add nothing. An enabled consent config or remembered refusal
means no offer.

## Goodnight

**Usage report, every goodnight (reflection-only included).** When Meter is
installed, run `python dev/tools/meter.py refresh --report --json` once, or use the
result if the session-end skill has already run it. On success, include the
complete sanitized `cairn-pulse/1` record in the reflection. For a closed
`partial`, `unavailable` or `disabled` receipt, include only the status and
reason exactly as reported; missing or failed usage is never zero. This fresh
report joins only the current configured project after its export succeeds. Do
not read an older `meter.json` export in `dev/measurement/`, pass an aggregate path, or
commit a per-project export. If it exits without a valid pulse or closed
receipt, report unavailable without raw diagnostics. Collection reads only roots and projects in the
private consent file `~/.cairn/meter.json`; never create or edit it without the
Maintainer's clear yes. The full-handoff pre-prune refresh remains a separate
locked step and still fails closed.

Slow tests remain due at release and whenever an accepted plan, safety or
security requirement, or the Maintainer requires them. Change-specific checks
and Boundary B remain due on their existing schedule. Goodnight does not defer
or replace them.
