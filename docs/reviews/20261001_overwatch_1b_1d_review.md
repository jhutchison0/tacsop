# Review: OVERWATCH Wave 1 Tasks 1b, 1c, 1d Gate (`topic/overwatch-template-docs`)

**Author**: code-reviewer
**Date**: 2026-10-01
**Type**: Doc review (merge gate, template doctrine)
**Subject**: `git diff main...HEAD`, four doc-only commits (`7428d33` 1b, `d7c640f` 1c, `9f1eada` 1d, `c0325ee` em-dash fix), 10 files. Acceptance tests: the Wave 1 Standards for 1b, 1c, 1d, `docs/plans/conop_overwatch_claim_verification_and_irreversible_guards.md:189-191`.

---

## Verdict: GO-WITH-FIXES

0 Critical, 7 Warning, 12 Suggestion.

The pin works. With a stray `VIRTUAL_ENV`, `uv pip install --python .venv` lands in `.venv`, and with no `.venv` it fails closed. The tool checks print the right line in all 5 required scenarios, plus an unauthenticated glab 1.120.0. Task 1d passes outright. Four things block a clean GO. The tool-check block exits 1 when everything is fine, and Claude Code shows that as `<error>Exit code 1</error>`. Both 1b Standard greps print one line each at HEAD, and the 1b commit says they print nothing. The remedy line tells the reader to `unset VIRTUAL_ENV`, which does not survive to the next Claude Code Bash call. And `--python .venv` breaks commands run from a subdirectory, a case the docs never mention.

`S` below is the session scratchpad, `/tmp/claude-1000/-home-jhutchison-projects-github-tacsop/4e9044e9-74ac-444f-bde7-7aa7f9c8fd81/scratchpad`. Every probe ran on Nidhogg with uv 0.12.1, gh 2.102.0, and glab 1.120.0, which I downloaded into `$S/glab` for this review.

---

## Critical

None.

---

## Warning

### W1. The tool-check block exits 1 when all is well

`.claude/commands/session-start.md:77-80`. The block's exit status comes from the loop's last `&&` chain. When glab is missing, `command -v glab` fails and the block exits 1. When glab is installed and authenticated, `! glab auth status` is false, so the block also exits 1. It exits 0 in one case only: glab installed and unauthenticated. The success signal is inverted, and the Claude Code Bash tool shows a healthy session as an error.

```
$ cd tacsop && bash $S/toolcheck.sh          # block extracted verbatim, all fine
<error>Exit code 1</error>
$ ... glab on PATH, empty GLAB_CONFIG_DIR
glab NOT AUTHENTICATED: PR/MR filing and CI status checks fail
[exit=0]
```

**Why it matters**: lines 67-68 promise "nothing when it is fine". A model running `/session-start` instead sees an error on every healthy session in 9 to 19 repos. It will learn to ignore this block or chase a failure that does not exist. A downstream script under `set -e` aborts here.

**Fix**: use `if` forms, which return 0 when the condition is false. I ran the version below against all 9 scenarios in this review. Each one printed the expected line and exited 0, including the stray-env case with no `realpath` on PATH (see S2):

```bash
if ! { git config user.name && git config user.email; } >/dev/null; then
  echo "NO GIT IDENTITY: commits fail (/session-end Step 3)"
fi
if [ -n "${VIRTUAL_ENV:-}" ] && [ "$(cd "$VIRTUAL_ENV" 2>/dev/null && pwd -P)" != "$(cd .venv 2>/dev/null && pwd -P)" ]; then
  echo "STRAY VIRTUAL_ENV=$VIRTUAL_ENV: an install without --python lands there, not in .venv"
fi
for cli in gh glab; do
  if command -v "$cli" >/dev/null && ! "$cli" auth status >/dev/null 2>&1; then
    echo "$cli AUTH CHECK FAILED (not logged in, or offline): merge and CI results are UNVERIFIED (/session-end Step 6)"
  fi
done
```

### W2. Task 1b's two Standard greps each print a line, and the 1b commit says they print nothing

- `.claude/commands/session-start.md:75`, added by 1c, matches grep 1: "a bare uv pip installs there" contains `uv pip install`.
- `.claude/skills/python-venv-management/SKILL.md:108`, the 3.1.0 version line added by 1b itself, matches grep 2 through the literal `` `VIRTUAL_ENV=` ``.

```
$ git grep -n 'VIRTUAL_ENV=' 7428d33 -- .claude/skills/python-venv-management/
7428d33:.claude/skills/python-venv-management/SKILL.md:108:**Version**: 3.1.0: ... the alternate-env route through `VIRTUAL_ENV=` and activation is removed ...
```

Commit `7428d33` says "Checks: both Standard greps print nothing". Grep 2 prints the line above at that same commit. Neither match teaches the old route, so the doctrine is sound. The defect is the claim: the lead reported an acceptance check as run and clean when it was not. That is the overclaim shape this CONOP exists to stop.

**Fix**: reword both lines so the Standard holds literally. For line 75, the W1 block's `an install without --python lands there` passes grep 1; I checked it. For line 108, "the alternate-env route through the `VIRTUAL_ENV` variable and activation is removed". Then re-run both greps and record the correction in the Status Log, the way the 1a gate recorded R3-S3.

### W3. The `unset VIRTUAL_ENV` remedy does not persist in Claude Code

`.claude/commands/session-start.md:83-84` says "run `deactivate` or `unset VIRTUAL_ENV` before any `uv pip` command". `TROUBLESHOOTING.md:243` gives "or `unset VIRTUAL_ENV`" as a fix. In the Claude Code Bash tool, environment changes end with the call, and `deactivate` does not exist:

```
$ export OVERWATCH_PROBE=set_in_call_1; unset GIT_EDITOR; type deactivate
call1: OVERWATCH_PROBE=set_in_call_1 GIT_EDITOR=unset
/bin/bash: line 2: type: deactivate: not found
$ # next Bash call
call2: OVERWATCH_PROBE=unset GIT_EDITOR=set
```

**Why it matters**: `/session-start` runs in exactly this tool. A model that runs `unset VIRTUAL_ENV` once believes the stray is cleared. Its next bare `uv pip install` lands in the other repo's venv. W7's in-code hint prints exactly such a command. The incident survives the fix.

**Fix**: "A stray `VIRTUAL_ENV` came from the shell that launched this session. Pin `--python .venv` on every `uv pip` command. To clear it, exit, run `deactivate` in the launching shell, and relaunch." Make the same change at `TROUBLESHOOTING.md:243`.

### W4. `--python .venv` resolves against the current directory, and the docs do not say so

`CLAUDE.md:81` used to say "from the project root"; the new line drops that. `TROUBLESHOOTING.md:210` gives Issue 5's cause as "running outside the project root without `--python`". From a subdirectory, the documented command now fails, while the old bare form found the parent `.venv`:

```
$ cd tacsop/src && uv pip install --python .venv --dry-run --offline -e ".[dev]"
error: No virtual environment found for executable name `.venv`; run `uv venv` to create an environment, or pass `--system` to install into a non-virtual environment
$ cd tacsop/src && uv pip list
Using Python 3.12.13 environment at: /home/jhutchison/projects/github/tacsop/.venv
```

The failure is fail-closed, which is the right direction. But a reader who hits it lands in Issue 5, whose Cause line says they skipped `--python`. They did not skip it. Issue 5's "works from anywhere" (`TROUBLESHOOTING.md:212`) holds for the `<project-root>/.venv` line only, not for the `.venv-ml` line under it.

**Fix**: put "from the project root" back in `CLAUDE.md:81`. Rewrite Issue 5's Cause as: "running outside the project root. A bare `uv pip` finds no `.venv`, and `--python .venv` is resolved against the current directory." Scope "works from anywhere" to the absolute-path form.

### W5. Task 1c Standard: 2 of the 3 checks do not name the step they block

The Standard reads "each with the step it blocks" (CONOP:190). Only the identity line names a step: "commits fail (/session-end Step 3)", and Step 3 is Commit (`session-end.md:23`). The stray-env line (`session-start.md:75`) names a consequence. The CLI line (`:79`) names activities, "PR/MR filing and CI status checks", but no step.

**Fix**: name a step in each message. The W1 block names `/session-end Step 6` (Evaluate Merge Readiness) for the CLI line. For the stray line, name the install steps. Or, if the lead reads "step" as "activity", record that reading in the Status Log.

### W6. `SETUP.md:42` gives a false reason for removing the `VIRTUAL_ENV=` prefix form

"Never route one through `VIRTUAL_ENV` or an activated shell: the variable outlives the command". That holds for activation and for `export`. It is false for the prefix form `VIRTUAL_ENV=.venv-ml uv pip install ...`, which is the form the line above it replaced:

```
$ VIRTUAL_ENV=.venv-ml uv pip install --dry-run --offline --no-deps six; echo ${VIRTUAL_ENV:-unset}
Using Python 3.12.13 environment at: .venv-ml
after prefix form: VIRTUAL_ENV=unset
$ source .venv-ml/bin/activate; cd ../projB && uv pip install --dry-run ...
Using Python 3.12.13 environment at: .../projA/.venv-ml
```

**Fix**: "Never route one through `VIRTUAL_ENV`. Activating a venv or exporting the variable outlives the command, and the next bare `uv pip` in that shell, in any repo, installs into `.venv-ml`. One form, `--python`, covers every case."

### W7. The in-code install hints still print a bare `uv pip install`

`src/myproject/decision_science/visualization.py:32` and `src/myproject/decision_science/scorer.py:304` print `Install it with: uv pip install -e '.[...]'`. These lines are outside 1b's Condition, which covers docs only. But they are the commands an agent copies verbatim at the moment an ImportError fires, and W3 explains why a stray env can still be live at that moment. They ship to every downstream repo that keeps the decision-science package.

**Fix**: do not change them on this doc-only branch. File a task to change them test-first: tighten the guard tests' `match=` (`tests/unit/test_scorer.py:376`, `tests/unit/test_visualization.py:264-274`) to `uv pip install --python .venv` first, watch them fail, then change the strings.

---

## Suggestion

**S1. A named conda env also redirects a bare install.** The 1c check and Issue 7 name only `VIRTUAL_ENV`. With `VIRTUAL_ENV` unset:

```
$ CONDA_PREFIX=$S/envs/ml CONDA_DEFAULT_ENV=ml uv pip install --dry-run --offline --no-deps six
Using Python 3.12.13 environment at: .../envs/ml
$ ... same, with --python .venv -v
DEBUG Using Python 3.12.13 environment at: .venv
```

The pin covers it. Add `CONDA_PREFIX` to the stray check and to Issue 7's first cause. The fleet migrated off conda, so this matters only on boxes where it lingers.

**S2. The stray check fails open when `realpath` is missing.** With a stray env and no `realpath` on PATH, the block prints only `realpath: command not found` on stderr. Both sides of the comparison become empty, so it reports nothing. macOS shipped no `realpath` before 13. The `cd ... && pwd -P` form in W1 works without it (verified).

**S3. The CLI check ignores which forge the repo uses, and it treats offline as unauthenticated.** Run from tacsop (a GitHub remote), an unauthenticated glab prints a line, though nothing in this repo uses glab. With the network unreachable (`HTTPS_PROXY=http://127.0.0.1:9`), an authenticated `gh auth status` exits 1, so the check reports NOT AUTHENTICATED. Both cases tell the model to mark results UNVERIFIED for no reason. Consider keying the CLI to the `origin` host, and the W1 wording covers the offline case. Also confirm the work terminal's glab version. Releases before gitlab-org/cli MR 1453 exit 0 when unauthenticated (issue #911), so the incident case would pass silently. Only 1.120.0 was tested here.

**S4. A `VIRTUAL_ENV` that points nowhere gets a false message.** `VIRTUAL_ENV=/nonexistent/venv` prints "a bare uv pip installs there", but uv falls back to `.venv` (`DEBUG Failed to inspect ... /nonexistent/venv/bin/python3`, then `environment at: .venv`). This case is rare, so a wording tweak is enough.

**S5. `uv pip compile` stays unpinned and resolves against the stray env's Python.** `SETUP.md:237`. Under a stray 3.11 env, `uv pip compile -v` logs `Using Python 3.11.15 interpreter at .../env311/bin/python3`; with no env set, it uses `.venv/bin/python3` (3.12.13). `CLAUDE.md:81` says "every package operation". Pin compile too, or carve it out in that sentence.

**S6. `SKILL.md:103` was rewritten to dodge grep 1, and the rewrite reads as a runnable command.** "pip-tools (uv's `pip compile` and `pip sync`)". Neither `pip compile` nor `pip sync` exists. Write: "pip-tools (`uv pip compile`, `uv pip sync --python .venv`)". That form passes grep 1.

**S7. The Makefile in `SETUP.md:96,99` writes a literal `.venv` beside `VENV := .venv`.** Use `--python $(VENV)`. A separate, older defect in the same block: the `venv:` target runs `uv venv --managed-python` without `--clear`, so a second `make install` exits 2 ("A virtual environment already exists", verified). That is out of scope; file it as a task.

**S8. `TROUBLESHOOTING.md:239`: an unset variable counts as "the cause".** The comment reads `echo "${VIRTUAL_ENV:-unset}"   # anything but this project's .venv is the cause`, so the output `unset` also qualifies. Rewrite: `# a path other than this project's .venv is the cause`.

**S9. Bare `pytest` survives where 1c's own reasoning applies.** `CLAUDE.md:87-90`, `README.md:97-100`, `.claude/agents/test-runner.md:13-22`, and `CI.md:163` (`pytest -n auto`, directly after the pinned xdist install). These still run bare `pytest`, which is what Step 4 stopped doing. Do not widen this branch. File a task. Activating the project's own venv (`CLAUDE.md:76`, `README.md:38`) is also how a stray env starts once the user leaves the repo; the same task can prefer `.venv/bin/<tool>`.

**S10. Three living docs still define TCS without Purpose, and two format docs never define the new column.** `LANGUAGE.md:61`, `CLAUDE.md:163`, and the heading at `task.md:69` define TCS as Task, Condition, Standard. The acronym can stay; add "plus a Purpose column" to the LANGUAGE.md entry. `CONOP-FORMAT.md:150` and `OPORD-FORMAT.md:85` add the column but not its meaning. `OPORD-FORMAT.md:57` already uses "Purpose" for the operation's "in order to". Add one line under each table: "Purpose: who gets the output and what decision it informs (`task.md` Level 2)".

**S11. Items for the Wave 1 doctrine entry.**
- Mark 1c breaking. This clause is PENDING because no OVERWATCH entry exists yet in `docs/doctrine-updates.md`.
- List the `CI.md` install-line change as a PATCH for downstream `.github/workflows/*.yml`. It supersedes the 2026-09-18 snippet (`docs/doctrine-updates.md:55`), which is a record and stays as it is.
- The shift-left-testing 2.2.0 version line (`SKILL.md:114`) names only ISOLATION. Add the CI.md pin.
- Correct the counts as in claim (c) below.
- Add "pin `--python .venv`" to the open from_template_to_project uv-swap task (`docs/tasks.md:32`). That doc still teaches `python3 -m venv` and `pip install` (`docs/design/from_template_to_project.md:91-102`).

**S12. Prose (Minor, writing-simple-and-direct).**
- [Minor] Rule 6: "A stray `VIRTUAL_ENV` usually means a shell activated another repo's venv" (`session-start.md:83`). Rewrite: see W3's text, which names the source.
- [Minor] Rules 2 and 6: "A task with no named consumer is the cheapest place to catch work aimed at the wrong question" (`task.md:87`). A task is not a place, and "cheapest" has no number. Rewrite: "The task spec is where wrong-question work costs least to catch: a walkthrough built when the need was a calibration cost a session, and Condition and Standard never ask what the output is for."
- [Minor] Term: "report it as UNVERIFIED" (`session-start.md:86`). D2 fixes the form as `UNVERIFIED: <blocker>`. Use it so Wave 2's kernel matches.

**Process.** The CONOP's Wave 1 heading reads "one branch each", and the approval adopted W4 (one branch per change, CONOP:267). This branch carries three tasks. That bundling is how 1c's new line broke 1b's grep without anyone seeing it. Record the deviation in the Status Log.

---

## 1. Acceptance checks

| Task | Standard clause | Result | Evidence |
|---|---|---|---|
| 1b | `grep -rnE 'uv pip (install\|sync\|uninstall)' CLAUDE.md README.md .claude/ \| grep -v -- '--python'` prints nothing | **FAIL** at HEAD (1 line); PASS at `7428d33` | A |
| 1b | `grep -rn 'VIRTUAL_ENV=' .claude/skills/python-venv-management/` prints nothing | **FAIL** at HEAD and at `7428d33` (1 line) | A |
| 1b | Wider grep (adds freeze, list, show) | Same single line as grep 1 | A |
| 1b | Scratch repro with the documented command reports `.venv` | PASS | B |
| 1c | Reports git identity | PASS | C |
| 1c | Reports a `VIRTUAL_ENV` that is not this project's `.venv` (silent for own) | PASS | C |
| 1c | Reports gh or glab auth when the CLI is installed | PASS (gh; glab 1.120.0) | C |
| 1c | Each with the step it blocks | **FAIL** (1 of 3) | W5 |
| 1c | Runs `.venv/bin/pytest` (Windows: `.venv\Scripts\pytest`) | PASS: `351 passed, 1 warning in 4.23s` | `session-start.md:62` |
| 1c | Marked breaking in the entry | PENDING (no entry yet) | S11 |
| 1d | `task.md:81` table gains Purpose: who gets the output, what decision it informs | PASS | `task.md:81-87` |
| 1d | CONOP-FORMAT and OPORD-FORMAT task tables match | PASS | `CONOP-FORMAT.md:150`, `OPORD-FORMAT.md:85` |

**A. Greps**

```
$ grep -rnE 'uv pip (install|sync|uninstall)' CLAUDE.md README.md .claude/ | grep -v -- '--python'
.claude/commands/session-start.md:75:  echo "STRAY VIRTUAL_ENV=$VIRTUAL_ENV: a bare uv pip installs there, not into .venv"
$ grep -rn 'VIRTUAL_ENV=' .claude/skills/python-venv-management/
.claude/skills/python-venv-management/SKILL.md:108:**Version**: 3.1.0: every `uv pip` command names its target (`--python .venv`). A `VIRTUAL_ENV` inherited from another repo's shell outranks the project's `.venv`, and a bare install lands there; the alternate-env route through `VIRTUAL_ENV=` and activation is removed (2026-10-01, CONOP OVERWATCH task 1b).
$ grep -rnE 'uv pip (install|sync|uninstall|freeze|list|show)' CLAUDE.md README.md .claude/ | grep -v -- '--python'
.claude/commands/session-start.md:75:  echo "STRAY VIRTUAL_ENV=$VIRTUAL_ENV: a bare uv pip installs there, not into .venv"
```

A per-occurrence scan closes the grep's blind spot, where a line passes because `--python` appears anywhere on it. The scan checks each `uv pip <cmd>` for `--python` before the next backtick, `&&`, `;`, `|`, or `#`. It found three prose mentions of the bare command (`CLAUDE.md:81`, `TROUBLESHOOTING.md:237` twice), all correct in meaning. No command in a living doc is left unpinned.

**B. Stray-VIRTUAL_ENV repro** (`$S/repro/projA`, `projB`, each with its own `.venv`; run in projA)

```
1. bare, VIRTUAL_ENV unset             -> Would install 1 package
2. bare, VIRTUAL_ENV=projB/.venv       -> Using Python 3.12.13 environment at: .../repro/projB/.venv
3. --python .venv, VIRTUAL_ENV=projB   -> Would install 1 package
4. bare -v, unset                      -> DEBUG Using Python 3.12.13 environment at: .venv
5. bare -v, VIRTUAL_ENV=projB          -> Found ... projB/.venv/bin/python3 (active virtual environment)
                                          Using Python 3.12.13 environment at: .../projB/.venv
6. --python .venv -v, VIRTUAL_ENV=projB -> DEBUG Using Python 3.12.13 environment at: .venv
7. --python .venv, no .venv yet, stray -> error: No virtual environment found for executable name `.venv` (fail closed)
```

**C. Tool-check block, extracted verbatim** (awk between `## Step 4` and `## Step 5`, second bash fence; run from the tacsop root)

```
=== 1. all fine                     -> (no output) [exit=1]
=== 2. stray VIRTUAL_ENV            -> STRAY VIRTUAL_ENV=.../repro/projB/.venv: a bare uv pip installs there, not into .venv [exit=1]
=== 3a. VIRTUAL_ENV=$PWD/.venv      -> (no output) [exit=1]
=== 3b. VIRTUAL_ENV=.venv           -> (no output) [exit=1]
=== 3c. VIRTUAL_ENV=symlink to own  -> (no output) [exit=1]
=== 4. GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
                                    -> NO GIT IDENTITY: commits fail (/session-end Step 3) [exit=1]
=== 5. GH_CONFIG_DIR=$S/emptygh, GH_TOKEN and GITHUB_TOKEN unset
                                    -> gh NOT AUTHENTICATED: PR/MR filing and CI status checks fail [exit=1]
=== 6. glab 1.120.0 on PATH, GLAB_CONFIG_DIR empty, GITLAB_TOKEN and GLAB_TOKEN unset
                                    -> glab NOT AUTHENTICATED: PR/MR filing and CI status checks fail [exit=0]
=== extra: no realpath on PATH, stray -> realpath: command not found (stderr only) [exit=1]   (S2)
=== extra: VIRTUAL_ENV nonexistent   -> realpath: ... No such file or directory / STRAY ... [exit=1]   (S4)
=== extra: run from src/, own .venv  -> STRAY VIRTUAL_ENV=.../tacsop/.venv ... (false positive off-root)
```

Identity probe: in a scratch repo with no identity, `git commit` printed `fatal: empty ident name (for <jhutchison@Nidhogg.localdomain>) not allowed` and exited 128. "commits fail" holds.

---

## 2. Claim re-runs

| Claim | Where | Result | Evidence |
|---|---|---|---|
| (a) uv prints `Using Python <version> environment at: <path>` when the target is not the cwd's `.venv` | `SKILL.md:50`, `TROUBLESHOOTING.md:237` | CONFIRMED in 10 shapes | Prints for: stray `VIRTUAL_ENV`; `--python .venv-ml`; bare from a subdir; `--python ../.venv`; `--python projA/.venv` from the parent; `CONDA_PREFIX`. Silent for: no env; `VIRTUAL_ENV` = own `.venv` (absolute); `--python <abs>/.venv`; `--python .venv/bin/python`; `--python .venv` under a stray env. `list`, `freeze`, `show`, `uninstall`, `check`, and `tree` print it too, on stderr (`freeze 2>/dev/null` gives 0 stdout lines from the empty projB env). |
| (b) `--python .venv`, a directory, overrides a stray `VIRTUAL_ENV` | `7428d33` | CONFIRMED | B3, B6; also overrides `CONDA_PREFIX` and `UV_PYTHON` |
| (c) 6 files | `7428d33` | CONFIRMED | `git show --stat`: 6 files, 68 insertions, 67 deletions |
| (c) "44 install/sync/uninstall lines and 10 freeze/list/show lines ... now pass `--python .venv`" | `7428d33` | PARTIAL | 44 and 10 are the bare lines removed. Of those, 38 and 9 now pass `--python .venv`. 2 pass `--python .venv-ml`. 5 became prose with no command: 3 install Symptom lines, 1 list Symptom line, and the pip-tools line (S6). |
| (d) `/session-end` Step 3 is the commit step | `session-start.md:73` | CONFIRMED | `session-end.md:23: ## Step 3: Commit` |
| uv 0.12.1 | `7428d33` | CONFIRMED | `uv 0.12.1 (x86_64-unknown-linux-gnu)` |
| "both Standard greps print nothing" | `7428d33` | REFUTED | W2 |
| "the repro with the documented command reports .venv" | `7428d33` | CONFIRMED with `-v` | B6 |
| "a first draft said 'whenever VIRTUAL_ENV is set'; the re-run refuted it" | `7428d33` | CONSISTENT | `VIRTUAL_ENV` = own `.venv` prints nothing |
| "`--python .venv` works on Windows; `.venv/bin/python` does not" | `7428d33` | NOT RUN | No Windows box. The second half follows from the `Scripts\` layout. |
| "prints nothing on Nidhogg" | `d7c640f` | CONFIRMED for stdout | The exit status is 1 (W1) |
| "one correct line each for a stray VIRTUAL_ENV, no identity, and an unauthenticated gh; silent when VIRTUAL_ENV is the project's own .venv" | `d7c640f` | CONFIRMED | C2, C4, C5, C3a-c |
| "Step 5 gains a Tools line" | `d7c640f` | CONFIRMED | `session-start.md:100` |
| glab unauthenticated in 2 sessions | `d7c640f` | NOT RE-RUNNABLE | Comes from the insights report; matches CONOP:267 |
| TCS tables in three files read Task, Purpose, Condition, Standard | `9f1eada` | CONFIRMED | §1, 1d rows |
| "the variable outlives the command" | `SETUP.md:42` | REFUTED for the prefix form | W6 |
| Bare `uv pip list` under a stray env checks the wrong env | `TROUBLESHOOTING.md:237` | CONFIRMED | `uv pip list` under `VIRTUAL_ENV=projB` printed `environment at: .../projB/.venv` |

---

## 3. Meaning after the mechanical pass

- **`CI.md:38-39`, `uv venv --clear` then `--python .venv`**: sound. I simulated setup-uv's environment in `$S/ci` with `UV_PYTHON=3.11`, `VIRTUAL_ENV=$PWD/.venv`, and an existing `.venv`. `uv venv --clear` recreated it, and the pinned install printed no redirect line. `.venv/bin/python -V` printed `Python 3.11.15`. The matrix version holds.
- **`CI.md:162-163`**: the pinned install is followed by a bare `pytest -n auto` (S9).
- **`SETUP.md:39`, `TROUBLESHOOTING.md:215`**: the `.venv-ml` targets are correct. The alternate env kept its own name.
- **`SETUP.md:96,99`**: the Makefile uses a literal `.venv` beside `$(VENV)` (S7).
- **`SETUP.md:237`**: `compile` was left unpinned (S5).
- **`SKILL.md:103`**: the grep-dodging rewrite lost the real command names (S6).
- **`TROUBLESHOOTING.md:210-215`**: Issue 5 meaning changed; see W4.
- **Prose lines that describe the bare command**: `CLAUDE.md:81`, `TROUBLESHOOTING.md:237`, and `session-start.md:75` correctly carry no flag. Only line 75 trips the grep (W2).
- **Windows**: no Windows-path line received the flag. `SKILL.md:40` (`.venv\Scripts\activate`) is untouched.
- **Cosmetic**: the inserted flag pushed comment columns out of line (`SETUP.md:238`, `CLAUDE.md:93-96`). No meaning changes.

## 4. Consistency across living docs

| Doc | Status | Action |
|---|---|---|
| `src/myproject/decision_science/visualization.py:32`, `scorer.py:304` | Living code; bare `uv pip install` | W7, follow-up task |
| `docs/design/from_template_to_project.md:91-102` | Living; pre-uv `python3 -m venv` and `pip install` | Already tracked at `docs/tasks.md:32`; add the pin (S11) |
| `CLAUDE.md:76`, `README.md:38,97`, `SETUP.md:14` | Living; activate the project's own venv for running tools, not to route `uv pip` | Consistent with the new rule; see S9 |
| `CONTEXT.md:50` | Living; "uv venv ..., uv pip", no bare command | None |
| `LANGUAGE.md:61`, `CLAUDE.md:163`, `task.md:69` | Living; TCS as three terms | S10 |
| `docs/propagation-protocol.md`, `docs/session-doc-format.md`, `.claude/README.md` | No matches | None |
| `docs/doctrine-updates.md:55,864,891,900`, `CHANGELOG.md:11` | Records (dated entries) | Do not edit; the Wave 1 entry supersedes them |
| `docs/sessions/*`, `docs/reviews/*` | Records | Do not edit |
| OVERWATCH CONOP tables `:172,:186,:201`; `decision_science_utility.md:153,205,235`; `conop_whetstone_recursive_doctrine_loop.md:154` | Existing plans, three columns | Grandfathered, per `9f1eada` |

## 5. Prose

- **Em dashes on added lines**: 2 matches, both exempt under RULES.md 8. One is a list-index separator (`SKILL.md:97`); the other sits in a code comment (`TROUBLESHOOTING.md:172`). There are 0 in running prose. `c0325ee` fixed the one that was (`SETUP.md:279`).
- **Cruft list (LANGUAGE.md:147-149)**: 0 matches on added lines. The anti-glossary terms ("module", "stage", unqualified "plan") also have 0 matches.
- **Findings**: S12, plus W6, which is a false claim rather than a style finding.

## Reviewer side effects

- During setup I ran `uv cache clean six`, which removed 10 files (51.4 KiB) from `~/.cache/uv`. I put them back by installing `six==1.17.0` into a throwaway scratch venv. After that, the offline dry run resolved from the cache again. No project file or project venv was touched. Every install against tacsop's `.venv` used `--dry-run`.
- I downloaded glab 1.120.0 into `$S/glab`. Nothing was installed system-wide.

## Fix list for the gate

1. W1: replace the block with the `if` form above, or an equivalent, and re-run C1 to C6, checking exit 0.
2. W2: reword `session-start.md:75` and `SKILL.md:108`, re-run both greps, and log the correction.
3. W3: rewrite the remedy at `session-start.md:83-84` and `TROUBLESHOOTING.md:243`.
4. W4: restore "from the project root" in `CLAUDE.md:81` and fix Issue 5's Cause.
5. W5: name a step in each message, or log the reading.
6. W6: correct `SETUP.md:42`.
7. W7: file a test-first task for the two in-code hints.

Per the 1a precedent (S10), the reviewer's probes in §1 B and C get re-run against the fixed branch before merge.
