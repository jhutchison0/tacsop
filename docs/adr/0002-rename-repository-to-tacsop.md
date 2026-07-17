# ADR-0002: Rename Repository from `utils` to `tacsop`

**Status**: Accepted
**Date**: 2026-07-17
**Decision-maker(s)**: jhutchison (lead)

---

## Triple-Filter Check

- [x] **Hard to reverse** — once the repo is shared and colleagues, talks, and downstream repos reference the name, a second rename compounds confusion. Downstream copies of `adopt_doctrine.py` hardcode the upstream path; every rename orphans them again. GitHub's redirect softens the mechanics but not the human cost.
- [x] **Surprising without context** — a future reader will ask "why is a Python project template named TACSOP?" The answer requires knowing the repo's second identity as a doctrine hub, which the old name never advertised.
- [x] **Result of a real trade-off** — four candidates were genuinely considered (`goldbook`, `sandtable`, `guidon`, `tacsop`); two were deliberately *parked* for future artifacts rather than rejected outright.

All three filter conditions pass. ADR is warranted.

---

## Context

This repo began as a personal grab-bag of Python utilities — `utils` was accurate. It has since grown a second, now-primary identity: the **upstream doctrine hub** for a family of downstream repos. It carries the agent framework, team templates, the task-escalation ladder (Task → TCS → CONOP → OPORD), the skills framework, the shift-left enforcement layer, and the propagation machinery (`propagate_doctrine.py` / `adopt_doctrine.py`) that pushes conventions to 10+ consumer repos.

The repo is about to be shared with colleagues. `utils` misdescribes the repo to a first-time reader (it suggests a utility library, which is now the minority of its value), collides with one of the most generic words in software, and is nearly un-searchable. The name should state the primary function: **the doctrinal foundation for agents and teams to operate together, and for task escalation.**

The repo's vocabulary is already deliberately military (doctrine, CONOP, OPORD, TCS, waves, SITREP, prowords), so candidates were drawn from the same register.

---

## Decision

Rename the GitHub repository `jhutchison0/utils` → **`jhutchison0/tacsop`**.

**TACSOP** — *Tactical Standing Operating Procedure* — is the document through which a headquarters publishes the standing procedures by which its units operate, and from which subordinate units derive their own local SOPs. That is structurally what this repo does: downstream repos copy the doctrine bundle and adapt it to their local context (package-name substitution in hooks, per-repo settings merges). The name is a term of art, not an allusion.

Scope boundaries, decided deliberately:

- **Repo identity only.** The `myproject` package placeholder (`src/myproject/`, `config/project.yaml` `name:`, the hook's package glob) is template content that downstream adopters substitute — it stays.
- **Historical documents are untouched.** `docs/sessions/`, `docs/reviews/`, and prior `doctrine-updates.md` entries keep the old name and old URLs; GitHub's rename redirect keeps those links live.
- **The name `utils` is never reused** under this account. Creating a new repo with that name would break every historical redirect at once.
- Living documents (README, CONTEXT.md, LANGUAGE.md, propagation-protocol.md, CLAUDE.md) and the two propagation scripts are updated; the rename is announced downstream via a `doctrine-updates.md` entry propagated through the system itself.

---

## Alternatives Considered

### Alternative A: `goldbook`

Homage to the 101st Airborne's Gold Book — the division's standards publication, and a personal touchstone (a copy sits on the decision-maker's desk as a reminder of standards put into excellent practice). Rejected: it honors the inspiration rather than describing the function, and it is unit-specific — the reference lands only for readers who know the 101st. The emotional pull was real, which is exactly why function had to win.

### Alternative B: `sandtable` (parked, not rejected)

A sand table is a rehearsal and wargaming exercise. Appealing image, but it names *planning rehearsal*, not *standing procedure*. Deliberately parked: a future command that generates CONOPs through structured rehearsal may be built around this name, where the metaphor actually holds. Spending it on the repo would forfeit that.

### Alternative C: `guidon` (parked, not rejected)

The genuine runner-up. A guidon is the pennant marking a company's identity and rallying point — evocative of downstream repos aligning on an upstream standard, a real English word, warmer than an acronym. Rejected for the repo because the metaphor breaks at the repo's distinguishing feature: a guidon names the *relationship* (rally to the standard), not the *content*, and guidons are singular — nobody copies a guidon, whereas this repo's entire mechanism is that its contents are copied and locally adapted. Parked for a possible future artifact where singularity is the point — e.g., a registry of downstream repos and their adoption status (the formation that follows the standard).

### Alternative D: `tacsop` (selected)

Function-accurate (see Decision), consistent with the repo's established vocabulary, and a rare token — unique on GitHub, unambiguously greppable, no namesake noise. Its one real cost: opaque to readers without a military background. Accepted deliberately; the README's first line carries a civilian gloss, and for a repo whose thesis is "standards, written down, enforced, and propagated," the acronym-shaped name *is* the brand.

---

## Consequences

### Positive

- The name states the repo's primary function to the audience it is about to meet.
- Announcing the rename via `doctrine-updates.md` and `propagate_doctrine.py` makes the rename a live demonstration of the propagation architecture — every downstream repo learns the new name at its next `/session-start` through the system itself.
- `tacsop` is uniquely greppable across machines, docs, and conversations in a way `utils` never was.
- Two strong names (`sandtable`, `guidon`) remain available for future artifacts whose metaphors they actually fit.

### Negative

- Opaque to non-military readers; requires the README gloss to decode. This cost is permanent.
- Rename tax on every machine with a clone: `git remote set-url`, local directory rename, and migration of the Claude Code per-project state directory (`~/.claude/projects/<path-slug>/`), which is keyed by absolute path and would otherwise orphan agent memory and session history.
- Downstream copies of `adopt_doctrine.py` hardcode `~/projects/github/utils` as the default upstream; until they re-copy the patched script (or pass `--upstream`), a fresh adoption run on those machines fails path discovery. The announcement entry must carry PATCH-COPY guidance.
- Historical links depend on GitHub's redirect, which survives only as long as the old name is never reused.

### Neutral

- The `myproject` placeholder and all template-substitution semantics are unchanged; downstream adopters see no behavioral difference in the bundle itself.
- `LANGUAGE.md` gains **TACSOP** as a glossary term; the **Doctrine** definition is reworded to reference the new name.
- `propagate_doctrine.py`'s `UTILS_ROOT` module attribute is renamed (`TACSOP_ROOT`), with the monkeypatched references in `tests/unit/test_propagate_doctrine.py` updated in lockstep.

---

## References

- [ADR-0001: Directory Form Mandatory for All New Skills](0001-directory-form-mandatory-for-new-skills.md) — first ADR under this format; this one exercises the "parked, not rejected" distinction.
- [`docs/propagation-protocol.md`](../propagation-protocol.md) — the propagation mechanism the rename announcement travels through.
- [`scripts/propagate_doctrine.py`](../../scripts/propagate_doctrine.py), [`scripts/adopt_doctrine.py`](../../scripts/adopt_doctrine.py) — the two code locations affected.
- [`CONTEXT.md`](../../CONTEXT.md) — the dual-identity (template + doctrine hub) statement that motivates the new name.
- `docs/doctrine-updates.md` — 2026-07-17 entry announces the rename downstream.
