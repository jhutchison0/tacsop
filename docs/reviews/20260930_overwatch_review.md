# Review: CONOP OVERWATCH Draft (Claim Verification and Irreversible-Operation Guards)

**Author**: code-reviewer
**Date**: 2026-09-30
**Type**: Plan review (CONOP document, pre-implementation)
**Subject**: `docs/plans/conop_overwatch_claim_verification_and_irreversible_guards.md` (untracked draft, Status: In Debate). Line numbers below refer to that file unless another file is named.

---

## Verdict: GO-WITH-FIXES

Approach B is the right design, and 28 of the 29 Situation claims I re-ran hold. One is REFUTED: the template `conftest.py` is 12 lines, not 11. Two gates do not work yet. Wave 2's exit replay cannot tell a working kernel from one that labels every claim UNVERIFIED (C1). Task 1a's acceptance tests would pass a tripwire with the same hole as the guard fixture that failed in the 138 GB incident (C2). Fix those two Standards, settle which document governs O1 (W1), and say what runs before approval (W2). After that, approve.

Counts: **2 Critical, 11 Warning, 16 Suggestion** (13 design, 3 prose Minor).

---

## 1. Situation Claims, Re-Run

| # | Claim (CONOP line) | Result | Evidence |
|---|---|---|---|
| 1 | `writing-simple-and-direct` is 5 files, 329 lines (:27) | CONFIRMED | `wc -l .claude/skills/writing-simple-and-direct/*` gives 5 files, `329 total` |
| 2 | `designing-clear-data-displays` is directory form (:27) | CONFIRMED | `SKILLS_FRAMEWORK.md:189-191` |
| 3 | Layer 4 PostToolUse audit is live (:28) | CONFIRMED | `.claude/settings.json` PostToolUse, matcher `Write\|Edit`, runs `post-tool-shift-left-audit.sh` |
| 4 | Layer 5 named as next candidate, `ENFORCEMENT.md:22` (:28) | CONFIRMED | `ENFORCEMENT.md:22`: "Layer 5 is a candidate for the next iteration." Layer 5 there is a "Stop hook diff audit" (`ENFORCEMENT.md:19`); see S10 |
| 5 | Layer 6 lost the 2026-05-19 MAUT; the sidecar states the revisit path (:28) | CONFIRMED | MAUT corrected ranking puts A4 (PreToolUse block) 9th at 0.640 (`20260519_pass4_enforcement_maut.md:104`); `ENFORCEMENT.md:89` |
| 6 | Hook tests feed JSON on stdin in a throwaway git repo (:29) | CONFIRMED | `tests/unit/test_shift_left_hook.py:3-6`, `:24-37` |
| 7 | propter fix in `docs/tasks.md`, P2, 2026-08-30 (:30) | CONFIRMED | `docs/tasks.md:51`. The dotenv stub there is scoped "in that test class"; see W5 |
| 8 | PCC check 6 requires a `[gate]` commit (:31) | CONFIRMED, overstated | `.claude/commands/pcc.md:91-96`: the check WARNs only |
| 9 | Pass 5 caught a BLOCKER, an invalid bash `case` alternation (:32) | CONFIRMED | `docs/reviews/20260519_pass5_grill.md:28` (proposer, F1 BLOCKER). code-reviewer caught the same defect as CONCERN-2 (`20260519_pass5_entry_audit.md:40`, `:140`); see S3 |
| 10 | Sample hook blocks `rm -rf /tmp/scratch`, exit 2 (:37) | CONFIRMED | Raw output A |
| 11 | Sample hook lets `rm -fr /data/grib` through, exit 0 (:38) | CONFIRMED | Raw output A |
| 12 | Sample hook misses `shutil.rmtree`, exit 0 (:39) | CONFIRMED | Raw output A |
| 13 | Sample hook lets `pytest` through, exit 0 (:40) | CONFIRMED | Raw output A; see W10 on what this row proves |
| 14 | A stray `VIRTUAL_ENV` redirects `uv pip install` (:41) | CONFIRMED | Raw output B |
| 15 | `--python .venv/bin/python` overrides it (:42) | CONFIRMED | Raw output B |
| 16 | `SETUP.md:42` recommends activating another env (:43) | CONFIRMED | `SETUP.md:42`: "point it at an alternate env with the `VIRTUAL_ENV` variable or by activating that env first." |
| 17 | Template `conftest.py`: 11 lines, Hypothesis profiles only (:44) | **REFUTED** (count); CONFIRMED (content) | Raw output C: 12 lines, unchanged since `9978231` (2026-07-20). No tripwires |
| 18 | `ENFORCEMENT.md` names the "Claude dice" problem (:48) | CONFIRMED | `ENFORCEMENT.md:7` |
| 19 | MAUT weighted false positives at 0.20 on "disabled within a week" (:50) | CONFIRMED | MAUT `:23`, `:29` |
| 20 | Hard blocks have a decision on record against them (:51) | CONFIRMED for test-first only | MAUT `:12` frames the decision as forcing "production code in `src/` to be written test-first"; see W1 |
| 21 | This repo is public (:52) | CONFIRMED | Unauthenticated `GET api.github.com/repos/jhutchison0/tacsop` returns HTTP 200 |
| 22 | `settings.json`: `defaultMode: acceptEdits`, `Bash` allowed outright (:53) | CONFIRMED | `.claude/settings.json:10` `"Bash"`, `:19` `"deny": []`, `:20` `"defaultMode": "acceptEdits"` |
| 23 | Propagation reaches 9 to 19 repos; the count is machine-local (:54) | CONFIRMED | `docs/tasks.md:39` (roster 19, discovery 9), `docs/tasks.md:12` |
| 24 | Scope matrix gives `python-prototyper` no `.claude/` access (:58) | CONFIRMED | `.claude/README.md:82`, quoted: "`.claude/` \| — \| Read \| Read \| — \| —" |
| 25 | CONOP Mission requires "in order to"; TCS table has no purpose (:60) | CONFIRMED | `CONOP-FORMAT.md:84-86`; `.claude/commands/task.md:81` |
| 26 | `/session-start` Step 4 runs bare `pytest` (:61) | CONFIRMED | Raw output D |
| 27 | Hub sessions are mostly doc work (:62) | CONFIRMED, with a number | 21 of 26 commits since 2026-08-01 touch nothing under `src/`, `tests/`, or `scripts/` |
| 28 | Re-run on Nidhogg (:7) | CONFIRMED | `hostname` prints `Nidhogg`; `uv 0.12.1` |
| 29 | The 2026-09-18 entry and the 2.1.1 bump are uncommitted on `main` (:172) | CONFIRMED | `git diff --stat`: `CI.md`, `SKILL.md`, `docs/doctrine-updates.md` |

**User-supplied, not verifiable here, not defects**: the report's figures (22 sessions, 345 messages, the date range), "at least 6 of 22" overclaim sessions, the four overclaim examples (:15), the 138 GB deletion, the swept `git add`, and the uv incident (:17, :49).

### Raw output A: the report's sample hook

Script is the hook verbatim from the sources file. Payloads built with `jq -cn --arg c "$cmd" '{tool_name:"Bash",tool_input:{command:$c}}'`, piped to `bash sample_hook.sh` and `sh sample_hook.sh` (identical results):

```
[bash] cmd=<rm -rf /tmp/scratch> exit=2 stderr=<BLOCKED: destructive op outside /tmp - confirm with user>
[bash] cmd=<rm -fr /data/grib> exit=0 stderr=<>
[bash] cmd=<python -c "import shutil; shutil.rmtree('/data/grib')"> exit=0 stderr=<>
[bash] cmd=<pytest> exit=0 stderr=<>
[bash] cmd=<rm -rf /data/grib> exit=2 stderr=<BLOCKED: destructive op outside /tmp - confirm with user>
```

The fifth row is not in the CONOP's table: the hook does block `rm -rf` outside `/tmp`. Capturing the command once (`c=$(jq -r ...)`, then grep `$c` twice) flips the `/tmp` case to exit 0 and keeps `/data` at exit 2, which confirms the stdin diagnosis.

### Raw output B: uv target selection

`S` is a scratch directory under `/tmp`; `proj/.venv` and `other/.venv` were made with `uv venv`. Run from `$S/proj`:

```
$ VIRTUAL_ENV=$S/other/.venv uv pip install --dry-run --offline --no-deps six
Using Python 3.12.13 environment at: $S/other/.venv
Resolved 1 package in 0.90ms
Would install 1 package
 + six==1.17.0

$ VIRTUAL_ENV=$S/other/.venv uv pip install --dry-run --offline --no-deps --python .venv/bin/python -v six | grep 'environment at'
DEBUG Using Python 3.12.13 environment at: .venv

$ env -u VIRTUAL_ENV uv pip install --dry-run --offline --no-deps six     # control
Resolved 1 package in 0.95ms
Would install 1 package
 + six==1.17.0
```

### Raw output C: conftest line count

```
$ wc -l tests/conftest.py
12 tests/conftest.py
$ git show HEAD:tests/conftest.py | wc -l
12
$ git log -1 --format='%h %cd' -- tests/conftest.py
9978231 Mon Jul 20 07:40:58 2026 -0500
```

### Raw output D: `/session-start` Step 4

```
$ sed -n '57,65p' .claude/commands/session-start.md
## Step 4: Verify Health
...
pytest                # Verify all tests pass
$ echo "VIRTUAL_ENV=${VIRTUAL_ENV:-<unset>}"; command -v pytest || echo "bare pytest: not on PATH"
VIRTUAL_ENV=<unset>
bare pytest: not on PATH
$ PATH=$S/other/.venv/bin:$PATH sh -c 'pytest'     # stub pytest in the other venv
pytest from OTHER venv
```

On this box, with no venv active, bare `pytest` does not resolve at all. With another venv first on `PATH`, it runs that venv's pytest.

---

## 2. Findings

### Critical

**C1. Wave 2's exit gate is uncalibrated** (:204, :156, :200, :202)

- **Issue**: "replay catches at least 5 of 6" scores the kernel on six known-bad shapes and no known-good cases. A kernel that makes the model label every claim UNVERIFIED scores 6 of 6. There is no control arm, so a 5 of 6 result cannot be credited to the kernel rather than to the current model. The replay protocol is unstated: what input each replay gets, who scores it, and what "catches" means. Task 2c writes "six before/after pairs, one per incident shape" and 2e replays "the six shapes", so the test set is the authoring set, written and scored by the same author. The kernel's own premise, that ambient text changes claim behavior, has no row in the Assumptions table; A1 covers only the Stop-hook detector.
- **Why it matters**: `CONOP-FORMAT.md:124-127`: "any metric used to gate a wave must first demonstrate that it rank-orders known-good above known-bad reference cases. An uncalibrated gate is worse than none." WHETSTONE D5 sets the floor that nothing is self-confirmed by its author (`conop_whetstone_recursive_doctrine_loop.md:109`).
- **Fix**: add an assumption row (A6: "An ambient kernel changes claim behavior"; falsifier and kill-criterion are the replay below). Replace the Wave 2 exit Standard:

  > Replay set: the six incident turns plus at least six clean turns whose success claims carry their own evidence, drawn from transcripts and held out from `EXAMPLES.md`. Each turn runs twice on the same model, with and without the kernel. A non-author scores each final message as flagged or not flagged. Pass: the kernel arm flags at least 5 of 6 incidents, flags at most 1 of 6 clean turns, and flags at least 2 more incidents than the no-kernel arm.

  A1's kill-criterion (:68) already pairs known-bad with known-good; copy its form.

**C2. Task 1a's acceptance tests would pass the guard shape that already failed** (:185, :69, :17)

- **Issue**: the source text records the 138 GB loss as the work of "an under-scoped autouse guard fixture". The CONOP's Problem (:17) drops the word "guard", and 1a proposes the same kind of fixture: the propter pattern is two autouse fixtures (`docs/tasks.md:51`). Two holes follow, and the 1a Standard and the A2 falsifier pass both.
- **Evidence 1, the name bound at import.** Scratch repro: an autouse fixture monkeypatches `shutil.rmtree`; the module under test did `from shutil import rmtree` at import time.

  ```
  $ VICTIM=$S/victim .venv/bin/python -m pytest -q -p no:cacheprovider test_bypass.py
  ..                                                                       [100%]
  2 passed in 0.07s
  $ ls $S/victim
  $
  ```

  The first test asserts the guard raised on a direct `shutil.rmtree`. The second calls the import-bound name and asserts the victim is gone; it passed, and `ls` shows the directory emptied.

  A2's falsifier, "a test that calls each API on a path outside `tmp_path` and asserts it raises" (:69), is the first test only. It passes by construction against a guard that lets the second through.
- **Evidence 2, the vacuous `/data` test.** `ls -ld /data` on Nidhogg prints "No such file or directory". With no tripwire installed, `shutil.rmtree("/data/grib")` raises `FileNotFoundError`. A test written as `pytest.raises(OSError)` "proves it fires on `/data`" with no tripwire at all. On a box where `/data` exists, a regressed tripwire makes the test itself delete real data.
- **Why it matters**: the template `conftest.py` reaches every downstream suite (:242). A tripwire that passes these tests ships false assurance against the incident it exists for.
- **Fix**: replace the 1a Standard's test clause:

  > Each tripwire test targets a sentinel directory the test creates outside `tmp_path` (never `/data`), asserts the tripwire's own exception class, and asserts the sentinel still exists afterwards. Tests cover a direct call, a call through a name bound at import (`from shutil import rmtree`), `Path.unlink`, and a subprocess `rm`. Any case the tripwire cannot close is listed in `ISOLATION.md` beside the test that shows it.

  Consider `sys.addaudithook` over monkeypatching. A scratch hook on the `shutil.rmtree`, `os.remove`, and `socket.connect` audit events caught all three shapes, including the import-bound `rmtree`:

  ```
  caught: tripwire(audit): shutil.rmtree $S/victim/sub
  caught: tripwire(audit): os.remove $S/victim/sub/f
  caught: tripwire(audit): socket.connect ('192.0.2.1', 80)
  victim still there: True
  ```

  A `socket.connect` guard also covers `psycopg` and `slack_sdk`, both installed in the hub venv. The 1a Standard's "HTTP client construction raises" covers neither, and `requests` and `httpx` are not installed in the hub venv, so that tripwire has no hub client to prove itself on. Two caveats: an audit hook cannot be removed, so it needs a per-test allowlist; and it must let pytest clean its own basetemp.

### Warning

**W1. D3 does not reverse the test-first decision, but the CONOP holds two readings of what `ENFORCEMENT.md` governs** (:127, :135, :51, :241, :19)

- D3 says ADR-0003 "scopes `ENFORCEMENT.md` without reversing it". That reading is right. "Why Not Hard Blocks" is about a PreToolUse hook "on `Write|Edit` to `src/myproject/**/*.py`" (`ENFORCEMENT.md:39`), and the MAUT's decision frame is test-first only (MAUT `:12`).
- O1 (:135), Enemy Forces (:51), and the agent table (:241) then say `ENFORCEMENT.md` requires re-running the 2026-05-19 MAUT "before any hard block". It does not. Its re-run trigger is `MISSING_TEST` counts (`ENFORCEMENT.md:83-89`). And that MAUT cannot be re-run on this question. Its six criteria have no term for harm that cannot be undone; its C6 "reversibility" means removing the mechanism (MAUT `:27`); every alternative fires on Write/Edit.
- `ENFORCEMENT.md:89` writes a new ADR "if the recommendation flips". D3 commits to ADR-0003 before any decision instrument runs. That is a pre-emption, not a reversal.
- The hub already has gate doctrine D3 does not cite. `lake-conventions/PREFLIGHT.md:44-60`: "A conservative gate is still a wrong gate ... Prefer a WARN you can read over a FAIL you will learn to bypass." The same file also refutes part of Problem :19 ("The hub's only enforcement doctrine"): the preflight is a fail-closed gate, "Exit 0 clean, 1 on any FAIL" (`PREFLIGHT.md:13`).
- **Fix**: use the scoped reading everywhere. O1 becomes: "`decision-scientist` runs a new MAUT for gating irreversible operations, with harm irreversibility and false-block cost (`PREFLIGHT.md`) among the criteria; the 2026-05-19 MAUT is the template, not the instrument." D3 moves under O1 as the hypothesis that MAUT tests. ADR-0003 is written after it reports.

**W2. Approval waits on data that only arrives after approval** (:133-140, :71, :208)

- The header "Open (these block approval)" covers O1 to O6. O1 depends on the MAUT, which the plan schedules in Wave 3 (:208). O2 depends on A4's log-only data, which needs 3 sessions after the Wave 3 guard ships (:71). O3 depends on A1 (Wave 0). Nothing says whether Wave 0 runs before approval.
- `CONOP-FORMAT.md:184` allows approval with decisions "explicitly deferred with rationale".
- **Fix**: state "Wave 0 runs while In Debate; approval follows its Status Log entry." Mark O2, O4, O5, and O6 deferred to their waves, each with a one-line rationale. O1 and O3 resolve at the Wave 0 report.

**W3. Task 1a assigns a `.claude/` file to `python-prototyper`** (:180, :185)

- 1a's Condition includes "a new `ISOLATION.md` sidecar in `shift-left-testing`", which is `.claude/skills/shift-left-testing/ISOLATION.md`. The team line gives 1a to "`bug-fix` (python-prototyper + test-runner)". `.claude/README.md:82` gives `python-prototyper` no `.claude/` access, and the CONOP's own Terrain (:58) says so.
- The `bug-fix` template fixes code in `src/myproject/` (`.claude/teams/bug-fix.md`, step 5); 1a has no `src/` change. `CONOP-FORMAT.md` asks for the template "with modifications", and none are stated.
- **Fix**: "1a: `python-prototyper` writes `tests/conftest.py` and the tripwire tests; the lead writes `ISOLATION.md` and its pointer in `shift-left-testing/SKILL.md`."

**W4. Waves 0 and 1 recreate the swept-commit conditions the CONOP names** (:172, :178-180)

- Wave 0's Standard is "Committed to `main` on its own". Before this review was written, `git status` also listed seven untracked files: five from 2026-03-26 (owned by `docs/tasks.md:25`), this CONOP, and a proposer review. This review makes eight. A directory-wide add sweeps them in, and the Standard does not forbid it. The task name, "Clear the working tree", promises a clean tree this commit will not produce.
- Wave 1 puts three unrelated changes and two authors (the prototyper in `tests/`, the lead in `CLAUDE.md` and `.claude/`) in one working tree on one branch, `topic/overwatch-wave1`. `using-topic-branches/SKILL.md:33`: "slug is the one logical change". "wave1" is three.
- **Fix**: Wave 0 Standard: "Commit by path, the three modified files only. Afterwards `git status --short` lists exactly the untracked files present before." Rename the task "Commit the 2026-09-18 entry". Wave 1: one branch per change (`topic/overwatch-sealed-tests` for 1a), or a separate worktree for the prototyper, and path-scoped `git add` in every commit.

**W5. Task 1a has no deliverable for the downstream merge, and it widens the propter stub** (:59, :185)

- Terrain (:59): "A tripwire ships as a pattern they merge, never a file they overwrite." No 1a Standard produces that pattern. Propagation only writes a notification (`docs/propagation-protocol.md:65`), so nothing is overwritten, but a downstream maintainer still needs something mergeable.
- propter's stub makes `load_dotenv` a no-op "in that test class" (`docs/tasks.md:51`). 1a makes it suite-wide. A downstream test that loads a fixture `.env` from `tmp_path` would silently load nothing.
- **Fix**: ship the tripwires as one module (for example `tests/isolation.py`) registered by one `pytest_plugins` line, so the downstream merge is one file and one line and touches none of their fixtures. Scope the dotenv stub the way the delete guard is scoped: a no-op for the repo's real `.env`, pass-through for a path under `tmp_path`.

**W6. A1 and A4 measure on the wrong machine and the wrong population** (:68, :71, :174, :62)

- A1 replays "the six incident shapes ... from local transcripts", and Wave 0 points at `~/.claude/projects/` (:174). The report ran on a work terminal (:7). Nidhogg is `scope: [personal]` (`config/project.yaml:35-37`). The six incident transcripts are not on this box.
- A4 measures "normal hub work". Terrain (:62) says the failure classes live in pipeline repos, and 21 of 26 hub commits since 2026-08-01 touched no code. A hub false-trigger rate says little about a repo that runs `rm -rf` on data directories daily.
- A4's falsifier takes 3 sessions. `CONOP-FORMAT.md:71-72` asks for the roughly one-afternoon test, and one exists: extract every Bash `tool_input.command` from existing transcripts and run them through the guard offline. This box holds 173 `.jsonl` transcripts; the report counts 2643 Bash calls on the work box.
- **Fix**: name the machine for A1 and A4 (the work terminal). Record only counts in this public repo's Status Log. Replace A4's falsifier with the offline replay, which also shortens W7's timeline.

**W7. The Mission's deadline cannot deliver its purpose clause** (:78, :71, :209)

- The Mission ends "by the end of four working sessions, in order to ... stop the unrecoverable mistakes ... at a gate". Wave 3 ships the guard log-only (:209), and A4 keeps it log-only for 3 sessions of data (:71). At the end of four sessions the guard stops nothing.
- A session count used as a clock has already collided once (`docs/tasks.md:6`, WHETSTONE's Wave 1 window).
- **Fix**: use a calendar date. Either split the by-when ("kernel and tripwires by <date>; guard enforcing by <date> if A4 passes") or narrow the purpose to what the date can deliver.

**W8. Two MOEs cannot observe what they claim** (:155, :157)

- MOE 1's baseline, "at least 6 sessions in 22", counts every repo on the work terminal. The window counts "10 sessions ... in one named work repo". One repo's rate is not the terminal's rate, and the 20% and 4% figures assume it is. The arithmetic holds: (16/22)^5 = 0.2035 and (16/22)^10 = 0.0414. No instrument is named. The baseline came from the Insights report, so either re-run that report over the window or define the hand count. "Measurable about three weeks after adoption" is short: 22 sessions in 56 days puts 10 sessions at about 25 days across all repos, and one repo takes longer.
- MOE 3: "The guard log shows each real catch." The conftest tripwires, the layer meant for the 138 GB class, write no log. WHETSTONE D7 (`conop_whetstone_recursive_doctrine_loop.md:111`): "Every gate names its stream."
- **Fix**: MOE 1 uses the baseline's instrument and that repo's own pre-kernel sessions as its baseline. Each tripwire appends one line to a named log when it fires, and MOE 3 reads both logs.

**W9. Three Standards a reviewer cannot mark pass or fail** (:187, :201, :151)

- **1b**: "Every `uv pip` example names `--python`". In which files? The Condition lists three. Across living docs, 46 `uv pip` lines lack `--python`, in 6 files: `python-venv-management/TROUBLESHOOTING.md` 17, `SETUP.md` 16, `CLAUDE.md` 5, `python-venv-management/SKILL.md` 4, `shift-left-testing/CI.md` 3, `README.md` 1. "A grep finds no 'activate that env' route" names no pattern, and two lines route the same way in other words: `SETUP.md:39` (`VIRTUAL_ENV=.venv-ml uv pip install ...`) and `SKILL.md:50` ("or the activated venv if one is active").
- **2d**: the Condition says "The four registration surfaces"; the Standard lists seven items, with `CLAUDE.md` twice. No hub document defines the phrase (grep of `.claude/`, `docs/adr/`, `CONOP-FORMAT.md`, `CLAUDE.md`: no match).
- **MOP (:151)**: "PCC check 5 reports 0 MISSING over every new doc." Check 5 reads a fixed list of surfaces (`pcc.md:62-63`), and no new doc is on it.
- **Fix**: 1b: "Scope: every living doc in `CLAUDE.md`, `README.md`, and `.claude/`. `grep -rnE 'uv pip (install|sync|uninstall)' <scope> | grep -v -- '--python'` prints nothing; `grep -rn 'VIRTUAL_ENV=' .claude/skills/python-venv-management/` prints nothing." 2d: list the surfaces as a checklist and drop "four". MOP: run check 5's grep and its directory pass over `git diff --name-only main...` for each wave branch.

**W10. The evidence table overstates what it shows** (:44, :89, :209, :265)

- `conftest.py` is 12 lines, not 11 (REFUTED, raw output C). The Status Log (:265) says "8 of 8 hold". The claim, no tripwires, holds; the evidence column does not.
- "The sample hook failed 4 of 4 cases" (:89). The exit codes reproduce. But the `pytest` row is a limit the CONOP says every Bash hook shares (:49), not a defect of this hook. And the table omits the case the hook gets right: `rm -rf /data/grib` exits 2. Accurate count: three defects in four probes, plus one shared limit; the hook blocks every `rm -rf`, `/tmp` included.
- Wave 3 (:209): "Written test-first, with the four sample-hook cases as its first four tests." The new guard's correct answer for `pytest` is exit 0, which the sample hook already returns. That test cannot fail first.
- **Fix**: correct the count and the framing. Record the `pytest` case as a pass-through test that documents the limit and points to the conftest layer. The 11-for-12 slip would make a fair `EXAMPLES.md` pair: the plan's first overclaim, caught by re-running.

**W11. O6's two options each break a propagation rule** (:140)

- "One doctrine entry at the end": the payload holds at least seven separable changes (sealed tests, install pinning, session-start checks, `verifying-claims`, the guard, the panel, the TCS purpose line). Batching Rule 2 (`docs/propagation-protocol.md:50`): "Never let a doctrine entry mix unrelated changes."
- "One per wave": the script ships only `entries[0]` (`docs/propagation-protocol.md:44`), and the notification already under-reports the outstanding set (`docs/tasks.md:10`, P1). Two waves landing between cycles drop the older entry.
- 1c changes Step 4's default command from `pytest` to `.venv/bin/pytest`. Rule 4 (`docs/propagation-protocol.md:54`) gives a changed default its own entry.
- **Fix**: resolve O6 as "one entry per wave, each propagated before the next is written, unless the `docs/tasks.md:10` transport fix lands first." Mark 1c's Step 4 change as breaking.

### Suggestion

**S1. A3 is half-answered by the published docs** (:70). `code.claude.com/docs/en/hooks`, fetched 2026-09-30: PreToolUse `permissionDecision` takes `allow|deny|ask|defer`, so "ask" exists. The Stop input example shows `transcript_path` and `last_assistant_message`; `stop_hook_active` does not appear on the page. I read the page through a summarizer, so keep the live run. If `stop_hook_active` is gone, the later exit-2 escalation needs its own loop guard, and `last_assistant_message` makes A1's detector simpler than parsing the transcript.

**S2. Write `--python .venv`, not `--python .venv/bin/python`** (D5 :129, 1b, 1c). uv 0.12.1 accepts the directory:

```
$ VIRTUAL_ENV=$S/other/.venv uv pip install --dry-run --offline --no-deps --python .venv -v six | grep 'environment at'
DEBUG Using Python 3.12.13 environment at: .venv
```

`.venv/bin/` does not exist on Windows (`.venv\Scripts\`), and the hub supports Windows (`pyproject.toml` win32 `tzdata` marker; `python-venv-management/SKILL.md:40`). 1c's `.venv/bin/pytest` needs its Windows form stated beside it. One cheap probe for 1c and `PROBES.md`: with a stray `VIRTUAL_ENV`, uv prints "Using Python ... environment at: <path>" at default verbosity, and the control run printed no such line.

**S3. A5's reference case cannot discriminate** (:72). Both single reviewers caught the 2026-05-19 `case` alternation at Pass 5 (proposer F1 BLOCKER; code-reviewer CONCERN-2). A panel replay on it can only tie, so the kill-criterion fires by construction. Use a defect a single review missed, such as the launch-control hook glob (`docs/tasks.md:38`), and add a clean diff to count panel false positives.

**S4. MOE 2 is a MOP** (:156). It is a pre-deployment replay at the Wave 2 gate, the same test as the Wave 2 exit. Move it under MOP.

**S5. The Problem section runs four paragraphs** (:13-19). `CONOP-FORMAT.md:42`: "One or two paragraphs, no more." The incident list fits under Situation.

**S6. Approach C's rejection mixes failure classes** (:114). "The worst incident happened mid-session" points at the 138 GB deletion, which C, an overclaim remedy, never targeted. Name the overclaim C would miss.

**S7. Record the exact probe commands in the evidence table** (:35-44). The four hook payloads become Wave 3's tests, and the uv commands are 1b's repro. "Same" and "two scratch venvs" cannot be re-run. Section 1's raw outputs carry both.

**S8. Two Wave 2d edits touch other plans' instruments** (:201). The `code-reviewer` checklist line changes a gate criterion. WHETSTONE D4 (`conop_whetstone_recursive_doctrine_loop.md:108`) puts such changes in `[gate]` commits with a non-author reviewer, though PCC check 6's path list (`pcc.md:91`) does not include agent files. The `/session-end` claims step lands in the file `docs/tasks.md:8` (P1) also edits for WHETSTONE's capture point. Sequence the two.

**S9. Wave 5 should state the entry's tier** (:219). Say whether it ships PROVISIONAL with a canary first (WHETSTONE D5, `conop_whetstone_recursive_doctrine_loop.md:109`); the MOE 1 work repo is the natural canary. Downstream-facing skill text uses the civilian vocabulary (`docs/propagation-protocol.md:142-154`).

**S10. Three citations say more than their source.** "PCC check 6 already requires" (:31): it warns (`pcc.md:96`). "The silent doctrine edit WHETSTONE exists to prevent" (:51): WHETSTONE's mission names "silent doctrine loss", and the rule that fits is D4. "Stop-hook claim audit (Layer 5)" (:210): `ENFORCEMENT.md:19` defines Layer 5 as a Stop-hook diff audit for test-first, and `docs/tasks.md:30` still waits on audit data to decide it. Call the claim audit a separate hook, or say Layer 5 now carries two checks.

**S11. The source texts live only in this session's scratchpad under `/tmp`.** A1's replay, 2c's examples, and any later fidelity check need them. State in the Evidence base line where the private copy is kept, outside this repo.

**S12. Widen the `git add` guard sketch** (:209). It checks `-A`, `.`, and directories. `git add -u` and `git commit -a` sweep tracked files the same way.

**S13. Pre-register the A5 score for this debate** (:240). Before reading the two reports, fix the count: verified findings unique to each reviewer, and findings the lead could not re-run.

### Prose (per `writing-simple-and-direct/REVIEWING.md`)

```
[Minor] Rule 6: "Hub sessions are mostly doc work, so effectiveness can only be measured downstream." (:62)
Rewrite: "21 of the 26 hub commits since 2026-08-01 touched nothing under src/, tests/, or scripts/, so effectiveness can only be measured downstream."

[Minor] Rule 3 (stated link): "The hub's only enforcement doctrine, `shift-left-testing/ENFORCEMENT.md`, was built for test-first, where every violation can be fixed later, so it logs and never blocks." (:19)
The "so" claims a reason ENFORCEMENT.md does not give; its three are false positives, cheap bypass, and teaching over punishing (ENFORCEMENT.md:41-43). "Only" is also wrong (W1).
Rewrite: "`ENFORCEMENT.md` logs and never blocks. The 2026-05-19 MAUT chose that for test-first on three counts: false positives, cheap bypass, and teaching over punishing. None of the three weighs a mistake that cannot be undone."

[Minor] Rule 2: "The user caught each one with a single follow-up question." (:15)
The private source summary records this for the pipeline incident only. User-supplied, so not a defect if the full report supports "each".
Rewrite, if it does not: "The user caught the pipeline overclaim with one follow-up question."
```

Rule 8: seven em dashes, all in headings (:1, :165, :178, :191, :206, :212, :217); exempt under `RULES.md` 8. Rule 5: "in order to" at :78 is the Mission exception and :60 quotes it; no other banned word appears.

---

## 3. Format Conformance (`CONOP-FORMAT.md`)

| Requirement | Result |
|---|---|
| Every template section present | Pass. Header, Problem, Situation (four parts), Mission, Approaches (A, B, bold C), Recommendation, Design Decisions, MOP/MOE, Waves, NOT Build, Agent and Team Design, References |
| Each assumption has falsifier, blast radius, kill-criterion | Pass for A1 to A5. The kernel's own premise has no row (C1) |
| Waves 0 to 2 at TCS detail with markable Standards | Partial: W4 (Wave 0), C2 and W9 (Wave 1), W9 (Wave 2) |
| Calibration rule for gating metrics | Fail at the Wave 2 exit (C1). A1 is calibrated |
| MOP vs MOE | Pass with S4; MOE gaps in W8 |
| Validate before detail | Pass. A2 runs inside Wave 1; Waves 3 to 5 wait on A1, A3, A4 |
| Mission with purpose clause | Present; its deadline cannot deliver it (W7) |
| Problem length | Over the two-paragraph limit (S5) |

## 4. Doctrine Consistency: Direct Answers

- **D3 vs `ENFORCEMENT.md` and the 2026-05-19 MAUT**: D3 does not reverse the test-first decision. It pre-commits ADR-0003 before the decision instrument runs, and three other passages cite `ENFORCEMENT.md` for a rule it does not contain (W1).
- **1a vs downstream `conftest.py` ownership**: respected in principle, because propagation only notifies. No Standard produces the mergeable form, and the dotenv stub widens from one class to the suite (W5).
- **Scope matrix**: 1a's `ISOLATION.md` breaks it (W3). Wave 4's "row before implementation" (:236) matches `.claude/README.md:146-147`.
- **Branching**: Wave 1's exit (merge, delete local and origin) matches `using-topic-branches`. The branch bundles three changes (W4).
- **Propagation protocol**: both O6 options break a rule, and 1c needs its own entry under Rule 4 (W11).

## 5. Public-Repo Hygiene: Pass

I grepped the CONOP for every system, product, project, and organization the sources file names. None appears. Three terms that do appear are already public in this hub: MinIO (:229; `lake-conventions/SKILL.md`), grib (:38; a file extension in `scripts/lake_preflight.py:55`), and glab (:187, a public CLI). `/data` (:38, :185) is a generic path. The risk moves to later artifacts written from work transcripts: A1's Status Log entry, `EXAMPLES.md`, and MOE 1's "named work repo". Name that repo privately and record only counts here.

## 6. What Holds

Approach B's layer table (:96-101) states what each layer cannot see, which is the right test for layered guards. A1's kill-criterion pairs known-bad with known-good references (:68). MOE 3's last sentence, that zero catches and zero incidents say nothing, is the honest form. D6 holds across the whole draft.
