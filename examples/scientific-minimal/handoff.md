# Example handoff

This note is illustrative, not a conversation transcript or evidence of an
actual review. A useful handoff is bounded enough for a new contributor to
resume without guessing.

- **Completed:** the synthetic monthly budget writes residuals and checks
  closure against 0.5 mm/month.
- **Open question:** what tolerance would real observations justify? No field
  data or measurement-error analysis is included here.
- **Next action:** obtain and assess measurement uncertainty before choosing a
  tolerance for real data; do not treat synthetic closure as model validation.
- **Verification run:** with Python 3.13, the balanced program exited 0 and
  the unbalanced input exited 2; the example tests passed. Repeat the
  [water-budget commands](README.md) and record the actual outputs in a real
  handoff.

The short run is a smoke check of this example. It is not scientific validation
against observations or release verification. The illustrative plan's review
and archive do not replace either kind of evidence.
