# Task Tracker

## Active

- [ ] [P1] Complete the `utils` → `tacsop` rename (ADR-0002, 2026-07-17). DONE 2026-07-17 evening: GitHub rename; WSL box fully migrated (directory, both remotes set-url'd, Claude project-state dir moved). (1) DONE 2026-07-20: old-path cleanup — `~/projects/github/utils` was already gone; `~/.claude/projects/-home-jhutchison-projects-github-utils` turned out to be a real directory (not a symlink) holding 4 never-migrated memory files; memories copied to the tacsop state dir (verified, `utils` references updated), old dir deleted. Remaining: (2) repeat directory rename + `git remote set-url` + project-state-dir move on every other machine with a clone (work, home, laptop); (3) update any external CI/mirror references to the old URL; (4) optional hygiene: `git remote remove main` (redundant duplicate of origin). Propagation itself is tracked in the Cycle 7 task below.
- [ ] [P2] Propagate Cycle 7 from remaining machines. The 2026-07-20 three-part entry (Part 1 NAME CHANGE breaking; Part 2 Planning Doctrine; Part 3 Writing & Testing Doctrine + relicense) shipped from this WSL box 2026-07-20: 14 repos reached (7 appended to unread notifications, 7 new; the box discovered 14, not the 5 predicted). Remaining: run `propagate_doctrine.py` (dry-run first) on the other machine(s) with downstream clones (work, home, laptop per the P1 rename task).
- [ ] [P3] Decide the five untracked March decision-science docs (docs/decision_audit_20260326.md, docs/plans/decision_science_gaps.md, docs/review_decision_science_waves_2_3.md, two docs/reviews/2026-03-26_* files with non-convention names): commit (renamed to convention), or delete. Untracked since March.
- [ ] [P3] Cut version 0.2.0. CHANGELOG [Unreleased] now holds the rename, Windows fixes, relicense, two skill versions, and the hypothesis pilot; the 20260529 session flagged 0.2.0 as due when a cycle accumulated real surface. Bump pyproject + project.yaml, cut the CHANGELOG section.
- [ ] [P3] Add GitHub Actions CI workflow
- [ ] [P3] Fix `exponential()` ZeroDivisionError for tiny nonzero rate (|rate| < ~2.2e-16, where `1 - e^(-rate)` rounds to 0.0). Contract-satisfying input, real crash; found during Hypothesis strategy design for the from_yaml round-trip pilot (2026-07-20). Repro: `exponential(50.0, low=0.0, high=100.0, rate=1e-17)`. Decide: extend the `rate == 0` guard to effectively-zero rates (ValueError), or fall back to `linear()`. Test-first either way.
- [ ] [P3] Evaluate `diagnosing-defects` skill — defer per code-reviewer (bug-fix.md team template already covers the loop); revisit if team template usage data shows underuse
- [ ] [P3] After 1–2 sessions of audit-log data, decide whether to add a Stop hook (Layer 5) or escalate to a PreToolUse hard block (Layer 6) per `.claude/skills/shift-left-testing/ENFORCEMENT.md` escalation criteria
- [ ] [P2] Fix `docs/design/from_template_to_project.md` Cycle-7 drift, found during the veil-engine bootstrap (2026-07-26). The trap that bites: Step 4's "Delete `docs/plans/*.md`" now deletes `CONOP-FORMAT.md`/`OPORD-FORMAT.md` (TEMPLATE-COPY doctrine), and §5's keep-table omits both. Also missing: prose-skill adoption steps (CLAUDE.md kernel, LANGUAGE.md cruft list is load-bearing and must not be deleted), `using-topic-branches`, `.gitattributes`, Apache-2.0 LICENSE, hypothesis plumbing, the consumer-side propagation contract (`.claude/upstream-update.md` appearing unexplained), and the `coverage_threshold` 80-vs-50 mismatch between project.yaml and pyproject. The veil bootstrap session doc records the corrected sequence to write from.
- [ ] [P3] Decide `elephant-graveyard`'s doctrine-consumer status. Its show is done and `veil-engine` (bootstrapped 2026-07-26) succeeds it, but it remains on the propagation roster and will keep receiving every cycle; the protocol names opt-out as an unresolved gap. Decide: keep receiving (it is public and maintained), or design the opt-out mechanism the protocol lacks.
- [ ] [P3] Parked findings from the 2026-07-17 four-repo planning retrospective (`docs/reviews/20260717_planning_retrospective_*.md`), wrong layer for the plan templates: (1) cross-component lessons-learned register — elephant-graveyard re-learned the master-clock fix on a structural twin a week later; (2) inherit sibling-repo pillars at project inception — add to `docs/design/from_template_to_project.md` Day-1 checklist (config-authority existed in 4 of 6 sister repos before elephant-graveyard started). Candidates for a future doctrine cycle.

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
- [x] 2026-05-19: Wave 2 — refactor 3 legacy single-file skills to directory form with sidecar progressive disclosure: `shift-left-testing` (1242→8 files), `configuration-management` (1533→6 files), `python-venv-management` (623→3 files). All SKILL.md files <110 lines; all sidecars <400 lines. Tests still green. SKILLS_FRAMEWORK.md and .claude/README.md updated to reflect the new layout.
- [x] 2026-05-19: Pass 4 fresh-eyes agent review — code-reviewer, decision-scientist, proposer ran in parallel before propagation. Reports in `docs/reviews/20260519_pass4_*.md`. Verdict: GO-WITH-FIXES; six pre-propagation blockers identified.
- [x] 2026-05-19: ADR-0001 — directory-form mandatory for all new skills (`docs/adr/0001-directory-form-mandatory-for-new-skills.md`). First ADR written under the format established same session; exercises the triple-filter gate.
- [x] 2026-05-19: Pre-propagation fixes — invert python-prototyper workflow to test-first; repoint stale `docs/design/pillars.md` ref to `CONTEXT.md` + `config/project.yaml`; correct shift-left-testing SKILL.md false v1.1.0 version-history line; remove snapshot agent count from LANGUAGE.md Roster definition; add `docs/adr/` to CONTEXT.md reading order.
- [x] 2026-05-19: Shift-left-testing enforcement layer — A5 PostToolUse audit hook (`.claude/hooks/post-tool-shift-left-audit.sh`) wired via `.claude/settings.json`, logs `MISSING_TEST` / `OK_TEST_EXISTS` to `.claude/audits/shift-left-violations.log` (gitignored). Never blocks. `ENFORCEMENT.md` sidecar documents the gradient (probabilistic → deterministic), the hook spec, and why we don't hard-block (per MAUT in `docs/reviews/20260519_pass4_enforcement_maut.md`). CLAUDE.md Development Principle strengthened to test-first vertical-slice. Hook verified firing in-session via real Edit.
- [x] 2026-05-19: Author the 2026-05-19 doctrine-updates.md entry (22-artifact bundle with adoption-mode master table; 469 lines). Largest propagation cycle to date. Propagation script extraction verified.
- [x] 2026-05-19: Pass 5 fresh-eyes review of the doctrine-updates entry (code-reviewer + decision-scientist + proposer; reports in `docs/reviews/20260519_pass5_*.md`). Verdict: SHIP-WITH-FIXES. One BLOCKER (invalid bash `case` alternation in §7 example), three HIGH footguns (settings.json merge worked example, diff-before-delete on session-end skill, diff-before-replace on directory-form skills, python-prototyper substitution sites), and seven CONCERNs all applied to the entry before commit.
- [x] 2026-05-19: Decision-scientist MAUT on propagation strategy — A6 (bundle + scripts/adopt_doctrine.py helper) ranked top at 0.760; A4 (1-week pilot to 2–3 repos first) runner-up at 0.743. A4 vs A6 fork deliberately deferred to next session.
- [x] 2026-05-19: Pass 6 review and comprehensive rewrite of `docs/design/from_template_to_project.md` (Day-1 playbook). code-reviewer found 11 FAILs + 10 CONCERNs against current repo state; proposer redesigned the structure to 12 sections (added NEW §3 Doctrine Infrastructure + NEW §4 Test-First Enforcement Layer). 569 → 791 lines. Closes the gap where the Day-1 playbook predated the entire doctrine cycle.
- [x] 2026-05-19: Build `scripts/adopt_doctrine.py` (A6 helper) test-first under the new shift-left enforcement layer. 9 vertical slices (one cycle each); 35 tests across 8 test classes covering all 9 functions including the fragile settings.json merge (5 cases: no file / no hooks key / other matcher / our matcher present / dry-run). End-to-end verified against a sandbox: dry-run plan correct, live run substitutes hook glob (3 sites), creates settings.json with `Write|Edit` matcher, appends gitignore, prints manual-attention checklist for the 10 judgment-required items. Idempotent re-run skips everything cleanly. Added as artifact #23 in the 2026-05-19 doctrine-updates entry (TEMPLATE-COPY mode) with new §23 subsection. Full repo: 189 → 224 tests passing.
- [x] 2026-07-17: Rename repo `utils` → `tacsop` — ADR-0002, living docs, both propagation scripts, standalone NAME CHANGE doctrine entry (commit `acfba0c`)
- [x] 2026-07-17: Four-repo planning retrospective (magic-movies, swimming-analytics, elephant-graveyard, tactics-game) — 20 episodes classified with hindsight-bias guard; reports in `docs/reviews/20260717_planning_retrospective_*.md`
- [x] 2026-07-17: Harden `CONOP-FORMAT.md`/`OPORD-FORMAT.md` from retrospective findings (Assumptions block with falsifiers/blast-radius/kill-criteria, validate-before-detail, gating-metric calibration, commit-gate checkpoints, first-contact rule, mid-wave halt, terminal statuses, append-only lifecycle) + wire `/task promote` to the templates
- [x] 2026-07-20: Hypothesis pilot — property-based round-trip tests for `from_yaml` wiring of exponential, logarithmic, step, piecewise_linear (`tests/unit/test_from_yaml_properties.py`: 1 concrete anchor + 4 properties, 5 vertical slices). Plumbing: `hypothesis>=6.0` in dev extras, `.hypothesis/` gitignored, dev/ci profiles in `tests/conftest.py` (50/300 examples). Suite 263 → 268 passing. Found 1 real bug during strategy design (tiny-rate ZeroDivisionError, new Active task).
- [x] 2026-07-20: Prose doctrine shipped. Reviewed the two lead-authored skill updates (writing-simple-and-direct v1.0.0; shift-left-testing 2.1.0 sidecars), resolved rule 8 scope (headings and special text exempt; crisp rule, gentle consequence), swept the doctrine corpus with 4 parallel editors (~150 edits, 31 files; `docs/reviews/20260719_writing_style_sweep.md`), ran ADOPTION steps 1-3 (CLAUDE.md kernel, LANGUAGE.md cruft list with term-of-art carve-out, code-reviewer checklist line), appended Amendments to ADR-0001/0002 recording the blessed append-only exception.
- [x] 2026-07-20: Relicense GPL v3 stub → Apache-2.0 (sole authorship verified via shortlog; full canonical LICENSE, README, pyproject PEP 639 + setuptools>=77 floor; CHANGELOG entry; metadata verified via editable reinstall).
- [x] 2026-07-20: Cycle 7 Part 3 authored and appended (entry retitled 2026-07-20); propagated from this box to 14 downstream repos (7 append, 7 new).
- [x] 2026-07-26: veil-engine bootstrapped from the template @5f70a48 (import, rename, strip, CI, doctrine artifacts, CONOP LANTERN in debate; 4 commits pushed). Roster updated in propagation-protocol.md; playbook-drift and elephant-graveyard-status tasks filed.
