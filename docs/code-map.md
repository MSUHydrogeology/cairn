# Filesystem Code Map

`code_map.py` makes a bounded, read-only map of a project tree for architecture
review. It lists top-level components and files, marks non-Python languages as
unsupported for symbol analysis, and reports public Python functions and classes
with their locations and short docstring summaries. It parses source as data;
it never imports or executes inspected files.

The command writes one JSON object to standard output:

```text
python -I tools/code_map.py --root PATH
python -I tools/code_map.py --root PATH --changed src/module.py
python -I tools/code_map.py --root PATH --changed src/a.py --changed src/b.py
python -I tools/code_map.py --root PATH --release
```

The default is a filesystem map. `--changed` compares functions, including
private and nested functions, from the named root-relative files with functions
in the scanned tree. `--release` compares functions throughout that scope.
The public map includes nested public classes and methods; local functions are
neighbor candidates rather than public entries. Similarity is a lead for human review,
not equivalence, correctness, or permission to remove code.

By default, directories named `.git`, `__pycache__`, or `.pytest_cache` are
excluded at any depth. The result declares these names in `scope` and lists each
omitted directory and reason in `omissions`; their contents are not inspected.
Each encountered directory still counts as an entry. Other hidden directories
are not excluded. To inspect one of these directories, name it as `--root`;
the same exclusions still apply to matching subdirectories beneath that root.
`complete` describes only the declared scope, not omitted contents.

Neighbor ranking normalizes identifiers by splitting underscores and
lower-to-upper camel-case boundaries, lowercasing tokens, and dropping numeric
tokens. The score is 70% multiset Jaccard similarity of AST node-type counts
and 30% Jaccard similarity of identifier-token sets. Results use at most five
neighbors per function. Candidate pairs are ordered by root-relative path,
source line, and name. When the pair limit truncates work, `sampling` reports
the full population, comparisons performed, and the unsampled count. Sampling
is deterministic and evenly spaced over the sorted pair population.

## Fixed Limits

The collector stops or reports affected analysis incomplete at these limits:

| Work | Limit |
|---|---:|
| Files and directories visited | 10,000 entries |
| Python source bytes read | 128 MiB total |
| One Python source | 1 MiB |
| AST nodes | 2,000,000 |
| Function and class definitions | 20,000 |
| Neighbor comparisons | 1,000,000 |
| One parser worker | 5 seconds |
| All parser workers | 30 seconds |
| Complete command | 60 seconds |

The parser runs in a separate process that can be terminated on timeout. An
`incomplete` result is not evidence that unreported files or functions are
clean. Each diagnostic names the affected path, the reason, and a concrete
remedy. The result includes measured counts, elapsed parser/command time, and
the limits applied.

## Traversal Boundary

On POSIX, filesystem mode requires descriptor-relative directory access with
no-follow opens. On 64-bit Windows, it supports roots reached through an
ordinary drive letter that maps directly to a local NTFS volume. The Windows
backend holds directory handles while it scans and opens each child relative to
its parent. It does not support network or UNC roots, device or extended path
forms, drive aliases such as SUBST, or non-NTFS volumes. Unsupported roots,
missing native APIs, and unverifiable identities produce an `incomplete`
result; the collector does not switch to weaker path-based traversal.

Both backends refuse symbolic links or reparse points, special files, path
races and inaccessible roots. On Windows, parser workers run under a
kill-on-worker-exit job so a terminated scan does not leave parser descendants
running. These limits address the collector's work and traversal boundaries;
they are not containment of a compromised host.

Filesystem mode does not inspect Git or determine revisions; `revision` is
`null` and `revision_note` explains that limitation. It writes JSON only; it
does not generate HTML. The map is evidence for investigation, not a clean bill
of health.

Run the single-file command with the trusted Python runtime in isolated mode
(`-I`). The script checks this before importing ordinary standard-library
modules, and parser workers also use `-I`; this prevents the inspected project
or the installed `tools/` directory from supplying modules such as `ast` or
`json` during tool startup. Python startup code that runs before the script
entry point remains part of the trusted runtime; this is not host containment.
