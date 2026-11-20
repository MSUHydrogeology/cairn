# Plan D1 detail: exact code, texts and cases

Companion to `dev/plans/2026-11-20-defect-arc-d-gate-and-windows-checks.md`, part of that plan. It exists because the exact code shapes and fixture cases would push the plan past its word budget, and a low-tier implementer must not have to invent them. Nothing here widens the plan's Scope. Line numbers are at the commit the plan was opened on; find each by the quoted text if they have moved.

## D1. Chunk 1, restore the new-file scan (`tests/_gate_preflight.py`)

Replace the two constants and their comment (near line 1345) with:

```python
#: Added files under these roots are scanned, except test modules and fixtures.
_SCAN_NEW_FILE_ROOTS = ("install/", "release/", "dev/tools/", "tests/")
_SCAN_NEW_FILE_EXCLUDED = ("tests/fixtures/",)
```

Add, directly under them, one function:

```python
def _is_test_module(rel: str) -> bool:
    """A file under tests/ named test_*.py: pytest runs it as a test, and the
    layout before 0.8 left it out of the new-file scan on purpose."""
    return (rel.startswith("tests/") and rel.endswith(".py")
            and rel.rsplit("/", 1)[-1].startswith("test_"))
```

In `_scan_range`, the `in_scope` expression gets one more clause, so the last term reads:

```python
or (change == "added"
    and rel.startswith(_SCAN_NEW_FILE_ROOTS)
    and not rel.startswith(_SCAN_NEW_FILE_EXCLUDED)
    and not _is_test_module(rel)))
```

Nothing else changes except the docstring of `_scan_range`: in its `Scope:` paragraph replace the line `range adds under `install/`, `release/`, or `dev/tools/`. Everything` with the two lines `range adds under `install/`, `release/`, `dev/tools/`, or `tests/` (test` and `modules and `tests/fixtures/` excepted). Everything`, so the list of roots matches the restored behaviour. `release/repin.py` line 203 reads these two constants from the prior verifier's own copy of the file, so it is not edited. The pattern list, size limits, `_LISTED_MODES` and the report schema stay as they are.

Why this shape. Before the move, `scripts/` (every new tool) and `bootstrap/` outside the old test folder were scanned. The move put the former `scripts/` tools at the top of `tests/` (for example `tests/gauge.py`), where the scan stopped looking. New non-test files under `tests/` (a tool, a `conftest.py` or `__init__.py` in a subfolder, a helper module) run at collection or as tools. New `test_*.py` modules and `tests/fixtures/` were left out before and stay out; scanning every new test would put `subprocess` and file-write hits for nearly every test on the Maintainer's page.

New test node in `tests/test_ceremony_review_report.py`, next to `test_scope_covers_the_roster_and_new_files_and_lists_the_rest`, built with the file's own `_make_range`, `_report` and `_hits`:

- Name: `test_a_new_non_test_file_under_tests_is_scanned_and_a_new_test_module_is_not`.
- Anchor holds `{"docs/guide.md": "a\n"}`. Candidate holds that file and five added files, each with the one line `import subprocess\n`: tests/new_tool.py, tests/sub/conftest.py, tests/security/test_new.py, tests/test_new.py, tests/fixtures/data.py.
- Expect `{p for p, _l, _n in _hits(rep)} == {"tests/new_tool.py", "tests/sub/conftest.py"}`, `rep["scan"]["scanned"] == ["tests/new_tool.py", "tests/sub/conftest.py"]`, and `sum(rep["scan"]["not_line_scanned"].values()) == 3` (the three excluded added files; docs/guide.md is unchanged and not listed).
- The existing node keeps its tests/test_new.py expectation unchanged.

Developmental probe (deleted before archive): put `"tests/"` back in `_SCAN_NEW_FILE_EXCLUDED`; the new node must fail. Run the new node once at the starting commit; it must fail there.

## D2. Chunk 2, name the record in the fork-advisory test (`tests/test_fork_advisory.py`)

In `test_node16_f5_parametric_no_lockfile_field_can_suppress_at_upgrade`, in the `elif overrides == {"src": "../../../../etc/hostname"}:` branch:

1. Keep `assert rc == 2, err` and the existing `'src' is not a plain relative file name` line. Delete nothing.
2. Before them, add (function-local import, as the file does everywhere): `from install.scaffold import read_lockfile  # noqa: PLC0415`, then
   `number = next(n for n, rec in enumerate(read_lockfile(target)["files"], 1) if rec.get("dst") == "dev/tools/intent.py")`.
3. Add `assert f"record {number}: the lockfile's 'src' is not a plain relative file name" in err, err`.

The refusal text comes from `_contained_lockfile_path` in `install/_scaffold/upgrade.py`, which prefixes `record {n}: ` with the record's position in the lock's `files` list, counted from 1; `_check_lockfile_paths` counts the same list. No word such as "containment" is matched, which is the Maintainer's answer on the wording check (chat, 2026-11-20: "Drop it.").

If the implementer's first run at the starting commit shows an `err` with no `record <n>:` text, stop and return the plan to `revising-plan`; do not match other words.

Developmental probe: change `number` to `number + 1`; the node must fail. A second probe: leave the planted record's `src` valid and give a different record the hostile `src` by hand; the node must fail.

## D3. Chunk 3, Windows spelling of `file=` (`release/check_release_test_members.py`)

Add above `compare`:

```python
def _report_file(raw: object, windows: bool | None = None) -> object:
    """pytest writes the `file=` field with the host's separator, a backslash
    on Windows. Read it as forward slashes there and nowhere else; the
    comparison with the file the classname names, and every later check in
    `_file`, are unchanged."""
    if windows is None:
        windows = os.name == "nt"
    return raw.replace("\\", "/") if windows and isinstance(raw, str) else raw
```

In `compare`, change only the `file` line to
`if "file" in case.attrib and _file(root, _report_file(case.attrib["file"])) != filename:`.
`_file`, the policy reader (`other_platform_skips`) and `required_files` keep refusing a backslash. The `file` field never decides which file a case belongs to; the classname does.

Permanent nodes in `tests/contract/test_release_members_contract.py`, through `_check` (the checker's command line), each built from the file's `_xml()` helper with `file=` set on its `testcase` (`suite[0].set("file", value)`):

- `test_backslash_file_field_is_refused_off_windows`, skipped on `os.name == "nt"` with reason `"on Windows the backslash spelling is accepted; the next test covers it"`: `file="tests\\test_security_lint.py"` gives return code 1 and `invalid test-file identity` on stderr.
- `test_backslash_file_field_is_accepted_on_windows`, skipped unless `os.name == "nt"` with reason `"pytest writes a backslash file= path only on Windows"`: the same report gives return code 0.
- `test_file_field_naming_another_file_is_refused`, every host: `file="tests/test_security_marker.py"` (written with the host's separator) for the `test_security_lint` case gives return code 1 and `test file and classname identities disagree`.
- `test_dotdot_in_a_windows_file_field_is_refused`, every host: `file="tests/../tests/test_security_lint.py"` (written with the host's path separator) gives return code 1 and `not a canonical relative path`.

The four nodes start from the `evidence` fixture and rewrite the report, as `test_report_refusals` does.

Developmental probe on any host: import the module with `importlib.util` and check `_report_file("tests\\a.py", windows=True) == "tests/a.py"`, `_report_file("tests\\a.py", windows=False) == "tests\\a.py"` and `_report_file(5, windows=True) == 5`.

## D4. Chunk 4, freeze from a fresh clone (`release/RELEASE_PROCESS.md`)

Insert after the first code block of "Strict release-security evidence" (the three `security_check.py` lines), by exact insertion, this paragraph:

> Freeze from a fresh clone, not from a working checkout. `--freeze-history` records every ref in the repository and stops with `cannot peel to a commit` when a ref points at a tree; some tools leave such refs in a working checkout (the Codex tool's `refs/codex/turn-diffs/...`). A new `git clone` of the clean Mac authority, checked out at the cut commit, copies branches and tags and none of those. Before the freeze, fetch `refs/cairn/gate-anchor` into the clone from the trusted origin and verify its signed commit; fetch nothing after the freeze. Take the Mac record and run the join from that same clone: the join refuses when the repository's refs or its location differ from the frozen manifest. The Windows record is taken in the Windows checkout, with the same manifest file. The join's `PASS` covers only the commit it names. Push only that commit as `master`: where you push from, `git rev-parse master` must print it; if not, stop and freeze again.

Do not touch the `bash` block that the contract test reads, or any other line. The basis is `release/security_check.py` (`_collect_source_inventory` and the live-against-frozen comparison in `_run_join`): read, not run.
