# Session: agent-eval Catches Up, GitHub Becomes the Source, and CONOP DISPATCH

**Date**: 2026-10-06 (on Nidhogg)
**Branch**: main
**Tags**: #session #doctrine #propagation #docs #complete
**Documents**: [docs/tasks.md](../tasks.md), [docs/gaps.md](../gaps.md), [docs/doctrine-updates.md](../doctrine-updates.md), [src/myproject/utils/gaps.py](../../src/myproject/utils/gaps.py), [.claude/hooks/post-tool-shift-left-audit.sh](../../.claude/hooks/post-tool-shift-left-audit.sh)
**Implements**: [docs/propagation-protocol.md](../propagation-protocol.md) (Cycle Anatomy, one live cycle); the Focus of 2026-10-05, steps 1 and 2
**References**: [20261005_overwatch_traversal_and_sextant.md](20261005_overwatch_traversal_and_sextant.md), [conop_sextant_doctrine_evaluation_repository.md](../plans/conop_sextant_doctrine_evaluation_repository.md) (D1), `assay`'s session doc of 2026-10-05 (read through its mirror), agent-eval's `docs/sessions/20261006_doctrine_catchup_and_conop_dispatch.md`, `docs/plans/20261006_conop_DISPATCH_cost_aware_evaluation.md` and `docs/reviews/20261006_doctrine_catchup_gate.md`
**Follows**: [20261005_overwatch_traversal_and_sextant.md](20261005_overwatch_traversal_and_sextant.md)

---

## Summary

The user went off-script: update agent-eval with the hub's doctrine, note that GitHub is the source now because the work GitLab will not supply updates to many projects anymore, and then think about how agent-eval becomes significantly meaningful in FY27 given assay's progress, with the hypothesis that it should recommend tasks to harnesses rather than route everything through Claude Code under a constrained token budget.

Three things happened in order. The hub read `assay`'s six lessons back through its mirror, fixed two in the gap checker test-first, wrote two into the unsent entries, and ran the 2026-10-06 cycle to 20 repos with `assay` skipped. agent-eval was merged with GitHub (ahead 2, behind 6), given a uv venv here, and brought through eight doctrine entries on a topic branch with a blind gate (GO-WITH-FIXES); its register opened with six gaps, and every one of them is about cost, contamination, or reach. The FY27 question became CONOP DISPATCH there, In Debate: `RunRecord` records no tokens and assay records no controlled effectiveness, so each repo holds half of a cost-effectiveness ratio, and the plan builds the cost-instrumented matrix first and runs three falsifiers before any recommender. Two defects came back upstream and are fixed here: the audit hook's import grep never fired in a repo whose tests import with the `src.` prefix, and the machine test's fixture carried a real host.

| Metric | Value |
|---|---|
| Hub tests, start / end | 540 / 545 |
| agent-eval tests, `main` before / after | 343 / 414 |
| Propagation cycle | 2 entries to 20 repos (15 appended, 5 new), 1 skipped (`assay`), 0 warnings |
| Doctrine entries adopted at agent-eval / skipped / previously adopted | 8 / 2 / 2 |
| Gate review at agent-eval | GO-WITH-FIXES: 0 Critical, 7 Warning, 12 Suggestion; 20 mutations, 15 caught |
| Hub commits this session, before this doc | 6 |
| agent-eval commits, including two merges | 9 |

---

## Work Completed

### 1. assay's lessons, read back

`KB-graph: outbound from assay's 2026-10-05 session doc, "What goes back to the hub" (six items), read via git show on the mirror's origin/main → two fixes in gaps.py, two sentences in the unsent entries, two tasks`

Item 1 (a delivery note prescribed `parents[2]` for a package that was not flat) and item 5 (an archive-only `known_issues` key, pinned by a test) went into rows 3 and 4 of the 2026-10-04 entries before they shipped. Items 2 and 3 went into `src/myproject/utils/gaps.py` test-first: `FILLERS` gains "nothing exists", and two rows under one id are reported, since a supersession pointer at that id would be ambiguous. Items 4 (a bare file pointer is satisfied by the file existing) and 6 (score a battery on the failure count; never build the scratch with `git archive`) are tasks. The read-back task is closed. Nothing quoted carries a private term, and nothing was written into the mirror.

### 2. The cycle

Dry run: 20 repos, `[skip] github/assay`, no `[warn]`. Live run the same. The five "new" repos (no unread notification) were `dnd-minis`, `daily_weather`, `fist`, `schelling-point`, `stx-server`; the other 15 appended. The consumption records are protocol step 6's job before the next cycle; two exist already (`assay` 2026-10-05, agent-eval 2026-10-06).

### 3. agent-eval

The clone's local commits were from 2026-06-28 under the GitHub identity; the six it lacked were from 2026-07-24 under the work identity, pushed from the work terminal: the tacsop alignment, the model matrix, an aider fix, and proxy-gateway stubs. One add/add conflict, the topic-branches skill with and without the em-dash sweep; origin's taken. Argo does not connect from Nidhogg, so the personal machine plans and reviews and the work terminal runs evaluations; that fact is now in agent-eval's CONTEXT.md and CLAUDE.md.

The adoption copied each Level 0 artifact from the commit its entry names (`git archive <commit> <path>`), because the hub's HEAD carries the held OVERWATCH release: `shift-left-testing` 2.1.1 from `d4ac4e4`, the figure skill and the writing skill 1.0.1 and the em-dash-swept format docs from `8797561`, `python-venv-management` 3.0.0 from `0965785`, the picture skill and `maintaining-project-context` 1.1.0 from HEAD. The gate verified every copy byte-identical to its commit. Skipped with reasons: 08-29 Part 2 (remote is `github.com`) and 08-30 (no personal scope); 03-26 stays skipped from July, with DISPATCH D8 naming the reversal condition.

The picture there: `src/ops/gaps.py` and `machine.py` (a new package, `parents[2]`), six gap rows, the state block and `known_issues` out of the config with each of seven entries given one home, the Focus at the head of `docs/work.md`, `/session-start` reading by name with tagged lines, and `tests/unit/test_state_block.py` adapted to `docs/work.md`. One local departure, which the gate judged equivalent on the key: the `known_issues` pin walks the parsed YAML for the key instead of matching the substring, because a closed `update_log` line there names the key's removal and a record is never rewritten.

### 4. CONOP DISPATCH

`proposer` was briefed blind with the facts of the day and returned SHIP-WITH-FIXES: the direction is right, the mechanism unproven, because the 13 tasks were designed to teach, not to sample work. Four approaches: A, the cost-instrumented matrix with a frontier table; B, the recommender, MAUT over pass rate, cost per pass, time and variance; C, agent-eval as assay's controlled-effectiveness arm, emitting rows in assay's shape and reading its rate card as a file; D, observed-first, replay tasks written only for the classes that dominate spend. The plan builds A shaped for C and lets two falsifiers decide B and D: five replicates on two cells (does the benchmark carry a routing signal), and a demand-concentration test on assay's records (does real work label). The boundary follows SEXTANT D1: agent-eval owns a run's score and tokens; assay owns the rate card, dollars and the observed task mix; dependency runs one way; nothing keyed by a person crosses. After the gate, Wave 1 is two tasks with no code (reconcile the work clone; run the smoke and read its output for usage counts), and the owner rules on nine open decisions.

### 5. The gate, and what came upstream

`code-reviewer` ran blind in a worktree, scoring 20 mutations on the failure count against the worktree's own baseline, as assay's lesson 6 prescribes; 15 were caught. Of the seven warnings, two are hub defects: the hook's fallback grep looked for `from <pkg>.<module> import` while every test in a template-layout repo writes `from src.<pkg>.<module> import`, so it had never fired; and `test_machine.py`'s fixture carried a real roster host and the lakehouse path, which a TEMPLATE-COPY carried downstream. Both fixed here, test-first, the hook in its own `[gate]` commit. The five surviving mutations are weaknesses in the hub's pins and are on the register-pin task. The reviewer also refuted a claim in a commit message (section 6).

### 6. Observations for the register

- **G7.** This session's `/session-start` summary carried a tag on all 11 lines and restated no record's count as current; the task counts and the staleness proxy were measured by command. Second observation; the window continues.
- **G8.** Retention is `3650` and stx-server's transcript of 2026-09-07 is present among 8 top-level files; the check does not discriminate until 2026-10-08.
- **G11**, opened: whether the seven consumers the roster lists by work-GitLab path still exist, and where, now that GitHub is the source.

---

## Claims

| Claim | State | Evidence |
|---|---|---|
| The hub suite passes on `e073661` plus this doc's companion edits | tested | `.venv/bin/pytest -q` → `545 passed, 1 warning in 5.12s` |
| The gap checker rejects a two-word filler and a duplicated id | tested | `.venv/bin/pytest -q tests/unit/test_gaps.py` → `31 passed` (two new cases red first: `2 failed, 29 passed`) |
| The hook's import grep matches the `src.` prefix | tested | `.venv/bin/pytest -q tests/unit/test_shift_left_hook.py` → `12 passed`, after `3 failed, 9 passed` on the red commit `9413238` |
| The cycle reached 20 repos and skipped `assay` | observed | the live run's output: 15 `Appended`, 5 `Notified`, 1 `[skip] github/assay`, exit 0; agent-eval's notification then held 12 `## 20` headings and its mark 17 lines |
| agent-eval `main` is merged, green, and on GitHub | observed | `git merge --no-ff` → `c329c11`; `.venv/bin/python -m pytest -q` there → `414 passed`; `git fetch && git status -sb` → `## main...origin/main` with no ahead or behind |
| agent-eval's topic branch is deleted locally and was never pushed | observed | `git branch -a` there lists `main`, `origin/main`, `origin/dev` only |
| Both 2026-10-04 Detect blocks print nothing at agent-eval, and its check 6 is clean | tested | the three state-block greps → no output; the rule-1 count → `0`; check 6 file pass → `0 MISSING` over 27 paths; directory pass → no output |
| No held OVERWATCH content reached agent-eval | observed | the gate's grep and version checks: `shift-left-testing` 2.1.1, no `ISOLATION.md`; the one `verifying-claims` mention is the picture skill's own Level 0 text |
| Argo is unreachable from this machine | observed | `curl -s -m 5 -o /dev/null -w '%{http_code}' https://apps.inside.anl.gov/argoapi/v1/models` → `000` |
| No private term in the hub's index or unpushed commits, nor in agent-eval's branch | observed, before this doc | check 7's block over both repos → no FAIL line; agent-eval: `0` content-hit paths over 7 unpushed commits |
| The hub's reference-integrity check is clean | tested | Correction, same session: the run before this doc's commit printed `MISSING: docs/reviews/20261006_doctrine_catchup_gate.md`, a cross-repo citation in `docs/tasks.md` that check 5 resolves against this repo (its blind spot 2); the citation was reworded in the follow-up commit and the re-run printed no `MISSING`; directory pass → no output |

Overclaims the user caught this session: 0

Overclaims a reviewer caught this session: 3

The three: a `[gate]` commit message at agent-eval claimed `0 MISSING over 28 paths` when the run at that SHA gave 18 paths and 1 MISSING (true only at HEAD); "pipe-tested on orchestrator.py" had exercised the name lookup, not the fallback it was meant to prove; and "each from the commit its entry names" held for six skills and not for the traversal skill, which came from HEAD (1.0.2, nothing held in the delta).

---

## Key Decisions

| Decision | By | Rationale |
|---|---|---|
| GitHub is the source for work-origin projects; the work GitLab will not supply updates | the user, 2026-10-06 | Stated at the start; agent-eval repointed; the roster's seven GitLab paths are G11 |
| Run the cycle today | the lead | The Focus's three conditions held: `assay` adopted, the lessons read back and the entries revised, the dry run clean |
| Copy Level 0 artifacts from named commits while a release is held | the lead | The hub's HEAD carries OVERWATCH content under hold; filed for the protocol |
| agent-eval's register pin checks the YAML key, not the substring | the lead; the gate: equivalent on the key | A closed record names the key's removal; the hub's version is on a task |
| Record the `pci.md` gate-separation exception rather than rewrite two commits | the lead | WARN-only; two example lines; the record is honest |
| DISPATCH builds the matrix before any recommender; Wave 1 costs no code | the lead, on the proposer's and the reviewer's rounds | The mechanism is unproven; the cheapest falsifier is reading a smoke run's output |

---

## Pillar Compliance

| Pillar | Status | Notes |
|---|---|---|
| **Simplicity First** | PASS | Two small hub fixes; the plan defers the recommender and the decision-science module until earned |
| **Shift-Left Testing** | PASS | `gaps.py` and the hook changed red-first here; `src/ops/` at agent-eval likewise. The hook logged nothing for files written through Bash (gap G2's shape) |
| **Config-Driven** | PASS | agent-eval's roster and `package_manager` live in its config; DISPATCH names the rate-card path by a role-named variable |

---

## Lessons

1. **A held release leaks by shape as well as by name.** The grep for held artifacts was clean; the reviewer found an `Evidence:` line and a `Purpose` column in a plan the lead wrote by hand.
2. **A pipe test proves the branch it took.** The fallback it was meant to prove had never fired in any template-layout repo, for five weeks.
3. **A test fixture travels.** A real host name in a hub fixture is a hostname in every consumer's test.
4. **The cheapest falsifier is often a read.** Whether a tool reports tokens is answered by looking at a smoke run's output, not by adding fields to capture them.
5. **A clone is not the repository.** Ahead 2 and behind 6, with the July work invisible until `git fetch`; the work clone's own state is a gap on both sides.

---

## Commits

| Hash | Subject |
|---|---|
| `0df6271` | [util] Gap checker: a two-word filler names nothing, and two rows under one id are a problem |
| `a834ffa` | [doc] The two unsent 2026-10-04 entries carry assay's layout check and the archive-only key |
| `be1462c` | [doc] Focus after the 2026-10-06 cycle; assay's lessons read back; G11 and four tasks from agent-eval's adoption |
| `9413238` | [test] The hook's import grep must match an import carrying the src. prefix |
| `d39305d` | [gate] The audit hook's import grep accepts the src. prefix |
| `e073661` | [test] The machine test's fixture uses a neutral host and path |
| this doc's commit | [doc] Session 2026-10-06, with the hook correction task |

agent-eval, on GitHub: `af81f61` (merge of origin), `f482bb6`, `c4803ee`, `c7157fa`, `be24eec`, `b0b0e3f`, `b710de2`, `72dedaf`, and the gate merge `c329c11`.

---

## Next Steps

1. The user rules on CONOP DISPATCH O1 to O9 (in agent-eval), and on G11: which of the seven GitLab-path consumers have a GitHub home.
2. SEXTANT Wave 0 by 2026-10-14; the retention check on or after 2026-10-08.
3. The two correction entries (register pin; hook prefix) drafted and batched for the next cycle, after the consumption records of this one are read.
4. On the work terminal: DISPATCH Wave 1 (reconcile the clone, two smoke runs), then the OVERWATCH and G6/G11 items in the Focus's step 3.
5. agent-eval has a standing `origin/dev` branch; audit it under the topic-branches skill at the next session there.

---

## Addendum, afternoon: the home branch and the first local evaluations

The user asked for a `home` branch on agent-eval like assay's, so today's work survives a work-side push that wipes `main`, and for Aider and OpenCode installed here so an evaluation could run today. Both done; the record is agent-eval's session 16 on its `home` branch. In brief: `home` tracks `origin/home` with a one-commit fork (`scope: personal`, a loopback gateway to a local Ollama server, two local models); Aider 0.86.2 via `uv tool`, OpenCode 1.18.34 via npm, a 14B coder model pulled; six crawl-tier runs persisted, Aider 1 of 3 on each of two models, OpenCode 0 of 3 and invalid because it wrote outside its worktree. Two harness defects from the first live Linux runs: the timeout handler killed the runner (fixed on `main`, test-first) and OpenCode's broken isolation (filed, two leads). DISPATCH's A1 holds for both tools with no code, and within-cell spread showed at the crawl tier, so its Status Log carries three entries. The hub's Focus step 2 now says so.

Evidence for the claims a reader would act on: `git -C ~/projects/github/agent-eval branch -vv` → `home` on `origin/home`, `main` on `origin/main`; `.venv/bin/python -m pytest -q` there → `418 passed`; `ls results/*/results.json` there → 3 files.

Overclaims the user caught this addendum: 0

Overclaims a reviewer caught this addendum: 0 (no reviewer ran)
