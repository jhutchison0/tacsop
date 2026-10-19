# OVERWATCH Release Entries: Draft

**Status**: DRAFT, held. Written 2026-10-02. This file lives in `docs/plans/`, which `scripts/propagate_doctrine.py` does not read, so no run can send it. The user's hold of 2026-10-01 stands: no OVERWATCH entry propagates until task 1e (ask rules) and task 2d (the controlled replay) are done, then everything goes in one cycle.

**Plan**: [conop_overwatch_claim_verification_and_irreversible_guards.md](conop_overwatch_claim_verification_and_irreversible_guards.md). **Protocol**: [propagation-protocol.md](../propagation-protocol.md), Rules 2 and 4 (unrelated changes separate; a breaking change alone).

**At release**, in order:

1. Fill the dates. One date for all; the delivery mark matches headings, not dates, so same-day entries are safe.
2. Fill entry B's result paragraph from task 2d, and entry G from task 1e.
3. Settle the two open items below.
4. Copy each entry to the top of `docs/doctrine-updates.md`, newest first, in the order A1, A2, B to G.
5. Pre-flight each against the Evaluation Gate's five questions. Dry run. Propagate on the lead's go.

**Open items**:

1. The WHETSTONE `KB-graph:` capture point (2026-10-01, `85342b4`) rides in the same two files entry B ships, `.claude/commands/session-end.md` and `docs/session-doc-format.md`. Rule 2 says a maintainer must be able to take B and skip it. Either a one-paragraph WHETSTONE entry of its own, or a row in B's table that names the line and says it is WHETSTONE's. Decision needed.
2. Entry F was implemented on 2026-10-02 after the drafts were begun. Its gate review is `docs/reviews/20261002_private_terms_gate.md` (round 1: GO-WITH-FIXES, fixes applied). Confirm the final verdict before release. Closed 2026-10-05: round 3 returned "Verdict: GO" (the review's Round 3 section).
3. Task 1c is split here into A1 (the pytest line, breaking) and A2 (the tool checks, additive), because protocol Rule 4 keeps a breaking change apart from additive ones. The 2026-10-01 decision read "1c alone as breaking" as one entry; the split needs the user's yes.

---

## A1. YYYY-MM-DD: BREAKING: `/session-start` Step 4 Runs the Project Venv's pytest

Step 4 of `/session-start` ran a bare `pytest`, which resolves through whatever environment the launching shell left active. In the incident this plan answers, a `VIRTUAL_ENV` inherited from another repo's shell took a `uv pip install` meant for this project. Step 4 now runs `.venv/bin/pytest` (Windows: `.venv\Scripts\pytest`).

**Breaking**: the default test command changes. A repo whose environment is not `.venv` must edit the line.

**Audience**: every repo with `.claude/commands/session-start.md`.

**Reversible**: one line. Rollback below.

### Detect

```bash
grep -nE '^pytest\b' .claude/commands/session-start.md   # a hit: the bare command is still there
```

### Adoption-Mode Table

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `.claude/commands/session-start.md`, Step 4 | **PATCH** | Replace the bare `pytest` line with `.venv/bin/pytest      # All tests, on this project's venv (Windows: .venv\Scripts\pytest)`. If your environment is not `.venv`, write your path. |

### Action required

1. Patch the line. Run `/session-start` once; Step 4 runs the suite on the project venv.

### Rollback

Restore the bare `pytest` line.

### Files (tacsop)

```
.claude/commands/session-start.md          (Step 4, one line; merged d98428a)
```

---

## A2. YYYY-MM-DD: `/session-start` Step 4 Checks the Session's Tools

Two gaps surfaced at the end of sessions instead of the start: a missing git identity, found at commit time, and an unauthenticated `gh` or `glab`, which blocked verification of merge and CI results in 2 sessions (CONOP OVERWATCH Status Log, the 2026-09-30 approved entry). Step 4 gains three read-only checks, each printing one line only when something is wrong: no git identity, a `VIRTUAL_ENV` that is not this project's `.venv`, and an installed `gh` or `glab` whose `auth status` fails. Step 5's summary gains item 9, Tools.

A `glab` older than gitlab-org/cli MR 1453 exits 0 when unauthenticated, so the auth check passes silently there; check your version.

**Audience**: every repo with `.claude/commands/session-start.md`. Additive; take it with or without A1.

**Reversible**: one block and one summary line. Rollback below.

### Detect

```bash
grep -c 'NO GIT IDENTITY' .claude/commands/session-start.md   # 0: not adopted
```

### Adoption-Mode Table

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `.claude/commands/session-start.md` | **TEMPLATE-COPY**, or **PATCH** Step 4 and Step 5 item 9 | Re-copy if yours is unmodified from the template (that also applies A1). Otherwise paste the second bash block of Step 4, the two paragraphs after it, and item 9 of Step 5. If your environment is not `.venv`, change the `VIRTUAL_ENV` comparison to your path. |
| 2 | `tests/unit/test_session_start_checks.py` | **OPTIONAL** | 9 tests that pin the three checks and the venv pytest line of A1. Take it if you keep template pins and have applied A1. |

### Action required

1. Re-copy or patch the command file.
2. Run `/session-start` once. Item 9 reads "all present", or lists each line the checks printed.

### Rollback

Remove the block and item 9. The checks are read-only; there is no state to undo.

### Files (tacsop)

```
.claude/commands/session-start.md          (Step 4 checks, Step 5 item 9; merged d98428a)
tests/unit/test_session_start_checks.py    (9 pins; 2a2e725)
```

---

## B. YYYY-MM-DD: Verifying Claims: a Kernel for Success Claims (`verifying-claims` 1.0.0)

A work-terminal Insights report found overclaims in at least 6 of 22 sessions: success reported because nothing errored, not because anything proved it. The shapes: a run called live when its log ended in a traceback; a mirror called synced when only the push was checked; an environment called unbuilt when `find` would have shown it; a fix called done when no run had exercised it; a validation reported that never ran; a number carried forward from earlier in the session.

The `verifying-claims` skill is a six-rule kernel, four claim states (written, tested, deployed, observed), one read-only probe per claim type, and five traps the probe table cannot hold. `EXAMPLES.md` holds seven before/after pairs and one clean report. The kernel's ambient copy lives in `CLAUDE.md` as a Claim Style block, and a test fails if the two copies differ. `/session-end` requires a `## Claims` table with two count lines under it, and `code-reviewer` re-runs the probe for each claim the change rests on.

**Result of the controlled replay (task 2d)**: FILL AT RELEASE. Six incident turns and six clean turns, each run with and without the kernel, scored by a non-author. Pass: the kernel arm flags at least 5 of 6 incidents, at most 1 of 6 clean turns, and at least 2 more incidents than the no-kernel arm.

**What the hub's first session under the kernel showed** (2026-10-01): reviewers refuted 16 of the lead's claims after the kernel was ambient, and the user caught 0. The control that worked was a second agent's re-run. That is why the reviewer line ships as one of the six surfaces, and why this entry's Action Required is all six, not the skill alone.

**Audience**: every repo.

**Reversible**: yes. Rollback below.

### Detect

```bash
test -d .claude/skills/verifying-claims || echo "skill missing"
grep -c '^## Claim Style' CLAUDE.md                        # 0: kernel block missing
grep -c 'Success claims' .claude/agents/code-reviewer.md   # 0: reviewer line missing
grep -c '## Claims' .claude/commands/session-end.md        # 0: the table is not required
```

### Adoption-Mode Table

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `.claude/skills/verifying-claims/` | **TEMPLATE-COPY** | `SKILL.md` and `EXAMPLES.md`. `scripts/adopt_doctrine.py` copies it (from 2026-10-02). |
| 2 | `.claude/commands/session-end.md` | **TEMPLATE-COPY** or **PATCH** | Step 5 gains "The Claims table" and the two count lines. The helper copies the whole file. See Open item 1: the file also carries WHETSTONE's `KB-graph:` line. |
| 3 | `docs/session-doc-format.md` | **TEMPLATE-COPY** or **PATCH** | Claims joins Summary and Next Steps as a required section. The helper copies it. |
| 4 | `.claude/skills/SKILLS_FRAMEWORK.md` | **TEMPLATE-COPY** | The Level 0 block and the inventory tree name the skill. The helper copies it. |
| 5 | `CLAUDE.md` | **PATCH** | Paste the `## Claim Style` block from the hub's `CLAUDE.md`. By hand. |
| 6 | `.claude/agents/code-reviewer.md` | **PATCH** | The "Success claims" checklist line. By hand, alone in a `[gate]` commit. |
| 7 | `.claude/README.md` | **PATCH** | Name the skill in the skills tree. By hand. |
| 8 | `tests/unit/test_verifying_claims.py` | **OPTIONAL** | 26 pins. They read rows 1 to 7 and the skill's two files, so take all seven rows or none of the tests. |

### Action required

1. Run `scripts/adopt_doctrine.py --dry-run` from your repo root, then without the flag. Rows 1 to 4 land.
2. Paste the three by-hand surfaces (rows 5 to 7). Commit the reviewer line alone, tagged `[gate]`.
3. If you took the tests: `.venv/bin/pytest tests/unit/test_verifying_claims.py -q` passes.
4. At your next `/session-end`, write the `## Claims` table and the two count lines. Zero is a count; write it.

### Rollback

Delete the skill directory, remove the block, the line, and the name, and restore `session-end.md` and the format doc. The tests go with them.

### Files (tacsop)

```
.claude/skills/verifying-claims/SKILL.md       (105 lines)
.claude/skills/verifying-claims/EXAMPLES.md
.claude/commands/session-end.md                (Step 5: the Claims table)
docs/session-doc-format.md
.claude/skills/SKILLS_FRAMEWORK.md
.claude/agents/code-reviewer.md                (one line)
.claude/README.md                              (one line)
CLAUDE.md                                      (the Claim Style block)
tests/unit/test_verifying_claims.py            (26 tests; merged ff0d8b2)
```

---

## C. YYYY-MM-DD: Test Isolation Tripwire (`shift-left-testing` 2.2.0)

A test suite deleted about 138 GB of real cached data, in a session that was building cache-eviction code. The guard fixture existed; it covered the wrong paths. The design answer is to pass the root in: code that deletes takes its root as a parameter, and every test points it at `tmp_path`. The backstop is `tests/isolation.py`, a pytest plugin. While a test runs, a delete outside an allowlist, a network connection to anything but this machine, or a `load_dotenv` that would read the repo's real `.env` raises `IsolationError` and appends one line to `.claude/audits/isolation-tripwire.log`.

`ISOLATION.md` lists what the tripwire cannot see: overwrites and moves, shell strings, child processes, C extensions, code outside a test, and more. Read that list before trusting a green run.

**Audience**: every repo with a pytest suite.

**Reversible**: two files and two `addopts` tokens. Rollback below.

### Detect

```bash
grep -c 'tests.isolation' pyproject.toml   # 0: not adopted
```

### Adoption-Mode Table

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `tests/isolation.py` | **COPY** | The plugin. Needs `tests` importable as a package (`tests/__init__.py`). |
| 2 | `tests/unit/test_isolation.py` | **COPY** | 43 tests, the registration canary: with the plugin unregistered, its catch tests fail. |
| 3 | `pyproject.toml` `[tool.pytest.ini_options]` | **PATCH** | `addopts = ["-p", "tests.isolation", "-p", "pytester"]`. Not `pytest_plugins` in `conftest.py`: pytest runs a whole conftest before it reads that line. |
| 4 | `.claude/skills/shift-left-testing/` | **TEMPLATE-COPY** | 2.2.0 adds `ISOLATION.md` and the `SKILL.md` lines that point at it. Entry D's 2.2.1 changes `CI.md`; one re-copy covers both. |
| 5 | `.gitignore` | **CONDITIONAL** | `.claude/audits/` must be ignored. The shift-left audit hook already needs it. |

### Action required

The four steps under "Adopting Downstream" in `ISOLATION.md`: copy the two files, patch `addopts`, run the suite with and without `CI=true` and read the log, check the gitignore. Each log line is a test reaching the real world (fix the test: pass the root in) or a directory that belongs in `isolation_allow`.

Measured at the hub: 308 existing tests ran armed with 0 catches (2026-09-30, after three gate rounds). The full suite, apart from the 38 matplotlib and pandas tests, passed on Python 3.11.15 on 2026-10-01 at `84dd487` (the Claims table of that day's session record); the 43 tripwire tests have no library skips, so they were in that run, and they pass on 3.12.13.

### Rollback

Remove the two tokens from `addopts` and delete the two files. The log file is yours to keep or drop.

### Files (tacsop)

```
tests/isolation.py
tests/unit/test_isolation.py
tests/conftest.py                                  (a comment pointing at addopts)
pyproject.toml                                     (addopts)
.claude/skills/shift-left-testing/ISOLATION.md
.claude/skills/shift-left-testing/SKILL.md         (2.2.0; merged d03e66a)
```

---

## D. YYYY-MM-DD: Pin Every `uv pip` Command to the Project Venv (`python-venv-management` 3.1.0, `shift-left-testing` 2.2.1)

A `VIRTUAL_ENV` inherited from another repo's shell outranks this project's `.venv`, and a bare `uv pip install` lands there. Every living doc now writes `uv pip <command> --python .venv`. The Standard is a grep that prints nothing.

**Audience**: every repo on uv (the 2026-08-03 entry).

**Reversible**: one flag per line. Rollback below.

### Detect

```bash
grep -rnE 'uv pip (install|sync|uninstall)' CLAUDE.md README.md .claude/ | grep -v -- '--python'
```

Any line printed is an unpinned command.

### Adoption-Mode Table

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `.claude/skills/python-venv-management/` | **TEMPLATE-COPY** | 3.1.0: `SETUP.md`, `TROUBLESHOOTING.md`, and `SKILL.md` carry the flag, and no `VIRTUAL_ENV=` line remains. |
| 2 | `.claude/skills/shift-left-testing/` | **TEMPLATE-COPY** | 2.2.1: the `CI.md` install step and its two notes. |
| 3 | `CLAUDE.md`, `README.md`, `LANGUAGE.md` | **PATCH** | Add `--python .venv` to each hit the Detect grep prints. |
| 4 | In-code install hints | **CONDITIONAL** | A module that prints `uv pip install` on `ImportError` prints the flag too. Open at the hub as a P2. |

### Action required

1. Run the Detect grep. Add the flag to each line it prints, reading the sentence around each: a mechanical pass inverted two sentences about bare commands at the hub.
2. Re-copy the two skills.
3. Re-run the grep. It prints nothing.

### Rollback

Remove the flag. Nothing else in those lines changes.

### Files (tacsop)

```
.claude/skills/python-venv-management/SKILL.md            (3.1.0)
.claude/skills/python-venv-management/SETUP.md
.claude/skills/python-venv-management/TROUBLESHOOTING.md
.claude/skills/shift-left-testing/CI.md
.claude/skills/shift-left-testing/SKILL.md                (2.2.1)
CLAUDE.md, README.md, LANGUAGE.md                         (merged d98428a)
```

---

## E. YYYY-MM-DD: Task-Condition-Standard Tables Gain a Purpose Column

The TCS table is now `| Task | Purpose | Condition | Standard |`. Purpose names who gets the output and what decision it informs. Fill it before planning the work; if you cannot, ask. Condition and Standard never ask what the output is for, and the task spec is where wrong-question work costs least to catch: a walkthrough built when the need was a calibration cost a session.

**Audience**: every repo with `/task`, `CONOP-FORMAT.md`, or `OPORD-FORMAT.md`.

**Reversible**: an added column. Rollback below.

### Detect

```bash
grep -c '| Task | Purpose | Condition | Standard |' .claude/commands/task.md docs/plans/CONOP-FORMAT.md docs/plans/OPORD-FORMAT.md
```

A 0 on any line: that file is not adopted.

### Adoption-Mode Table

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `.claude/commands/task.md` | **PATCH** | The Level 2 TCS block: the table header, two example rows, and the Purpose paragraph. |
| 2 | `docs/plans/CONOP-FORMAT.md`, `docs/plans/OPORD-FORMAT.md` | **TEMPLATE-COPY** or **PATCH** | The task table in each wave block, and the one-line pointer to `task.md`. |
| 3 | Existing plans | **NO ACTION** | Records. A plan still in execution may add the column at its next wave. |

### Action required

1. Patch the three files, or re-copy the two format files.
2. The next TCS you write carries a Purpose for each row.

### Rollback

Drop the column. Rows lose nothing that Condition and Standard held.

### Files (tacsop)

```
.claude/commands/task.md                 (Level 2)
docs/plans/CONOP-FORMAT.md
docs/plans/OPORD-FORMAT.md               (merged d98428a)
```

---

## F. YYYY-MM-DD: An Agent's Output Goes Where Its Input's Sensitivity Lives; Pre-Commit Check 7 Keeps Private Terms Out of a Public Tree

On 2026-10-01 three agents reviewed another project's plan, staged in `/tmp`, and were told to write reports into this repo's `docs/reviews/` and `docs/plans/`. This repo is public. The reports arrived carrying an internal hostname, a colleague's username seventeen times, an internal codename, and another repository's name. Nothing was committed, and `code-reviewer` sanitized its own draft and said so, but that was luck, not a control. The same day, the record of the containment pasted the five terms into an `Evidence:` line, committed and pushed. It was found and redacted on 2026-10-02.

Two controls, one at the point of action and one at the push gate:

1. **The rule.** An agent's output goes to the repository that owns the sensitivity of its input, not to the working directory the agent runs in, with one test the agent can run: if the material's path is outside this repository's working tree (not under `git rev-parse --show-toplevel`) or it was handed over from outside, write to the scratchpad and name the owning repository in the final message, or describe it when its name is itself private. It is written under the scope matrix in `.claude/README.md`, in the Write scope of each reviewing agent (`code-reviewer`, `proposer`, `decision-scientist`), and in the two team templates that name a destination.
2. **`/pcc` check 7, Private-Term Check.** A list of private terms lives outside every repository, one per line, at `$HOME/.config/tacsop/private-terms` (override with `TACSOP_PRIVATE_TERMS`). The check runs `git grep -l -i -F` with that list over the index and over every commit not on any remote, and also checks tracked file names and unpushed commit messages. It prints each hit as a path with no commit prefix or count, withholds the paths that themselves hold a term and reports those as a count, and does the same for file names and messages. Any line is FAIL. No list, or no git repository, is WARN: the check did not run.

**Audience**: the rule, every repo whose agents read another repository's material. The check, every public repo. The list is per machine, not per repo, and it is never committed anywhere.

**Reversible**: yes. Rollback below.

### Detect

```bash
grep -c '### 7. Private-Term Check' .claude/commands/pcc.md   # 0: not adopted
test -s "${TACSOP_PRIVATE_TERMS:-$HOME/.config/tacsop/private-terms}" || echo "no list on this machine"
```

### Adoption-Mode Table

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `.claude/commands/pcc.md` | **PATCH** | Check 7 and its Quick Reference row. Alone in a `[gate]` commit. |
| 2 | `.claude/agents/code-reviewer.md` | **PATCH** | One sentence in the Write scope. Alone in a `[gate]` commit. |
| 3 | `.claude/agents/proposer.md`, `.claude/agents/decision-scientist.md`, `.claude/README.md`, `.claude/teams/feature-development.md`, `.claude/teams/decision-science.md` | **PATCH** | The same sentences; one paragraph under the scope matrix; one clause where a template names `docs/plans/` or `docs/reviews/` as a destination. |
| 4 | `tests/unit/test_pcc_private_terms.py` | **OPTIONAL** | Runs the check in scratch repos: content, path names, file names, unpushed commits and their messages, a binary, a subdirectory, list trimming, no list, no repo; the term is never in the output. Pins the rule on six surfaces. |
| 5 | `$HOME/.config/tacsop/private-terms` | **Per machine**, not an artifact in the repo | Hostnames, usernames, codenames, repository names that must not appear in a public tree. One per line; matched case-insensitively as fixed strings, inside words too, so choose distinctive terms. |

### Action required

1. Write the list on each machine you push from. Terms are matched case-insensitively as fixed strings.
2. Patch the gate surfaces, each in its own `[gate]` commit.
3. Run check 7 once against HEAD. A FAIL line on an old commit is a leak already pushed: redact forward, then decide about history.

### One lesson that travels

A probe for an absence names what it looks for, and an `Evidence:` line pastes the probe. On 2026-10-01 the hub's own record of keeping five private terms out of this public repo pasted the five terms, in the Evidence line that certified their absence. When the names must stay out, record the count and where the list lives, never the list.

### Rollback

Remove the check and the sentences. The list file is harmless on its own.

### Files (tacsop)

```
.claude/commands/pcc.md                    (check 7, Quick Reference)
.claude/agents/code-reviewer.md
.claude/agents/proposer.md
.claude/agents/decision-scientist.md
.claude/README.md                          (under the Scope Matrix, and one line)
.claude/teams/feature-development.md
.claude/teams/decision-science.md
tests/unit/test_pcc_private_terms.py
```

---

## G. YYYY-MM-DD: `permissions.ask` Rules for Irreversible Commands (task 1e)

FILL WHEN 1e LANDS. Ships alone as a `[gate]` change to `.claude/settings.json`: `permissions.ask` over `rm` with recursive flags, `git add -A`, `git add .`, `git add -u`, `git commit -a`, `git clean`, and `mc rm`, as tuned by falsifier A4. Record the Claude Code version and the permission mode the rules were verified in (falsifier 0b), and whether `bypassPermissions` honors them.
