# Session: Knowledge Graph Lane, Harness-Agnostic Contract Aligned

**Date**: 2026-11-04 (titanx, all day)
**Branch**: main
**Tags**: #session #doctrine #infra #docs #complete
**Documents**: [lanes_contract.md](../../.claude/lanes_contract.md), task file in assay defining the lane interface; [01-knowledge-graphs](https://git-out.gss.anl.gov/ai-cop/lanes/01-knowledge-graphs), the lane repo this session modified
**Follows**: [20261030_picket_rulings_and_shelving.md](20261030_picket_rulings_and_shelving.md)

---

## Summary

The user had a zip of the new lane `ai-cop/lanes/01-knowledge-graphs` that unpacked into a nested directory instead of the repo root. After fixing the extraction, the user shared the intended lane contract from `assay/.claude/lanes_contract.md`: eight tasks making the lane completable with only a terminal and a browser, with one interface to tacsop (the `LESSONS.md` format). The session reviewed the contract, recommended leaving `config/` out until cycle 2, then executed all eight tasks. Follow-on work from the user's live test and an agentic review fixed the pip fallback, clarified endpoint and activation docs, recommended WSL without requiring it, and hardened the debrief tooling. The lane now has `AGENTS.md`, a one-line `CLAUDE.md` shim, `scripts/debrief.py` with derived titles and a single-source template, a group-level label set, a fixed `LESSONS.md` format, and a harness-free README that trains novices back to plain `python`. A fresh clone on this box runs `uv sync` and `check_env.py` green except the expected missing endpoint.

| Metric | Value |
|---|---|
| Hub tests at close | 528 passed, 5 skipped |
| Lane commits this session | 8 on `ai-cop/lanes/01-knowledge-graphs`, all pushed |
| Hub commits this session | 1 (this doc) |
| AGENTS.md / CLAUDE.md created | 1 / 1 |
| Labels on group `ai-cop` | 10 (4 `type::` + 6 `week::`), 0 project-level duplicates |
| Fresh-clone check_env | all GREEN except `OPENAI_BASE_URL` not set (expected) |

---

## Work Completed

### 1. Unzip without losing the repo format

The zip contained a top-level `cop-cycle-01-knowledge-graphs/` directory but the repo root is `01-knowledge-graphs`. A plain `unzip` would create `01-knowledge-graphs/cop-cycle-01-knowledge-graphs/...` with `.git` at the wrong level. The fix extracted to a temp directory then `rsync -av`'d the contents of the inner directory into the repo root, which strips the wrapper and correctly places dotfiles (`.gitignore`, `.python-version`). Verified `git log` still at `42497dd`, `origin` still `git-out.gss.anl.gov/ai-cop/lanes/01-knowledge-graphs.git`, no nested directory, and the zip's `cop-cycle-01-knowledge-graphs.zip` removed from the working tree after staging.

### 2. Contract review and the config question

Read `assay/.claude/lanes_contract.md` (eight tasks, four constraints, report shape) and surveyed the lane repo as unpacked: `README.md`, `LESSONS.md`, `pyproject.toml`, `.python-version`, `.gitignore`, `docs/` (four files), `notebooks/README.md`, `skills/kg-traversal/SKILL.md`, `data/sample_docs/README.md`, `scripts/check_env.py` + `fetch_storm_narratives.py`. `docs/` was not in the contract's required list; the user confirmed it stays. Discussed the central-config pillar: recommended leaving `config/` and YAML out until cycle 2, because the lane's variable surface is two lists in a notebook cell, `pyproject.toml` and `.python-version` already are config, and indirection would cost clarity for a repo whose learning objective is “what is a triple.” The user agreed.

### 3. Lane aligned to the contract (cea18a0)

Each task mapped to a file change in `ai-cop/lanes/01-knowledge-graphs` on `main`:

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

### 4. Live test and README fixes

The user followed the README and hit three stacked failures: a truncated `OPENAI_BASE_UR` copy from the file open at line 63, `python` not found on the box, and `python3` checking the system 3.14 with no packages. The README then said `.venv/bin/python` without explaining why. Fixed to recommend `source .venv/bin/activate` then `python` as the formal path — it returns novices to the plain command they already know — with `docs/env-setup.md` noting `.venv/bin/python` and `uv run` as alternatives. Added an Argo-first endpoint section (a raw OpenAI key works but loses audit and cost tracking) and a verbose `docs/env-setup.md` that coaches activation, endpoint setup, and the red-line triage. The `LCRC/ALCF` comparison was struck after recall it was `module load`, not `source`.

Clarified the two base URLs: coding agents use `ANTHROPIC_BASE_URL` without `/v1`, the workbook uses `OPENAI_BASE_URL` with `/v1` because the OpenAI client adds `/chat/completions` and `/models`. The README states the workbook connection is separate from any agent connection.

### 5. Agentic review and hardening (a33b0f2, d0b7fb2, 2fb296f)

The user's agentic review found one real break and several consistency issues. Triaged with the user: fix the break and easy alignment now, defer the opinionated debrief/LESSONS enrichment to the handbook discussion.

* **Must fix, landed in a33b0f2:** `pip install -e .` failed — `pyproject.toml` had no `[build-system]` so setuptools treated `data/`, `skills/`, `notebooks/` as packages. Added `requires = ["setuptools>=69"]`, `build-backend = "setuptools.build_meta"`, and `packages = []`. Verified `uv run --with pip python -m pip install -e .` and `uv sync` both pass. Fixed Windows `python3.13 -m venv` to `py -3.13` on native and made `uv sync` + `.venv\Scripts\activate` the recommended Windows path. Dropped the ALCF line from the README (kept once in `docs/env-setup.md`), fixed the session plan label from `env` to `type::defect` + `week::1`, struck the leaked “That is why python3 shows 3.14” note, and widened `.gitignore` to `.agent/` and `.cursor/` whole.

* **OS recommendation, landed in d0b7fb2:** WSL as the recommended Windows path with a link to `docs/env-setup.md#wsl`, native as a tested fallback, not a requirement. The README now has a three-platform note; the WSL section in `docs/env-setup.md` names the four failure modes (admin and reboot, clone inside WSL filesystem not `/mnt/c` or OneDrive, lab CA bundle, VS Code WSL extension). The division-level recommendation was noted as belonging in the handbook with this lane's platform data, not in the lane README.

* **Debrief and LESSONS, landed in 2fb296f:** The review wanted `week::N` labels, milestones, derived titles, and a single-source template. Agreed milestones are ahead of schedule and the cycle owner builds them as they update the repo. Coded title derivation (`Debrief: GREEN` or `Debrief: RED (n)`, with optional `--week N` prefix such as `Debrief week 1: RED (1)`), `--week` adding `week::N` label (milestone line left commented until `Week N` milestones exist), and a single-source read: `debrief.py` now substitutes the `<!-- env:auto -->` block in `.gitlab/issue_templates/debrief.md` with a fallback to the inline body. For `LESSONS.md` the example moved inside the fenced format block so the hub does not harvest it; a horizontal rule separates entries from running session notes. The broader split to `docs/aar.md` and the handbook as the home for instructional material was agreed as the next design.

---

## Claims

| Claim | State | Evidence |
|---|---|---|
| The lane repo at `2fb296f` contains the required contract files | written | `ls` in the lane → `AGENTS.md CLAUDE.md LESSONS.md README.md pyproject.toml scripts/check_env.py scripts/debrief.py notebooks/ skills/ data/ docs/env-setup.md` and `ls .claude 2>&1` → `no such file` |
| `CLAUDE.md` is one line pointing to `AGENTS.md` | written | `cat CLAUDE.md` → `See AGENTS.md.` |
| `AGENTS.md` and `CLAUDE.md` are on `main` at `2fb296f` | deployed | `git -C lane log --oneline -1` → `2fb296f ...` ; `git -C lane push` for each of the 8 → `... main -> main` |
| 10 labels exist on group `ai-cop` and are inherited by the project | observed | `curl --header PRIVATE-TOKEN ... /api/v4/groups/2077/labels` → 10 names (`type::debrief` … `week::6`); `/api/v4/projects/1214/labels` → same 10 with identical IDs (1196–1205) |
| `pip install -e .` works after the build-system fix | tested | `uv run --with pip python -m pip install -e .` → `Successfully installed 01-knowledge-graphs-0.1.0`; `uv sync` → `Resolved 194 packages` |
| `LESSONS.md` has the fixed format with the example inside the fence | written | `head -16 LESSONS.md` shows the fenced format block containing `Example:` and `## 2026-11-04 (AAR, lane 01)`; `grep "^## 2026" LESSONS.md` outside the fence → 0 hits |
| `scripts/debrief.py --dry-run` builds the issue URL | tested | `.venv/bin/python scripts/debrief.py --dry-run` → URL with `issue[title]=Debrief` and four prompt headings plus `/assign @jhutchison` |
| `scripts/debrief.py --dry-run --week 1` title and label | tested | `... --week 1 --dry-run` → URL `Debrief+week+1%3A+RED+%281%29` and `week::1` label |
| Fresh clone runs `uv sync` and `check_env.py` green except endpoint | tested | temp-dir clone + `uv sync` → deps resolved; `.venv/bin/python scripts/check_env.py` → 8 `GREEN` imports, `RED OPENAI_BASE_URL not set`, `GREEN write to data/` |
| No em dashes in the lane | tested | `grep -rn "—" --include="*.md"` over lane excluding `.venv` → 0 hits |
| Lane has no tacsop structure | observed | `ls` for `.claude/ CONTEXT.md LANGUAGE.md config/` in lane → all `no such file` |
| Hub suite passes at close | tested | `.venv/bin/pytest -q` in tacsop → `528 passed, 5 skipped, 1 warning` |

Overclaims the user caught this session: 0

Overclaims a reviewer caught this session: 0

---

## Key Decisions

| Decision | By | Rationale |
|---|---|---|
| Keep `docs/` in the lane | the user | Four files are the week 1 takeaway; removing them would break the 6 Nov approval that depends on `CYCLE-PLAN.md`. |
| No `config/` until cycle 2 | the user, on the lead's recommendation | `pyproject.toml` and `.python-version` already are config; a YAML layer would move two notebook lists behind an extra read for no deployment to vary. |
| Distro owner `@jhutchison` in the debrief template | the lead | Cycle lead owns the repo until the distro owner seat is filled on 9 Nov; one-line change when it is. |
| `source .venv/bin/activate` then `python` as the formal path | the user | Returns novices to the plain command they already know; `source` is the one step they will reuse after they learn it. The HPC comparison was mistaken (`module load`), so the why was cut to the novice reason alone. |
| `pip` needs `[build-system]` + `packages = []` | the user, on the reviewer's report | `uv` already worked; `pip` treated `data/`, `skills/`, `notebooks/` as packages and refused. The fix makes both installers pass. |
| WSL recommended, not required, for Windows | the user | Week 1 is the wrong week to change someone's OS; recommend WSL with a link, keep native as a tested fallback, and let debrief platform data drive a later division recommendation. The handbook holds that recommendation, not the lane. |
| Debrief milestone deferred, title and template now | the user | Milestones are ahead of schedule and the cycle owner builds them as they update the repo. Title derivation and single-source template were worth coding now; the broader `LESSONS.md` split to `docs/aar.md` belongs in the handbook. |

---

## Pillar Compliance

| Pillar | Status | Notes |
|---|---|---|
| **Simplicity First** | PASS | Lane stays runnable with a terminal and a browser; no agent, no server, no config loader added. Build-system fix is two blocks, not a src layout. |
| **Shift-Left Testing** | PASS | `check_env.py` is the executable gate; fresh-clone verification and pip vs uv checks ran before each push. Hub suite green. |
| **Config-Driven** | PASS | Pins live in `pyproject.toml` and `.python-version`; no hardcoded endpoint values. `config/` deferred deliberately. |

---

## Commits

| Hash | Subject | Where |
|---|---|---|
| `cea18a0` | Lane 01: align with harness-agnostic contract | `ai-cop/lanes/01-knowledge-graphs` on `origin/main` |
| `ec565fc` | Lane 01: README shows Argo-first endpoint and .venv/bin/python | `ai-cop/lanes/01-knowledge-graphs` on `origin/main` |
| `1144f2a` | Lane 01: recommend source activate as the formal path | `ai-cop/lanes/01-knowledge-graphs` on `origin/main` |
| `46f6fc1` | Lane 01: clarify workbook vs agent Argo endpoints | `ai-cop/lanes/01-knowledge-graphs` on `origin/main` |
| `8df5f8c` | Lane 01: strike LCRC/ALCF comparison for activate step | `ai-cop/lanes/01-knowledge-graphs` on `origin/main` |
| `a33b0f2` | Lane 01: fix pip fallback and align docs before team test | `ai-cop/lanes/01-knowledge-graphs` on `origin/main` |
| `d0b7fb2` | Lane 01: recommend WSL for Windows, do not require it | `ai-cop/lanes/01-knowledge-graphs` on `origin/main` |
| `2fb296f` | Lane 01: debrief title derived, single-source template, LESSONS harvest fix | `ai-cop/lanes/01-knowledge-graphs` on `origin/main` |
| this doc | [doc] Session 2026-11-04: knowledge graph lane, harness-agnostic contract aligned | `tacsop` on `main` (next) |

---

## Next Steps

1. Fill the distro owner, week-2 lead, week-4 builder, and week-3 briefer seats by the dates in `docs/sessions/01-crawl.md` section 7.
2. Week 4 builder lands `notebooks/01_build_and_traverse.ipynb` and `data/sample_docs/*.txt` + `manifest.csv` from NOAA bulk CSVs; the CW-3 gate (23 Nov) requires a fresh-clone run by a non-author.
3. Week 5 builder completes `skills/kg-traversal/SKILL.md` and the `kg_traversal.py` traversals.
4. Create the handbook repo (tacsop lite for users and cycle owners) to hold the division-level WSL recommendation, the full AAR split, and the instructional material that should not repeat in each weekly lane.
5. Consider cycle 2 `config/` only when a real deployment variance appears.

