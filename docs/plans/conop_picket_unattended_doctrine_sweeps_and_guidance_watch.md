# CONOP PICKET — Unattended Doctrine Sweeps and the Anthropic Guidance Watch, from the NAS

**Status**: In Debate. Draft written 2026-10-29 from the user's three rulings that day (apply-then-review for opted-in repos; the NAS as the host; a turn cap, not a dollar cap, on a Max subscription) and the install records of four sibling repositories. Round 1 returned the same day: `code-reviewer` GO-WITH-FIXES, 2 Critical, 11 Warning, 7 Suggestion (`docs/reviews/20261029_picket_review.md`); every finding is applied below (Status Log). Approval is the user's.
**Date**: 2026-10-29
**Lead**: jhutchison (session lead: Claude)
**Parent task**: `docs/tasks.md`, the PICKET line (added 2026-10-29), which supersedes the P1 register task's "scheduled check" clause and the 2026-10-22 decisions 3, 5 and 7 as the user ruled on them 2026-10-29.

---

## Problem

Doctrine reaches a consumer only when a human opens a session there. The 2026-10-06 cycle reached 20 repositories; two recorded adoption, and 18 recorded none in this box's clones over 23 days, so the hub cannot say what the fleet runs. The same shape holds upstream: Anthropic's Claude Code guidance changed substantively in every monthly interval from August to October, and the hub's standing reference is a December 2025 snapshot. Both delays have one cause: the reader is the collector, and the reader is intermittent.
Evidence: `docs/tasks.md` Focus step 2 (assay 2026-10-05, agent-eval 2026-10-06, "the other 18 report in their own sessions"); `docs/reviews/20261022_anthropic_docs_inventory.md` section 6; hub session gaps from `ls docs/sessions | grep -oE '^[0-9]{8}' | sort -u` with today appended → 26 dates, longest 52 days, 6 intervals over 14.

The household NAS is not intermittent. It runs two daily services under a pattern three repositories have adopted, one of them calling Claude Code non-interactively on the Max subscription since 2026-10-24. This plan adds a third service of that shape with two ticks: a sweep that applies each unread doctrine notification in an opted-in repository on a branch and opens a pull request for the human to accept or refuse, and a watch that hashes Anthropic's guidance pages daily and opens a pull request carrying the diff when one changes. The human's work moves from applying to reviewing, and the pull request lands where the human already looks.

---

## Situation

### Friendly Forces (what we have)

- `scripts/propagate_doctrine.py`: discovery under `~/projects`, the delivery mark, append mode, `--dry-run`, `--since`, the `propagation.exclude` list. Runs unchanged on any box whose `~/projects` holds the clones. It sends every heading a mark lacks, whatever the date (`entries_to_deliver`), which is the fact behind D2's idempotency guard.
- `scripts/adopt_doctrine.py`: the deterministic adopter for verbatim-copy artifacts; prior art for what an agent need not do by hand.
- `docs/propagation-protocol.md`: the Evaluation Gate, Rules 1 to 4, the delivery mark, rollback by REVERT entry. Apply-then-review changes step 6 of the Cycle Anatomy and the consumer's Step 3.6, nothing else.
- The register design, already reviewed: `docs/reviews/20261022_anthropic_docs_feed_proposer.md` (Approach A) with `docs/reviews/20261022_anthropic_docs_feed_review.md` W1's schema (collector, universe, motion, surprise, append-only reviews, two-shape output), W2's changelog rule, C2's first-seen requirement. Sources in `docs/reviews/20261022_anthropic_docs_inventory.md`.
- The NAS app pattern, proven three times: one key-only account per app named by us, its home on the apps dataset, a clone in the home, a host-built uv venv at a pinned Python, supercronic as PID 1 of a Custom App that bind-mounts the home, a tracked crontab, a deploy script that refuses dirty or unpushed states and proves with read-only steps, a canary window with a fixed checklist. Records: paperboy `deploy/README.md` and its four COURIER session docs (2026-10-24 to 10-26); daily_weather `docs/runbooks/home-server-custom-app.md` and its HERALD session docs (2026-10-02 to 10-12); urd's D11 step list of 2026-10-26.
- Claude Code headless on that box, proven: paperboy runs `claude -p` on a `claude setup-token` one-year token held in `.env` at mode 600, CLI pinned at 2.1.310 by the native installer, auto-update off and the model pinned in the account's settings file, the token kept out of the App's environment by declaring no `env_file`.
- The docs as read 2026-10-29, each verified again by the round 1 reviewer: auto mode works in `-p` with `--permission-mode auto`; `--permission-prompts none` denies what would prompt and tells the model not to retry; the result message carries `permission_denials` with `tool_name`, `tool_use_id` and `tool_input` (documented on the `stream-json` result and the SDK result type; whether `--output-format json` prints it is A1's probe); `--max-turns` ends the run with an error at the limit; hooks and the `env` block run under `-p` in an untrusted folder and only `permissions.allow` rules are dropped; servers in a repo's `.mcp.json` connect without asking under `-p`; the classifier routes writes under `.claude/` to itself as protected paths, and no allow rule pre-approves them; `CLAUDE_CODE_OAUTH_TOKEN` is read in every mode but bare, and bare is slated to become the `-p` default.
Evidence: `docs/reviews/20261029_picket_review.md`, findings C2, W1, W2, W11 and S1, each with the page and the quoted line.
- Hub tests that pin the surfaces this plan touches: `tests/unit/test_propagate_doctrine.py`, `test_adopt_doctrine.py`, `test_pcc_private_terms.py`, `test_gaps.py`, `test_state_block.py`.
- The topic-branch rule (`.claude/skills/using-topic-branches/SKILL.md`): `topic/<scope>-<slug>`, merged at a gate, deleted after.

### Enemy Forces (what works against us)

- The pattern's image ships no CA store, no `git`, no `jq`, no mDNS resolver; nothing is installed system-wide and the account has no sudo. git has no official static Linux binary, so a sweep that needs git changes the image (D6).
- Every proven headless run on the box used `--tools ""` from a temp directory. A run that edits files, runs git and reads a repo under `--permission-prompts none` is unmeasured there.
- Auto mode routes every write under `.claude/` to the classifier, and doctrine entries write almost nowhere else. A block does not stop a `-p` run; it denies the action and continues. No unattended mode other than `bypassPermissions` writes those paths without the classifier, and that mode is out (What We Do NOT Build).
- The propagation script re-sends any heading a mark lacks. A clone reset to `origin/main` while its pull request waits would be swept again every day, a full model run per repository per day for up to 52 days (round 1, C1).
- Entries are written for a maintainer with judgment. urd and hallmark bootstrapped with subtractions; agent-eval maps roles onto a custom roster. An agent that follows Action Required verbatim in such a repo does the wrong thing.
- supercronic reads the crontab once and never replays a missed tick; a YAML save restarts every service in the App; the App definition lives only in the UI, readable by root; no dataset on the box has a snapshot.
- The subscription pool is one pool: paperboy's 05:30 run, interactive work and this service's ticks share the five-hour window.
- The hub's history holds a 138 GB fixture deletion and a swept `git add`. The sibling records gave every app account the same workstation deploy key, so a key that opens one home opens them all and their tokens.
- The boundary line has been crossed within hours of being written, twice, by the lead and by a review's own example. A push from the box runs with no private-term guard unless one is installed there, and check 7 lives as a bash block inside a command file, not a script.
- Session gaps on the hub run to 52 days, so the human half of apply-then-review can still lag by that much.

### Terrain (the ground we operate on)

- TrueNAS SCALE 25.10 on a 6-thread 15 W x86-64 box, Docker 28, Custom Apps from UI-pasted compose YAML with no variable interpolation and absolute paths only; apps capped at 512 MB; a shared dataset the desktop mounts holds outputs; NFSv4 ACLs with inheritance that reaches only later-created folders.
- Three reach channels: a per-account SSH alias from the workstation (the agent's one credential), the web shell as the owner account for `midclt` and `setfacl` (the lead's), the UI for the App and its logs (the lead's).
- The hub is public on GitHub; the opted-in canaries are personal repositories on GitHub. Work repositories are excluded until gaps G6 and G11 close. Branch protection and rulesets on a private repository are a GitHub Pro feature: the API answered `Upgrade to GitHub Pro or make this repository public` for every private repository on Nidhogg on 2026-10-30, so a free personal account cannot make `main` refuse a push by rule, and the sweep's write boundary is drawn by ownership instead (D4, A9).
- Egress from the box is open to Anthropic's endpoints and the hosts the two existing apps use; the docs domains are unmeasured.
- The register's pull half runs at `/session-start` on Nidhogg regardless of this plan; the NAS adds the push half and first-seen.

### Assumptions

| Assumption | Cheapest falsifier | Blast radius if wrong | Kill-criterion |
|------------|--------------------|-----------------------|----------------|
| A1. Auto mode engages in a `-p` run under the OAuth token on the box with the pinned model, approves a doctrine entry's writes under `.claude/`, and `--output-format json` prints `permission_denials`. | One hand tick as the account in a login shell on a scratch clone holding a known entry; read the result's mode, `num_turns` and `permission_denials`; retry with `stream-json` if the field is absent. First reading, Nidhogg 2026-10-30, under the user's login, CLI 2.1.310, `claude-sonnet-5-5`: four writes, three under `.claude/`, `permission_denials` present and empty in the `json` result, `num_turns` 2, `subtype` `success`, 7 s; the box reading is still owed. | D5; Waves 2 and 3. | The classifier is unavailable for the account or model, or denies the `.claude/` writes on three consecutive runs: Approach B (cloud scheduled tasks, auto mode by default) or Approach D. No weaker mode is a fallback, because none writes protected paths unattended. |
| A2. The image of D6 runs the pattern unchanged (non-root uid, bind-mounted home, supercronic as PID 1) and `git --version`, `gh --version` print inside the container; a clone of the public hub over HTTPS succeeds there. | The 0g container's first tick, which runs exactly those three commands and writes their output to the record. | D6; Wave 1's 1g. | Any of the three fails: the sweep leaves the box for Approach B; the watch stays, since it needs no git. |
| A3. A `-p` run in a clone loads its `CLAUDE.md` and runs its `PostToolUse` hooks. | A hand tick in a clone with a probe hook that writes a marker file. | Whether the audit log on the box is evidence; which entries the sweep may carry. | Hooks never run under `-p`: entries whose Action Required depends on a hook firing (entry H of the 2026-10-22 draft) leave the sweep's scope and go by hand. |
| A4. A sweep tick with the CLI and git stays under the memory cap. | `memory.peak` from the cgroup after the first real tick, read as the account. First reading, Nidhogg 2026-10-30, `/usr/bin/time -v` around the A1 probe: maximum resident set 276 MB for a 2-turn run; the container reading is still owed. | D18. | Over 480 MB: raise the cap to 1 GB. Over 2 GB: the sweep leaves the box for Approach B. |
| A5. A sweep tick at 04:10 and paperboy's 05:30 run fit one five-hour window. | Both run on one morning; read both record lines for a rate-limit error. | D12. | A limit hit on two of seven canary mornings: the sweep runs weekly, in a different window. |
| A6. A pull request gets a decision sooner than a notification file does. | Today, on Nidhogg: `gh pr list --state all --json createdAt,closedAt` on the three canaries, open-to-close times over the last months, against the age of each unread notification in this box's clones. Measured 2026-10-30: none of the three canaries, nor `fist`, `veil-engine`, `magic-movies` or `propter`, has ever had a pull request (0 each), so the history reading exists only for `daily_weather`: 65 pull requests, 56 merged, median open-to-close 0.0 days, longest 300 days, 5 open at 4 to 17 days; the unread notifications on this box are 24 days old (`stx-server`, `veil-engine`, `magic-movies`). The kill-criterion cannot fire from history; MOE 1 decides live. | The premise; Approaches A to C all fall. | The canaries' historic pull requests sat longer than their notifications: Approach D. MOE 1 keeps measuring after launch. |
| A7. The container reaches the two docs domains. | `curl -sI` of both as the account on the host, then the first watch tick's record line. | D9, D14. | Blocked: the hub gets the GitHub Actions cron the 2026-10-22 review proposed as W3, and the box keeps only the sweep. |
| A8. The agent applies a real entry correctly. | The 0f hand tick on a scratch clone of `stx-server` with the entry the lead adopted there by hand on 2026-08-27; diff the two adoptions. | D2, D8; the premise that review is cheaper than applying. | Two of three canaries need a rewrite in Wave 3: Approach D. |
| A9. The fork boundary works on a private personal repository: the service GitHub account, a read collaborator, can fork each canary, push a branch to its fork, open a pull request to the upstream `main`, and the canary's CI runs on that pull request without waiting for approval. | 0c by hand on one canary before the other two: allow forking and add the account as a read collaborator, fork, push a one-line branch, open the pull request with the account's token, read whether CI ran and whether it waited; then `git push upstream main` from the fork clone, which must be refused. | D3, D4, 0c, 0e; the user's 2026-10-30 ruling. | The fork cannot be created, the pull request cannot be opened, or CI will not run on a fork pull request in a private repository: GitHub Pro for the account, so `main` refuses a push by rule, the user's second option on 2026-10-30. A tick-only rule is not a fallback. |

Discovery finding exactly the opted-in clones is a Wave 0 standard (0e), not an assumption.

---

## Mission

The hub, through a third service on the NAS, hashes Anthropic's guidance pages daily and opens a pull request when one changes, from Wave 2 close onward, and applies each unread doctrine notification in every opted-in repository on a branch and opens a pull request, from Wave 3 close onward, **in order to** move the human's work from applying to reviewing and to make the fleet's adoption state and the guidance drift measurable by command at every session start.

---

## Approaches Considered

### Approach A: A fourth Custom App on the NAS, by the proven pattern (recommended)

One account, one home, one App, two crontab lines. The sweep tick pulls the hub clone, probes each opted-in repository for a pull request of this cycle in any state, runs the propagation script into the clones that have none, and for each clone with an unread notification resets it to `origin/main`, branches, runs `claude -p` with the adoption prompt in auto mode under a turn cap, reads the denial list, runs the private-term and secret checks over the diff and the pull request body, pushes, opens the pull request (a draft labeled `needs-human` when anything was denied), and writes one record line. The watch tick runs the register script and, on a change, commits the register's new fetch block and a unified diff of the page to a hub branch and opens a pull request, with no model call.

- Pros: reuses the propagation script, the notification channel and the delivery mark unchanged; reaches any repository cloned on the box; the always-on box becomes the first census of the opted-in fleet (gap G3); subscription-billed; the data path stays home apart from the model conversation; three runbooks already cover the install.
- Cons: three secrets on the box (an SSH key, a model token, a GitHub token) with yearly renewal; the image changes to one that ships git; the App YAML lives only in the UI; the lead's hands are needed for the account, the tokens and every UI paste.
- Risk: medium. Every piece has run on the box except a tool-enabled `-p` run, which Wave 0 measures first.

### Approach B: Cloud scheduled tasks

One task per opted-in repository on Anthropic's infrastructure, pull request as the gate, no credential stored anywhere.

- Pros: zero operations; runs with every box off; auto mode by default; the fallback for A1, A2 and A4.
- Cons: a cloud clone cannot see the uncommitted notification file, so the task needs a second delivery channel reading the hub's doctrine file and the committed mark; GitHub-hosted repositories only; the clone goes to Anthropic's infrastructure; research preview; a lapsed GitHub connection turns a task off silently after 72 hours.
- Risk: low to build, medium to keep true to the protocol.

### Approach C: A Desktop local task or cron on Nidhogg

- Pros: sees local files; no new box.
- Cons: Nidhogg is on and off; a Desktop task fires only while the app is open and the machine is awake, and a missed day replays once; the user ruled the NAS the host on 2026-10-29.
- Risk: low, and rejected by the ruling.

### Approach D: Prune the roster and keep hand delivery (bold alternative)

Eighteen repositories that recorded no adoption in 23 days may not need doctrine at all. Shrink the roster to the repositories the user opens, deliver by hand, build nothing.

- Pros: nothing to run or renew; honest about which repositories are alive.
- Cons: does nothing for the repositories that are alive and still lag; leaves gap G13 without a collector; the user has asked for the automation.
- Risk: none to build; the cost is the lag it accepts.

**Recommendation**: Approach A, with Approach D's pruning applied first through the opt-in list (D3), so the sweep touches only repositories someone will review. Approach B is the kill-criterion of A1, A2 and A4; Approach D is the kill-criterion of A6 and A8.

---

## Design Decisions

| # | Decision | Status | Rationale |
|---|---|---|---|
| D1 | The host is a fourth Custom App on the NAS by the COURIER pattern: an account named `picket` with its own SSH key pair, home on the apps dataset, supercronic as PID 1, the home bind-mounted, `mem_limit` 512m, `user` the account's uid, `hostname` `picket`, `working_dir` the hub clone, `restart: unless-stopped`, `TZ` set. The roster in `config/project.yaml` gains an entry keyed `picket` with role `service` and scope `[personal]`, so HOME-STORAGE's gate passes for the record file on the share. No snapshot of the home: a loss re-runs 0b to 0e, and 0g keeps a copy of the App YAML in the lead's machine-local topology doc. | Resolved, the user 2026-10-29 | Three repositories proved the pattern in October; a fourth copies it, with the image of D6 as its one departure. |
| D2 | Apply-then-review replaces review-then-apply for opted-in repositories. The sweep branches `topic/doctrine-<cycle-date>`, commits the applied entry together with the updated delivery mark and the removal of the notification file, pushes to the fork, opens a pull request on the upstream labeled `doctrine`, never merges, and cannot push an upstream `main` (D4). Idempotency guard: before any model call the tick probes `git ls-remote --exit-code origin refs/heads/topic/doctrine-<cycle-date>` (`origin` is the fork) and `gh api "repos/<upstream>/pulls?state=all&head=<account>:<branch>"` (the `gh pr list --head` flag takes no `owner:branch` form, checked 2026-10-30 on gh 2.102.0); a hit writes a `pending` (open) or `refused` (closed unmerged) record line and the tick applies nothing. The human re-arms a refused repository by deleting the branch. Merging carries the mark, so the entry is never re-sent. | Resolved, the user 2026-10-29; the guard from round 1 C1 | The branch is the existing topic-branch gate; the pull request is the nag that lands where the reader looks; the probe makes a waiting repository cost zero model calls. |
| D3 | Opt-in by list: `propagation.auto_adopt` in `config/project.yaml`, read by the tick with the same slip-tolerant reading as `exclude`; a clone on the box the list does not name prints `[skip]`. Criterion to join: a personal GitHub repository with a CI workflow that runs on pull requests, forking allowed, the service GitHub account added as a read collaborator with a fork, and fork pull request workflows enabled with read-only tokens and no secrets. The three: `stx-server`, `schelling-point`, `hallmark`. Measured 2026-10-30 on Nidhogg: each has one workflow with a `pull_request` trigger on `main` that runs pytest; `propter`, proposed on 2026-10-29, has no workflow and is out. | Resolved, the user 2026-10-30 | Repositories bootstrapped with subtractions or custom rosters must not be swept blind; without CI on the pull request, D8 makes the review a rubber stamp (round 1 W7). Branch protection left the criterion when it proved a Pro feature on private repositories (Terrain). |
| D4 | Secrets on the box, three, each with a dated renew-by comment: the account's own SSH key pair, minted for this service and shared with no other account; a `claude setup-token` token minted for this service on Nidhogg, not paperboy's; a personal access token (classic) with the `repo` scope and an expiry, owned by a GitHub account created for this service, which owns the four forks (the hub and the three canaries), holds read on the three canaries, and nothing else. A fine-grained token cannot serve: it reaches only repositories its owner owns and cannot contribute where the owner is a collaborator (GitHub's token docs, read 2026-10-30), so it could push the forks but never open the pull request. The token pair lives in the clone's `.env` at mode 600, delivered once by `scp`, loaded by the tick itself; the App declares no `env_file`. Blast radius of the SSH key: the home, which holds both tokens and the private-term list; bounded by what the service GitHub account can reach: write on its own forks, read and pull requests on the three canaries and the public hub, no write on any upstream `main`, so GitHub's own permission check is the rule the tick cannot break. The hub, being public, may carry branch protection on `main` at no cost; the canaries cannot without GitHub Pro (Terrain). | Resolved; the per-service key from round 1 W3; the fork boundary the user's 2026-10-30 ruling | The sibling pattern's shared deploy key makes one key open every home; this service does not inherit that. Ownership draws the write boundary where branch protection would have, on an account with no plan fee. |
| D5 | The adoption run is `claude -p --permission-mode auto --permission-prompts none --max-turns N --strict-mcp-config --output-format json` from the clone root, N set from the 0f hand tick's `num_turns` with headroom. A normal end with entries in `permission_denials` pushes the branch and opens a draft pull request labeled `doctrine needs-human`, its body listing each denial's tool name and target path with terms redacted; the record's status is `denied`, never `success`. An error subtype (`error_max_turns`, any other) resets the clone, opens nothing, and records `error_<subtype>`. `--strict-mcp-config` keeps a repository's `.mcp.json` servers from connecting. | Open until A1; first reading on Nidhogg 2026-10-30 passed (A1) | The classifier keeps the run a success while guarding the destructive edge; a partial diff is evidence the reviewer needs, so it ships as a draft, not as silence (round 1 W2). |
| D6 | The image is `buildpack-deps:bookworm-scm` pinned by tag and digest, which ships git, curl and a CA store; `gh` arrives as a static binary in `~/bin` with a sha256 check; `jq` is not needed, since the tick parses JSON in Python. `SSL_CERT_FILE` is not set. | Resolved, from round 1 W10 | git has no official static Linux binary, and a third-party build run by an agent holding a GitHub token is an exposure the plan will not take. |
| D7 | Cut. The trust key in the account's config file lifts only the allow-rule warning, which auto mode makes moot; hooks and the `env` block run regardless. | Cut, round 1 S1 | A write per tick that buys silence. |
| D8 | The sweep neither builds a consumer's venv nor runs its tests. The repository's CI runs on the pull request (a D3 criterion); the pull request body states the CI result and that the adoption record's evidence reaches `written` and no higher; the reviewer merges on green CI and the diff. | Resolved | Simplicity First; a venv per consumer on a 512 MB app is the wrong trade; the CI criterion keeps the review from being a rubber stamp. |
| D9 | The watch is a second crontab line in the same App, with no model call. The hash check is deterministic Python; on a change it commits the register's new `last_fetch` block and a `difflib` unified diff of the page under a gitignored-text-free review file on a hub branch and opens a pull request. Triage (the surface map, the `--accept` verdict) is the lead's, at review on Nidhogg. | Resolved, the user 2026-10-29; the model call cut by round 1 S2 | The reviewer reads the diff; an agent-written summary beside it is a second thing to check, and the only model credential the watch would need goes away. |
| D10 | Records: one JSON line per tick per repository in a run-history file on the shared dataset: `at` (UTC), `tick`, `repo`, `status` (`idle`, `pending`, `refused`, `opened`, `denied`, `error_<subtype>`, `skipped`), `repos_listed`, `repos_present`, `repos_skipped`, `entries`, `denials` (tool names), `branch`, `pr_url`, `hub_commit`, `cli_version`, `model`, `num_turns`, `total_cost_usd`, `duration_s`, `terms_list_lines`, `terms_list_mtime`. The tick also appends to a log file in the clone, since the container's stdout retention in the UI is unknown. Session transcripts persist under the account's config directory with `cleanupPeriodDays` 3650. | Resolved; fields from round 1 W1 and W9 | paperboy's record shape with the picture's fields; the transcripts are CONOP SEXTANT's "transcripts in home storage" for this service. |
| D11 | `/session-start` on Nidhogg gains two measured lines, each with the two-shape contract: the age of the newest record line when the shared-dataset path variable is set, else `unchecked: <reason>`; and the count of open `doctrine` pull requests across the opted-in repositories by a `gh` search, or `unchecked: gh <error>`. Their gap rows ship with them in Wave 1, per the picture skill's "For a probe" procedure. The record's `at` against the hub's receipt time is the clock check. | Resolved | The hub reads the picture before asserting; a box with no self-report when dead needs the reader to measure its age. |
| D12 | Schedule: the watch at 03:40 daily, no model call; the sweep at 04:10 daily, a model call only for a repository with an unread notification and no pull request of this cycle. Both away from 05:30, 06:30, every `:00` and 20:30. | Resolved, minutes adjustable | The pattern's rule: two apps' model calls at different minutes, restarts away from scheduled minutes. |
| D13 | Check 7 is extracted to `scripts/private_terms_check.sh`, with a test pinning it byte-equal to the block `pcc.md` carries; the tick runs it and check 1's secret patterns (the OAuth token prefix, GitHub token shapes) over the branch's diff and over the pull request body before every push, refuses on a hit, and records the list's line count and mtime, never a term. The account holds its own list at the path the script reads, written by the lead over `scp`. | Resolved; the scope from round 1 W4 | The boundary line has been crossed within hours twice; the body goes through `gh`, which the index scan never sees. |
| D14 | No `.github` workflow in the hub. The GitHub Actions cron of the 2026-10-22 review stays the fallback if A7 fails. Cost: the hub's deploy script (1g) has no CI result to gate on, so it runs the hub suite on Nidhogg and refuses on a failure. | Resolved, the user 2026-10-29 | One mechanism for both threads; the 60-day inactivity rule and the hub's 52-day gaps were a poor fit anyway. |
| D15 | Work repositories are out of scope until G6 and G11 close. The work-terminal sweep, if any, is a CONOP DISPATCH cell on local inference, not this plan. | Resolved, the user 2026-10-29 | Anthropic does not support Claude Code against non-Claude models through any gateway; the work constraint is local inference. |
| D16 | Division of hands, urd's D11: the agent holds the `picket` account's key and nothing else, syncs files and runs read-only probes over the alias; the lead performs every web-shell, UI, token-minting, branch-protection and router step from a step list; every destructive command is the lead's. Every push from the box is the tick's own. | Resolved | The pattern that unstuck urd on 2026-10-26. |
| D17 | CLI pinned at 2.1.310 with auto-update off, as paperboy; the model pinned by name in the account's settings file to `claude-sonnet-5-5`, which is on auto mode's supported list (the user chose it on 2026-10-30, after the Nidhogg probe of A1 ran on it: 2 turns, $0.045, the classifier's calls billed on `claude-haiku-5-5`). The register's `headless.md` and `permission-modes.md` rows are the re-pin triggers: `--bare` is slated to become the `-p` default and reads no OAuth token, and the model list moves. | Resolved, the user 2026-10-30; the list check from round 1 S4 | The two documented changes that would silently kill the service. |
| D18 | Memory cap 512m to start. | Open until A4; first reading on Nidhogg 2026-10-30, 276 MB (A4) | paperboy's canary memory line was never read out; a Python tick peaked at 40 MB; the only CLI reading is the Nidhogg probe's, 276 MB for 2 turns, which leaves 236 MB under A4's threshold for a longer run. |
| D19 | No Slack line per tick. | Closed as no, round 1 S3 | One more place to leak a term; the pull request already lands where the reader looks. |

ADR filter: D2 reverses cleanly, D1 is the pattern's fourth instance, and no decision here is surprising with this document in hand. No ADR.

---

## Measures of Success

**MOP (performance)**

- The hub suite passes with the new tests selected: `.venv/bin/pytest -q -k "anthropic_sources or picket or private_terms"` with at least one test selected per keyword.
- Wave 0: every assumption A1 to A9 has a measured value in the session doc, none `unchecked`.
- Wave 2 canary: seven consecutive watch ticks with a record line each; first-seen stamped on every change seen.
- Wave 3 canary: three pull requests opened in one cycle; the tick after each opening writes `pending` and calls no model; zero private-term and secret-pattern hits across their diffs and bodies; the denial tool names recorded per repository.
- Every wave closes with a code-reviewer gate report in `docs/reviews/`.

**MOE (effectiveness)**

- MOE 1, decision latency: median days from a sweep pull request's opening to its decision, merge or close with a reason, across the opted-in repositories. Reference for calibration: the canaries' own historic pull requests from A6's probe, which must show the instrument ranking a request decided in days above one left open for a month before Wave 4 is gated on it. The lead measures it at Wave 3 close plus 30 days with `gh pr list --state all --label doctrine --json createdAt,closedAt`, and writes the value into this plan's Status Log; that entry is the trigger for the plan's terminal status.
- MOE 2, publish-to-review delay: median days from a guidance change's first-seen stamp to its `--accept` in the register, over the first six flagged changes; the 2026-10-22 review's C2 target is under 21. Measurable once six changes have been flagged, which at the measured cadence is three to six months; the lead records each in the register's review rows.
- MOE 3, adoption state: the fraction of opted-in repositories whose `.claude/doctrine-delivered` on the upstream `main` holds every hub heading, read by `gh api` from Nidhogg at session start. This is gap G3's collector for the opted-in set. Baseline at Wave 3 open; target 1.0 at Wave 4 close plus 30 days.

---

## Wave Breakdown

### Wave 0: The account, the tools, and the nine falsifiers

- **Team**: lead only, with the lead's hands for every UI, web-shell and GitHub-settings step (D16). The agent drafts each pasted line fully resolved in chat and reads the result back from the box.
- **Tasks**

  | Task | Purpose | Condition | Standard |
  |------|---------|-----------|----------|
  | 0a. Create the `picket` account by urd's D11 step list, with a new key pair for this service: `user.create` with the apps dataset as parent and `home_create`, the public key by database id in a second call, the traverse entry on the apps dataset, the full-rights entry on its own output folder of the shared dataset; the alias on Nidhogg. | The agent, so it has its one credential; the lead, so the account's damage ceiling is known. | Web shell as the owner account; the step list of 2026-10-26 with the three recorded traps beside each placeholder. | `getent passwd picket` prints; `id` over the alias shows one group and no docker; the key opens no other account's alias; `nfs4xdr_getfacl` on the apps dataset lists the account. |
  | 0b. Install into the home as the account: uv with the managed Python 3.12, supercronic v0.2.49 with its sha256, Claude Code 2.1.310 by the native installer, `gh` as a static binary with its sha256; the settings file with the model pin of D17, `DISABLE_AUTOUPDATER`, `cleanupPeriodDays` 3650. | Wave 1's scripts have a runtime to land on. | Login shell over the alias; nothing outside the home. | Each `--version` prints in a login shell and in a non-login shell with the deploy script's PATH export; `supercronic -test` prints valid. |
  | 0c. Mint this service's `setup-token` on Nidhogg and prove it there; create the service GitHub account; on each canary allow forking, add the account as a read collaborator, and enable `Run workflows from fork pull requests` with write tokens and secrets left off and the approval requirement off; fork the hub and the three canaries into the account; mint its classic token with the `repo` scope and an expiry; run A9 on one canary before the other two; build `.env.server` with both tokens and their renew-by comments; check without printing a value; `scp` once; `chmod 600`. | Both ticks can call the model and push to the forks, and no tick can push an upstream `main`. | The lead mints, clicks and copies whole lines; the agent sources the file in bash before it travels. | `claude -p "Reply with OK"` from `~` on the box with `.env` loaded prints OK; `gh auth status` as the account reports the token's scopes; A9's one-line pull request from the fork runs the canary's CI without waiting for approval, and `git push upstream main` from the fork clone is refused by GitHub. |
  | 0d. Write the account's private-term list at the path the check script reads, mode 600, by `scp` from the lead's own list. | D13 has a list to read. | The lead decides the list's contents; the agent records only its line count. | The check script run as the account prints no `WARN` and reports the count. |
  | 0e. Clone the four forks under the account's `~/projects/github/` from GitHub over HTTPS, with `upstream` set to the user's repository on each; the tick reads doctrine and the delivery mark from `upstream`, pushes to `origin`. | Wave 3 has its canaries; the clones carry the fork boundary. | Clones only; the committed mark comes with each clone. | `propagate_doctrine.py --dry-run` as the account lists exactly the three and nothing else; `git remote -v` in each shows `origin` on the account and `upstream` on the user. |
  | 0f. Run falsifiers A1, A3, A5, A7 and A8 by hand ticks as the account in a login shell on the host (A2 and A4 wait for the container in 0g; A6 was read on 2026-10-30; A9 is 0c's standard), each with its command and output pasted in the session doc; A1's tick also fixes `--max-turns`. | The waves that depend on each. | Read-only probes except the hand ticks, which run on scratch clones and push nothing. | Each Assumptions row carries a value, a time and the command. |
  | 0g. Draft the App YAML fully resolved in chat for the lead to paste: the D6 image by digest, user, hostname, working_dir, the home mount, `TZ`, `mem_limit`, `restart: unless-stopped`, the supercronic command on `deploy/picket/crontab`; no `env_file`. The first container tick runs A2's three commands and A4's memory read, and records whether the account's config directory is honoured inside the container. Keep a copy of the YAML in the lead's machine-local topology doc. Add the `picket` roster entry to `config/project.yaml`. | The App exists, its definition survives the UI, and A2 and A4 are measured where they apply. | The lead pastes; the agent reads `/proc/<pid>/environ` back the same minute. | The environment read back carries every variable and no token; the first tick lands within a minute of its schedule and its record line carries A2's and A4's values. |

- **Exit criterion**: every Assumptions row has a measured value; the App runs an idle tick that writes a record line.

### Wave 1: The scripts, test-first on Nidhogg

- **Team**: `feature-development` (python-prototyper, test-runner, code-reviewer).
- **Tasks**

  | Task | Purpose | Condition | Standard |
  |------|---------|-----------|----------|
  | 1a. The register: `docs/anthropic-sources.yaml` by the 2026-10-22 W1 schema, with the ten docs pages, the platform prompting page, the model deprecations page, `llms.txt`, and the four pages this plan rests on (permission modes, auto mode configuration, scheduled tasks, headless runs); `scripts/docs_watch.py` with `--check`, `--accept <id> --reason`, and the two-shape output; page text to a gitignored directory; the changelog as a version string, not a hash; gap row G13's pointer to the script, pinned by a test. | Gap G13's collector; the P1 register task. | Test-first with mocked fetches. | `.venv/bin/pytest -q -k anthropic_sources` passes with tests selected; `--check` offline prints one `unchecked` line per source and nothing that reads clean. |
  | 1b. `/session-start` step: run `--check`, print at most one line per changed source tagged `[measured: scripts/docs_watch.py --check]`, and the last-review age. | The pull half of the watch. | One step, after 3.7. | A session start prints the lines; a test over the command file pins the step. |
  | 1c. The tick: `scripts/picket_tick.py` with `sweep` and `watch` subcommands. `sweep`: pull the hub clone ff-only; run the D2 probe per listed clone and write `pending` or `refused` on a hit; run propagation; for each clone with an unread notification: fetch, reset to `origin/main`, branch, run the adoption prompt by D5, parse the result, apply D5's denial and error rules, run D13's checks over the diff and the body, commit, push, open the pull request with the record as its body, write the record line. `watch`: run `--check`; on a change, commit the register's fetch block and the unified diff on a hub branch, push, open the pull request, write the record line. Every subprocess env drops `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN`. The denial and error branches are contingent on A1's reading. | Both ticks exist as one tested program. | Test-first with a fake `claude` and a fake `gh` on PATH; no network in tests (the isolation tripwire). | `.venv/bin/pytest -q -k picket` passes with tests selected; a `--dry-run` on Nidhogg against a scratch clone prints the plan and opens nothing; a second dry run against a scratch clone with an open branch prints `pending` and no model command. |
  | 1d. The adoption prompt, `scripts/picket_adopt_prompt.md`: read the notification; apply each entry's Action Required for this repository's audience; skip an entry whose audience excludes this repository and say why; edit nothing the entry does not name; write an adoption record under `docs/sessions/` with a Claims table whose evidence is the diff and whose state is `written`; remove the notification file; stop. | The agent has one instruction per tick, versioned with the tick. | Written by the lead, challenged by the code-reviewer against the protocol's authoring rules. | The hand tick of 0f ran on this prompt and its record names what it applied and what it skipped. |
  | 1e. `propagation.auto_adopt` in `config/project.yaml`, read by the tick with the same slip-tolerant reading as `exclude`; the `picket` roster entry. | D3 and D1 have a home. | Test-first. | A listed name the box lacks prints `[warn]`; an unlisted clone prints `[skip]`; the state-block tests still pass. |
  | 1f. `scripts/private_terms_check.sh` extracted from `pcc.md` with the test that pins the two byte-equal; the secret-pattern check; the record-line schema and a reader that prints the newest line's age; `/session-start` step for D11's two lines with their gap rows. | D13 runs on the box; the heartbeat and the ledger exist with their gaps named. | Test-first; the share path comes from one environment variable with no default. | `pytest -q -k private_terms` passes; a session start on Nidhogg prints the two lines, or `unchecked` with the reason. |
  | 1g. `deploy/picket/`: the crontab, the deploy script by paperboy's shape (refuse non-main, dirty, unpushed, or a failing hub suite on Nidhogg; push to GitHub, pull ff-only on the box; proof by `--dry-run` of both subcommands, never a posting run; print the CLI version and the three renew-by comments). | The box runs what `main` holds, provably, with the suite as the gate CI would have been. | The executable bit pinned in the index by a test. | The script's proof step exits 0 on the box; its tests pass. |

- **Exit criterion**: the suite passes with the new tests selected; the code-reviewer's gate report lists no Critical finding.

### Wave 2: The watch, live

- **Team**: lead only.
- **Tasks**: 2a deploy by the script; 2b hand-run `watch` once as the account; 2c canary of seven ticks with a fixed checklist (a record line by 03:50 each day, `unchecked` lines only on fetch failures, first-seen stamped on any change, memory under the cap, no pull request unless a page changed); 2d if a change occurs in the window, the lead reviews the diff pull request and stamps `--accept` on Nidhogg, which is MOE 2's first data point.
- **Exit criterion**: seven of seven ticks with record lines, read out from the shell as the account after the window.

### Wave 3: The sweep canary on three repositories

- **Team**: lead only, the code-reviewer at the close.
- **Tasks**: 3a one hand-run `sweep --dry-run` then `sweep` as the account against a real unread notification (the cycle that carries entries H and P, or a seeded one); 3b cron live; 3c seven ticks: idle lines on days with nothing due, and after a pull request opens, a `pending` line with no model call every day until its decision; 3d the lead reviews each pull request at the next session: merge on green CI and the diff, or close with a reason in the pull request; 3e record per repository the denial tool names, the days to decision, and whether the adoption record's Claims held; 3f A5's pool read from the same window.
- **Exit criterion**: three pull requests opened in one cycle, each merged or closed with a reason, the `pending` lines present, zero private-term and secret hits, the gate report filed.

### Wave 4: Doctrine and the picture

- **Team**: lead, proposer on the entry's wording, code-reviewer on the entry.
- **Tasks**: 4a one doctrine entry for consumers: Step 3.6 gains the branch-or-pull-request gate; the opt-in rule and criterion and how a repository joins; the pull request body format; the `[skip]` behavior; 4b the gap register: G13 closed by the register with its pointer, G3 restated with the opted-in collector (MOE 3's probe), a row for "which hub commit the box ran" with the record line as collector; 4c the protocol's Cycle Anatomy step 6 and the consumer-side record; 4d a Status Log line in CONOP SEXTANT naming the box's transcripts as a source; 4e the first live cycle that carries 4a, delivered by the sweep itself.
- **Exit criterion**: the entry reaches the three opted-in repositories by the sweep and each pull request is decided; MOE 3's baseline and first reading are in the Status Log.

---

## What We Do NOT Build

- A `.github` workflow in the hub, unless A7 fails (D14).
- A Claude Code GitHub Action in any consumer.
- Cloud scheduled tasks, unless A1, A2 or A4 fails and stays failed.
- `bypassPermissions` in any tick, on any box, for any reason.
- Consumer venvs or test runs on the box (D8).
- An agent that writes doctrine entries, or a model call in the watch (D9).
- A sweep of work repositories or anything on the work terminal (D15).
- A watchdog service on the box; the session-start age line and its gap row stand in for it until a real outage defines the need.
- Any user interface beyond the pull request and the record file; no Slack line (D19).
- A shared token or a shared SSH key with any other app account, or any token in the App's YAML or environment.
- A write credential on any upstream repository: the service GitHub account holds write on its forks only, and no token of the user's travels to the box.
- A GitHub Pro dependency, unless A9 fails (the user's fallback of 2026-10-30).

---

## Agent and Team Design

None new. Wave 1 uses `feature-development`; each wave closes with a `code-reviewer` gate; the `proposer` challenges Wave 4's entry wording. The agent on the box is the `picket` account's key holder under D16, with the scope urd's `.claude/README.md` gives its own: read, sync, probe; never the owner account, never sudo, never a write outside the home.

---

## References

- `docs/reviews/20261029_picket_review.md`: round 1.
- `docs/reviews/20261022_anthropic_docs_feed_proposer.md`, `docs/reviews/20261022_anthropic_docs_feed_review.md`, `docs/reviews/20261022_anthropic_docs_inventory.md`: the register's design and sources.
- `docs/sessions/20261022_anthropic_docs_feed_and_prompt_audit.md`: the seven deferred decisions this plan resolves or supersedes.
- `docs/propagation-protocol.md`; `scripts/propagate_doctrine.py`; `scripts/adopt_doctrine.py`; `.claude/commands/pcc.md` checks 1 and 7.
- `docs/plans/conop_sextant_doctrine_evaluation_repository.md` (transcripts in home storage); `docs/plans/conop_overwatch_claim_verification_and_irreversible_guards.md` (the guards the classifier now carries by default).
- `.claude/skills/lake-conventions/HOME-STORAGE.md`: the boundary line, the roster gate and the server-side path form.
- Sibling records, read 2026-10-29 and redacted in two scratchpad findings files that were not committed: paperboy `deploy/README.md`, `docs/plans/conop_COURIER_daily_run_slack_delivery.md`, `docs/reviews/20261022_courier_claude_cli_headless_check.md`, sessions 2026-10-24 to 10-26; daily_weather `docs/runbooks/home-server-custom-app.md`, `docs/guides/local-models.md`, sessions 2026-10-02 to 10-12; urd `docs/plans/20261026_steplist_app_account_and_alias.md`, session 2026-10-26; stx-server session 2026-09-15; schelling-point sessions 2026-09-27 and 09-30.
- Claude Code docs, read 2026-10-29: permission modes, auto mode configuration, headless runs, CLI reference, authentication (`setup-token`), scheduled tasks, desktop scheduled tasks, LLM gateways, self-hosted environments, setup. The Docker library `buildpack-deps` README for D6.

---

## Status Log

- 2026-10-29: Draft written; sent to the code-reviewer for round 1.
- 2026-10-29: Round 1 returned GO-WITH-FIXES (2 Critical, 11 Warning, 7 Suggestion). Applied the same day: C1 the idempotency probe and the `pending` and `refused` lines (D2, 1c, 3c, MOP); C2 A1's kill-criterion abandons to Approach B or D and `bypassPermissions` is named out; W1 the turn cap and `num_turns` (D5, D10); W2 denials ship as a draft pull request labeled `needs-human` (D5); W3 a per-service SSH key, branch protection on `main`, the key's blast radius (D4, 0a, 0c); W4 check 7 extracted to a script and run with the secret patterns over the diff and the body (D13, 1f); W5 MOE 1 as decision latency with a named measurer, MOE 3 as the adoption state by `gh api`; W6 A6's falsifier runs today on the canaries' pull-request history; W7 A8 the apply-correctness falsifier and CI-on-pull-request in D3's criterion; W8 the hub suite as 1g's gate; W9 the record's picture fields and the two-shape session-start lines with their gap rows in Wave 1; W10 the image that ships git (D6, A2); W11 evidence lines under the Problem and the docs claims; S1 D7 cut and `--strict-mcp-config` added; S2 the watch's model call cut; S3 D19 closed; S4 the model named; S5 A2, A3 reshaped, A8 moved to 0e's standard and replaced by apply correctness, 1c's contingent steps marked; S6 Status In Debate, the Mission's two dates, wave headings without em dashes, 0e's seeding clause removed; S7 the roster entry and the no-snapshot decision (D1, 0g). Open for the user: D5 (until A1), D18 (until A4), the three canary names and D17's model.
- 2026-10-30: The 2026-10-29 files committed (`a836838`). The user ruled on three open items after measurements on Nidhogg: the canaries are `stx-server`, `schelling-point`, `hallmark` (D3; `propter` has no CI workflow); the write boundary is ownership, pull requests from forks held by a service GitHub account, because branch protection on a private repository needs GitHub Pro (D4, 0c, 0e rewritten; A9 added with the Pro upgrade as its fallback; D2's guard moved to the REST endpoint, since `gh pr list --head` takes no `owner:branch` form); the model is `claude-sonnet-5-5` (D17). First readings recorded against A1 (pass: four writes, three under `.claude/`, `permission_denials` present and empty), A4 (276 MB) and A6 (no canary has pull request history; `daily_weather`'s median decision is same-day). D5 and D18 stay open until the box readings.
