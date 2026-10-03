# Session: The Backlog Cycle, a Redacted Leak, and the Private-Term Gate

**Date**: 2026-10-02
**Branch**: main; topic branch `topic/overwatch-private-terms` (merged `667ff59`, deleted)
**Tags**: #session #doctrine #overwatch #propagation #security #review #infra #testing
**Documents**: [20261002_overwatch_release_entries_draft.md](../plans/20261002_overwatch_release_entries_draft.md), [pcc.md](../../.claude/commands/pcc.md), [test_pcc_private_terms.py](../../tests/unit/test_pcc_private_terms.py), [adopt_doctrine.py](../../scripts/adopt_doctrine.py), [code-reviewer.md](../../.claude/agents/code-reviewer.md), [README.md](../../.claude/README.md), [docs/tasks.md](../tasks.md), [CHANGELOG.md](../../CHANGELOG.md)
**Implements**: [conop_overwatch_claim_verification_and_irreversible_guards.md](../plans/conop_overwatch_claim_verification_and_irreversible_guards.md) (release preparation; the destination rule and check 7 sit outside its waves); [propagation-protocol.md](../propagation-protocol.md) (one cycle, six steps)
**References**: [20261002_private_terms_gate.md](../reviews/20261002_private_terms_gate.md), [20261001_doctrine_transport_gate.md](../reviews/20261001_doctrine_transport_gate.md) (W1, the seeding table), [20261001_assay_bootstrap_and_agent_output_destination.md](20261001_assay_bootstrap_and_agent_output_destination.md), [SKILL.md](../../.claude/skills/verifying-claims/SKILL.md)
**Follows**: [20261001_overwatch_wave2_verifying_claims.md](20261001_overwatch_wave2_verifying_claims.md)

---

## Summary

The user asked for three things and all three landed: the OVERWATCH release entries are drafted, the doctrine backlog reached 16 repos in one cycle, and the agent-output-destination rule shipped as prose on six surfaces plus a deterministic `/pcc` check, after three `code-reviewer` rounds. The hold on propagating any OVERWATCH entry stands; the drafts sit in `docs/plans/`, which the script does not read.

On the way, the session found that yesterday's record of keeping five private terms out of this public repo had pasted the five terms into the Evidence line that certified their absence. The line was redacted, the unpushed history was rebuilt so that no pushed tree carries it, and the user chose to accept that seven already-public commits still do. The check built this session, `/pcc` check 7, fails on any recurrence and keeps its term list outside every repository.

Found at close: a GitHub mirror of a GitLab work repository sits under `~/projects` with a `.claude/commands/` directory, so propagation discovery lists it. This hub must never write into it. It was not notified today only because it appeared after the run.

| Metric | Value |
|---|---|
| Tests on `main`, start of session | 432 |
| Tests on `main`, end of session | 462 (29 for check 7 and the rule, 1 for the adoption helper) |
| Commits on `main` this session, before this doc | 24 (22 rebuilt before push, 1 merge among them) |
| Review agent runs | 1 `code-reviewer`, three rounds in one report |
| Subagent tokens, as reported at each round's end | about 0.75M (172k, 264k, 310k; later rounds count earlier context again) |
| Gate findings, round 1 | 1 Critical, 11 Warning, 11 Suggestion |
| Gate findings, round 2 | 1 Critical, 3 Warning, 9 Suggestion |
| Gate findings, round 3 | 0 Critical, 0 Warning, 4 Suggestion |
| Harness cases with a term in the output, final block | 0 of 45 |
| Doctrine deliveries | 70 entries to 16 repos (10 appended, 6 new) |
| Delivery marks seeded by hand before the run | 5 |
| PCC check 5, at close | 0 MISSING over 34 paths; 0 MISSING-DIR |
| Lead claims a reviewer refuted | 5 (Appendix A) |
| Lead errors the lead caught itself | 4 (Appendix A) |

## Work Completed

### 1. The adoption helper copies every Level 0 skill (`7495612`)

`scripts/adopt_doctrine.py` copied 6 of the 12 Level 0 directory-form skills; its list was frozen at the 2026-05-19 bundle, while the `session-end.md` and `session-doc-format.md` it copies had come to point at `traversing-the-knowledge-base` and `verifying-claims`, neither of which it shipped. The six added: `using-topic-branches`, `writing-simple-and-direct`, `traversing-the-knowledge-base`, `designing-clear-data-displays`, `lake-conventions`, `verifying-claims`. A pin test reads the framework's Level 0 headings and fails on any directory-form skill the list lacks: red with 6 missing, green after. The open P3 named the traversal skill alone; the full gap surfaced here. `lake-conventions` is included because the template bootstrap ships it to every repo and the skill routes work against personal by `project.scope` itself.

### 2. The leak, the redaction, and the rebuild (`7af6625`, `527abd4`)

The 2026-10-01 assay session record's Claims table certified that no internal hostname, username, codename, or sibling repository name had reached this public repo, and its Evidence line pasted the shell loop that searched for them, terms included. One commit (`5a04f2b`), on `origin/main` since 2026-10-01 17:40, in a public repository.

The line now names the count and says the list lives outside the repo. The redaction was committed a few minutes after the adoption-helper fix, so that fix's tree still carried the line, and the first live run of check 7 at the hub printed exactly that path. Nothing after the public tip had been pushed, so the 22 unpushed commits were rebuilt with the redaction first (`git cherry-pick` twice, then `git rebase --rebase-merges --onto`), the final tree unchanged, and `main` went up as a fast-forward. The 22 new SHAs were substituted in the task list, the changelog, and the gate review record, which carries the map.

Seven public commits, `5a04f2b` through `368dd5a`, keep the line in history. The user accepted that, on the lead's recommendation: the redacted tip stops casual exposure, the terms are low value in isolation, and a rewrite is not a purge without a GitHub support request, while it would cost the other box a reset and 17 SHA citations a remap.

### 3. The OVERWATCH release drafts (`bae2873`, revised through `0db0c35`)

`docs/plans/20261002_overwatch_release_entries_draft.md` holds the entries the release will copy to the top of `docs/doctrine-updates.md`: A1 (the Step 4 pytest line, breaking), A2 (the tool checks), B (`verifying-claims` 1.0.0 with its six surfaces and a task 2d paragraph to fill), C (the isolation tripwire), D (install pinning), E (the Purpose column), F (the destination rule and check 7), and a slot G for task 1e. Each answers the Evaluation Gate's five questions and carries a Detect block, an Adoption-Mode Table, Action required, Rollback, and Files. Three open items head the file: the WHETSTONE `KB-graph:` line rides in the same two files as entry B and needs its own entry or a named row; entry F's final verdict is in the review; the A1/A2 split follows Rule 4 but departs from the 2026-10-01 reading of "1c alone as breaking" and needs the user's yes.

### 4. The backlog cycle: 70 entries to 16 repos

`KB-graph: from the OVERWATCH task line to the propagation protocol's Delivery Mark section, then to the transport gate review's W1 table (2026-10-01) → the five marks to seed and what each repo already held: fist and schelling-point all 15 headings; stx-server and propter all but 09-18; beesly-equilibrium all but 08-29, 08-30, 09-18. Without that walk the run would have sent 20 redundant entries.`

The five marks were seeded from the hub's 15 headings, the dry run with `--since 2026-08-21` was read repo by repo against a probe of what each already held (skill versions, the traversal directory, `machine.py`, `HOME-STORAGE.md`), and the live run followed. The protocol's step 5 asks for the cycle number; the 2026-07-20 cycle was the seventh and no record numbers the 2026-08-03 run, so this is the ninth if that one was the eighth. Repos: 16 written, 10 appended and 6 new. Anomalies: `daily_weather`, not on the roster, had hand-adopted through 09-18 that morning and committed a full mark, so it was up to date; the lead's first count said 15 repos and 18 marks, and the reviewer counted 16 and 19 (Appendix A). No OVERWATCH entry was in the cycle. The script's output, the only record of the 70:

```
Appended 5 entries (2026-08-21, 2026-08-27, 2026-08-29, 2026-08-30, 2026-09-18): cad/digquad-mount
Notified 5 entries (2026-08-21, 2026-08-27, 2026-08-29, 2026-08-30, 2026-09-18): cad/dnd-minis
Appended 5 entries (2026-08-21, 2026-08-27, 2026-08-29, 2026-08-30, 2026-09-18): cad/shark
Appended 5 entries (2026-08-21, 2026-08-27, 2026-08-29, 2026-08-30, 2026-09-18): github/agent-eval
Notified 3 entries (2026-08-29, 2026-08-30, 2026-09-18): github/beesly-equilibrium
Up to date: github/daily_weather
Appended 5 entries (2026-08-21, 2026-08-27, 2026-08-29, 2026-08-30, 2026-09-18): github/elephant-graveyard
Up to date: github/fist
Appended 5 entries (2026-08-21, 2026-08-27, 2026-08-29, 2026-08-30, 2026-09-18): github/magic-movies
Appended 5 entries (2026-08-21, 2026-08-27, 2026-08-29, 2026-08-30, 2026-09-18): github/paperboy
Appended 5 entries (2026-08-21, 2026-08-27, 2026-08-29, 2026-08-30, 2026-09-18): github/project-megan
Notified 1 entry (2026-09-18): github/propter
Appended 5 entries (2026-08-21, 2026-08-27, 2026-08-29, 2026-08-30, 2026-09-18): github/quest-engine
Up to date: github/schelling-point
Notified 1 entry (2026-09-18): github/stx-server
Appended 5 entries (2026-08-21, 2026-08-27, 2026-08-29, 2026-08-30, 2026-09-18): github/swimming-analytics
Notified 5 entries (2026-08-21, 2026-08-27, 2026-08-29, 2026-08-30, 2026-09-18): github/tactics-game
Notified 5 entries (2026-08-21, 2026-08-27, 2026-08-29, 2026-08-30, 2026-09-18): github/veil-engine
Appended 5 entries (2026-08-21, 2026-08-27, 2026-08-29, 2026-08-30, 2026-09-18): sony/heimdall-darkroom
```

The notifications and marks are uncommitted in their repos; committing them is each consumer's step. Ten of the appended repos still hold their 2026-08-03 notice unread.

### 5. The destination rule and `/pcc` check 7 (merged `667ff59`)

The 2026-10-01 incident had three candidate homes. Two were taken. The rule, on the scope matrix, the three reviewing agents, and the two team templates: an agent's output goes to the repository that owns the sensitivity of its input, and the test the agent can run is whether the material's path is under `git rev-parse --show-toplevel`; outside it, or handed over from outside, the scratchpad is the default and the owning repository is named, or described when its name is itself private. The gate, check 7: a per-machine term list at `$HOME/.config/tacsop/private-terms` (override `TACSOP_PRIVATE_TERMS`), never in any repo; `git grep -l -i -F` over the index and every commit not on any remote, with tracked file names and unpushed commit messages checked too; each hit printed as a path, paths that are themselves hits withheld and counted. The list exists on this box with five terms.

Three review rounds. Round 1's Critical: a term in a directory or file name printed in the FAIL line, and the bullet told the reader to paste the path, which reproduces the `5a04f2b` shape; a term only in a file name was not detected at all. Its Warnings: `-- .` scanned the current directory only; the index is not what a push carries; `-I` skipped binaries for nothing; surrounding whitespace made a list line inert; the second incident was misdated; the rule had no decision procedure; three surfaces still sent output to `docs/` unconditionally. Round 2's Critical was the unpushed redaction. Its Warnings: a hex-only term inside a commit's short sha vanished between the withheld count and the printed lines; the no-upstream fallback scanned 1 of 12 commits a push of the branch would carry; the `ls-files` test sent this repo's own uncommitted files to the scratchpad. Round 3: GO, with two Suggestions applied in the reviewer's wording after the GO (`git grep -c` to `-l` in the changelog; the tracking refs are a cache, fetch first) and no fourth round. Every defect was reproduced before it was fixed, and every behavior went in red first: 6 missing, then 15 failed of 25, then 8 failed of 29.

The final block's shape is simpler than either draft: list hit paths, strip the commit prefix, deduplicate, and split the same strings with one grep into withheld and printed, so no hit can fall between the two whatever the term is made of.

### 6. The assay mirror, found at close

`~/projects/github/assay` is a GitHub mirror of a GitLab work repository, bootstrapped from this template, so it has `.claude/commands/` and the dry run now lists it. The user's rule: this hub is never responsible for updating it, and nothing is written into it from here. Filed as a P1 with a recommendation for a hub-side exclusion in config, which keeps the decision where the responsibility is and writes nothing downstream. The user also named the reverse leg: the hub lead reading that repo's lessons from here, the way D10 harvests a downstream lesson file. Filed as a P3.

## Claims

| Claim | State | Evidence |
|---|---|---|
| The suite passes on `main` | tested | `.venv/bin/pytest -q` → `462 passed, 1 warning in 5.12s`, `exit=0`; `CI=true .venv/bin/pytest -q` → `462 passed, 1 warning in 5.91s`, `exit=0` (at `0db0c35`'s tree, unchanged in code since); `.venv/bin/python -V` → `Python 3.12.13`; at `32fd4c0` |
| The session's work is on `origin/main` | deployed | `git rev-parse --short HEAD` → `32fd4c0`; `git ls-remote origin refs/heads/main` → `32fd4c0…`; `git status --porcelain` → no output |
| No commit pushed today carries a private term in its tree | observed | for each of `git rev-list 368dd5a..origin/main` (24 commits), `git grep -c -i -F -f <list> <commit> -- .` → no output; the public tip the same → no output |
| Seven public commits still carry the line | observed | the same grep over `5a04f2b^..origin/main` → 7 commits with 1 file each; `d1deddc`, the parent, 0. Accepted by the user. |
| The topic branch is merged and deleted | deployed | `git merge-base --is-ancestor 667ff59 main` → yes; `git branch --list 'topic/*'` → no output |
| Check 7 is clean at the hub | observed | the block extracted from `pcc.md` and run at the repo root → no output, `exit=0`; at `32fd4c0` |
| Living docs name no missing path | tested | PCC check 5 file pass → no MISSING line over 34 paths; directory pass → no MISSING-DIR line |
| The backlog cycle wrote 16 notifications and left 19 marks at 15 headings | observed | `find ~/projects -maxdepth 4 -name upstream-update.md -path '*/.claude/*' -newermt '2026-10-02 00:00'` (the hub excepted) → 16; `wc -l` over every `doctrine-delivered` → 19 files, each 15; the script's own output above → 70 entries |
| The assay mirror was not notified | observed | `test -f ~/projects/github/assay/.claude/upstream-update.md` → absent; the dry run at close → `github/assay: would send 1 entry (2026-09-18) (new)` |
| The adoption helper plans all 12 Level 0 skills and writes nothing in a dry run | observed | from a scratch downstream, `adopt_doctrine.py --upstream <hub> --dry-run` → twelve `would copy dir → .claude/skills/...` lines, `exit=0`; the scratch tree held only the `src/demo` the lead made |
| The gate ended in GO | observed | `grep -n '^Verdict' docs/reviews/20261002_private_terms_gate.md` → three lines, the last `Verdict: GO` |
| The kernel changes what a model claims | observed | UNVERIFIED: task 2d, the controlled replay, needs transcripts that exist only on the work terminal |

Overclaims the user caught this session: 0

Overclaims a reviewer caught this session: 5

## Key Decisions

| Decision | Chosen | Over | Why |
|---|---|---|---|
| OVERWATCH entries (user, unchanged) | Hold until 1e and 2d | Propagate the skill now | 2d is the only test of the kernel's effect; the hub's own first session under it refuted 16 claims |
| The three trap candidates (user, on the lead's recommendation) | Hold until 2d | Add now | The replay measures the text as it stands; the leak-shaped one has the strongest case to go first after 2d |
| Backlog cycle (user) | Run now from Nidhogg, OVERWATCH entries excluded | Wait for the one cycle after 2d | The work repos are not on this box; the five seeds were needed anyway; a low-stakes first live run of the transport |
| `lake-conventions` in the helper (lead) | Copy it | Leave it out as scope-dependent | The template bootstrap ships it to every repo; the skill routes by `project.scope` itself |
| Where the destination rule lives (lead) | Prose at the point of action and a `/pcc` check | One of the three alone | The prose names the test; the check is deterministic; the term list outside the repo is what the leak demanded |
| Check 7's unit of output (lead, round 2) | Paths, no commit prefix, no count | Lines carrying sha and count | One grep splits the same strings into withheld and printed, so nothing can fall between |
| Content a remote already holds (reviewer and lead, round 3) | Flag it when an unpushed commit carries it | Exclude it | The contract is what a push carries; after a rewrite the stale local commit is exactly what must be flagged |
| The leak's history (user, on the lead's recommendation) | Accept: redact on the tip, rebuild the unpushed commits | Rewrite from `5a04f2b` | A rewrite is not a purge without GitHub support; it costs the other box a reset and 17 citations a remap |
| The one FAIL at the hub (user) | Repair: rebuild the unpushed history with the redaction first | Push and let the flag clear | "Merge clean"; no force-push was needed because nothing after the public tip had been pushed |

## Pillar Compliance

- **Shift-Left Testing**: every behavior of check 7 and the adoption helper went in red first, and each gate finding was reproduced before its fix. The audit hook saw none of it: it watches `src/myproject/`, and this session's code is in `scripts/`, `tests/`, and `.claude/`. The red runs are in the commit messages.
- **Simplicity First**: the final check 7 block is shorter in logic than the round 1 block, with one grep deciding both branches. The reviewer's `while read` loop was declined for the path-only design. The adoption helper fix is a six-line list change and one pin.
- **Config-Driven**: the term list is a per-machine file with an environment override, not YAML, because it must never be in the repository. The assay exclusion is recommended as config.
- **Branching**: one topic branch for the gate work, merged with a merge commit at GO and deleted. The adoption-helper fix and the redaction were lead-only and landed on `main` directly, which is where the ordering defect came from: a fix committed before a redaction in the same unpushed span.

## Lessons

1. **A probe for an absence names what it looks for.** The Evidence line that certified five terms absent republished them. Record the count and where the list lives, never the list. Filed as a trap candidate for the skill.
2. **Build both branches of a filter from the same strings.** Check 7's first two drafts counted on one form of a line and printed on another, and a hit could vanish between them. The reviewer found it with a hex term inside a sha; the fix was to stop carrying anything but the path.
3. **Reproduce with the real input shape.** The lead's first re-run of three findings passed the list as a process substitution, the block read it twice, and the second read got nothing. Three "misses" were artifacts. A real file reproduced all three.
4. **Commit order is a scan boundary.** A fix committed before a redaction carries the leak in its tree; a push carries every tree. Rebuilding unpushed history is cheap and needs no force; pushing the leak and letting the flag clear is not the same thing.
5. **Discovery is shape, not intent.** A mirror bootstrapped from the template is a propagation target by the presence of one directory. The protocol's open opt-out question is now a P1, and the answer belongs on the hub's side.
6. **An exit status read after a broken chain belongs to the command that broke it.** "check7 exit=1" was `git branch -D` failing; the check had not run. Yesterday's pipe trap in another coat.
7. **The tracking refs are a cache, twice.** Yesterday a stale `origin/main` refuted a claim; today "not on any remote" reads the same refs. Fetch first is now a bullet in the check.

## Next Steps

1. Before any propagation run from any box: the assay exclusion (P1), hub-side, test-first.
2. The work terminal: Wave 0 (0b to 0d), task 1e, task 2d. 2d decides Wave 2 and lifts the hold.
3. The release from the draft: fill the dates and the 2d paragraph, settle the A1/A2 split and the KB-graph entry, copy, pre-flight, dry run, propagate.
4. After 2d: the three held traps for `verifying-claims`.
5. The other box pulls `main`, which moved by 25 commits today, before it commits anything.
6. Still open from before: the WHETSTONE Wave 1 count, the launch-control and veil-engine harvests, the audit-hook pin, the dev/prod config-profile ADR, the configuration-management reconciliation, the fleet ledger, the 0.2.0 cut; and from today, check 6's regex against D4's path list (P3) and reading assay's lessons from here (P3).

## Commits

| Commit | Change |
|---|---|
| `7af6625` | Redact five private terms from one Evidence line (rebuilt to precede the next) |
| `7495612` | The adoption helper copies every Level 0 skill; a pin holds the two lists together |
| `6d06553`, `e90c512`, `0f5a6b2`, `5fded32`, `bae2873` | The destination rule on five surfaces, check 7, its first 12 tests, the release drafts |
| `1c3895d`, `9bdc0d7`, `b6d5ca2`, `b9f2229`, `8c719fc` | Gate round 1 fixes: paths withheld, names and history scanned, the rule's test, 25 tests, the records |
| `f01a8ce`, `6f89c62`, `0f0ca35`, `e3bc491`, `0db0c35` | Gate round 2 fixes: hits as paths, not on any remote, the working-tree test, 29 tests, the records |
| `8baad24`, `a0539bc` | Round 3 suggestions, after the GO |
| `667ff59` | Merge `topic/overwatch-private-terms` |
| `16c208b`, `c41b293` | The gate review record; the destination task closes |
| `527abd4`, `32fd4c0` | The SHA remap after the rebuild; the records name the pushed state |

## Appendix A: The Lead's Claims and Errors, by Who Caught Them

**Refuted by the reviewer's re-run (5, the M count)**

| # | Claim | Where | Caught by |
|---|---|---|---|
| 1 | "The output names a file and a count, never the term" (a term in a path name printed) | `pcc.md`, the first check 7, and a message to the user | round 1, C1 |
| 2 | "70 deliveries to 15 repos" (16) | `docs/tasks.md`, and a message to the user | round 1, W11 |
| 3 | "18 marks at 15 headings" (19) | `docs/tasks.md`, and a message to the user | round 1, W11 |
| 4 | "Two incidents, 2026-10-01 and 2026-10-02" (both 10-01; the second found 10-02) | `pcc.md`, the draft | round 1, W6 |
| 5 | "18 written by the run" (16; two seeds were left as seeded) | `docs/tasks.md` | round 2, R2-S6 |

Numbers 1 to 3 were said to the user as well; the user did not act on them before the reviewer's re-run, so they are in M, not N.

**Caught by the lead's own re-run (4, in neither count)**

1. "23 commits ahead" in a message to the user; `git rev-list --count` said 22.
2. "All five reproduce": three of the five re-runs had passed the term list as a process substitution the block read twice, so they showed nothing. Re-run with a real file, all five reproduced.
3. "check7 exit=1" after a broken command chain; the exit belonged to `git branch -D`, and the check had not run.
4. The round 2 reviewer's R2-S7 and round 1 S11 said the CONOP lacked the 2-sessions figure; the lead's grep found it in the Status Log, and the reviewer retracted both. A reviewer's claim, listed here because the lead's first draft had cited the CONOP without a line.
