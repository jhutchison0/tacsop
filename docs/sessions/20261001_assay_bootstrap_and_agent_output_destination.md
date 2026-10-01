# Session: A New Project Leaves the Hub, and an Agent Writes to the Wrong Repo

**Date**: 2026-10-01
**Branch**: main
**Tags**: #session #doctrine #infra #propagation #complete

**Documents**: [docs/tasks.md](../tasks.md), [config/project.yaml](../../config/project.yaml)
**References**: [.claude/README.md](../../.claude/README.md), [docs/design/pillars.md](../design/pillars.md), [using-topic-branches/SKILL.md](../../.claude/skills/using-topic-branches/SKILL.md), [traversing-the-knowledge-base/SKILL.md](../../.claude/skills/traversing-the-knowledge-base/SKILL.md); the new `assay` repository, whose own session record is the primary account of the work
**Follows**: [20260930_overwatch_claim_checks_and_data_loss_guards.md](20260930_overwatch_claim_checks_and_data_loss_guards.md)

---

## Summary

The hub cloned itself into a new project and found a defect in how it deploys agents.

Most of the work belongs to the new repository and is written up there. What belongs
here is one lesson and one merge. Three agents were pointed at a plan staged in `/tmp`
and told to write their reports into this repository, which is public. They did as
asked. The reports arrived carrying an internal hostname, a colleague's username
seventeen times, an internal project codename and another repository's name, none of
which appears anywhere at `HEAD`.

Nothing was committed and nothing was pushed. The reports moved to the internal
repository that owns them. But the near-miss was luck plus one agent's own care, not a
control, and the hub is where the control belongs.

## Findings

**An agent's output destination belongs to the repository that owns the sensitivity, not
the working directory the agent runs in.** The lead staged another project's plan into
`/tmp` so three agents could read it without permission prompts, then wrote the output
paths as `docs/reviews/` and `docs/plans/` without thinking about whose `docs/` that was.
The agent definitions are scoped to this repo's paths, the scope matrix in
`.claude/README.md` says `code-reviewer` writes to `docs/reviews/`, and every one of
those statements is correct and none of them is about publicness. The gap is between
"which paths may this agent write" and "which repository is this material allowed to
land in".

**`code-reviewer` caught its own half and said so.** It sanitized the internal names out
of its first draft before reporting, and added a handling note explaining the
substitutions. It also flagged that the sibling report, written by a different agent,
still carried one, and declined to edit another agent's output. That is the behaviour the
adversarial-by-design principle is supposed to produce, and it is the only reason the gap
was visible rather than discovered later by `git add -A`. Worth noting that this repo's
own task list already carries a swept `git add` among the OVERWATCH incidents.

**Three agents reviewing a plan before any code was written found ten defects in it**,
two of which would have been expensive: a raw object-path grammar that would have
silently destroyed 49 of 79 archive files, and a least-squares rate fit whose design
matrix has rank 10 against 22 columns and which returns negative prices while reproducing
every billed day within 1.14%. Both were caught by re-deriving the agents' claims rather
than accepting them, which is the practice OVERWATCH exists to install. The review-first
deployment is worth repeating; the finding rate per agent-hour was higher than any
review-after-code pass this fleet has run.

**The template clone worked, with three deviations worth recording.** The standing memory
about not stripping `.claude/commands/` or `.claude/skills/` held and was followed. The
`myproject` to package-name substitution in the audit hook was verified live against a
nested path rather than assumed, and the hook fired. Two modules the proposer wanted
dropped were kept for reasons specific to the new domain, and one it wanted kept was
dropped.

## Claims

| Claim | State | Evidence |
|---|---|---|
| No internal hostname, colleague username, codename, or sibling repo name reached this public repo, at `HEAD` or in the working tree | observed | `for s in dis.anl.gov KEIRA ai-budget-tracker dgolden titanx.dis; do git grep -lI "$s" HEAD \| wc -l; grep -rlI "$s" . --exclude-dir=.git \| wc -l; done` → `0` for all ten checks, at `e7cf1ae` |
| This repo's suite passes after merging the 29 commits from the other box | tested | `.venv/bin/pytest -q` → `432 passed, 1 warning in 7.71s` |
| The `docs/tasks.md` merge kept one Active entry per CONOP and lost neither of this box's two findings | tested | `grep -c` on four keys → OVERWATCH 1 Active (second hit is in Completed), WHETSTONE 1 Active, audit-hook blind spot 1, sibling-path class 1 |
| The new repository is bootstrapped, tested and pushed | deployed | `git status -sb` → `## main...origin/main` with no divergence; `.venv/bin/pytest -q` → `137 passed` |
| The frozen raw archive is intact | observed | `sha256sum -c MANIFEST.sha256` → 0 non-OK lines over 102 files |
| The audit hook fires on a path nested inside a subpackage | tested | hook invoked with a `PostToolUse` payload for `src/<pkg>/adapters/_hookprobe.py` → logged `MISSING_TEST` |
| The reviewed plan contains ten defects, two of them expensive | tested | each load-bearing agent claim re-derived by the lead against the frozen snapshot before being acted on; counts and arithmetic in the new repo's review directory |

Overclaims the user caught this session: 1

Overclaims a reviewer caught this session: 0

The one the user caught was not a number. The lead proposed harvesting a colleague's
existing adapters and treated it as the likely answer; the proposer refuted it with two
specifics the lead did not have. Separately, the lead wrote "403 tests pass" into a commit
message in the new repository when that repo has 137, and amended before pushing. That one
was self-caught and is recorded here rather than in the counts.

## Key Decisions

| Decision | Rationale |
|---|---|
| Build the new project in its own repository, cloned from this template | It is a real project, not hub work. The hub stays a template |
| Keep `decision-scientist` in the clone, re-scoped from MAUT to estimation | It found the rank-10 design matrix. The agent is more portable than its original framing suggested |
| File the agent-output-destination rule as a task, not a staged doctrine entry | `docs/tasks.md` records a release hold: no OVERWATCH entry propagates until tasks 1e and 2d are done, then all in one cycle. Staging an unrelated entry now would collide with that hold |

## Next Steps

1. Decide where the agent-output-destination rule lives: the scope matrix in
   `.claude/README.md`, the agent definitions themselves, or a `/pcc` check that refuses
   to stage a file carrying strings absent from `HEAD`. The third is the only
   deterministic one.
2. Release the held OVERWATCH entries once 1e and 2d land, and consider whether this
   lesson rides with them or waits for its own cycle.
3. Everything else in this session continues in the new repository.
