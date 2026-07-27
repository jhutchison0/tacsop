# Session: veil-engine Bootstrap from the Template

**Date**: 2026-07-26
**Branch**: main
**Tags**: #session #template #downstream #planning #complete

**Documents**: [docs/propagation-protocol.md](../propagation-protocol.md) (roster), [docs/tasks.md](../tasks.md)
**References**: `~/projects/github/veil-engine` (the work product: 4 commits, pushed); veil-engine `docs/sessions/20260726_bootstrap_from_tacsop_template.md` (the detailed record); [docs/design/from_template_to_project.md](../design/from_template_to_project.md) (exercised, drift found)
**Follows**: [20260720_prose_doctrine_hypothesis_relicense.md](20260720_prose_doctrine_hypothesis_relicense.md)

---

## Summary

The template got its first post-Cycle-7 field exercise: veil-engine (reactive LED installation runtime, successor to `elephant-graveyard`) was bootstrapped from tacsop @`5f70a48` in one session, from bare `git init` to a doctrine-complete repo with 200 passing tests, day-one CI, and a build CONOP in debate. The Day-1 playbook mostly held; where it drifted from Cycle 7, the drift is now a filed P2 task. Hub-side changes this session are small: roster line, two tasks, this doc.

## Work Completed

1. **veil-engine bootstrapped** (work recorded in its own session doc). Highlights of the hub-relevant findings:
   - Exploration first: two Explore agents (elephant-graveyard architecture map; tacsop doctrine specifics) and one Plan agent (CONOP architecture) fed a plan-mode design before any file moved.
   - The retrospective lessons got applied, not just cited: config-authority is a day-one pillar; a cross-cutting patterns register exists from birth (7 entries from elephant-graveyard's paid lessons); the CONOP's Wave 0 is falsifiers, and its assumptions table caught a tension inside the guidance doc itself (costume classification is a color signal; the primary camera is grayscale IR).
   - Import method: `git archive HEAD | tar -x` copies tracked files only, which cleanly avoided dragging tacsop's five untracked March docs into the new repo.
2. **Playbook drift found and filed (P2)**. `from_template_to_project.md` predates Cycle 7. The trap that would have destroyed doctrine: Step 4 says delete `docs/plans/*.md`, which now includes the CONOP/OPORD format specs. Also missing: prose-skill adoption, `using-topic-branches`, `.gitattributes`, the Apache-2.0 LICENSE, hypothesis plumbing, the consumer-side propagation contract, and the coverage-threshold mismatch. Full list in the task.
3. **Roster updated**: veil-engine added to the informational roster in `propagation-protocol.md`. Discovery is automatic (it has `.claude/commands/` under `~/projects`), so it will receive the next doctrine cycle without further action.
4. **elephant-graveyard status question filed (P3)**: its show is done and its successor now exists, but it keeps receiving doctrine; the protocol still lacks an opt-out mechanism.

## Key Decisions

| Decision | Rationale |
|---|---|
| Bootstrap + CONOP only; no engine code in veil session 1 | Doctrine: the plan reaches Approved before its first wave launches. |
| veil keeps `decision_science` and the decision-scientist agent | The build's open decisions (controller split, perception ceiling) are MAUT candidates; the user's call. |
| Drift fixed as a filed task, not inline this session | The playbook rewrite deserves its own session; the veil session doc preserves the corrected sequence to write from. |
| tacsop's uncommitted tasks.md progress note rides along in this commit | It was true bookkeeping from 2026-07-20 that simply never got committed. |

## Commits

- (this commit) [doc] Register veil-engine downstream; file playbook-drift and elephant-graveyard-status tasks; session doc

## Next Steps

- veil-engine: review CONOP LANTERN to Approved; run Wave 0 falsifiers (bench nights).
- tacsop: fix the Day-1 playbook drift (P2); the corrected sequence lives in veil's bootstrap session doc.
- tacsop: the pre-existing P1/P2 propagation-from-other-machines tasks are untouched and still open.

---

*Session closed 2026-07-26. The template's real test is whether a repo built from it needs the hub again for anything but doctrine; veil-engine starts that experiment.*
