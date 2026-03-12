# Session: Infrastructure Audit

**Date**: 2026-03-12
**Branch**: main
**Tags**: #session #config #complete

**Documents**: [pillars.md](../design/pillars.md), [roadmap.md](../design/roadmap.md)

---

## Summary

Full audit of the template repository at Phase 1 completion. This document records findings across project structure, utility modules, test coverage, configuration, dev workflow, documentation, and packaging.

---

## Strengths

### Project Structure
- Clean `src/myproject/` layout follows Python packaging best practices.
- `pyproject.toml` is the single packaging source of truth; `config/project.yaml` is the single runtime source of truth — no duplication.
- Optional dependency groups (`excel`, `slack`, `database`, `weights`, `all`) are a real strength. Users only install what they need.
- `.gitignore` is comprehensive and covers all expected artifact types.
- `archive/` is gitignored — old experiment files are preserved but not polluting the active codebase.

### Utility Modules — Individual Quality
- **logger.py**: Solid OOP design. Color-terminal detection via `isatty()` is correct and non-intrusive. Handler clearing on re-import avoids a common "duplicate log" footgun. Timezone fallback logic is clean.
- **geo.py**: Pure stdlib, zero dependencies. Haversine and bearing formulas are correct; reference URL cited. Function signatures are clean and fully typed.
- **math_utils.py**: The docstring correctly flags that `math.comb` exists in 3.8+ and explains why the module is kept. Two implementations for the same computation is educational.
- **parallel.py**: Both patterns (producer-consumer and starmap) are included. Default worker counts are sensible (2x CPU for I/O-bound, CPU-1 for CPU-bound).
- **slack.py**: Thin wrapper around `slack_sdk`. Token falls back to env var — correct pattern. Raises `ValueError` when no token is available rather than silently failing.
- **database.py**: Clear separation between `DatabaseManager` (write) and `LogReader` (read). `UNIQUE` constraint on `log_name` plus SELECT FOR UPDATE before INSERT is a reasonable conflict-avoidance pattern.

### Dev Workflow Infrastructure
- Three-agent roster (test-runner, code-reviewer, python-prototyper) with clear separation of concerns. Agent README includes a scaling table — genuinely useful guidance.
- PCC/PCI command pair is well-designed. PCC is a fast, deterministic checklist; PCI is context-aware. The military framing is effective for explaining the distinction.
- `/task` escalation ladder (Task → TCS → CONOP → OPORD) is a strong framework for scoping work appropriately.
- Session-start and session-end commands provide real workflow guardrails.
- `SKILLS_FRAMEWORK.md` clearly distinguishes Level 0 (portable) from Level 1 (project-specific) skills — makes the framework maintainable.
- `CLAUDE.md` is accurate, concise, and actionable.

### Documentation
- `pillars.md` includes violation examples for each pillar — exactly what makes pillars actionable rather than aspirational.
- `roadmap.md` uses a good phased structure and explicitly allows Phase 3+ to be vague.
- `CHANGELOG.md` follows Keep a Changelog format correctly.
- Mermaid-over-ASCII preference is documented in CLAUDE.md.

---

## Gaps & Issues

### Critical

**1. Coverage is 4% — only math_utils has any tests.**

Seven of eight utility modules have 0% test coverage. Given that "Shift-Left Testing" is a named design pillar and the CLAUDE.md says "Every new component must include a test plan," this is a direct pillar violation at Phase 1 completion. The modules that ship with zero tests:
- `geo.py` — pure functions, trivially testable
- `logger.py` — handler setup is testable; timezone fallback is testable
- `excel.py` — requires optional deps but can be gated with `pytest.importorskip`
- `parallel.py` — producer-consumer and starmap both testable
- `weights.py` — pure computation, testable
- `slack.py` — testable with mock
- `database.py` — testable with mock or in-memory

**2. `database.py` mixes sync and async incorrectly.**

`DatabaseManager.__init__` and `_create_table` are synchronous and use a sync `psycopg.connect`. But `insert_or_update_data` and `process_logs` are `async` and call `await self.conn.cursor()` and `await self.conn.commit()` on what is a sync connection. This will raise `TypeError` at runtime: sync psycopg connections don't support `async with` or `await`.

The fix requires either: (a) switch to `psycopg.AsyncConnection` throughout, or (b) make `insert_or_update_data` synchronous. As written, the module is broken.

**3. `weights.py` imports `numpy` and `pandas` but they are listed under the `weights` optional group, not `all`-inclusive by default.**

The `all` group in pyproject.toml does include `weights`, so `pip install -e ".[all]"` works. But the CLAUDE.md Quick Commands section lists `pip install -e ".[excel]"` for Excel and doesn't mention `[weights]` as a separate install step. A user following CLAUDE.md exactly would not know they need `[weights]` to use `weights.py`. Minor, but creates a friction point.

### Warnings

**4. `excel.py` — `update_excel_workbook` resets the DataFrame index unconditionally.**

At line 98: `df = df.reset_index(level=0, drop=False)` is called when `keep_index=False`. The intent seems inverted — when `keep_index=False`, you want to drop the index. But `drop=False` means "add the index as a column." This looks like a logic error.

Compare to `save_excel_table` which respects `keep_index` correctly (only inserts index column when `keep_index=True`). The `update_excel_workbook` behavior is inconsistent.

**5. `logger.py` — `Formatter.converter` is a global mutation.**

Line 72: `logging.Formatter.converter = lambda *args: datetime.now(tz).timetuple()` modifies a class-level attribute on the standard library's `logging.Formatter`. This affects all formatters in the process, not just the ones created by this logger. If multiple loggers are set up with different timezones, the last one wins globally. This is a known Python logging footgun.

**6. Coverage configuration is incomplete in `pyproject.toml`.**

`[tool.pytest.ini_options]` only has `testpaths` and `pythonpath`. There is no `[tool.coverage.run]` or `[tool.coverage.report]` section. Running `pytest --cov=myproject` fails with a "Module myproject was never imported" warning because the package path is `src/myproject` but coverage is looking for a top-level `myproject` module. The correct invocation is `pytest --cov=src` but this is not documented anywhere.

**7. `session-end.md` skill contains domain-specific content for a different project.**

The commit tag taxonomy includes `[source]`, `[select]`, `[distill]`, `[pipeline]`, `[tts]` — these appear to be from a news-aggregation project ("paperboy"). The session-end command (`.claude/commands/session-end.md`) uses the correct generic tags (`[util]`, `[config]`, `[doc]`). The skill and the command are inconsistent, and the skill would mislead users of this template.

Similarly, the branch naming section in `session-end.md` lists `dev-source`, `dev-select`, `dev-distill`, `dev-pipeline` — domain-specific to the other project. Level 0 skills should contain no project-specific content.

**8. `SKILLS_FRAMEWORK.md` references "paperboy" in the Level 1 examples section.**

> For paperboy, potential Level 1 skills might include...

This exposes the origin project. Should be replaced with generic placeholder examples.

**9. `src/__init__.py` is empty; `src/myproject/__init__.py` is empty.**

Having `src/__init__.py` as a package (with `__init__.py`) is unusual and conflicts slightly with the `where = ["."]` + `include = ["src*"]` package discovery in pyproject.toml. The standard `src` layout convention treats `src/` as a root directory, not a package. This works in practice but is unconventional and could confuse new users of the template.

**10. `math_utils.py` has no input validation.**

`nCr(n, r)` calls `math.factorial(r)` and `math.factorial(n - r)`. If `r > n` or if either argument is negative, `math.factorial` will raise a `ValueError` from the stdlib. There is no guard or descriptive error message. The function signature promises `int` arguments but doesn't validate them. At minimum, the docstring should note the constraints.

**11. `conftest.py` fixtures are unused.**

`project_root` and `sample_data` fixtures exist in `tests/conftest.py` but neither is referenced in any test. They appear to be placeholder stubs.

### Informational

**12. No `README.md` at the project root.**

The repository is a GitHub template. Without a README, new users cloning it have no entry point. CLAUDE.md is for Claude Code, not for humans browsing GitHub.

**13. No CI/CD configuration.**

The shift-left-testing skill documents a GitHub Actions example, but there's no `.github/workflows/` directory. A template repository arguably should ship with a working CI workflow.

**14. `src/myproject/utils/__init__.py` doesn't re-export anything.**

It contains only a docstring. Whether this is intentional (users import directly from submodules) or an oversight (convenience imports were planned) is unclear. Documenting the intended import pattern would help.

**15. `config/project.yaml` coverage threshold is 80% but the project ships at 4%.**

The YAML says `coverage_threshold: 80`. This config value is not read by any Python code and is not wired into pytest. It's documentation-only. If taken at face value against the current codebase, the project fails its own threshold by a wide margin.

---

## Recommendations

### Must Fix (before claiming Phase 1 is production-ready)

1. **Fix `database.py`**: Choose sync or async throughout. Recommend converting to fully async with `psycopg.AsyncConnection` since `insert_or_update_data` and `process_logs` are already declared async. Or simplify to sync if async isn't needed.

2. **Add tests for `geo.py` and `logger.py`**: These are pure functions / deterministic setup code — easiest to test, highest value. Start here. Target `tests/unit/test_geo.py` and `tests/unit/test_logger.py`.

3. **Fix `excel.py` `update_excel_workbook`**: The `drop=False` in `reset_index` when `keep_index=False` looks inverted. Verify intended behavior and add a test that covers both `keep_index=True` and `keep_index=False`.

4. **Fix `session-end.md` skill**: Remove all domain-specific content (paperboy branch names, commit tags). Replace with generic examples. This is a Level 0 skill — it must be project-agnostic.

5. **Fix `SKILLS_FRAMEWORK.md`**: Remove "paperboy" reference from the Level 1 examples section.

### Should Fix

6. **Add coverage configuration to `pyproject.toml`**:
   ```toml
   [tool.coverage.run]
   source = ["src"]

   [tool.coverage.report]
   fail_under = 80
   show_missing = true
   ```
   And update CLAUDE.md to document the correct coverage invocation.

7. **Add a `README.md`**: A template repository needs a human-readable entry point that explains what it is, how to use it, and how to customize it for a new project.

8. **Add `logger.py` timezone mutation note to docstring**: Document that `Formatter.converter` is a global — callers setting up multiple loggers with different timezones will encounter conflicts.

9. **Add input validation to `math_utils.py`**: Guard for `r > n`, negative inputs.

10. **Add `[weights]` install note to CLAUDE.md**: Add `pip install -e ".[weights]"` to the optional deps table.

### Consider

11. **Add a GitHub Actions CI workflow**: Even a minimal `pytest` run on push would demonstrate the shift-left-testing pillar in practice.

12. **Re-export public API from `src/myproject/utils/__init__.py`**: Document whether `from myproject.utils import get_distance` is the intended pattern or whether `from myproject.utils.geo import get_distance` is preferred.

13. **Replace or remove unused `conftest.py` fixtures**: Either use them or remove them to avoid confusion.

---

## Module-by-Module Notes

| Module | Quality | Issues |
|--------|---------|--------|
| `logger.py` | Good | Global `Formatter.converter` mutation; no tests |
| `geo.py` | Excellent | No issues found; no tests |
| `math_utils.py` | Good | No input validation; well-tested |
| `weights.py` | Good | Complex algorithm, readable; no tests |
| `excel.py` | Mixed | `update_excel_workbook` `keep_index` logic appears inverted; no tests |
| `parallel.py` | Good | Clean patterns; no tests |
| `slack.py` | Good | Thin, correct; no tests |
| `database.py` | Broken | Sync/async mismatch makes `insert_or_update_data` uncallable; no tests |

---

## Test Coverage Assessment

**Current state**: 4% overall. Only `math_utils.py` (100%) has tests.

**Priority order for adding tests** (easiest to hardest):

1. `geo.py` — pure functions, stdlib only, no side effects. Write 8-10 tests covering known distances and bearings, edge cases (same point, antipodal points, poles).

2. `logger.py` — create temp directory, call `setup_logger`, assert handlers are created, assert log file exists. Test handler deduplication on re-call.

3. `math_utils.py` — already at 100%; add edge case for negative inputs and `r > n`.

4. `weights.py` — requires `numpy`/`pandas`; gate with `pytest.importorskip("numpy")`. Test with int input, list input, dict input, and ties.

5. `parallel.py` — producer-consumer and starmap can be tested with trivial functions (e.g., `lambda x: x * 2`). Requires care around multiprocessing in pytest (use `if __name__ == "__main__"` guard or `spawn` context).

6. `excel.py` — requires openpyxl/xlsxwriter; gate with `pytest.importorskip`. Test `excel_style_index` (pure function, no deps). Test `save_excel_table` with a temp file.

7. `slack.py` — test with `unittest.mock.patch` on `WebClient`. Test token-from-env fallback and `ValueError` when no token.

8. `database.py` — fix sync/async issue first, then test with mock psycopg connection.

**Target**: After fixing `database.py` and adding tests for `geo.py` and `logger.py`, coverage should be near 40%. Completing the list above should reach the documented 80% threshold.
