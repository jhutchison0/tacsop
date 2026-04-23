# Session: docs/reviews/ Convention and Python 3.11 Bump

**Date**: 2026-04-21
**Branch**: main
**Tags**: #session #infra #agents #doctrine #complete

**Documents**: [.claude/README.md](../../.claude/README.md) — Scope matrix split into per-directory rows
**Documents**: [CLAUDE.md](../../CLAUDE.md) — Agent table updated; Python version bumped
**References**: [project.yaml](../../config/project.yaml) — `paths.reviews` added; Python pinned to 3.11
**References**: [pyproject.toml](../../pyproject.toml) — `requires-python = ">=3.11"`
**Follows**: [20260331_testing_docs_and_template_hardening.md](20260331_testing_docs_and_template_hardening.md) — Previous session
**Cites**: [velocity-scoring/.claude/agents/decision-scientist.md](/home/jhutchison/projects/gitlab/araia_team/c3po_team/velocity-scoring/.claude/agents/decision-scientist.md) — Source of the new convention

---

## Summary

Cross-repo cleanup session driven by a real-world signal: the user noticed that auditing agents (decision-scientist in velocity-scoring) had drifted to a cleaner output convention than the utils template still encoded. Adopted the new convention, ran the code-reviewer to catch what was missed, fixed the gaps, and propagated to 11 downstream repos. Closed with a Python-version bump.

## Work Completed

### 1. Adopt `docs/reviews/YYYYMMDD_<subject>.md` Convention

**Problem**: Reporting agents (decision-scientist, code-reviewer, proposer) wrote to `docs/` with inconsistent filenames. Worst offender: `decision_audit_YYYYMMDD.md` — date buried at the end, no subject, doesn't sort chronologically.

**Solution**: Standardized on `docs/reviews/YYYYMMDD_<subject>.md` across all reporting agents, modeled on the velocity-scoring repo's recent update.

**Files changed (initial pass)**:
- `.claude/agents/decision-scientist.md` — output path + Scope Write
- `.claude/agents/code-reviewer.md` — added Output Format block with header template; Scope Write
- `.claude/agents/proposer.md` — proposals → `docs/plans/`, investigations → `docs/reviews/`; Scope Write split
- `.claude/README.md` — scope matrix `docs/` row replaced with three explicit rows (`docs/sessions/`, `docs/plans/`, `docs/reviews/`)
- `config/project.yaml` — `reviews: "docs/reviews/"` added under `paths:`
- `docs/reviews/.gitkeep` — directory created

### 2. Code-Reviewer Audit and Gap Fixes

Ran `code-reviewer` agent on the changes. It found 4 missed locations and 1 inconsistency:

| Finding | Resolution |
|---------|-----------|
| `.claude/README.md` Inter-Agent Communication prose still said `docs/` | Updated to `docs/reviews/`, added `decision-scientist` |
| `.claude/teams/decision-science.md` role description stale | Updated to `docs/reviews/` |
| `.claude/teams/feature-development.md` table vs workflow inconsistency | Updated proposer row to `docs/plans/` |
| `decision-scientist` missing from `CLAUDE.md` agent table | Added with output path note |
| `python-prototyper.md` had blanket `docs/` Write — contradicted scope matrix | Narrowed to `docs/sessions/`, `docs/plans/` (excludes `docs/reviews/`) |

Final auditor verdict: 12/12 checks pass. Audit report at [docs/reviews/20260421_docs_reviews_convention.md](../reviews/20260421_docs_reviews_convention.md).

### 3. Doctrine Propagation (5th)

Added 2026-04-21 entry to `docs/doctrine-updates.md` with full action checklist. Propagated to **11 repos**:

- **New notifications (3)**: `contract-knowledge-graph`, `velocity-scoring`, `fema_cria`
- **Appended to existing (8)**: `paperboy`, `flood_model`, `fps/maut_platform`, `aar_ai_pipeline`, `agent-eval`, `ldrd2025_ai_pipeline`, `rmi-reboot`, `tc_hurr_risk_modeling`

### 4. Python Minimum Version Bump (3.10 → 3.11)

Updated four locations:
- `pyproject.toml` — `requires-python = ">=3.11"`
- `config/project.yaml` — `python_requires` and `min_version`
- `CLAUDE.md` — Tech Stack section

Tests pass under venv's 3.13.2 interpreter. Tracked in `docs/tasks.md` as `[P2]` for inclusion in the next doctrine propagation push.

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Adopt velocity-scoring's convention rather than invent a new one | The downstream repo already worked through the design; mirror it back so all repos converge instead of diverge |
| Run code-reviewer mid-change rather than at the end | Surfaced 4 missed files (team templates, README prose, CLAUDE.md table) before propagation locked in the gap |
| Narrow python-prototyper scope explicitly | Scope matrix and agent file should agree without enforcement; the matrix is authoritative |
| Hold Python 3.11 bump out of this propagation | User asked to bundle with future updates rather than send a tiny one-line change |

## Pillar Compliance

| Pillar | Status | Notes |
|--------|--------|-------|
| **Simplicity First** | PASS | Convention is one rule (`docs/reviews/YYYYMMDD_<subject>.md`); no new abstractions. |
| **Shift-Left Testing** | PASS | Code-reviewer agent ran during the change, not after — caught 4 issues before commit. |
| **Config-Driven** | PASS | New `paths.reviews` entry in `project.yaml`. Filenames follow the date-prefixed pattern shared with sessions. |

## Commits

| Hash | Subject |
|------|---------|
| `0ae6ab6` | [infra] Adopt docs/reviews/ convention for agent report output |
| `f54e54f` | [infra] Bump minimum Python to 3.11 |

(Plus 2 prior unpushed commits from a previous session: `994f414`, `fd021f0`. 4 commits ahead of origin.)

## Next Steps

- Push to origin (4 commits pending)
- Bundle Python 3.11 bump into the next doctrine propagation
- Continue P3 tasks: GitHub Actions CI workflow; from_yaml round-trip tests for 4 value functions
