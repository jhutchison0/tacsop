# Session: OVERWATCH, Claim Checks and Data-Loss Guards

**Date**: 2026-09-30 to 2026-10-01
**Branch**: main; topic branches `topic/overwatch-sealed-tests`, `topic/overwatch-template-docs`, `topic/doctrine-transport-backlog` (all merged and deleted)
**Tags**: #session #doctrine #overwatch #testing #propagation #review #infra
**Documents**: [conop_overwatch_claim_verification_and_irreversible_guards.md](../plans/conop_overwatch_claim_verification_and_irreversible_guards.md), [ISOLATION.md](../../.claude/skills/shift-left-testing/ISOLATION.md), [propagation-protocol.md](../propagation-protocol.md), [session-start.md](../../.claude/commands/session-start.md), [task.md](../../.claude/commands/task.md), [docs/tasks.md](../tasks.md)
**Implements**: [conop_overwatch_claim_verification_and_irreversible_guards.md](../plans/conop_overwatch_claim_verification_and_irreversible_guards.md) (Wave 1 tasks 1a to 1d; the transport fix that gates its release)
**References**: [20260930_overwatch_review.md](../reviews/20260930_overwatch_review.md), [20260930_overwatch_proposer.md](../reviews/20260930_overwatch_proposer.md), [20260930_overwatch_1a_gate.md](../reviews/20260930_overwatch_1a_gate.md), [20261001_overwatch_1b_1d_review.md](../reviews/20261001_overwatch_1b_1d_review.md), [20261001_doctrine_transport_gate.md](../reviews/20261001_doctrine_transport_gate.md), [ENFORCEMENT.md](../../.claude/skills/shift-left-testing/ENFORCEMENT.md), [20260519_pass4_enforcement_maut.md](../reviews/20260519_pass4_enforcement_maut.md); `code.claude.com/docs/en/permissions` (read 2026-09-30)
**Follows**: [20260829_machine_identity_and_lake_conventions.md](20260829_machine_identity_and_lake_conventions.md) (no session docs exist for the 2026-08-30, 09-10, and 09-18 work committed in between)

---

## Summary

A Claude Code Insights report from the work terminal (22 sessions, 2026-08-04 to 09-28) named two failure classes hub doctrine did not cover: success claimed without proof (at least 6 sessions), and operations that reach past their scope (a test fixture that deleted about 138 GB of real cache, a directory-wide `git add`, an install into another repo's venv). The session turned the report and a second agent's recommendation into CONOP OVERWATCH, approved it after a blind two-reviewer debate, and shipped Wave 1's first four tasks into the template: a test tripwire, pinned install targets, session-start tool checks, and a Purpose column on task specs.

Releasing that work exposed an older defect. The propagation script shipped only the newest doctrine entry, so three entries sat unsent. The lead chose a consumer-side delivery mark; its first design (a date) failed its gate on two Criticals, and the rebuilt design (a set of entry headings) passed on the third round and merged. Nothing has propagated downstream.

The plan's thesis was tested on its own author. Every review round caught at least one claim of the lead's that its own runs had not, starting with five overstatements in the plan that is meant to stop overstatement.

| Metric | Value |
|---|---|
| Tests on `main`, start of session | 308 |
| Tests on `main`, end of session | 403 |
| Commits | 24 on `main` (including 3 merges) |
| Review agent runs | 13 (proposer 1; code-reviewer 10, counting resumed rounds; test-runner 2) |
| Subagent tokens, summed as reported per run | about 2.3M (resumed runs may count earlier context again) |
| Lead claims refuted by a reviewer's re-run | 19 (5 in the CONOP draft, 14 later; listed in Appendix A) |
| Lead errors caught by the lead's own re-run before commit | 9 (Appendix A) |
| PCC check 5, last run | 0 MISSING over 30 paths; 0 MISSING-DIR |
| Downstream repos written to | 0 |

## Work Completed

`KB-graph: walked ENFORCEMENT.md to its MAUT and to CONOP-FORMAT.md before drafting → found the Layer 6 re-evaluation rule is scoped to test-first, not to irreversible operations; the lead's first answer to the user said otherwise and was corrected in the same session`

`KB-graph: read docs/propagation-protocol.md Rules 1 to 4 before drafting a release entry → found that "one entry for 1a to 1d, 1c marked breaking" (written twice into the plan) violated Rules 2 and 4 and that the transport shipped only entries[0]; release shape reopened and the transport P1 pulled forward`

### 1. The plan (CONOP OVERWATCH, approved 2026-09-30)

The second agent's eight load-bearing claims were re-run before drafting; all eight held, including that the report's sample hook blocks `rm -rf /tmp/x` and lets `rm -fr /data/x` and pytest through. `tacsop` was confirmed public, so the incidents are written as failure shapes and the source texts live in the gitignored `docs/design/hold/`. Proposer and code-reviewer debated the draft blind to each other: code-reviewer re-ran 29 Situation claims and refuted 5; proposer cut the design (settings `ask` rules over a hook script, one audit hook over patched APIs, a `## Claims` ledger). The lead's decisions: `ask` rules, four claim states plus a freshness rule, start Wave 1 the same session.

### 2. Task 1a: the test tripwire (`tests/isolation.py`, merged `d03e66a`)

One Python audit hook, armed during each test's setup, call, and teardown, raises `IsolationError` on deletion outside the allowlist (including `rmtree` bound at import, `posix_spawn`, a launched `rm`), on non-loopback network and DNS, and stops `load_dotenv()` from reading the real `.env`. Registered through `addopts = ["-p", "tests.isolation"]`, because pytest runs a whole conftest before it reads `pytest_plugins`. `ISOLATION.md` documents the design (pass data roots in), adoption, and the limits. Three gate rounds: 3 Critical and 9 Warning, then 0 and 4 (two were regressions from round-1 fixes), then GO with 27 of 30 mutants killed. 43 tests; 0 catches across the hub's 308 existing tests, with and without `CI=true`.

### 3. Tasks 1b to 1d (merged `d98428a`)

- **1b**: every `uv pip` command in the template names its target (`--python .venv`); the routes through `VIRTUAL_ENV=` and activation are gone. Re-run: with a stray `VIRTUAL_ENV`, a bare install lands in the other repo's venv (uv 0.12.1).
- **1c**: `/session-start` Step 4 runs `.venv/bin/pytest` and prints one line per gap: git identity, a stray `VIRTUAL_ENV`, `gh` or `glab` auth. Pinned afterward by 9 tests (`2a2e725`) that fail 9 of 9 against the original block and fail exactly one against the pre-`CDPATH` block.
- **1d**: task specs read Task, Purpose, Condition, Standard.

One review pass (0 Critical, 7 Warning, two of them the lead's overclaims), fixes, then a probe re-run: GO.

### 4. The transport fix (merged `d602c8e`)

`propagate_doctrine.py` now sends each repo every entry its delivery mark (`.claude/doctrine-delivered`) does not hold. The first design stored a date; the gate showed a same-day entry never ships (C1) and the mark could move backward or close the backlog on a `--since` typo (C2). The rebuild stores the set of entry headings offered, unioned on every run and never shrunk; malformed marks, undated or repeated headings, and unclosed fences refuse rather than guess; one failing repo no longer stops the run. Three gate rounds: 2 Critical and 7 Warning, then 0 and 3, then GO. 57 propagation tests. The real dry run with `--since 2026-08-21` would send 5 entries to each of 19 repos and write 0 marks; the gate measured 20 of those 95 deliveries as redundant for five repos, which the protocol now handles with hand-seeded marks.

## Key Decisions

| Decision | Chosen | Over | Why |
|---|---|---|---|
| Guard form for irreversible commands | Settings `ask` rules | A bash PreToolUse hook | Docs confirm ask outranks the blanket `Bash` allow and prompts in auto mode; no parsing code to ship fleet-wide |
| Claim taxonomy | Four states plus freshness | Proposer's three | The worst incident is deployed reported as observed |
| Test tripwire | One audit hook | Monkeypatched APIs | A patch misses `from shutil import rmtree`, the incident's own shape |
| Arming collection | No | Reviewer's W3 | Collection imports libraries that build caches; armed, a fresh matplotlib cache stopped the suite |
| Merge granularity | Merge each gated unit; release as separate entries | One branch until the plan completes | Branch lifetime is one session; half the plan needs the work terminal; Rules 2 and 4 decide the release shape |
| Delivery record | Heading-set mark in each consumer | Date mark; hub ledger; consumer-written ack | Identity, not order: same-day and backdated entries ship, an older checkout cannot regress it |

## Pillar Compliance

- **Shift-Left Testing**: every code slice had a failing test first, with stated exceptions. Three pin tests passed on first run because they pinned behavior an earlier slice built (tripwire disarm, setup and teardown arming, two `/proc`-masked branches); each is labeled as a pin. The 1b pinning pass was mechanical, verified by grep and a repro rather than tests. Two round-2 fixes in 1a were doc-only, and the commit called them test-first (corrected in the CONOP Status Log).
- **Simplicity First**: the tripwire grew from 164 to 224 lines across three gate rounds, each addition driven by a probe that deleted real data or tripped falsely. The transport redesign replaced a date with a set, which removed date logic rather than adding it. Library special cases stayed out of the plugin (matplotlib is documented, not coded).
- **Config-Driven**: the tripwire's extra allowlist is a pytest ini option in `pyproject.toml`, not `config/project.yaml`; pytest reads its own configuration, and nothing here is a decision model.
- **Branching**: tasks 1b to 1d shared one branch against the plan's one-per-task rule, by the lead's choice. Within the hour, 1c's new line broke 1b's acceptance grep and only the review saw it. Logged in the Status Log.

## Lessons

1. **An independent re-run is the control that worked.** The lead's own runs never set `CI=true`, never checked an exit status, and certified two greps after editing a line that broke one. Every one was caught by an agent that re-ran the claim instead of reading it.
2. **A mechanical edit changes the meaning of prose that mentions the thing edited.** The `--python` pass inverted two sentences about bare commands.
3. **A reviewer acted outside its scope.** While probing, a code-reviewer ran `uv cache clean six` on the real uv cache, disclosed it, and restored it. Review prompts now carry a write-scope rule; no planned `ask` rule covers cache commands.
4. **Order is not identity.** A date mark lost same-day and backdated entries; a set of headings does not.
5. **Bundling hides cross-task breakage.** One branch for three tasks let one task break another's acceptance check unseen.

## Next Steps

1. Seed marks for fist, schelling-point, stx-server, propter, and beesly-equilibrium (the lead's go), then draft four OVERWATCH entries (1a; 1b; 1c alone as breaking; 1d), pre-flight, dry run, and propagate the backlog in one cycle on the lead's go. The cycle also carries the 08-27 Figure Style entry, which has awaited the lead's go since August.
2. On the work terminal: Wave 0 (A3 `ask` rules in that terminal's mode, with its `glab` version; A1 claim-detector spike; A4 command replay), then task 1e.
3. Wave 2: the `verifying-claims` kernel and its controlled replay.
4. Filed this session: in-code install hints (P2, test-first), bare `pytest` outside Step 4 (P3), the audit hook's `src/`-only watch (folded into the P1 hook task).
5. WHETSTONE: this session is another candidate for the Wave 1 window, whose count is still unresolved (P1).

## Commits

| Commit | Change |
|---|---|
| `d4ac4e4` | 2026-09-18 entry: `uv venv --clear` (shift-left-testing 2.1.1) |
| `17db809` | CONOP OVERWATCH approved, with both debate reviews |
| `6039e14`, `28e8482`, `393d640`, `5e7bcac` | Task 1a tripwire and its three gate rounds |
| `d03e66a` | Merge task 1a |
| `7428d33`, `d7c640f`, `9f1eada`, `c0325ee`, `f7d917b`, `fee1601` | Tasks 1b to 1d and their review fixes |
| `d98428a` | Merge tasks 1b to 1d |
| `3e8b59d` | Release shape reopened (Rules 2 and 4) |
| `2a2e725` | Tests pinning the session-start tool checks |
| `539ba3a` | This session doc, task list, and project state |
| `c2eb3f2`, `9f0af02`, `f268c51`, `3da00c9` | Transport fix and its three gate rounds |
| `d602c8e` | Merge the transport fix |

## Appendix A: The Lead's Claims and Errors, by Who Caught Them

Recounted from the review reports at session end. A first draft of this doc said 14 refuted claims; the first recount said 18 and missed number 14 below.

**Refuted by a reviewer's re-run after the CONOP draft (14)**

| # | Claim | Where | Caught by |
|---|---|---|---|
| 1 | A `pytest_plugins` line "above any import" guards the dotenv patch | ISOLATION.md | 1a gate C2 |
| 2 | An `rmtree` with `dir_fd` "is checked at its top directory" | ISOLATION.md | 1a gate W2 |
| 3 | The allowlist's temp dir "holds `tmp_path`" (false under `--basetemp`) | ISOLATION.md | 1a gate W6 |
| 4 | "Each fixed test-first" (two were doc-only) | `393d640` | 1a gate R3-S3 |
| 5 | A stranded matplotlib lock makes the next rebuild "stop" | ISOLATION.md | 1a gate R3-S1 |
| 6 | "Every matplotlib upgrade" refreshes the cache | ISOLATION.md | 1a gate R3-S1 |
| 7 | "Both Standard greps print nothing" | `7428d33` | 1b-1d W2 |
| 8 | The `VIRTUAL_ENV=` prefix form "outlives the command" | SETUP.md | 1b-1d W6 |
| 9 | Issue 5's cause and its "works from anywhere" | TROUBLESHOOTING.md | 1b-1d W4 |
| 10 | "Three more stacked up behind it" | propagation-protocol.md | transport W6 |
| 11 | The script "sends each repo every entry it has not been sent" | propagation-protocol.md | transport W6 |
| 12 | The mark is "the hub's newest date" (the script wrote the top entry's) | protocol and docstring | transport W6, S2 |
| 13 | Same-day entries "both go or both wait" | propagation-protocol.md | transport C1 |
| 14 | The newest-only default "is right for a repo bootstrapped from the template" | protocol and docstring | transport W1, round 2 W3 |

The 5 in the CONOP draft are in its Status Log. Separately, `test-runner` found the `CI=true` failure that the lead's runs had missed.

**Caught by the lead's own re-run before commit (9)**

1. The network tests wrote their deliberate catches to the real tripwire log.
2. "uv prints its target whenever `VIRTUAL_ENV` is set" (it prints only when the target is not the cwd's `.venv`).
3. The mechanical `--python` pass inverted two sentences about bare commands.
4. A lint check printed "no new em dashes" whether or not it found any.
5. "The hub's CI" sets `CI=true` (the hub has no workflow).
6. "One entry for 1a to 1d, 1c marked breaking" (breaks propagation Rules 2 and 4).
7. The first fence-aware parser treated a fenced copy of a real heading as a heading.
8. This doc's first draft said 14 refuted claims; the recount above is 19.
9. This doc's first draft said the tripwire grew "from about 100 to about 240 lines"; `git show` says 164 to 224.

