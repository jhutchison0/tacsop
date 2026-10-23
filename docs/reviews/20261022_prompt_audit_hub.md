# Review: Prompt Audit of the Hub's Instruction Files

**Author**: code-reviewer
**Date**: 2026-10-22
**Type**: Config review (Anthropic prompt-audit guide, Steps 0 through 7)

## Assumptions (Step 0)

**Scope.** The request named the surface: `CLAUDE.md`, every file under `.claude/agents/`, `.claude/commands/`, and `.claude/teams/`, and the top-level `SKILL.md` of each directory under `.claude/skills/`. Sidecar files, `.claude/skills/SKILLS_FRAMEWORK.md`, `.claude/settings.json`, `.claude/settings.local.json`, `.env`, `.mcp.json`, `docs/design/hold/`, and user-level configuration under `~/.claude` were not read as audit surface. `SKILLS_FRAMEWORK.md`, `LANGUAGE.md`, `CONTEXT.md`, `config/project.yaml`, `pyproject.toml`, `CHANGELOG.md`, and the tests were read as repository facts to check claims against, not audited.

**Target model.** The files are read by Claude Code, so they are audited against Claude Fable 5.1, the model running this audit. Three agent files pin their own model and are audited against the current model of that line: `proposer` and `python-prototyper` pin `sonnet` (Claude Sonnet 5.5); `test-runner` pins `haiku` (Claude Haiku 5.5). `code-reviewer` and `decision-scientist` inherit and are audited against Claude Fable 5.1.

**Provenance.** `git blame` was run on every line this report proposes to change; each finding names the commit and date.

**Quoting.** Three Level 0 skill files and one command file name sibling repositories inside history narratives. The diff reproduces those lines verbatim, because a hunk must match to apply, and the lines are already tracked in this public repository. The Evidence fields in the report replace the names with `<repo>`.

**Verification (Step 7).** Every stale-fact and conflict finding was checked against the repository: the path listed, the command run read-only, both files read. No behavioral probe was run for the Group 1 findings; those removals are hypotheses to re-test on the next sessions that exercise the file.

## Summary

The surface is in good shape for its target model. Nothing in it steers thinking with prose, forces output through scaffolds, or suppresses narration, and the one capitalised booster in `CLAUDE.md` is the only pressure-language hit. The findings that matter are Group 2 facts the repository has outgrown, and they are multiplied by propagation to about twenty downstream repos.

Three findings carry the most weight. `/session-end` Step 6 still describes merging to `main` at "major milestones" from a standing branch, which is the branching convention the topic-branch skill retired on 2026-06-28; every session end reads the old rule. The `CLAUDE.md` project tree lists three of five agents, three of four teams, five of six commands, and eight of ten utility modules, and omits the `decision_science` package, so the file loaded into every session contradicts its own agent table forty lines below. The ADR skill's "find the next number" command prints `ADR-FORMAT.md`, not the latest ADR, so a model that follows it numbers the next ADR wrong.

| Group | High | Medium | Low (flag) | Total |
|---|---|---|---|---|
| 1 Dated prompt text | 0 | 5 | 1 | 6 |
| 2 Brittle configuration | 8 | 2 | 4 | 14 |
| 3 Tool descriptions | not applicable | | | 0 |
| 4 Request config and roster | 0 | 0 | 0 | 0 |
| **Total** | **8** | **7** | **5** | **20** |

Group 3 has no tool definitions in scope; the agent `description:` fields are trigger text and were read as such. Group 4 has no request-building code; the five-agent roster was inspected and holds no redundant pair.

## Inventory (Step 1)

| Surface | Files | Lines |
|---|---|---|
| `CLAUDE.md` | 1 | 218 |
| `.claude/agents/` | 5 (`code-reviewer`, `decision-scientist`, `proposer`, `python-prototyper`, `test-runner`) | 285 |
| `.claude/commands/` | 6 (`pcc`, `pci`, `session-end`, `session-start`, `sitrep`, `task`) | 753 |
| `.claude/teams/` | 4 (`bug-fix`, `code-review`, `decision-science`, `feature-development`) | 132 |
| `.claude/skills/*/SKILL.md` | 13 | 1,416 |
| **Total** | **29** | **2,804** |

Loaded every session: `CLAUDE.md`. Loaded on invocation: commands, agents, teams. Loaded on trigger: skill bodies (frontmatter loads every session).

## Findings, highest confidence first (Step 5)

### High

**H1. `/session-end` Step 6 contradicts the branching doctrine**

| Field | Content |
|---|---|
| Location | `.claude/commands/session-end.md:76-79` |
| Evidence | `## Step 6: Evaluate Merge Readiness` / `- Is this a major functional milestone?` / `- If yes, consider merging to main` / `- If no, continue on current branch` |
| Pattern | Group 2, instruction files that contradict each other; also Group 1d, text that outlived its convention |
| Why obsolete | `CLAUDE.md:19-20` and `.claude/skills/using-topic-branches/SKILL.md:21-37` say lead-only work lands on `main` directly and topic branches merge at the gate and are deleted at once. Step 6 assumes a standing branch merged at milestones. `git blame`: Step 6 is from `88c350a4` (2026-03-12); the branching rule is from `e9eb51c0` (2026-06-28). The older passage is rewritten to the newer. Test `tests/unit/test_session_end_capture.py` anchors on the `## Step 6` heading and `tests/unit/test_session_start_checks.py` names "/session-end Step 6" as where merge results are verified; the rewrite keeps both. |
| Confidence | High |
| Action | `rewrite` (hunk 1) |

**H2. The `CLAUDE.md` project tree is stale on five counts**

| Field | Content |
|---|---|
| Location | `CLAUDE.md:142-177` |
| Evidence | `agents/` lists `test-runner.md`, `code-reviewer.md`, `python-prototyper.md`; `teams/` lists three; `commands/ # session-start, session-end, pcc, pci, task`; `utils/` lists eight modules; no `decision_science/`, `scripts/`, `docs/adr/`, `docs/reviews/`, `docs/gaps.md`, `docs/tasks.md` |
| Pattern | Group 2, volatile specifics (a listing the repository contradicts) |
| Why obsolete | The directory holds 5 agents, 4 teams, 6 commands, 10 utility modules plus a `decision_science` package of 4 modules. `CLAUDE.md:204-210`, in the same file, lists all 5 agents. `git blame`: `29ee0ee4` and `88c350a4`, both 2026-03-12. The fix encodes architecture (directories and their purpose) and points at `.claude/README.md` for the roster, so the tree stops rotting with each added file. |
| Confidence | High |
| Action | `rewrite` (hunk 2) |

**H3. `CLAUDE.md` Tech Stack misplaces numpy**

| Field | Content |
|---|---|
| Location | `CLAUDE.md:137-138` |
| Evidence | `- **Base Dependencies**: pyyaml, python-dotenv` / `- **Optional**: pandas, openpyxl, xlsxwriter, slack-sdk, psycopg, numpy` |
| Pattern | Group 2, volatile specifics |
| Why obsolete | `pyproject.toml:12-16` lists `numpy>=1.24` as a base dependency, and the optional groups are `dev`, `excel`, `slack`, `database`, `weights`, `decision-science`, `all`. `git blame`: `88c350a4` (2026-03-12). |
| Confidence | High |
| Action | `rewrite` (hunk 3) |

**H4. The Workflow Commands table omits `/sitrep`**

| Field | Content |
|---|---|
| Location | `CLAUDE.md:181-187` (and the tree comment at `CLAUDE.md:172`, covered by hunk 2) |
| Evidence | Five rows: `/session-start`, `/session-end`, `/task`, `/pcc`, `/pci` |
| Pattern | Group 2, volatile specifics |
| Why obsolete | `.claude/commands/sitrep.md` has existed since `64d740a3` (2026-03-23); the table and the tree comment both enumerate five. `git blame` on the table: `88c350a4` (2026-03-12). |
| Confidence | High |
| Action | `add` (hunk 4) |

**H5. `python-prototyper` carries a stale module list**

| Field | Content |
|---|---|
| Location | `.claude/agents/python-prototyper.md:13-18` |
| Evidence | `- \`utils/\` — Reusable utility modules (logger, excel, parallel, geo, weights, slack, database, math_utils)` |
| Pattern | Group 2, volatile specifics |
| Why obsolete | `src/myproject/utils/` also holds `gaps.py` and `machine.py`, and `src/myproject/decision_science/` (scorer, value functions, sensitivity, visualization) is the package most feature work touches; neither is named. `scripts/` is in the agent's write scope at line 53 but not in its layout. `git blame`: `88c350a4` (2026-03-12). Audited against Claude Sonnet 5.5, which follows a given layout literally. |
| Confidence | High |
| Action | `rewrite` (hunk 5) |

**H6. The ADR skill's next-number command returns the template file**

| Field | Content |
|---|---|
| Location | `.claude/skills/recording-architecture-decisions/SKILL.md:60` |
| Evidence | `` `ls docs/adr/ | tail -1` shows the most recent. Increment. `` |
| Pattern | Group 2, volatile specifics (a command the repository contradicts) |
| Why obsolete | `docs/adr/` holds `0001-...`, `0002-...`, and `ADR-FORMAT.md`; the template sorts last, so the command prints `ADR-FORMAT.md`. Read-only re-run this turn: `ls docs/adr/ \| tail -1` printed `ADR-FORMAT.md`. `git blame`: `cf946b5b` (2026-05-19). |
| Confidence | High |
| Action | `rewrite` (hunk 6) |

**H7. The glossary skill's "real example" no longer matches `LANGUAGE.md`**

| Field | Content |
|---|---|
| Location | `.claude/skills/maintaining-ubiquitous-language/SKILL.md:42-47` |
| Evidence | `Real examples from this project's LANGUAGE.md:` then `**Wave**: A tactical parallel-execution unit inside a CONOP or OPORD where agent teams deploy. _Avoid:_ sprint, batch.` |
| Pattern | Group 2, volatile specifics |
| Why obsolete | `LANGUAGE.md:67` reads `**Wave**: A tactical parallel-execution unit inside a CONOP or OPORD where agent teams deploy. Bounded by a shared exit criterion. _Avoid:_ sprint, batch.` The `Criterion` and `Skill` examples match their entries. `git blame`: `cf946b5b` (2026-05-19). See L4 for the tension the current entry has with the skill's one-sentence rule. |
| Confidence | High |
| Action | `rewrite` (hunk 7) |

**H8. Three Level 0 skill histories carry project names the framework forbids**

| Field | Content |
|---|---|
| Location | `.claude/skills/shift-left-testing/SKILL.md:111-119`; `.claude/skills/lake-conventions/SKILL.md:170-189`; `.claude/skills/using-topic-branches/SKILL.md:96-100` |
| Evidence | `**Prior**: 2.1.1 fixes the CI sidecar's workflow example ... (2026-09-18, found in \`<repo>\`).` / `- **1.0.0** (2026-08-29): Initial, in the hub. Harvested from \`<repo>\`'s local \`lake-conventions\` 1.0.0 (2026-07-27) ...` / `- Distilled from <project>'s CONOP-002 §4.2 retrospective (2026-05-24), where six permanent \`dev-*\` branches were retired ...` |
| Pattern | Group 2, history narratives; Group 2, instruction files that contradict each other |
| Why obsolete | `.claude/skills/SKILLS_FRAMEWORK.md:103` says Level 0 skills "contain no project names, no domain-specific content", and its Content Guidelines say not to include project-specific references in Level 0 skills. These passages are past-tense change logs that load with the skill body on every trigger and prescribe nothing; the rule's authority is the behavior it states, which the bodies already state. The frontmatter `version:` field carries the number. `git log` on each skill directory and `CHANGELOG.md` hold the narrative. `git blame`: `6039e144` (2026-09-30), `61a81628` (2026-08-29), `e9eb51c0` (2026-06-28). Nothing in `tests/`, `scripts/`, or `.claude/hooks/` parses these sections. |
| Confidence | High |
| Action | `move` to `CHANGELOG.md` and git history (hunks 8a, 8b, 8c; the changelog note is hunk 16) |

### Medium

**M1. One capitalised booster in `CLAUDE.md`**

| Field | Content |
|---|---|
| Location | `CLAUDE.md:202` |
| Evidence | `**IMPORTANT**: Before deploying any agent team, read \`.claude/README.md\` for the current roster and usage guide.` |
| Pattern | Group 1a, pressure language |
| Why obsolete | Claude Fable 5.1 follows a plainly stated instruction; the marker carries no reason and is the file's only capitalised emphasis, so it reads as the one thing the author was anxious about. The instruction has a live purpose (the table below it is a summary of the README), so it is restated with that reason. `git blame`: `29ee0ee4` (2026-03-12). |
| Confidence | Medium |
| Action | `rewrite` (hunk 9) |

**M2. `proposer` steers thinking depth with prose**

| Field | Content |
|---|---|
| Location | `.claude/agents/proposer.md:52-54` |
| Evidence | `## Thinking Guidelines` / `- **Explore before converging** — spend time understanding the problem before proposing solutions` |
| Pattern | Group 1b, prose that steers thinking depth |
| Why obsolete | Audited against Claude Sonnet 5.5. Depth is controlled by configuration, not prose; Claude Code documents an `effort` frontmatter field for subagent definitions, which is the control if the proposer needs more depth than the session default. The bullet also duplicates Workflow step 2 at line 18 ("Explore the relevant codebase"). The other four bullets state the quality bar and stay. `git blame`: `10fdbdbd` (2026-03-24). The diff removes the bullet and renames the heading; it does not add `effort:`, since that changes cost and is the user's call. |
| Confidence | Medium |
| Action | `rewrite` (hunk 10) |

**M3. `/sitrep` caps output by screen and tells the model to cut**

| Field | Content |
|---|---|
| Location | `.claude/commands/sitrep.md:82` |
| Evidence | `- **Keep it to one screen** — if it scrolls too much, cut the least important items` |
| Pattern | Group 1f, output-shaping choreography (a ceiling plus a cut-the-detail instruction) |
| Why obsolete | Written for a model that padded; Claude Fable 5.1 does not, and a ceiling now trims content the reader wanted. The goal is re-expressed as the audience and outcome. `git blame`: `64d740a3` (2026-03-23). |
| Confidence | Medium |
| Action | `rewrite` (hunk 11) |

**M4. The topic-branch skill is written as a diff against a convention the model never saw**

| Field | Content |
|---|---|
| Location | `.claude/skills/using-topic-branches/SKILL.md:13-18` and `:89` |
| Evidence | `This replaces the older "one permanent branch per domain" convention.` / `- **Permanent domain branches** (\`dev-<domain>\`) — the convention this skill replaces.` |
| Pattern | Group 1d, migration-relative phrasing |
| Why obsolete | Relative phrasing implies a phantom alternative; the rule reads cleanly as the only rule. The reason (resync ceremony, no review benefit) is kept, and the anti-pattern bullet stays because downstream repos still hold `dev-*` branches. `git blame`: `e9eb51c0` (2026-06-28). |
| Confidence | Medium |
| Action | `rewrite` (hunks 12a, 12b) |

**M5. `/session-start` discourages reading its own reference table**

| Field | Content |
|---|---|
| Location | `.claude/commands/session-start.md:132` |
| Evidence | `## Quick Reference (Don't Read Unless Needed)` |
| Pattern | Group 1d, tool-use and reading discouragement |
| Why obsolete | Current models follow such a line literally, and the next sentence already gives the positive rule ("reference them when relevant"). `git blame`: `88c350a4` (2026-03-12). |
| Confidence | Medium |
| Action | `rewrite` (hunk 13) |

**M6. Incident archaeology inside `/pcc` and `/session-end`**

| Field | Content |
|---|---|
| Location | `.claude/commands/pcc.md:59-64`, `:76-77`, `:107-109`; `.claude/commands/session-end.md:12` |
| Evidence | `# Catches drift like the March-2026 case` / `(found by the <repo> canary 2026-08-17, where it produced 3 false positives against real files)` / `(found in the field, 2026-08-21 \`<repo>\` and 2026-08-22 \`<repo>\`; see the amendments to the 2026-08-21 doctrine entry)` / `In \`<repo>\` this hid 4 of 5 broken references` / `Two incidents on 2026-10-01, the second found 2026-10-02:` / `(an earlier copy of the list drifted from \`pcc.md\` and was caught 2026-08-14)` |
| Pattern | Group 2, history narratives |
| Why obsolete | Each rule's reason is load-bearing and stays (the extension bound, the three blind spots, why hits are withheld, why the list is not copied). The dates, incident counts, and sibling-repo names are archaeology that the session docs and `docs/doctrine-updates.md` already record. `tests/unit/test_pcc_reference_integrity.py` and `tests/unit/test_pcc_private_terms.py` extract the bash blocks by their `###` headings and run them; the rewrites touch comment lines only. `git blame`: `73f0b7c3` (2026-08-14), `dd5b0235` (2026-08-24), `8cef47de` (2026-08-28), `f01a8ce8` (2026-10-02), `475c88a7` (2026-08-14). |
| Confidence | Medium |
| Action | `rewrite` (hunks 14a, 14b, 14c, 14d) |

**M7. Version histories and footers in the other eight skills**

| Field | Content |
|---|---|
| Location | `configuration-management/SKILL.md:84-88`; `python-venv-management/SKILL.md:105-110`; `maintaining-project-context/SKILL.md:105-108`; `maintaining-the-common-operating-picture/SKILL.md:175-186`; `traversing-the-knowledge-base/SKILL.md:78-82`; `designing-clear-data-displays/SKILL.md:91-94`; `writing-simple-and-direct/SKILL.md:76-79`; `verifying-claims/SKILL.md:102-105` |
| Evidence | `**Maintained by**: Configuration Management Skill` / `**Previous version**: 1.0.0 single-file at \`.claude/skills/configuration-management.md\`, replaced by this directory.` / `- **0.1.1** (2026-10-04): \`ADOPTION.md\`'s first slice moves an existing known-issues list into the register in the same slice ...` |
| Pattern | Group 2, history narratives |
| Why obsolete | Same reasoning as H8 without the project-name contradiction: past-tense change logs that prescribe nothing, loaded on every trigger. The "Maintained by" lines name the skill as its own maintainer and carry no information. `SKILLS_FRAMEWORK.md`'s structure template has no such section; its Skill Maintenance section asks for semver in frontmatter. `traversing-the-knowledge-base` has no `version:` in frontmatter, so its hunk adds `version: "1.0.2"` before removing the history. `git blame`: `54c0022b` (2026-05-19) for the three footers, `0ebd059e`, `fcc094e6` (2026-10-04), `475c88a7` (2026-08-14), `8797561f` (2026-08-27), `9978231b` (2026-07-20), `ef5b4883` (2026-10-01). |
| Confidence | Medium |
| Action | `move` to `CHANGELOG.md` and git history (hunks 15a through 15h; the changelog note is hunk 16) |

### Low (flag only; no edit proposed)

**L1. `proposer` Background duplicates the role's reason with a paper citation.** `.claude/agents/proposer.md:66-68` restates line 13 ("that safety net is why you can afford to be bold") with a 10x-to-11,000x claim from an arXiv paper. Group 1c near-duplicate; keep-list item 8 (working redundancy that agrees). The user may want to drop it; this audit does not.

**L2. `lake-conventions` makes a dated claim about an external repository.** `.claude/skills/lake-conventions/SKILL.md:166-168` says the lakehouse repo's top-level docs may name an older host than its `docker/` tree. Group 2 volatile specifics, outside the project, not probed; no verification date on the claim. Flag for the lake maintainers.

**L3. `traversing-the-knowledge-base` carries a dated snapshot table.** `.claude/skills/traversing-the-knowledge-base/SKILL.md:12-19` gives counts as of 2026-08-14 (17 of 18 session docs; there are now 30). The text labels them a snapshot, states the ratio is the load-bearing fact, and carries its date, which is the form Picture Style rule 2 asks for. Group 2 time-sensitive content; no edit.

**L4. `LANGUAGE.md`'s Wave entry has two sentences against the skill's one-sentence rule.** `.claude/skills/maintaining-ubiquitous-language/SKILL.md:29` says "One sentence max"; `LANGUAGE.md:67` has two. `LANGUAGE.md` is outside this audit's scope; the user decides which side moves.

**L5. `python-prototyper` asks a subagent to confirm with the user.** `.claude/agents/python-prototyper.md:32` says "Confirm with the user when the public interface is non-obvious." A subagent returns to the lead, not the user; the instruction cannot be followed as written. No guide row covers it; flagged as an environment mismatch.

### Checked and kept

These matched a grep or a pattern name and stay, with the keep-list item that protects each.

- The Prose, Figure, Claim, and Picture kernels in `CLAUDE.md:28-90`: context the model cannot get elsewhere and the quality bar (item 1). Their duplicates in the four skill bodies agree word for word (item 8).
- `CLAUDE.md:94`, `:105`, `:112` venv emphasis: each carries its reason (uv venvs bundle no pip; an inherited `VIRTUAL_ENV` outranks `.venv`), and `/session-start` Step 4 enforces it (items 1 and 5).
- `CLAUDE.md:10` and `python-prototyper.md:23` shift-left prohibitions: a current, hook-audited failure, with the reason in the sentence before (item 5).
- `session-start.md:56` "Do NOT delete the file — the user decides when to act on it": the reason is in the line (Group 1e).
- `python-prototyper.md:33-37` RED-then-GREEN steps: order is the point (item 3).
- `/pcc` checks 5 through 7 as exact scripts, tested by `tests/unit/test_pcc_*.py` (item 3).
- `test-runner.md:40-41` "Keep your report concise. Only include failing test details": qualitative, format-sensitive, and the form the guide prefers over a numeric cap (item 7). Nothing in the file needs re-baselining for Claude Haiku 5.5.
- `decision-scientist.md` domain rules (weights sum to 1.0, no negative weights): business constraints with reasons (Group 1e).
- Team files' "do not reduce it further" and "should never be removed": reasons adjacent (Group 1e).
- Agent `model:` values `haiku`, `sonnet`, `inherit` are Claude Code aliases, not pinned IDs; they track each line's current model.
- The three near-verbatim Scope paragraphs in `code-reviewer`, `decision-scientist`, and `proposer` agree (item 8).
- `code-reviewer` and `decision-scientist` share tools and a report path but differ in checklist and domain; the decision-science team runs them as independent passes by design. Not a redundant pair (Group 4 roster check).
- `.claude/README.md:11` is the "design principle 5" that `writing-simple-and-direct:57` and `designing-clear-data-displays:66` cite; it exists.
- Paths named across the 29 files: every in-repo path resolves except three the files describe as replaced (`.claude/skills/<name>.md` single-file forms), two runtime notification files the `/pcc` allowlist names, and `.github/` in `python-prototyper`'s never-modify list, which is a placeholder for downstream repos with CI. None is a contradiction.

## Proposed diff (Step 6)

Apply nothing from this report without reading the hunk. Hunks are independent; take them selectively. Line numbers are as of commit `d51338e`.

### Hunk 1 (H1): `/session-end` Step 6

```diff
--- a/.claude/commands/session-end.md
+++ b/.claude/commands/session-end.md
@@ -76,6 +76,7 @@
-## Step 6: Evaluate Merge Readiness
-- Is this a major functional milestone?
-- If yes, consider merging to main
-- If no, continue on current branch
+## Step 6: Land the Branch
+- On `main` (lead-only doc, ADR, or small-refactor work): nothing to merge; the push in Step 3 landed it.
+- On a `topic/<scope>-<slug>` branch whose audit gate has passed: merge via merge-commit, push `main`, and delete the branch local and origin in the same step. If the gate has not run, leave the branch and name the gate in the session doc's Next Steps.
+- The rules and the commands live in `.claude/skills/using-topic-branches/SKILL.md`.
 
 Please walk me through each step, showing me the current state before asking what I want to do.
```

### Hunk 2 (H2): `CLAUDE.md` project tree

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -140,38 +140,33 @@
 ## Project Structure
 
 ```
 tacsop/
 ├── src/myproject/
-│   ├── __init__.py
-│   └── utils/                    # Reusable utility modules
-│       ├── logger.py             # OOP logging with colors and timezones
-│       ├── excel.py              # DataFrame-to-Excel tables
-│       ├── parallel.py           # Multiprocessing patterns
-│       ├── geo.py                # Haversine distance and bearing
-│       ├── weights.py            # SMARTER/reciprocal/rank-sum weights
-│       ├── slack.py              # Slack webhook posting
-│       ├── database.py           # Async PostgreSQL with JSONB
-│       └── math_utils.py         # Combinatorics (nCr, nCk)
+│   ├── utils/                    # Reusable utility modules, one file per concern
+│   └── decision_science/         # MAUT scorer, value functions, sensitivity, visualization
 ├── config/
-│   └── project.yaml              # Project identity and phases
-├── tests/                        # pytest suites
+│   └── project.yaml              # Project identity, pillars, machines, phases
+├── scripts/                      # Doctrine propagation and adoption, lake preflight
+├── tests/                        # pytest suites: unit/, integration/, fixtures/, isolation.py
 ├── docs/
+│   ├── adr/                      # Architecture decision records
 │   ├── design/                   # Pillars and roadmap
+│   ├── plans/                    # CONOPs, OPORDs, proposals
+│   ├── reviews/                  # Agent review reports
 │   ├── sessions/                 # Session documentation
-│   └── plans/                    # Implementation plans
+│   ├── gaps.md                   # Gap register
+│   └── tasks.md                  # Task list, Focus section at its head
 ├── .claude/
-│   ├── README.md               # Agent roster, teams, scope matrix
-│   ├── agents/                  # Individual agent definitions
-│   │   ├── test-runner.md
-│   │   ├── code-reviewer.md
-│   │   └── python-prototyper.md
-│   ├── teams/                   # Team composition templates
-│   │   ├── feature-development.md
-│   │   ├── bug-fix.md
-│   │   └── code-review.md
-│   ├── commands/                # session-start, session-end, pcc, pci, task
-│   └── skills/                  # Level 0 skills (config, testing, venv, etc.)
+│   ├── README.md                 # Agent roster, teams, scope matrix: the authoritative list
+│   ├── agents/                   # One file per agent
+│   ├── teams/                    # Team composition templates
+│   ├── commands/                 # Slash commands (Workflow Commands below)
+│   ├── hooks/                    # PostToolUse shift-left audit hook
+│   └── skills/                   # Level 0 skills in directory form; SKILLS_FRAMEWORK.md indexes them
+├── CONTEXT.md                    # One-page project narrative
+├── LANGUAGE.md                   # Glossary and the banned-word list
 ├── pyproject.toml
 ├── .env.example
 └── CLAUDE.md
 ```
```

### Hunk 3 (H3): `CLAUDE.md` Tech Stack

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -136,3 +136,3 @@
 - **Language**: Python (3.11+)
-- **Base Dependencies**: pyyaml, python-dotenv
-- **Optional**: pandas, openpyxl, xlsxwriter, slack-sdk, psycopg, numpy
+- **Base Dependencies**: pyyaml, python-dotenv, numpy (and tzdata on Windows)
+- **Optional groups** (`pyproject.toml`): dev, excel, slack, database, weights, decision-science, all
```

### Hunk 4 (H4): `CLAUDE.md` Workflow Commands

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -185,2 +185,3 @@
 | `/task` | Manage task list, escalate work items | Track and plan work |
+| `/sitrep` | Status report for teammates and leadership | When someone outside the session needs the state of the work |
 | `/pcc` | Pre-Code Check — fast pass/fail checklist | Before every push |
```

### Hunk 5 (H5): `python-prototyper` layout

```diff
--- a/.claude/agents/python-prototyper.md
+++ b/.claude/agents/python-prototyper.md
@@ -13,6 +13,8 @@
 - `src/myproject/` — Project modules
-  - `utils/` — Reusable utility modules (logger, excel, parallel, geo, weights, slack, database, math_utils)
+  - `utils/` — Reusable utility modules, one file per concern; read the directory rather than a list here
+  - `decision_science/` — MAUT scorer, value functions, sensitivity analysis, visualization
 - `config/` — YAML configuration
-  - `project.yaml` — Project identity and structure
+  - `project.yaml` — Project identity, pillars, machines, phases
+- `scripts/` — Doctrine propagation and adoption, lake preflight
 - `tests/` — pytest test suites
 - `docs/` — Design docs, session logs, plans
```

### Hunk 6 (H6): ADR next number

```diff
--- a/.claude/skills/recording-architecture-decisions/SKILL.md
+++ b/.claude/skills/recording-architecture-decisions/SKILL.md
@@ -60,1 +60,1 @@
-2. **Find the next ADR number.** `ls docs/adr/ | tail -1` shows the most recent. Increment.
+2. **Find the next ADR number.** `ls docs/adr/ | grep -E '^[0-9]{4}-' | tail -1` shows the most recent; the filter is needed because `ADR-FORMAT.md` sorts after the numbered files. Increment.
```

### Hunk 7 (H7): glossary example

```diff
--- a/.claude/skills/maintaining-ubiquitous-language/SKILL.md
+++ b/.claude/skills/maintaining-ubiquitous-language/SKILL.md
@@ -47,1 +47,1 @@
-**Wave**: A tactical parallel-execution unit inside a CONOP or OPORD where agent teams deploy. _Avoid:_ sprint, batch.
+**Wave**: A tactical parallel-execution unit inside a CONOP or OPORD where agent teams deploy. Bounded by a shared exit criterion. _Avoid:_ sprint, batch.
```

### Hunk 8a (H8): `shift-left-testing` footer

```diff
--- a/.claude/skills/shift-left-testing/SKILL.md
+++ b/.claude/skills/shift-left-testing/SKILL.md
@@ -108,12 +108,3 @@
 - [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) — Python's built-in mocking
 - [pytest-cov](https://pytest-cov.readthedocs.io/) — coverage plugin
-
----
-
-**Maintained by**: Shift-Left Testing Skill
-**Version**: 2.2.1 pins the CI sidecar's install to `--python .venv` (2026-10-01, CONOP OVERWATCH task 1b).
-**Prior**: 2.2.0 adds the ISOLATION sidecar and the `tests/isolation.py` tripwire plugin: one audit hook that stops a running test from deleting outside its sandbox or opening a network connection, and a `load_dotenv` guard (2026-09-30, CONOP OVERWATCH task 1a).
-**Prior**: 2.1.1 fixes the CI sidecar's workflow example: `uv venv --clear`, because `setup-uv@v5` has already created `.venv` and uv refuses a second bare `uv venv` (exit 2); adds the self-hosted cache inputs (2026-09-18, found in `fist`).
-**Prior**: 2.1.0 adds four sidecars: PROPERTY-BASED (Hypothesis invariants), NUMERIC (tolerances and determinism), REGRESSION (characterization and golden files), SCRIPTS (CLI testing and perimeter widening). New sidecars follow writing-simple-and-direct (2026-07-17).
-**Prior**: 2.0.0, restructured to directory form with sidecar progressive disclosure, vertical-slicing discipline added, ENFORCEMENT sidecar describes deterministic hooks (2026-05-19)
-**Replaces**: prior single-file at `.claude/skills/shift-left-testing.md` (deleted in the same commit).
```

### Hunk 8b (H8): `lake-conventions` Version History

```diff
--- a/.claude/skills/lake-conventions/SKILL.md
+++ b/.claude/skills/lake-conventions/SKILL.md
@@ -166,24 +166,3 @@
 Its documentation lags its deployment. Endpoints named in its top-level docs
 may describe an older host than the one its `docker/` tree now ships. Trust the
 deployment tree over the prose when they disagree.
-
-## Version History
-
-- **1.1.0** (2026-08-30): Home-storage coverage as a new sidecar,
-  `HOME-STORAGE.md`, for personal projects on personal-scoped machines.
-  Harvested from a gitignored local storage doc and generalized: every
-  hostname, share name, pool name, and drive path removed. Keeps the
-  three-address-forms rule, roots-from-environment with a required-variable
-  loud-failure pattern (no address defaults, role-named `HOME_<ROLE>_ROOT`
-  variables), the embedded-database-over-SMB hazard, mirror-is-not-backup,
-  address-by-name, least-privilege credentials, and bulk-data-to-device.
-  `config/project.yaml` gains an optional `project.scope` field (absent
-  means work); the routing paragraph above reads it alongside the machine
-  roster's scope.
-- **1.0.0** (2026-08-29): Initial, in the hub. Harvested from `launch-control`'s
-  local `lake-conventions` 1.0.0 (2026-07-27), which covered format-by-bucket
-  and the `_tmp/` scratch namespace for one repo. Generalized: repo-specific
-  writers, package paths, and maintainer identity removed; bucket tiers, both
-  path grammars, the companion-file contract, client settings, and the dev/prod
-  section added, the last drawn from what launch-control learned by writing to
-  production for five days.
```

### Hunk 8c (H8): `using-topic-branches` Sources

```diff
--- a/.claude/skills/using-topic-branches/SKILL.md
+++ b/.claude/skills/using-topic-branches/SKILL.md
@@ -93,8 +93,2 @@
 - **Leaving merged topic branches standing** — that is how a clean repo accrues debt.
 - **Branching for lead-only doc/ADR work** — overhead with no gate to justify it.
-
-## Sources
-
-- Distilled from MEGAN's CONOP-002 §4.2 retrospective (2026-05-24), where six permanent
-  `dev-*` branches were retired in favor of this policy after they were found to force
-  resync ceremony for no review benefit.
```

### Hunk 9 (M1): `CLAUDE.md` agents booster

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -202,1 +202,1 @@
-**IMPORTANT**: Before deploying any agent team, read `.claude/README.md` for the current roster and usage guide.
+Before deploying an agent team, read `.claude/README.md`: it holds the roster, the scope matrix, and the team templates, and the table below is a summary of it.
```

### Hunk 10 (M2): `proposer` guidelines

```diff
--- a/.claude/agents/proposer.md
+++ b/.claude/agents/proposer.md
@@ -52,5 +52,4 @@
-## Thinking Guidelines
+## Proposal Guidelines
 
-- **Explore before converging** — spend time understanding the problem before proposing solutions
 - **Challenge assumptions** — "we've always done it this way" is not a reason
 - **Name the trade-offs** — every approach has costs; make them visible
```

### Hunk 11 (M3): `/sitrep` length rule

```diff
--- a/.claude/commands/sitrep.md
+++ b/.claude/commands/sitrep.md
@@ -82,1 +82,1 @@
-- **Keep it to one screen** — if it scrolls too much, cut the least important items
+- **Written for a reader who skims** — a teammate gets the state of the work from the first line of each section; detail only the author needs stays in the session doc
```

### Hunk 12a (M4): `using-topic-branches` opening

```diff
--- a/.claude/skills/using-topic-branches/SKILL.md
+++ b/.claude/skills/using-topic-branches/SKILL.md
@@ -13,5 +13,4 @@
-This replaces the older "one permanent branch per domain" convention. Permanent domain
-branches (`dev-safety`, `dev-ui`, `dev-perception`, …) force constant resyncing against
-`main` for **no review benefit**: the audit gate happens at merge time regardless of how
-long the branch has existed. Short-lived topic branches keep the isolation and drop the
-permanence.
+Permanent domain branches (`dev-safety`, `dev-ui`, `dev-perception`, …) force constant
+resyncing against `main` for no review benefit: the audit gate happens at merge time
+regardless of how long the branch has existed. Short-lived topic branches keep the
+isolation and drop the permanence.
```

### Hunk 12b (M4): `using-topic-branches` anti-pattern bullet

```diff
--- a/.claude/skills/using-topic-branches/SKILL.md
+++ b/.claude/skills/using-topic-branches/SKILL.md
@@ -89,1 +89,1 @@
-- **Permanent domain branches** (`dev-<domain>`) — the convention this skill replaces.
+- **Permanent domain branches** (`dev-<domain>`) — resync ceremony with no review gate to justify it.
```

### Hunk 13 (M5): `/session-start` reference heading

```diff
--- a/.claude/commands/session-start.md
+++ b/.claude/commands/session-start.md
@@ -132,1 +132,1 @@
-## Quick Reference (Don't Read Unless Needed)
+## Quick Reference
```

### Hunk 14a (M6): `/pcc` check 5 comment

```diff
--- a/.claude/commands/pcc.md
+++ b/.claude/commands/pcc.md
@@ -58,9 +58,8 @@
-# Path-shaped references in orientation surfaces must resolve.
-# Catches drift like the March-2026 case: tasks.md carrying paths to files
-# that do not exist. Allowlist covers runtime artifacts that are
-# legitimately absent (the two upstream notification files, gitignored audit logs).
+# Path-shaped references in orientation surfaces must resolve; a task list
+# carrying paths to files that do not exist is the drift this catches.
+# Allowlist covers runtime artifacts that are legitimately absent (the two
+# upstream notification files, gitignored audit logs).
 # Extension bound is {2,8}, not {2,4}: a 4-cap truncates .geojson/.service/.shtml
-# and then reports the truncated path as MISSING (found by the launch-control
-# canary 2026-08-17, where it produced 3 false positives against real files).
+# and then reports the truncated path as MISSING against a file that exists.
 # The task list is scanned from its first line, so the ## Focus section above
 # ## Active is covered; ## Completed and below are records and are not.
```

### Hunk 14b (M6): `/pcc` check 5 blind spots

```diff
--- a/.claude/commands/pcc.md
+++ b/.claude/commands/pcc.md
@@ -76,2 +76,2 @@
-**Three known blind spots. A clean run means clean only within them** (found in the field, 2026-08-21 `contract-knowledge-graph` and 2026-08-22 `aar_ai_pipeline`; see the amendments to the 2026-08-21 doctrine entry):
-1. **Directory references are invisible.** The regex requires a file extension, so `.claude/agents/` never matches. In `aar_ai_pipeline` this hid 4 of 5 broken references sitting in the same table as the one that was caught. Run the directory pass below alongside the file pass.
+**Three known blind spots. A clean run means clean only within them:**
+1. **Directory references are invisible.** The regex requires a file extension, so `.claude/agents/` never matches, and a table of broken directory references passes while the one file reference beside them is caught. Run the directory pass below alongside the file pass.
```

### Hunk 14c (M6): `/pcc` check 7 comment

```diff
--- a/.claude/commands/pcc.md
+++ b/.claude/commands/pcc.md
@@ -103,10 +103,9 @@
 # Private terms (hostnames, usernames, codenames, sibling repo names) stay out
 # of a public tree. The list lives outside every repo, so this check cannot
 # republish it, and the output carries each hit as a path, withholding any
 # path, file name, or commit message that is itself a hit and reporting those
-# as counts. Two incidents on 2026-10-01, the second found 2026-10-02: agents
-# wrote another repo's names into docs/reviews/, and the record of containing
-# that pasted the five terms into an Evidence line, committed and pushed.
+# as counts: a review that names another repo, and the containment record
+# that pastes the terms into an Evidence line, both reach the remote otherwise.
 # Scans what a push would carry: the index, and every commit not on any
 # remote, their file names and messages included. A line printed is the
 # finding; the block itself exits 0.
```

### Hunk 14d (M6): `/session-end` Step 2

```diff
--- a/.claude/commands/session-end.md
+++ b/.claude/commands/session-end.md
@@ -12,1 +12,1 @@
-Run the full `/pcc` checklist before committing. The authoritative check list lives in `.claude/commands/pcc.md`; do not re-enumerate it here (an earlier copy of the list drifted from `pcc.md` and was caught 2026-08-14). Two session-end extras `/pcc` does not cover:
+Run the full `/pcc` checklist before committing. The authoritative check list lives in `.claude/commands/pcc.md`; do not re-enumerate it here, because a copy drifts. Two session-end extras `/pcc` does not cover:
```

### Hunk 15a (M7): `configuration-management` footer

```diff
--- a/.claude/skills/configuration-management/SKILL.md
+++ b/.claude/skills/configuration-management/SKILL.md
@@ -82,7 +82,1 @@
 - [YAML Specification](https://yaml.org/spec/) — YAML reference (including anchors used in `TESTING-AND-PATTERNS.md`).
-
----
-
-**Maintained by**: Configuration Management Skill
-**Version**: 2.0.0 restructured to directory form with sidecar progressive disclosure (2026-05-19)
-**Previous version**: 1.0.0 single-file at `.claude/skills/configuration-management.md`, replaced by this directory.
```

### Hunk 15b (M7): `python-venv-management` footer

```diff
--- a/.claude/skills/python-venv-management/SKILL.md
+++ b/.claude/skills/python-venv-management/SKILL.md
@@ -103,8 +103,1 @@
 - Replaced by uv: pyenv (`uv python`), pipx (`uvx`), pip-tools (`uv pip compile`, `uv pip sync --python .venv`)
-
----
-
-**Maintained by**: Python Venv Management Skill
-**Version**: 3.1.0: every `uv pip` command names its target (`--python .venv`). A `VIRTUAL_ENV` inherited from another repo's shell outranks the project's `.venv`, and a bare install lands there; the alternate-env route through the `VIRTUAL_ENV` variable and activation is removed (2026-10-01, CONOP OVERWATCH task 1b).
-**Prior**: 3.0.0 rebuilt on uv as the environment engine; pyenv/pip command surfaces replaced (2026-08-03)
-**Previous versions**: 2.0.0 restructured to directory form with sidecar progressive disclosure (2026-05-19); 1.0.0 single-file at `.claude/skills/python-venv-management.md`.
```

### Hunk 15c (M7): `maintaining-project-context` Version History

```diff
--- a/.claude/skills/maintaining-project-context/SKILL.md
+++ b/.claude/skills/maintaining-project-context/SKILL.md
@@ -103,6 +103,1 @@
 - This project's [config/project.yaml](../../../config/project.yaml) — machine-readable identity.
-
-## Version History
-
-- **1.1.0** (2026-10-04): Current State names where each part of the state lives instead of holding a snapshot, and `config/project.yaml` is identity, not state. The hub's own snapshot still named the 2026-04-21 propagation as the latest after three later cycles. Slice 2 of the hub's common operating picture.
-- **1.0.0** (2026-05-19): First version.
```

### Hunk 15d (M7): `maintaining-the-common-operating-picture` Version History

```diff
--- a/.claude/skills/maintaining-the-common-operating-picture/SKILL.md
+++ b/.claude/skills/maintaining-the-common-operating-picture/SKILL.md
@@ -173,14 +173,1 @@
   measurement requirements for agents.
-
-## Version History
-
-- **0.1.2** (2026-10-04): `ADOPTION.md`'s second slice says most status lines leave the
-  orientation surfaces rather than gain marks, as the hub's slice 2 found: every one it had
-  moved to a command, the task list's Focus section, or the gap register.
-- **0.1.1** (2026-10-04): `ADOPTION.md`'s first slice moves an existing known-issues list
-  into the register in the same slice, so the list has one home. Learned from the hub's own
-  first slice the same day (`docs/gaps.md`), whose gate review also found that a filler
-  such as `None exists.` passed the two-field check until punctuation was stripped.
-- **0.1.0** (2026-10-04): Draft. Kernel, vocabulary and procedure after a three-agent
-  pre-draft review (proposer, code-reviewer, decision-scientist) of an earlier eight-rule
-  draft; the decay model from the owner's convoy example. Success criterion open.
```

### Hunk 15e (M7): `traversing-the-knowledge-base` frontmatter and Version History

```diff
--- a/.claude/skills/traversing-the-knowledge-base/SKILL.md
+++ b/.claude/skills/traversing-the-knowledge-base/SKILL.md
@@ -1,4 +1,5 @@
 ---
 name: traversing-the-knowledge-base
 description: Traverse this repo's knowledge base by its existing link graph (typed session-doc headers, markdown links, path mentions) instead of blind keyword search. Use when tracing why an artifact exists, assessing blast radius before editing a living doc, orienting on session lineage, or checking reference integrity.
+version: "1.0.2"
 ---
@@ -76,7 +77,1 @@
 No cell triggers automatically; each outcome is a recorded human decision in `docs/tasks.md`.
-
-## Version History
-
-- **1.0.2** (2026-10-04): Recipe 5 names check 5's task-list scope as everything above Completed, the Focus section included, after `/pcc` check 5 widened to cover it.
-- **1.0.1** (2026-10-01): Recipe 5 no longer mentions three allowlisted March paths; that allowlist line left `/pcc` check 5 when its task closed.
-- **1.0.0** (2026-08-14): Initial. Ships proposal Approach B (`docs/plans/20260813_kb_graph_traversal_proposal.md`) with the adversarial review's corrections: falsifiable five-session criterion, neighbors defined as both directions, integrity check wired into `/pcc`.
```

### Hunk 15f (M7): `designing-clear-data-displays` footer

```diff
--- a/.claude/skills/designing-clear-data-displays/SKILL.md
+++ b/.claude/skills/designing-clear-data-displays/SKILL.md
@@ -89,6 +89,1 @@
 - The writing-simple-and-direct skill: the prose-side twin of this skill. Findings about figures are prose and follow its kernel.
-
----
-
-**Maintained by**: Designing Clear Data Displays Skill
-**Version**: 1.1.0, the external feedback round: the pre-question, Named Failures, the window test, the density guardrail (2026-08-27). 1.0.0, first committed version: directory form with four sidecars and the review protocol (2026-08-27)
```

### Hunk 15g (M7): `writing-simple-and-direct` footer

```diff
--- a/.claude/skills/writing-simple-and-direct/SKILL.md
+++ b/.claude/skills/writing-simple-and-direct/SKILL.md
@@ -74,6 +74,1 @@
 - CLAUDE.md "Simplicity First": the code-side twin of this skill.
-
----
-
-**Maintained by**: Writing Simple and Direct Skill
-**Version**: 1.0.1, one scope sentence handing the chart-or-table question to designing-clear-data-displays (2026-08-27). 1.0.0, first committed version: directory form with four sidecars and the review protocol (2026-07-20)
```

### Hunk 15h (M7): `verifying-claims` footer

```diff
--- a/.claude/skills/verifying-claims/SKILL.md
+++ b/.claude/skills/verifying-claims/SKILL.md
@@ -100,6 +100,1 @@
 - The writing-simple-and-direct skill, rule 6: hedge with numbers or not at all. An `Evidence:` line is that rule applied to success.
-
----
-
-**Maintained by**: Verifying Claims Skill
-**Version**: 1.0.0, first committed version: directory form with one sidecar (2026-10-01)
```

### Hunk 16 (H8, M7): changelog note for the moved histories

```diff
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -10,2 +10,3 @@
 ### Changed
+- **Skill version histories leave the SKILL.md bodies.** The frontmatter `version:` field carries each skill's number (`traversing-the-knowledge-base` gains one at 1.0.2); the narrative of each bump is in this changelog's earlier entries, `docs/doctrine-updates.md`, and `git log -- .claude/skills/<name>/`. Level 0 skill bodies no longer name sibling repositories, per `SKILLS_FRAMEWORK.md`'s Level 0 rule.
 - **Propagation skips the repos `config/project.yaml` excludes.** `propagation.exclude` lists repos, by path under `~/projects`, that this hub never writes into; the first is `github/assay`, a GitHub mirror of a work repository. `scripts/propagate_doctrine.py` names each skip (`[skip] <path>: excluded by config/project.yaml propagation.exclude`) and writes neither a notification nor a mark there; discovery is unchanged. `docs/propagation-protocol.md` settles its open opt-out question as this hub-side list. The guard fails closed: a single-value or unparseable list refuses the run; a trailing `/`, `./`, a backslash or a case difference still excludes; a repo under an excluded path is skipped; an entry that matches no repo prints `[warn]` (12 tests; gate review `docs/reviews/20261004_propagation_exclude_gate.md`).
```

## After applying any hunk

- Run `.venv/bin/pytest tests/unit/test_pcc_reference_integrity.py tests/unit/test_pcc_private_terms.py tests/unit/test_session_end_capture.py tests/unit/test_session_start_checks.py tests/unit/test_state_block.py -q`. These extract sections of the edited command files by heading; the hunks keep every heading they anchor on.
- Run `/pcc` check 5. Hunk 2 keeps `src/myproject/` as the tree's only path-shaped reference, as today; the other entries are tree branches the check does not match, so its result should not change.
- Hunks 8 and 15 are a propagation event: downstream copies of the eleven skills will differ from the hub by their footers until the next doctrine cycle carries the change. Propagation Rule 3 (`docs/propagation-protocol.md:50`) says to bundle such a change with the next substantive update rather than cycle for it alone.

## Counts

| Group | High | Medium | Low (flag) | Findings | Hunks |
|---|---|---|---|---|---|
| 1 Dated prompt text | 0 | 5 | 1 | 6 | 6 |
| 2 Brittle configuration | 8 | 2 | 4 | 14 | 23 |
| 3 Tool descriptions | not applicable | | | 0 | 0 |
| 4 Request config and roster | 0 | 0 | 0 | 0 | 0 |
| **Total** | **8** | **7** | **5** | **20** | **29** |

Proposed edits: 29 hunks across 21 files (`CLAUDE.md`, `CHANGELOG.md`, 2 agent files, 4 command files, 13 skill files). Applied: none.
