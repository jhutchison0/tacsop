# CONOP OVERWATCH — Claim Verification and Irreversible-Operation Guards

**Status**: Approved (2026-09-30; append-only from this point, changes land in the Status Log)
**Date**: 2026-09-30
**Lead**: jhutchison (session lead: Claude)
**Parent task**: `docs/tasks.md`, OVERWATCH line (added 2026-09-30)
**Evidence base**: a Claude Code Insights report (22 sessions, 345 messages, 2026-08-04 to 2026-09-28, run on a work terminal) and a second agent's recommendation built from it, both supplied by the user on 2026-09-30. Neither is in git: the report names work systems and this repo is public. A private copy sits in `docs/design/hold/overwatch_sources.md`, which `.gitignore:61` keeps out of every commit, on Nidhogg only. The incidents below are written as failure shapes. Debate round 1: `docs/reviews/20260930_overwatch_review.md` (`code-reviewer`) and `docs/reviews/20260930_overwatch_proposer.md` (`proposer`), blind to each other.

---

## Problem

The insights report names two failure classes that hub doctrine does not cover. The first is the overclaim: Claude reported success because nothing errored, not because anything proved it, in at least 6 of 22 sessions. A pipeline was called live when its engine had crashed on a schema mismatch; a mirror sync was asserted without a check; a venv was called unbuilt when it had existed on disk for weeks; a validation was reported twice without being run. The user or a review pass caught each one afterward, at the cost of a round trip. The second class is the operation that reaches past its scope: a test fixture let the suite delete about 138 GB of real cached data, a directory-wide `git add` swept unrelated in-progress files into a commit, and `uv pip install` under a stray `VIRTUAL_ENV` installed into a different repo's venv.

`shift-left-testing/ENFORCEMENT.md` logs and never blocks. The 2026-05-19 MAUT chose that for test-first on three counts: false positives, cheap bypass, and teaching over punishing. None of the three weighs a mistake that cannot be undone, and an overclaim is a reporting defect, not a coding one. Every downstream repo inherits the gap from the template.

---

## Situation

### Friendly Forces (what we have)

- **The kernel-plus-skill pattern, validated twice.** Prose Style (`writing-simple-and-direct`, 5 files, 329 lines) and Figure Style (`designing-clear-data-displays`) each put a short ambient kernel in `CLAUDE.md` with a directory-form skill behind it.
- **The enforcement gradient** in `ENFORCEMENT.md`. Layer 4 (PostToolUse audit) is live. Layer 5 (a Stop-hook diff audit for test-first) is named as the next candidate (`ENFORCEMENT.md:19-22`). Layer 6 (hard block on test-first) lost the 2026-05-19 MAUT.
- **A fail-closed gate already exists.** `scripts/lake_preflight.py` exits 1 on any FAIL (`lake-conventions/PREFLIGHT.md:13`), and `PREFLIGHT.md:44-60` states the hub's gate doctrine: prefer a WARN you can read over a FAIL you will learn to bypass.
- **A pattern for testing bash hooks from pytest.** `tests/unit/test_shift_left_hook.py` feeds the hook a JSON payload on stdin inside a throwaway git repo.
- **propter's fix for tests that reach the real world** (`docs/tasks.md`, P2, 2026-08-30): set env explicitly, stub `load_dotenv`, make HTTP client construction raise.
- **PCC check 6** warns when a hook or settings change is staged with other files and asks for a separate `[gate]` commit. It warns only (`.claude/commands/pcc.md:96`).
- **A review roster with a pre-flight record.** Pass 5 caught a BLOCKER (an invalid bash `case` alternation) in the 2026-05-19 entry before it shipped.
- **Harness permission rules that outrank the blanket `Bash` allow.** From `code.claude.com/docs/en/permissions`, read 2026-09-30: "Rules are evaluated in order: deny, then ask, then allow"; "a matching ask rule prompts even when a more specific allow rule also matches the same call"; ask rules apply "when any subcommand matches them, including a command nested inside a subshell", and still prompt "even in auto mode". The same page warns that a Bash rule "isn't a security boundary around the program": another invocation form slips past.
- **Python audit hooks see deletion and network from inside the test process.** Probed on Python 3.12.13: `Path.unlink`, `os.unlink`, and `os.remove` raise `os.remove`; `shutil.rmtree` raises `shutil.rmtree` first; `Path.rmdir` raises `os.rmdir`; `shutil.move` raises `shutil.move`; a subprocess `rm` raises `subprocess.Popen` with its argv; a socket raises `socket.connect`. `open(path, "w")` raises no deletion event.
- **The second agent's claims, re-run 2026-09-30:**

| Claim | How checked | Result |
|---|---|---|
| The report's sample hook blocks `rm -rf /tmp/scratch` | the hook verbatim, fed `{"tool_input":{"command":…}}` on stdin | exit 2: `jq` consumes stdin, so the `/tmp` grep reads nothing |
| It lets `rm -fr /data/grib` through | same | exit 0 |
| It misses `shutil.rmtree` | same, `python -c "import shutil; shutil.rmtree(…)"` | exit 0 |
| It lets `pytest` through | same | exit 0, a limit every Bash hook shares |
| It blocks `rm -rf /data/grib` | same (found by `code-reviewer`) | exit 2 |
| A stray `VIRTUAL_ENV` redirects `uv pip install` | `VIRTUAL_ENV=other/.venv uv pip install --dry-run --offline --no-deps six`, uv 0.12.1 | `Using Python 3.12.13 environment at: …/other/.venv` |
| `--python .venv` overrides it | same, plus `--python .venv -v` | `DEBUG Using Python 3.12.13 environment at: .venv` |
| `SETUP.md` recommends activating another env | grep | `python-venv-management/SETUP.md:42` |
| The template `conftest.py` has no tripwires | read, `wc -l` | 12 lines, Hypothesis profiles only (first draft said 11; corrected after `code-reviewer` re-ran it) |

### Enemy Forces (what works against us)

- **The model that overclaims decides whether to apply any probabilistic remedy.** A `/verify` command does nothing on the turns that need it most. This is the "Claude dice" problem `ENFORCEMENT.md:7` names.
- **A command-pattern guard sees only what Claude types.** The 138 GB deletion ran inside pytest, from fixture code Claude wrote earlier.
- **A monkeypatched guard has the incident's own hole.** Patching `shutil.rmtree` does not reach a module that ran `from shutil import rmtree` at import; `code-reviewer` reproduced the deletion going through, and the lead re-ran it.
- **A test that "fires on `/data`" proves nothing on a box without `/data`.** Nidhogg has none, so the call raises `FileNotFoundError` with no tripwire installed.
- **Free-text claim detection will misfire.** The 2026-05-19 MAUT weighted false positives at 0.20 on the record that "false-positive hooks get disabled within a week."
- **This repo is public**, and the incidents happened in work repos.
- **Nothing asks today.** `.claude/settings.json` sets `defaultMode: acceptEdits` and allows `Bash` outright.
- **Hub defects ship as fleet defects.** Propagation reaches 9 to 19 repos; the count is machine-local (`docs/tasks.md`, P1 fleet ledger). The notification ships only the newest entry (`docs/tasks.md`, P1 transport).

### Terrain (the ground we operate on)

- **`.claude/` is lead-write only.** The scope matrix in `.claude/README.md:82` gives `python-prototyper` no access there.
- **Downstream repos own their `conftest.py`.** A tripwire ships as one module and one registration line they add, never a file they overwrite.
- **The purpose gap is at task level only.** The CONOP Mission already requires an "in order to" clause. The TCS table (`.claude/commands/task.md:81`) has Task, Condition, and Standard, and no purpose.
- **`/session-start` Step 4 runs bare `pytest`**, which resolves through `PATH` and so through whatever venv is active.
- **44 `uv pip` lines in living docs name no target**: `python-venv-management/TROUBLESHOOTING.md` 16, `SETUP.md` 15, `CLAUDE.md` 5, `python-venv-management/SKILL.md` 4, `shift-left-testing/CI.md` 3, `README.md` 1.
- **The failure classes live in pipeline repos, not here.** 22 of the 27 hub commits since 2026-08-01 touched nothing under `src/`, `tests/`, or `scripts/`, so effectiveness can only be measured downstream. The incident transcripts are on the work terminal; Nidhogg is `scope: [personal]`.

### Assumptions

| # | Assumption | Cheapest falsifier | Blast radius if wrong | Kill-criterion |
|---|---|---|---|---|
| A1 | Overclaims are detectable from a turn's final message: success words with no supporting tool output in the same turn. The Stop input may carry `last_assistant_message` (docs, read by `code-reviewer`) | A 2-hour spike on the work terminal: replay the six incident turns and 20 clean session closes through a log-only detector | D8, Wave 3 | Fewer than 5 of 6 caught, or more than 2 of 20 clean closes flagged: no Stop hook |
| A2 | One Python audit hook catches deletion, subprocess `rm`, and non-loopback network from inside the test process, including names bound at import, without breaking legitimate tests | Task 1a's tests (below) plus the full suite armed | Wave 1 task 1a | The armed suite breaks more than 1 legitimate test in 100 here or in a downstream suite: fall back to a patched-API tripwire with an env opt-out |
| A3 | Ask rules prompt in the permission mode the work terminal runs, despite the blanket `Bash` allow | Live run on the work terminal: one `ask` rule, one matching compound command, in that terminal's mode; also note whether `bypassPermissions` skips it | Task 1e | No prompt in the work terminal's mode: a PreToolUse hook returning an ask decision, log-only first (Wave 3) |
| A4 | The ask patterns prompt rarely enough to stay in use | Offline replay: every Bash `tool_input.command` in existing transcripts (173 `.jsonl` files on Nidhogg; the work terminal's set) run through the patterns; counts only | Task 1e | More than 3 prompts per session on average: narrow the patterns before shipping |
| A5 | A blind multi-reviewer panel finds defects a single `code-reviewer` misses | Replay a defect a single review missed (the launch-control hook glob, `docs/tasks.md:38`) and one clean diff through one reviewer and through the panel | Wave 4 | The panel finds nothing the single reviewer missed: keep one reviewer and add a fail-open charter line only |
| A6 | An ambient kernel changes claim behavior | Task 2d's controlled replay | Wave 2 | The kernel arm flags fewer than 2 more incidents than the no-kernel arm: keep only the `Evidence:` line and the `## Claims` ledger |

---

## Mission

The hub lead, with the review roster, ships sealed test environments, ask rules on irreversible commands, and a claim-verification kernel into the template by 2026-10-16, in order to make every success claim carry evidence from the turn that makes it and to stop unrecoverable mistakes (deletion, wrong-target installs, swept commits) at a prompt or a tripwire rather than at the user.

---

## Approaches Considered

### Approach A: The report as written

A `/verify` command, five `CLAUDE.md` sections, the report's sample PreToolUse hook, and a ruff auto-fix PostToolUse hook.

- **Pros**: one session of work.
- **Cons**: `/verify` runs only when the overclaiming model chooses to run it. The sample hook shows three defects in the four probes above; the fourth, `pytest`, is a limit every Bash hook shares. The ruff hook would rewrite hub-owned files downstream before the P3 ruff decision is made.
- **Risk**: high. It ships a broken guard fleet-wide.

### Approach B: Layered defense (the second agent's recommendation)

A probabilistic kernel (`verifying-claims`) plus deterministic layers, each covering a gap the others cannot see:

| Layer | Sees | Cannot see |
|---|---|---|
| Kernel in `CLAUDE.md` | every claim, when the model complies | the turns it does not comply |
| `## Claims` ledger at `/session-end` | every claim the session reports, as a table a reader can audit | a claim made mid-session and never reported |
| Audit-hook tripwire under pytest | deletion and network from code that runs in the test process | commands typed into Bash; C extensions; overwrites |
| Ask rules in `settings.json` | commands typed into Bash, compound ones included | code that runs under pytest; another invocation form |

Smaller fixes come with it: install targets pinned in docs, tool checks at session start, and a purpose line in TCS.

- **Pros**: no single layer has to be perfect.
- **Cons**: more surface to maintain.
- **Risk**: medium.

### Approach C (bold): No kernel; an independent verifier only

Every `/session-end` hands its claims to a read-only verifier agent that never sees the reasoning. An auditor works from the ledger, not from the CFO's explanation.

- **Pros**: it removes self-assessment entirely, with one mechanism.
- **Cons**: it fires only at session end, and the crashed-engine overclaim was made mid-session, where the user acted on it. It costs one agent per session.
- **Risk**: medium.

**Recommendation**: B, with the debate's cuts. C's verifier stays available as an optional `/session-end` step that reads only the `## Claims` table.

---

## Design Decisions

### Resolved (2026-09-30, the lead's decisions after debate round 1)

- **D1. A kernel, not a command, in the slim shape.** `verifying-claims` is a directory-form skill (ADR-0001): `SKILL.md` with the kernel and the probe table inline, plus `EXAMPLES.md`. `ADOPTION.md` and `REVIEWING.md` are added only when a second repo asks. There is no `/verify` command and no second session-close skill.
- **D2. Four claim states plus freshness.** Written, tested, deployed, observed, because the crashed-engine incident is exactly deployed reported as observed. Every success claim carries an `Evidence:` line with output from the turn that makes it, or says `UNVERIFIED: <blocker>`. `/session-end` writes a `## Claims` table.
- **D3. Reversibility decides gating, and the gate is an ask.** Irreversible commands prompt the user through `permissions.ask` rules; nothing is denied at the hub. A consumer with a data volume may add its own deny. No ADR: a settings line is easy to reverse, so the decision fails the triple filter's first gate. If A3 fails and deny comes on the table, `decision-scientist` builds a new MAUT with irreversibility and false-block cost among its criteria; the 2026-05-19 MAUT is its template, not its instrument (`ENFORCEMENT.md:83-89` scopes a re-run to test-first data).
- **D4. Tests never touch the real world.** The primary design passes data roots in as parameters a fixture points at `tmp_path`, documented as a pattern in `ISOLATION.md`. The backstop is one audit-hook tripwire armed only while a test runs, allowed to delete under the system temp dir and the repo's `.hypothesis` and `.pytest_cache`, extended per repo through one pytest ini option, and logging each catch to `.claude/audits/isolation-tripwire.log`.
- **D5. Install commands name their target.** `uv pip … --python .venv` across every living doc (works on Windows, unlike `.venv/bin/python`). `SETUP.md:42` loses the "activate that env first" route.
- **D6. Incidents are written as failure shapes**, never under work-system names. The measurement repo is named by alias only.
- **D7. Not shipped**: the report's sample hook, its ruff hook, and a bash PreToolUse guard (ask rules replace it unless A3 fails).
- **D8. The Stop-hook detector is out of committed scope.** A1 runs as a 2-hour spike. A hook is built only if the spike clears A1's bar and the ledger still shows overclaims after the kernel ships.
- **D9. The TCS purpose line ships in Wave 1**: who gets the output, and what decision it informs.
- **D10. Two kernel rules come from incidents the first draft missed**: a claim of "deployed" requires a clean tree (`git status --porcelain` empty), because half-finished code was picked up by a live timer; and verification probes are read-only, because a verification run wrote the wrong data into a production cache.

### Deferred, with rationale

- **O4. The blind review panel** waits for A5. If built, it is a new `merge-review` template beside `code-review`, not a replacement. Debate round 1 is one data point: the two reviewers shared four themes and otherwise found different things, which argues for distinct charters more than for blindness.
- **O6. Propagation**: one doctrine entry per wave, each propagated before the next is written, unless the transport fix (`docs/tasks.md`, P1) lands first. Batching Rule 2 rules out one entry for all waves. Task 1c changes Step 4's default command and is marked breaking (Rule 4).

---

## Measures of Success

**MOP (performance)**

- Every guard ships with a test that reproduces its incident shape and fails closed. The plan closes with a table: incident shape, guard, catching test.
- The full suite is green at each gate, with the tripwire armed.
- `code-reviewer` returns GO or GO-WITH-FIXES at each gate, with all fixes applied.
- Check 5's grep and its directory pass report 0 MISSING over `git diff --name-only main...` for each branch.
- The Wave 2 replay passes task 2d's Standard. It is a regression check: the six shapes wrote the kernel.

**MOE (effectiveness)**

- **The overclaim rate falls.** Counted by the `## Claims` ledger line `Overclaims the user caught this session: N` in one work repo (alias in the Status Log), over 20 sessions after adoption, against that repo's own pre-kernel rate from the same Insights instrument. Reported as a rate with its interval, not as pass or fail: at 10 sessions a zero-count bet passes 23% of the time under a real halving and 4% under no change, so it cannot confirm anything short of elimination. Measurable no sooner than seven weeks after adoption: the work terminal ran 22 sessions in 56 days across all repos, so one repo takes longer.
- **No unrecoverable incident in the same window.** The tripwire log shows each catch. A window with zero catches and zero incidents says nothing about the guard, and gets reported that way.

---

## Wave Breakdown

Waves 0 to 2 are detailed. Waves 3 and 4 stay at sketch level until A1, A3, and A5 report. Each wave closes with its own doctrine entry (O6).

### Wave 0 — Falsifiers

- **Team**: lead only, mostly on the work terminal.
- **Tasks**:

  | Task | Condition | Standard |
  |------|-----------|----------|
  | 0a. Commit the 2026-09-18 entry | Three modified files on `main` | Done 2026-09-30 (`d4ac4e4`), committed by path; `git status --short` afterward listed the same untracked files as before |
  | 0b. Run A3 | The work terminal, in its own permission mode | Prompt observed or not for one `ask` rule on a compound command; `bypassPermissions` behavior noted; Status Log records the result and the Claude Code version |
  | 0c. Run A1 | The work terminal's transcripts, 2 hours | Counts on the six shapes and 20 clean closes in the Status Log; no transcript text in this repo |
  | 0d. Run A4 | Transcripts on both machines | Prompts per session for each proposed pattern, counts only |

- **Exit criterion**: 0b to 0d results are in the Status Log. Tasks 1a to 1d do not depend on Wave 0; 1e does.

### Wave 1 — Independent fixes, one branch each

- **Team**: the lead implements; `test-runner` and `code-reviewer` review each branch at its gate. The lead writes 1a because its design choices (the armed window, the allowlist, the import-time dotenv patch) carry the incident's risk; `python-prototyper` would have no `.claude/` access for `ISOLATION.md` anyway.
- **Tasks**:

  | Task | Condition | Standard |
  |------|-----------|----------|
  | 1a. Sealed test environment (`topic/overwatch-sealed-tests`) | `tests/isolation.py`, registered from `tests/conftest.py` by one line; `ISOLATION.md` sidecar in `shift-left-testing` | Each tripwire test narrows the allowlist, targets a sentinel outside it (never `/data`), asserts the tripwire's own exception class, and asserts the sentinel still exists. Cases: `Path.unlink`, `shutil.rmtree` through a name bound at import, `os.rmdir`, a subprocess `rm`, a non-loopback `socket.connect`. `load_dotenv` is a no-op for the repo's real `.env` and passes through for a path under `tmp_path`. A catch appends one line to the tripwire log. `ISOLATION.md` lists what the tripwire cannot see. The full suite passes armed. |
  | 1b. Pin install targets | Every living doc in `CLAUDE.md`, `README.md`, and `.claude/` | `grep -rnE 'uv pip (install\|sync\|uninstall)' CLAUDE.md README.md .claude/ \| grep -v -- '--python'` prints nothing. `grep -rn 'VIRTUAL_ENV=' .claude/skills/python-venv-management/` prints nothing. The scratch repro, re-run with the documented command, reports `.venv`. |
  | 1c. Tool checks at session start | `/session-start` Step 4 | Reports git identity, a `VIRTUAL_ENV` that is not this project's `.venv`, and `gh` or `glab` auth when the CLI is installed, each with the step it blocks. Runs `.venv/bin/pytest` (Windows: `.venv\Scripts\pytest`). Marked breaking in the entry. |
  | 1d. TCS purpose line | `.claude/commands/task.md:81` | The TCS table gains a Purpose column: who gets the output, and what decision it informs. `CONOP-FORMAT.md` and `OPORD-FORMAT.md` task tables match. |
  | 1e. Ask rules | `.claude/settings.json`; after 0b and 0d | `permissions.ask` covers `rm` with recursive flags, `git add -A`, `git add .`, `git add -u`, `git commit -a`, `git clean`, and `mc rm`, as tuned by A4. Ships alone as a `[gate]` commit. |

- **Exit criterion**: each branch merged after `code-reviewer` GO and deleted (local and origin).

### Wave 2 — The `verifying-claims` kernel

- **Team**: the lead writes. `proposer` stress-tests the kernel wording; `code-reviewer` reviews at the gate.
- **Tasks**:

  | Task | Condition | Standard |
  |------|-----------|----------|
  | 2a. `SKILL.md` | ADR-0001 directory form; D1, D2, D10 | Under 110 lines. The kernel has at most 6 rules. The probe table holds one read-only probe per claim type: run landed (exit code, log tail, an output newer than the launch), pushed (`git ls-remote` against the local SHA), mirror synced, tests pass (this turn's summary line, on CI's Python), venv exists (`pyvenv.cfg` and `python -V`), merged, deployed (clean tree). |
  | 2b. `EXAMPLES.md` | D6 | Six before/after pairs, one per incident shape, plus this plan's own line-count slip (11 claimed, 12 measured). No work-system names. |
  | 2c. Wiring | One commit per gate surface | Kernel in `CLAUDE.md`; `Evidence:` line and `## Claims` table in `/session-end`, sequenced after the WHETSTONE capture-point task (`docs/tasks.md`, P1) that edits the same file; a `code-reviewer` checklist line, reviewed by a non-author. Registered in: `SKILLS_FRAMEWORK.md` Level 0 block, `SKILLS_FRAMEWORK.md` inventory tree, `.claude/README.md` tree, `CLAUDE.md`. |
  | 2d. Controlled replay | The work terminal; six incident turns and at least six clean turns, held out from `EXAMPLES.md` | Each turn runs twice on the same model, with and without the kernel. A non-author scores each final message flagged or not. Pass: the kernel arm flags at least 5 of 6 incidents, at most 1 of 6 clean turns, and at least 2 more incidents than the no-kernel arm. |

- **Exit criterion**: 2d passes and `code-reviewer` returns GO.

### Wave 3 — Conditional deterministic layers (sketch)

- A Stop-hook claim audit, log-only, only if A1's spike clears and the ledger still shows overclaims (D8). It is a separate hook from `ENFORCEMENT.md`'s Layer 5 diff audit.
- A PreToolUse hook returning an ask decision, only if A3 fails. Written test-first; the four sample-hook probes become its tests, with `pytest` recorded as a pass-through that documents the shared limit.

### Wave 4 — Review panel (sketch)

- The `merge-review` template, only if A5's replay shows the panel finding a defect a single reviewer missed (O4).

---

## What We Do NOT Build

- A `/verify` slash command or a second session-close skill.
- The report's sample hook, its ruff auto-fix hook, or a bash PreToolUse guard unless A3 fails.
- ADR-0003: the ask-rule decision is easy to reverse.
- A hard block on test-first. `ENFORCEMENT.md` Layer 6 stays declined.
- A commit check that guesses a task's scope from prose. The ask rules check argument form only.
- Delete guards for object stores at the hub beyond `mc rm`. That is `lake-conventions` ground.
- Any change to WHETSTONE's instruments.

---

## Agent and Team Design

No new agents. Wave 4 may add a team template; if it adds an agent, its scope-matrix row is written before implementation.

| Stage | Agents | Why |
|---|---|---|
| Debate round 1 (done) | `proposer`, `code-reviewer`, blind to each other | The blast radius is fleet-wide |
| Each Wave 1 branch | `test-runner` and `code-reviewer` at the gate | The template reaches every downstream suite and settings file |
| Wave 2 | `proposer` on the kernel wording; `code-reviewer` at the gate | The kernel is ambient text in every repo |
| Deny, if A3 fails | `decision-scientist` | A decision model is then in scope |
| Each doctrine entry | `code-reviewer` pre-flight | Entries ship fleet-wide |

Reviewers can overclaim too. Every finding must cite a file, a line, or command output (`.claude/README.md` principle 2), and the lead re-runs any finding before acting on it.

---

## References

- `.claude/skills/shift-left-testing/ENFORCEMENT.md`: the gradient, Layer 5, and the scope of the Layer 6 re-evaluation rule
- `docs/reviews/20260519_pass4_enforcement_maut.md`: the template for any deny MAUT
- `.claude/skills/lake-conventions/PREFLIGHT.md`: the hub's existing gate doctrine
- `.claude/skills/writing-simple-and-direct/`: the kernel shape D1 slims
- `docs/adr/0001-directory-form-mandatory-for-new-skills.md`
- `docs/plans/conop_whetstone_recursive_doctrine_loop.md`: the falsifiable-bet pattern and the session-count collision
- `docs/tasks.md`: the propter dotenv lesson (P2), git identity (P3), ruff adoption (P3), the transport fix (P1)
- `docs/propagation-protocol.md`: batching Rules 2 and 4
- `code.claude.com/docs/en/permissions`: rule precedence and compound-command matching, read 2026-09-30

---

## Status Log

- **2026-09-30**: Drafted, In Debate. The second agent's claims re-run on Nidhogg: 8 of 8 hold. `proposer` and `code-reviewer` dispatched blind to each other.
- **2026-09-30, debate round 1**: both reviewers return GO-WITH-FIXES. `code-reviewer` re-ran 29 Situation claims and refuted 1: `conftest.py` is 12 lines, not 11. It found four more statements that said more than their sources: PCC check 6 "requires" (it warns), the hub's "only" enforcement doctrine (the lake preflight is a fail-closed gate), "failed 4 of 4" (three defects and one shared limit), and three citations of `ENFORCEMENT.md` for a MAUT re-run rule it scopes to test-first. The lead re-ran each and corrected all five. The plan's first draft overclaimed five times, and an independent re-run caught all five.
- **2026-09-30, approved**: the lead chose ask rules over a bash hook (D3), four claim states plus freshness over the proposer's three (D2), and to start Wave 1 this session. The rest of the debate folded in: the audit-hook tripwire (both reviewers, independently), the calibrated replay (C1), the tripwire test Standard (C2), deferrals with rationale (W2), one branch per change (W4), the downstream module (W5), work-terminal falsifiers (W6), a calendar date (W7), the ledger-based rate (W8, proposer §4), markable Standards (W9), and per-wave entries (W11). Not adopted: the proposer's deferral of the `glab` check, because an unauthenticated `glab` blocked verification in 2 sessions. The 2026-10-16 date is the session lead's placeholder; the user may move it.
- **2026-09-30, task 1a gate**: `code-reviewer` returned GO-WITH-FIXES, with 3 Critical, 9 Warning, and 11 Suggestion findings (`docs/reviews/20260930_overwatch_1a_gate.md`). Of those, `test-runner` independently found C3, a test that fails under `CI=true`. The lead re-ran each Critical before fixing it. Fixes went in test-first, and the tripwire tests grew from 17 to 37. Four changes to the approved plan: (1) Task 1a's Condition "registered from `tests/conftest.py` by one line" becomes "registered through `addopts = ["-p", "tests.isolation"]` in `pyproject.toml`", because pytest runs a whole conftest before it reads `pytest_plugins` (C2). (2) D4's allowlist drops `.pytest_cache`: the plugin builds the cache directory at configure time instead, and `--basetemp` joins the roots (W5, W6). (3) Arming collection (W3) is not adopted. Collection imports libraries that build caches at import time, so collection stays a listed limit. (4) The Wave 1 exit reads: GO, or GO-WITH-FIXES with every fix applied and the reviewer's own probes re-run against the fixed branch (S10). W8 stays PARTIAL: the ask rules (1e) write no log, so MOE 2 counts tripwire catches only. The lesson for the gate checklist: the lead's own runs never set `CI=true`, and GitHub Actions sets it in every downstream repo that copies `CI.md` (the hub itself has no workflow yet). Any change that touches Hypothesis or test configuration runs the suite both ways.
- **2026-09-30, task 1a gate rounds 2 and 3**: round 2 (on `28e8482`) found 0 Critical and 4 Warning. Two of the four were regressions or omissions the round-1 fixes introduced: the new DNS checks tripped on this machine's own hostname, and the doc rewrite dropped the `dir_fd` limit while the code still skipped it. Commit `393d640` fixed all four. Its message says "each fixed test-first", which overclaims (round 3, R3-S3): two fixes had tests written first (own hostname, `dir_fd` through `/proc/self/fd`), and two were doc-only (the matplotlib false-catch class, the module docstring). Round 3 (on `393d640`) returned **GO**: no probe fail-open and unlisted, 27 of 30 mutants killed. The three survivors: M7 (never disarm, stated in its test), plus M16 and M26, which `/proc` masks on Linux and which two tests now pin. Round 3 also corrected the lead's False Catches paragraph, measured against matplotlib 3.11.1. A stranded lock makes every later import wait about 5 seconds and skip saving the cache, rather than stopping. And patch releases reuse the cache file. The Wave 1 exit for task 1a is met. Final state: 351 passed with and without `CI=true`, 0 catches in the real log, 43 tripwire tests on Python 3.11.15 and 3.12.13.
- **2026-10-01, tasks 1b to 1d**: task 1a merged alone (`d03e66a`) after its GO. Tasks 1b, 1c, and 1d share one branch, `topic/overwatch-template-docs`. That departs from "one branch each": the lead chose it so the batch ships as one doctrine entry. The cost showed at once: 1c's new line broke 1b's grep, and only the review saw it. One `code-reviewer` pass returned GO-WITH-FIXES: 0 Critical, 7 Warning, 12 Suggestion (`docs/reviews/20261001_overwatch_1b_1d_review.md`). Two Warnings were the lead's own overclaims. The tool-check block exited 1 when all was well (W1). And commit `7428d33` claims "both Standard greps print nothing" while grep 2 matched a version line written after the grep ran (W2). All seven Warnings are fixed. Ten Suggestions were applied in whole or part. S9 and part of S7 were filed as tasks, and S3's per-forge CLI check was declined for its complexity; the new wording covers its offline case. The 1c Standard's "the step it blocks" is read as "the step or activity": the stray-env line names every `uv pip` command. While probing, the reviewer ran `uv cache clean six` against the real uv cache, then restored it; the lead verified the restore with an offline dry run. A reviewer writing outside the scratchpad is the scope class this plan guards against. No proposed ask rule covers cache commands, so the lesson goes to task 1e and to any Wave 4 reviewer charter: a review agent writes only its report and scratch files.
- **2026-10-01, merged and release shape reopened**: 1b to 1d merged (`d98428a`) after review round 2 returned GO; a CDPATH false flag from its notes was reproduced and fixed first. The plan to ship 1a to 1d as one entry with 1c "marked breaking" (this log's 1b to 1d entry, and `docs/tasks.md`) conflicts with `docs/propagation-protocol.md`. Rule 4 gives a breaking change its own entry, and 1c changes Step 4's default test command. Rule 2 forbids mixing unrelated changes, and the tripwire, the install pin, and the Purpose column are separable. The script also ships only the newest entry, while 08-27, 08-30, and 09-18 are still unsent. The release shape is open until the lead decides it, together with the transport task.
