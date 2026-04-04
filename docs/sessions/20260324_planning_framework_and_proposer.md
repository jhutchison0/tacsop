# Session: Planning Framework, Proposer Agent, and Doctrine Propagation

**Date**: 2026-03-24
**Branch**: main
**Tags**: #session #infra #agents #complete

**Documents**: [task.md](../../.claude/commands/task.md) — Escalation ladder updated
**Documents**: [proposer.md](../../.claude/agents/proposer.md) — New agent definition
**Documents**: [feature-development.md](../../.claude/teams/feature-development.md) — Team workflow updated
**References**: [README.md](../../.claude/README.md) — Agent catalog and scope matrix
**Follows**: [20260317_rmi_reboot_clone_cleanup.md](20260317_rmi_reboot_clone_cleanup.md) — Previous session
**Cites**: https://arxiv.org/html/2511.07262v2 — AgenticSciML multi-agent framework paper

---

## Summary

Three infrastructure changes to the agent framework and planning system: unified task detail standard (TCS universal), deconflicted terminology (waves vs phases), and a new proposer agent inspired by the AgenticSciML paper. Also built a doctrine propagation system to notify downstream repos of shared workflow changes.

## Changes Made

### Planning Framework
- **TCS universal**: Every task within a CONOP or OPORD is now specified at TCS (Task, Condition, Standard) detail level. The document type escalates the frame; the task granularity stays consistent.
- **Wave terminology**: "Wave" adopted for tactical parallel agent deployment within CONOPs/OPORDs. "Phase" reserved for strategic roadmap milestones (`project.yaml` build_phases). Added "Terminology: Phases vs Waves" section to escalation ladder.
- Files: `.claude/commands/task.md`, `CLAUDE.md`, `.claude/README.md`

### Proposer Agent
- New `.claude/agents/proposer.md` — reads codebase, writes proposals to `docs/`, instructed not to write code. Same access pattern as code-reviewer (read all, write reports).
- Feature-development team workflow updated: proposer → code-reviewer challenges → user decides → python-prototyper builds → test-runner verifies.
- Inspired by AgenticSciML paper: structured debate before implementation produces better solutions than jumping straight to code.
- Files: `.claude/agents/proposer.md`, `.claude/README.md`, `.claude/teams/feature-development.md`, `CLAUDE.md`

### Doctrine Propagation System
- `docs/doctrine-updates.md` — changelog for shared command/framework changes
- `scripts/propagate_doctrine.py` — drops `.claude/upstream-update.md` into downstream repos across `~/projects/` (github + gitlab)
- `.claude/commands/session-start.md` — new Step 3.6 checks for upstream notifications
- First propagation run notified: paperboy, fema_cria, flood_model, rmi-reboot

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| TCS as universal grain, not just Level 2 | Document type escalates the frame; task detail should be consistent regardless of plan complexity |
| "Wave" not "phase" within orders | Deconflicts from strategic roadmap phases in `project.yaml`. Campaign OPORDs may contain phases of waves but this is deliberate |
| Proposer writes reports, not code | Same access as code-reviewer. Freed from implementation conservatism so it can be bold. Instructed not to write code, not mechanically prevented |
| Proposer model: sonnet | Matches python-prototyper. Creative work benefits from capable model but doesn't need the orchestrator's model |
| Notification via file drop, not git push | Non-destructive, respects downstream tailoring. Each repo reviews and merges selectively |
| Consolidate doctrine entries | One notification per push, not per change. Simpler for downstream repos to process |
| Scan all ~/projects/ subdirs | Not just github siblings — gitlab repos also consume the template workflow |

## Next Steps

- [ ] Add tests for `scripts/propagate_doctrine.py`
- [ ] Update `from_template_to_project.md` with clone-cleanup steps (carryover)
- [ ] Remove dead conftest fixtures (carryover)
- [ ] Downstream repos: review and merge doctrine update on next session-start
