# Review: Pass 6 — Day-1 Playbook (`docs/design/from_template_to_project.md`) Audit

**Author**: code-reviewer
**Date**: 2026-05-19
**Type**: Doc accuracy audit (post-doctrine-cycle)

## Summary

The doctrine cycle on 2026-05-19 added LANGUAGE.md, CONTEXT.md, the ADR system, the propagation protocol, three directory-form skills, a PostToolUse hook, two new commands/agents, and a Python 3.11 floor. The Day-1 playbook predates all of it. The doc has 23 findings: 11 hard FAILs (factually wrong), 10 CONCERNs (silent on artifacts that now exist), and 2 OK confirmations. Most damaging: the agent count (4 vs 5), the substitution list (misses the hook, LANGUAGE.md, CLAUDE.md test-first section, README.md, CHANGELOG.md, agent files, the propagate_doctrine test, and `pyproject.toml`'s `[tool.coverage.run] source` and `[tool.setuptools.packages.find]` keys), the missing mention of `docs/adr/`, `docs/propagation-protocol.md`, `docs/session-doc-format.md`, `.claude/hooks/`, and the wholesale absence of the test-first vertical-slice principle from Section 7. The "Preserve `.claude/commands/` and `.claude/skills/` intact" guidance is now actively misleading because the cycle deleted `.claude/skills/session-end.md` — the rule needs a "directory form" caveat and an exception for the session-end skill.

---

## FAIL findings (factually wrong; will mislead next clone)

### FAIL-1. Section 1, line 15: agent count is "four"

Current text:
> Claude Code workflow: session commands, four prepositioned agents, PCC/PCI quality gates

Repo currently ships **5 agents**: `code-reviewer.md`, `decision-scientist.md`, `proposer.md`, `python-prototyper.md`, `test-runner.md`.

**Fix**:
> Claude Code workflow: session commands, five prepositioned agents (proposer, code-reviewer, decision-scientist, python-prototyper, test-runner), PCC/PCI quality gates

### FAIL-2. Section 1, line 15 and Section 7, line 389: test count "189 tests across 8 test files"

`pytest --collect-only -q` reports **192 tests collected**. `find tests -name "test_*.py"` reports **9 test files** (added `test_propagate_doctrine.py` 2026-04-21). Coverage still rounds to 53% (53.33%).

**Fix**: replace both occurrences with "192 tests across 9 test files (53% coverage)".

### FAIL-3. Section 1, line 16: "four prepositioned agents" again

Same issue as FAIL-1 — second occurrence on the same line. Already covered by the FAIL-1 fix.

### FAIL-4. Section 2 Step 1, lines 43–56: substitution table is incomplete

`grep -rl myproject` (excluding venv/git/cache) returns ~30 hits. The table only lists 9 file categories. Missing files that now contain `myproject` and must be substituted:

| File | Why missed |
|---|---|
| `.claude/hooks/post-tool-shift-left-audit.sh` | New (Pass 4); has `*/src/myproject/*.py)` glob — wrong substitution = silent hook failure |
| `LANGUAGE.md` | New (line 29 references `src/myproject/utils/decision_science/`) |
| `CONTEXT.md` | New — needs verification (likely contains identity refs) |
| `CLAUDE.md` Development Principle section | Now contains 3 fresh `src/myproject/` paths (lines 8, 12, 74) from Pass 4, beyond the existing tree |
| `.claude/agents/python-prototyper.md` | Contains `src/myproject/` in Project Layout, Scope, and Shift-Left Testing sections (lines 14, 23, 35, 39, 52) |
| `.claude/agents/code-reviewer.md`, `.claude/agents/decision-scientist.md`, `.claude/agents/proposer.md`, `.claude/agents/test-runner.md` | Need to be grep-checked at minimum |
| `.claude/teams/bug-fix.md`, `.claude/teams/code-review.md` | Both hit |
| `.claude/README.md` | Hit (Scope Matrix row `src/myproject/`) |
| `src/myproject/decision_science/scorer.py`, `sensitivity.py`, `visualization.py`, `__init__.py` | Source files contain self-referential imports/strings |
| `tests/unit/test_logger.py`, `test_value_functions.py`, `test_visualization.py`, `test_scorer.py`, `test_geo.py`, `test_math_utils.py`, `test_sensitivity.py`, `tests/integration/test_decision_science_e2e.py` | All do `from myproject...` |
| `README.md`, `CHANGELOG.md` | New project-root files added since the playbook was written |
| `pyproject.toml` `[tool.coverage.run] source = ["src/myproject"]` | Separate line from `name = "myproject"`; easy to miss |
| `pyproject.toml` `all = ["myproject[...]"]` | Already listed but with wrong wording — see FAIL-5 |
| `docs/doctrine-updates.md`, `docs/reviews/*.md`, `docs/sessions/*.md`, `docs/plans/decision_science_utility.md` | Historical references — usually fine to leave, but should be called out as "skip these" |

**Fix**: replace the table with a `grep -rl` command and a curated list of high-risk substitution targets. Concrete recommended addition:

```bash
# Run this first to see every occurrence:
grep -rln myproject . \
  --exclude-dir=.venv --exclude-dir=.git --exclude-dir=.pytest_cache \
  --exclude-dir=dist --exclude-dir=build --exclude-dir='*.egg-info' \
  --exclude-dir=audits --exclude-dir=docs/sessions --exclude-dir=docs/reviews
```

Then list the substitution-required categories explicitly: **source** (`src/myproject/**`), **tests** (`tests/unit/*.py`, `tests/integration/*.py`), **config** (`pyproject.toml` × 4 locations: `[project] name`, `[project.optional-dependencies] all`, `[tool.coverage.run] source`, plus `config/project.yaml` × 2 locations), **docs visible to clone consumer** (`CLAUDE.md`, `README.md`, `CHANGELOG.md`, `LANGUAGE.md`, `CONTEXT.md`), **agent infra** (`.claude/agents/python-prototyper.md`, `.claude/README.md`, `.claude/commands/pci.md`, `.claude/teams/bug-fix.md`, `.claude/teams/code-review.md`), and **the hook** (`.claude/hooks/post-tool-shift-left-audit.sh` — call out explicitly with the `case` syntax warning from doctrine-updates §7).

### FAIL-5. Section 2 Step 1, line 48: `all` group example is now stale

Current: `"myproject[dev,excel,...]" in `all` group`. Actual `all` group lists `dev,excel,slack,database,weights,decision-science` (the `decision-science` extra was added with the decision_science subpackage). Doc should either list the extras explicitly or note that the list will grow as you add extras.

**Fix**: `"myproject[dev,excel,slack,database,weights,decision-science]" → "newname[dev,excel,slack,database,weights,decision-science]"`

### FAIL-6. Section 2 Step 4, line 115: "Preserve `.claude/commands/` and `.claude/skills/` intact"

This now misleads in three ways:
1. `.claude/skills/session-end.md` was **deleted** on 2026-05-19 — "preserve intact" implies it should still be there.
2. Three skills are now directories with sidecars (`shift-left-testing/`, `configuration-management/`, `python-venv-management/`) — `cp -r` not `cp`.
3. A new sibling directory `.claude/hooks/` exists and is also load-bearing (the audit hook). Missing from the preserve list entirely.

**Fix**:
> Preserve `.claude/commands/`, `.claude/skills/` (directory form — copy recursively), `.claude/hooks/`, and `.claude/teams/` intact. These carry workflow logic, not template scaffolding. The hook script in `.claude/hooks/post-tool-shift-left-audit.sh` requires both a path-glob substitution (see Step 1) and `chmod +x` after copy.

### FAIL-7. Section 2 Step 4, lines 108–116: deletion table is incomplete

Missing template artifacts that exist now and should be cleaned on Day 1:
- `docs/reviews/*.md` (11 review files, all template-specific Pass-N audits — should be wiped just like sessions)
- `docs/adr/0001-directory-form-mandatory-for-new-skills.md` — needs the "re-attribute decision-maker" treatment from doctrine-updates §3 step 3, not deletion
- `docs/design/hold/` is gitignored (good) but worth mentioning that it's a scratch dir
- `CHANGELOG.md` — template changelog, not yours
- `docs/doctrine-updates.md` and `docs/propagation-protocol.md` — relevant only if you're a propagation hub (per doctrine-updates §4)

**Fix**: extend the table with rows for `docs/reviews/*.md` (delete), `docs/adr/0001-*.md` (re-author, don't delete — points to your own ADR-0001), `CHANGELOG.md` (reset to empty), `docs/doctrine-updates.md` + `docs/propagation-protocol.md` (delete unless you're also a hub).

### FAIL-8. Section 2 Step 1, line 53: `.env.example` claim is mis-stated

Current: "Comments referencing `src/myproject/utils/`". Actual `.env.example` lines 5 and 8 reference `src/myproject/utils/slack.py` and `src/myproject/utils/database.py` specifically. Wording fine but the line note should make clear there are 2 hits (low-effort substitution).

**Fix (minor)**: "Two comments referencing `src/myproject/utils/slack.py` and `src/myproject/utils/database.py`".

### FAIL-9. Section 4, line 219: pillars.md format reference

The doc says "the format in `docs/design/pillars.md` is the right structure". `docs/design/pillars.md` **does exist** in this repo — but it's a *template stub* (Instructions + Template + Example Pillars sections, mostly TODO). The doc treats it as a worked example. It is a fill-in-the-blank template. (Note: the python-prototyper agent's own pillars reference was repointed to `CONTEXT.md` + `config/project.yaml` in this cycle precisely because `pillars.md` is empty/stub.) This is not strictly *wrong* — the structure described in the doc *is* what pillars.md contains — but the implication that pillars.md holds the project's actual pillars is misleading. The current pillar names live in `config/project.yaml` `design_pillars:` and `CLAUDE.md`.

**Fix**: 
> Replace them with your project's actual constraints. Use `docs/design/pillars.md` (a stub in the template) as the structural starting point, and update the pillar names in `config/project.yaml` `design_pillars:` to match.

### FAIL-10. Section 7, lines 386–436: testing section never mentions test-first / vertical-slice / the audit hook

This is the largest gap in the doc. The CLAUDE.md Development Principles section was strengthened to mandate test-first vertical-slice TDD with a deterministic PostToolUse audit hook. The Day-1 playbook's entire Testing Strategy section is silent on:
- The test-first vertical-slice mandate
- The `.claude/hooks/post-tool-shift-left-audit.sh` enforcement layer
- `.claude/audits/shift-left-violations.log`
- `.claude/skills/shift-left-testing/VERTICAL-SLICING.md` and `ENFORCEMENT.md`

This is a FAIL not a CONCERN because a clone consumer who reads only this section will adopt the old code-first-tests-second pattern that doctrine-updates §9 explicitly calls out as the workflow that undermines the rest of the propagation.

**Fix**: prepend a subsection "The discipline: test-first vertical-slice TDD" that summarizes the mandate, links to `.claude/skills/shift-left-testing/VERTICAL-SLICING.md`, and notes the audit hook fires on every Write/Edit to `src/<yourpkg>/`. Reference doctrine-updates §6, §7, §10 wording.

### FAIL-11. Section 8, lines 496–504: agent table missing `proposer` and `decision-scientist`

Current text only lists `test-runner`, `code-reviewer`, `python-prototyper` (and mentions "four prepositioned agents" upstream). Doc shows 4-row table; reality is 5 agents in 2 tiers (Level 0: 4 portable; Level 1: 1 project-specific = `decision-scientist`).

**Fix**: replace the "Agent usage" subsection's narrative claim about Level 0/Level 1 to match `.claude/README.md`'s split (proposer, code-reviewer, python-prototyper, test-runner = Level 0 portable; decision-scientist = Level 1, drop when removing decision_science). Update the parenthetical "(test-runner, code-reviewer, python-prototyper)" on line 504 to add `proposer`.

---

## CONCERN findings (silent on artifacts; should mention)

### CONCERN-1. Section 1: doctrine artifacts not mentioned in "what you get"

Day-1 reader learns nothing about LANGUAGE.md, CONTEXT.md, the ADR system, the propagation protocol, the session-doc-format spec, or the audit hook — all of which they will encounter the moment they `ls` the repo.

**Fix**: add a bullet to the "What you get on clone" list:
> - Doctrine artifacts: `LANGUAGE.md` (project glossary), `CONTEXT.md` (one-page project identity), `docs/adr/` (architecture decision records), `docs/propagation-protocol.md` (only relevant if this becomes a hub), `docs/session-doc-format.md` (session-doc spec), and a PostToolUse audit hook for shift-left TDD enforcement

### CONCERN-2. Section 2 should add a "Customize LANGUAGE.md and CONTEXT.md" step

These are CUSTOMIZE adoption mode (per doctrine-updates table rows 1, 3). The Day-1 checklist should include a step "Rewrite LANGUAGE.md and CONTEXT.md for your project" between Step 4 (strip what you don't need) and Step 5 (verify tests pass).

### CONCERN-3. Section 2 should add an "Adopt or skip ADR-0001" step

Per doctrine-updates §3 step 3: ADR-0001 either becomes your own ADR-0001 (re-author the Decision-maker field) or you delete it and start fresh. The Day-1 checklist does not surface this.

### CONCERN-4. Section 2 should add a "Decide if you're a propagation hub" step

`docs/propagation-protocol.md` is SKIP-OR-CUSTOMIZE (doctrine-updates table row 18). Most cloners are not hubs; they should delete the protocol file. The Day-1 checklist is silent.

### CONCERN-5. Section 3 ("What to Keep, Evaluate, or Remove") never mentions `decision_science/`

The `decision_science/` subpackage is the largest single module in the repo (4 files in `src/myproject/decision_science/` plus 4 test files plus a dedicated agent plus a team template). Section 3 lists `utils/` modules only. A clone consumer who doesn't need MAUT will not see guidance on removing it.

**Fix**: add a paragraph in Section 3 under "Evaluate":
> **`decision_science/`** — Keep if you're doing MCDA / weighted scoring. Drop the whole subpackage (`src/<yourpkg>/decision_science/`, the 4 test files, the `decision-science` extra in `pyproject.toml`, `.claude/agents/decision-scientist.md`, `.claude/teams/decision-science.md`, and the agent rows in `.claude/README.md`) if not. Doing so also lets you simplify `numpy` from a required dep to an optional dep.

### CONCERN-6. Section 6: nothing about `numpy` as a *required* (not optional) dep

`pyproject.toml` line 13 lists `numpy` as a base `dependencies` entry (required for decision_science). The doc treats numpy as optional in Section 6's "Adding new optional dependencies" example and in Section 3's `weights.py` callout. A reader trimming numpy will break decision_science silently.

**Fix**: add to Section 3 note for `decision_science/`: "numpy is currently a *required* dep solely because of this subpackage. If you remove `decision_science/`, move numpy to an extra (`weights`)."

### CONCERN-7. Section 8: commands table is missing `/sitrep`

`.claude/commands/` contains `sitrep.md` (narrative status report). The Workflow Commands table in Section 8 lists 5 commands; reality is 6.

**Fix**: add a row to the table:
> `/sitrep` | Narrative status report | When asked for context-rich status

### CONCERN-8. Section 8, line 500: team table missing `decision-science`

`.claude/teams/` has 4 templates: bug-fix, code-review, feature-development, decision-science. The Day-1 table lists 3.

**Fix**: add a row:
> Review + MCDA implementation | MAUT/MCDA work | `.claude/teams/decision-science.md`

### CONCERN-9. Section 8: "Level 0 / Level 1 agents" naming is correct but the agent list is wrong

Line 504 says "Level 0 agents (test-runner, code-reviewer, python-prototyper)". Per current `.claude/README.md`, Level 0 is 4 agents (adds `proposer`) and Level 1 is `decision-scientist`. SKILLS_FRAMEWORK.md still uses Level 0 / Level 1 vocabulary so the framing itself is fine — just the count is off.

**Fix**: "Level 0 agents (proposer, test-runner, code-reviewer, python-prototyper) are portable — don't modify them."

### CONCERN-10. Section 9 / Section 10 should add new pitfalls from the doctrine cycle

The Common Pitfalls list does not include the most likely Day-1 mistakes introduced by the new doctrine artifacts:
- Forgetting to substitute `myproject` in `.claude/hooks/post-tool-shift-left-audit.sh` (silent failure — hook runs, never matches, empty audit log)
- Forgetting `chmod +x` on the hook after `git clone` on systems with `core.fileMode=false`
- Not having `jq` installed (hook exits silently if missing)
- Editing `.claude/settings.json` instead of `.claude/settings.local.json` for per-developer overrides
- Adopting LANGUAGE.md / CONTEXT.md verbatim without customizing (template content masquerading as yours)
- Writing a new ADR without applying the triple-filter gate

**Fix**: add 4–6 new pitfall bullets covering the above.

---

## OK findings (verified accurate for high-risk facts)

### OK-1. Section 6, lines 313–320: config flow Mermaid diagram

YAML + .env → code, no overlap. Still accurate.

### OK-2. Section 7, lines 397–411: `pytest.importorskip` pattern

Pattern is still the convention used in `test_excel.py` (and others). The example code-block compiles against current `src/myproject/utils/excel.py`.

---

## Replacement Inventory

Numbered list of every section needing edits and the change type. Sequence reflects suggested editing order (top of file down).

| # | Section / Line | Change | Type |
|---|---|---|---|
| 1 | §1 line 15 | "four prepositioned agents" → "five (proposer, code-reviewer, decision-scientist, python-prototyper, test-runner)" | REPLACE |
| 2 | §1 line 15 | "189 tests across 8 test files" → "192 tests across 9 test files" | REPLACE |
| 3 | §1 line 15 | Add bullet listing doctrine artifacts (LANGUAGE.md, CONTEXT.md, docs/adr/, docs/propagation-protocol.md, docs/session-doc-format.md, .claude/hooks/) | ADD |
| 4 | §2 Step 1 lines 43–56 | Replace substitution table with `grep -rln` command + curated categories (source / tests / config / docs / agent-infra / hook) | REPLACE |
| 5 | §2 Step 1 line 48 | `dev,excel,...` → explicit `dev,excel,slack,database,weights,decision-science` list | REPLACE |
| 6 | §2 Step 1 line 53 | `.env.example` description → "Two comments referencing slack.py and database.py" | REPLACE |
| 7 | §2 Step 1 | Add row for `.claude/hooks/post-tool-shift-left-audit.sh` substitution with `case` syntax warning | ADD |
| 8 | §2 Step 1 | Add row for `pyproject.toml` `[tool.coverage.run] source` and `[tool.setuptools.packages.find]` (and note 4 separate hits in pyproject.toml) | ADD |
| 9 | §2 Step 1 | Add rows for `LANGUAGE.md`, `CONTEXT.md`, `README.md`, `CHANGELOG.md`, agent files, team files | ADD |
| 10 | §2 Step 4 line 108 onward | Extend deletion table: `docs/reviews/*.md`, `CHANGELOG.md`, conditional deletion of `docs/doctrine-updates.md`/`docs/propagation-protocol.md` | ADD |
| 11 | §2 Step 4 line 115 | Rewrite "Preserve `.claude/commands/` and `.claude/skills/` intact" → include `.claude/hooks/`, `.claude/teams/`, note directory-form skills need `cp -r`, note `.claude/skills/session-end.md` was already deleted | REPLACE |
| 12 | §2 | New Step between 4 and 5: "Customize LANGUAGE.md and CONTEXT.md for your project" | ADD |
| 13 | §2 | New Step: "Adopt or delete ADR-0001 (re-author Decision-maker field)" | ADD |
| 14 | §2 | New Step: "Decide whether you're a propagation hub (delete `docs/propagation-protocol.md` if not)" | ADD |
| 15 | §3 | Add paragraph under "Evaluate" for `decision_science/` subpackage with full removal checklist | ADD |
| 16 | §3 | Add note on `numpy` being a required dep solely for decision_science | ADD |
| 17 | §4 line 219 | Reword "the format in `docs/design/pillars.md`" to clarify it's a stub template, and that pillar names live in `config/project.yaml design_pillars:` and CLAUDE.md | REPLACE |
| 18 | §7 lines 386–389 | Update "189 tests across 8 test files" → "192 / 9", and prepend "The discipline: test-first vertical-slice TDD" subsection referencing VERTICAL-SLICING.md, ENFORCEMENT.md, and the hook | REPLACE + ADD |
| 19 | §8 line 500 (teams table) | Add `decision-science` team row | ADD |
| 20 | §8 (commands table at top of section) | Add `/sitrep` row | ADD |
| 21 | §8 line 504 | "Level 0 agents (test-runner, code-reviewer, python-prototyper)" → add `proposer`; note `decision-scientist` is Level 1 | REPLACE |
| 22 | §9 | Add "Previously fixed" entries for the 2026-05-19 cycle: pillars-ref stale in python-prototyper, code-first workflow in python-prototyper, session-end skill/command duplication, Python 3.10 floor | ADD |
| 23 | §10 | Add 4–6 new pitfalls: hook path-glob substitution, hook chmod +x, missing jq, settings.json vs settings.local.json, adopting LANGUAGE/CONTEXT verbatim, writing ADRs without the triple filter | ADD |

Estimated effort: 90–120 minutes for an editor with the doctrine-updates entry open in the other pane.
