# Session: Knowledge Graph Lane, Harness-Agnostic Contract Aligned

**Date**: 2026-11-04 (titanx)
**Branch**: main
**Tags**: #session #doctrine #infra #docs #complete
**Documents**: [lanes_contract.md](../../.claude/lanes_contract.md), task file in assay defining the lane interface; [01-knowledge-graphs](https://git-out.gss.anl.gov/ai-cop/lanes/01-knowledge-graphs), the lane repo this session modified
**Follows**: [20261030_picket_rulings_and_shelving.md](20261030_picket_rulings_and_shelving.md)

---

## Summary

The user had a zip of the new lane `ai-cop/lanes/01-knowledge-graphs` that unpacked into a nested directory instead of the repo root. After fixing the extraction, the user shared the intended lane contract from `assay/.claude/lanes_contract.md`: eight tasks making the lane completable with only a terminal and a browser, with one interface to tacsop (the `LESSONS.md` format). The session reviewed the contract, recommended leaving `config/` out until cycle 2, then executed the contract. The lane now has `AGENTS.md`, a one-line `CLAUDE.md` shim, `scripts/debrief.py`, a group-level label set, a fixed `LESSONS.md` format, and a harness-free README. A fresh clone on this box runs `uv sync` and `check_env.py` green (except the expected missing endpoint).

| Metric | Value |
|---|---|
| Hub tests at close | 528 passed, 5 skipped |
| Lane commits this session | 1 (`cea18a0` on `ai-cop/lanes/01-knowledge-graphs`, pushed) |
| Hub commits this session | 0 (lane work lives in the lane; this doc is the hub record) |
| AGENTS.md / CLAUDE.md created | 1 / 1 |
| Labels on group `ai-cop` | 10 (4 `type::` + 6 `week::`), 0 project-level duplicates |
| Fresh-clone check_env | all GREEN except `OPENAI_BASE_URL` not set (expected) |

---

## Work Completed

### 1. Unzip without losing the repo format

The zip contained a top-level `cop-cycle-01-knowledge-graphs/` directory but the repo root is `01-knowledge-graphs`. A plain `unzip` would create `01-knowledge-graphs/cop-cycle-01-knowledge-graphs/...` with `.git` at the wrong level. The fix extracted to a temp directory then `rsync -av`'d the contents of the inner directory into the repo root, which strips the wrapper and correctly places dotfiles (`.gitignore`, `.python-version`). Verified `git log` still at `42497dd`, `origin` still `git-out.gss.anl.gov/ai-cop/lanes/01-knowledge-graphs.git`, no nested directory, and the zip's `cop-cycle-01-knowledge-graphs.zip` removed from the working tree after staging.

### 2. Contract review and the config question

Read `assay/.claude/lanes_contract.md` (eight tasks, four constraints, report shape) and surveyed the lane repo as unpacked: `README.md`, `LESSONS.md`, `pyproject.toml`, `.python-version`, `.gitignore`, `docs/` (four files), `notebooks/README.md`, `skills/kg-traversal/SKILL.md`, `data/sample_docs/README.md`, `scripts/check_env.py` + `fetch_storm_narratives.py`. `docs/` was not in the contract's required list; the user confirmed it stays. Discussed the central-config pillar: recommended leaving `config/` and YAML out until cycle 2, because the lane's variable surface is two lists in a notebook cell, `pyproject.toml` and `.python-version` already are config, and indirection would cost clarity for a repo whose learning objective is “what is a triple.” The user agreed.

### 3. Lane aligned to the contract

Each task mapped to a file change in `ai-cop/lanes/01-knowledge-graphs` on `main` (`cea18a0`):

* **Task 1 — repo contract.** Confirmed the required set plus `docs/` is present: `README.md`, `LESSONS.md`, `AGENTS.md`, `pyproject.toml`, `scripts/check_env.py`, `scripts/debrief.py`, `notebooks/`, `skills/`, `data/`.
* **Task 2 — agent-facing files.** Wrote `AGENTS.md` (what the repo is, how to run it, what not to touch) and `CLAUDE.md` as `See AGENTS.md.` No `.claude/` directory in the lane. `skills/kg-traversal/SKILL.md` stays plain markdown with frontmatter, no install step.
* **Task 3 — debrief naming.** No `sitrep` existed to rename; fixed the one `METL` hit in `docs/sessions/01-crawl.md` and renamed `cop-cycle-01-knowledge-graphs` to `01-knowledge-graphs` in `pyproject.toml` and `docs/sessions/01-crawl.md`. `tacsop` `/sitrep` skill untouched.
* **Task 4 — labels at group level.** Created 10 labels on group `ai-cop` (2077) via the GitLab API: `type::debrief`, `type::defect`, `type::lesson`, `type::task` and `week::1` through `week::6`. No project-level duplicates — the project inherits the group labels (identical IDs).
* **Task 5 — issue template.** Wrote `.gitlab/issue_templates/debrief.md` with auto environment block and four prompts (what I ran / what broke / what I changed / harness used), plus `/assign @jhutchison` and `/label ~"type::debrief"`. `scripts/debrief.py` mirrors it and opens a prefilled GitLab issue URL.
* **Task 6 — LESSONS.md fixed.** Replaced the skeleton AAR template with the contract's shape (`Lesson / Evidence / Applies to / Harness`) plus one example entry dated 2026-11-04. Retained facilitator prompts below.
* **Task 7 — README.** Clone line now passes an explicit folder (`git clone https://git-out.gss.anl.gov/ai-cop/lanes/01-knowledge-graphs.git 01-knowledge-graphs`). Added “You need only a terminal and a browser. No agent is required.” and “Participants file debriefs as issues. The distro owner files merge requests.” `uv.lock` committed for reproducible installs.
* **Task 8 — verify.** Simulated fresh clone in `/tmp` then cloned from remote after push: `uv sync` green, `check_env.py` all green except endpoint not set, `debrief.py --dry-run` builds the issue URL, `jupyter` available, no `.claude/` in lane, no tacsop structure.

Constraints checked: no tacsop structure in lane, participant-facing text uses only `lanes`, `debrief`, `AAR`, no em dashes in any file, sample data is NOAA public domain reachable off VPN.

`scripts/debrief.py` fix: the initial `from scripts.check_env import EnvChecker` failed when run as `python scripts/debrief.py` (no package context, and `dataclass` resolution on Python 3.13 needs `sys.modules`). Switched to `importlib.util.spec_from_file_location` with `sys.modules` registration.

---

## Claims

| Claim | State | Evidence |
|---|---|---|
| The lane repo at `cea18a0` contains the required contract files | written | `ls` in the lane → `AGENTS.md CLAUDE.md LESSONS.md README.md pyproject.toml scripts/check_env.py scripts/debrief.py notebooks/ skills/ data/` and `ls .claude 2>&1` → `no such file` |
| `CLAUDE.md` is one line pointing to `AGENTS.md` | written | `cat CLAUDE.md` → `See AGENTS.md.` |
| `AGENTS.md` and `CLAUDE.md` are on `main` at `cea18a0` | deployed | `git log --oneline -1` in the lane → `cea18a0 Lane 01: align with harness-agnostic contract`; `git push` → `42497dd..cea18a0 main -> main` |
| 10 labels exist on group `ai-cop` and are inherited by the project | observed | `curl --header PRIVATE-TOKEN ... /api/v4/groups/2077/labels` → 10 names (`type::debrief` … `week::6`); `/api/v4/projects/1214/labels` → same 10 with identical IDs (1196–1205) |
| `LESSONS.md` has the fixed format with one example entry | written | `head -15 LESSONS.md` → `## YYYY-MM-DD (AAR, lane NN)` / `Lesson / Evidence / Applies to / Harness` and `## 2026-11-04 (AAR, lane 01) example` |
| Fresh clone runs `uv sync` and `check_env.py` green except endpoint | tested | temp-dir clone + `uv sync` → deps resolved; `.venv/bin/python scripts/check_env.py` → 8 `GREEN` imports, `RED OPENAI_BASE_URL not set`, `GREEN write to data/` |
| `scripts/debrief.py --dry-run` opens a prefilled issue URL | tested | `.venv/bin/python scripts/debrief.py --dry-run` → URL containing `issue[title]=Debrief` and four prompt headings plus `/assign @jhutchison` |
| No em dashes in participant-facing files | tested | `grep -rn "—\|–" --include="*.md"` over lane → 0 hits after fix |
| No banned doctrine terms in the lane | tested | `grep -rn "METL\|OPORD\|SITREP\|red cell"` over lane → 0 hits |
| Lane has no tacsop structure | observed | `ls` for `.claude/ CONTEXT.md LANGUAGE.md config/` in lane → all `no such file` |
| Hub suite passes at close | tested | `.venv/bin/pytest -q` in tacsop → `528 passed, 5 skipped, 1 warning` |

Overclaims the user caught this session: 0

Overclaims a reviewer caught this session: 0

All 11 claims were re-run at close except the deployed and written claims whose evidence is the commit content. The private-term check warned “no list at ~/.config/tacsop/private-terms” on this host (titanx); no push from the hub was made, so no new content was scanned.

---

## Key Decisions

| Decision | By | Rationale |
|---|---|---|
| Keep `docs/` in the lane | the user | Four files are the week 1 takeaway; removing them would break the 6 Nov approval that depends on `CYCLE-PLAN.md`. |
| No `config/` until cycle 2 | the user, on the lead's recommendation | `pyproject.toml` and `.python-version` already are config; a YAML layer would move two notebook lists behind an extra read for no deployment to vary. |
| Distro owner `@jhutchison` in the debrief template | the lead | Cycle lead owns the repo until the distro owner seat is filled on 9 Nov; one-line change when it is. |

---

## Pillar Compliance

| Pillar | Status | Notes |
|---|---|---|
| **Simplicity First** | PASS | Lane stays runnable with a terminal and a browser; no agent, no server, no config loader added. |
| **Shift-Left Testing** | PASS | `check_env.py` is the executable gate; fresh-clone verification ran before push. Hub suite green. |
| **Config-Driven** | PASS | Pins live in `pyproject.toml` and `.python-version`; no hardcoded endpoint values. `config/` deferred deliberately. |

---

## Commits

| Hash | Subject | Where |
|---|---|---|
| `cea18a0` | Lane 01: align with harness-agnostic contract | `ai-cop/lanes/01-knowledge-graphs` on `origin/main` |
| this doc | [doc] Session 2026-11-04: knowledge graph lane, harness-agnostic contract aligned | `tacsop` on `main` (next) |

---

## Next Steps

1. Fill the distro owner, week-2 lead, week-4 builder, and week-3 briefer seats by the dates in `docs/sessions/01-crawl.md` section 7.
2. Week 4 builder lands `notebooks/01_build_and_traverse.ipynb` and `data/sample_docs/*.txt` + `manifest.csv` from NOAA bulk CSVs; the CW-3 gate (23 Nov) requires a fresh-clone run by a non-author.
3. Week 5 builder completes `skills/kg-traversal/SKILL.md` and the `kg_traversal.py` traversals.
4. Consider cycle 2 `config/` only when a real deployment variance appears.

