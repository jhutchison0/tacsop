# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **Windows portability**: `scripts/adopt_doctrine.py` now forces UTF-8 stdio at module load so the Unicode arrows (`→`) in status messages don't crash on Windows cp1252. Caught when `heimdall-darkroom` adopted the 2026-05-19 doctrine bundle as the first Windows downstream.
- **Windows portability**: `.claude/hooks/post-tool-shift-left-audit.sh` now normalizes Windows backslash paths to forward slashes before the case-glob match. Without this, the hook silently no-op'd on Windows because `*/src/<pkg>/*.py` could not match `C:\…\src\<pkg>\foo.py`. Recursive subdirectory matching also clarified in comments (case patterns match across slashes).
- **Windows portability**: `src/myproject/utils/logger.py` now catches `ZoneInfoNotFoundError` (a `KeyError` subclass, NOT `ImportError`/`ValueError`) in the timezone-resolution fallback. On Windows + Python 3.9+ without the `tzdata` package, `ZoneInfo("America/Chicago")` raises this exception; the prior except clause did not catch it and any caller of `get_logger()` would crash at import time. Originally surfaced in `heimdall-darkroom` on 2026-04-22, finally propagated.
- **Windows portability**: `tests/unit/test_adopt_doctrine.py::TestPlanCopies::test_sources_rooted_at_upstream` now uses `Path.is_relative_to` instead of `str(src).startswith("/fake/upstream/")` so the assertion works on Windows where `Path()` normalizes to backslash separators.
- **Windows portability**: `tests/unit/test_adopt_doctrine.py::TestSubstituteHook::test_executable_bit_preserved` now skips on `win32`. NTFS has no POSIX `+x` bit; `chmod(0o755)` is a no-op on Windows. Hooks invoked via `bash <path>` from the harness don't need the bit anyway.

### Added
- `tzdata; sys_platform == 'win32'` to the base dependencies in `pyproject.toml`. CPython's bundled `zoneinfo` has no backing data on Windows; installing `tzdata` makes named timezones work as expected. The `logger.py` fallback above guarantees graceful behavior even if the dep is missing.
- `tests/unit/test_logger.py::TestTimezoneFallback::test_setup_logger_falls_back_when_zoneinfo_data_missing` — regression coverage for the `ZoneInfoNotFoundError` fix.

## [0.1.0] - 2026-03-12

### Added
- Project template structure with `src/myproject/utils/` layout
- Utility modules: logger, excel, parallel, geo, weights, slack, database, math_utils
- `pyproject.toml` with optional dependency groups (dev, excel, slack, database, weights, all)
- Claude Code infrastructure: 3 agents, 5 commands, 5 Level 0 skills
- Documentation templates: design pillars, roadmap, task tracker
- Example test suite with conftest fixtures
- `config/project.yaml` as single source of truth
