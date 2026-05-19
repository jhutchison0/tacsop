# Task Tracker

## Active

- [ ] [P1] Sixth doctrine propagation — bundle: LANGUAGE.md skill, CONTEXT.md skill, ADR system, SKILLS_FRAMEWORK v2 (Anthropic Dec 18 open standard), shift-left-testing vertical-slicing upgrade, session-end skill/command deduplication, propagation-protocol.md, Python 3.11 minimum bump. Each downstream repo will receive LANGUAGE.md and CONTEXT.md as **starter templates** to be customized per-project.
- [ ] [P3] Add GitHub Actions CI workflow
- [ ] [P3] Add from_yaml round-trip tests for exponential, logarithmic, step, piecewise_linear value functions
- [ ] [P3] Evaluate `diagnosing-defects` skill — defer per code-reviewer (bug-fix.md team template already covers the loop); revisit if team template usage data shows underuse

## Blocked

## Completed

- [x] 2026-03-12: Infrastructure audit — full template quality review (docs/sessions/20260312_infrastructure_audit.md)
- [x] 2026-03-12: From Template to Project guide (docs/design/from_template_to_project.md)
- [x] 2026-03-12: Rewrite .claude/ agent framework — single README, teams/, scope matrix
- [x] 2026-03-17: Fix database.py sync/async mismatch — converted to fully synchronous
- [x] 2026-03-17: Scrub paperboy content from session-end.md skill and SKILLS_FRAMEWORK.md
- [x] 2026-03-24: Update escalation ladder — TCS as universal task detail standard across all plan types
- [x] 2026-03-24: Adopt "wave" terminology for tactical agent deployment, reserve "phase" for strategic roadmap
- [x] 2026-03-24: Add proposer agent — bold problem analyst with debate-before-implementation workflow
- [x] 2026-03-24: Build doctrine propagation system — changelog, notification script, session-start check
- [x] 2026-03-24: First doctrine propagation to 4 downstream repos (paperboy, fema_cria, flood_model, rmi-reboot)
- [x] 2026-03-25: Add .gitattributes for cross-platform line ending normalization (LF)
- [x] 2026-03-25: Second doctrine propagation — 9 repos notified (shark, agent-eval, beesly-equilibrium, elephant-graveyard, magic-movies, paperboy, project-megan, quest-engine, tactics-game)
- [x] 2026-03-26: Decision science module — Wave 1: MAUT scorer, 7 value functions, from_yaml(), 82 tests
- [x] 2026-03-26: Decision science module — Wave 2: sensitivity analysis (OAT, Monte Carlo, scenario compare), 31 tests
- [x] 2026-03-26: Decision science module — Wave 3: visualization (radar, tornado, heatmap), 32 tests
- [x] 2026-03-26: Add decision-scientist agent (Level 1) and decision-science team template
- [x] 2026-03-26: CONOP: decision_science_utility.md — full 4-wave plan with migration path for 6 repos
- [x] 2026-03-26: End-to-end integration test for decision_science pipeline (8 tests)
- [x] 2026-03-26: Team review hardening — 3 bugs fixed, 3 defensive guards, 3 analysis features (explain, dominance, robustness)
- [x] 2026-03-26: Third doctrine propagation — 9 repos notified of decision_science module
- [x] 2026-03-30: Add append mode to doctrine propagation script — preserves unread updates instead of overwriting
- [x] 2026-03-30: Fourth doctrine propagation — decision science update to 10 repos (5 new, 5 appended to existing)
- [x] 2026-03-31: Add 14 tests for propagate_doctrine.py — extract, build, discovery, propagate with append
- [x] 2026-03-31: Fix excel.py update_excel_workbook keep_index inverted logic
- [x] 2026-03-31: Remove dead sample_data and project_root fixtures from conftest.py
- [x] 2026-03-31: Add 10 tests for geo.py — haversine distance and bearing with known city pairs and edge cases
- [x] 2026-03-31: Improve logger.py — optional log_dir, get_logger() convenience function, customizable datefmt
- [x] 2026-03-31: Add 10 tests for logger.py — color handling, file creation, console-only, handler dedup, custom datefmt
- [x] 2026-03-31: Add coverage config to pyproject.toml — threshold 50%, show_missing, exclude_lines
- [x] 2026-03-31: Update from_template_to_project.md — clone-cleanup steps, logger/pathlib/coverage updates, fixed issues archived
- [x] 2026-03-31: Rewrite README.md — template repo + upstream doctrine hub with two LOEs
- [x] 2026-04-21: Adopt docs/reviews/YYYYMMDD_<subject>.md convention across all reporting agents
- [x] 2026-04-21: Add decision-scientist to CLAUDE.md agent table (was missing)
- [x] 2026-04-21: Narrow python-prototyper write scope to exclude docs/reviews/
- [x] 2026-04-21: Fifth doctrine propagation — docs/reviews/ convention to 11 repos (3 new, 8 appended)
- [x] 2026-04-21: Bump minimum Python version 3.10 → 3.11 in pyproject.toml, project.yaml, CLAUDE.md
- [x] 2026-05-19: Three-agent Pass 1 review of `docs/design/hold/plan1.md` (proposer grill, code-reviewer audit, decision-scientist MAUT — reports in `docs/reviews/`)
- [x] 2026-05-19: Add `docs/design/hold/` to .gitignore as per-repo scratch workspace
- [x] 2026-05-19: Rename `.claude/settings.local.json` → `.claude/settings.json` (Anthropic convention)
- [x] 2026-05-19: Write `LANGUAGE.md` (project-specific glossary; decision science + agent framework + escalation ladder + governance terms; cites Pocock's pattern, not vocabulary)
- [x] 2026-05-19: Write `CONTEXT.md` (project identity, mission, current state, constraints, key relationships)
- [x] 2026-05-19: Write `docs/propagation-protocol.md` (formalized the doctrine-propagation evaluation gate, batching rules, append mode, rollback)
- [x] 2026-05-19: Build ADR system — `docs/adr/ADR-FORMAT.md` + `docs/adr/.gitkeep` + `.claude/skills/recording-architecture-decisions/SKILL.md` (Pocock's triple-filter gate)
- [x] 2026-05-19: Build `.claude/skills/maintaining-ubiquitous-language/` skill (directory form)
- [x] 2026-05-19: Build `.claude/skills/maintaining-project-context/` skill (directory form)
- [x] 2026-05-19: Update `.claude/skills/SKILLS_FRAMEWORK.md` to Anthropic Dec 18 open standard (frontmatter spec, directory form, progressive disclosure, civilian/military vocabulary crosswalk)
- [x] 2026-05-19: Upgrade `.claude/skills/shift-left-testing.md` with vertical-slicing (tracer-bullet) discipline from Pocock's tdd skill
- [x] 2026-05-19: Resolve session-end skill/command duplication — moved reference content to `docs/session-doc-format.md`, deleted `.claude/skills/session-end.md`, updated command to reference new doc
