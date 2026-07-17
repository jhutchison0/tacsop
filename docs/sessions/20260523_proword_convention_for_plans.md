# Session: Proword Convention for CONOPs and OPORDs

**Date**: 2026-05-23
**Branch**: main
**Tags**: #session #doctrine #infra #docs #complete

**Documents**: [.claude/commands/task.md](../../.claude/commands/task.md) — the file modified this session
**Follows**: [20260519_adopt_doctrine_helper_and_propagation.md](20260519_adopt_doctrine_helper_and_propagation.md) — sixth doctrine propagation cycle that just shipped
**References**: [docs/tasks.md](../tasks.md) — stale P1 cleared, new P3 propagation-bundle task added

---

## Summary

A focused doctrine session. User noticed recent plans had lost their handles — earlier work used memorable prowords (PATHFINDER, "something WIZARD") that made multi-plan conversations easier; current plans were referred to by topic phrases. Investigated `/task`, confirmed the proword logic was not (or no longer) baked into the command. Added a Prowords section to [.claude/commands/task.md](../../.claude/commands/task.md) covering form, picking rules, and a campaign-scaling hook preserved for future use. Also cleared a stale P1 task in [docs/tasks.md](../tasks.md) (the sixth propagation cycle had shipped last session but the task entry hadn't been updated) and replaced it with a P3 entry tracking the two small refinements accumulating for the next propagation cycle.

No production code changed. No tests required. 259 passing, same as session-start.

## Work Completed

### 1. Investigation: where did prowords go?

User question: *"my last several plans haven't had useful names ... does /task still direct that logic or no?"*

Searched [.claude/commands/task.md](../../.claude/commands/task.md) and grepped `.claude/` + `docs/` for `proword|pathfinder|nickname`. Zero hits. Existing CONOP format at line 96 was `conop_NNN_descriptive_name.md` — purely descriptive, no proword. Confirmed proword logic was absent.

Existing plans in [docs/plans/](../plans/) (`decision_science_gaps.md`, `decision_science_utility.md`) bear this out — descriptive but unmemorable, with no single-word handle to refer to them by in conversation.

### 2. Convention design

Two design axes considered, in two rounds with the user.

**Axis 1: per-document-type conventions vs let-loose.** I recommended *light structure for plans only, let everything else loose* — per-type conventions earn their weight only when many of each kind nest inside each other (operations contain objectives contain routes), and this template has plans and tasks. Designing conventions for lower-level nouns (targets, routes, checkpoints) that this template doesn't have would be YAGNI; downstream projects that develop such nouns can add their own conventions. User agreed.

**Axis 2: scope of the doctrine — current vs future.** User clarified that the convention should also preserve doctrine for higher levels (above OPORD) in case a future project ever runs a multi-OPORD campaign — *"a line or two here that preserves the doctrine."* This is a different axis from Axis 1: not which document types get prowords today, but what the convention says about types we might use later. I added a Scaling subsection explicitly marked as *"preserved for future use, not currently needed in this template,"* covering the themed-family pattern (CAMPAIGN THUNDER → OPORD THUNDER STRIKE, OPORD THUNDER BOLT) and the same pattern for waves inside an OPORD.

### 3. Edit applied to [.claude/commands/task.md](../../.claude/commands/task.md)

Three changes in one edit:

| Location | Change |
|---|---|
| Line 96 (CONOP format) | `conop_NNN_descriptive_name.md` → `conop_<PROWORD>_<descriptive_name>.md`, with worked example `conop_pathfinder_decision_science_gaps.md` and the first-line-of-doc convention `# CONOP PATHFINDER — Decision Science Gaps` |
| Line 107 (OPORD format) | Added (was missing entirely): `opord_<PROWORD>_<descriptive_name>.md`. Often inherits the parent CONOP's proword. |
| New Prowords subsection | Form, picking, and scaling rules — about 18 lines. Placed after the Escalation Ladder and before the Phases-vs-Waves terminology section. |

The Prowords subsection content:

- **Scope**: CONOPs and OPORDs only. TCS too small to justify a handle.
- **Form**: 2–3 syllable concrete noun, NATO-phonetic-adjacent. Solo by default; modifier+noun for flavor or family.
- **Picking**: Roll your own. No approved list — memorability is the point. Avoid reusing a proword from an open plan; reuse is fine once that plan closes.
- **Scaling** (future-preservation): Campaign-level work gets a proword and child OPORDs inherit a themed family. Same pattern for waves inside a single OPORD if useful. Convention does not extend to lower-level nouns (objectives, routes, targets) — those belong to downstream projects.

### 4. Task list cleanup

Replaced the stale P1 entry in [docs/tasks.md](../tasks.md):

- **Removed**: "Sixth doctrine propagation — RUN scripts/propagate_doctrine.py to ship the 2026-05-19 entry ..." — already shipped last session per [20260519_adopt_doctrine_helper_and_propagation.md](20260519_adopt_doctrine_helper_and_propagation.md); task entry was never updated.
- **Added (P3)**: "Next doctrine propagation cycle — bundle two small refinements when enough downstream value accumulates" — captures (1) the deep-modules discipline added to CLAUDE.md/python-prototyper in commit `8ad387e` on 2026-05-20, and (2) the proword convention from this session. Explicit "no urgency" framing: 23-artifact bundle shipped 4 days ago; 7 downstream repos still carry unread cycles.

User explicitly opted *not* to distribute this session's changes — bundling for a later cycle is the deliberate choice.

## Key Decisions

| Decision | Rationale |
|---|---|
| Light structure (CONOP/OPORD get prowords; TCS does not) | Per-type conventions earn their weight only when there's a nesting/collision risk to manage. TCS items are too small and numerous for a proword to add signal; CONOPs and OPORDs are the right granularity to want a one-word handle. |
| Roll-your-own picking, no approved word list | The whole point of a proword is the chuckle and the memorability to *the people using it*. A canonical list would centralize the choice and kill the joke. Avoiding open-plan reuse is the only hard rule. |
| Preserve campaign-scaling doctrine even though we don't need it | User's call: *"a line or two here that preserves the doctrine."* Marginal cost of the lines now is much lower than rediscovering the convention later when staring at three related OPORDs without a parent name. Explicit "preserved for future use, not currently needed" disclaimer keeps future readers from thinking it's a current requirement. |
| Explicitly *not* extend the convention to lower-level nouns (objectives, routes, targets) | This template doesn't have them; downstream projects that do can add their own conventions. Preemptively designing for nouns we don't have is the YAGNI failure mode that the propagation system makes expensive (every artifact we ship is a 12-repo blast radius). |
| Do not distribute this session's changes — bundle for next cycle | User's explicit instruction. Two small refinements ([deep-modules discipline](../../CLAUDE.md) from 2026-05-20 + proword convention from today) don't yet justify the disruption of a propagation cycle when 7 downstream repos still have unread cycles backed up. Bundle accumulates; cycle ships when value warrants. |

## Pillar Compliance

| Pillar | Status | Notes |
|---|---|---|
| **Simplicity First** | PASS | Convention design deliberately small. Three changes inside one file. Did not invent new infrastructure (no skill, no hook, no template generator). The convention is a few paragraphs of prose in an already-used command file. Refused the "let's also design conventions for objectives/routes/targets" temptation explicitly. |
| **Shift-Left Testing** | N/A | No production code changed. Pure documentation. Test suite (259 passed) run as PCC verification, not as coverage of the change itself. |
| **Config-Driven** | PASS | The convention is in [.claude/commands/task.md](../../.claude/commands/task.md), which is the single source of truth for the task-management workflow. No duplication elsewhere. |

## Commits

| Hash | Subject |
|---|---|
| (this session) | `[infra] Add proword convention for CONOP/OPORD plans in /task` |
| (this session) | `[doc] Session 20260523: proword convention + propagation cycle accounting` |

## Notes

- The dice-stop hook fired a "Nat 6 — run pytest and check recent code has coverage" prompt mid-session. Acknowledged but not actionable: this session's edits are pure documentation, so coverage doesn't apply. Ran the suite anyway as part of PCC.
- Five untracked files in [docs/](../) and [docs/reviews/](../reviews/) predate the `docs/reviews/YYYYMMDD_<subject>.md` convention and are not from this session. Not touching them in this commit — they belong to a separate cleanup decision (delete vs. rename to the convention vs. archive).
- Convention design followed a clean two-round dialogue: I proposed three options + a recommendation, user picked the recommendation, then user expanded the scope with a thoughtful "and preserve doctrine for above-OPORD too." Worth noting: the user's expansion was the right call and I should have considered it in the first round.

## Next Steps

- [ ] **(P3, carried)** Next doctrine propagation cycle — bundle this session's proword convention with commit `8ad387e`'s deep-modules discipline when downstream value warrants a cycle.
- [ ] **(P3, carried)** GitHub Actions CI workflow.
- [ ] **(P3, carried)** `from_yaml` round-trip tests for 4 value functions.
- [ ] **(P3, carried)** After 1–2 sessions of audit-log data, decide whether to add a Stop hook (Layer 5) or escalate to PreToolUse (Layer 6) per [.claude/skills/shift-left-testing/ENFORCEMENT.md](../../.claude/skills/shift-left-testing/ENFORCEMENT.md).
- [ ] **(housekeeping)** Decide what to do with the five untracked decision-science review docs from 2026-03-26 — they predate the `docs/reviews/YYYYMMDD_*` convention.
