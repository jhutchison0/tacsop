# Review: Anthropic docs feed proposal

**Author**: code-reviewer
**Date**: 2026-10-22
**Type**: Code review (proposal challenge round)

**Verdict: GO-WITH-FIXES.** The direction holds (catch up by hand, then a hub-side register read at `/session-start`, and keep paperboy and daily_weather out of it), but the comparison table omits the dominant recurring cost, neither falsifier can fire as written, and the register as sketched does not meet the hub's picture doctrine.

Subject: `docs/reviews/20261022_anthropic_docs_feed_proposer.md`. Every docs quotation below comes from the saved fetches under the session scratchpad's `probe/` directory, taken 2026-10-22 21:01 UTC, treated as data. Line numbers for docs pages refer to those `.md.out` files. I ran no live fetch, no `/doctor prompt-audit`, and no hook experiment. I did not read `.claude/settings.json`. I read two files in daily_weather and three in paperboy, and wrote nothing anywhere but this file.

| Severity | Count |
|---|---|
| Critical | 2 |
| Warning | 8 |
| Suggestion | 6 |

## Findings

### Critical

**C1. The comparison table charges Approach A no run cost and charges E 2 hours per review, which inverts the two.** Report lines 122 to 130 and 163.

What I verified: the parallel inventory (`docs_inventory.md` section 6, a record I did not re-run) diffed four monthly captures of the best-practices and memory pages. All six consecutive pairs changed instructions Claude follows. The register flags each such change, and a person then reads the diff and decides. The table counts that time for E and not for A.

| Quantity | Value | Kind |
|---|---|---|
| Monthly capture pairs with a substantive change, 2 pages | 6 of 6 | record, inventory section 6 |
| Text blocks added plus removed per pair | 12 to 166 | record, inventory section 6 |
| Minutes to read one flagged diff and decide | 10 to 40 | estimate, basis the block counts |
| Flags per month across 6 pages | 2 to 6 | estimate, basis 2 of 6 pages measured monthly |
| Reviewer hours per month, Approach A | 0.3 to 4 | estimate, product of the two rows above |
| Reviewer hours per month, Approach E | 0.7 | report line 116, 2 hours a quarter |

The observation that would prove the estimate wrong: fewer than two flags a month over the register's first three months.

Why it matters: the choice between A and E rests on this column, and reviewer time is the cost that lapsed paperboy. Its output directory was last written 2026-07-22 (observed, `ls -lt` on its `output/`).

Fix: add a "reviewer hours per month" column with a range and basis, and change line 163 to say run cost is machine cost only.

**C2. Neither falsifier can fire as written, and the pull-only design cannot measure the delay the user asked about.** Report lines 165 to 169.

Falsifier 1 says the build fails if fewer than two of six pages change by 2026-12-17. The inventory already measured both tracked pages changing in each of the last three monthly intervals. Eight weeks will flag at least two pages with near certainty, so the count cannot falsify anything. The relevance half (three reviews in a row closed as no doctrine change) is the only live part. Keep that and drop the count.

Falsifier 2 says the pull model fails if the last-review age exceeds 14 days on two occasions "without anyone acting". Measured hub session gaps, from the dates of `docs/sessions/*.md` plus today:

| Quantity | Value |
|---|---|
| Session dates on disk | 24 |
| Intervals, including newest doc to today | 24 |
| Intervals of 7 days or fewer | 17 |
| Intervals over 14 days | 6 |
| Longest interval, days | 52 |
| Newest session doc (2026-10-06) to today, days | 16 |

A quarter of session starts will show an age over 14 days. If "acting" means reviewing at that session, the step itself prompts it, so the falsifier never fires. If "acting" means writing a doctrine entry, two irrelevant changes fire it. Either way it does not measure the quantity that matters, the days from publish to review, because a pull-only register records first-seen as the session date.

Does the delay matter? Only up to the next hub session. A docs change becomes doctrine when a person writes an entry, and that is hub work (report line 14, which I agree with). Today's baseline is the December 2025 snapshot the report cites, about 10 months. Approach A alone cuts that to the session gap: most often under a week, a quarter of the time over two weeks, once 52 days. A push shortens it further only if it makes the user open a hub session sooner. That is a real benefit for the user's stated concern, and it costs little (W3).

Fix: record first-seen per change from a daily collector, and restate falsifier 2 as a measured quantity: "if the median first-seen-to-reviewed delay over the first six flagged changes exceeds 21 days, add an inbox notification." State in the report that pull-only A cannot measure its own delay.

### Warning

**W1. Approach A's register does not meet the picture doctrine.** Report lines 71 to 79 against `.claude/skills/maintaining-the-common-operating-picture/SKILL.md` rules 2, 4, 5 and 8.

As sketched, a row carries a URL, the reviewed hash, a review date and a verdict. Missing: the collector; the measurement as a thing distinct from the review (last fetched hash, fetch time, HTTP status); the universe (which pages it enumerates, and that it is blind to pages `llms.txt` does not list, to anthropic.com posts, and to rendered HTML); motion and surprise; supersede in place (line 73's "stamps the new hash" is an overwrite); the two-shape output so an offline session renders `unchecked` rather than nothing; and a gap-register row pinned by a test. The schema that satisfies the rules:

```yaml
# docs/anthropic-sources.yaml. reviews: hand-edited through --accept. last_fetch: written by the collector only.
collector: scripts/docs_watch.py
universe: the urls below plus llms.txt; blind to pages llms.txt omits, to anthropic.com posts, and to rendered HTML
sources:
  - id: memory
    url: https://code.claude.com/docs/en/memory.md
    motion: constant until a change event
    surprise: hash differs, fetch fails, status not 200, or a redirect
    reviews:                       # append-only; the newest unmarked row is the holding
      - hash: sha256:...
        reviewed_at: 2026-10-22
        reviewer: <git user.name>
        verdict: "doctrine entry 2026-10-22" or "no doctrine change: <why>"
        status: current            # or: superseded 2026-11-03 by sha256:...
    last_fetch:                    # the measurement
      hash: sha256:...
      fetched_at: 2026-10-22T21:01:00Z
      status: 200
      bytes: 54043
      first_seen: 2026-10-22       # first fetch that returned this hash; meaningful only with a daily collector
```

Output contract, one line per source: `checked id=memory age=16d fetched=2026-10-22T21:01Z verdict=unchanged`, or `verdict=changed first_seen=...`, or `unchecked id=memory reason=offline`. Add a `docs/gaps.md` row ("which guidance pages changed since the hub last reviewed them", collector the script, decision blocked "whether a doctrine entry is due this session") and a test that fails when the script or the row disappears, per the skill's "For a probe" procedure.

**W2. The changelog as a register source will flag at every session.** Report line 156.

Re-run: 57 of the 429 dated versions in `changelog.md.out` fall in the last 60 days, about one a day. A page hash therefore changes between any two sessions, the reviewer stamps it every time, and the stamp becomes the decorative mark the skill warns about. Fix: store the newest version string as the value and show the versions added since review; for the doctrine trigger, run the proposer's keyword parse (memory, hooks, skills, agents, settings) over the new sections and print the count. Or drop the page and rely on `/release-notes` in the CLI (inventory section 4) plus the releases Atom feed.

**W3. A missing approach: a daily scheduled run inside the hub's own GitHub repository.**

The user asked for a daily call so that an update is never missed. The report answers with pull-only A and defers push to a fallback. A GitHub Actions `schedule` workflow in the hub, running the same script in check mode, fails the run when any source hash differs from its reviewed hash, and GitHub mails the failure. It runs when every workstation is off, touches no home server, and lands in the repo where doctrine is written. Its run history is the collector for first-seen (C2). The hub has no `.github` directory today (observed), so this would be its first workflow; `.claude/skills/shift-left-testing/CI.md` already documents the pattern. Whether the hub gets a workflow is the user's policy call. Cost: 1 to 2 hours beyond A, an estimate, basis the script already existing. Blast radius: none. Caveat: a failing run keeps failing until the change is reviewed, which nags and could hide a second change behind the first; acceptable because the register lists each source on its own line.

**W4. Cost figures stated as measurements.** Report lines 76, 96, 107, 116, 124 to 128 and 163.

"About 5 hours" for A, "about 1 hour" for D, "about 2 hours per review" for E, "7 hours in total", and "Run cost is zero" carry no range and no basis. Line 130 marks only B and C as judgment, and the claims table at line 196 carries only B and C. Fix: ranges with a basis for all five, and one claims row covering them.

**W5. The summary overclaims the hook finding.** Report lines 11 and 138.

Line 11: "The audit hook's warning never reaches the agent under the current hooks reference." Line 138: "the current reference says its warning is never seen." The claims table at line 190 marks the live behavior UNVERIFIED. The docs rule is observed; the behavior is not. Fix: "per the hooks reference, unverified by experiment" in both places.

**W6. The premise check and open question 1 are now answered, and Approach E's miss risk rests on the old answer.** Report lines 16, 115 and 173.

Inventory section 6: six consecutive monthly capture pairs, all six substantive, 7 to 28 blocks added per pair on best-practices and 20 to 138 on memory. Line 115's "acceptable if the guidance pages change slowly, which is unmeasured" is measured false. Fix: replace line 16's premise, close open question 1 with the inventory's numbers, and re-rate E.

**W7. `ENFORCEMENT.md:32` and the hook header are false under the current docs, with two precisions the report lacks.** Ruling requested by the lead.

- `.claude/skills/shift-left-testing/ENFORCEMENT.md:32` says the stderr warning is "surfaced back to the agent in the tool result". The script exits 0 on the warning path (`.claude/hooks/post-tool-shift-left-audit.sh:97-110`). `hooks.md.out:816`: "Claude never sees stderr from a hook that exits 0." False under the current docs.
- Header lines 8 to 10 say a non-zero exit "can suppress or fail the tool call". `hooks.md.out:993`: PostToolUse exit 2 "Shows stderr to Claude; the tool already ran". `hooks.md.out:792`: any other non-zero exit is a non-blocking error carrying the first line of stderr. False under the current docs.
- Precision 1: the warning is five lines (script lines 97 to 103), not the "one-line warning" line 32 describes.
- Precision 2: `tests/unit/test_shift_left_hook.py:35` asserts exit 0 on every path and nothing about stderr or stdout, so the "warns" half of layer 4 has never been tested.

Fix for line 32: "writes a warning to stderr, which reaches the debug log only; Claude never sees stderr from a hook that exits 0 (hooks reference)." Fix for header lines 8 to 10: "exit 0 in all paths, so the hook never renders as a hook error; on PostToolUse no exit code can undo the tool call."

**W8. The daily_weather claim is half right.** Report line 87.

"Its container image carries no app code and no Claude CLI." `deploy/Dockerfile` lines 13 to 16 copy `src/`, `config/` and `deploy/` and install the package, so that image does carry app code. `deploy/README.md` section 7 runs a bare Debian image with a bind mount and says "The image carries no app code"; that is the home server's App. Neither carries a Claude CLI (grep for claude, npm and node in the Dockerfile: no hits). The crontab-restart claim holds (`deploy/README.md:7`), the canary rule holds (line 35), and the deploy script's CI check is at line 23, not 7. Fix: "the home server's App image carries no app code; the Dockerfile image does; neither carries a Claude CLI."

### Suggestion

**S1. Take the diff base from the Wayback Machine.** Report line 79. The weak point (a fresh clone can only say "changed") has a cheaper answer than a gitignored snapshot: fetch the capture nearest the reviewed date through the CDX API and diff against it. The inventory did this for eight captures with a small script in the scratchpad. Fall back to the local snapshot when archive.org is down. Nothing is committed either way.

**S2. Treat a redirect or a non-200 as a surprise, not a change.** The inventory found the engineering post redirecting (308) and the platform prompting page moved. A register that hashes whatever the redirect returns will silently track the wrong page.

**S3. Weekly digest: weeks 31 and 36 are both absent, not 31 alone.** Report line 65 and the claims row at 187. Re-run on `llms.txt`: weeks 28, 29, 30, 32, 33, 34, 35, 37 are listed.

**S4. "About 17 fields" for skill frontmatter.** Report line 33. The skills page's frontmatter table has 20 rows (`skills.md.out:399-418`), none named `version`. The claim that `version` is undocumented holds. Put the count in the table and match it.

**S5. `.claude/README.md:72` wording (row 9 holds).** `sub-agents.md.out:356-360` gives the order: the per-invocation parameter, the frontmatter, `CLAUDE_CODE_SUBAGENT_MODEL`, the main model. Lines 362 to 365: a family alias runs on the main conversation's exact model when the main model is in that family. Suggested line: "Agents set to `inherit` use the orchestrator's model. An alias such as `sonnet` is a default: a per-invocation model wins over it, and when the orchestrator already runs that family the agent runs on the orchestrator's exact version. Check with `/tasks`."

**S6. Tag form and precedent.** Report line 159 says the step tags lines `[measured]`. The command's form is `[measured: <command>]` and `[unchecked: <reason>]` (`.claude/commands/session-start.md`, step 5). Step 3.6's upstream-update flag is the precedent for one prominent line that the user decides when to act on.

## The hook question

Should the audit hook switch to exit 2 so the agent sees its warning? My view: switch the channel, but to exit 0 plus JSON, not to exit 2.

What the docs say about each channel, from `hooks.md.out`:

| Channel | Line | What happens on PostToolUse |
|---|---|---|
| stderr, exit 0 | 816 | Claude never sees it; debug log only |
| stderr, exit 2 | 993, 822 | Claude sees the stderr; the tool already ran; the message is delivered as the block message |
| stderr, exit 2, user side | hooks-guide 1067 | the user sees the block message; the PreToolUse example at 845 to 849 renders as `<Event>:<Tool> hook error: [script]: text`; the PostToolUse rendering is not shown |
| JSON `additionalContext`, exit 0 | 2205, 1104, 1131 | added to Claude's context alongside the tool result as a system reminder, not a chat message; named for "the operation that just ran" |
| JSON `systemMessage`, exit 0 | 1058 | a warning shown to the user |
| JSON that fails to parse, exit 0 | 791, 1038 | non-blocking error notice; stdout must be the JSON object alone |

Three reasons for JSON over exit 2. First, it keeps the invariant that the header, `ENFORCEMENT.md:35` and the test at line 35 all state, so no doctrine text or test flips. Second, exit 2 is the harness's blocking-error channel and renders as a hook error, which labels a successful write as an error; an agent that reads "error" may retry the write or apologize instead of writing a test, while `additionalContext` is the channel the docs name for this purpose. Third, `systemMessage` gives the human the warning that `ENFORCEMENT.md` always promised, where exit 2 gives it only as a red notice. The trade-off accepted: the JSON path depends on stdout parsing, so a stray shell-profile echo downgrades it to a notice without anyone noticing, while exit 2 is one line and cannot be mis-parsed. If the experiment below shows `additionalContext` does not reach the agent on the versions the fleet runs, exit 2 is the fallback, and the docs at line 816 endorse it.

What to test before the change ships to the roster's consumers:

1. **Three-arm experiment** in a throwaway clone under `claude --debug-file`: the current script, an exit-2 variant, and the JSON variant. Write `src/myproject/zz_probe.py` with no test, then ask the agent to quote the last hook message. Record for each arm what the agent, the transcript and the debug log show. This is the proposer's five-minute experiment with two more arms.
2. **Unit tests** in `tests/unit/test_shift_left_hook.py`: keep the exit-0 assertion; add that the warning path prints exactly one JSON object with `hookEventName` set to `PostToolUse` and a non-empty `additionalContext`; that the OK and skip paths print nothing on stdout; and that stdout stays parseable under a shell with a noisy profile.
3. **Version floor.** The docs give no minimum version for PostToolUse `additionalContext`; `classifierContext` on the same event needs 2.1.236 (`hooks.md.out:2208`). Record `claude --version` on each box before relying on it. Older downstream installs are UNVERIFIED.
4. **Windows Git Bash.** The script already normalizes paths for it (lines 25 to 30). Run the JSON arm there, since `jq -n --arg` is the new path.
5. **A behavioral measure after rollout.** In each audit log, the share of `MISSING_TEST` lines followed in the same session by `OK_TEST_EXISTS` for the same file. The hub's log is no baseline (17 lines, 1 `MISSING_TEST`, from a probe file, last written 2026-10-04); take the baseline from the most active downstream.
6. **Propagation.** One doctrine entry carrying the script as template-copy, with `ENFORCEMENT.md:32` and header lines 8 to 10 rewritten in the same entry. The settings snippet is unchanged because the matcher is untouched.

## Claims

| Claim | State | Evidence |
|---|---|---|
| The hooks reference says Claude never sees stderr from a hook that exits 0, that PostToolUse exit 2 shows stderr to Claude after the tool ran, and that `additionalContext` is added alongside the tool result. | observed | `sed -n 816p; sed -n 993p; sed -n 2205p` on `hooks.md.out`: "Claude never sees stderr from a hook that exits 0"; "`PostToolUse` \| No \| Shows stderr to Claude; the tool already ran"; "String added to Claude's context alongside the tool result". |
| `ENFORCEMENT.md:32` claims the warning reaches the agent, and the script exits 0 on the warning path. | observed | `sed -n 32p ENFORCEMENT.md` contains "which the harness surfaces back to the agent in the tool result"; script lines 97 to 110 end in `exit 0`. |
| Whether a live agent sees the warning today. | UNVERIFIED: no experiment run; I may not write under `src/`, and the probe needs a Claude session. | |
| `/doctor prompt-audit` was added under 2.1.283, dated September 25, 2026. | observed | `changelog.md.out`: line 2084 `**2.1.283**`, line 2086 `September 25, 2026`, line 2094 "Added `/doctor prompt-audit`". |
| 57 releases in the last 60 days; newest 2.1.309 dated 2026-10-22. | observed | Python parse of `changelog.md.out` bold version lines and the date line below each: 429 dated versions, newest `('2.1.309', 2026-10-22)`, `last60 57`. |
| `CLAUDE.md` is 218 lines; its tree lists 3 agents, 3 teams and 5 commands; disk holds 5, 4 and 6. | observed | `wc -l CLAUDE.md` printed 218; `sed -n 140,177p` shows three agent files, three team files, "session-start, session-end, pcc, pci, task"; `ls .claude/agents .claude/teams .claude/commands \| wc -l` printed 5, 4, 6. |
| The memory page states the 200-line guideline in the proposer's terms. | observed | `memory.md.out:88`: "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." |
| daily_weather's Dockerfile carries no Claude CLI; its image does carry app code; a crontab change needs an App restart. | observed | `grep -n -i "claude\|npm\|node" deploy/Dockerfile` printed nothing; Dockerfile lines 13 to 16 `COPY src/ src/` and `uv pip install -e .`; `deploy/README.md:7` "a crontab change needs the App restarted, because supercronic reads the file once"; `crontab.stage` has 3 non-comment lines. |
| Hub session gaps: 24 intervals, 17 of 7 days or fewer, 6 over 14 days, longest 52, newest doc to today 16. | observed | `ls docs/sessions \| grep -oE '^[0-9]{8}' \| sort -u` piped to a Python date-diff with today appended: `max 52 gaps>14: 6 gaps>7: 7 newest to today 16`. |
| The hub has no GitHub Actions workflow. | observed | `ls .github` printed "No such file or directory". |
| The hook's test suite asserts exit 0 on every path and nothing about stderr or stdout. | observed | `grep -n "returncode\|stderr\|stdout" tests/unit/test_shift_left_hook.py` printed one line, 35: `assert result.returncode == 0`. |
| The skills page lists 20 frontmatter fields and no `version`. | observed | `grep -n "^\| \`[a-z_-]*\` \|" skills.md.out` rows 399 to 418; `grep -n "\`version\`"` printed nothing. |
| The sub-agents page's resolution order is parameter, frontmatter, env var, main model, and a same-family alias runs on the main model's exact version. | observed | `sed -n 356,365p sub-agents.md.out`. |
| paperboy's output was last written 2026-07-22 and its pinned models are `claude-sonnet-4-20250514` and `claude-haiku-4-5-20251001`. | observed | `ls -lt --time-style=long-iso output/` newest `2026-07-22 08:30 briefings`; `sed -n 99,103p config/paperboy.yaml`. |
| The weekly digest index lists weeks 28, 29, 30, 32, 33, 34, 35, 37. | observed | `grep -o "Week [0-9]* · ..." https___code.claude.com_docs_llms.txt.out`. |
| The proposer's report carries no em dash and no private term. | observed | `grep -c` for the U+2014 character printed 0; `grep -c -i -F -f ~/.config/tacsop/private-terms` printed 0, count only. |
| The hub's audit log holds 17 lines, 1 `MISSING_TEST`, last written 2026-10-04. | observed | `wc -l` 17; `grep -c MISSING_TEST` 1; `ls -l --time-style=long-iso` 2026-10-04. |
| Both tracked guidance pages changed substantively in each of the last three monthly intervals. | record, not re-run | `docs_inventory.md` section 6, written this session by the inventory agent from Wayback captures and its own text diff. |
| Reviewer hours per month under Approach A: 0.3 to 4. | estimate | Basis in C1's table; proved wrong by fewer than two flags a month over three months. |
| A hub-side scheduled workflow costs 1 to 2 hours beyond A. | estimate | Basis: the script exists under A; the workflow is a cron trigger plus one check-mode call. |
| The "about 138 of 757 changelog lines" figure (report line 195). | not re-run | Marked crude by the proposer; nothing here rests on it. |
