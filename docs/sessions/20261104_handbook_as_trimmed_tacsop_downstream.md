# Session: Handbook as Trimmed Tacsop Downstream

**Date**: 2026-11-04 (titanx)
**Branch**: main
**Tags**: #session #doctrine #infra #docs #complete
**Documents**: [handbook_contract.md](../../.claude/handbook_contract.md), task file in assay defining the handbook; [01-knowledge-graphs](https://git-out.gss.anl.gov/ai-cop/lanes/01-knowledge-graphs), the lane this handbook harvests
**Follows**: [20261104_knowledge_graph_lane_alignment.md](20261104_knowledge_graph_lane_alignment.md)

---

## Summary

The first ai-cop lane (01-knowledge-graphs) shipped the prior session from lane 01 work alone; the handbook is where the repeatable machinery lives. This session built `ai-cop/handbook` as a trimmed tacsop downstream: stripped to what a documents-and-tooling repo needs, with one participant page, three owner guides, a lane template, three scripts, and four ADRs. The contract's ten tasks all landed in one lead-only pass on handbook `main`, test-first, with the lane report and scaffold as the gates. A second pass removed military jargon across the handbook. The handbook is live on `origin/main`.

| Metric | Value |
|---|---|
| Handbook commits | `79f01d1` (charter) + `0183e58` (jargon pass) on `ai-cop/handbook` `origin/main` |
| Files in charter commit | 120 changed (119 new, 1 rewritten README) |
| Charter net | −80 lines across 23 files in jargon pass |
| Skills kept | 9 of 14 (dropped 5: data-displays, lake, cop, config-mgmt, traversal) |
| Agents kept | 3 of 5 (dropped decision-scientist, python-prototyper; kept proposer) |
| Tests at close | 81 passed in handbook (`pytest -q`), 528 passed in tacsop |
| Lane template files | 17 (README, AGENTS, CLAUDE, LESSONS, pyproject, .python-version, .gitignore, debrief template, 2 scripts, 4 docs, 3 directories) |

---

## Work Completed

### 1. Clone and strip (Task 1)

Handbook checkout at `~/projects/gitlab/ai-cop/handbook` already existed with origin `https://git-out.gss.anl.gov/ai-cop/handbook.git` and one initial commit. Stripped in place: rsync from tacsop excluding `.git`, `.venv`, caches, and `.claude/audits`, then dropped `src/myproject/`, two agents, one team, five skills, five docs trees, `config/project.yaml`, three scripts, and two test groups. No `LICENSE` per the user's hold. Remaining files rewritten:

- `CLAUDE.md` — project structure, lane voice section, handbook quick commands (`new_lane`, `lane_report`, `harvest`), tacsop-to-handbook glossary crosswalk removed
- `.claude/README.md` — roster trimmed to three agents, scope matrix rewritten for `src/handbook/` + `lane-template/`
- `.claude/hooks/post-tool-shift-left-audit.sh` — retargeted `src/myproject` to `src/handbook`
- `.claude/skills/SKILLS_FRAMEWORK.md` — five dropped skill sections and inventory entries removed
- `.claude/commands/session-start.md`, `session-end.md`, `pcc.md`, `pci.md` — `config/project.yaml` to `handbook.yaml`, gaps/machine refs removed, team refs retargeted
- `.claude/skills/shift-left-testing/ENFORCEMENT.md`, `SCRIPTS.md`, `writing-simple-and-direct/SKILL.md` — stale cross-skill refs corrected
- `.claude/teams/bug-fix.md`, `code-review.md`, `feature-development.md` — `src/myproject` to `src/handbook`
- `pyproject.toml` — name `handbook`, package `src/handbook`, deps `requests` not `numpy`, no importable `src.*` packages, coverage source `src/handbook`
- `.env.example` — trimmed to `GITLAB_TOKEN` only
- `CONTEXT.md`, `LANGUAGE.md` — handbook terms (lane, debrief, AAR, cycle owner, distro owner, harvest), civilian-only glossary
- `docs/tasks.md` — reset to one completed charter line, one active Focus item
- `docs/session-doc-format.md` — traversal `KB-graph:` line removed (no traversing skill in handbook)

### 2. Participant page (Task 2)

Wrote `README.md`: one page, what the AI CoP is, what a lane is (clone, run, debrief, AAR), how to file a debrief, where to ask for help, cycle shapes (planning: 6 sessions background/project/future/hands-on/hands-on/AAR; short: 3 sessions background/project/future), current lane 01 link, per the user's decision to keep the calendar generic and owner references as "see handbook".

### 3. Config (Task 3)

Wrote `config/handbook.yaml`: GitLab host `https://git-out.gss.anl.gov`, group `ai-cop`, lanes subgroup `ai-cop/lanes`, 10 labels (4 `type::` + 6 `week::`), five seats (cycle lead, distro owner, week lead, builder, AAR facilitator), default session count, read by all three scripts. Design pillars preserved.

### 4. Lane guide (Task 4)

Wrote `docs/LANE-GUIDE.md`: two sections, recommending voice. Section 1 (the only musts, four items): LESSONS.md parses to four fields, debrief template with labels by name, no secrets committed, README with a clone line for a named folder. Section 2 (ten recommendations, each one sentence of why): AGENTS.md + CLAUDE.md pointer, no `.claude/` in lanes, terminal-and-browser completable, at most three lane terms in participant text, no em dashes, explicit folder in clone line, `check_env.py`, `debrief.py`, `[build-system]`, shareable sample data with provenance noted, fresh-venv check.

### 5. Owner guides (Task 5)

Four files under `docs/owners/`:

- `new-lane.md` — scaffold (`new_lane.py`), create project, milestones `Week N` with due dates, fill seats, fresh-clone verification checklist
- `running-a-cycle.md` — weekly rhythm table, fresh-clone verification (non-author), triage of `type::debrief` into `type::defect`/`lesson`/`task`, closing a week
- `aar.md` — facilitator prompts moved from lane 01's LESSONS.md, entry format (`## YYYY-MM-DD (AAR, lane NN)` with Lesson/Evidence/Applies to/Harness), rollup MR via `harvest.py`
- `glossary.md` — owner-side terms (cycle lead, distro owner, week lead, builder, AAR facilitator, harvest, lane report, planning/short cycle, group labels, milestone, rollup MR)

Each links to LANE-GUIDE rather than repeating it.

### 6. Lane template (Task 6)

Built `lane-template/` derived from lane 01 with five placeholders (`{{lane_number}}`, `{{lane_slug}}`, `{{lane_title}}`, `{{start_date}}`, `{{distro_owner}}`): README.md, AGENTS.md, CLAUDE.md, LESSONS.md (format block only, no live heading; handbook fix: inside fence so harvest skips it), pyproject.toml with `[build-system]` + `packages = []`, `.python-version` 3.12, `.gitignore` (covers `.claude/` and `.cursor/` whole), debrief template, `check_env.py` (minimal generic, REQUIRED empty, no endpoint check; owner fills per lane), `debrief.py` (reads single-source template, derives `Debrief week N: GREEN/RED`, adds `week::N` label, `--week` from `--week` flag; carries the `importlib.util.spec_from_file_location` + `sys.modules` fix from lane 01; GitLab URL templated from `{{lane_number}}-{{lane_slug}}`), `docs/CYCLE-PLAN.md`, `docs/glossary.md`, `docs/env-setup.md`, `notebooks/README.md`, `skills/README.md`, `data/README.md`, `docs/sessions/.gitkeep`.

Nothing from `.claude/` is in the template. Verified `ls lane-template/.claude` reports no such file.

### 7. Scripts in `src/handbook/` (Task 7)

Three scripts, test-first (fail before impl, fix, green):

**`lessons.py`** (shared by the other two): `LessonEntry` dataclass with `source`, `parse_lessons(text)` stripping fenced blocks, `HEADING_RE` with `re.MULTILINE`, `Evidence` must contain `#N`, fenced example inside format block excluded. A file with the format header but no live AAR headings is now empty-ok (fresh scaffold), while bare `Lesson:` bullets without a heading still error.

**`lane_report.py`** (14 rules from one `RULES` table, one function per rule, so guide and checker cannot disagree):

- Needed: `lessons_parse`, `debrief_template_present`, `no_secrets` (sk-\* pattern including `sk-proj-` form, `.env` check, gitignored files skipped), `readme_clone_line`
- Consider: `agents_md`, `claude_md_pointer` (must be `See AGENTS.md.`), `no_claude_dir`, `term_budget` (max 3, no doctrine terms), `no_em_dashes` (skips `.claude/` + `tests/fixtures/` + provenance ADRs), `clone_folder_named` (second `\S+` not ``` fence), `check_env_present`, `debrief_script_present`, `build_system_present`, `data_provenance`, optional `fresh_venv_check_env` via `--run`
- `Report` with `exit_code` (1 unless all needed ready, or `--strict` and any consider not ready), `format()` prints two blocks

**`new_lane.py`**: copies template, substitutes five placeholders, skips existing dir with `FileExistsError`, prints dry-run tree, `--gitlab` prints a not-yet note. Every written file is a starting point.

**`harvest.py`**: `list_lane_projects` via `GET /api/v4/groups/%2F/projects`, `fetch_lessons` via `GET /projects/%2F/repository/files/LESSONS.md/raw`, `build_rollup` (broken lane gets one notice, never an error), `format_rollup` grouped by lane with source links. Round-trippable: rollup entries re-parse via `parse_lessons`.

### 8. Tests (Task 8)

81 tests, no network (recorded API responses via `unittest.mock.patch` on `requests.get`):

- `test_lessons_parse.py` (10): ok fixture 2 entries, required fields, dates/lanes, drift/missing/empty/no-heading/evidence, fence exclusion
- `test_lane_report.py` (44): one class per rule plus 7 full-report cases (needed vs consider, exit codes, strict flag, format)
- `test_new_lane.py` (15): dry-run, creates dir, README clone line, LESSONS heading, distro owner substitution, default owner, pyproject build-system, CYCLE-PLAN start date, no placeholders remain, scaffold passes report needed (fixed lessons parser to treat template as ok), no `.claude`, GitLab URL, refuses existing
- `test_harvest.py` (12): fetch+browse/404, build from two lanes/broken/empty/sort, format entries/links/notices/header/round-trip

Fixtures: `tests/fixtures/lane-ok/` (passes every check) and `lane-drift/` (fails needed checks, has `.env` secret, em dashes, `.claude/`, no AGENTS.md). Lane-ok's `data/README.md` carries NOAA provenance. Isolation plugin retained but `conftest.py` no longer loads hypothesis profiles.

### 9. ADRs (Task 9)

Kept `0001-directory-form-mandatory-for-new-skills.md` (still applies), dropped `0002-rename-repository-to-tacsop.md` (tacsop provenance). Added four handbook ADRs, all Accepted 2026-11-04 by jhutchison:

- `0002-lanes-are-harness-agnostic.md`: lanes completable with terminal+browser, AGENTS.md + CLAUDE.md shim, no `.claude/` in lanes
- `0003-debrief-not-sitrep.md`: `debrief` in lanes, `status` in handbook, term budget 3, civil-military split
- `0004-lane-discovery-by-gitlab-group-not-filesystem.md`: harvester via group API, `config/handbook.yaml` pins host/group/subgroup, filesystem scan retained for tacsop tier
- `0005-recommend-not-enforce.md`: four musts vs ten recommendations, two-block report, recommending voice everywhere else, one RULES table

Each satisfies the triple filter; em dashes removed from handbook-authored docs, provenance ADR retained with its own.

### 10. Verify (Task 10)

- `pytest -q` in handbook: 81 passed, 0 failures.
- `lane_report.py` on `01-knowledge-graphs`: all 4 needed ready. Two consider items flagged: `term_budget` (5 lane terms in lane 01's README, limit 3; lane 01's longer vocabulary was deliberate) and `no_em_dashes` (em dash in `.gitlab/issue_templates/debrief.md:4`, from lane 01's `<!-- env:auto: replaced ... -->` comment). Neither blocks the report; exit 0.
- `new_lane.py --dry-run 02 gnn "Graph neural networks"`: 17 files, dry run prints tree and does not write.
- Scaffolded `02-gnn` to `/tmp` with `--start 2026-12-01`: every needed item ready, exit 0. No `.claude/` in the scaffold.
- `harvest.py --dry-run`: 404 from git-out without a token (expected off VPN / unauthenticated); `fetch_lessons` returns one notice per 404, never an exception. With a token on VPN, the same call lists `ai-cop/lanes` and parses lane 01's example entry.

### 11. Reduce military jargon

The handbook is written for ANL scientists. Military language was fine in tacsop (personal vocabulary, range analogy for the agent), but should not reach that audience.

**Decisions from the user:**

- (a) Collapse the four-level escalation ladder (Task / TCS / CONOP / OPORD) to two: Task and Plan. Keep the TCS idea (what to do / when done right / how you will know) as a table inside a plan, without the acronym. Rationale: the ladder name and the middle rungs were the bulk of the jargon; the well-scoped-task idea is the payload.
- (b) Keep `pillar`, `phase`, `wave`: structural terms (config keys, plan waves) whose rename would cost more than it clarifies; same reasoning as in tacsop.
- (c) Handbook no longer names `tacsop` outside contributor provenance. The handbook reads as self-standing to a scientist; the upstream is invisible.

**Changes (23 files, net −80 lines, commit `0183e58`):**

- `CONTEXT.md`: Three-tier `tacsop → handbook → lanes` diagram removed; identity rewritten as "the AI CoP guide." `Upstream: tacsop` removed; `Mission: Carry tacsop doctrine` removed. `Tacsop Heritage` section left to the ADRs.
- `LANGUAGE.md`: `Tacsop` / `Doctrine` glossary entries removed; `Tacsop Heritage` section gone. `TCS` / `CONOP` / `OPORD` removed. `Wave` redefined from "inside a CONOP or OPORD" to "inside a plan." New `Plan` entry replaces the three.
- `CLAUDE.md`: `tacsop is headquarters doctrine; handbook is range control SOP` opening rewritten to plain identity. `Planning Escalation` (4 levels) rewritten to `Planning: Task and Plan` (2 levels with well-scoped-task table). `/sitrep` → `/status` in the command table and structure tree.
- `README.md`: Only handbook-surface tacsop mention was in `Handbook development: This repo is itself a tacsop downstream`; reworded to plain development instructions.
- `docs/LANE-GUIDE.md`, `lane-template/*`, `docs/owners/*`: Already clean (never named tacsop; only the term-budget line mentions "lane vocabulary," not military vocabulary).
- `config/handbook.yaml`: Description `gated` → `verified`.
- `docs/owners/new-lane.md`, `running-a-cycle.md`, `glossary.md`, `lane-template/docs/CYCLE-PLAN.md`: `CW-3` → `fresh-clone verification` (opaque tacsop gate name, now plain).
- `.claude/commands/task.md`: Full rewrite of `Escalation Ladder` (4 levels, prowords, phase-vs-wave, campaign OPORD) → `When to Promote` + `Writing a Well-Scoped Task` (same decision guidance in plain words). `/task promote` kept as the tool name.
- `.claude/commands/status.md` (renamed from `sitrep.md` via `git mv`): `SITREP` → `Status Report` header; `TCS/CONOP/OPORD` removed from the "no internal jargon" advisory.
- `.claude/commands/pcc.md`: `per CONOP WHETSTONE D4` → plain `change alone:`.
- `.claude/commands/session-end.md`: `escalation ladder` → `when a task has outgrown a line`.
- `.claude/README.md`, `.claude/skills/SKILLS_FRAMEWORK.md`: 4-level ladder tables → 2-level (Task / Plan); `escalation ladder` → plain "approach for promoting complex work." Crosswalk section (SITREP→status-report, OPORD→operations-order, etc.) removed; replaced with a short note on the few persistent tacsop-derived config keys. `sitrep` → `status` in the "why commands not skills" paragraph.
- `.claude/skills/maintaining-ubiquitous-language/SKILL.md`: Wave redefined; "military escalation ladder" removed from docstring and topical-section guidance.
- `.claude/skills/writing-simple-and-direct/`: `CONOP-FORMAT` / `OPORD-FORMAT` → generic format refs (3 files).
- `docs/session-doc-format.md`: `doctrine` example/tag → `lesson-harvest`/`infra`; `KB-graph:` line removed (no traversing skill in handbook); preamble reworded.

**What stayed and why:**

- ADRs (`docs/adr/0003`-`0005`) still name tacsop: they are provenance records explaining the *lineage* of a decision (alternative A was "the tacsop pattern, applied directly"). Their audience is future handbook maintainers deciding whether to reverse, not lane participants.
- `.claude/skills/shift-left-testing/*` internals still carry tacsop-origin phrasing in non-participant surfaces. These are developer-facing skill sidecars behind the handbook; the participant-facing layer is already clear.
- `lane_report.py:TERM_RE` still matches `METL|OPORD|PCC|PCI|SITREP|red cell`: it is the checker that *polices* jargon, not jargon itself.
- `pillar`/`phase`/`wave` kept per (b). `phase` = roadmap milestone, `wave` = parallel tasks within a plan.

**Verification:** `pytest -q` in handbook: 81 passed. `lane_report` on lane 01: all 4 needed ready, exit 0. Scaffold still produces a clean lane. No `tacsop`/`CONOP`/`OPORD`/`TCS`/`proword`/`SITREP`/`CW-3` remains in handbook-facing docs outside ADRs; `docs/tasks.md` history line rewritten from "stripped tacsop" to "created handbook."

ADRs updated with references to `status` not `sitrep`:

- ADR `0003-debrief-not-sitrep.md` notes that `/status` (not tacsop's `SITREP`) serves the handbook's own reporting.

---

## Claims

| Claim | State | Evidence |
|---|---|---|
| Handbook commits `79f01d1` + `0183e58` on `origin/main` | deployed | `git -C handbook log --oneline -2` → `0183e58 [handbook] Reduce military jargon …` / `79f01d1 [handbook] Build ai-cop …`; `git -C handbook push` on each → `34581ff..79f01d1  main -> main` / `79f01d1..0183e58  main -> main` |
| `pytest` 81 passed in handbook | tested | `cd handbook && .venv/bin/python -m pytest -q` → `81 passed in 0.19s` (same output after jargon pass) |
| `pytest` 528 passed in tacsop | tested | `cd tacsop && .venv/bin/python -m pytest -q` → `528 passed, 5 skipped, 1 warning in 4.57s` |
| Lane template has no `.claude/` | observed | `ls handbook/lane-template/.claude 2>&1` → `no such file` and `.gitignore` covers `.claude/` whole |
| Fresh scaffold `02-gnn` passes all needed checks | tested | `.venv/bin/python src/handbook/new_lane.py 02 gnn … --dest /tmp && … lane_report.py /tmp/02-gnn` → 4 needed ready, `Exit code: 0` |
| `lane_report.py` on `01-knowledge-graphs` all needed ready | tested | `.venv/bin/python src/handbook/lane_report.py lanes/01-knowledge-graphs` → 4 `ready` under Needed, `Exit code: 0` |
| No em dashes in handbook new content | tested | `grep -r "—" --include="*.md" handbook/README handbook/CLAUDE handbook/CONTEXT handbook/LANGUAGE handbook/LESSONS handbook/config handbook/docs/LANE-GUIDE handbook/docs/owners handbook/docs/adr/000{2..5}*` → 0 hits |
| No military jargon in handbook docs | tested | `grep -rn -i "tacsop\|CONOP\|OPORD\|TCS\b\|proword\|CW-3" handbook --include="*.md" --include="*.yaml" --include="*.py` filtered to handbook-facing docs → 0 hits (ADRs and `.claude/skills/` retained as provenance/internal; `TERM_RE` in `lane_report.py` is the checker itself) |
| tacsop commit `adaf0c5` on `origin/main` | observed | `git -C tacsop log --oneline -1` → `adaf0c5 [doc] Session 2026-11-04: handbook as trimmed tacsop downstream`; `git -C tacsop status --porcelain` after push → `?? curl` / `?? docs/plans/…` only (pre-existing untracked) |

Overclaims the user caught this session: 0

Overclaims a reviewer caught this session: 0

---

## Key Decisions

| Decision | By | Rationale |
|---|---|---|
| Strip handbook in place, keep its `.git` | the user | Handbook checkout already had correct origin; fresh clone would be a round-trip for the same tree. |
| No `LICENSE` yet | the user | Holder undecided; contract flag noted, file removed from scaffold (lane template does not carry a license placeholder). |
| Keep `proposer` in handbook | the user | Lane planning and gate debates benefit from the debate step, as lane 01's agentic review showed. |
| Generic calendar in handbook README | the user | Two shapes (6-session planning: background/project/future/hands-on/hands-on/AAR; 3-session short: background/project/future) avoid manual per-cycle updates. Cycle 01's six dates live in lane 01's `docs/CYCLE-PLAN.md`. |
| `check_env.py` in template is minimal, REQUIRED empty | the lead | A lane's dependency surface is one notebook and sample data, not yet known at scaffold time; the owner fills the list per lane rather than carrying lane 01's 8-package surface into unrelated lanes. |
| `LESSONS.md` parse treats format-only file as empty-ok | the lead | The template has no live AAR heading by design; reporting it as failed would mean every new scaffold is not ready on day one. Bare `Lesson:` bullets without a heading still error. |
| `no_em_dashes` skips `.claude/` + `tests/fixtures/` + provenance ADR | the lead | `.claude/` is tacsop infrastructure, fixtures intentionally contain drift, and ADR-FORMAT's provenance em dashes are append-only history. The handbook's own new content (8 docs + 4 ADRs) is what the constraint governs. |
| Lane 01's `term_budget` and `no_em_dashes` flagged consider-only | verified | Lane 01 legitimately carries a longer participant vocabulary (5 terms) and one em dash in the debrief template comment. Neither violates a must; the report's two-block split exists for exactly this. |
| Task→Plan, not TCS/CONOP/OPORD | the user + lead | The TCS table (what to do / when done right / how you will know) is the craft; the acronym and the four-level ladder were the jargon. Collapsing to Task and Plan keeps the well-scoped-task idea without asking scientists to learn a military framework. Proposer suggested the rename; the user approved. |
| Keep `pillar`/`phase`/`wave` | the user + lead | Structural terms (config keys, plan phases/waves) whose rename would churn code and tooling for little clarity win; same reasoning as in tacsop. |
| Tacsop silent on participant surfaces | the user + lead | Handbook earns trust by being clear, not by citing lineage. Scientists meet one name: the handbook. ADRs and `.claude/` still carry provenance for maintainers who need it. |
| `CW-3` → `fresh-clone verification` | the lead | Opaque tacsop gate name with no meaning to the new audience; plain words cost nothing. |
| `/sitrep` → `/status` | the lead | Same verb as the prose skill's "the point of a status report is the status"; short, civilian, unambiguous. The underlying format is unchanged. |

---

## Pillar Compliance

| Pillar | Status | Notes |
|---|---|---|
| **Simplicity First** | PASS | Handbook is docs + template + 3 scripts. No lake, no decision science, no machine roster, no gaps. Template scripts are generic stubs; the owner fills the dependency list per lane. Jargon pass was net negative 80 lines. |
| **Shift-Left Testing** | PASS | 81 tests, written failing first per vertical slice, 8 red cases seen before the fix. Hook retargeted to `src/handbook/`. Jargon pass kept all tests green. |
| **Config-Driven** | PASS | `config/handbook.yaml` is the source for GitLab host/group/labels/seats; all three scripts read it. `GITLAB_TOKEN` in `.env`, never committed. |

---

## Commits

| Hash | Subject | Where |
|---|---|---|
| `79f01d1` | [handbook] Build ai-cop handbook as trimmed tacsop downstream | `ai-cop/handbook` on `origin/main` |
| `0183e58` | [handbook] Reduce military jargon to a minimum | `ai-cop/handbook` on `origin/main` |
| this doc | [doc] Session 2026-11-04: handbook as trimmed tacsop downstream | `tacsop` on `main` (next, amended to cover jargon pass) |

---

## Next Steps

1. Fill cycle 1 handbook seats (distro owner, week-2 lead, week-4 builder, week-3 briefer) by the dates in lane 01's `docs/sessions/01-crawl.md` section 7.
2. Week 4 builder lands `notebooks/01_build_and_traverse.ipynb` and `data/sample_docs/*.txt` + `manifest.csv` from NOAA bulk CSVs; the fresh-clone verification (23 Nov) requires a non-author check.
3. Week 5 builder completes `skills/kg-traversal/SKILL.md` and the traversals.
4. Migrate `assay/.claude/handbook_contract.md` and `lanes_contract.md` to the handbook (consider archiving the assay copies or marking them superseded by the handbook's `docs/LANE-GUIDE.md` and owner guides).
5. Consider the two `lane_report.py` consider-only findings against lane 01 (term budget 5 > 3, em dash in debrief template) as candidate cleanups outside a must fix. The division-level WSL recommendation from lane 01 also belongs in the handbook's participant page or owner guide, not in the lane README.
