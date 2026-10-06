# CONOP SEXTANT — An Evaluation Repository for Doctrine Measures

**Status**: In Debate. Round 1 returned 2026-10-05: `proposer` SHIP-WITH-FIXES, `code-reviewer` GO-WITH-FIXES. Revised the same day after the user's four rulings (Status Log). Approval is the user's.
**Date**: 2026-10-05
**Lead**: jhutchison (session lead: Claude)
**Parent task**: `docs/tasks.md`, the SEXTANT line (added 2026-10-05). The user's decisions of 2026-10-04 that started it: this hub tracks what happened in other repos but does not maintain data; Nidhogg computes and home storage is the system of record for personal data; OVERWATCH MOE 1 measures `fist`, with `propter` if necessary. The user raised two shapes, a repository for OVERWATCH alone or one built like the `stx-server` trainer where many plans' measures live; the lead recommended the second, and the user's 2026-10-05 rulings build on it.

---

## Problem

The hub keeps measurements as sentences, and a sentence drifts while it still reads as current. Row A4 of OVERWATCH's Assumptions table counts "173 `.jsonl` files on Nidhogg" (2026-09-30); the same count on 2026-10-05 is 287, and 232 of those are subagent files the original count never separated out. The fleet-ledger task in `docs/tasks.md` says `stx-server`, `veil-engine`, and `tactics-game` are not "on this box"; all three are on disk on Nidhogg, because the line was written on another machine and does not say which. WHETSTONE's Wave 1 session count collided when two machines numbered the same window. Meanwhile the plans' measures have no executable home: OVERWATCH MOE 1 and MOE 2, falsifiers A1 and A4, task 2d's scoring, WHETSTONE E1 to E6, the picture's G7, and fleet membership (G3) are each counted by hand in a session doc or not collected at all.

Evidence: `grep -n '173' docs/plans/conop_overwatch_claim_verification_and_irreversible_guards.md` → line 73, row A4; `find ~/.claude/projects -name '*.jsonl' | wc -l` → `287`, and with `-path '*subagents*'` → `232`; `test -d ~/projects/github/<repo>/.git` → present for all three repos.

`maintaining-the-common-operating-picture/ADOPTION.md` already says where measurements belong: "a generated report under a root named in config, outside every checkout". Nothing writes there. The hub cannot write personal data there: it declares no `project.scope`, so the routing rule treats it as work and keeps home storage closed (`lake-conventions/HOME-STORAGE.md:20-22`; `config/project.yaml`, "The hub is a template and declares neither").

---

## Situation

### Friendly Forces (what we have)

- **The picture's doctrine.** `ADOPTION.md` gives the "Where things live" table, four degenerate cases (one box, no observations yet, a second clone or box, an unreachable store), and three rules for probes: a probe never writes into any probe's universe; a reader quarantines a record it does not recognise and reports the count; every quantity renders as `{checked: true, value, measured_at, collector, subject, universe, shape}` or `{checked: false, reason}`.
- **Home-storage doctrine.** `lake-conventions/HOME-STORAGE.md`: role-named variables in `.env` with a loud failure, no address in git, and rules 1, 2, 5, 6, and 7 (no embedded database on the share; a mirror with deletions is not a backup; a least-privilege data account; bulk data on the device and compute local; sync down once and compute against the copy). `fist` already reads `HOME_CORPUS_ROOT`.
- **The trainer shape, proven.** `stx-server` "logs what happens, and recommends a tier each week by rules", with Append-Only History among its pillars (`docs/reviews/20260827_stx_server_lessons_harvest.md`). Its loop maps onto doctrine: the program is the doctrine, the learner is the agents' sessions, the practice log is the transcripts and ledgers, and the weekly tier is a verdict per measure.
- **Transcripts carry what the first collectors need.** fist's oldest surviving transcript holds 113 `user` and 176 `assistant` records, 104 `tool_use` blocks matched by 104 `tool_result` blocks, and 58 Bash calls with a command string. Across fist, propter, and stx-server, 0 of 11,190 Bash calls lack one (`docs/reviews/20261005_sextant_review.md`, claim 30).
  Evidence: a line-by-line Python count over that file, 2026-10-05 → `user 113, assistant 176, tool_use 104, tool_result 104, Bash with command 58, unparsable 0`.
- **An exclusion that fails closed.** `propagation.exclude` in `config/project.yaml`, read by `scripts/propagate_doctrine.py` and pinned in `tests/unit/test_propagate_doctrine.py`: it matches a path relative to `~/projects` and stops on a malformed list.
- **Measures already defined.** OVERWATCH's MOE and kill-criteria; WHETSTONE's E1 to E6, of which E4 and E5 name no known-bad reference; the picture's M1 to M3. This plan builds instruments for them, not new measures.
- **A bootstrap path used at least four times**: `docs/design/from_template_to_project.md` (`veil-engine` 2026-07-26, `stx-server` 2026-08-26, `propter` 2026-08-30, `assay` 2026-10-01).

### Enemy Forces (what works against us)

- **Transcripts age out.** Claude Code deletes transcripts, with their subagent files and tool results, once they are older than `cleanupPeriodDays`: default 30, minimum 1, and `0` fails validation (gap G8). Before 2026-10-05 nothing on Nidhogg set it, and the oldest surviving transcripts were stx-server's from 2026-09-07, propter's from 09-13, and fist's from 09-15. The user set `3650` on 2026-10-05 (task 0a). Clients before v2.1.89 read `0` as "write no transcripts", so `0` must never be written anywhere.
- **The sampling frame is partial.** 5 of fist's 15 session docs, dated 2026-09-10 to 09-14, have no transcript on Nidhogg, and age-out does not explain it, since older transcripts survive in stx-server. Those sessions ran on another machine or in another directory. MOE 1's frame is fist sessions on Nidhogg.
- **Work material is not confined to one directory.** `assay` has 6 transcripts here. The hub, which counts as work, has 9 top-level transcripts, and 4 of them hold a term from the per-machine private-terms list; one records the session that bootstrapped `assay` from the hub.
  Evidence: count-only `grep -l -i -F -f ~/.config/tacsop/private-terms` over the hub's top-level transcripts → `4`; `ls` count in `assay`'s transcript directory → `6`.
- **Directory names are encoded, so decoding them is ambiguous.** Claude Code names a transcript directory after its working path with separators replaced by `-`. `~/projects/github/daily_weather`, which declares `scope: personal`, writes to `…-daily-weather`. A session started in a subdirectory writes to a longer name.
- **A transcript holds conversation text**, including whatever the session read, and the home NAS's name appears in 36 subject transcript files (`docs/reviews/20261005_sextant_review.md`, W9). The outputs are counts and verdicts, but a raw copy on home storage is still a copy of that text.
- **Self-report.** A session's own `N` line is written by the model the kernel targets. A measure built on it inherits the overclaim risk it exists to measure.
- **A scorer that disagrees with itself is noise with a number on it.** OVERWATCH predicted that free-text claim detection "will misfire", and the 2026-05-19 MAUT weighted false positives at 0.20 on the record that "false-positive hooks get disabled within a week."
- **One more repo is one more place for prose to rot**, and one more doctrine consumer. The fleet-ledger line above is the type specimen.
- **The share is slow for many reads.** About 200 scans of a store under 1 GB ran two hours over the mount and 41 to 44 seconds against a local copy (HOME-STORAGE rule 7, `propter`, 2026-09-04).
- **The topology doc is missing on Nidhogg**, and the roster's `references.home_storage` points into the hub's working tree, one `git add -f` from publication (`docs/tasks.md`, P3, 2026-10-04).

### Terrain (the ground we operate on)

- **Nidhogg computes; home storage is the system of record for personal data** (the user, 2026-10-04). Work data stays on the lake, and crossing that line is an explicit human decision (`HOME-STORAGE.md:33-36`).
- **A bootstrap copies the whole template and strips by hand.** `assay`, bootstrapped 2026-10-01, still carries `scripts/adopt_doctrine.py` and `scripts/lake_preflight.py`. A collector in the hub's `scripts/` would ride into every new repo the same way.
  Evidence: `test -e` on both paths under `~/projects/github/assay/scripts/` → present (stat only).
- **Subagent files are most of the record.** fist's 10 top-level transcripts hold 1,133 Bash calls; its 51 subagent transcripts hold 4,877. Subagents inherit the parent conversation's permission rules (`code.claude.com/docs/en/sub-agents.md`, read 2026-10-05), so ask rules reach their commands unless a subagent's own `permissionMode` skips prompts.
  Evidence: a line-by-line Python count over fist's transcript tree, 2026-10-05 → `(1133, 2)` and `(4877, 0)`, calls and unparsable lines.
- **The hub's own state is a separate job.** The hub's suite, branch, and tools are measured at `/session-start` (`CONTEXT.md:37`); a hub probe under the picture's slice 3 would take them. This plan's subject is sessions and repos.

### Assumptions

| # | Assumption | Cheapest falsifier | Blast radius if wrong | Kill-criterion |
|---|---|---|---|---|
| A1 | An agent labels candidate turns as the user does. A candidate turn is a user message that follows an assistant statement; its label says whether the user there contests a claim that proved false | The user labels the candidates from 10 fist sessions; an agent labels the same list blind. Report raw agreement, the count of positive labels, and Cohen's kappa | Wave 2; the switch the user ruled on 2026-10-05 (MOE 1 reads `N` until A1 passes) | Kappa below 0.6 with at least 10 positive labels: no automated scorer, and MOE 1 stays on `N`, labeled self-report. Fewer than 10 positives in 10 sessions: the event is too rare to rate on fist, and MOE 1 reports counts without a rate |
| A2 | The candidate list holds the corrections: the pre-pass misses few turns where the user contests a claim | The user reads 3 whole fist sessions and marks every correction; count how many the pre-pass listed | Wave 2's unit of scoring | The pre-pass misses more than 1 in 10 of the user's marks: the unit is wrong, and Wave 2 is redesigned before any scoring |
| A3 | Transcripts carry every Bash call's command string, in top-level and subagent files | Held 2026-10-05 over three subjects (Friendly Forces). Task 1c's first test repeats it on the copied set | Task 1c | More than 1 in 100 calls without a command: A4's counts cannot stand for what the harness prompts on, and 1c reports no rate |
| A4 | Home storage is reachable from Nidhogg through a role-named variable and the topology doc | Task 0b's doc exists, and a listing of the raw-inputs root returns without error | Task 1b's store half; D2's third home | Not reachable by 2026-10-31: SEXTANT stays local under the header `local picture, one box`, and D2's third home is dropped |
| A5 | fist keeps running at least 3 sessions a week on Nidhogg | The collector's own weekly count | Wave 2's timing; MOE 1's window | Neither fist nor propter reaches 20 sessions within 10 weeks of adopting the kernel: MOE 1 on a personal repo is abandoned and reported unmeasured |

The numeric bars are the lead's proposals; approval sets them.

---

## Mission

The hub lead bootstraps a personal-scope evaluation repository on Nidhogg that copies session transcripts into home storage and renders its first measure from them, OVERWATCH's A4 counts, by 2026-10-23, and runs MOE 1's scorer as a throwaway spike until it passes A1 and A2, in order to take measurement out of the hub's prose and give every plan's measure one re-runnable instrument whose output carries its age.

---

## Approaches Considered

### Approach A: Collectors in the hub

Collectors under the hub's `scripts/`, writing to a report root outside the checkout.

- **Pros**: no new repo and no new consumer; the hub's suite and gate habits apply at once.
- **Cons**: the hub declares no scope, so home storage stays closed to it, and declaring `personal` in a template would ship the wrong scope into every work bootstrap. A collector in `scripts/` rides into every new repo. The author of the doctrine would grade it.
- **Risk**: medium.

### Approach B: One evaluation repository, shaped like the trainer

`scope: personal`. One collector and one estimator per measure, as tested code. Raw-input copies on home storage; measurement records rendered locally first, then on the store. Each verdict uses its owning plan's own bar. The hub keeps the definitions and cites measure IDs with their stamps.

- **Pros**: the scope line holds by construction. The instrument is not the doctrine's author. The template stays clean. Measures outlive their plans, and this gives them one home.
- **Cons**: one more repo and doctrine consumer; a second place for prose to rot unless the picture is adopted at birth; a plan's bar lives in the hub while its code lives here, and the two can drift.
- **Risk**: medium.

### Approach C (bold): No central instrument; each subject measures itself

A `/session-end` step in every repo writes its own measurement records and a heartbeat line to the shared store, and the picture is their join.

- **Pros**: it scales with the fleet, and every personal repo reports itself, which would close G3 for them.
- **Cons**: it is self-report, which OVERWATCH Approach C rejected: "An auditor works from the ledger, not from the CFO's explanation." It arrives only through propagation, which is lossy (G3). Work repos cannot write to home storage, so the store splits by scope anyway.
- **Risk**: high.

### Approach D: One repository per plan

A repository for OVERWATCH alone, the first shape the user raised. Plans end and their measures outlive them: OVERWATCH targets 2026-10-16, and MOE 1 reads no sooner than about five weeks after fist adopts. Every CONOP carries measures, so every plan would spawn a repo. Rejected.

### Approach E: Copy first, repository on evidence

`proposer`'s alternative from round 1: copy transcripts with an untracked script, count A4's patterns with `jq`, spike the scorer in scratch, and create the repository only if A1 and A2 pass.

- **Pros**: no repository before a tested estimator exists.
- **Cons**: the copy is the riskiest code in the plan. It decides which projects are read and keeps the data, and E leaves it untested. `jq` also stops at the first unparsable line, which fist's transcripts hold (Terrain).
- **Risk**: medium.

Reusing `stx-server` itself was not an option: its subject is a practice season, its code holds no evaluation of agent sessions, and SEXTANT borrows its shape, not its repo.

**Recommendation and the user's ruling**: B, which the user chose on 2026-10-05 ("Now; scorer stays a spike"), with E's discipline inside it: the scorer is a throwaway spike until A1 and A2 pass, and no estimator joins the repository before then.

---

## Design Decisions

D3's switch is the user's ruling of 2026-10-05. The rest are proposed until the user approves the plan.

- **D1. Boundary by subject.** A measure whose subject is the hub's own checkout stays a hub probe. A measure whose subject is sessions or repos belongs to SEXTANT.
- **D2. Three homes.** The hub keeps each measure's definition, its bar, and the decision it informs. SEXTANT keeps the collector, the estimator, and any rubric, as tested code. Home storage keeps raw-input copies and, from the second slice, measurement records. The report root comes from a role-named `.env` variable with a loud failure; config holds only the variable's name (`HOME-STORAGE.md:89-102`). The hub cites a measure's ID and stamp, never a path, and never restates a count as current.
  ADR: D2 passes the triple filter. It is hard to reverse once plans cite SEXTANT's measure IDs, surprising without this context because every other plan keeps its numbers in its own Status Log, and a real trade-off against Approach A. Write it at approval.
- **D3. One instrument for both windows (the user's ruling, gated on A1).** MOE 1 reads `N` until A1 passes; then one collector scores both windows from transcripts, and a session's own line is a cross-check. Sessions under the kernel carry `Evidence:` lines and a `## Claims` table that tell a scorer which window it is in, so the collector strips both markers from both windows before scoring, and the report states what blinding remains imperfect.
- **D4. An allowlist by declared scope.** The collector lists checkouts under `~/projects`, encodes each path the way Claude Code names its transcript directories, and copies a directory only on an exact match to a repo whose committed config declares `project.scope: personal`. A directory that matches no repo, matches a repo with no scope, or matches only by prefix (a session started in a subdirectory) is skipped and counted. The hub is skipped: it declares no scope, and its transcripts hold private terms. `assay` stays on a deny list as a second layer. A quarantine on work terms waits on O6.
- **D5. Copies are additive.** The copy takes the whole project tree: top-level transcripts, subagent files, and tool results. A copy's name carries its source's size and modification time, so an updated file lands beside the earlier copy and never over it (HOME-STORAGE rule 2). A file modified within the last 10 minutes waits for the next run. Unparsable lines are kept and counted (`ADOPTION.md`, probe rule 2). A `README.md` beside the root says what it copies and as of when. The topology doc names who can read the root: the least-privilege data account only (rule 5). No transcript text enters git.
- **D6. It recommends; a human decides.** Each verdict applies the bar its owning plan states and prints that plan's path beside it. Only the user moves a plan's gate, as WHETSTONE D1 already requires: "Only a human flips status."
- **D7. The picture at birth, local first.** No state block in SEXTANT's config, and measurements render in the two shapes. Records render locally under `local picture, one box` and reach the store in the second slice, as ADOPTION asks ("Do not start with the join or the shared store"). One departure, stated: the empty-root render test ships in the first slice, not the third, because the picture is SEXTANT's product, not a side job.
- **D8. No framework before the second measure.** Wave 1 builds one collector end to end. A shared collector interface appears when a second measure needs it.
- **D9. A doctrine consumer like any other.** Bootstrapped from the template, it receives propagation cycles. Doctrine it discovers goes upward through WHETSTONE's D10 upward channel.

### Deferred, with rationale

- **O1. The repository's name.** SEXTANT is the plan's proword; the user names the repository.
- **O2. When fist adopts the kernel.** fist can adopt only through a release, and the user's hold blocks the release until OVERWATCH 1e and 2d run on the work terminal. The user may grant fist a canary exception or wait. Decide after A1, A2, and the first baseline count, since adoption closes the baseline.
- **O3. WHETSTONE Wave 3's utility slice** (`orphans()`, full-corpus `validate()`). Its subject is the hub's corpus, so D1 keeps it in the hub.
- **O4. A work-side twin** under lake doctrine (G9). The user's decision, on the work side.
- **O5. The retention stopgap.** Whether `3650` stays once task 1b's copy runs. A per-project retention for `assay` is not proposed: project settings outrank user settings, and whether a session in a repo with a shorter value sweeps every project's transcripts is UNVERIFIED.
- **O6. Which terms mark work material.** The per-machine private-terms list mixes work names with the NAS name, so a quarantine on the whole list would hold back most personal data. A work-terms subset kept outside git, like the list, is the likely answer. Decide before task 1b.
  Evidence: count-only `grep -l -i -F -f ~/.config/tacsop/private-terms` per transcript tree, 2026-10-05 → stx-server 33 of 37 files, daily-weather 19 of 59, fist 2 of 61, propter 1 of 49.

---

## Measures of Success

**MOP (performance)**

- Every collector's test runs on synthetic records built in test code with a fixed fake `sessionId`, including one unparsable line.
- The copy's test: counts by kind (top-level, subagent, tool result) equal the source's; a fixture project with no scope is never opened; a prefix-only match is skipped; a second run over a frozen fixture copies 0 files; a grown file lands as a new versioned copy.
- A guard test fails if any committed file holds a real session ID from the local transcript tree (compared by count, never printed) or a term from the private-terms list.
- Task 1c's counter matches labels assigned from the harness's documented matching rules (OVERWATCH, Friendly Forces), over fixture commands that include a compound command, a subshell, `rm -r -f`, `rm --recursive`, and `git add .` inside `&&`.
- The empty-root render test passes: no line reads clean.
- `code-reviewer` returns GO, or GO-WITH-FIXES with every fix applied, at each wave gate.

**MOE (effectiveness)**

- **Decisions rest on rendered lines.** OVERWATCH's next gate (task 1e's patterns) and WHETSTONE's next gate cite a measure ID and its stamp, not a prose count. Measurable at each plan's next gate.
- **Drift is caught where nobody looked.** Before Wave 1 starts, the lead names in this plan's Status Log one prose count in the hub that nobody has re-measured since it was written, and Wave 1's first render checks it. The 173-versus-287 drift cannot serve; it is already known. Measurable at Wave 1 exit.
- **OVERWATCH MOE 1 reports.** A baseline rate with its interval over fist sessions on Nidhogg, beside the smallest drop the design can detect, at Wave 2 exit. With at most 10 baseline sessions, a failure to detect is the likely result, and the report says so. The after-window no sooner than about five weeks after fist adopts.

**Calibration**: A1 applies CONOP-FORMAT's calibration rule with the user's labels as the known references; task 1c's labeled fixture applies it to the counter.

---

## Wave Breakdown

The dependency chain: inputs survive (Wave 0), then the repository, the copy, and the first deterministic measure (Wave 1), then the scored measure, whose design waits on A1 and A2 (Wave 2).

### Wave 0: Stop the loss (by 2026-10-14)

- **Team**: the lead and the user.
- **Tasks**:

  | Task | Purpose | Condition | Standard |
  |------|---------|-----------|----------|
  | 0a. Retention | Lets the user trust that no subject's inputs age out before task 1b copies them | `~/.claude/settings.json`; the user's yes, given 2026-10-05 | Done 2026-10-05: `cleanupPeriodDays` is `3650`, and no settings file on the box sets a smaller value. Open half: after a session start on or after 2026-10-08, stx-server's transcript dated 2026-09-07 is still present |
  | 0b. Topology doc | Tells task 1b where the raw-inputs root is, and lets any agent on Nidhogg find the store | The user writes it, since it holds addresses, at a path outside every checkout, and repoints the roster's `references.home_storage` there; the device's snapshot schedule covers the raw-inputs root | `test -f` on the roster's path succeeds; `/pcc` check 7 on the hub prints nothing |
  | 0c. NAS name guarded | Lets the user publish the hub without the NAS name, including in a pasted transcript record | The per-machine private-terms list; the one committed hit | Done 2026-10-05: the name is on the list; `810e931` redacted the 2026-08-30 review forward; check 7's content and message scans find 0 hits |
  | 0d. Debate and approval | The user's go or no-go on this plan | Round 1 done; a second round on this revision if the user asks | Status set by the user |

- **Exit criterion**: 0a's open half, 0b, and 0d done.

### Wave 1: Bootstrap, the copy, and the first measure

- **Team**: `feature-development`. The lead runs 1a, since it writes `.claude/`. `python-prototyper` may write collectors, test-first. `test-runner` and `code-reviewer` at the gate.
- **Tasks**:

  | Task | Purpose | Condition | Standard |
  |------|---------|-----------|----------|
  | 1a. Bootstrap | Gives the lead a repo whose scope routes data to home storage; every later task builds on it | `from_template_to_project.md`; `scope: personal`; the picture's first slices at birth (D7) | Config declares `scope: personal`, the report root's variable name, and the `assay` deny entry; a test fails closed on a malformed deny list; the empty-root render test passes |
  | 1b. Copy | Lets the user retire 0a's stopgap (O5) and lets every collector read inputs that no longer expire | `~/.claude/projects` into the raw-inputs root, by D4's allowlist and D5's rules; O6 decided | The MOP copy tests pass; on the real tree, counts by kind on the store equal the source's for fist and propter; skipped directories are counted in the run's output |
  | 1c. A4 counts | Gives the lead OVERWATCH task 1e's pattern list, to decide which patterns ship | Every Bash command in the copied personal transcripts, top-level and subagent; task 1e's seven patterns | Prompts per session per pattern, as records in the two shapes; one rendered line per pattern with its stamp; the labeled-fixture test passes; unparsable lines counted |

- **Exit criterion**: OVERWATCH's Status Log cites 1c's measure IDs and stamps, and `code-reviewer` returns GO.

### Wave 2: OVERWATCH MOE 1 on fist (a spike until A1 and A2 report)

- 2a. The deterministic pre-pass lists candidate turns; A2 against the user's marks on 3 sessions; A1 with the user's labels and an agent's blind labels on 10 sessions; the smallest detectable drop, stated before any scoring.
- 2b. The baseline: every surviving pre-kernel fist session on Nidhogg, scored; the rate rendered with its interval.
- 2c. The after-window, once fist adopts (O2).

### Wave 3: Further measures (sketch)

Each further measure moves here one at a time, with its owning plan's definition and a test, and only when that plan names a decision it informs.

---

## What We Do NOT Build

- A dashboard or a web app. The picture is a rendered file.
- An automated scorer before A1 and A2 pass.
- Any write into a subject repo. Probes read.
- Transcript text in git, in SEXTANT or the hub.
- Work-scope inputs or outputs, the hub's transcripts included.
- A quarantine keyed to the whole private-terms list (O6).
- A metrics framework before the second measure (D8).
- New measures. Each measure belongs to the plan that defines it.

---

## Agent and Team Design

None new. Round 1 used `proposer` and `code-reviewer`, blind to each other. Wave 1 uses the `feature-development` template as above. Wave 2's scorers are the user, who labels A1's set, and an agent that labels it blind; the agent never sees the turns after each candidate.

---

## References

- `.claude/skills/maintaining-the-common-operating-picture/ADOPTION.md`: "Where things live", the degenerate cases, the probe rules, the slice order
- `.claude/skills/lake-conventions/HOME-STORAGE.md`: the routing rule, the boundary line, the code pattern, rules 1, 2, 5, 6, 7
- `docs/plans/conop_overwatch_claim_verification_and_irreversible_guards.md`: MOE 1, falsifier A4, task 1e, Status Log 2026-10-05
- `docs/plans/conop_whetstone_recursive_doctrine_loop.md`: D1, D4, D7, D8, D10, E1 to E6
- `docs/gaps.md`: G3, G7, G8, G9
- `docs/reviews/20261005_sextant_proposer.md` and `docs/reviews/20261005_sextant_review.md`: debate round 1
- `docs/reviews/20260827_stx_server_lessons_harvest.md`: the trainer shape
- `docs/design/from_template_to_project.md`: the bootstrap
- `code.claude.com/docs/en/settings-reference.md` and `claude-directory.md`, the raw pages, read 2026-10-05: `cleanupPeriodDays` and what the sweep deletes

---

## Status Log

- **2026-10-05**: Drafted on Nidhogg after the user's decisions of 2026-10-04.
- **2026-10-05, debate round 1, and the user's rulings.** `proposer` returned SHIP-WITH-FIXES with 8 findings. `code-reviewer` returned GO-WITH-FIXES with 3 Critical, 11 Warning, and 16 Suggestion findings, and checked 56 of the lead's claims: 43 hold, 5 are refuted, 7 are refuted in part, and 1 cannot be re-run. The reviewer disclosed that it saw the opening of the proposer's hand-back while scanning the session transcript; its C1, C3, and W2 predate that, and W3 may be primed. The lead re-ran each finding before changing the plan.
  **Held and applied**: the `0` retention value (both reviewers), now `3650`, done as 0a; the instrument change stated as decided (C2), now the user's ruling with its gate; the deny-list (C3, proposer 4), now D4's allowlist by declared scope; subagent files (W1); versioned copies (W2, proposer 2); the deadline set by the wrong subject (W3); the calibration set measuring a different construct (W4, proposer 5), replaced by A1 and A2 on fist with the user's labels; the partial frame (W5); the release hold on fist's adoption (W6, O2); the report root and slice order (W7, D2, D7); the hub's transcripts kept off home storage (W8); synthetic fixtures and the NAS name (W9, 0c); the counter's calibration (W10); `Evidence:` lines (W11); kill lines that abandon (S2); kappa with a minimum count of positives (S3, proposer 6); a drift measure that can fail (S4); scorer blinding (S5); and S6 to S9, S11 to S16.
  **Refuted on re-run**: C3's "`daily-weather` has no repo on disk". The repo is `~/projects/github/daily_weather` and declares `scope: personal`; its transcript directory encodes `_` as `-`. W4's count of rows naming a message to the user re-ran as 8, not 7; the finding stands.
  **Declined**: `proposer`'s cut of Approaches C and D, since the format asks for a bold alternative and D was the user's own option (both now shorter); Approach E as the plan's shape, by the user's ruling. Found by the lead on re-run: a quarantine keyed to the whole private-terms list would hold back most personal data once the NAS name joined the list (O6).
  **The user's rulings**, asked through the harness's question tool; each answer is the option label chosen: (1) retention, "Set 3650 now (Recommended)"; (2) MOE 1's instrument, "Yes, once the scorer passes A1 (Recommended)"; (3) the repository, "Now; scorer stays a spike (Recommended)"; (4) the NAS name, "Add it and redact forward (Recommended)".
  **The lead's errors the round caught**: a WebFetch summary quoted as the docs on `0`; the exclusion said to skip "by name" (it matches a relative path, a correction the 2026-10-04 Appendix A had already made); "OVERWATCH's Terrain" for a row of its Assumptions; three degenerate cases, not four; slice 3's contents; fist's first sessions "gone through age-out"; and the OVERWATCH entry's instrument change stated as decided.
