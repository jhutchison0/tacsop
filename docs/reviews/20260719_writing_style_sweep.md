# Review: Writing Style Sweep of Doctrine Corpus

**Date**: 2026-07-19
**Reviewer**: Lead (Claude), with four parallel editor agents
**Protocol**: `.claude/skills/writing-simple-and-direct/REVIEWING.md` (four passes: point, structure, words, punctuation)
**Scope**: `.claude/skills/` (all skills), `README.md`, `LANGUAGE.md`, `CONTEXT.md`, `CLAUDE.md`, `config/project.yaml` prose strings, `docs/design/`, `docs/adr/`
**Excluded**: `docs/plans/`, `docs/reviews/`, `docs/sessions/` (records, grandfathered per the skill's "Not retroactive" guardrail)

---

## Verdict

The corpus passed at Minor-only severity and now passes clean. Roughly 150 edits landed across 31 files (+167/−145 lines). No content, links, commands, code, version numbers, or data values changed; every edit is punctuation, a stated connective, or a cut throat-clearing sentence. All 263 tests pass and `config/project.yaml` parses after the sweep.

This sweep deliberately overrides the skill's grandfathering clause for one reason, on the lead's instruction: these files are the doctrine source that propagates downstream, so they serve as the style exemplars.

## Findings by pass

1. **Point (rule 1)**: 4 findings, all fixed. `SKILLS_FRAMEWORK.md` and `docs/design/roadmap.md` opened with "This document defines..."; `maintaining-ubiquitous-language` led with attribution instead of its point (attribution moved to a References section); `CLAUDE.md` line 3 trimmed.
2. **Structure (rule 3)**: folded into the rule 8 fixes. Where a dash hid a causal claim, the rewrite states the link ("because", "so"). Examples: `VERTICAL-SLICING.md` L9, `ANTIPATTERNS.md` L195, `from_template_to_project.md` L219/L769.
3. **Words (rules 5/6)**: 1 finding ("core" in `pillars.md` L3, cut). The corpus was otherwise already clean: zero banned cruft words and zero information-free hedge stacks across ~40 files. "Robust Pick" in `LANGUAGE.md` stays; it is a decision-science term of art, not cruft.
4. **Punctuation (rule 8)**: ~140 em dashes in running prose replaced with the mark that states the relationship. Exempt positions untouched: headings, list-lead separators ("**Name** — gloss"), tables, blockquotes, code fences and docstrings, quoted specimens, en-dash ranges.

## Content patches (from the shift-left 2.1.0 lens)

- `TIERS.md` directory layout gained `golden/` and `scripts/` entries, matching the updated `SKILL.md` tree and pointing to `REGRESSION.md` / `SCRIPTS.md`.
- `PATTERNS.md` gained a float-equality caveat after the OrderCalculator tests, pointing to `NUMERIC.md`. The editor agent corrected the orchestrator's proposed wording: 0.10 is not exactly representable in binary, so the note says the products "happen to come out exact" (verified in Python), not "exactly representable".

## Flags for the lead

1. **Accepted ADRs were edited.** `ADR-FORMAT.md` declares accepted ADRs append-only. ADRs 0001 and 0002 received punctuation-only fixes (meaning, status, dates, checkboxes untouched) per the sweep instruction. Either bless style-only fixes as an exception at commit, or revert: `git checkout docs/adr/0001* docs/adr/0002*`.
2. **One wording addition**: `maintaining-project-context/SKILL.md` L94 gained the word "belong" so a parenthetical parses as a sentence.
3. **Optional consistency items, not applied**: `roadmap.md` L43 keeps a "**Name** — gloss" list separator its siblings integrate into sentences; `from_template_to_project.md` §5 module catalog (10 entries) and unbolded definition-list leads in `VALIDATION.md` L81-84 / `maintaining-project-context` L24-26 keep their exempt lead-separator dashes. Converting them is a house-pattern decision, not a rule violation.
4. **Left stale by design**: `config/project.yaml` `state.*` strings (session-end rewrites them) and `commands:` glosses (name-to-gloss separators, exempt).

## Verification

- Em-dash residue grep across the swept corpus: every remaining match sits in an exempt position.
- Cruft grep: zero matches.
- `config/project.yaml`: parses (`yaml.safe_load`).
- Test suite: 263 passed, 0 failed, 2.0s.
- Spot-read diffs of `CLAUDE.md` (machine instructions) and both rewritten openers: meaning identical.

## Related

- Prior finding source: in-session prose review of the skills corpus, 2026-07-19 (this sweep implements it).
- Rule 8 scope resolution (headings and special text exempt) landed the same day in `writing-simple-and-direct/RULES.md`; this sweep is its first application.
- Pending, deliberately not part of this sweep: `ADOPTION.md` steps 1-3 (CLAUDE.md kernel block, LANGUAGE.md cruft list, code-reviewer checklist line) and the hypothesis dev-dependency for `PROPERTY-BASED.md`.

---

## Resolutions (2026-07-20)

- Flag 1 resolved: the lead blessed the accepted-ADR edits as a one-time exception while field-testing the skill. Amendment notes appended to ADR-0001 and ADR-0002 record it.
- ADOPTION step 2 landed: the cruft list is now in `LANGUAGE.md` with a term-of-art carve-out (a listed word used as a defined selection or design criterion, e.g. "robust", is vocabulary, not cruft).
