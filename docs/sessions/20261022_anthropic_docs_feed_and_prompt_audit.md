# Session: The Anthropic Docs Feed Question, the Hook's Silent Warning, and a Prompt Audit Applied

**Date**: 2026-10-22, finished after midnight on 2026-10-23 (on Nidhogg)
**Branch**: main
**Tags**: #session #doctrine #hooks #prompt-audit #propagation #complete
**Documents**: [docs/tasks.md](../tasks.md), [docs/gaps.md](../gaps.md), [CLAUDE.md](../../CLAUDE.md), [.claude/hooks/post-tool-shift-left-audit.sh](../../.claude/hooks/post-tool-shift-left-audit.sh), [.claude/skills/shift-left-testing/ENFORCEMENT.md](../../.claude/skills/shift-left-testing/ENFORCEMENT.md), [docs/plans/20261022_hook_channel_and_prompt_audit_entries_draft.md](../plans/20261022_hook_channel_and_prompt_audit_entries_draft.md)
**References**: [20261022_anthropic_docs_inventory.md](../reviews/20261022_anthropic_docs_inventory.md), [20261022_anthropic_docs_feed_proposer.md](../reviews/20261022_anthropic_docs_feed_proposer.md), [20261022_anthropic_docs_feed_review.md](../reviews/20261022_anthropic_docs_feed_review.md), [20261022_prompt_audit_hub.md](../reviews/20261022_prompt_audit_hub.md), [20261022_hook_channel_and_audit_application_gate.md](../reviews/20261022_hook_channel_and_audit_application_gate.md), [20260927_schelling_point_bootstrap.md](20260927_schelling_point_bootstrap.md)
**Follows**: [20261006_agent_eval_catchup_and_dispatch.md](20261006_agent_eval_catchup_and_dispatch.md)

---

## Summary

The user asked whether the hub needs a standing connection to Anthropic's Claude Code guidance, probably through paperboy triggered daily from daily_weather, and whether that guidance would improve the hub's work. Four agents answered: a docs inventory with measured cadence, the proposer, and two code-reviewer rounds. The guidance moves (both tracked pages changed substantively in every monthly interval from August to October), Anthropic publishes no feed, and the right carrier is a small hub-side register of source hashes read at `/session-start` with a scheduled check recording first-seen. paperboy and daily_weather stay out: one emits podcast briefings and has lapsed since July, the other is a family-facing service with a canary and a deploy gate.

The first return came without any feed. Measured against the docs as they stand, the hub carried three defects that ship to about 20 repos: the audit hook's warning went to stderr, which Claude never sees from a hook that exits 0, so the enforcement gradient's deterministic layer had warned nobody since 2026-05-19; `/session-end` Step 6 still taught the branching rule retired on 2026-06-28; the ADR skill's next-number command printed the format template. Anthropic's prompt-audit procedure over the hub's 29 instruction files found 20 findings and proposed 29 hunks. The user, leaving for the night, directed all of it: the hook now sends its warning as JSON `additionalContext` plus `systemMessage`, observed live under Claude Code 2.1.309; all 29 hunks are applied; two doctrine entries are drafted for the user's go. Six decisions are deferred to the user, listed below.

| Metric | Value |
|---|---|
| Hub tests, start / end | 545 / 566 |
| Agents deployed | 5: claude-code-guide, proposer, code-reviewer (audit), code-reviewer (challenge), code-reviewer (gate) |
| Docs pages with substantive text changes, monthly capture pairs Aug to Oct | 6 of 6, both pages tracked |
| Prompt audit findings / hunks proposed / hunks applied | 20 / 29 / 29 |
| Gate review of the hook and the application | GO-WITH-FIXES: 0 Critical, 4 Warning, 6 Suggestion; all four warnings fixed the same night |
| Hub commits this session, before this doc | 9 |
| `CLAUDE.md` lines, start / end | 218 / 213 |

---

## Work Completed

### 1. Session start, and a pull that needed merging

The pull was refused by uncommitted edits: the hallmark (2026-10-13) and urd (2026-10-18) bootstraps had left roster lines, a playbook note, and a skills-tree entry here without a hub commit, while two commits from the Windows side (the 2026-09-27 schelling-point bootstrap record) touched the same roster line. An autostash fast-forwarded the branch and conflicted on one line in each of two files; both were merged by union in date order and committed (`2d673db`). Gap G8's Nidhogg half was measured in passing: the user setting holds `cleanupPeriodDays` 3650 and stx-server's transcript dated 2026-09-07 is present at 45 days old. Two of the six tasks the pull brought in were already overtaken (the hook's `src.` prefix, fixed 2026-10-06; the "unpublished `fee9d11`" clone, now an ancestor of `main`) and are closed.

### 2. The docs feed question

The claude-code-guide agent inventoried ten Claude Code docs pages that serve Markdown, an `llms.txt` index, a sitemap whose `lastmod` proved to be a build stamp (all ten pages stamped within two days, three with one identical timestamp), no RSS or Atom feed anywhere on anthropic.com, and the engineering best-practices post folded into the docs. Wayback digest counts overcount, so the cadence was settled by text diffs of monthly captures: the best-practices page changed three times (auto mode as the starting permission mode; a `dontAsk` batch example) and the memory page three times (AGENTS.md support and a 200-line `CLAUDE.md` ceiling in early October). Claude Code itself released 0.85 times a day over its last 100 releases, so the changelog is not a register source.

The proposer compared fifteen current recommendations with the hub's state and proposed five carriers; the code-reviewer returned GO-WITH-FIXES with two Criticals (reviewer time is the real run cost, 0.3 to 4 hours a month at the measured cadence, and reviewer time is what lapsed paperboy; a pull at session start cannot measure its own delay, since hub session gaps run to 52 days) and one missing approach (a scheduled GitHub Actions check in the hub that fails on a hash change, so GitHub mails the user and the run history records first-seen). The user accepted the direction and the hook channel recommendation. The register is a P1 task; the scheduled check waits on the `.github` decision below.

### 3. The hook's warning, test-first and observed

Four red tests (`58d1989`): the `MISSING_TEST` path prints one JSON object with `hookSpecificOutput.hookEventName` `PostToolUse`, `additionalContext` and `systemMessage`, writes nothing to stderr; the OK path prints nothing. The hook (`16f664e`, `[gate]`) builds the object with `jq`; exit 0 on every path is unchanged; `ENFORCEMENT.md` step 5 and its exit paragraph say what the channel is and why. Then scratch repos under `claude -p` 2.1.309, three arms: the new hook's warning came back quoted verbatim by the agent; the old hook's came back as `NONE`; an exit-2 variant came back framed as `PostToolUse:Write hook blocking error from command:` on a write that had succeeded. A `stream-json` run showed the `systemMessage` as a `system` event of subtype `informational`, level `notice`. The gate review asked for three more pins (`eecc7de`): silent without `jq`, parseable with a quote or newline in the path, silent for a feature-named partner. A backslash in a Linux path silences the audit, a pre-existing effect of the Windows normalization, filed as a suggestion.

### 4. The prompt audit, applied

The code-reviewer ran the prompt-audit guide (the same procedure as `/doctor prompt-audit`, which shipped in Claude Code 2.1.283 and the hub had not run) over `CLAUDE.md`, 5 agents, 6 commands, 4 teams and 13 `SKILL.md` files against Claude Fable 5.1, with `git blame` on every line it proposed to change. Eight high-confidence findings were facts the repository had outgrown; six medium ones were dated phrasings; five low ones are flagged, not edited. The 29 hunks applied cleanly once the patch was split per file (27 by `git apply --recount --unidiff-zero`, two in `session-end.md` by hand). The three `pcc.md` hunks landed alone (`e744d64`, `[gate]`); the other 26 in `4d4b476`. The gate review confirmed every hunk landed once in 21 of 21 files, the `pcc.md` bash blocks are byte-identical, and the six em dashes on added lines are list-item label dashes in the files' existing style. A strict-YAML parse of the skill frontmatters, now the only home of each skill's version, failed on two unquoted descriptions; a pin test went in red (`10546c9`) and the two descriptions were quoted (`aa3fabb`).

### 5. Records for tomorrow

Entries H (the hook, two corrections) and P (the audit bundle) are drafted in `docs/plans/20261022_hook_channel_and_prompt_audit_entries_draft.md`, outside the file the propagation script reads, with four open items. Gap G12 restates G8 with its Nidhogg half closed; G13 names Anthropic guidance drift with the register as its collector. The task list's Focus leads with the deferred decisions; five tasks were added and three closed.

---

## Decisions Deferred to the User

Each was mine to make under the night's authority, and each changes something you own, so each waited. The recommendation is the lead's; the decision is yours.

| # | Decision | Options | Recommendation |
|---|---|---|---|
| 1 | Entry H ships before a Windows Git Bash run of the new hook | Ship with the caveat in the entry; or hold H until the next work-terminal or Windows session runs the hook once | Ship. The worst case on a box without `jq` is the old silence, which every consumer already has. |
| 2 | Entry P's rows 7 and 8 touch `shift-left-testing` and `verifying-claims`, both under the OVERWATCH hold | Keep the rows as PATCH (delete a footer, copy nothing); or move them into the OVERWATCH release draft | Keep as PATCH; a consumer that follows them copies no held content. |
| 3 | A `.github` directory in the hub for the scheduled docs check | Yes, as the register's first-seen collector and the hub's first workflow; or no, pull-only at session start | Yes. It is the one carrier that runs with every workstation off and lands where doctrine is written. |
| 4 | `CLAUDE.md` below the docs' 200-line guideline (213 now) | Move the 16-line Figure Style kernel to its skill; or cut the Project Structure block to a pointer; or leave it | Cut the structure block to a pointer at `.claude/README.md` and the docs tree; the figure kernel is your doctrine and stays. |
| 5 | paperboy's own cadence and its year-old model pins | Give it its own daily schedule off the home server; or leave it manual; either way repin the models | Repin now; schedule on paperboy's merits, not as the watcher. |
| 6 | The prompt audit's five Low flags, L1 to L5 | Each is drop, keep, or reword | Drop L1's paper citation; keep L3's dated snapshot (it carries its date); the other three are judgment calls I did not want to make for you. |
| 7 | Whether the user-facing `systemMessage` ships with the hook (gate review D1) | Keep both channels; or `additionalContext` alone | Keep both. The human who escalates under `ENFORCEMENT.md` never sees the agent's context. |

Two things I did that you may want to reverse: nine commits landed on `main` before this doc, and all 29 audit hunks were applied as you asked, with no hunk held back. Everything restores from git.

---

## Claims

| Claim | State | Evidence |
|---|---|---|
| The hub suite passes on `aa3fabb` | tested | `.venv/bin/pytest -q` after the last code change: `566 passed, 1 warning in 5.48s` |
| The hook's new tests were red before the change | tested | `.venv/bin/pytest -q tests/unit/test_shift_left_hook.py` at `58d1989`: `3 failed, 13 passed`; the gate review re-ran it in a worktree with the same result |
| The agent receives the new hook's warning and not the old hook's | observed | `claude -p` 2.1.309 in two scratch repos: new arm replied `HOOK_CONTEXT=[shift-left-audit] No test partner found for ...` with all five lines; old arm replied `HOOK_CONTEXT=NONE`; both logs hold one `MISSING_TEST` |
| Exit 2 on PostToolUse reaches the agent as a blocking error on a successful write | observed | third arm, old hook plus `exit 2`: `HOOK_CONTEXT=PostToolUse:Write hook blocking error from command: ...` and the probe file exists |
| `systemMessage` reaches the user channel | observed | `--output-format stream-json`: one `{"type":"system","subtype":"informational","level":"notice","content":"PostToolUse:Write says: [shift-left-audit] No test partner for probe.py; ..."}` |
| Claude never sees stderr from a hook that exits 0 | observed | the hooks reference, fetched 2026-10-22, line 816: "Claude never sees stderr from a hook that exits 0 ... To surface a warning to Claude from a PostToolUse ... hook, exit 2 instead" |
| All 29 audit hunks are applied, each once, nothing outside them changed | observed | the gate review's per-file comparison of `git diff 0c1fbdd 4d4b476` against the report: 21 of 21 files; my own: `git apply --check` per section, 27 of 27 applied, 2 by hand |
| The `pcc.md` gate commit changed comment lines only | observed | the gate review: 8 bash blocks, 6 byte-identical, 2 differ in comment lines; `tests/unit/test_pcc_*.py` 32 passed |
| The best-practices and memory pages changed substantively in every monthly interval Aug to Oct | observed | `docs/reviews/20261022_anthropic_docs_inventory.md` section 6: six capture pairs, 6 to 138 blocks added each, none build noise |
| Anthropic publishes no RSS or Atom feed | observed | `curl -sI` on `/news/rss.xml`, `/engineering/rss.xml`, `/feed.xml`: 404, 404, 404 |
| G8's Nidhogg half holds | observed | `grep cleanupPeriodDays ~/.claude/settings.json` → `3650`; `ls -l` on the stx-server transcript directory lists one file dated 2026-09-07 among 10 |
| The gap register's test passes after G12 and G13 | tested | `.venv/bin/pytest -q tests/unit/test_gaps.py` → `31 passed` |
| No private term in the files this session wrote | observed | the check 7 block over the index, and the same list over the untracked reports, the drafts, the task list diff and the register: 0 hits each; the gate review: 0 hits in added lines, messages, file names |
| Reference integrity is clean with this doc present | tested | check 5 file pass after this doc was written: 0 MISSING over 56 paths; directory pass: no output. The run before this doc existed printed 3 MISSING, all planned paths in the task list, since reworded |
| The suite stood at 545 at session start | observed, 2026-10-22 | `.venv/bin/pytest -q` at `2750d33`: `545 passed, 1 warning in 5.35s` |

Overclaims the user caught this session: 0

Overclaims a reviewer caught this session: 1

The one: the `4d4b476` commit message says the `IMPORTANT` booster "states its reason", while hunk 9 removed the marker and stated the reason in plain prose; the file is right, the message imprecise. Two claims were unverified when first written and proved true the same night (exit 2 renders as a hook error; `systemMessage` reaches the user); their rows above show the observation. One count was wrong for a minute (a changelog line said 20 hook tests where 19 exist) and was fixed before anything relied on it.

---

## Key Decisions

| Decision | By | Rationale |
|---|---|---|
| A hub-side register, not paperboy or daily_weather, watches Anthropic's docs | the user, on the proposer's and the reviewer's rounds | The output must land where doctrine is written; both other carriers fail that test and one has a canary gate |
| The hook's warning travels as JSON at exit 0, not exit 2 | the user, on the reviewer's recommendation; confirmed by the exit-2 arm | Exit 2 frames a successful write as a blocking error; JSON keeps the run a success and reaches both the agent and the user |
| Apply all 29 audit hunks | the user | "all" |
| Entries H and P wait as drafts in `docs/plans/` | the lead | Four open items are the user's; the script reads only `docs/doctrine-updates.md` |
| Sync the pull with an autostash and merge the two conflicted lines by union | the lead | Both sides appended independent roster entries; nothing was lost, and the result stayed uncommitted for review |

---

## Pillar Compliance

| Pillar | Status | Notes |
|---|---|---|
| **Simplicity First** | PASS | The hook change is one branch and one `jq` call; the register is deferred to its own task rather than built tonight |
| **Shift-Left Testing** | PASS | Every behavior change went red first: 3 hook tests at `58d1989`, 2 frontmatter cases at `10546c9`. The three pins at `eecc7de` are characterization, green on arrival, and say so |
| **Config-Driven** | PASS | Nothing hardcoded; the register's sources will live in a YAML file per the task |

---

## Lessons

1. **A warning nobody reads is a log line.** Layer 4 of the enforcement gradient claimed to warn the agent for five months and reached a log file only. The claim was never tested against the harness; one read of the reference and one `claude -p` run settled it.
2. **A docs snapshot rots faster than an annual re-check.** `SKILLS_FRAMEWORK.md`'s field list was copied in December and is four of seventeen fields now; the register replaces the calendar.
3. **A sitemap `lastmod` is a build stamp.** Ten pages stamped within two days, three with the same second; only a text diff of captures measured the cadence.
4. **The cheapest carrier is the one that already lands where the reader looks.** paperboy would turn a docs diff into a podcast; daily_weather would put a hub failure inside a family service.
5. **Split a multi-hunk patch per file before `git apply`.** The whole patch failed on the first file with overlapping hunks; the same 27 sections applied one at a time.

---

## Commits

| Hash | Subject |
|---|---|
| `2d673db` | [doc] Roster: hallmark and urd; the playbook-drift task gains hallmark's seven corrections; the picture skill joins the skills tree |
| `0c1fbdd` | [doc] Anthropic docs feed: the inventory with measured cadence, the proposal, its review, and the prompt audit of the hub's instruction files |
| `58d1989` | [test] The audit hook's warning must reach the agent as JSON additionalContext, not stderr |
| `16f664e` | [gate] The audit hook's warning travels as JSON additionalContext and systemMessage, not stderr |
| `e744d64` | [gate] /pcc checks 5 and 7 keep their reasons and drop the incident archaeology |
| `4d4b476` | [doc] Apply the 2026-10-22 prompt audit: 26 hunks across 20 instruction files |
| `eecc7de` | [test] Three pins on the audit hook's stdout |
| `10546c9` | [test] Every skill's frontmatter parses as strict YAML and carries name, description, version |
| `aa3fabb` | [doc] Two skill descriptions are quoted so their frontmatter is strict YAML |
| this doc's commit | [doc] Session 2026-10-22: the register, the gate review, the drafts, G12 and G13, the Focus, and this record |

---

## Next Steps

1. The user rules on the seven deferred decisions above (Focus step 1).
2. Read the 2026-10-06 cycle's consumption records, then the cycle that carries entries H and P (Focus step 2).
3. Build the register, test-first, so G13 has its collector (Focus step 3); the scheduled check follows decision 3.
4. CONOP SEXTANT: 0b, O6, approval (Focus step 4). CONOP DISPATCH: the O1 to O9 rulings (Focus step 5).
5. On the next work-terminal visit: the Windows run of the hook, G12's retention check, the G6 and G11 dry run, OVERWATCH Wave 0 (Focus step 6).
