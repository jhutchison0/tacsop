# Session: RMI Reboot Clone Cleanup

**Date**: 2026-03-17
**Branch**: main
**Tags**: #session #infra #complete

**References**: [from_template_to_project.md](../design/from_template_to_project.md) — Template-to-project guide consulted during cleanup
**Follows**: [20260317_pre_clone_fixes.md](20260317_pre_clone_fixes.md) — Pre-clone fixes session

---

## Summary

Cleaned the rmi-reboot repo (cloned from utils template) down to a minimal starting point. Stripped 7 unused utility modules, reset template-era docs, and updated all references. Also captured two memory entries for improving future clone workflows.

## Changes Made (in rmi-reboot)

- Deleted 7 utility modules: `geo.py`, `math_utils.py`, `weights.py`, `excel.py`, `parallel.py`, `slack.py`, `database.py`
- Deleted `tests/unit/test_math_utils.py`
- Cleaned `pyproject.toml` — removed 4 optional dep groups, removed `all` group (dead indirection)
- Updated `CLAUDE.md` — stripped deleted module references, removed optional install commands, updated tech stack
- Reset `docs/tasks.md`, `CHANGELOG.md`
- Deleted 3 template-era session docs and `from_template_to_project.md`
- Updated `docs/design/roadmap.md` — removed deleted module references
- Updated `.claude/README.md` — removed template wording
- Cleaned `conftest.py` — removed unused `sample_data` and `project_root` fixtures
- Created `docs/design/background/example_session.md` — session doc format reference

## Changes Made (in utils — memory only)

- Added `project_template_clone_workflow.md` — lessons from the clone process, missing Day-1 checklist steps
- Added `feedback_clone_preserve_commands.md` — guardrail: never strip `.claude/commands/` or `.claude/skills/` during clone cleanup

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Remove `all` dep group entirely | Was just `[dev]` alias after stripping others — dead indirection |
| Remove both conftest fixtures | Neither was referenced by any test in template or clone |
| Preserve `.claude/commands/` and `.claude/skills/` intact | Carry workflow logic (knowledge graph in session-end) — not template scaffolding |

## Next Steps

- [ ] Update `from_template_to_project.md` in utils to include clone-cleanup steps (delete session docs, reset CHANGELOG, reset tasks, clean .claude/README.md)
- [ ] Remove dead `sample_data` fixture from utils template conftest.py
- [ ] Consider removing `project_root` fixture from utils template conftest.py (also unused)
