# Session: schelling-point Bootstrapped from a Seed Plan

**Date**: 2026-09-27
**Branch**: main
**Tags**: #session #template #downstream #bootstrap #doctrine #complete

**Documents**: [docs/propagation-protocol.md](../propagation-protocol.md) (roster), [docs/tasks.md](../tasks.md)
**References**: `~/projects/github/schelling-point` in WSL on Nidhogg (the work product; its `docs/sessions/20260927_bootstrap_and_phase0_scaffold.md` is the detailed record and its Phase 0 gate report); [docs/design/from_template_to_project.md](../design/from_template_to_project.md) (followed with the corrections in the playbook-drift task); [20260726_veil_engine_bootstrap.md](20260726_veil_engine_bootstrap.md); propter `docs/sessions/20260830_bootstrap_and_tracer_conop.md`
**Follows**: [20260829_machine_identity_and_lake_conventions.md](20260829_machine_identity_and_lake_conventions.md)

---

## Summary

The hub's newest consumer, `schelling-point`, went from a bare `git init` holding one seed plan to a doctrine-complete repo at its Phase 0 gate in one session. It teaches game theory by simulating it, with every model checked against a textbook answer. It is the third bootstrap in two months and the first built from a maintainer's requirements document rather than a template clone. Hub-side changes are small: two roster names, six filed tasks, one extended task, and this doc.

| Metric | Value |
|---|---|
| Hub commit imported | `54a86a0` (published `origin/main`) |
| Downstream commits | 18 on its `main`, nothing pushed |
| Downstream tests | 23, all passing; CI replayed from a fresh clone |
| Agents deployed | proposer, code-reviewer (challenge, then audit gate), python-prototyper, test-runner |
| Hub findings filed | 6 new tasks, 1 extended |
| Hub tests after the edits | 269 passed, 6 skipped (unchanged) |
| Hub check 5 after the edits (file pass) | 0 MISSING over 24 paths |

## Work Completed

`KB-graph: traversed the bootstrap lineage before importing (the veil-engine hub doc and veil's own record, propter's 20260830 bootstrap doc, the playbook-drift task, and the 2026-08-29 and 2026-08-30 entries) → the import followed the corrected sequence, and a dangling-reference grep found three stale references the playbook does not mention (pcc.md's allowlist of this hub's March docs, pci.md's geo example, two roadmap.md rows), all fixed downstream`

`KB-graph: traced the hook's 2026-08-26 import scan to propter's test imports → src.-prefixed imports never match a partner; verified by execution against 54a86a0 and filed below`

1. **schelling-point bootstrapped** (its own session doc holds the detail). The feature-development team ran the propose-then-challenge cycle before any code: the proposer took twelve decisions against the seed and the doctrine, and the code-reviewer challenged by execution, finding an import cycle and mypy strict failures the spec would have shipped. The prototyper then built the scaffold test-first on a topic branch; the audit gate caught a CI action tag that does not exist, and the branch merged with every code finding fixed.
2. **Roster**: `propter` (missing since its 2026-08-30 bootstrap) and `schelling-point` added to the informational roster in `docs/propagation-protocol.md`.
3. **Findings filed in `docs/tasks.md`**: the hook's import scan misses `src.`-prefixed imports (P2); the WSL tacsop clone holds unpublished hub work (P2); ruff 0.16 rewrites Markdown code fences, Level 0 skill copies included, unless excluded (P2); a WSL distro shares its host's hostname, so one roster entry spans two homes (P3); `/session-start` Step 1.5 hardcodes a POSIX venv path (P3); `setup-uv` needs full version tags past v7 (P3). The playbook-drift task gains this bootstrap's corrections.

## Findings

**The import came from `origin/main`, not the nearest clone.** The WSL tacsop clone on this box sits one unpushed commit ahead (`fee9d11`) with an uncommitted doctrine entry in its working tree. A bootstrap that archived that clone's HEAD would have shipped doctrine the hub never published.

**The seed plan carried two stale premises about the hub's world.** It asked whether to use "GPL v3 to match tacsop" (the hub relicensed to Apache-2.0 on 2026-07-20), and it feared axelrod's Python support (stale) while missing its new hard torch dependency. Downstream plans written from memory of the hub drift the way the hub's own docs do.

**Three fleet-level tool facts surfaced by execution, none by reading**: ruff 0.16 formats Markdown fences by default; `setup-uv` stopped publishing major tags at v8; the hook's import scan cannot see `src.`-prefixed imports. Each is now a task with its evidence.

## Commits

| Hash | Subject |
|---|---|
| (this commit) | [doc] Register propter and schelling-point downstream; file bootstrap findings; session doc |

## Next Steps

- schelling-point: the maintainer reviews its Phase 0 gate report (license, Beesly source, where Phase 1 code lives, lesson format, first push).
- tacsop: the new tasks; the Day-1 playbook rewrite (P2) now has three bootstraps' corrections to draw on.
