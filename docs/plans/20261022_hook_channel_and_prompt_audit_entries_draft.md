# Hook Channel and Prompt Audit Entries: Draft

**Status**: DRAFT, awaiting the user's go. Written 2026-10-22 by the lead with the user away. This file lives in `docs/plans/`, which `scripts/propagate_doctrine.py` does not read, so no run can send it.

**Sources**: [20261022_anthropic_docs_feed_proposer.md](../reviews/20261022_anthropic_docs_feed_proposer.md), [20261022_anthropic_docs_feed_review.md](../reviews/20261022_anthropic_docs_feed_review.md), [20261022_prompt_audit_hub.md](../reviews/20261022_prompt_audit_hub.md), [20261022_hook_channel_and_audit_application_gate.md](../reviews/20261022_hook_channel_and_audit_application_gate.md). **Protocol**: [propagation-protocol.md](../propagation-protocol.md), Rules 2 to 4.

**At release**, in order:

1. Settle the open items below.
2. Fill the dates. One date for both entries; the delivery mark matches headings, not dates.
3. Copy each entry to the top of `docs/doctrine-updates.md`, newest first, H then P.
4. Pre-flight each against the Evaluation Gate's five questions. Dry run. Propagate on the user's go.

**Open items, each the user's decision**:

1. **Entry H ships before the Windows run.** The review of 2026-10-22 asked for a Windows Git Bash run of the new hook and a `claude --version` on each box before the hook reaches about 20 repos. Neither has happened. The hook builds its JSON with `jq`, which the script already required, and a Windows path is normalized before use; the risk is low but unmeasured. Ship with the caveat in the entry, or hold H until the next work-terminal visit runs the hook once there.
2. **Entry P and the OVERWATCH hold.** Rows 7 and 8 of P's table delete footers from `shift-left-testing/SKILL.md` and `verifying-claims/SKILL.md`. Both files carry held OVERWATCH content (the 2026-10-01 hold: no OVERWATCH entry propagates until tasks 1e and 2d are done). The rows are written as PATCH (delete the section) and not TEMPLATE-COPY, so a consumer that follows them copies nothing held. Confirm that reading of the hold, or move those two rows into the OVERWATCH release draft.
3. **Entry P is a bundle under Rule 3.** It carries eleven skill footers, a command rewrite, and six phrasings. Rule 3 says to bundle such changes with the next substantive cycle rather than cycle for them alone; H is substantive, so P rides with it. If H is held (item 1), P waits with it.
4. **The register and `.github`.** Neither entry covers the Anthropic source register; it does not exist yet. It is a task, not an entry.

---

## H. YYYY-MM-DD: The Audit Hook, Two Corrections: the Import Grep Accepts `src.`, and the Warning Reaches the Agent

Two defects in `.claude/hooks/post-tool-shift-left-audit.sh`, both present in every copy made since 2026-08-27 and 2026-05-19 respectively.

**The import grep never matched a `src.` import.** The 2026-08-27 Part 3 fallback counts a feature-named test as a partner when it imports the module. It looked for `from <pkg>.<module> import`, while every test in a repo laid out like the template writes `from src.<pkg>.<module> import`. In such a repo the fallback never fired, and every feature-named suite logged `MISSING_TEST` for every edit to a shared module. Found by agent-eval's gate on 2026-10-06 (53 such imports, 0 bare); fixed in the hub the same day, test-first (`9413238` red, `d39305d`).

**The warning reached nobody.** The hook wrote its `MISSING_TEST` warning to stderr and exited 0. Claude never sees stderr from a hook that exits 0 (hooks reference, "Exit code 0", read 2026-10-22), and a PostToolUse hook cannot undo the write. `ENFORCEMENT.md` claimed the harness surfaced the warning in the tool result; it did not, from 2026-05-19 to 2026-10-22. The hook now prints one JSON object on stdout: `hookSpecificOutput.additionalContext` carries the warning to the agent beside the tool result, and `systemMessage` shows it to the user. Exit 0 on every path is unchanged. Observed on 2026-10-22 and 2026-10-23 under Claude Code 2.1.309 in scratch repos: with the new hook the agent quoted the warning verbatim; with the old hook it reported receiving nothing; both logged `MISSING_TEST`. An exit-2 variant of the old hook reached the agent framed as `PostToolUse:Write hook blocking error from command: ...` on a write that had succeeded, which is why the hook keeps exit 0 and JSON. In a `--output-format stream-json` run the `systemMessage` arrived as a `system` event of subtype `informational`, level `notice`, reading `PostToolUse:Write says: [shift-left-audit] No test partner for probe.py; expected tests/**/test_probe.py`; in an interactive session the same line shows to the user. Fixed test-first (`58d1989` red, `16f664e`; gate review `docs/reviews/20261022_hook_channel_and_audit_application_gate.md`).

**Audience**: every repo with `.claude/hooks/post-tool-shift-left-audit.sh`. A repo that patched the first defect on its own (agent-eval did, 2026-10-06) takes the second alone.

**Reversible**: one file plus one sidecar. Rollback below.

### Detect

```bash
# Defect 1: a feature-named test that imports with the src. prefix is not a partner.
# Expect OK_TEST_EXISTS in the last log line; MISSING_TEST means the old grep.
m=$(ls src/*/ -d | head -1 | xargs basename); f=$(ls src/$m/*.py | grep -v __init__ | head -1); b=$(basename "$f" .py)
grep -rlE "^(from|import) src\.$m\.$b\b" tests --include='test_*.py' | head -1   # a file here, and then:
printf '{"tool_name":"Edit","tool_input":{"file_path":"%s"}}' "$PWD/$f" | bash .claude/hooks/post-tool-shift-left-audit.sh; tail -1 .claude/audits/shift-left-violations.log
# Defect 2: the warning channel. 0 means the silent stderr form.
grep -c 'hookSpecificOutput' .claude/hooks/post-tool-shift-left-audit.sh
```

### Adoption-Mode Table

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `.claude/hooks/post-tool-shift-left-audit.sh` | **TEMPLATE-COPY** | Copy the hub's file. `adopt_doctrine.py` substitutes the package name at the three sites; by hand, replace `myproject` in the `*/src/myproject/*.py` glob. Keep the exec bit (`git update-index --chmod=+x`). |
| 2 | `.claude/skills/shift-left-testing/ENFORCEMENT.md`, step 5 and the exit paragraph | **PATCH** | Replace the two sentences with the hub's. The rest of the file is unchanged by this entry; do not copy the whole file while the OVERWATCH hold stands. |
| 3 | `tests/unit/test_shift_left_hook.py` | **CUSTOMIZE** | Copy the hub's 16 tests and change `myproject` to your package. A repo without the file gains it. |

### Action required

1. Run Detect. Two clean results mean nothing to do.
2. Copy the hook (row 1), patch the sidecar (row 2), copy the tests (row 3), run them.
3. Edit a module under `src/` once and look for the `[shift-left-audit]` line in your transcript. Its absence after a `MISSING_TEST` log line is the finding to report upstream.

### Rollback

Restore the hook, the sidecar, and the test file from git. The warning returns to stderr, where nobody reads it.

### Files (tacsop)

```
.claude/hooks/post-tool-shift-left-audit.sh         (9413238, d39305d, 58d1989, 16f664e)
.claude/skills/shift-left-testing/ENFORCEMENT.md     (16f664e)
tests/unit/test_shift_left_hook.py                   (9413238, 58d1989)
```

---

## P. YYYY-MM-DD: Instruction Files After a Prompt Audit: Eight Stale Facts and Six Dated Phrasings

Anthropic's prompt-audit procedure (`/doctor prompt-audit` since Claude Code 2.1.283; the same guide ships in the `claude-api` skill) was run over the hub's 29 instruction files on 2026-10-22, against Claude Fable 5.1: `CLAUDE.md`, the agents, commands, teams, and the 13 `SKILL.md` files. It found 20 findings, 8 high; all 29 proposed hunks were applied (`e744d64`, `4d4b476`). The ones that travel are below. The rest were hub-specific facts (the `CLAUDE.md` tree, the prototyper's module list) and are listed so a consumer can run the same audit on its own copies.

Three findings reach every consumer. `/session-end` Step 6 still taught the branching rule the topic-branch skill retired on 2026-06-28 ("if a major milestone, consider merging to main"). The ADR skill's next-number command, `ls docs/adr/ | tail -1`, prints `ADR-FORMAT.md` because the template sorts last, so a model following it numbers the next ADR wrong. Eleven `SKILL.md` bodies carried version histories and "Maintained by" footers that load on every trigger and prescribe nothing; three named sibling repositories, which `SKILLS_FRAMEWORK.md` forbids in a Level 0 skill. The histories now live in the frontmatter `version:` field, `CHANGELOG.md`, and git.

**Audience**: every repo with `.claude/commands/session-end.md`, the ADR skill, or any of the eleven skills. The audit itself applies to every repo: run `/doctor prompt-audit` on your own instruction files.

**Reversible**: every change is one file and restores from git.

### Detect

```bash
grep -n 'consider merging to main' .claude/commands/session-end.md          # a hit: the retired rule
grep -n 'ls docs/adr/ | tail -1' .claude/skills/recording-architecture-decisions/SKILL.md   # a hit: numbers the next ADR wrong
grep -ln -E '^\*\*Maintained by\*\*|^## Version History|^## Sources' .claude/skills/*/SKILL.md   # each file: a footer to move
grep -n 'Keep it to one screen' .claude/commands/sitrep.md
grep -n "Don't Read Unless Needed" .claude/commands/session-start.md
```

### Adoption-Mode Table

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `.claude/commands/session-end.md`, Step 6 | **PATCH** | Replace the four lines with the hub's "Land the Branch". Step 2 also loses a dated aside. |
| 2 | `.claude/skills/recording-architecture-decisions/SKILL.md`, step 2 | **PATCH** | `ls docs/adr/ \| grep -E '^[0-9]{4}-' \| tail -1`. |
| 3 | `.claude/commands/pcc.md`, checks 5 and 7 comments | **PATCH** | Comment lines only; the bash is unchanged. Commit alone, per check 6. |
| 4 | `.claude/commands/sitrep.md`, `.claude/commands/session-start.md` | **PATCH** | The screen cap becomes an audience statement; the reference heading loses its discouragement. |
| 5 | `.claude/agents/proposer.md` | **PATCH** | The thinking-depth bullet goes; the heading is "Proposal Guidelines". Depth is the `effort` frontmatter field if a repo wants it. |
| 6 | `.claude/skills/using-topic-branches/SKILL.md` | **PATCH** | Two migration-relative sentences and the Sources section go. |
| 7 | `.claude/skills/shift-left-testing/SKILL.md` footer | **PATCH** | Delete the footer only. The file carries held OVERWATCH content; do not copy it whole until that release. |
| 8 | `.claude/skills/verifying-claims/SKILL.md` footer | **PATCH** | Same hold. A repo without the skill does nothing. |
| 9 | The other nine skill footers and histories | **PATCH** or **TEMPLATE-COPY** | `configuration-management`, `python-venv-management`, `maintaining-project-context`, `maintaining-the-common-operating-picture`, `traversing-the-knowledge-base` (gains `version: "1.0.2"` in frontmatter), `designing-clear-data-displays`, `writing-simple-and-direct`, `lake-conventions`, `maintaining-ubiquitous-language`. Copy whole if your copy matches the hub's last entry; otherwise delete the section. |
| 10 | `CHANGELOG.md` | **PATCH** | One line under Unreleased, Changed, noting the move. |
| 11 | `CLAUDE.md`, the IMPORTANT booster and the project tree | **CUSTOMIZE** | Hub-specific. The audit's finding travels: a file-by-file tree rots; a directory-level tree pointing at `.claude/README.md` does not. The memory page's 200-line guideline (October 2026) applies to every `CLAUDE.md`. |
| 12 | Your own instruction files | **CUSTOMIZE** | Run `/doctor prompt-audit` (Claude Code 2.1.283 or later). Apply nothing from it unread. |

### Action required

1. Run Detect. Apply rows 1 to 10 where it hits.
2. Run `/doctor prompt-audit` and triage its report (row 12).
3. Measure `wc -l CLAUDE.md` and decide what moves to a skill or `.claude/rules/` if it exceeds 200.

### Rollback

Every file restores from git. Nothing here changes a test or a bash block.

### Files (tacsop)

```
.claude/commands/session-end.md, sitrep.md, session-start.md     (4d4b476)
.claude/commands/pcc.md                                           (e744d64, gate)
.claude/agents/proposer.md, python-prototyper.md                  (4d4b476)
.claude/skills/*/SKILL.md, eleven files                           (4d4b476)
CLAUDE.md, CHANGELOG.md                                           (4d4b476)
docs/reviews/20261022_prompt_audit_hub.md                         (the audit; 0c1fbdd)
```
