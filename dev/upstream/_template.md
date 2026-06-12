<!-- Usage: copy this file to dev/upstream/<YYYY-MM-DD>-<slug>.md and fill
     the sections. Keep the draft clean and factual — it is a precursor to
     a real upstream report. Move to archive/ once filed/resolved/abandoned. -->

# {{short-slug}} — upstream issue draft

**Library / tool**: {{name and version of the upstream dep}}
**Date first observed**: {{YYYY-MM-DD}}
**Reporter**: {{role or name}}
**Status**: draft  <!-- update to: filed | resolved | wont-fix | abandoned -->
**Upstream reference**: (none yet)  <!-- fill with issue/PR URL once filed -->

## Environment / versions

```
Cairn version: (your version)
library: (e.g. somelib==1.2.3)
Python: (e.g. 3.12.4)
OS: (e.g. macOS 14.5)
```

Add any other version details that affect reproducibility (CUDA, libc,
driver version, compiler, etc.).

## Reproduction

Minimal, self-contained steps to trigger the issue:

```python
# Paste the smallest reproducer here.
```

Or describe the steps in prose if code is not the right medium.

## Expected behavior

What should happen.

## Actual behavior

What actually happens. Include error messages / tracebacks verbatim.

## Analysis

(Optional) What you believe is the root cause. Useful for the upstream
maintainer; skip if you are not yet sure.

## Filing status

* [ ] Maintainer approved filing
* [ ] Filed at: {{issue URL}}
* [ ] Upstream response: {{summary or link}}
* [ ] Resolved / closed: {{resolution outcome}}

---

*Move this file to `dev/upstream/archive/` once filed and resolved
(or abandoned). Update the Status field before moving.*
