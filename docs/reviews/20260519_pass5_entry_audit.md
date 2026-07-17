# Review: Pass 5 — doctrine-updates.md 2026-05-19 Entry (Pre-Propagation Gate)

**Author**: code-reviewer
**Date**: 2026-05-19
**Type**: Pre-propagation entry audit

---

## Audit Lens

This is the final gate for the entry that will ship to ~11 downstream repos. Pass 4 cleared the artifacts; this pass audits whether the **instructions for adopting them** are executable as written. Errors cost 11x.

Verified directly against artifacts: hook script, settings.json, all three refactored skills + sidecars, ADR-0001, ADR-FORMAT.md, python-prototyper.md, session-end.md, session-doc-format.md, pyproject.toml, project.yaml, .gitignore, CLAUDE.md, CONTEXT.md, LANGUAGE.md, propagation-protocol.md, propagate_doctrine.py.

The propagation regex `## \d{4}-\d{2}-\d{2}:` was simulated on the live file. Extraction succeeds cleanly: extracted body is 27,751 chars, first line is the correct entry header, last line is the Source Material section. No `## ` heading conflicts inside the entry (only `### ` and `####`); the `## Step 3.6:` heading at line 620 sits inside the 2026-03-24 entry, well below the regex split point. **Script compatibility: OK.**

The entry is well-structured, includes the master Adoption-Mode Table (a strong improvement over prior entries), and the Suggested Adoption Order in §13.5 sequences correctly. Most steps are executable as written. Findings below are dominated by one FAIL (a wrong line count in §5), two CONCERNs that bite if a downstream maintainer is in a hurry, and several OK call-outs for high-risk items already verified.

---

## Findings

### FAIL-1 — §5 table: shift-left-testing SKILL.md line count is wrong

**Location**: §5, line 184 of doctrine-updates.md.
**Issue**: Entry says "8 files (SKILL.md 102 lines)". Actual `wc -l` on `.claude/skills/shift-left-testing/SKILL.md` is **103 lines**.
**Why it matters**: This is the only numeric line-count claim in the entry that downstream maintainers might use to verify they received the canonical version (e.g., during a manual diff against their existing single-file 1242-line predecessor). A maintainer copying the directory and confirming "SKILL.md is ~100 lines" will not be tripped up, but the table is presented as authoritative reference data. Trivial to fix.
**Fix**: Change `(SKILL.md 102 lines)` → `(SKILL.md 103 lines)`. Verify the other two counts are right (88 and 105 both check out).

### CONCERN-1 — §3 step 1 conflicts with §3 step 2 and the actual repo state

**Location**: §3, lines 152–157.
**Issue**: Step 1 says `mkdir -p docs/adr && touch docs/adr/.gitkeep`. Step 2 says copy `docs/adr/ADR-FORMAT.md`. The "Files added" list at line 26 lists both `docs/adr/ADR-FORMAT.md` and `docs/adr/.gitkeep`. **But** Adoption Mode row 5 packages them together as TEMPLATE-COPY. A downstream maintainer who does Step 1 (creating .gitkeep) and then drops ADR-FORMAT.md into the same directory has a non-empty directory — making the .gitkeep redundant. Not a bug, just redundant work; some maintainers will leave it, some will delete it, the entry should pick one.
**Why it matters**: Low-grade ambiguity. Eleven repos will end up in eleven slightly-different states. Recommend dropping the `.gitkeep` step or noting "skip if you already placed ADR-FORMAT.md in the directory".
**Fix**: Either drop `touch docs/adr/.gitkeep` from step 1, or add a parenthetical "(.gitkeep can be removed once any real file lands in docs/adr/)".

### CONCERN-2 — §7 step 3 path-glob substitution example is ambiguous for multi-package repos

**Location**: §7 step 3, lines 240–247.
**Issue**: The instruction says "If your repo has multiple packages, use `*/src/*/*.py` or an alternation `*/src/(pkg1|pkg2)/*.py`." The second example uses **regex alternation syntax inside a bash `case` glob**, which is invalid — `case` patterns are globs, not regexes. The hook actually uses `case "$file_path" in */src/myproject/*.py) ;;` which is a bash pattern. To match multiple packages in `case` you need `*/src/pkg1/*.py|*/src/pkg2/*.py)` (pipe at the pattern level, not inside parens).
**Why it matters**: A multi-package downstream maintainer who follows the example verbatim will write a syntactically wrong case branch that silently never matches, and the hook becomes a no-op for everything. They will not notice because the hook is supposed to be quiet on non-matches.
**Fix**: Replace the alternation example with the bash-correct form:
```bash
case "$file_path" in
    */src/pkg1/*.py|*/src/pkg2/*.py) ;;
    *) exit 0 ;;
esac
```
Drop the `*/src/*/*.py` suggestion or qualify it ("matches any package under src/, including third-party vendored code — use only if your src/ has no vendored packages").

### CONCERN-3 — §13 (settings.json rename) is an OS-level rename only; it does not migrate content

**Location**: §13 step 1, lines 382–385.
**Issue**: "If your repo has `.claude/settings.local.json` with team-wide content: rename to `.claude/settings.json`, commit." A downstream maintainer whose `.claude/settings.local.json` is gitignored (the more likely state — that's Anthropic's local-override default) will find that a bare `mv` plus `git add` does nothing because the source was never tracked. The entry should either acknowledge this case explicitly or use `cp` + delete + commit.
**Why it matters**: A maintainer who follows this literally and sees `git add` silently succeed will assume they're done. They have to verify the new file is actually staged. Low risk, but the "rename, commit" wording over-promises.
**Fix**: Reword step 1 to: "Copy the contents of `.claude/settings.local.json` (or your existing local settings) into a new `.claude/settings.json`. Commit `.claude/settings.json`. Confirm `.claude/settings.local.json` remains in `.gitignore` as a per-developer override."

### CONCERN-4 — §7 step 3 substitution instruction does not name the hook's hardcoded `myproject` consistently with §10's `<yourpkg>` placeholder

**Location**: §7 step 3 says "Replace `myproject` with your repo's package name." §10's template uses `<yourpkg>` as the substitution variable. §12 in the master table also uses `myproject` literally.
**Why it matters**: Trivial, but consistent placeholder style prevents grep-replace foot-guns when maintainers script the adoption. Pick one and use it.
**Fix**: Standardize on `<yourpkg>` (or `myproject` — your call) across §7, §10, and the master table row 12. Mention once at the top of §7: "throughout this section, substitute `myproject` with your repo's package name; `<yourpkg>` is used as the placeholder in template snippets."

### CONCERN-5 — Rollback section omits the `.claude/settings.json` rename and the `.gitignore` additions

**Location**: §13 (Rollback), lines 408–414.
**Issue**: Rollback covers the hook, the skill refactors, LANGUAGE/CONTEXT, the ADR system, and the Python bump. It does **not** mention how to roll back the settings.local.json → settings.json rename (§13) or the `.gitignore` additions (§12). For the rename, the rollback is non-trivial because it interacts with what the maintainer's per-user `.claude/settings.local.json` contained before.
**Why it matters**: Per the propagation-protocol.md Evaluation Gate Q5, every entry must have a rollback path for every artifact. This one has gaps.
**Fix**: Add two bullets:
- **`.gitignore` additions** — Remove the two added lines (`docs/design/hold/` and `.claude/audits/`) to revert. No data is lost; only future audit logs would re-appear in git status.
- **`settings.local.json` → `settings.json` rename** — Move the team-wide content back into `.claude/settings.local.json`, delete `.claude/settings.json`, and unignore `.claude/settings.local.json` in `.gitignore` if your team wants it tracked again. Note: per-user overrides written into `.claude/settings.local.json` after the rename will need to be merged manually.

### CONCERN-6 — §7 step 8 verification instruction may not work in fresh sessions

**Location**: §7 step 8, line 268.
**Issue**: "Verify by editing any file under your package's `src/`. Check `.claude/audits/shift-left-violations.log` for a fresh entry. If empty, open `/hooks` in Claude Code to reload settings, or restart the session." The `/hooks` command exists in Claude Code, but the entry assumes the maintainer is using Claude Code interactively at adoption time. If they adopt via a script or in a fresh session, this verification step is the only feedback loop, and the failure mode (empty log) is silent. Consider adding: "If the log file isn't created at all after editing a file, check that the hook script is executable (`ls -l .claude/hooks/post-tool-shift-left-audit.sh` should show `x` bits)."
**Why it matters**: Step 4 says `chmod +x`, but if a downstream maintainer's git config strips the exec bit on commit (common on Windows or with `core.fileMode false`), the hook will be silently inert. The verification step doesn't catch that case.
**Fix**: Add a sentence: "If the log file is missing entirely (not just empty), re-run `chmod +x .claude/hooks/post-tool-shift-left-audit.sh` — some git configs strip the exec bit."

### OK-1 — Settings JSON hook block in §7 step 5 matches `.claude/settings.json` byte-for-byte

Verified: the JSON snippet in the entry (lines 251–265) is identical to the `hooks.PostToolUse` block in the actual `.claude/settings.json` (lines 25–38). Matcher, command, timeout, and structure all match. **High-risk item, verified accurate.**

### OK-2 — Hook script path glob `*/src/myproject/*.py` is the literal pattern in the script

Verified: line 35 of `post-tool-shift-left-audit.sh` reads `*/src/myproject/*.py) ;;`. The §7 substitution instruction (find this case branch) is targetable by a downstream maintainer via grep. **OK.**

### OK-3 — ADR-0001 description in §3 matches the ADR contents

Verified: the entry describes ADR-0001 as "the same decision you adopt when you adopt SKILLS_FRAMEWORK v2." ADR-0001's Decision section confirms: "All new skills MUST be authored in directory form … regardless of expected size." The Decision-maker(s) field in the ADR (line 5) is `jhutchison (lead); code-reviewer, proposer, decision-scientist agents (Pass 4 review)` — which is what §3 step 4 tells downstream to edit for local attribution. **OK.**

### OK-4 — python-prototyper.md workflow §9 description matches the agent file

Verified: lines 28–37 of `.claude/agents/python-prototyper.md` contain the test-first workflow (Plan → RED → GREEN → no refactor while RED → full pytest) exactly as §9 of the entry describes. The pillars reference fix is also present (line 9 now points to `CONTEXT.md` and `config/project.yaml` instead of the missing `docs/design/pillars.md`). **OK.**

### OK-5 — Session-end command/skill dedup in §8 matches the file states

Verified: `.claude/skills/session-end.md` does not exist (deleted). `docs/session-doc-format.md` exists and contains the reference content. `.claude/commands/session-end.md` Step 5 (line 57–69) references `docs/session-doc-format.md` and does not duplicate the body. **OK.**

### OK-6 — Python 3.11 claim in §11 matches pyproject.toml and project.yaml

Verified: `pyproject.toml` line 9 is `requires-python = ">=3.11"`; `config/project.yaml` line 8 is `python_requires: ">=3.11"` and line 42 is `min_version: "3.11"`. **OK.** Note: pyproject.toml does not include `[project.classifiers]` (the entry claims it was updated). The classifiers table is not present in the file at all. This is a CONCERN only if you actually want the classifier listed; suppressing it is fine for an internal-only package. Recommend removing the `[project.classifiers]` claim from §11 line 350.

### OK-7 — .gitignore additions §12 match the file

Verified: `.gitignore` lines 58 (`.claude/audits/`) and 61 (`docs/design/hold/`) match the entry. The placement note ("append to your existing .gitignore") is accurate. **OK.**

### OK-8 — Propagation script extracts the entry correctly

Simulated the regex against the live file. Extracted entry body is the entire 2026-05-19 section, terminating cleanly at the 2026-04-21 entry boundary. No `## ` heading collisions inside the entry. The `## Step 3.6:` heading at line 620 sits inside an older entry and does not interfere. **OK.**

### OK-9 — All sidecar names in §5 table match the actual directory contents

Verified:
- `shift-left-testing/`: ANTIPATTERNS, CI, ENFORCEMENT, FIXTURES, MOCKS, PATTERNS, SKILL, TIERS, VERTICAL-SLICING (9 files including SKILL.md — entry says "8 files", and there are indeed 8 sidecars + SKILL.md, but "8 files" reads as the total. Minor: the entry's "8 files (SKILL.md 102 lines)" is ambiguous between "8 files total including SKILL.md" or "8 sidecars". Recommend "9 files: SKILL.md + 8 sidecars" for clarity. Not a FAIL because the sidecar list right after disambiguates.)
- `configuration-management/`: LOADER, SECRETS, STRUCTURE-AND-FILES, TESTING-AND-PATTERNS, VALIDATION (5 sidecars — matches "+ 5 sidecars").
- `python-venv-management/`: SETUP, TROUBLESHOOTING (2 sidecars — matches "+ 2 sidecars").

### OK-10 — CONTEXT.md and LANGUAGE.md starter-template framing matches actual content

Verified: §1 lists LANGUAGE.md sections (Decision Science, Agent Framework, Escalation Ladder, Governance & Propagation, Workflow Artifacts, Vocabulary Crosswalk, Anti-Glossary) — all seven exist in the live file. §2 lists CONTEXT.md sections (Identity, Mission, Current State, Constraints, Key Relationships, Reading Order, plus the "Distinguishing This File" table) — all present. The CUSTOMIZE adoption mode correctly captures that the content is utils-specific. **OK.**

### OK-11 — Adoption-Mode Table is internally consistent with per-section guidance

Spot-checked rows 1/§1, 7/§3, 9/§5, 12/§7, 17/§8, 19/§11. Each row's mode matches the language used in the corresponding section. No contradictions found. **OK.**

---

## Out-of-Scope but Worth Flagging

**Working tree is not yet committed.** `git status` shows ADR-0001, the entire `.claude/hooks/` directory, and `ENFORCEMENT.md` as **untracked**, plus several modified files. The propagation script only reads `docs/doctrine-updates.md`, so the script itself will run. But downstream maintainers receive a notification telling them to copy `.claude/hooks/post-tool-shift-left-audit.sh` from `utils` — and if they `git pull` and the file isn't there, the instruction is dead on arrival. **Commit and push before propagating.** This is a precondition, not a content issue with the entry.

---

## Propagation Verdict: **SHIP-WITH-FIXES**

Blocking fixes (must land before propagation):

1. **FAIL-1**: Correct SKILL.md line count in §5 table from 102 → 103. (Trivial; one character.)
2. **CONCERN-2**: Fix the `case`-pattern alternation example in §7 step 3 (regex syntax inside bash `case` is invalid and will silently disable the hook for multi-package downstream repos).

Non-blocking but strongly recommended:

3. **CONCERN-5**: Add `.gitignore` and settings rename rollback bullets in §13 — propagation-protocol.md mandates rollback for every artifact.
4. **CONCERN-3**: Reword §13 step 1 to clarify the rename is content-copy, not git-mv.
5. **CONCERN-6**: Add the exec-bit verification note in §7 step 8.
6. **CONCERN-1**: Resolve the `.gitkeep` redundancy in §3.
7. **CONCERN-4**: Standardize the `myproject` / `<yourpkg>` placeholder usage.
8. **OK-6 sub-note**: Drop the `[project.classifiers]` claim in §11 — the file doesn't have one.
9. **OK-9 sub-note**: Disambiguate "8 files" → "9 files: SKILL.md + 8 sidecars" in §5 table.

**Precondition** (not an entry fix, but blocks propagation): commit and push the working tree so downstream `git pull` finds the artifacts the entry references.
