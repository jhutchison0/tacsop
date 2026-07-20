# Session: Prose Doctrine, Hypothesis Pilot, Apache-2.0 Relicense, Cycle 7 Ship

**Date**: 2026-07-19 / 2026-07-20
**Branch**: main
**Tags**: #session #doctrine #skills #testing #license #propagation #complete

**Documents**: [.claude/skills/writing-simple-and-direct/](../../.claude/skills/writing-simple-and-direct/), [.claude/skills/shift-left-testing/](../../.claude/skills/shift-left-testing/), [tests/unit/test_from_yaml_properties.py](../../tests/unit/test_from_yaml_properties.py), [LICENSE](../../LICENSE)
**References**: [docs/doctrine-updates.md](../doctrine-updates.md) 2026-07-20 entry; [docs/reviews/20260719_writing_style_sweep.md](../reviews/20260719_writing_style_sweep.md); [CHANGELOG.md](../../CHANGELOG.md) `[Unreleased]`
**Follows**: [20260529_windows_portability_fixes.md](20260529_windows_portability_fixes.md)

---

## Summary

Cycle 7 shipped. The session took the lead's two uncommitted skill updates (a new
`writing-simple-and-direct` prose-style skill and four new `shift-left-testing`
sidecars), hardened them by review, applied them to the whole repo, and closed the
long-staged propagation cycle: entry retitled 2026-07-20 with a new Part 3,
committed, and pushed to 14 downstream repos from this box.

| Metric | Value |
|---|---|
| Prose sweep | ~150 edits across 31 files, 4 parallel editor agents |
| Skills shipped | writing-simple-and-direct v1.0.0 (new); shift-left-testing 2.1.0 |
| Tests | 263 → 268 passing (5 new property tests; hypothesis 6.157.0) |
| Real bugs found | 1 (`exponential()` tiny-rate ZeroDivisionError, task filed) |
| License | GPL v3 stub → Apache-2.0 (full canonical text, PEP 639 metadata) |
| Propagation | 14 repos (7 append, 7 new) |
| Commits | `9978231` (53 files) + this session-close commit |

## Work Completed

1. **Session start caught rename fallout.** The `utils` → `tacsop` rename had left
   the venv shebangs dead (rebuilt at the new path), `origin` pointing at the old
   URL (lead fixed), and three stray personal scripts at repo root from an Aug 2025
   catch-up commit (lead deleted; committed this cycle).
2. **Rule 8 resolved.** Em dashes stay banned in running prose; headings, list-lead
   separators, tables, quotes, and specimens are exempt. The "pirate's code"
   question (guidelines vs. rules) settled as: crisp rule, gentle consequence.
   Bright lines transfer to weaker models; the non-blocking severity ladder is
   where the flexibility lives. An explicit "Not a gate" bullet was drafted and
   deliberately held.
3. **Skills reviewed, then the review implemented.** Four-pass protocol over the
   corpus found Minor-only severity: zero cruft words anywhere, two rule 1 openers,
   ~45 prose em dashes, two consistency gaps. Four parallel editors applied the
   sweep; verification greps, YAML parse, and the suite all clean. One editor
   corrected the orchestrator's float-representability wording in the PATTERNS.md
   patch (verified in Python before writing).
4. **Adoption ran in-repo before propagating.** CLAUDE.md Prose Style kernel,
   LANGUAGE.md cruft list with the term-of-art carve-out ("robust" as a selection
   criterion is vocabulary, not cruft), code-reviewer checklist line. ADR-0001 and
   ADR-0002 style edits were blessed as an append-only exception, recorded via new
   Amendments sections in each.
5. **Hypothesis pilot.** Dev-extra + dev/ci profiles + five vertical slices closed
   the standing from_yaml round-trip task. Strategy design alone surfaced a real
   crash: `exponential()` divides by zero for nonzero `|rate| < ~2.2e-16`. Filed
   with repro; fix awaits a design call (extend the zero guard vs. linear fallback).
6. **Relicense.** GPL v3 (a 22-line stub) → Apache-2.0 full text. Sole authorship
   verified via `git shortlog`; README and pyproject (`license = "Apache-2.0"`,
   setuptools>=77) updated; installed metadata verified. Rationale: a template hub
   should not copyleft-contaminate downstream derivatives; Apache keeps attribution
   and adds the patent grant.
7. **Cycle 7 shipped.** Part 3 (writing/testing doctrine + relicense + known-issue
   notice) appended to the combined entry, entry retitled 2026-07-20,
   SKILLS_FRAMEWORK inventory tree brought current (it had also been missing
   ENFORCEMENT.md and using-topic-branches since their creation). Propagated:
   14 repos discovered on this box, not the 5 the task predicted.

## Key Decisions

| Decision | Rationale |
|---|---|
| Rule 8 exemptions over softened wording | A graded rule fails on exactly the models that need it; enforcement gentleness lives in the severity ladder, matching the audit hook's detect-deterministically, respond-educationally posture. |
| Sweep overrides grandfathering for the hub | The hub's files are the exemplars downstream repos copy; records (sessions, reviews, plans) stayed untouched. |
| ADR style edits via Amendments, not revert | Lead blessed a one-time exception while field-testing the skill; the append records the exception, keeping the append-only rule's spirit. |
| Writing skill ships as 1.0.0 | The drafted two-file 2.0.0/1.0.0 history never existed in git; first committed version is 1.0.0 so footers keep mapping to history. |
| Apache-2.0 over MIT | Keeps attribution and license retention (§4) plus the explicit patent grant; "lessen friction, maintain lines of credit" was the lead's stated intent. |
| Constrain the rate strategy instead of widening the test | The tiny-rate crash is a value_functions bug, not a from_yaml wiring bug; the round-trip suite keeps one claim per test and the bug gets its own task. |

## Next Steps

- Propagate Cycle 7 from the remaining machines (work/home/laptop clones).
- Fix `exponential()` tiny-rate crash, test-first, after the design call.
- Cut 0.2.0 (CHANGELOG `[Unreleased]` has accumulated real surface).
- Decide the five untracked March decision-science docs.
- P1 rename remainders: other machines' clones, old Claude state dir cleanup.
- GitHub Actions CI workflow (P3): the hypothesis ci profile is already wired for it.

---

*Session closed 2026-07-20. Cycle 7 is live downstream; the style doctrine applies to everything written here from now on, this document included.*
