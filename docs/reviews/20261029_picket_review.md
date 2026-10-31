# Review: CONOP PICKET, challenge round 1

**Author**: code-reviewer
**Date**: 2026-10-29
**Type**: Config review (CONOP challenge round)

**Verdict: GO-WITH-FIXES.** The plan carries every section CONOP-FORMAT requires, names what is unmeasured, and runs its eight falsifiers before the build. Two defects would be built into Wave 1 as written: the sweep repeats a full adoption every day until its pull request merges, and A1's named fallback cannot write the files doctrine lives in. Eleven warnings follow; most are one-line changes to a decision's text.

Subject: `docs/plans/conop_picket_unattended_doctrine_sweeps_and_guidance_watch.md`, the uncommitted working-tree copy of 2026-10-29. Inputs: `CONOP-FORMAT.md`, the two redacted findings files in the session scratchpad (cited by section, never by path), the protocol, `scripts/propagate_doctrine.py`, the 2026-10-22 review, three skills, and five live docs pages fetched today. I ran no tick, opened no connection to the NAS, and wrote nothing but this file and one memory note.

| Severity | Count |
|---|---|
| Critical | 2 |
| Warning | 11 |
| Suggestion | 7 |

## Critical

**C1. The sweep is not idempotent while a pull request is open.** Lines 77, 114, 185.
Each tick resets the clone to `origin/main`, whose delivery mark lacks the entry's heading until the PR merges. `propagate_doctrine.py` sends every heading the mark lacks, so the tick re-runs the whole adoption, and the push to the existing `topic/doctrine-<entry-date>` branch is rejected as non-fast-forward (or rewrites the diff under the reviewer if the tick forces). Under the hub's own session gaps (longest 52 days, 6 of 25 intervals over 14) a repo gets a full model run daily for weeks. This is the cost shape that matters: not the idle tick, the pending one. Wave 3's exit ("three pull requests opened in one cycle") passes on day one and hides it.
Fix: before branching, `git ls-remote --exit-code origin refs/heads/topic/doctrine-<date>` or `gh pr list --label doctrine --state open`; on a hit write a `pending` record line, apply nothing, call no model. Add to 3c's standard: "the tick after an opened PR writes `pending` and calls no model".
Evidence: `scripts/propagate_doctrine.py`, `entries_to_deliver`: `if held is not None: wanted = [e for e in entries if _heading(e) not in held]`; plan line 185 "fetch, reset to `origin/main`, branch"; `ls docs/sessions | grep -oE '^[0-9]{8}' | sort -u` piped to a date diff with today appended → `n 26 max 52 over14 6 newest_to_today 7`.

**C2. A1's fallback cannot write under `.claude/`.** Line 56.
The kill-criterion falls back to "`acceptEdits` plus narrow allow rules and a deny on `git push`". The docs: `acceptEdits` still prompts on writes to protected paths, `permissions.allow` rules do not pre-approve protected-path writes, and a `-p` run with no host denies every prompt. Line 36 says doctrine writes almost nowhere else. So the fallback applies nothing, and the only unattended mode that writes `.claude/` without the classifier is `bypassPermissions`, which the hub's OVERWATCH history argues against. A gate decision rests on this row.
Fix: A1's kill-criterion is Approach B or D, no patch (CONOP-FORMAT: the kill-criterion "abandons the approach rather than patching it"). Name `bypassPermissions` in What We Do NOT Build.
Evidence: permission-modes.md: "`permissions.allow` rules in settings files do not pre-approve protected-path writes. The safety check runs before Claude Code evaluates allow rules"; `acceptEdits` "These still prompt: ... Writes to protected paths"; headless.md: "In a `-p` run with no host, these requests are denied either way".

## Warning

**W1. The user's turn cap is missing.** Line 117. `docs/tasks.md:17` records the 2026-10-29 ruling "a turn cap, not a dollar cap"; D5's command has no `--max-turns`, and D10's record has no `num_turns`. `--max-turns` ends the run with an error subtype, which the tick must read as "needs a human", not as a crash. Fix: `--max-turns N` (N from the 0f hand tick, with headroom), `num_turns` and `total_cost_usd` in the record, `error_max_turns` a named status.
Evidence: `grep -n -i "max-turns\|turn cap\|turns"` on the plan → no cap anywhere; cli-reference.md: "`--max-turns` Limit the number of agentic turns (print mode only). Exits with an error when the limit is reached. No limit by default"; SDK result subtypes include `error_max_turns`.

**W2. "Any denial" discards what the reviewer needs.** Line 117. Auto-mode denials include benign ones (a read outside the clone, a critical-path `rm` the agent then avoids). On any of them the tick resets and opens nothing, so the human gets a word and a count while the partial diff survives only in a transcript on the box. The PR never merges itself, so the safer record is the branch pushed and the PR opened as a draft labeled `doctrine needs-human`, its body listing each denial's `tool_name` and `tool_input` path (terms redacted). Reset only on an error subtype. The record line carries the tool names, not a count.
Evidence: agent-sdk/typescript.md: `permission_denials: SDKPermissionDenial[]`; `SDKPermissionDenial = { tool_name; tool_use_id; tool_input }`.

**W3. The key's blast radius is unstated.** Lines 40, 116, 128. The sibling records gave each app account the same workstation deploy key, so the key that opens `picket` opens paperboy's home and its token; D4's "a revoked token then stops one service, not two" is true of the tokens and false of the key. Inside the home: a one-year Max token, a GitHub token with contents write on four repos (pushing `main` is a tick rule, not a token limit), and the lead's private-term list (0d). Fix: a per-service key for `picket`; branch protection requiring a PR on `main` in the hub and the three canaries, so "never pushes main" is GitHub's rule; the blast radius written into D4.
Evidence: findings (urd, stx-server, schelling-point) section B "the key is the workstation's existing deploy key"; findings (paperboy, daily_weather) section A "same host entry and deploy key as the first app".

**W4. D13 guards the push, not the pull request, and not the tokens.** Lines 125, 144. Check 7 scans the index and unpushed commits; the PR body (the record, per 1c) goes through `gh`, which it never sees, yet MOP line 144 claims zero hits "across their diffs and bodies". Check 7 looks for terms, not secrets; the OAuth token sits in the agent's Bash environment and the GitHub token in `.env`, and /pcc check 1 (secrets) is not named. Check 7 is also a bash block inside `pcc.md` that the tick would slice out at run time, as the test does. Fix: extract it to `scripts/private_terms_check.sh` so command, test and tick run one file; run it and check 1's patterns over the branch and the PR body; record the list's line count and mtime per tick so drift from the lead's list is visible.
Evidence: `.claude/commands/pcc.md:108-110` "Scans what a push would carry: the index, and every commit not on any remote"; `tests/unit/test_pcc_private_terms.py` `_check_7_block()` slices the section by regex; `pcc.md:22` "### 1. Secrets Check".

**W5. MOE 1's calibration is decorative; MOE 3 measures activity.** Lines 149-153, 209. No wave gates on MOE 1 (Wave 4's exit is MOE 3), so "before gating Wave 4 on it" never fires, and "merged within a week ranks above open for a month" is the metric ordering itself, not a known-good against a known-bad. MOE 1 has no value for a PR closed with a reason, a review outcome the plan invites; its baseline (adoption records at 23 days) is a different instrument. MOE 3 reads 1.0 the day D11 ships. Fix: MOE 1 = median days from PR open to close, merged or refused; MOE 3 = fraction of opted-in repos whose `.claude/doctrine-delivered` on `origin/main` holds every hub heading, by `gh api` (a real adoption state, and G3's collector for the set). Name who runs MOE 1 at Wave 3 close plus 30 and where it lands, since a CONOP needs a terminal status.

**W6. A6's falsifier is sixty days, not an afternoon.** Line 61. The premise can be tested today: `gh pr list --state all` on the three canaries gives open-to-close times over the last months, against the notification ages in Nidhogg's clones. Keep MOE 1 as the live measure.

**W7. No assumption covers the apply being right, and D8 makes the PR a rubber stamp where no CI runs.** Lines 37, 120, 186. Enemy Forces names the risk; no row carries it; the first check is 3e, after three PRs exist. Add A9: the 0f hand tick on a real entry in a scratch clone of `stx-server`, diffed against the lead's own adoption of that entry; kill: two of three canaries need a rewrite, which is Approach D. What the reviewer sees under D8: a `.claude/` markdown diff and a record whose evidence is the diff, which reaches `written` and no higher; say so in the prompt. For a repo with no CI, the plan's own premise (the human does not open the repo) makes "the reviewer runs the tests" the step that will not happen; make a CI workflow on pull requests part of D3's opt-in criterion and state the CI result in the PR body.
Evidence: verifying-claims `SKILL.md`, states table: "written | The change exists in a file | The diff, or the path".

**W8. D14 removes the gate the deploy script relies on.** Lines 126, 189. The pattern's script refuses a commit whose CI did not pass and skips when `.github/workflows` is absent; the hub has no `.github`, so 1g skips forever and deploys a red `main`. Fix: 1g runs `.venv/bin/pytest -q -k "picket or anthropic_sources or propagate"` on Nidhogg and refuses on failure; name it as D14's cost.
Evidence: `ls .github` → `No such file or directory`; findings (paperboy) section D: "prints a skip line when `.github/workflows` is absent".

**W9. The record and the session-start line miss picture fields.** Lines 122-123. The record has no time, no universe (repos listed, present, skipped), no `num_turns`; the PR-count line has no `unchecked` shape, so "0 open" and "`gh` failed" render alike. Fix: add `at`, `repos_listed`, `repos_present`, `repos_skipped`, `num_turns`; give the second line the two-shape contract; ship the gap rows with the probes in Wave 1 (the skill's "For a probe" procedure), not in Wave 4.
Evidence: maintaining-the-common-operating-picture `SKILL.md` rules 2 and 8; plan line 122's field list.

**W10. "Static git" has no official source; an image that ships it is simpler.** Lines 34, 57, 118. git-scm.com offers Linux git by package manager or source build only; `gh` and `jq` publish binaries. A third-party git build curl'd into the home and run by an agent holding a GitHub token is an exposure the plan does not weigh, and `gh pr create` calls git. The Docker library image `buildpack-deps:bookworm-scm` ships git, curl and ca-certificates; pinned by digest per urd's lesson, it retires the `SSL_CERT_FILE` workaround, and the tick parses JSON in Python already, so `jq` is optional. The pattern's one-image rule is about consistency; its records also say "pin by tag and digest". Recommend the image; A2 becomes "the image pulls and `git --version` prints in the container".
Evidence: git-scm.com/install/linux: every Linux entry is a package-manager command, plus "download a tarball and build from source"; docker-library `buildpack-deps` README: `curl` variant "includes just the `curl`, `wget`, and `ca-certificates` packages", `scm` "adds ... `git`"; findings (urd) section F "pin by tag and digest in one file".

**W11. Claims without evidence lines.** Lines 12, 28, 42. Line 42's 52 days holds on re-run. Line 12's "18 have not opened a session" is not measurable from the hub (G3); the measurable form is "18 recorded no adoption in this box's clones". Line 28 holds on the pages read today, with one shade: `permission_denials` is documented on the `stream-json` result and in the SDK result type; the headless page names the `json` format only for `total_cost_usd`. A1's hand tick reads the field and settles it. Put `Evidence:` or `UNVERIFIED:` under each.
Evidence: headless.md "With `--output-format stream-json` ... the final result message lists them in `permission_denials`"; permissions.md table: hooks and `env` "Used" under `claude -p`, allow rules "Not used. Claude Code prints a `this workspace has not been trusted` warning to stderr", and "set `projects["<path>"].hasTrustDialogAccepted` to `true` in `~/.claude.json`"; authentication.md "generate a one-year OAuth token with `claude setup-token`" and "Bare mode does not read `CLAUDE_CODE_OAUTH_TOKEN`"; headless.md "`--bare` ... will become the default for `-p` in a future release"; permission-modes.md "When repeated blocks reach a threshold, the action doesn't run and Claude keeps working. Claude Code doesn't stop the run" and the protected-path table row `auto`: "Routed to the classifier".

## Suggestion

**S1. Cut D7.** Line 119. The plan says the key lifts only the allow-rule warning; auto mode uses no allow rules; hooks and `env` run regardless. A write to `~/.claude.json` per tick buys silence. One row the plan omits: `.mcp.json` servers connect without asking under `-p`; a canary with one would run it.
Evidence: permissions.md table: "Servers in `.mcp.json` ... Connected without asking, approved or not".

**S2. Cut the watch's model call.** Line 121. A `difflib` unified diff in the PR body is what the reviewer reads; the surface map is the lead's judgment at `--accept`. One prompt file, one `-p` path, and the only push from the box to the hub go away.

**S3. Close D19 as no.** Line 131. The plan's own reason: one more place to leak a term.

**S4. Name the model and check it against auto mode's list.** Lines 27, 167. Auto mode needs Opus 4.6 or later, Sonnet 4.6 or later, Haiku 5.5, or a Fable model; 0b copies paperboy's pin without naming it. Make "the pinned model is on the list" part of A1's probe.
Evidence: permission-modes.md: "Older models, including Sonnet 4.5, Opus 4.5, Haiku 4.5, and claude-3 models, are not supported on any provider".

**S5. Assumptions table housekeeping.** Lines 57-63. A2 and A3 kill-criteria patch (amend D1; adopt without the trail); A8's "None" leaves a mandatory field empty, so move A8 to a Wave 0 standard. Wave 1 is at TCS detail while 1c rests on A1 and A3 (sequencing rule 2); Wave 0 runs them first, so mark 1c's denial and trust steps contingent.

**S6. Status, mission, headings.** Lines 1, 3, 69, 159-205. Status reads Draft while under review (In Debate). The Mission says "from Wave 3 close onward" while the watch goes live in Wave 2 and the sweep during Wave 3. Six em dashes in headings; the title is the template's form, the wave headings can take a colon. 0e's "seed each consumer's delivery mark" is a no-op: the clone carries the committed mark.
Evidence: `grep -n` for U+2014 → lines 1, 159, 176, 193, 199, 205.

**S7. Roster entry and snapshots.** Lines 46, 172. HOME-STORAGE's gate needs the box in a roster with personal scope before a personal data root is used; the record file on the share is one. paperboy solved it with an entry keyed by the container hostname, which D1 sets to `picket`; add it to 0g. Write "no snapshot of the home; loss re-runs 0b to 0e" rather than leave the sibling question open.
Evidence: `HOME-STORAGE.md` "The machine is in the roster with `personal` in its scope, and `known` is true"; `config/project.yaml` `machines:` lists two workstations and `unknown`.

## Answers the brief asked for

- **D2's blast radius.** A tick can reset its own clones, write anywhere in the home (`.env`, the term list, the config file; none is a protected path), truncate the record file on the share, and push branches and open PRs on four repos. Bounded by: never merge, reset on denial, D16's scope, the classifier on `.claude/`, and critical-path removals denied outright in a `-p` run. Not bounded: push to `main` (W3), force-push and branch deletion (W3), run length (W1), daily re-runs (C1).
- **Cost shape.** An idle tick calls no model: the watch is a hash, the sweep is `git pull` plus `propagate_doctrine.py`. An active repo costs one `-p` session; estimate 20 to 80 tool calls per entry (basis: an Action Required of 5 to 15 numbered steps, each a read and an edit, plus the record and the removal), and in auto mode each call is also a classifier request, so about twice that in model requests; paperboy's single-call runs took 131 to 360 s. Proved wrong by `num_turns` outside that range in the 0f tick. A pending repo costs the same every day (C1).
- **Sibling records' open questions.** Answered by the plan: host versus container cron, token lifetime, trust, permission mode and tools, version pin, the GitHub push and guard, ACL reach, memory, failure reporting, the docs domains. Assigned to a falsifier: git and jq in the image (A2), hooks under `-p` (A3), the five-hour pool (A5). Ignored: the roster gate (S7), snapshots of the home and whether the YAML survives an upgrade (S7), clock sync (the record's `at` against the hub's receipt time is a free check), container stdout retention, and `HOME` or `CLAUDE_CONFIG_DIR` inside the container (0f runs in a login shell on the host; the 0g container tick is where this is first measured; say so).
- **Simplicity First cuts.** D7, the watch's model call, D19, 0e's seeding clause, and 4d as a Status Log line rather than a task. None touches the mission.
- **Sibling warnings the plan repeats.** The YAML living only in the UI (kept, with 0g's copy); a success line beside a failure (paperboy's first tick): the record's `status` must not read `success` when `permission_denials` or an `error_*` subtype is present (W2); merged is not deployed (1g's proof covers it).

## Format check

Every section CONOP-FORMAT names is present; the Mission carries "in order to"; four approaches include a bold one; open decisions are flagged; each MOE states when it becomes measurable. Defects against the format's rules: C2 (kill-criterion patches), W6 (falsifier not an afternoon's test), S5 (A8 blank; A2 and A3 patch), W5 (calibration decorative), S6 (status value).

## Claims

| Claim | State | Evidence |
|---|---|---|
| The plan has every CONOP-FORMAT section. | observed | `grep -n "^## \|^### "` on the plan against the template: Problem, Situation (four subsections), Assumptions with four columns, Mission, Approaches A to D, Design Decisions, Measures, Waves 0 to 4, NOT Build, Agent and Team Design, References. |
| `propagate_doctrine.py` re-sends any heading absent from a repo's mark, whatever its date. | observed | `entries_to_deliver`: `if held is not None: wanted = [e for e in entries if _heading(e) not in held]`. |
| Hub session gaps: 26 dates, longest 52, 6 over 14, newest doc to today 7. | observed | `ls docs/sessions \| grep -oE '^[0-9]{8}' \| sort -u` into a Python date diff → `n 26 max 52 over14 6 newest_to_today 7`. |
| `acceptEdits` prompts on protected paths; allow rules do not pre-approve them; a `-p` run with no host denies prompts. | observed | permission-modes.md and headless.md, quoted under C2. |
| Hooks and `env` run under `-p` in an untrusted folder; allow rules are dropped with a stderr warning; `hasTrustDialogAccepted` is the hand key. | observed | permissions.md "What runs before you trust a folder", quoted under W11. |
| The result message carries `permission_denials` with `tool_name`, `tool_use_id`, `tool_input`; the headless page names it for `stream-json`. | observed | agent-sdk/typescript.md `SDKResultMessage`; headless.md, quoted under W11. |
| `--max-turns` exits with an error at the limit; no limit by default. | observed | cli-reference.md line quoted under W1. |
| `setup-token` mints a one-year token on Pro, Max, Team or Enterprise; bare mode reads no OAuth token and is slated to become the `-p` default. | observed | authentication.md and headless.md, quoted under W11. |
| Auto mode's model list excludes Sonnet 4.5, Opus 4.5, Haiku 4.5. | observed | permission-modes.md, quoted under S4. |
| `docs/tasks.md:17` holds the turn-cap ruling; the plan names no cap. | observed | `grep -n -i picket docs/tasks.md` → line 17 "a turn cap, not a dollar cap"; plan grep under W1. |
| Check 7 scans the index and unpushed commits; the test slices it from `pcc.md`. | observed | `pcc.md:108-110`; `test_pcc_private_terms.py` `_check_7_block()`. |
| The hub has no `.github` directory; the five test files line 29 names exist. | observed | `ls .github` → not found; `ls tests/unit/test_{propagate_doctrine,adopt_doctrine,pcc_private_terms,gaps,state_block}.py` → five paths. |
| Six lines of the plan carry an em dash, all headings. | observed | `grep -n` for U+2014 → 1, 159, 176, 193, 199, 205. |
| The plan and this report hold no term from this machine's private-term list (6 terms). | observed | `grep -c -i -F -f <list> <file>` → `0` for each; counts only. |
| git-scm.com offers Linux git by package manager or source build only; `buildpack-deps` `scm` ships git over `curl`, `wget`, `ca-certificates`. | observed | git-scm.com/install/linux and the docker-library README, quoted under W10. |
| Each NAS app account received the same workstation deploy key; the slim image lacks git and a CA store; the deploy script skips the CI check without a workflow. | record, not re-run | The two redacted findings files, read this session; not re-checked against the sibling repos. |
| 20 to 80 tool calls per entry, doubled in auto mode. | estimate | Basis under "Cost shape"; proved wrong by `num_turns` outside the range in the 0f tick. |
| Whether `--output-format json` prints `permission_denials` on the box. | UNVERIFIED: needs a tool-enabled `-p` run, which only the 0f hand tick can do. | |
