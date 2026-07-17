# Doctrine Updates — Staging Area

Entries authored ahead of their propagation cycle. `propagate_doctrine.py` extracts
only the **topmost** entry of `docs/doctrine-updates.md`, so an entry cannot sit in
that file while an earlier cycle is still unpropagated — it stages here instead.

**Promotion checklist** (per staged entry, at distro time):
1. Confirm the prior cycle has been propagated.
2. Set the entry's real date in the `## YYYY-MM-DD:` heading.
3. Move the entry to the **top** of `docs/doctrine-updates.md` (below the header `---`).
4. Delete it from this file (leave the file with just this header when empty).
5. Run the propagation (dry-run first).

---

## 2026-07-XX: Planning Doctrine — Plan-Format Standards, Prowords, Deep-Modules

*(Staged 2026-07-17 for Cycle 8. Do not propagate before the 2026-07-17 NAME CHANGE
entry has shipped — see promotion checklist above.)*

The task-escalation ladder (`/task`: task → task-condition-standard → concept-of-
operations → operations-order) has always specified tasks to a known standard (TCS),
but the two plan-document levels above it had no format standard at all. Two pinned
schemas now exist, following the `docs/adr/ADR-FORMAT.md` house pattern:
`docs/plans/CONOP-FORMAT.md` (concept-of-operations: where design decisions get
debated) and `docs/plans/OPORD-FORMAT.md` (operations-order: the execution form of a
decided strategy, five-paragraph, checkpointed).

The formats were validated against your history before shipping. A four-repo
retrospective (magic-movies, swimming-analytics, elephant-graveyard, tactics-game)
mined 20 multi-session churn episodes, classified with an explicit hindsight-bias
guard: 6 preventable-by-planning, 10 mixed, 3 discovery-priced-in, 1 pure process.
The dominant failure shape everywhere: **a load-bearing assumption with no falsifier
and no kill-criterion**. Second place: **named risks with toothless mitigations**
("we'll add a test later"). The formats' hardening targets exactly these:

- **Assumptions table** — every load-bearing assumption carries its cheapest
  empirical falsifier, its blast radius if wrong, and a kill-criterion.
- **Validate before detailing** — the falsifier runs before dependent
  execution-phases are authored in detail.
- **Execution-phase order derives from the stated dependency chain** — if the plan
  names a source of truth, phase 1 secures it.
- **Gating-metric calibration** — a metric may not gate work until it rank-orders
  known-good above known-bad references.
- **First-contact rule** — the earliest feasible checkpoint runs against the real
  target (real payloads, real hardware, real platform).
- **Checkpoints are commit-gates with a named owner** — a phase is not closed until
  its verifying commit exists.
- **Mid-phase halt** — a live finding that invalidates a phase's precondition halts
  the phase; it outranks the plan's momentum.
- **Terminal statuses + append-only lifecycle** — every plan ends Rejected,
  Complete, or Superseded; approved plans change only by dated amendment.

### Files (tacsop)

```
docs/plans/CONOP-FORMAT.md                        (new)
docs/plans/OPORD-FORMAT.md                        (new)
.claude/commands/task.md                          (promote wiring, template pointers, Prowords section)
CLAUDE.md                                         (deep-modules sentence in Simplicity First)
.claude/agents/python-prototyper.md               (Step 4d interface check)
docs/reviews/20260717_planning_retrospective_*.md (evidence, reference-only)
```

### Adoption-Mode Table

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `docs/plans/CONOP-FORMAT.md` | **TEMPLATE-COPY** | Copy verbatim into your `docs/plans/`. Existing plans are grandfathered — do not rename or restructure them. |
| 2 | `docs/plans/OPORD-FORMAT.md` | **TEMPLATE-COPY** | Copy verbatim. Co-dependent with #1 and #3. |
| 3 | `.claude/commands/task.md` changes | **CUSTOMIZE** | Merge three additions into your copy (exact lines below). Includes the proword convention, which the format files' naming scheme (`conop_<PROWORD>_<slug>.md`) requires. |
| 4 | Deep-modules discipline (`CLAUDE.md`) | **CUSTOMIZE** | One sentence merged into your Simplicity First principle (below). Independent of #1–3; skip cleanly if unwanted. |
| 5 | `python-prototyper.md` Step 4d | **CONDITIONAL** | Only if your repo carries this agent. Copy Step 4d from tacsop's file. |
| 6 | Retrospective reports | **NO ACTION** | Read the one about your repo (table below) — the evidence is your own session docs. |

### Action required

1. Copy `docs/plans/CONOP-FORMAT.md` and `docs/plans/OPORD-FORMAT.md` from tacsop
   into your `docs/plans/` (create the directory if absent).
2. In your `.claude/commands/task.md`, merge:
   - Under the `promote` subcommand, replace
     `- If the user agrees, create a skeleton document in docs/plans/`
     with:
     ```
     - If the user agrees, create a skeleton document in `docs/plans/` using the template in `docs/plans/CONOP-FORMAT.md` (or `docs/plans/OPORD-FORMAT.md`)
     - The plan must exist and reach Approved **before** its first wave launches — a plan written after the build documents, it does not plan
     - Every exit/kill-criterion in the plan carries a named owner; an ownerless criterion defers itself indefinitely
     ```
   - Append to the Level 3 and Level 4 **Format** lines respectively:
     `Template and section standard: docs/plans/CONOP-FORMAT.md.` /
     `Template and section standard: docs/plans/OPORD-FORMAT.md.`
   - If your copy predates the proword convention (no `## Prowords` section), copy
     that whole section from tacsop's `task.md`.
3. (Optional, #4) Append to your CLAUDE.md Simplicity First principle:
   > Prefer deep modules — small interfaces hiding meaningful implementation — over
   > shallow ones; before declaring an interface done, ask whether each parameter is
   > load-bearing or whether the function could derive it from one it already has.
4. (Conditional, #5) If you carry `python-prototyper.md`, copy Step 4d (the
   10-second load-bearing-parameter check after GREEN) from tacsop's file.
5. Read your repo's retrospective report — the format additions cite your own
   sessions as evidence:

   | Repo | Report |
   |---|---|
   | magic-movies | `tacsop/docs/reviews/20260717_planning_retrospective_magic_movies.md` |
   | swimming-analytics | `tacsop/docs/reviews/20260717_planning_retrospective_swimming_analytics.md` |
   | elephant-graveyard | `tacsop/docs/reviews/20260717_planning_retrospective_elephant_graveyard.md` |
   | tactics-game | `tacsop/docs/reviews/20260717_planning_retrospective_tactics_game.md` |
   | (all others) | Skim any report's SUMMARY — the failure shapes are general. |

### Rollback

Everything here is additive. Delete the two FORMAT files, revert the `task.md`
merge, and drop the CLAUDE.md sentence to return to prior state; no artifact
changes runtime behavior. Existing plans are untouched either way.
