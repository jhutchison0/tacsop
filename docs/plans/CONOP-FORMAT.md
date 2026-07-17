# CONOP Format

This is the template for Concepts of Operations in this repo. CONOPs live in `docs/plans/conop_<PROWORD>_<descriptive_name>.md`. See `.claude/commands/task.md` for the escalation ladder that promotes work to CONOP level, and the proword conventions.

A CONOP is where **design decisions get debated**. If the strategy is already decided and the work only needs sequenced execution, skip the CONOP and write an OPORD (see `OPORD-FORMAT.md`). If there are no design decisions and no parallel tracks, the work does not warrant a CONOP — keep it at TCS level in `docs/tasks.md`.

This format codifies the structure validated in practice by `docs/plans/decision_science_utility.md` — the sections below existed there before they existed here.

---

## When to Write a CONOP

Promote from TCS to CONOP when **any** of the following hold (from the escalation ladder in `task.md`):

- Multiple waves of work that could run in parallel
- Design decisions needed before coding
- Touches 4+ components or introduces new architecture
- Will span multiple sessions

Every task inside a CONOP is specified at **TCS detail level** — the document type escalates the frame; the task granularity stays consistent.

---

## Template

Copy this template into `docs/plans/conop_<PROWORD>_<slug>.md`. First line of the doc carries the proword.

```markdown
# CONOP <PROWORD> — <Descriptive Name>

**Status**: Draft | In Debate | Approved | Superseded by OPORD <PROWORD>
**Date**: YYYY-MM-DD
**Lead**: <name>
**Parent task**: <link or line reference into docs/tasks.md>

---

## Problem

What we're solving and why it matters. One or two paragraphs, no more.
If this can't be stated crisply, the work isn't understood well enough
to plan yet.

---

## Situation

### Friendly Forces (what we have)
Existing modules, agents, skills, fixtures, and prior art this plan
can build on. Name files.

### Enemy Forces (what works against us)
Risks, failure modes, constraints, and technical debt actively working
against this plan. Be specific — "complexity" is not an enemy force;
"the scorer has no test coverage for degenerate weight vectors" is.

### Terrain (the ground we operate on)
The relevant shape of the codebase and ecosystem: gaps we can exploit,
boundaries we must respect, dependencies we inherit.

---

## Mission

One sentence. Who, what, by when, **in order to** what. The "in order
to" clause is mandatory — it is the purpose that survives contact when
the plan's specifics don't.

---

## Approaches Considered

At least two, including one bold alternative that challenges
assumptions (per the `proposer` agent's charter). For each: what it
is, pros, cons, risk level.

### Approach A: <Name>
### Approach B: <Name> (bold alternative)

**Recommendation**: Which approach and why. Be direct about trade-offs.

---

## Design Decisions

Decisions this CONOP resolves, each with its rationale. Decisions that
remain **open** must be flagged here — open design decisions block
promotion to OPORD. If a resolved decision passes the ADR triple
filter (hard to reverse, surprising without context, real trade-off),
write the ADR and link it.

---

## Measures of Success

- **MOP (performance)**: Did we do the thing right? Tests green,
  coverage, lint, review findings addressed. Mechanical, checkable.
- **MOE (effectiveness)**: Did the thing work? The outcome in the
  world the plan exists to change — the downstream repo migrated, the
  scorer adopted, the workflow faster.

A plan with MOP but no MOE measures activity instead of outcome.

---

## Wave Breakdown

Waves are tactical parallel-execution units. Each wave gets:

### Wave N — <Name>
- **Team**: which template from `.claude/teams/`, with modifications
- **Tasks**: every task at TCS detail level

  | Task | Condition | Standard |
  |------|-----------|----------|
  |      |           |          |

- **Exit criterion**: the single shared condition that closes the wave

---

## What We Do NOT Build

Explicit non-goals. This section prevents scope creep more cheaply
than any review gate.

---

## Agent and Team Design

New agents or team templates this plan requires, or "none — uses
existing roster." If new, specify scope-matrix rows before
implementation begins.

---

## References

Related CONOPs/OPORDs, ADRs, session docs, external sources.
```

---

## Status Values

- **Draft** — being written; not yet ready for challenge.
- **In Debate** — under review by `code-reviewer` (and `decision-scientist` when a decision model is in scope).
- **Approved** — lead has selected an approach; open design decisions resolved or explicitly deferred with rationale.
- **Superseded by OPORD <PROWORD>** — execution has begun under an OPORD, which usually inherits the proword. The CONOP is kept as the record of *why*; the OPORD is the record of *how*.

---

## Promotion Gate: CONOP → OPORD

Promote only when **all** of the following hold (from the escalation ladder):

- [ ] The CONOP's design decisions are resolved (or explicitly deferred with rationale)
- [ ] Waves must run in a defined sequence
- [ ] Wave-by-wave completion needs tracked checkpoints

If any box is unchecked, execute directly from the approved CONOP — not every CONOP needs an OPORD.

---

## Adoption

Reference this file from the `promote` subcommand in `.claude/commands/task.md`:

> If the user agrees, create a skeleton document in `docs/plans/` **using the template in `docs/plans/CONOP-FORMAT.md` (or `OPORD-FORMAT.md`)** and link the task to the new document.

---

## Sources

- FM 5-0 / ADP 5-0 (Army planning doctrine) — Situation/Mission structure, mission statement form, MOE/MOP distinction.
- `docs/plans/decision_science_utility.md` — the validated in-practice structure this format codifies.
- `docs/adr/ADR-FORMAT.md` — the house pattern for pinned document schemas.
