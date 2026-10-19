# Proposer review: CONOP OVERWATCH

**Date**: 2026-09-30
**Subject**: `docs/plans/conop_overwatch_claim_verification_and_irreversible_guards.md`
**Reviewer**: proposer (blind to code-reviewer)

## Verdict

GO-WITH-FIXES, with a smaller cut line than drafted. The diagnosis is right and the layered shape is right. Three parts are over-built or mis-aimed. First, the PreToolUse delete guard is mostly redundant for the 138 GB incident once a Python audit hook (about 15 lines) and a pinned data root exist, and the `git add` and `uv pip` guards need no hook at all because `permissions.ask` rules in `settings.json` do the job with zero parsing code. Second, the MOE bet cannot confirm a real improvement: a 10-session zero-count window has 24% power against a halved overclaim rate. Third, the kernel is ambient text the overclaiming model must choose to apply, and the draft's own Enemy Forces say so; the stronger alternative is to move the claim evidence into a file the harness or a reader can check. I recommend shipping Waves 0, 1 (reshaped), and a slim Wave 2, then deciding Waves 3 to 5 on data.

## 1. Resolve O1 to O6

### O1. Deny or ask: ask, via `permissions.ask`, with deny only for a short fixed list

Evidence:
- `.claude/settings.json` allows `Bash` outright and sets `defaultMode: acceptEdits`. Nothing asks today (CONOP Enemy Forces, confirmed by reading the file).
- Claude Code evaluates permission rules in the order deny, ask, allow, so an `ask` rule overrides the blanket `Bash` allow. Prefix rules such as `Bash(git add -A:*)`, `Bash(git add .:*)`, `Bash(rm -rf:*)`, `Bash(uv pip install:*)` need no jq, no stdin handling, and none of the four defects the sample hook showed (CONOP table, lines 35-40). A5/A3 should confirm the precedence on a live run; I did not run it.
- ENFORCEMENT.md lost Layer 6 on false positives, bypass cost, and "educational vs punitive" (ENFORCEMENT.md:41-43). Ask has near-zero false-positive cost because the user answers in one keystroke. Deny recreates the "disabled within a week" risk (MAUT, section 2).
- The `uv pip` case is a correctness rule with one right answer. `--python .venv/bin/python` already fixes it in docs (D5). An ask rule on `uv pip install` without the flag is not expressible as a prefix, so skip the guard there and rely on D5 plus the Step 4 check (1c).

Recommendation: ask for `git add -A`, `git add .`, directory-wide `git add`, `rm -rf`, `mc rm`. Deny nothing at the hub. A consumer repo with a data volume may add a deny for its own root. This also shrinks ADR-0003 to a settings.json convention, which keeps "reversibility decides blocking" intact without a new bash hook to maintain in 9 to 19 repos.

Would change my mind: (a) A3 shows `ask` rules do not outrank the `Bash` allow in the installed harness version; then a PreToolUse hook returning an ask decision is the fallback, and if that is also unsupported, log-only. (b) The log-only data from one downstream repo shows prefix rules miss more than 2 of 6 real command shapes (compound commands such as `cd x && rm -fr y`, flag reorderings like `rm -fr`). Then a parsed hook earns its cost.

### O2. Allowlist: `tmp_path` and the system temp dir only

Evidence: the draft's A4 data does not exist yet, and the allowlist only matters if a delete hook ships. In the audit-hook design below (section 2), the allowlist is "inside `tmp_path`", period. Build output (`.pytest_cache`, `__pycache__`, `dist`) is deleted by pytest and build tools themselves, outside the tripwire's reach when they run in a subprocess, and by Claude with `rm -rf dist` in Bash, which `ask` handles at the cost of one prompt. Do not pre-build an allowlist for it. Add entries only when a prompt fires 3 times in one repo.

Would change my mind: log-only data showing more than 1 false trigger per session on build output specifically (A4's own kill-criterion).

### O3. Stop-hook claim detector: out of scope for this CONOP; run A1 as a 2-hour spike and stop there

Evidence:
- The detector must match "success words" against "supporting tool output in the turn". The incidents are semantic: "half live" when the engine had crashed, a mirror sync asserted, a venv called unbuilt (Source 1). Only the mirror case is a success word with no tool call in the turn. The crashed-engine case had tool output that looked like success. A transcript heuristic cannot see that the output was the wrong output (the CONOP table admits this, line 101).
- Layer 5 has been "a candidate for the next iteration" since 2026-05-19 with no data. The task at `docs/tasks.md:30` has waited 87 days for audit data. The hub already runs one Layer 4 hook with a log nobody reads on a schedule.
- The 2026-05-19 MAUT weighted false positives at 0.20 (MAUT section 2). A Stop hook that writes to stderr on every turn ending in "done" will fire on most turns in a doc-heavy hub.
- A1's own kill-criterion (3 of 6 missed, or over 25% of clean closes flagged) is the right bar, but the replay corpus is 6 shapes and 20 closes: at 20 closes, a 25% threshold is 5 flags, and the 95% interval on a 5-of-20 observation spans roughly 9% to 49%. The test cannot distinguish a 10% hook from a 40% one.

Recommendation: keep A1 in Wave 0 as a bounded spike, but move the Stop hook out of the CONOP's committed scope. Build it only if the spike clears both thresholds and the downstream tally (section 4) still shows overclaims after the kernel ships.

Would change my mind: a replay that catches at least 5 of 6 shapes with at most 2 of 20 clean closes flagged. A hook that clears that bar has earned log-only status.

### O4. Blind panel: a separate `merge-review` template, scaled by diff, and defer it

Evidence: A5 is unfalsified, and this debate is its first test (CONOP Agent table). `code-review.md` should not be replaced; replacing it silently changes fleet behavior. A new template beside it adds one file and costs nothing until invoked. Scale rule: one reviewer under 150 changed lines, panel above 400 or when the diff touches `.claude/hooks/`, `settings.json`, or template-copy files. Do not detail this until the debate itself shows whether two blind reviewers disagree on anything material.

Would change my mind: this debate. If code-reviewer and I converge on every finding, the panel adds cost without signal; if each of us finds a BLOCKER the other missed, ship the template.

### O5. Guard doctrine: ADR-0003 plus the `settings.json` snippet, not a skill

Evidence: with the ask-rule design the guard is 4 to 6 lines of JSON. A skill directory (ADR-0001 form) for six lines is a shallow module. Put the convention in a short `ISOLATION.md` or in the ADR, and link from `ENFORCEMENT.md` "See Also". If a bash hook does ship, its header comment carries the contract.

### O6. Propagation: one entry after Wave 2, one after any deterministic layer ships

Evidence: Wave 1 changes the template `conftest.py` and `CLAUDE.md` install commands; Wave 2 adds a kernel to `CLAUDE.md`. Both change ambient text and should land as one downstream merge to avoid two rounds of conflicts in each repo's own `conftest.py` and `CLAUDE.md`. Hooks and settings changes ship alone, per PCC check 6. Do not wait for Waves 4 and 5.

Would change my mind: `docs/propagation-protocol.md` batching rules that cap entry size; I did not re-read them for this review.

## 2. Attack the wave order and the cut line

### 2a. Replace the conftest monkeypatch tripwire with one audit hook

The draft's A2 lists seven APIs to patch (`shutil.rmtree`, `os.remove`, `os.unlink`, `Path.unlink`, and three HTTP clients). The incident shape is "an under-scoped autouse guard fixture let the suite delete 138 GB" (Source 1). A tripwire built as a list of patched functions is itself an under-scoped guard, the same failure shape one level up.

Python's `sys.addaudithook` covers every Python-level delete through one callback. I ran it on Python 3.12.3 and got events for `Path.unlink` (`os.remove`), `Path.rmdir` (`os.rmdir`), `shutil.rmtree` (`shutil.rmtree`, then `os.rmdir`), `os.unlink` (`os.remove`), and `shutil.move` (`shutil.move`, `os.rename`). A hook raising on any of these events when the resolved path is outside `tmp_path` and the system temp dir closes all of them with about 15 lines. It cannot be removed once installed, and it needs no per-API list. What it misses: `subprocess` `rm` (a `subprocess.Popen` event carries argv and can be pattern-checked) and C extensions that call `unlink(2)` directly. Both limits belong in the `ISOLATION.md` "cannot see" list the draft already plans.

Recommendation for Wave 1a: filesystem tripwire as an audit hook. Network tripwire as one `socket.socket.connect` check in the same hook (event `socket.connect`), which also covers `requests`, `httpx`, and `urllib` without patching three client constructors. Keep `load_dotenv` as a no-op, since it is the propter pattern and costs 2 lines. Each still needs the proving test the draft requires. Note an audit hook installed at conftest import time also sees non-test code the suite imports, so the allowlist must include the pytest cache dir and `.hypothesis`.

### 2b. Is the PreToolUse delete guard redundant for the 138 GB incident?

Yes for that incident, with one condition. The deletion ran inside pytest (CONOP Enemy Forces, line 49). A Bash-matcher hook never saw it. The audit hook plus a data root passed as a parameter (D4) covers it from inside the process. The PreToolUse layer covers a different case: Claude typing `rm -rf /data/x`. The `permissions.ask` rule covers that case with less code. So the PreToolUse bash hook is the only item in Wave 3 whose cost (jq, stdin, `case` alternations, exit codes, the Pass 5 BLOCKER precedent, a `[gate]` commit, a test file) exceeds its marginal value. Cut it from the committed scope; keep it as the fallback named under O1.

Condition: the parameterized root (D4) is a per-repo code change the hub cannot make. The hub ships the pattern and the tripwire. The incident repo must apply D4 itself, so the hub's MOP row "guard reproduces its incident" is only true in a repo that adopts. State that.

### 2c. What is in Waves 0 to 2 that is not worth its cost

- **1c Step 4 tool checks**: the `VIRTUAL_ENV` mismatch check and the `.venv/bin/pytest` switch are cheap and map to a real incident; keep. The git-identity and `gh`/`glab` auth checks address a P3 task and a friction item (2 of 22 sessions) that is not an overclaim or a destructive op; defer them to their own task so Wave 1 stays on-theme.
- **2c EXAMPLES.md with six before/after pairs and 2b PROBES.md with seven probes**: these are the real value of Wave 2, but at 5 files the skill matches the prose kernel's 329 lines. That is the right size for a style skill that is read at every write. For a claims skill read once, a single `SKILL.md` of 80 lines with the probe table inline is a deeper module. Ship `SKILL.md` with probes inline and `EXAMPLES.md`; add `ADOPTION.md` and `REVIEWING.md` only if a second repo asks. ADR-0001 requires directory form, not five files.
- **2d four registration surfaces**: each is a drift point (an earlier session-end checklist copy drifted from `pcc.md`, per `.claude/commands/session-end.md` Step 2). Wire the kernel to `CLAUDE.md` and `/session-end` only in the first pass.

### 2d. What in Waves 3 to 5 is cheaper and higher value than what is detailed

- **TCS purpose line (Wave 4)**: one line in `.claude/commands/task.md:81`, one column. It addresses purpose drift (3 incidents in Source 1: data-viz vs calibration, mirror rename vs repo rename, inverted assumption), which is a more frequent failure than the six overclaims, and it costs minutes. Move it to Wave 1.
- **The `[gate]` PreToolUse hook (Wave 3)**: covered above; cheaper as settings rules.
- **Wave 5 doctrine entry**: required, not optional, but not a wave of its own; it is the closing task of whichever wave ships last.

### 2e. Proposed order

| Wave | Content |
|---|---|
| 0 | Clear the tree. A3 (confirm ask-rule precedence and `ask` hook decision, capture payloads). A1 spike, time-boxed. |
| 1 | `permissions.ask` snippet. Audit-hook tripwire plus proving tests. D5 install pin and the `VIRTUAL_ENV` check. TCS purpose line. |
| 2 | `verifying-claims` slim kernel with inline probes, and the session-end ledger (section 3 and 4). |
| 3 | One propagation entry. Then stop and measure. |

## 3. Challenge the claim-verification kernel (D1, D2)

### 3a. Four states

Written, tested, deployed, observed is a defensible ladder, but it is a taxonomy of the claim, and the incidents are failures of the evidence. Mapping the six overclaim shapes (Source 1):

| Incident shape | State of the claim made | State with evidence |
|---|---|---|
| Run called landed, engine crashed | observed | deployed |
| Mirror sync asserted | deployed | none |
| Venv called unbuilt | observed (negative) | none (one `ls` disproves) |
| Scan fix claimed, not exercised | tested | written |
| Validation reported twice, not run | tested | none |
| Stale numbers re-reported | observed | observed earlier, not this turn |

Two of six are not a state mismatch at all: the negative claim ("does not exist") and staleness. The ladder has no place for "this turn". A fifth axis, freshness, matters more than the middle two states. "Deployed" and "observed" are also hard to tell apart at write time: a pushed commit is deployed, and a cron that fired is observed, but "the pipeline is live" is both.

Recommendation: keep the ladder to three terms that need distinct evidence, and add the freshness rule explicitly: **a claim cites output from this turn or says UNVERIFIED**. That one rule covers 4 of the 6 shapes (no evidence, stale evidence, never run, never checked) without asking the model to classify its own claim, which is the step the overclaiming model skips.

### 3b. Will an ambient kernel change behavior?

Not reliably, and the draft says as much (Enemy Forces, first bullet). Prose Style works because every output can be checked by a reader against five visible rules. A claims kernel asks the model to notice its own missing evidence, which is the exact failure. Two cheap changes make it checkable instead of aspirational:

1. **Evidence line in the report, not in the head.** The kernel requires every success claim in a final message or session doc to be followed by a literal `Evidence:` line pasting the command and its last output lines, or `UNVERIFIED: <blocker>`. A missing line is a visible, greppable defect for the user and for `code-reviewer`. The user's catch cost today is one follow-up question per incident (CONOP Problem); a visible `UNVERIFIED` tag turns that question into a reading task.
2. **The strongest alternative: a claims ledger written by `/session-end`.** `/session-end` already forces a pass over the session. Add one required section to the session doc, `## Claims`, a table of claim, state, evidence command, and output tail. Grep makes it testable (`tests/` can assert the section exists in the template). It requires no hook and no new agent. Approach C's verifier (CONOP lines 109-117) then becomes optional and cheap: it reads only that table. The ledger also creates the data the MOE needs (section 4).

Neither is deterministic, but both move the check from "model notices" to "artifact exists", which a reviewer, a test, and the user can audit.

## 4. MOE math and observability

Arithmetic check: 0.73^5 = 0.207, 0.73^10 = 0.043. Both match the draft. The problems are elsewhere.

1. **Power.** The 4% figure is the false-positive rate under no change. Under a real improvement, a zero-count window rarely appears. If the kernel halves the per-session overclaim rate from 27% to 13.5%, P(0 in 10) = 0.865^10 = 0.23. If it cuts it by 80% (to 5.4%), P(0 in 10) = 0.57. So a bet that demands zero cannot confirm an 80% improvement 43% of the time. As written, the bet can only fail or confirm complete elimination.
2. **"At least 6 of 22" is a lower bound, and a count of hand-caught events.** Hand catches depend on user attention, which the kernel may change (visible `UNVERIFIED` tags change what the user sees). The numerator is a function of the observer.
3. **Observability.** The incidents occurred in work repos; the hub sees none of them. The Insights report ran on a work terminal and is not persisted here (CONOP header). The draft's fix is "one named work repo that has adopted the kernel". That repo is unnamed, and its session count is not visible from the hub. A bet that cannot be read from the hub's own files is a bet the hub cannot close.

Proposals:
- Replace "zero in 10" with a rate bound: at most 1 hand-caught overclaim in 10 sessions after adoption (P(at most 1 | 27%) = 0.043 + 10(0.27)(0.73^9) = 0.043 + 0.162 = 0.205, still weak). The honest statement is that 10 sessions cannot distinguish 27% from 10%; use 20 sessions or report the number and the interval without a pass/fail.
- Make the count observable by design: the `## Claims` ledger from 3b carries one line, `Overclaims the user caught this session: N`, filled at `/session-end`. That is a number the downstream repo writes in its own session docs, countable by `grep` with no work-system names leaving the work repo. The hub never needs to read the repo; the user reads the count.
- Name the repo in the Status Log by alias (for example "repo W1") before Wave 2 ships, or state that the MOE is the user's to report.

Replay MOE ("catches at least 5 of 6") is circular: the six shapes wrote the kernel, so it will catch them. Label it a regression check, not effectiveness.

## 5. What not to build, and what is missing

### Do not build

- **The bash PreToolUse guard** (section 2b) as committed scope.
- **A Stop-hook claim detector** (O3) before the downstream tally shows residual overclaims.
- **Five-file skill shape for a claims skill** (section 2c) in the first pass.
- **MinIO or object-store notes**: the CONOP already excludes them; good. The MinIO bulk-delete block in Source 1 was the permission classifier working. Treat it as a data point for O1: the classifier already asks on some destructive shapes, which supports an ask-first posture.

### Missing, and justified by the source texts

1. **A data-root parameter check in the template tests.** D4 is the real fix and the hub ships only a tripwire. Add one test to the template: assert that any path setting named in `config/project.yaml` resolves under `tmp_path` when the test fixture is active. Small, config-driven, in the spirit of the "all models from YAML" rule in memory.
2. **"Uncommitted half-finished code was picked up by a live production timer"** (Source 1, scope incidents) has no guard and no line in the CONOP. This is a deployment-hygiene rule: a timer reads from a checkout, so the checkout must be on a clean commit. It is a doctrine sentence in the kernel (claim state "deployed" requires a clean tree, `git status --porcelain` empty), and a probe. It costs one line in the probes table.
3. **The wrong-cycle cache pull and "a verification run pulled the wrong GFS cycle into production cache"** (Source 1) are the verify-against-prod shape: a verification step with write access to production. The kernel should say that verification probes are read-only; one rule.
4. **The best success in Source 1** (a three-agent review that independently surfaced a fail-open defect) is the only evidence in either source for the blind panel, and it is a launch-failure review, not a diff review. A5's replay test should use a fail-open defect, which the draft does name (fail-open reviewer); good, but note that the source evidence supports a fail-open charter line (cheap) more than a four-reviewer panel (expensive). A5's own kill-criterion already says this.
5. **Excessive change (3 incidents) and reverted slices**: not addressed anywhere. The scope guard the CONOP declines (commit check from prose) is right; a cheaper rule is "state the file list before the first edit, re-state when it grows". That is a CLAUDE.md line, not a mechanism. Include it only if you want a Scope kernel line; it has no evidence of working.

## 6. Numbered recommendations (summary)

1. Replace the bash PreToolUse guard with `permissions.ask` rules in `settings.json`; fall back to a hook only if A3 shows ask rules do not outrank the `Bash` allow. (O1, O2, O5)
2. Replace the multi-API conftest monkeypatch with one `sys.addaudithook` tripwire for deletes and sockets; tested to fire on 5 delete APIs on Python 3.12.3. Document the subprocess and C-extension limits. (Section 2a)
3. Keep Waves 0 to 1 plus a slim Wave 2; move the TCS purpose line into Wave 1; cut the Stop hook and the panel to "decide on data". (O3, O4, Section 2e)
4. Add a freshness rule ("cite this turn's output or say UNVERIFIED"), an `Evidence:` line convention, and a `## Claims` ledger at `/session-end`. Collapse the claim states to three and add freshness. (Section 3)
5. Rewrite the MOE as a reported rate with a stated interval and an in-ledger overclaim count; label the replay as a regression check. (Section 4)
6. Add guards for the missing incident shapes: clean tree before "deployed", read-only verification probes, and a template test that data roots resolve under `tmp_path`. (Section 5)

## What would change these recommendations

- A3 shows `ask` rules do not override the `Bash` allow in the installed harness: restore a PreToolUse hook (log-only first), written test-first with the four sample-hook cases.
- A1 clears both thresholds (5 of 6 caught, at most 2 of 20 clean flagged): build the Stop hook log-only as drafted.
- The downstream tally after 20 sessions still shows 3 or more overclaims: promote the independent verifier (Approach C) to the default at `/session-end`.
- The audit hook breaks more than 1 legitimate test per 100 in a downstream suite (for example, libraries that write caches outside `tmp_path`): fall back to a patched-API tripwire with an env opt-out.
- The user reports that `ask` prompts get approved reflexively: that is the bypass-cost failure in ENFORCEMENT.md:42 and argues for deny on the 2 or 3 most destructive shapes.
