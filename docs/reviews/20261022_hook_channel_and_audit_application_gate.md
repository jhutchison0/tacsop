# Review: Hook Channel Change and Prompt Audit Application

**Author**: code-reviewer
**Date**: 2026-10-22
**Type**: Code review (gate)

**Verdict: GO-WITH-FIXES.** The four commits do what their messages say. The hook change is correct against the hooks reference and the live transcripts support it. Every one of the 29 audit hunks landed exactly once, and no line outside a hunk changed. The fixes below are three claims that outrun their evidence, three hook behaviors the tests do not pin, and three path references the working tree's uncommitted task list carries. One item is the user's decision.

Scope: commits `58d1989`, `16f664e`, `e744d64`, `4d4b476` on `main`. Reference: the hooks page saved at the session scratchpad's `probe/hooks.md.out`, read as data. Private-terms check: the list at `~/.config/tacsop/private-terms` was loaded and scanned against every added line, commit message, and file name of the four commits, and against this report. Counts are in the Claims table; no term is reproduced here.

| Severity | Count |
|---|---|
| Critical | 0 |
| Warning | 4 |
| Suggestion | 6 |
| Needs the user's decision | 1 |

## Part 1: the hook change (`58d1989`, `16f664e`)

### What was verified

**The JSON shape is right.** `.claude/hooks/post-tool-shift-left-audit.sh:109-112` prints `{systemMessage, hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext}}`. The reference's "Add context for Claude" example (lines 1108 to 1115) uses the same nesting, the universal-fields table (line 1058) lists `systemMessage` at the top level, and the "JSON output" section (line 1051) requires `hookEventName` inside `hookSpecificOutput`. The reference's own PostToolUse test-runner example (line 4108) builds the object with the same `jq -nc --arg` idiom.

**One object on stdout and nothing else, on every path.** Read the script end to end: every other command that writes to stdout is inside `$(...)` or redirected to the log file. Probed with hostile inputs, all exit 0 with empty stderr:

| Input | stdout | Parsed as JSON |
|---|---|---|
| Plain path, no partner | 1 line, 597 bytes | yes, both keys, event `PostToolUse` |
| Directory name containing `"` | 1 line | yes, full path inside `additionalContext` |
| Directory name containing a newline | 1 line | yes, full path inside `additionalContext` |
| Directory name containing `\` | empty | not applicable (see Suggestion 1) |
| Name-matched partner present | empty | |
| Feature-named partner present | empty | |
| jq absent from PATH | empty | |
| git exits 127 | empty | |
| Empty stdin | empty | |
| Malformed JSON on stdin | empty | |
| `tool_name` is `Read` | empty | |
| Windows-style path | empty | |

**Nothing from the old stderr text is lost.** The old heredoc (five lines: the path, the expected partner, the TDD sentence, the sidecar pointer, the log pointer) is the new `warning` string at lines 104 to 108, verbatim. `systemMessage` is a one-line digest of the first two.

**The 16 tests pass and were red first.** At `58d1989` the three MISSING-path tests fail and the OK-path pin passes, run in a throwaway worktree. At `16f664e` and at HEAD all 16 pass.

**The transcripts support the claim.** Both scratch repos carry a hook identical to the hub's (new: identical to HEAD; old: identical to `16f664e~1`), the same `settings.json` matcher, and one `MISSING_TEST` log line each. The new-hook run's `result` field is `HOOK_CONTEXT=` followed by the five-line warning verbatim, with the scratch path; the old-hook run's is `HOOK_CONTEXT=NONE`. Both ran `claude-fable-5-1` in two turns. `claude --version` on this box prints 2.1.309, which the draft entry names.

**ENFORCEMENT.md step 5 is accurate.** Line 32's sentence "Claude never sees stderr from a hook that exits 0" is the reference's line 816 word for word, and the channel description matches lines 1104 and 1121 (context inserted next to the tool result).

### Findings

**Warning 1. The exit-2 sentence is an inference without evidence, and it ships in four places.** `.claude/hooks/post-tool-shift-left-audit.sh:9-10`, `.claude/skills/shift-left-testing/ENFORCEMENT.md:35`, the `16f664e` message, and `docs/plans/20261022_hook_channel_and_prompt_audit_entries_draft.md:29` all say exit 2 "would render a successful write as a hook error". The reference says something narrower and friendlier: line 993, "`PostToolUse` | No | Shows stderr to Claude; the tool already ran", and line 816 names exit 2 as the documented way to surface a PostToolUse warning. The reference never says the exit-2 notice marks the write as an error on this event; the `hook error` wording at line 845 describes a PreToolUse block. The design choice (JSON at exit 0, so the run is a success and the user gets a message) is sound, but the reason given for rejecting exit 2 is unverified. Fix, one of two: run the old hook with `exit 2` in the scratch repo under `claude -p` and paste what the agent and the transcript show, then keep the sentence with an `Evidence:` line; or reword the four sites to "the reference offers exit 2 for this; this hook uses JSON at exit 0 so the run stays a success and the user gets `systemMessage`". Do this before entry H leaves, because the sentence travels to about 20 repos.

**Warning 2. `systemMessage` reaching the user is unverified, and entry H's consumer check depends on it.** The experiment ran `claude -p` with JSON output; the reference (line 1058) says that in SDK and `stream-json` output `systemMessage` arrives as an informational message, and in an interactive session as a warning shown to the user. Neither was observed. The reference's line 1104 also says `additionalContext` "doesn't appear as a chat message in the interface", so entry H's action step 3 (`docs/plans/20261022_hook_channel_and_prompt_audit_entries_draft.md:59`, "look for the `[shift-left-audit]` line in your transcript") can only succeed through `systemMessage`. If that channel does not render for PostToolUse in the interactive UI, every consumer will report the "finding" the step describes. Fix: one interactive edit of a partnerless module in the scratch repo, or `claude -p --output-format stream-json` with the same prompt and a grep for the digest line; record what rendered. Before entry H leaves.

**Warning 3. Three hook behaviors the tests do not pin.** `tests/unit/test_shift_left_hook.py` pins the four claims in the commit (one object, both fields, empty stderr, silent OK path). Not pinned: stdout is empty when `jq` is absent (the module skips entirely without `jq`, so the branch at script line 22 has never run under pytest; a shadow `PATH` built from `/usr/bin` without `jq` makes it testable, and the probe above shows it empty); a directory name with `"` or a newline still yields one parseable object (probed above); the feature-named-partner path prints nothing (`test_feature_named_test_that_imports_the_module_counts_as_partner`, line 98, calls `_run_hook`, which discards stdout). Fix: three tests, each a copy of an existing one with one assertion added. Tonight if the entry goes this week; the probes are the evidence until then.

**Suggestion 1. A backslash in a Linux path silences the audit.** Line 34 turns every `\` into `/` before the `cd` at line 64, so a directory literally named `back\slash` resolves to nothing and the hook exits 0 with no log line and no JSON. Pre-existing since the Windows normalization; not caused by this change. Record it as a known gap in ENFORCEMENT.md or leave it; such paths are rare.

**Suggestion 2. The warning text is imperative.** Reference line 1139 asks for `additionalContext` written as factual statements, because text framed as a system command can trigger the model's prompt-injection defenses. "Vertical-slice TDD says: write a failing test first, then minimum impl to pass it" (script line 106) passed through cleanly in the live run, so this is low risk. If it is ever rephrased, "This project's rule is a failing test first, then the minimum implementation" is the factual form.

**Suggestion 3. `CHANGELOG.md` has no line for the channel change.** Earlier hook changes each got one under Unreleased (lines 24, 27, 37: Windows portability, the import-grep fallback). One line under Changed, tonight.

### What to test before entry H goes

1. Warning 2's interactive or `stream-json` run, so step 3 of the entry describes something a consumer can see.
2. Warning 1's exit-2 run, or the reword.
3. The Windows Git Bash run and `claude --version` on each box, already `docs/tasks.md` item P3. Note that the reference names no version floor for PostToolUse `additionalContext`; on an older Claude Code the hook still exits 0 and logs, and only the warning is lost, so the failure mode is the status quo.
4. `scripts/adopt_doctrine.py:166` substitutes `myproject` by plain global replace; the new hook adds no new occurrence, so the substitution is unchanged. No test needed.

## Part 2: the pcc.md gate commit (`e744d64`)

Verified. The file has 8 fenced bash blocks before and after; 6 are byte-identical and 2 (checks 5 and 7) differ only in lines beginning with `#`. The two non-comment changed lines are the blind-spot heading and bullet 1 in prose. `tests/unit/test_pcc_reference_integrity.py` and `tests/unit/test_pcc_private_terms.py` pass (32 tests). No finding.

## Part 3: the audit application (`4d4b476`, with the two session-end.md hunks)

### What was verified

All 29 hunks of `docs/reviews/20261022_prompt_audit_hub.md` were parsed and compared, file by file, against `git diff 0c1fbdd 4d4b476` (pcc.md against `e744d64`) as multisets of added and removed lines, and against the working tree. Result: 21 of 21 files match exactly; every hunk's `+` line is in the file once, no hunk's `-` line remains, and no added or removed line in the diff is outside a hunk. No hunk landed partially or twice. The two session-end.md hunks placed by hand (Step 2 and Step 6) match the audit's text exactly. The only files in the diff without a hunk are the three hook files, which belong to Part 1.

`.claude/skills/traversing-the-knowledge-base/SKILL.md` frontmatter parses as YAML with `version: '1.0.2'` as a string. Ten of the thirteen skill frontmatters parse; see Suggestion 5 for the two that do not, which predate this change.

Em dashes in added lines: 6 in `4d4b476`, 0 in the other three commits. All 6 are list-item label dashes (a bullet whose code or bold label is followed by the dash and then the text) in files whose sibling bullets already use that form (`python-prototyper.md`, `sitrep.md`, `using-topic-branches/SKILL.md`). None is in running prose.

Full suite: 549 passed, 1 pre-existing warning from `test_scorer.py`.

`/pcc` check 5, run bare from the current `pcc.md`:

| Pass | Candidates | MISSING | At `4d4b476` |
|---|---|---|---|
| File pass | 58 | 3 | 0 |
| Directory pass | 17 | 0 | 0 |

### Findings

**Warning 4. The working tree's uncommitted `docs/tasks.md` carries three path references that do not resolve.** Lines 7, 17 and 20 name `docs/sessions/20261022_anthropic_docs_feed_and_prompt_audit.md`, `docs/anthropic-sources.yaml` and `config/paperboy.yaml`. None exists. At `4d4b476` the count is 0, so the three commits under review are clean; the drift is tonight's task-list edit. The session doc will exist once `/session-end` writes it. The other two are planned artifacts. Fix tonight, the lead's call: write the two planned files without path shape until they exist ("a source register under `docs/`"), or keep them and record M2 = 2 with the reason in the session doc, which check 5's own rule requires either way.

**Suggestion 4. The `4d4b476` message says the IMPORTANT booster "states its reason"; it was removed.** Hunk 9 replaced the bold `IMPORTANT` line with a plain sentence that gives the reason (`CLAUDE.md:197`). The file is right; the message is loose. No fix possible without a rewrite; note it in the session doc.

**Suggestion 5. Two skill frontmatters fail strict YAML.** `.claude/skills/lake-conventions/SKILL.md:3` and `.claude/skills/recording-architecture-decisions/SKILL.md:3` have a `description` containing `: ` unquoted, so `yaml.safe_load` raises. Both fail at `0c1fbdd` too; not caused by this change. Claude Code's skill loader may be lenient, and the skills have been listed in sessions since, so treat as a task: quote the two descriptions and add a test that every `SKILL.md` frontmatter parses, which would also guard the `version:` field the audit now relies on.

**Suggestion 6. Records in `docs/doctrine-updates.md` still describe the stderr warning** (lines 1732, 1789, 1976). They are dated entries and stay as written under the picture rule; entry H supersedes them. Nothing to change. Listed so nobody "fixes" them.

### Needs the user's decision

**D1. Whether the user-facing `systemMessage` should ship at all.** The defect was that the agent never saw the warning; `additionalContext` alone repairs that. `systemMessage` adds a warning line in the user's transcript on every partnerless edit, in about 20 repos, which sits uneasily beside ENFORCEMENT.md's "output is evidence, not friction". Keep both, or drop `systemMessage` and keep the hook agent-facing. If dropped, Warning 2 and entry H's step 3 change shape (the consumer check becomes the log line plus the agent's own report).

## Claims

| Claim | State | Evidence |
|---|---|---|
| 16 hook tests pass at HEAD | tested | `.venv/bin/pytest -q tests/unit/test_shift_left_hook.py`: `16 passed in 0.38s` |
| The 3 new MISSING-path tests were red at `58d1989` | tested | worktree at `58d1989`, same command: `3 failed, 13 passed`; the 3 named `test_missing_partner_*` |
| The hook prints one parseable object with both fields on the MISSING path, and nothing on 11 other paths | observed | probe script output table above; plain case `stdout_lines=1`, `stderr=''`, keys `['hookSpecificOutput', 'systemMessage']` |
| Paths with `"` and a newline do not break the object | observed | probe: `[double-quote] ... json=parsed ctx_has_full_path=True`; `[newline] ... json=parsed ctx_has_full_path=True` |
| stdout is empty when jq is absent | observed | probe with shadow PATH: `[jq-absent] jq_on_path=None rc=0 stdout='' stderr=''` |
| The two scratch hooks are the hub's old and new hook | observed | `diff` of each against HEAD and `16f664e~1`: no output |
| The transcripts show the new hook's warning reaching the agent and the old one's not | observed | `result` fields: `HOOK_CONTEXT=[shift-left-audit] No test partner found for ...` and `HOOK_CONTEXT=NONE`; both logs carry one `MISSING_TEST` line |
| This box runs Claude Code 2.1.309 | observed | `claude --version`: `2.1.309 (Claude Code)` |
| Exit 2 on PostToolUse marks the write as a hook error | UNVERIFIED: not run; the reference's line 993 says only "Shows stderr to Claude; the tool already ran" | |
| `systemMessage` renders to the user for a PostToolUse hook | UNVERIFIED: the `-p` JSON run cannot show it | |
| pcc.md bash blocks are code-identical before and after `e744d64` | tested | fence extraction script: `blocks before/after: 8 8`, `byte-identical blocks: 6 of 8`, `identical ignoring comment lines: 8 of 8` |
| The two pcc test files pass | tested | `.venv/bin/pytest -q tests/unit/test_pcc_reference_integrity.py tests/unit/test_pcc_private_terms.py`: `32 passed` |
| All 29 hunks landed exactly, none partially or twice, no line outside a hunk changed | tested | hunk comparison script: `hunks parsed: 29`, `files matching exactly: 21 of 21` after a fence-aware re-check of `CLAUDE.md` (`proposed +/-: 22 27`, `applied +/-: 22 27`, no extras, no shortfalls) |
| `traversing-the-knowledge-base` frontmatter parses with the version field | tested | `yaml.safe_load`: `{'name': 'traversing-the-knowledge-base', 'version': '1.0.2'}` |
| Two other skill frontmatters fail strict YAML, before and after | tested | `lake-conventions 0c1fbdd FAIL`, `lake-conventions 4d4b476 FAIL`, `recording-architecture-decisions 0c1fbdd FAIL`, `recording-architecture-decisions 4d4b476 FAIL` |
| No em dash in running prose in any added line | tested | scan: `4d4b476: em_dash_lines=6 em_dash_in_running_prose=0` after reading the one flagged bullet, `e744d64: 0`, `16f664e+58d1989: 0` |
| No private term in any added line, commit message, or file name of the four commits, nor in this report | tested | scan over 6 terms: `private_term_hits_in_added_lines=0 in_messages=0 in_filenames=0` for all three ranges; `.claude/` tree 0 file-term pairs; this file 0 |
| Full suite passes | tested | `.venv/bin/pytest -q`: `549 passed, 1 warning in 5.62s` |
| `/pcc` check 5 file pass: 58 candidates, 3 MISSING, all from uncommitted `docs/tasks.md`; 0 at `4d4b476` | observed | block run bare: `file pass: candidates=58 missing=3`; `git show 4d4b476:docs/tasks.md` head: `0` matches |
| `/pcc` check 5 directory pass: 17 candidates, 0 MISSING | observed | block run bare: `directory pass: candidates=17 missing=0 output_bytes=0` |
| `adopt_doctrine.py` substitution still covers the new hook | observed | `scripts/adopt_doctrine.py:166`: `body.replace("myproject", package)`; new hook adds no `myproject` occurrence (`git diff 16f664e~1 16f664e` shows none) |
