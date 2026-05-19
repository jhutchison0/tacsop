# ADR-0001: Directory Form Mandatory for All New Skills

**Status**: Accepted
**Date**: 2026-05-19
**Decision-maker(s)**: jhutchison (lead); code-reviewer, proposer, decision-scientist agents (Pass 4 review)

---

## Triple-Filter Check

- [x] **Hard to reverse** — once propagated to 11+ downstream consumer repos, reverting requires coordinated cross-repo rewrite. The progressive-disclosure benefit (sidecar files loaded on demand) is forfeited on reversion.
- [x] **Surprising without context** — a contributor authoring a 50-line skill might reasonably ask: "Why am I creating a directory for this?" The default intuition is that single-file is simpler for small things.
- [x] **Result of a real trade-off** — single-file is genuinely simpler per-skill and was the historical pattern; directory form has structural overhead. The trade-off chose prevention of the 1500-line monolith over per-skill ergonomics.

All three filter conditions pass. ADR is warranted.

---

## Context

By the end of the 2026-05-19 doctrine-artifact session, this repo held six skills. Three were under 150 lines; three were 623, 1242, and 1533 lines in single-file form. The large skills had grown gradually past the point where they could be loaded into agent context without consuming a disproportionate share of the budget, and past the point where a contributor could orient quickly to "what does this skill do?"

Anthropic's December 2025 open skills standard had codified a directory form (`SKILL.md` plus sidecar files, progressive disclosure) explicitly to prevent skills from outgrowing their context budget. Matt Pocock's skills repo had been using the pattern in production for months.

The Wave 2 refactor of the same session migrated all three legacy single-file skills to directory form. The question this ADR resolves is: **what rule do we propagate downstream and apply going forward?**

A draft of `SKILLS_FRAMEWORK.md` v2 included a numeric trigger ("migrate at >500 lines"). The author noted in the Pass 4 review that every legacy skill we had crossed the 500-line trigger without anyone noticing — the rule self-violated until a manual audit caught it. That observation drove this decision.

---

## Decision

**All new skills MUST be authored in directory form** (`.claude/skills/<name>/SKILL.md` + optional sidecars), regardless of expected size. The single-file form (`.claude/skills/<name>.md`) is **not used** for any new skill. Legacy single-file skills have been migrated; no further single-file skills are added to this repo or any downstream repo adopting this doctrine.

Concretely:

- A new skill starts at `.claude/skills/<name>/SKILL.md` with the standard YAML frontmatter (`name`, `description`, `version`, optional `allowed-tools`).
- Sidecars are added when topical separation warrants them, not at a line-count threshold. A 30-line skill is a directory with one file; that is correct.
- `SKILLS_FRAMEWORK.md` v2 documents the layout spec; this ADR records the mandatory-not-optional nature of the rule.

---

## Alternatives Considered

### Alternative A: Numeric trigger ("migrate at >N lines")

A line-count threshold (500 was the leading number) that mandates directory form only past that point. Smaller skills stay single-file. Appealing because it preserves zero-overhead for genuinely small skills.

Rejected because:
- Every legacy skill in this repo crossed the 500-line trigger without anyone noticing or acting on it. The rule self-violated.
- Authors do not reliably predict how a skill will grow; the threshold debate would recur at every PR.
- The cost of "premature" directory form is one extra directory and one extra file — trivial. The cost of "delayed" directory form is a 1500-line monolith refactor — non-trivial.
- A numeric rule invites argument; a categorical rule does not.

### Alternative B: Keep single-file as default; allow directory form when authors prefer

The historical pattern in this repo. Continues what most external skill packs use. Rejected because we had just spent a session refactoring three monoliths created under exactly this rule. Continuing it predicts a re-occurrence.

### Alternative C: Mandatory directory form for all (this ADR)

Slight per-skill overhead: even a 30-line skill is a directory with one file. Eliminates the "when to migrate" debate. Aligns with the Anthropic Dec 2025 open standard. Makes future sidecar additions (ENFORCEMENT.md, HOW-TO.md, etc.) natural to add without restructuring.

---

## Consequences

### Positive

- New skills are structurally ready for sidecars from day one. The "we need to restructure to directory form" sprint cannot recur.
- Aligns with Anthropic's December 2025 skills open standard.
- Progressive disclosure becomes the default frame when authoring a new skill, even when the first version is small.
- Eliminates a recurring debate ("is this skill big enough to warrant a directory?").
- Sidecars that capture enforcement, how-to guides, or anti-pattern catalogs are first-class — see `shift-left-testing/ENFORCEMENT.md` written the same day as this ADR for a concrete example.

### Negative

- Per-skill overhead: a 30-line skill is a directory with one file instead of a single file. Slightly more typing; slightly more `ls` output.
- Contributors new to the project may find the convention surprising at first. `SKILLS_FRAMEWORK.md` and this ADR carry the explanation.
- Single-file skills authored externally (e.g., quoted from third-party skill packs) cannot be dropped in unchanged; they require minimal wrapping into a directory.

### Neutral

- No legacy single-file skills remain after the Wave 2 refactor. This ADR codifies the existing state of the repo, it does not change current files.
- Propagating this ADR downstream means all consumer repos adopt the same rule. They receive the SKILLS_FRAMEWORK v2 in the same propagation cycle, so the rule arrives with its documentation.

---

## References

- [`.claude/skills/SKILLS_FRAMEWORK.md`](../../.claude/skills/SKILLS_FRAMEWORK.md) v2 — the layout spec this ADR enforces.
- [`docs/sessions/20260519_doctrine_artifact_buildout.md`](../sessions/20260519_doctrine_artifact_buildout.md) — Wave 2 refactor that surfaced the need for this decision.
- [`docs/reviews/20260519_pass4_doctrine_audit.md`](../reviews/20260519_pass4_doctrine_audit.md) — code-reviewer flagged ADR-0001 as overdue.
- [`docs/reviews/20260519_pass4_enforcement_grill.md`](../reviews/20260519_pass4_enforcement_grill.md) — proposer flagged ADR-0001 as the strongest candidate.
- [`.claude/skills/shift-left-testing/ENFORCEMENT.md`](../../.claude/skills/shift-left-testing/ENFORCEMENT.md) — first sidecar authored under this ADR's rule.
- Anthropic, Skills Open Standard (December 2025) — directory form with frontmatter.
- Matt Pocock, [`mattpocock/skills`](https://github.com/mattpocock/skills) — the prior-art that established directory-form as production-tested.
