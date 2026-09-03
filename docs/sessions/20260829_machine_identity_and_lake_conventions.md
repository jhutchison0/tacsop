# Session: Machine Identity, and a Skill That Was Already Written

**Date**: 2026-08-29
**Branch**: main
**Tags**: #session #doctrine #whetstone #propagation #infra #config #complete

**Documents**: [docs/tasks.md](../tasks.md), [config/project.yaml](../../config/project.yaml), [CONTEXT.md](../../CONTEXT.md), [.claude/commands/session-start.md](../../.claude/commands/session-start.md), [.claude/skills/SKILLS_FRAMEWORK.md](../../.claude/skills/SKILLS_FRAMEWORK.md)
**Implements**: [conop_whetstone_recursive_doctrine_loop.md](../plans/conop_whetstone_recursive_doctrine_loop.md) (D10 harvest, second intake and first whole-skill one; Wave 1 window session, numbering still unresolved)
**References**: [docs/doctrine-updates.md](../doctrine-updates.md) (2026-08-29 entry), [docs/propagation-protocol.md](../propagation-protocol.md), [traversing-the-knowledge-base/SKILL.md](../../.claude/skills/traversing-the-knowledge-base/SKILL.md), [20260827_stx_server_lessons_harvest.md](../reviews/20260827_stx_server_lessons_harvest.md); `launch-control` `origin/main` commit `1ea7659`, its ADR `0002-narrowed-engine-core-hook-glob`, its `lake-conventions` 1.0.0 and `upstream-lesson` channel file; the `dis-lakehouse` reference repo at `d280269`
**Follows**: [20260828_fleet_poll_and_loop_closure_audit.md](20260828_fleet_poll_and_loop_closure_audit.md)

---

## Summary

The fleet learned to name itself, and a skill came home that had been written a month ago downstream.

Three things were asked for: machines that know which box they are, a pointer from work repos to the lakehouse SOP, and a new `lake-conventions` skill. The third turned out to exist already. `launch-control` wrote `lake-conventions` 1.0.0 on 2026-07-27 and the hub never knew. That is the D10 case in its purest form: a downstream invention with no channel home, found only because someone traversed the repo by hand.

The harvested skill was good on formats and buckets and silent on everything the request actually named: environment checks, reference-repo availability, off-machine data, dev and production paths. Those lessons were in that repo too, scattered across its code and its retrospectives, paid for at full price. The generalized skill puts them in one place.

| Metric | Value |
|---|---|
| Tests, start of session | 240 |
| Tests, end of session | 270 |
| New tests, all written failing first | 30 |
| Vertical slices | 10 |
| Repos notified | 9 (2 appended, 7 new) |
| Of those, in the Part 2 audience | 8 |
| Check 5, first run against new prose | 5 MISSING over 32 paths |
| Check 5, after rewording | 0 MISSING over 27 paths, 0 MISSING-DIR |
| Machines in the roster | 2 of an unknown total |
| Days since the reference repo last moved | 7 |
| Em dashes added to running prose | 0 |

## Work Completed

`KB-graph: traversed launch-control by its typed headers and tasks.md rather than grepping for "dev" and "prod" → found lake-conventions 1.0.0 already written there, which turned the third task from build into harvest, and found the five-day production leak that became the preflight's leg-threading check`

`KB-graph: blast radius on the four skill-registration surfaces before adding lake-conventions → SKILLS_FRAMEWORK.md needs two edits, not one (the Level 0 block and the ASCII inventory tree are separate and have drifted apart before); all four edited in the same commit`

### 1. Machine identity

`config/project.yaml` gains a `machines:` block keyed by hostname. `src/myproject/utils/machine.py` reads it and is the first code in this repo to read that file at all. `/session-start` gains Step 1.5, placed before Step 4 because Step 4 is the first step whose behavior depends on where it is running.

An unlisted hostname resolves to `unknown` and never errors. The name stays truthful off-roster and a separate `known` flag carries membership, a correction made mid-implementation when the fourth slice showed the first design had thrown away the one fact an unknown box most needs to report.

Committed rather than a per-machine dotfile, deliberately. A dotfile avoids drift and would leave the fleet with no written record of its own members, which is the open problem: discovery is per-machine and no participant sees the whole. A roster in version control is the first artifact about a machine that survives that machine being switched off.

No usernames. `launch-control` committed one into its config and now needs a config edit per operator.

### 2. The preflight

`scripts/lake_preflight.py`, six checks, 24 tests. Real `main(argv)`, per the doctrine its sibling `propagate_doctrine.py` does not follow.

The leg-threading check is the reason the script exists. `launch-control` threaded `--lake-profile` through its engine and stage1 but not stage2. One process loaded production config while its siblings ran in dev. Nothing errored, and it wrote to the live `staging` bucket for five days before someone inspecting the lake noticed. The same class recurred a month later in a different driver. So the check takes the legs and names the one that misses, verified here against a synthetic three-leg chain: it names `stage2`.

Bare invocation fails rather than defaulting. In that repo, bare meant production in every entry point but one.

The environment check asserts credential presence and says so in its own output, because it opens no socket. `PREFLIGHT.md` spends more words on what each check cannot prove than on what it can, which is the honest ratio.

### 3. The skill, and the doctrine cycle

`lake-conventions` 1.0.0 in the hub: harvested, stripped of one repo's package paths and writer classes and a maintainer's email address, then extended with bucket tiers, both path grammars, the two-companion-file contract, the three mandatory S3 client settings, the two live credential namespaces, and dev/prod. Registered on all four surfaces.

The 2026-08-29 doctrine entry carries both parts. Part 1 universal, Part 2 scoped to work-remote repos and saying so. Propagated to 9 repos.

## Findings

**The May 2026 audit-hook glob defect is confirmed.** It has been a P1 guess since it was heard about second-hand. `launch-control`'s ADR `0002-narrowed-engine-core-hook-glob` documents it: all three review agents independently flagged the upstream glob, which is one level deep and so never matches a module inside a subpackage. Every consumer with subpackages got an inert hook. It went into a local ADR in May and stopped there. The task moves from re-check to fix.

**The upward channel worked and the collection step never ran.** `launch-control`'s `upstream-lesson` file has existed on its `origin/main` since 2026-08-17 and has never been harvested. This is now the second such file known and unread.

**A trap worth naming: that repo's local `HEAD` is 102 commits behind its own `origin/main`.** The channel file is absent from the working tree and present on the remote. A traversal that read only the checkout would have concluded the channel was never adopted. This is the argument for preflight check 3 in one sentence.

**A conflict this session declined to resolve.** `launch-control`'s `CONTEXT.md` and its local configuration sidecar both list profile layers as an anti-pattern that "will fail code review", while its shipped `lake_config` module implements exactly that. The anti-rule descends from this hub's own `configuration-management` skill, so the contradiction is the hub's to settle. The doctrine entry blesses no mechanism and requires only that a target be named at every entry point and that an unknown name fail closed. A new P2 tracks the ADR.

**The `configuration-management` skill describes a system nothing implements.** Its `LOADER.md` specifies a full loader with layering and profiles. Until today no code here read `config/project.yaml` at all. That skill has shipped to roughly 19 repos for three months reading like a description of practice. A new P3.

**Check 5 caught this session's own prose.** The first run after editing `tasks.md` reported 5 MISSING, all cross-repo citations and illustrative paths landing in the documented base-directory blind spot. Hand-verified, then reworded rather than extending the allowlist, because an allowlist that grows every time someone cites another repo stops being a check.

## Next Steps

1. Harvest the `launch-control` channel file from `origin/main`, not the checkout.
2. Fix the hook glob and pin it with a test that audits a nested path.
3. Settle the Wave 1 session count. Still unresolved, and this session adds another window candidate.
4. Add the remaining machines to the roster on the next visit to each box.
