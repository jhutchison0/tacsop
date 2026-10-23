# Anthropic Docs Feed: Proposer Report

Date: 2026-10-22. Author: proposer. Scope: whether and how the hub should connect to Anthropic's Claude Code guidance, and whether the guidance would improve the hub's work.

## 1. Summary

Connect the hub to Anthropic's docs with a small hub-side register of source hashes, read at `/session-start`, and do not route it through paperboy or daily_weather. The verdict rests on four facts.

1. **The guidance moves, but the pages are stable between changes.** Two fetches of six guidance pages, taken seconds apart, returned identical bytes. A hash against the last-reviewed state therefore works, and it catches up after a missed day. A daily trigger is not needed to avoid missing an update.
2. **The release feed is too noisy for a doctrine trigger.** The Claude Code changelog shows 57 releases in the last 60 days. By a crude parse, about 138 added or changed lines in that window touch memory, hooks, skills, agents or settings. No person reads that daily, and paperboy would turn it into a podcast.
3. **The hub already differs from the docs in ways that cost something.** The audit hook's warning never reaches the agent under the current hooks reference. `CLAUDE.md` is 218 lines against a 200-line target and carries a stale file tree. Anthropic shipped `/doctor prompt-audit` on 2026-09-25, which audits exactly these files and which the hub has not run.
4. **paperboy and daily_weather are the wrong carriers.** paperboy scores research papers by keyword and emits a briefing. daily_weather is a family-facing service with a deploy gate. A doctrine diff fits neither, and a watcher failure would land in the wrong place.

Nothing here turns docs text into doctrine by itself. A docs change becomes hub doctrine only after a person reads it and writes a doctrine entry, so the output must land where that person already looks.

Premise check, "the docs update regularly": true for the product and its changelog, unmeasured for the guidance prose. The changelog's newest entry, version 2.1.309, is dated today. The guidance has demonstrably moved since the hub's December 2025 snapshot, but I did not measure how often. The parallel cadence measurement should settle that.

## 2. Where the hub stands against what Anthropic says now

State key: every row below is **observed** this session, from a fetch of the cited URL and a read of the cited hub file. Where I could not observe the hub side, the row says UNVERIFIED. I did not read `.claude/settings.json`, as instructed.

| # | Recommendation | Hub state | Delta | Does the delta cost us | Evidence |
|---|---|---|---|---|---|
| 1 | Target under 200 lines per `CLAUDE.md`; longer files reduce adherence. [memory](https://code.claude.com/docs/en/memory.md) | `CLAUDE.md` runs 218 lines. | 18 lines over a soft target. | Unknown. The docs claim lower adherence; the hub has no adherence measurement. | `wc -l CLAUDE.md` printed 218. |
| 2 | Exclude file-by-file codebase descriptions and information that changes frequently. [best-practices](https://code.claude.com/docs/en/best-practices.md) | `CLAUDE.md:140-177` is a 38-line file tree. It lists 3 agents, 3 teams and 5 commands. | The tree is wrong. The disk holds 5 agents, 4 teams and 6 commands. | Yes. The tree gives a reader a wrong roster, and the correct table sits 30 lines below it at `CLAUDE.md:204-210`. | `ls .claude/agents .claude/teams .claude/commands` against `CLAUDE.md:165-172`. |
| 3 | Put emphasis such as IMPORTANT on one stubborn line; many emphasized lines stand out less. [best-practices](https://code.claude.com/docs/en/best-practices.md) | One IMPORTANT at `CLAUDE.md:202`. Ten "never", four "must" and sixteen bold lines, mostly in the style kernels. | None on IMPORTANT. The "never" and "must" density is the open question. | Unknown. The changelog says `prompt-audit` flags "prompting patterns written for older models"; the hub has not run it. | `grep -o -i -E 'never|must|IMPORTANT' CLAUDE.md` counts. |
| 4 | `@imports` do not cut context cost. Path-scoped `.claude/rules/` load only for matching files. Move multi-step procedures to skills. [memory](https://code.claude.com/docs/en/memory.md) | `CLAUDE.md` links with plain markdown at lines 8, 12 and 20. There is no `.claude/rules/` directory. | The hub has no path-scoped rules. The shift-left and branching text at `CLAUDE.md:7-20` loads every session. | Unknown. Small in the hub, which has little `src/`. Larger in downstream code repos. | `ls .claude` shows no `rules`. |
| 5 | Subagent `memory: project` is the recommended default scope. [sub-agents](https://code.claude.com/docs/en/sub-agents.md) | All five agents set `memory: project`. Memory lives in `.claude/agent-memory/<name>/`. | None. | No. | `sed -n 1,8p .claude/agents/*.md`; `ls .claude/agent-memory`. |
| 6 | Hooks are deterministic. Exit 0 stderr is never seen by Claude. On PostToolUse, exit 2 shows stderr to Claude although the tool already ran. Other exit codes are non-blocking errors. JSON `additionalContext` also reaches Claude. [hooks-guide](https://code.claude.com/docs/en/hooks-guide.md), [hooks reference](https://code.claude.com/docs/en/hooks.md) | The audit hook always exits 0 and writes its warning to stderr. `ENFORCEMENT.md:32` says the harness surfaces that warning to the agent. The script header at `post-tool-shift-left-audit.sh:8-9` says a non-zero exit "can suppress or fail the tool call". | Two stale beliefs. The warning is probably invisible to the agent. A PostToolUse non-zero exit cannot undo the tool call. | Yes, probably. Layer 4 of the enforcement gradient may be log-only. The log holds 17 lines, one `MISSING_TEST` from a deliberate probe file, last written 2026-10-04. | Docs quoted above. Hub side UNVERIFIED: a five-minute experiment in a scratch repo would show whether the agent sees the warning. |
| 7 | The PostToolUse example uses matcher `Edit\|Write`. [hooks-guide](https://code.claude.com/docs/en/hooks-guide.md) | The script filters `Write\|Edit` itself at `post-tool-shift-left-audit.sh:34-38`. The matcher in `settings.json` is UNVERIFIED. | None visible. The script is safe under any matcher. | No. | Script read. Matcher not read by instruction. |
| 8 | Subagent frontmatter has about 17 fields. Unrecognized names are ignored without an error. [sub-agents](https://code.claude.com/docs/en/sub-agents.md) | Agents use `name`, `description`, `tools`, `model` and `memory`. | None invalid. Unused: `maxTurns`, `effort`, `isolation`, `permissionMode`, `disallowedTools`, `skills`. | No. Not using a field costs nothing until a problem needs it. | First 8 lines of each agent file. |
| 9 | Aliases float; a full model ID pins. Resolution order is the per-invocation parameter, then frontmatter, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the main model. A same-family alias runs on the main model's exact version. [sub-agents](https://code.claude.com/docs/en/sub-agents.md) | Agents use `sonnet`, `haiku` and `inherit`. `.claude/README.md:72` says pinned agents "always use that model regardless of the orchestrator". | The README claim is overstated twice: the per-invocation parameter wins, and a same-family alias follows the main model. | Low. It misleads a person debugging which model ran. The docs name `/tasks` as the check. | `.claude/README.md:72` against the resolution list. |
| 10 | Skill frontmatter has about 17 fields, among them `when_to_use`, `disable-model-invocation`, `paths`, `context`, `hooks` and `metadata`. Outside Claude Code only six fields are accepted, and others fail packaging. [skills](https://code.claude.com/docs/en/skills.md) | `SKILLS_FRAMEWORK.md:62-71` specifies four fields. Twelve of thirteen skills carry `version`, which the docs do not list. | The hub's spec is a snapshot of the December 2025 standard and is behind. | No today, since unknown fields are ignored. Unknown if skills are ever uploaded to claude.ai. | `awk` over skill frontmatter; the docs field table. |
| 11 | Keep `SKILL.md` under 500 lines; description plus `when_to_use` is truncated at 1,536 characters. [skills](https://code.claude.com/docs/en/skills.md) | Longest `SKILL.md` is 189 lines. Longest description line is 556 characters. | None. The hub is ahead on sidecars. | No. | `wc -l`; `awk` on `^description:`. |
| 12 | Use `disable-model-invocation: true` for workflows with side effects, invoked as `/name`. [best-practices](https://code.claude.com/docs/en/best-practices.md) | Side-effect workflows stay as commands. The anti-rule against moving them to auto-triggering skills appears in paperboy's `CONTEXT.md:73`. | The anti-rule's premise is out of date: a flag now removes auto-triggering. | No. Commands still work. Value is a single mechanism instead of two. | Docs example `fix-issue`; no `disable-model-invocation` in the hub. |
| 13 | Settings: commit `.claude/settings.json`; keep `settings.local.json` out of git; deny `.env` reads. [settings](https://code.claude.com/docs/en/settings.md) | `settings.json` is tracked. `.gitignore:57` ignores the local file. Permission contents UNVERIFIED. | None observable. | Unknown. | `git ls-files`; `git check-ignore -v`. |
| 14 | Give Claude a check it can run; show evidence; use a fresh-context reviewer. [best-practices](https://code.claude.com/docs/en/best-practices.md) | `verifying-claims`, `code-reviewer`, and the proposer-then-reviewer debate. | None. The hub is ahead of the docs on evidence lines. | No. | Skill and agent files read. |
| 15 | Facilities with no hub equivalent: `/doctor prompt-audit` since 2026-09-25; Stop hook and `/goal` as completion gates; `SessionStart` with a `compact` matcher; `ConfigChange` hook; `claudeMdExcludes`; `CLAUDE.local.md`; `AGENTS.md`; plugins; scheduled tasks. [memory](https://code.claude.com/docs/en/memory.md), [hooks-guide](https://code.claude.com/docs/en/hooks-guide.md), [changelog](https://code.claude.com/docs/en/changelog.md) | None used. | `prompt-audit` is the one that matches a standing hub need. | Yes for `prompt-audit`: a free audit of the files in rows 1 to 3 goes unused. Unknown for the rest. | Changelog line "Added `/doctor prompt-audit`" under 2.1.283, September 25, 2026. |

## 3. Does the hub contradict the docs, and does it do what the docs advise against

The hub contradicts the docs in four places. None is severe, and all four are cheap.

1. **The audit hook's stated mechanics.** `ENFORCEMENT.md:32` says the stderr warning "surfaces back to the agent in the tool result". The hooks reference says Claude never sees stderr from a hook that exits 0. The same reference says exit 2 on PostToolUse shows stderr to Claude without undoing the tool, which matches the hub's "evidence, not friction" stance. The hook header at `post-tool-shift-left-audit.sh:8-9` also overstates what a non-zero exit does: on PostToolUse the tool has already run, and exit codes other than 0 and 2 are non-blocking errors. The fix is one line in the script plus a test, but first run the five-minute experiment, because I could not observe the agent's side.
2. **`CLAUDE.md` file tree.** The docs advise against file-by-file descriptions and frequently changing information. The tree at `CLAUDE.md:140-177` is both, and it is already wrong (row 2). It also breaks the hub's own Picture Style rule against kept snapshots.
3. **`.claude/README.md:72`.** The "always use that model" claim contradicts the model resolution order (row 9).
4. **`SKILLS_FRAMEWORK.md`.** The file states "Active per Anthropic Skills open standard (December 18, 2025)" and "re-check annually". It copies a field list that the docs have since extended from four fields to about seventeen. Copying the docs' detail is itself the drift source. The docs' own advice is to link to docs instead of restating API detail.

The hub does one thing the docs do not advise, and it is a choice, not an error. `CLAUDE.md:44-59` carries the figure-style kernel, 16 lines, though it applies only when a figure is made. The docs would move it to a skill, and the skill `designing-clear-data-displays` already exists. The user took Tufte's course and made this fleet doctrine on 2026-08-27, so this stays as a decision for the user and not a defect.

Where the hub is ahead: evidence lines, fresh-context review, sidecar progressive disclosure, project-scoped agent memory.

## 4. Approaches for the connection

### Premise facts used below

| Measurement | Value | Source | Taken |
|---|---|---|---|
| Newest Claude Code release | 2.1.309, 2026-10-22 | `code.claude.com/docs/en/changelog.md` | 2026-10-22 |
| Releases in the last 60 days | 57 | same, parsed by version and date | 2026-10-22 |
| Releases per month, March to September 2026 | 20 to 28 | same | 2026-10-22 |
| Added or changed lines in 60 days | about 757, crude parse | same | 2026-10-22 |
| Of those, touching memory, hooks, skills, agents or settings | about 138, crude parse | same | 2026-10-22 |
| Guidance pages fetched twice, seconds apart | 6 of 6 identical by SHA-256 | the six `.md` pages | 2026-10-22 |
| Weekly "What's New" digest, newest entry | week 37, September 7 to 11; week 31 absent | `llms.txt` | 2026-10-22 |
| Claude Code release Atom feed | exists, 10 entries, updated today | `github.com/anthropics/claude-code/releases.atom` | 2026-10-22 |
| Anthropic engineering best-practices post | permanent redirect to the docs page | HTTP 308 | 2026-10-22 |

Three conclusions follow. The weekly digest lags about five weeks and skips a week, so it is not a trigger. The release feed is real but high volume. The guidance pages do not embed timestamps or session noise, so a content hash is a valid change detector. Paperboy's config comment that Anthropic publishes no official feed is correct for the research blog and does not cover this Atom feed.

### Approach A: hub-side register with hashes, read at `/session-start`

A file `docs/anthropic-sources.yaml` lists each source URL with the SHA-256 of the content a person last reviewed, the review date, and a one-line verdict. A small script fetches each source, compares hashes, and prints one line per changed source. `/session-start` runs it as a new step and tags the result `[measured]`. Reviewing means reading the diff, then either writing a doctrine entry or stamping the new hash with a reason.

- **Miss probability.** Low. The comparison is against reviewed state, so a missed day loses nothing. It fails only if no one starts a session for weeks, and the age of the last review is shown at the top.
- **Cost.** About 5 hours to build with tests, nothing to run.
- **Coupling.** None. One script and one YAML file in the hub.
- **Reader.** The person or agent opening a session, who is the same person who writes doctrine entries.
- **Weak point.** The hash says "changed", not "what". A text snapshot is needed for a diff, and the page text should not be committed to a public repo. Keep snapshots in a gitignored directory. A fresh clone can report "changed" and nothing more.

### Approach B: paperboy as the watcher, daily run from daily_weather's crontab

Add the docs pages and the Atom feed to paperboy's sources, run it daily, and have the home server's crontab call it.

- **Miss probability.** Medium. paperboy's output directory was last written 2026-07-22, so the run has already lapsed once. Its selector keeps one paper a day by keyword score, so a docs change competes with ArXiv papers and loses unless its keywords match.
- **Cost.** High. paperboy ingests papers and articles; a page diff needs a new sourcer, a new scorer, and a briefing format that is a doctrine diff, not a podcast script. Its pinned models, `claude-sonnet-4-20250514` and `claude-haiku-4-5-20251001`, are also a year behind and would need a decision.
- **Coupling and blast radius.** Worst of the five. daily_weather's crontab has three lines, and a change needs an App restart in the home server UI, a canary window and a deploy script that checks CI (`deploy/README.md:7`, `:35`). Its container image carries no app code and no Claude CLI, so paperboy would need an API key and its own venv there. A hub watcher failure would sit inside a family-facing service.
- **Reader.** A listener of a podcast, not a doctrine author. The output lands where no one writes doctrine.
- **Merit.** It does solve the separate problem that paperboy runs too rarely. That is a decision about paperboy's own mission and should be made on those grounds.

### Approach C: standalone minimal watcher

A script, run from a user cron on the workstation, hashes the pages daily and writes a notification file.

- **Miss probability.** Medium. A push file that no session reads goes stale. This is the failure mode paperboy already shows.
- **Cost.** About 3 hours, plus a cron entry per machine that must be kept alive.
- **Coupling.** None, but it is a second moving part outside the hub's `/session-start` picture, so its state is invisible to the hub.
- **Reader.** Whoever opens the notification file, which nothing prompts.

Approach A contains C's script. The difference is where the output lands.

### Approach D: Claude Code's own facilities

Two pieces exist. `/doctor prompt-audit` audits the hub's own files against current model behavior, once, on demand. The docs also list scheduled tasks that run in the cloud on a schedule, formerly called routines, at `code.claude.com/docs/en/routines.md`. The `claude-code-guide` agent answers questions from the docs when asked.

- **Miss probability.** High for the guide agent, which has no state and no diff, and which acts only when someone asks. Medium for a scheduled task, which would have the same hash problem as C and a cloud-to-public-repo write path to configure.
- **Cost.** `prompt-audit`: about 1 hour including triage, and that is the best value per hour in this report. Scheduled task: unknown, not evaluated beyond the index entry.
- **Coupling.** None for `prompt-audit`. A scheduled task adds an account-side dependency.
- **Reader.** The person who ran it. Good for a one-time catch-up, unsuited as a standing watch.

### Approach E: manual review on a fixed cadence with a named trigger

Add a gap row for "Anthropic guidance drift", with the collector "quarterly manual review" and the decision it blocks. The trigger is a named calendar date, or any Claude Code major version bump.

- **Miss probability.** High between reviews, and a quarter is long against 20 to 28 releases a month. Acceptable if the guidance pages change slowly, which is unmeasured.
- **Cost.** About 2 hours per review, no build.
- **Coupling.** None.
- **Reader.** The person, by design. It fails the way every calendar reminder fails, quietly.

### Comparison

| Approach | Miss risk | Build hours | Run cost | Blast radius | Output lands where a doctrine author looks |
|---|---|---|---|---|---|
| A hub register | Low | 5 | 0 | Hub only | Yes |
| B paperboy and daily_weather | Medium | 25 or more | API spend | Family service | No |
| C standalone watcher | Medium | 3 | 0 | None | No |
| D `prompt-audit` | n/a, one shot | 1 | 0 | None | Yes, once |
| E manual cadence | High | 0 | 2 per review | None | Yes |

The estimates for B and C are my judgment, not measurements.

## 5. Would the docs actually improve our work

Yes, in three places, and the hub should ignore most of the rest. The evidence comes from sections 2 and 3.

**The three changes with the highest expected value**

1. **Make the shift-left audit visible to the agent, or correct the claim.** The hub's strongest enforcement story rests on layer 4, and the current reference says its warning is never seen. Switching to exit 2 or `additionalContext` fits the "evidence, not friction" stance, because PostToolUse cannot block. Cost: about 1 hour with the scratch experiment. Fan-out: every downstream repo that adopted the hook. Not a decision I can make for the user, because it changes how often agents see a warning.
2. **Run `/doctor prompt-audit`, prune `CLAUDE.md` below 200 lines, and delete or regenerate the file tree.** The tree is already wrong, and the audit exists for this class of defect. Cost: about 2 hours including a doctrine entry. Fan-out: every downstream `CLAUDE.md` that copied the tree.
3. **Replace `SKILLS_FRAMEWORK.md`'s copied field list with a link plus the hub's four required fields.** This stops the hub's most-cited Anthropic snapshot from rotting, and it retires the "re-check annually" rule that the 20 to 28 releases a month make unreasonable. Cost: about 1 hour. Fan-out: low.

**Churn to decline**

- Moving to plugins. The hub's adopt, adapt or skip model needs per-artifact choice that a plugin install does not give.
- Converting commands to skills with `disable-model-invocation`. Real, but it buys one mechanism instead of two and moves six files.
- Pinning full model IDs in agents. It trades a floating alias for a maintenance chore.
- Adopting prompt, agent and HTTP hooks, agent teams, `effort` and `maxTurns` fields, or `AGENTS.md`. No observed problem calls for them.
- A Stop hook that enforces evidence lines. The enforcement gradient, `ENFORCEMENT.md:37-45`, already records why hard gates were declined. The docs now describe a cap on consecutive Stop blocks, which weakens one objection, but the hub's audit log holds one violation in 17 lines, so there is no pressing violation rate to enforce against.

## 6. Recommendation

Do these in order.

1. **This week, about 2 hours: catch up by hand.** Run `/doctor prompt-audit` over the hub, run the five-minute hook experiment, and land the three changes in section 5 as one doctrine entry. This clears the existing backlog, and it is the cheapest sample of what future drift costs.
2. **Next, about 5 hours: build Approach A.**
   - Write `docs/anthropic-sources.yaml` with eight sources: the six guidance pages, the changelog, and the `llms.txt` page list. Diffing the page list catches new pages the hub has no equivalent for, which is the discovery path the table in section 2 shows matters.
   - Store hashes and verdicts in the register. Keep page text in a gitignored directory.
   - Add the script and a test with mocked fetches, test first per `CLAUDE.md`.
   - Add one step to `/session-start` that prints at most ten lines and tags them `[measured]`.
   - Add a `--accept` command that stamps a reviewed hash with a reason.
3. **Decide separately, on paperboy's own merits, whether it should run daily.** Do not load the doctrine duty onto it. If the user wants paperboy daily, give it its own schedule and treat the daily_weather crontab as off limits, because of the canary and the restart rule.

Cost estimate: 7 hours in total, about 2 for the catch-up and 5 for the build. Run cost is zero.

**Falsifier 1.** If, by 2026-12-17, the register has flagged fewer than two of the six guidance pages as changed, or has flagged changes that three reviews in a row closed as "no doctrine change", then the pages move too slowly or too irrelevantly to justify the build. Fall back to Approach E with a quarterly date and remove the session-start step.

**Falsifier 2.** If a `/session-start` shows a last-review age above 14 days on two separate occasions without anyone acting, the pull model is failing in the same way a push model would. Then add a push, as a user cron or a scheduled task, that writes into the same register. Do not move to paperboy.

A third observation would also show the recommendation wrong: if the hook experiment shows that the agent does see the exit 0 warning, then the headline example in section 2, row 6, falls, and the case for the build rests on rows 1 to 3 alone.

## 7. Open questions

- What is the real change rate of the six guidance pages? The parallel cadence measurement should answer this and could move falsifier 1.
- Is there a model deprecations page the register should include? I did not fetch it, so I have not proposed a URL. paperboy's pinned model IDs suggest the hub should know about retirements.
- Does the user want the hook to warn the agent? That is a change in how the enforcement gradient behaves, and it is theirs to decide.
- Should `.claude/settings.json` be audited against the settings page? I did not read it, as instructed. Someone with that access should run the deny-rule check in row 13.

## 8. Claims

| Claim | State | Evidence |
|---|---|---|
| Claude Code 2.1.309 is dated 2026-10-22 and 57 releases fall in the last 60 days. | observed | `curl https://code.claude.com/docs/en/changelog.md`, parsed by a Python script: 310 versions total, newest `2.1.309`, `last60 57`. |
| Six guidance pages returned identical content on two fetches. | observed | `sha256sum` of two `curl` fetches per page matched for all six; sizes 36,360 to 114,542 bytes. |
| `/doctor prompt-audit` was added in 2.1.283 on 2026-09-25. | observed | `grep -n prompt-audit changelog.md` line 2094; the nearest preceding version header is `2.1.283`, `September 25, 2026`. |
| A GitHub Atom feed for Claude Code releases exists and updated today. | observed | `curl` returned 200, `application/atom+xml`, 10 entries, `<updated>2026-10-22T22:18:33Z`. |
| The Anthropic engineering best-practices post now redirects to the docs page. | observed | `curl -w '%{http_code} %{redirect_url}'` printed `308 https://code.claude.com/docs/en/best-practices`. |
| The weekly digest index ends at week 37 and lacks week 31. | observed | `llms.txt` fetch, summarized by the fetch tool, not re-parsed by me. Treat as a lead, not a count. |
| Claude never sees stderr from a hook that exits 0; PostToolUse exit 2 shows stderr to Claude. | observed | The hooks reference fetch, quoting "Claude never sees stderr from a hook that exits 0" and the PostToolUse table row. |
| The hub's `ENFORCEMENT.md:32` says the stderr warning reaches the agent. | observed | `sed -n 28,36p .claude/skills/shift-left-testing/ENFORCEMENT.md`. |
| The agent does not see the hook's warning in practice. | UNVERIFIED: I may not write to `src/` and did not run the scratch experiment. The docs imply it. |
| `CLAUDE.md` is 218 lines and its tree lists 3 agents, 3 teams and 5 commands against 5, 4 and 6 on disk. | observed | `wc -l CLAUDE.md` printed 218; `ls .claude/agents .claude/teams .claude/commands` counted 5, 4 and 6; `CLAUDE.md:165-172` read. |
| The shift-left audit log holds 17 lines, one of them `MISSING_TEST`. | observed | `wc -l` printed 17; `uniq -c` showed one `MISSING_TEST` on `zz_throwaway_nobody.py`; file mtime Oct 4. |
| The longest `SKILL.md` is 189 lines; the longest description line is 556 characters. | observed | `wc -l` on 13 skill files; `awk` on `^description:` lines. |
| Twelve of thirteen skills carry a `version` field. | observed | Frontmatter key listing; only `traversing-the-knowledge-base` lacks it. |
| About 138 of 757 added or changed changelog lines in 60 days touch memory, hooks, skills, agents or settings. | observed, crude | A keyword parse of the changelog; section tracking is approximate and "memory" matches non-doctrine uses. Use as an order of magnitude only. |
| Approach B costs 25 hours or more, and approach C costs 3. | written | My estimates. No measurement. |
| daily_weather's crontab change needs an App restart and a canary window. | observed | `deploy/README.md:7` and `:35`. |
| paperboy's pinned models are `claude-sonnet-4-20250514` and `claude-haiku-4-5-20251001`. | observed | `config/paperboy.yaml:101-102`. |

I did not run the register script, the hook experiment, or `/doctor prompt-audit`. I did not read `.claude/settings.json`, `.env`, or `docs/design/hold`, and I wrote nothing outside this file.
