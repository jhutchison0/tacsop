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
- **2026-10-01, Wave 2 tasks 2a to 2c drafted on Nidhogg; release held**: the user reviewed Wave 1 and chose to hold every OVERWATCH entry until 1e and Wave 2 are done, so downstream repos get the plan in one cycle, not three. Tasks 2a to 2c sit on `topic/overwatch-verifying-claims`; 2d and 1e still need the work terminal, so the Wave 2 exit criterion is not met and cannot be met from this box. **Sequencing**: the WHETSTONE capture point went first on its own branch (`d565df9`, fixed in `1ed229c`), as 2c's Condition requires. Its review found that the task line's second half, Step 5.5 in the template, is WHETSTONE Wave 4 surface; the user chose to hold it, and only the `KB-graph:` reminder shipped (WHETSTONE Status Log, same date). **Test-first**: `tests/unit/test_verifying_claims.py` pins each markable Standard (the 110-line cap, the six-rule cap, seven probe rows, seven pairs, the registration surfaces, the `## Claims` table) and one thing the Standards do not name: the kernel in `CLAUDE.md` must equal the kernel in `SKILL.md`, rule for rule. Each test was red before its edit. **Kernel wording**: `proposer` returned SHIP-WITH-FIXES (`docs/reviews/20261001_overwatch_kernel_wording.md`); the lead re-ran its five checkable findings and all five reproduce. Two of them were the lead's own errors: example pair 1 pasted an `exit=1` that `tail` cannot print, and the pushed and mirror probes read an empty `git ls-remote` as a match. Four places where the shipped wording refines an approved decision: (1) D10's clean-tree rule reads "a checkout that runs code is deployed only when clean". As D10 words it ("a claim of deployed requires a clean tree"), the rule voids every push claim in a repo with untracked files, and `git status --porcelain` prints five in this one; a push rests on ref SHAs, and the incident was a timer reading a dirty checkout. (2) D2's freshness rule reads "this turn, after your last change": a test run before a later edit in the same turn is from this turn and still stale. (3) D2's "every success claim" is bounded to "each claim a reader will act on", with a plan, an opinion, and a diff shown in the same message named as not claims. Task 2d fails a kernel that flags more than 1 of 6 clean turns, and the unbounded form puts a line under every sentence. (4) Task 2b's Standard is six pairs plus the line-count slip; `EXAMPLES.md` adds one clean report after the seven, for the same reason. Not adopted from the proposer: folding the read-only rule into rule 3 to make room to split rule 4 (D10 names it as a kernel rule; rule 4 was instead cut to one idea), and cutting pair 7 (2b's Standard requires it; its last sentence, which taught probing every number, is reworded). The approach C verifier stays unbuilt: `SKILL.md` says in one line that a weak check honestly labeled, or invented output, passes the letter, and that a reader or a second agent closes that. **2c surfaces**, one commit each: the kernel block and registry entries (`cbd2ef5`), the `code-reviewer` checklist line alone as `[gate]` (`1edf0d4`), `/session-end` and the format doc (`d1614fc`). State before the gate: 421 passed with and without `CI=true` (403 on `main`, 15 in the new file, 3 capture-point pins).
- **2026-10-01, Wave 2 gate, round 1**: `code-reviewer` returned GO-WITH-FIXES for tasks 2a to 2c: 1 Critical, 16 Warning, 15 Suggestion (`docs/reviews/20261001_overwatch_wave2_gate.md`). All three task Standards held by the reviewer's own count, and `test-runner` matched the lead's suite numbers. The lead re-ran C1, W2, W3, W5, and S1 before fixing; all five reproduce. Fixes: `1b50924` (the three gate surfaces, tagged `[gate]`) and `6bde122` (the skill, the examples, the ambient block, the tests). **The lead's errors this gate caught**: `SKILL.md` said the read-only rule "holds" for tests through the tripwire, which does not see overwrites (C1). The ambient block exempted plans, and the unbuilt-venv incident is a plan (W1). The Pushed row held with uncommitted work, and a bare branch name in `git ls-remote` matches `feature/<branch>` (W2). Example pair 1 taught a probe with a silent default: `systemctl show` prints `ExecMainStatus=0` for a unit that does not exist (S1). Pair 7's evidence line printed 16 at HEAD, not 12 (W5). The reviewer checked 41 of the lead's claims: 30 hold, 10 cannot be re-run, and 1 is refuted in part. The refuted one is this log's previous entry, "pins each markable Standard": six mutants each cut an element a Standard names and left all 15 tests green (W14). The pins are tightened to 25 tests, and the test file's docstring names the two requirements no test holds: read-only, and no work-system names. One more error the lead caught itself: `1b50924`'s message said the tests pass before they had been run on that tree; it was amended to cite the run, with the tree unchanged. **Changes to the approved plan, for the user to confirm at merge** (S8, W10): (1) rule 5 now reads "a checkout a timer or service runs from is deployed only when clean", narrower again than the previous entry's wording, because "a checkout that runs code" fits any repo with tests (S6). (2) Rule 4's bound, "each claim a reader will act on", now stands on every surface, the ledger included (W9). (3) The ledger count is defined: N counts a claim made to the user that proved false after the user corrected it or asked about it. A claim a reviewer's re-run refuted first goes on a second line, `Overclaims a reviewer caught this session: M`, and is not in N. The MOE reads N only. The second line is the lead's addition. **Decided**: commit messages stay in the skill's scope (W13). The seven commits before the gate carry no `Evidence:` line and keep their SHAs, which two review reports cite; from `1b50924` on the messages carry them. `d1614fc` added the MOE's instrument under an `[infra]` tag; under WHETSTONE D4 it is a gate change, and this gate is its non-author review (W16). **For the release entry** (W15): the new tests expect `docs/session-doc-format.md`, the Step 5 heading in `/session-end`, the `SKILLS_FRAMEWORK.md` block, the reviewer line, and the `CLAUDE.md` block; the reviewer found the format doc absent in 3 of 15 sibling repos and the heading in 1, so Action Required must say to take all five surfaces with the tests. **Not adopted**: a Windows form in the Tests row (S2, for table width); S12 (`d2cdaf8` cites a review file that enters the tree one commit later; a record, not a defect to fix). Rule 2 still asks for a re-run at every report (the proposer's defect B, the reviewer's S6): that is D2 as approved, and 2d will show its cost on clean turns. Tests pass (tested), 431: 403 from `main`, 25 in the skill's file, 3 capture-point pins.
  Evidence: `.venv/bin/pytest -q` → `431 passed, 1 warning in 3.98s`, `exit=0`; `CI=true .venv/bin/pytest -q` → `431 passed, 1 warning in 5.31s`, `exit=0`; `.venv/bin/python -V` → `Python 3.12.13`; at `6bde122`. The hub has no CI config.
  Evidence: on Python 3.11.15, in a scratch venv with the dev extras, `python -m pytest -q` → `393 passed, 5 skipped, 1 warning in 1.94s`, `exit=0`, and the same counts with `CI=true`. The 5 skips are the matplotlib and pandas tests; neither library is in the dev extras. `6bde122`'s message calls this run UNVERIFIED; it was a skipped check, and the lead then ran it.
  Disclosure: that scratch install was editable, and it rewrote the gitignored `myproject.egg-info/` in the repo root. `git status --porcelain` lists no tracked file.
  The Wave 2 exit criterion is still open: task 2d needs the work terminal.
- **2026-10-01, Wave 2 gate, round 2: GO for tasks 2a to 2c.** C1 and 14 of 16 Warnings closed; W13 and W15 partial, both closed by this entry. The reviewer's round 1 mutation set went from 25 of 46 killed to 41 of 46. Its new set, 23 mutants that each revert one round 1 fix, killed 5; `278a426` adds four pins for the reverted probes, and the rest are wording a test cannot judge. Of 45 new claims by the lead the reviewer found 41 hold, 2 cannot be re-run, and 2 refuted in part, both in the previous entry. First: "from `1b50924` on the messages carry them" was false for two claims in `6bde122`, whose evidence is below. Second: "the new tests expect five surfaces"; there are six, and the sixth is `.claude/README.md`, which must name the skill. The release entry's Action Required lists all six. One correction to the 3.11 line: "5 skipped" is 38 tests that did not run, because two of the five skips are whole modules (431 minus 393). All 28 tests in the two new files ran there. Records, no action: `1b50924` holds two gate surfaces in one commit, against 2c's "one commit per gate surface" (R2-S7); the reflog holds `1b50924`'s pre-amend commit `4893bd7` with the same tree and parent, so the amend changed the message only. Applied in `278a426`: R2-S1, R2-S3, R2-S4, R2-S5. Open until the user rules on the second count line: R2-S2 (`SKILL.md` says "one count"; a claim refuted after the user relied on it falls in neither count). A watch item for 2d, from the reviewer: "the belief a plan rests on is one" may raise the flag rate on clean turns.
  Evidence, for "seven of the new pins were red against the unfixed text" (`6bde122`): the reviewer ran the new test file on `2e33662`'s tree → 7 failed; the lead's own run before the fixes → `7 failed, 18 passed in 0.04s`.
  Evidence, for "all five reproduce": `sed -n 71p .claude/skills/shift-left-testing/ISOLATION.md` → `- **Overwrites and moves.** ...` (C1); in a scratch remote holding only `feature/main`, `git ls-remote origin main` → `7043fef... refs/heads/feature/main`, `exit=0` (W2); `find . -maxdepth 3 -name pyvenv.cfg` → `./.venv/pyvenv.cfg` (W3); `wc -l tests/conftest.py` → `16 tests/conftest.py` (W5); `systemctl show no-such-unit-xyz.service -p ExecMainStatus` → `ExecMainStatus=0`, `exit=0` (S1).
  Evidence, for "`test-runner` matched the lead's suite numbers": its report to the lead, at `f100c2b` on Python 3.12.13 → `421 passed, 1 warning`, `exit=0`, with and without `CI=true`. The report was a message, not a file; nothing in the repo holds it.
  Tests pass (tested), 431. Evidence: `.venv/bin/pytest -q` → `431 passed, 1 warning in 4.64s`, `exit=0`; `CI=true .venv/bin/pytest -q` → `431 passed, 1 warning in 5.58s`, `exit=0`; `.venv/bin/python -V` → `Python 3.12.13`; at `278a426`.
  The Wave 2 exit criterion is still open: task 2d needs the work terminal.
- **2026-10-01, the user's four decisions at the Wave 2 gate.** Asked through the harness's question tool; each answer is the option label the user chose. (1) Merge: "Merge both now (Recommended)". Tasks 2a to 2c merge to `main` before 2d runs, so the work terminal can pull them; nothing propagates, and the Wave 2 exit criterion stays open. (2) Rule 5: "Keep narrow (Recommended)". D10 now reads: a checkout a timer or service runs from is deployed only when clean. (3) Rule 4: "Keep bound (Recommended)". D2 now reads: each claim a reader will act on carries an `Evidence:` line or `UNVERIFIED: <blocker>`. (4) Ledger: "Two lines (Recommended)". The MOE reads N, `Overclaims the user caught this session: N`: claims made to the user that proved false and that the user corrected, asked about, or had already relied on. M, `Overclaims a reviewer caught this session: M`, holds every other claim a reviewer's re-run refuted (`447a459`, which closes R2-S2). Earlier the same day the user also chose to hold every OVERWATCH entry until 1e and Wave 2 are done, and to hold WHETSTONE's Step 5.5 for its Wave 4. What remains of the plan: 0b to 0d, 1e, and 2d on the work terminal, then the release.
- **2026-10-01, Wave 2 gate, round 3: GO for merge.** The reviewer checked `447a459` as its non-author reviewer under WHETSTONE D4. N and M are disjoint and the four surfaces agree; the pin fails 6 of 6 rewordings. All round 2 items are closed. Mutation at `fcf63c3`: 61 of 81 non-equivalent mutants killed. Two more of the lead's claims are refuted in part (R3-W1). First, `447a459`'s subject says every refuted claim lands in one count: a claim its author retracts alone lands in neither, and so does one a tool refutes. `c58e69e` says so in `/session-end`, in the reviewer's wording, and pins the definitions the user ruled on. Second, the round 2 entry says the release entry's Action Required "lists all six" surfaces. No release entry exists yet; the sentence states a requirement for one. `docs/tasks.md` carries it on the OVERWATCH line. `c58e69e` changes a gate surface after the last review round. Its text is the reviewer's own and no fourth round was run. Totals for this gate across three rounds: 1 Critical, 18 Warning (16, 1, 1), 25 Suggestion (15, 7, 3). The reviewer listed 86 of the lead's claims in rounds 1 and 2 (41 and 45) and refuted 3 in part; round 3 refuted 2 more in part. The lead's first draft of this line said 26 Suggestions and "5 of 86"; a count of the report's headings caught both before the commit.
  Tests pass (tested), 432: 403 from `main`, 26 in the skill's file, 3 capture-point pins. Evidence: `.venv/bin/pytest -q` → `432 passed, 1 warning in 4.29s`, `exit=0`; `CI=true .venv/bin/pytest -q` → `432 passed, 1 warning in 5.27s`, `exit=0`; `.venv/bin/python -V` → `Python 3.12.13`; at `c58e69e`.
- **2026-10-05, MOE 1 moves to a personal repo by the user's rulings, and this log catches up.** **The subject.** The user decided on 2026-10-04 that MOE 1 measures `fist` first, and `propter` "if necessary"; the lead reads that as: if fist cannot reach 20 sessions after adoption. That supersedes "one work repo (alias in the Status Log)" in the MOE, and D6's alias rule for the measurement repo with it: the rule kept a work repo's name out of a public tree, and fist is personal and already named here. fist suits the role: it has not adopted the kernel, so every session it has run is baseline, and it runs about four sessions a week. The frame is fist sessions on Nidhogg: 5 of its 15 session docs, dated 2026-09-10 to 09-14, have no transcript here, and age-out does not explain it, since transcripts last modified 2026-09-07 survive in another project.
  Evidence: in `~/projects/github/fist`, `grep -n 'scope:' config/project.yaml` → `11:  scope: personal`; `grep -c 'Claim Style' CLAUDE.md` → `0`; `ls docs/sessions/` → 15 docs, the first dated 2026-09-10, 5 dated 09-10 to 09-14; its transcript directory holds 10 top-level `.jsonl` files, the oldest last modified `2026-09-15`; stx-server's oldest is `2026-09-07`.
  **The instrument, by the user's ruling.** As approved, the MOE compared a baseline from the Insights report with an after-window from each session's own `N` line. Two instruments make the comparison measure the switch between them, and fist's pre-kernel sessions wrote no `N` line at all. Asked through the harness's question tool on 2026-10-05, the user chose "Yes, once the scorer passes A1 (Recommended)": the MOE reads `N` until CONOP SEXTANT's agreement test, its A1, passes; from then on one collector scores both windows from transcripts, and `N` is a cross-check. No collector exists yet. The MOE's timing moves with its subject: "no sooner than seven weeks after adoption" becomes about five weeks at fist's rate, 20 sessions at about four a week. fist adopts the kernel only through a release, and the user's hold blocks the release until 1e and 2d run (SEXTANT, O2). The work-side rate is now unmeasured: gap G9. This entry lands alone as a `[gate]` commit under WHETSTONE D4. Its non-author review is `docs/reviews/20261005_sextant_review.md`, whose C2 found that the first draft stated this instrument change as decided before the user ruled.
  **Where it would live.** The collector and its measurements would live outside this repo: [CONOP SEXTANT](conop_sextant_doctrine_evaluation_repository.md), In Debate, proposes a personal-scope evaluation repository. Measurements go outside every checkout, as `maintaining-the-common-operating-picture/ADOPTION.md` requires, and on home storage, by the user's 2026-10-04 decision. Their first input was at risk: Claude Code deletes transcripts older than `cleanupPeriodDays`, default 30 (gap G8). The user set `3650` on Nidhogg on 2026-10-05. Never set `0`: the installed client rejects it, and clients before v2.1.89 read it as "write no transcripts". On the work terminal, check the setting before Wave 0 and copy the incident sessions into work storage.
  Evidence: `curl -sL https://code.claude.com/docs/en/settings-reference.md`, the `cleanupPeriodDays` entry, 2026-10-05: "a whole number, minimum `1`", "Default: `30`", "Setting `0` fails validation, so pick a large value such as `3650` for long retention"; `grep -a -c 'cleanupPeriodDays must be at least 1'` over the installed 2.1.289 client → `2`; `json.load` of `~/.claude/settings.json` → `cleanupPeriodDays` `3650`.
  Correction before commit: the first draft of this entry quoted a WebFetch summary as the docs, "`0` turns deletion off". A second summary of the same page said `0` deletes transcripts after each session, and the raw page says neither. Both round 1 reviewers caught it (`docs/reviews/20261005_sextant_review.md` C1; `docs/reviews/20261005_sextant_proposer.md` finding 1). Nothing acted on it: no settings file held `0`.
  **Catch-up.** This log stopped at the Wave 2 gate. Since then: the transport fix merged (`d602c8e`, 2026-10-01), which meets O6's condition; the user's one-cycle hold stands. The release grew to eight drafted entries, A1, A2, and B to G, in [20261002_overwatch_release_entries_draft.md](20261002_overwatch_release_entries_draft.md), including entry F from outside the waves. Entry F's gate returned GO in round 3 (`docs/reviews/20261002_private_terms_gate.md`), so the draft's open item 2 can close. G4 and G5 now live in `docs/gaps.md`. The `assay` exclusion merged (`8e73508`, 2026-10-04), so any release from the work terminal waits on G6. A traversal on 2026-10-04 found four threads this log handed off that never landed, each still open: the 1a gate's `CI=true` line for the gate checklist reached no gate surface, only `ISOLATION.md:100`; the reviewer's `uv cache clean` lesson (2026-10-01, tasks 1b to 1d) reached neither 1e's Standard nor entry G; task 2d has a Standard but no procedure, naming neither its scorer nor how one turn runs with and without the kernel; and G4 has no task line.
  Evidence: `grep -l -i 'CI=true\|with and without'` over `.claude/agents/`, `.claude/commands/`, `.claude/teams/` → 0 files; `grep -c -i 'uv cache\|cache clean'` over the draft and `docs/tasks.md` → 0 lines; `grep -c 'M7\|\bG4\b' docs/tasks.md` → `0`; `git log -1 d602c8e`, `git log -1 8e73508` → the two merges, dated as above.
