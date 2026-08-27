# Doctrine Updates

Changes to shared workflow commands and planning framework. Downstream repos are notified via `.claude/upstream-update.md` — review and selectively merge.

---

## 2026-08-27: Figure Style Doctrine (designing-clear-data-displays) + Research Tools + Audit-Hook Fallback

Three parts, each independently adoptable through its own table. **Part 1 is the
headline**: a Level 0 skill for data displays, the twin of `writing-simple-and-direct`,
built downstream in `stx-server` on 2026-08-27 and copied into the hub whole. Parts 2
and 3 are two small fixes the same repo routed upstream. Audience: every downstream repo;
Part 2 has one stated opt-out. All three are additive; nothing breaks.

Credit: `stx-server` built the skill (proposal, adversarial challenge, 26 numbered lead
decisions, two gate reviews, an outside feedback round; 34 Tufte quotations verified by
fetch) to settle a label-collision bug on a field map, then measured the fix in a headless
browser: 12 collisions before, 0 after, font unchanged. The hub's harvest of that repo's
eight sessions is `docs/reviews/20260827_stx_server_lessons_harvest.md`.

### Part 1: Figure Style, the `designing-clear-data-displays` skill (1.1.0)

Every chart, figure, map, table, or data-bearing layout now follows eight rules, the way
every prose artifact follows the writing kernel:

1. Show the data; erase ink that carries none, within reason.
2. Label the data where it lives; a key the eye must decode fails.
3. Make every distinction as subtle as it can be and still be seen.
4. Two marks too close make a third; move one, do not shrink both.
5. Show the effect at its true size: lie factor between 0.95 and 1.05.
6. Answer "compared to what?"; small multiples over one lonely chart.
7. Document the display: title, source, units, scale on the figure.
8. Content counts most: simple design, intense content.

Before the eight: could a table or a sentence carry these numbers? Under about twenty,
a table usually does. The skill is Tufte's material as named rules with sources and
tests, not a persona: `RULES.md` expands each rule with the failure it counters, its
source (primary or secondary, marked), and the test that catches it; `EXAMPLES.md` gives
six generic before/after pairs including the one that grows (documentation is data-ink);
`REVIEWING.md` is a five-pass review protocol with a finding format that requires a
redraw; `ADOPTION.md` is the install procedure below.

Two boundary conditions, restated so no consumer over-applies the rules:

- **Grandfathering**: adoption triggers no sweep. A figure a change touches, or a queued
  task names, gets the full pass order; a display the app still renders is not a record.
- **UX rules outrank style**: a repo's own UX or accessibility rules can require a less
  dense display, a larger label, or a sentence in place of a table. State the override in
  CLAUDE.md, the pillars, or the plan's decision table; do not ignore the rule. The skill
  governs only how the ink goes. (`stx-server` states its Kid-First override in one
  sentence under the kernel; copy that shape.)

#### Adoption-Mode Table (Part 1)

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `.claude/skills/designing-clear-data-displays/` (SKILL.md + `RULES.md`, `EXAMPLES.md`, `REVIEWING.md`, `ADOPTION.md`) | **TEMPLATE-COPY** | All five files, 409 lines, no repo names. Level 0: copy, never edit locally; route fixes upstream. |
| 2 | `CLAUDE.md` Figure Style section | **PATCH** | Paste the block in `ADOPTION.md` step 1 beside Prose Style. Add one sentence naming your UX override if you have one. |
| 3 | `.claude/agents/code-reviewer.md` | **PATCH** | One checklist line beside the prose line (`ADOPTION.md` step 2). |
| 4 | `.claude/skills/SKILLS_FRAMEWORK.md`, `.claude/README.md` | **PATCH** | Index entry and tree line (`ADOPTION.md` step 3). While there: the description rule now reads "one to three sentences" (was "one"; two shipped skills carry three). |
| 5 | `.claude/skills/writing-simple-and-direct/SKILL.md` | **TEMPLATE-COPY** (1.0.1) or **PATCH** | One scope sentence: a chart that could be a table or a sentence is the figure skill's pre-question, not the prose skill's tokens to cut. Copy the file, or add the sentence after "Never cut a required section to save tokens." and bump the version. |
| 6 | A headless-browser layout probe | **OPTIONAL, LATER** | `ADOPTION.md` step 4. No dependency today; the seam exists. |

#### Action required (Part 1)

1. Copy the skill directory from the hub:
   ```bash
   cp -r ~/projects/github/tacsop/.claude/skills/designing-clear-data-displays .claude/skills/
   diff -r ~/projects/github/tacsop/.claude/skills/designing-clear-data-displays .claude/skills/designing-clear-data-displays && echo identical
   ```
2. Open `.claude/skills/designing-clear-data-displays/ADOPTION.md` and run its steps 1
   to 3: the CLAUDE.md block, the reviewer line, the two index entries.
3. If your repo has a UX or accessibility rule that outranks density, add one sentence
   under the CLAUDE.md block naming it as a decided trade-off.
4. Copy `writing-simple-and-direct/SKILL.md` (1.0.1) from the hub, or add the one scope
   sentence by hand.
5. Do not sweep existing figures. The next change that touches one gets the review.

Expected outcome: the code reviewer, on the next change that draws anything, produces
findings in the `REVIEWING.md` format (severity, rule, element by coordinate or selector,
concrete redraw). A finding without a redraw is a complaint, not a finding.

### Part 2: Research tools on the two Level 0 reasoning agents

`proposer` and `code-reviewer` gain `WebSearch, WebFetch` in their `tools:` lines so a
proposal can cite a source it fetched and a challenge can re-fetch it. The Level 0 rule
(keep them unchanged; they "should not accumulate project-specific knowledge")
guards knowledge, not capability; `.claude/README.md` now says so. First use: every
quotation in the Tufte skill traces to a fetched page or names the secondary source that
carries it, and the proposer left two rules out rather than invent their wording. A
ledger that excludes is worth more than one that fills in.

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 7 | `.claude/agents/proposer.md`, `.claude/agents/code-reviewer.md` | **PATCH** | `tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch` |
| 8 | `.claude/README.md` Level 0 paragraph | **PATCH** | The capability-versus-knowledge sentence, or copy the hub paragraph. |

Action required: edit the two `tools:` lines. Skip this part if your repo forbids
network access from agents; the skill in Part 1 does not depend on it.

### Part 3: Audit hook import-grep fallback

The shift-left audit hook looked for a test partner only by name
(`tests/**/test_<module>.py`). A repo that names its suites by feature
(`test_demo.py` exercising `app.main`) logged 27 false `MISSING_TEST` lines in one
execution-phase, and noise that large trains everyone to ignore the log. After the name
lookup misses, the hook now greps `tests/**/test_*.py` for an import of the module
(`from pkg.mod import`, `import pkg.mod`, or `from pkg import mod`) before logging. It
still never blocks and still exits 0 on every path.

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 9 | `.claude/hooks/post-tool-shift-left-audit.sh` | **TEMPLATE-COPY** then re-glob, or **PATCH** | If your copy is otherwise unpatched: copy the hub file and change `src/myproject/` to your package on the `case` line (`scripts/adopt_doctrine.py` does this substitution). If you patched it: port the one `if [ -z "$test_partners" ]` block that precedes the `MISSING_TEST` branch. Keep the executable bit: `git update-index --chmod=+x`. |
| 10 | `.claude/skills/shift-left-testing/ENFORCEMENT.md` | **TEMPLATE-COPY** | Step 4 and the limitations list describe the two-stage lookup. |
| 11 | `tests/unit/test_shift_left_hook.py` | **HUB-ONLY** | Nine tests (three behaviors) drive the hook with a JSON payload in a throwaway git repo. They assume `src/myproject/`; copy only if you change that path to your package. |

Action required:

1. Apply #9 and #10.
2. Verify from a shell (needs `jq` and `git`; replace `app/main.py` with a module you have, since the hook exits silently when the path's directory does not exist):
   ```bash
   printf '%s' '{"tool_name":"Edit","tool_input":{"file_path":"'"$PWD"'/src/app/main.py"}}' | bash .claude/hooks/post-tool-shift-left-audit.sh
   tail -1 .claude/audits/shift-left-violations.log
   ```
   A module that some `test_*.py` imports logs `OK_TEST_EXISTS` with that file as partner.

### Also fixed in the hub, mirror if you copied these files

- Running-prose em dashes in four template-copied docs (`docs/plans/CONOP-FORMAT.md`,
  `docs/plans/OPORD-FORMAT.md`, `docs/session-doc-format.md`, `.claude/README.md`):
  27 replaced per prose rule 8. Found by `stx-server`'s bootstrap audit, which could not
  fix hub copies locally without forking doctrine. TEMPLATE-COPY the four files if yours
  are unpatched; headings, table cells, and list-label separators were exempt and are
  untouched.
- `.claude/skills/shift-left-testing/SCRIPTS.md` line 3 no longer says "in this repo"
  about hub scripts.
- The hub's own skills trees (`.claude/README.md`, `SKILLS_FRAMEWORK.md`) listed six of
  nine Level 0 skills; both now match the directory. Check yours.

### Rollback

All three parts are additive and reversible by deletion. Part 1: remove the skill
directory, the CLAUDE.md section, the reviewer line, and the index entries; revert the
one sentence in the writing skill. Part 2: remove the two tool names. Part 3: restore
the prior hook (the name-only lookup is the `find` line that remains; delete the
fallback block). Nothing downstream depends on any of the three once removed.

### Files (tacsop)

```
.claude/skills/designing-clear-data-displays/SKILL.md          (1.1.0, copied whole from stx-server)
.claude/skills/designing-clear-data-displays/RULES.md
.claude/skills/designing-clear-data-displays/EXAMPLES.md
.claude/skills/designing-clear-data-displays/REVIEWING.md
.claude/skills/designing-clear-data-displays/ADOPTION.md
.claude/skills/writing-simple-and-direct/SKILL.md              (1.0.1: the hand-off sentence)
.claude/skills/SKILLS_FRAMEWORK.md                             (entry, tree, description rule)
.claude/skills/shift-left-testing/ENFORCEMENT.md               (step 4, limitations)
.claude/skills/shift-left-testing/SCRIPTS.md                   (line 3)
.claude/agents/code-reviewer.md                                (figure checklist line; tools)
.claude/agents/proposer.md                                     (tools)
.claude/hooks/post-tool-shift-left-audit.sh                    (import-grep fallback)
.claude/README.md                                              (skills tree; Level 0 paragraph; 3 dashes)
CLAUDE.md                                                      (Figure Style section)
docs/plans/CONOP-FORMAT.md                                     (9 dashes)
docs/plans/OPORD-FORMAT.md                                     (9 dashes)
docs/session-doc-format.md                                     (6 dashes)
docs/reviews/20260827_stx_server_lessons_harvest.md            (new: 33 lessons with provenance)
tests/unit/test_shift_left_hook.py                             (new: 9 tests, first written failing)
CHANGELOG.md
```

Hub verification: 278 tests passing (269 + 9 hook tests), `bash -n` clean on the hook,
skill bundle byte-identical to `stx-server` at its `307d195`.

---

## 2026-08-03: Environment Doctrine — uv Replaces pip/venv/pyenv/conda (Drop-In)

**uv** (Astral, written in Rust) is now the environment engine for every repo in this
doctrine family: one tool for interpreters, virtual environments, and packages. This
cycle is the **drop-in** adoption level: command surfaces change, `pyproject.toml` does
not, and no lockfile appears. The uv-native level (`uv sync`, committed `uv.lock`,
`uv run`) is deliberately deferred to a later cycle and will get its own ADR; drop-in
is forward-compatible with it.

The doctrine in three rules:

1. **uv is the only environment engine.** `uv venv --managed-python` creates
   environments; `uv pip ...` does all package operations. Never `sudo pip`, never
   system pip.
2. **Venvs build on uv-managed interpreters.** Without `--managed-python`, `uv venv`
   grabs whatever Python it finds first on `PATH` (pyenv shim, conda, system). A venv
   symlinked into an incumbent's install dies with it; a managed interpreter survives.
3. **Incumbents are removed last.** conda/miniforge/pyenv come off a machine only
   after every venv built on their interpreters has been rebuilt and parity-tested.
   Removal first bricks every one of those venvs.

Why: measured on the hub (WSL2, warm cache), a full rebuild of the tacsop environment
with all extras took under 30 seconds including the interpreter download; the
`.[all]` install alone took 8 seconds where pip took minutes. The managed-interpreter
model also ends the class of breakage where a pyenv/conda removal or system Python
upgrade silently kills every venv on the machine (the hub found 5 of 9 sibling venvs
exposed this way).

### Adoption-Mode Table

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | uv itself | **MANUAL** | Per machine: `curl -LsSf https://astral.sh/uv/install.sh \| sh` (installs to `~/.local/bin`). |
| 2 | Your repo's `.venv` | **MANUAL** | Rebuild on a managed interpreter; parity-test (steps below). |
| 3 | `.claude/skills/python-venv-management/` (SKILL.md + 2 sidecars) | **TEMPLATE-COPY** | v3.0.0 rebuilt on uv; replaces v2.0.0 wholesale. Includes the incumbent-migration order and a new uv failure-mode table. |
| 4 | `.claude/skills/shift-left-testing/CI.md` | **TEMPLATE-COPY** | CI pattern moves from `actions/setup-python` + pip to `astral-sh/setup-uv` with built-in caching. If you PATCHed your copy, port the four uv hunks instead. |
| 5 | `CLAUDE.md` Environment Setup + Quick Commands | **PATCH** | Setup block becomes `uv python install` / `uv venv --managed-python` / `uv pip install -e ".[dev]"`. `.venv/bin/pytest` and `source .venv/bin/activate` are unchanged. |
| 6 | `README.md` / setup docs | **PATCH** | Same substitution as #5. |
| 7 | `config/project.yaml` | **PATCH** | `python.package_manager: "pip"` → `"uv"` (config is the source of truth; say what is true). |
| 8 | In-code install hints (`pip install -e '.[x]'` in error messages) | **PATCH** | Hub did this test-first: guard tests assert `match="uv pip install"`, then the message strings change. Copy the pattern if your guards are tested. |
| 9 | conda / miniforge / pyenv | **MANUAL, LAST** | Remove only after step 5 of the sequence below passes on every repo on that machine. |

### Action required (the migration sequence, per machine)

1. **Install uv** and confirm: `uv --version`.
2. **Map the blast radius** — every venv coupled to an incumbent interpreter. Find
   venvs by their `pyvenv.cfg` marker, never by directory name: a `.venv/`-only glob
   missed 5 of 10 venvs on the first machine migrated (alternate names like
   `.venv-training/` and bare `venv/`, plus repos outside the main projects
   directory).
   ```bash
   find ~/projects -maxdepth 4 -name pyvenv.cfg | while read c; do
     echo "$(dirname "$c"): $(grep ^home "$c")"
   done
   ```
   Any `home` resolving into `~/.pyenv/`, `~/miniforge3/`, `~/miniconda3/`, or
   `~/anaconda3/` is on the rebuild list. Record it.
3. **Per repo on the list**: record the current test pass count and freeze the old
   venv as insurance, then rebuild:
   ```bash
   .venv/bin/pip list --format=freeze > /tmp/<repo>.freeze.txt
   uv python install 3.12          # or the repo's pinned version
   uv venv --clear --managed-python
   uv pip install -e ".[dev]"      # plus the extras the repo actually uses
   .venv/bin/pytest                # parity: pass count must match the recorded one
   ```
   (`uv venv --clear` beats `rm -rf`: it refuses to replace a directory that is not
   actually a virtual environment.) A shortfall means the old venv held something the
   repo's spec never listed, not a uv defect. The first machine hit three classes:
   a package absent from `requirements.txt` (48 tests silently uncollected), an
   unbounded major (`mcp>=1.0` resolving to 2.0.0, which moved the imported API),
   and a documented editable install that had never actually worked. Diff the freeze
   against `uv pip list` to close the gap, then file the spec fix in that repo.
4. **Adopt the artifacts** (#3–#8 above) in the repo.
5. **Verify the machine is clean**: rerun the step-2 loop; nothing may resolve into an
   incumbent path.
6. **Remove the incumbents** — the only destructive step, which is why it is last:
   ```bash
   # pyenv
   rm -rf ~/.pyenv    # plus its init lines in ~/.bashrc / ~/.zshrc / ~/.profile
   # conda / miniforge
   conda init --reverse
   rm -rf ~/miniforge3 ~/miniconda3 ~/anaconda3
   ```

### Footguns found in the field

- **uv venvs do not bundle pip.** `.venv/bin/pip` does not exist. Grep your scripts,
  Makefiles, and hooks for `.venv/bin/pip` or in-venv `pip` calls and route them
  through `uv pip`. If a tool genuinely needs in-venv pip, `uv venv --seed`.
- **Do not commit `.python-version` yet.** uv reads it, but pyenv reads the same file
  and errors on specs it lacks. Commit it only when every machine cloning the repo is
  off pyenv.
- **`uv venv` without `--managed-python` recreates the coupling** this cycle exists to
  remove. The hub hit this on its first attempt: uv silently picked the pyenv shim.

### Rollback

Fully reversible until step 6. `python3 -m venv .venv` + `pip install -e ".[dev]"`
still works at any point before the incumbents are removed; after step 6, rollback
means reinstalling the incumbent, which is why step 5's verification gates it.

### Files (tacsop)

```
.claude/skills/python-venv-management/SKILL.md            (3.0.0, rewritten on uv)
.claude/skills/python-venv-management/SETUP.md            (rewritten: uv patterns, uv python, migration order)
.claude/skills/python-venv-management/TROUBLESHOOTING.md  (rewritten: uv failure modes)
.claude/skills/shift-left-testing/CI.md                   (setup-uv workflow, cache section, xdist install line)
CLAUDE.md                                                 (Environment Setup, Quick Commands)
README.md                                                 (setup block)
CONTEXT.md                                                (hard-rules line)
config/project.yaml                                       (package_manager: uv; stale numpy known-issue removed)
src/myproject/decision_science/scorer.py                  (install hint → uv pip)
src/myproject/decision_science/visualization.py           (install hint → uv pip)
tests/unit/test_scorer.py                                 (new pandas-guard test, uv hint asserted)
tests/unit/test_visualization.py                          (guard matches tightened to "uv pip install")
```

Hub verification: 269 tests passing on a uv-built venv over uv-managed CPython
3.12.13. Field verification (first machine, 2026-08-03): the `pyvenv.cfg` sweep found
10 venvs across 9 repos where the name-based glob saw 5; 8 rebuilt on managed
interpreters at exact test parity, 6,898 passing tests total; 2 torch/CUDA venvs
consciously deferred with saved freezes (one held an expired March nightly no tool
could reproduce). pyenv was then removed and every rebuilt suite re-verified green.

---

## 2026-07-20: NAME CHANGE (`utils` → `tacsop`) + Planning Doctrine + Writing & Testing Doctrine

One combined cycle in three parts, each independently adoptable via its own
adoption-mode table. **Part 1 is the breaking item and leads deliberately; read it
even if you defer the rest.** Part 2 (planning doctrine, 2026-07-17) and Part 3
(writing and testing doctrine + relicense, 2026-07-20) are fully additive.

---

### Part 1 — NAME CHANGE: upstream hub renamed `utils` → `tacsop` (BREAKING)

The upstream hub repository has been renamed from `utils` to **`tacsop`** (Tactical
Standing Operating Procedure — the document through which a headquarters publishes the
standing procedures its units operate by, and from which each unit derives its own
local SOP). The old name described a utility library; the new name describes what the
hub actually is: the doctrinal foundation for agent/team workflows and task escalation.
Full rationale and candidate names in
[`docs/adr/0002-rename-repository-to-tacsop.md`](adr/0002-rename-repository-to-tacsop.md).

New canonical locations:

- GitHub: `https://github.com/jhutchison0/tacsop` (old URLs redirect as long as the
  name `utils` is never reused — it will not be)
- Local convention: `~/projects/github/tacsop/`

Nothing inside the bundle changes behavior: the `myproject` package placeholder, hook
substitution, and settings merges are all unchanged. The only breaking edge is the
hardcoded default upstream path in copies of `scripts/adopt_doctrine.py`.

### Adoption-Mode Table (Part 1)

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `scripts/adopt_doctrine.py` | **PATCH-COPY** | If your repo carries a copy from the 2026-05-19 bundle, its `DEFAULT_UPSTREAM` points at `~/projects/github/utils/`, which no longer exists after the local hub clone is renamed. Re-copy the current script from the hub, or edit the one line, or always pass `--upstream PATH`. |
| 2 | Local hub clone | **MANUAL** | Any machine with a clone of the hub needs a directory rename and remote update (steps below). |
| 3 | Historical docs/links | **NO ACTION** | Session docs, reviews, and old notifications that link `github.com/jhutchison0/utils` keep working via GitHub's rename redirect. Do not rewrite history. |

### Action required (Part 1)

1. On each machine with a local clone of the hub:
   ```bash
   mv ~/projects/github/utils ~/projects/github/tacsop
   cd ~/projects/github/tacsop
   git remote set-url origin https://github.com/jhutchison0/tacsop.git
   ```
2. If your repo carries `scripts/adopt_doctrine.py`, re-copy it from
   `~/projects/github/tacsop/scripts/adopt_doctrine.py` (its `DEFAULT_UPSTREAM` now
   points at the new path), or pass `--upstream ~/projects/github/tacsop` on every run.
3. If any CI job, mirror, or script of yours references the old GitHub URL directly,
   update it to `https://github.com/jhutchison0/tacsop` rather than trusting the
   redirect long-term.
4. Leave historical documents unchanged.

### Rollback (Part 1)

None needed. Taking no action costs nothing until you either (a) run a stale copy of
`adopt_doctrine.py` without `--upstream` after your local hub clone is renamed, or
(b) depend on the redirect from a context that resolves URLs strictly. Both are fixed
by the steps above at any later time.

---

### Part 2 — Planning Doctrine: plan-format standards, prowords, deep-modules (additive)

The task-escalation ladder (`/task`: task → task-condition-standard → concept-of-
operations → operations-order) has always specified tasks to a known standard (TCS),
but the two plan-document levels above it had no format standard at all. Two pinned
schemas now exist, following the `docs/adr/ADR-FORMAT.md` house pattern:
`docs/plans/CONOP-FORMAT.md` (concept-of-operations: where design decisions get
debated) and `docs/plans/OPORD-FORMAT.md` (operations-order: the execution form of a
decided strategy, five-paragraph, checkpointed).

The formats were validated against your history before shipping. A four-repo
retrospective (magic-movies, swimming-analytics, elephant-graveyard, tactics-game)
mined 20 multi-session churn episodes, classified with an explicit hindsight-bias
guard: 6 preventable-by-planning, 10 mixed, 3 discovery-priced-in, 1 pure process.
The dominant failure shape everywhere: **a load-bearing assumption with no falsifier
and no kill-criterion**. Second place: **named risks with toothless mitigations**
("we'll add a test later"). The formats' hardening targets exactly these:

- **Assumptions table** — every load-bearing assumption carries its cheapest
  empirical falsifier, its blast radius if wrong, and a kill-criterion.
- **Validate before detailing** — the falsifier runs before dependent
  execution-phases are authored in detail.
- **Execution-phase order derives from the stated dependency chain** — if the plan
  names a source of truth, phase 1 secures it.
- **Gating-metric calibration** — a metric may not gate work until it rank-orders
  known-good above known-bad references.
- **First-contact rule** — the earliest feasible checkpoint runs against the real
  target (real payloads, real hardware, real platform).
- **Checkpoints are commit-gates with a named owner** — a phase is not closed until
  its verifying commit exists.
- **Mid-phase halt** — a live finding that invalidates a phase's precondition halts
  the phase; it outranks the plan's momentum.
- **Terminal statuses + append-only lifecycle** — every plan ends Rejected,
  Complete, or Superseded; approved plans change only by dated amendment.

### Files (Part 2, tacsop)

```
docs/plans/CONOP-FORMAT.md                        (new)
docs/plans/OPORD-FORMAT.md                        (new)
.claude/commands/task.md                          (promote wiring, template pointers, Prowords section)
CLAUDE.md                                         (deep-modules sentence in Simplicity First)
.claude/agents/python-prototyper.md               (Step 4d interface check)
docs/reviews/20260717_planning_retrospective_*.md (evidence, reference-only)
```

### Adoption-Mode Table (Part 2)

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `docs/plans/CONOP-FORMAT.md` | **TEMPLATE-COPY** | Copy verbatim into your `docs/plans/`. Existing plans are grandfathered — do not rename or restructure them. |
| 2 | `docs/plans/OPORD-FORMAT.md` | **TEMPLATE-COPY** | Copy verbatim. Co-dependent with #1 and #3. |
| 3 | `.claude/commands/task.md` changes | **CUSTOMIZE** | Merge three additions into your copy (exact lines below). Includes the proword convention, which the format files' naming scheme (`conop_<PROWORD>_<slug>.md`) requires. |
| 4 | Deep-modules discipline (`CLAUDE.md`) | **CUSTOMIZE** | One sentence merged into your Simplicity First principle (below). Independent of #1–3; skip cleanly if unwanted. |
| 5 | `python-prototyper.md` Step 4d | **CONDITIONAL** | Only if your repo carries this agent. Copy Step 4d from tacsop's file. |
| 6 | Retrospective reports | **NO ACTION** | Read the one about your repo (table below) — the evidence is your own session docs. |

### Action required (Part 2)

1. Copy `docs/plans/CONOP-FORMAT.md` and `docs/plans/OPORD-FORMAT.md` from tacsop
   into your `docs/plans/` (create the directory if absent).
2. In your `.claude/commands/task.md`, merge:
   - Under the `promote` subcommand, replace
     `- If the user agrees, create a skeleton document in docs/plans/`
     with:
     ```
     - If the user agrees, create a skeleton document in `docs/plans/` using the template in `docs/plans/CONOP-FORMAT.md` (or `docs/plans/OPORD-FORMAT.md`)
     - The plan must exist and reach Approved **before** its first wave launches — a plan written after the build documents, it does not plan
     - Every exit/kill-criterion in the plan carries a named owner; an ownerless criterion defers itself indefinitely
     ```
   - Append to the Level 3 and Level 4 **Format** lines respectively:
     `Template and section standard: docs/plans/CONOP-FORMAT.md.` /
     `Template and section standard: docs/plans/OPORD-FORMAT.md.`
   - If your copy predates the proword convention (no `## Prowords` section), copy
     that whole section from tacsop's `task.md`.
3. (Optional, #4) Append to your CLAUDE.md Simplicity First principle:
   > Prefer deep modules — small interfaces hiding meaningful implementation — over
   > shallow ones; before declaring an interface done, ask whether each parameter is
   > load-bearing or whether the function could derive it from one it already has.
4. (Conditional, #5) If you carry `python-prototyper.md`, copy Step 4d (the
   10-second load-bearing-parameter check after GREEN) from tacsop's file.
5. Read your repo's retrospective report — the format additions cite your own
   sessions as evidence:

   | Repo | Report |
   |---|---|
   | magic-movies | `tacsop/docs/reviews/20260717_planning_retrospective_magic_movies.md` |
   | swimming-analytics | `tacsop/docs/reviews/20260717_planning_retrospective_swimming_analytics.md` |
   | elephant-graveyard | `tacsop/docs/reviews/20260717_planning_retrospective_elephant_graveyard.md` |
   | tactics-game | `tacsop/docs/reviews/20260717_planning_retrospective_tactics_game.md` |
   | (all others) | Skim any report's SUMMARY — the failure shapes are general. |

### Rollback (Part 2)

Everything in Part 2 is additive. Delete the two FORMAT files, revert the `task.md`
merge, and drop the CLAUDE.md sentence to return to prior state; no artifact
changes runtime behavior. Existing plans are untouched either way.

---

### Part 3 — Writing & Testing Doctrine: prose-style skill, property-based testing, Apache-2.0 relicense (additive)

Three additions authored 2026-07-19/20, each validated in the hub before shipping.

**Writing style.** A new Level 0 skill, `writing-simple-and-direct` (v1.0.0, five
files), pins the house prose style: eight kernel rules distilled from Barzun's
*Simple and Direct*, each with a test that catches its violation; six before/after
example pairs; a four-pass review protocol for prose artifacts; and a per-repo
adoption guide. The kernel also lands as a CLAUDE.md "Prose Style" section and the
cruft-word list as a LANGUAGE.md section; the skill's `ADOPTION.md` walks through
both plus a one-line code-reviewer checklist addition. Before shipping, the entire
hub corpus was swept to comply (~150 edits across 31 files, verification and flags
in `docs/reviews/20260719_writing_style_sweep.md`), so the files you copy are their
own exemplars. Two boundary conditions, restated from `ADOPTION.md` so nobody
over-applies the rules: existing docs are grandfathered (session docs and reviews
are records; leave them), and document schemas outrank style (never cut a required
section to save tokens).

**Testing depth.** `shift-left-testing` goes 2.0.0 → 2.1.0 with four sidecars:
`PROPERTY-BASED.md` (invariant testing with Hypothesis), `NUMERIC.md` (float
tolerances, numpy/pandas assertions, injectable randomness, stochastic code),
`REGRESSION.md` (characterization pins for legacy code, golden files, the bless
workflow), and `SCRIPTS.md` (testing CLIs and filesystem scripts, dry-run as a
contract, widening the audit-hook perimeter to `scripts/`). Validated by use: the
hub's first property suite (`tests/unit/test_from_yaml_properties.py`, five tests)
closed a standing decision-science test gap, and strategy design alone surfaced a
real crash bug (Known Issue below). That is the sidecar doing exactly what it
promises before it ever left the building.

**License.** The hub relicensed from GPL v3 to Apache-2.0. The hub had never been
distributed, so no copyleft obligations ever attached; the sole author relicensed
cleanly. Template content you copy from the hub is now Apache-2.0: attribution and
license retention (§4) instead of copyleft, plus an explicit patent grant.

### Adoption-Mode Table (Part 3)

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `.claude/skills/writing-simple-and-direct/` (5 files) | **TEMPLATE-COPY** | Copy the directory, then run its `ADOPTION.md`: CLAUDE.md kernel block, LANGUAGE.md cruft list, code-reviewer checklist line. Applies without adaptation. |
| 2 | `.claude/skills/shift-left-testing/` 2.1.0 | **TEMPLATE-COPY** | Copy the four new sidecars plus the updated `SKILL.md` (new sidecar index, `tests/golden/` + `tests/scripts/` in the layout). Fully additive over 2.0.0. |
| 3 | Property-testing plumbing | **PATCH-COPY** | `hypothesis>=6.0` in dev extras; `.hypothesis/` in `.gitignore`; the profile block from `tests/conftest.py` (50 examples locally, 300 in CI, switched by the `CI` env var). Needed only when you write your first property test. |
| 4 | Copies of other Level 0 skills | **NO ACTION** (or refresh) | A style-only sweep touched every skill file; meaning is unchanged. Refresh copies whenever convenient. |
| 5 | `LICENSE` | **MANUAL** | Informational for repos with their own license. If you copied the hub's old GPL stub verbatim, replace it (with the new Apache-2.0 text or your own choice). |

### Known Issue (repos carrying `decision_science`)

`value_functions.exponential()` raises `ZeroDivisionError` for nonzero `|rate|`
below ~2.2e-16, where `1 - e^(-rate)` rounds to exactly 0.0. The input satisfies
the documented contract ("rate must be nonzero"); the crash is real. Repro:
`exponential(50.0, low=0.0, high=100.0, rate=1e-17)`. Found during property-test
strategy design, 2026-07-20. The upstream fix is pending a design call (extend the
zero guard vs. fall back to linear); until it ships, avoid effectively-zero rates.

### Rollback (Part 3)

Everything is additive or informational. Delete the skill directory and revert the
CLAUDE.md, LANGUAGE.md, and code-reviewer additions to drop the style doctrine.
Delete the four sidecars and re-copy the prior `SKILL.md` to return shift-left-testing
to 2.0.0. The relicense requires no downstream action at all.

---

## 2026-06-28: Line-Ending Guard — `.gitattributes` as Doctrine

`utils` has shipped a `.gitattributes` (`* text=auto eol=lf` + explicit text/binary
rules) for a while, but it was never recorded as doctrine, so most downstream repos
never adopted it. The gap surfaced concretely when `magic-movies` — developed across
both Windows and WSL — accumulated a phantom "uncommitted change" of 948 insertions /
948 deletions that was **pure CRLF↔LF churn**, not real work: `core.autocrlf` was unset
and no `.gitattributes` existed, so git saw every line as modified each time the tree
bounced between platforms.

This entry records `.gitattributes` as a propagatable artifact and the one-time
renormalization step that should accompany it.

### Files (utils — already present, now recorded as doctrine)

```
.gitattributes
```

### Adoption-Mode Table

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `.gitattributes` | **TEMPLATE-COPY** | Copy `utils/.gitattributes` verbatim. Extend the binary list if your repo tracks asset types not already covered (`*.mp4`, `*.wasm`, `*.ttf`, etc.) — `text=auto` auto-detects binaries, but explicit rules are belt-and-braces. |

### Action required

1. Copy `utils/.gitattributes` into your repo root.
2. Renormalize existing files so the working tree and index agree with the new rules:
   ```bash
   git add .gitattributes
   git add --renormalize .
   git status        # review — only files currently committed with CRLF should change
   git commit -m "[infra] Add .gitattributes — normalize line endings to LF (CRLF guard)"
   ```
   The renormalize diff is usually small (the few files that happened to be committed with
   CRLF). If it is unexpectedly large, inspect before committing — a misdetected binary is
   the thing to rule out.
3. Verify `core.autocrlf` is not fighting the attributes: with `.gitattributes` present,
   `eol=lf` wins regardless of the local `core.autocrlf` setting, so no per-machine config
   is required.

### Why this matters cross-platform

The failure mode is silent: nothing errors, but every Windows↔Linux hop produces a
full-file "change" that masks real diffs, pollutes `git status`, and can swallow genuine
edits in the noise (as nearly happened in `magic-movies`). The `.gitattributes` guard makes
LF the single source of truth in the repo; platforms check out and commit through it
transparently.

### Rollback

`.gitattributes` is inert to delete — remove the file to revert to platform-default
behavior. Any renormalization commit is a normal content commit and can be reverted like
any other.

---

## 2026-06-28: Branching Doctrine — Short-Lived Topic Branches by Work Shape

A new skill codifies the branching policy that emerged from MEGAN's CONOP-002 §4.2
retrospective: **branch on the shape of the work, not on a permanent partition of the
codebase.** This replaces the older "one permanent branch per domain" convention
(`dev-safety`, `dev-ui`, `dev-perception`, …), which forced constant resyncing against
`main` for no review benefit.

### Files added (utils)

```
.claude/skills/using-topic-branches/SKILL.md
```

### Files changed (utils)

```
CLAUDE.md   (new "Branching" Development Principle, references the skill)
```

### The policy

- **Lead-only doc / ADR / small-refactor work** → land directly on `main`. No branch
  overhead where there is no audit gate and no parallel contributors.
- **Team-deployed or multi-agent code work with an audit gate** → a short-lived
  `topic/<scope>-<slug>` branch, created at the start, merged via merge-commit at the gate,
  and **deleted local + origin immediately after merge**. Lifetime: hours to one session.
- **Parallel contributors on independent files within one task** → share the same topic
  branch (file ownership prevents conflict); do not split per-contributor.

The skill also includes an **auditing standing branches** procedure — classify every
non-`main` branch by its `ahead`/`behind` count vs `origin/main`, and act by `ahead` only
(`ahead==0` → safe delete; `ahead>0, behind==0` → main is behind, merge then delete;
diverged → investigate before deciding). **Never delete a branch on `behind` alone.**

### Adoption-Mode Table

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `.claude/skills/using-topic-branches/` | **TEMPLATE-COPY** | Skill mechanics are universal — copy the directory verbatim. The policy is git-workflow doctrine, not project-specific. |
| 2 | `CLAUDE.md` "Branching" principle | **TEMPLATE-COPY** | Copy the wording template into your Development Principles section. No path substitution needed (the skill path is the same in every repo). |

### Action required

1. Copy `.claude/skills/using-topic-branches/` verbatim into your repo.
2. Add the "Branching" Development Principle to your `CLAUDE.md` (wording template in the
   utils CLAUDE.md).
3. **Audit your own standing branches** with the procedure in the skill. Retire fully-merged
   branches; merge-then-delete any branch `main` is behind; investigate diverged branches
   before touching them.

### Rollback

The skill is docs only — no code consumes it. Delete the directory and revert the CLAUDE.md
principle to remove it. Adopting it changes no existing branches; it only changes how new
work is branched going forward.

---

## 2026-05-29: Windows-Portability Patch

A small, bug-fix-only follow-up to the 2026-05-19 cycle. `heimdall-darkroom` adopted the cycle on 2026-05-28 as the first Windows-native downstream and surfaced three Windows-only failure modes in artifacts shipped by that propagation. All three are patched in this entry; no new doctrine, no new artifacts.

**Adoption mode for downstreams**: PATCH-COPY. If you adopted the 2026-05-19 cycle but haven't yet run on Windows, you can ignore this entry. If you have run on Windows (or expect to), the cleanest path is to:

1. Re-copy `.claude/hooks/post-tool-shift-left-audit.sh` from utils (the path-normalization fix is one new line near the top; verify the comment block then take the file as-is).
2. Re-copy `scripts/adopt_doctrine.py` if you keep a local copy (the UTF-8 stdio fix is at the top of the imports block).
3. If you scaffolded `src/<pkg>/utils/logger.py` from the utils template, port the broader `except` clause: add `ZoneInfoNotFoundError` to the import and to the except tuple.
4. Append `tzdata; sys_platform == 'win32'` to your `pyproject.toml` base dependencies if not already present.

`heimdall-darkroom` applied all four locally on 2026-05-28 (before this upstream patch existed); see [`heimdall-darkroom` `docs/sessions/20260528_doctrine_adoption.md`](https://github.com/jhutchison0/heimdall-darkroom/blob/main/docs/sessions/20260528_doctrine_adoption.md) for the discovery context.

### The three fixes

| # | File | Symptom | Fix |
|---|---|---|---|
| 1 | `scripts/adopt_doctrine.py` | `UnicodeEncodeError` on first invocation: `'charmap' codec can't encode character '→' in position 61`. The helper crashes before doing any work. | Reconfigure `sys.stdout` / `sys.stderr` to UTF-8 at module-load time. Fail-soft (wrapped in `try/except` for streams that don't support reconfigure). |
| 2 | `.claude/hooks/post-tool-shift-left-audit.sh` | Hook fires (exit 0) but does nothing — `case "$file_path" in */src/<pkg>/*.py)` cannot match `C:\…\src\<pkg>\foo.py`. Silent no-op for every Edit/Write on Windows. | Normalize backslashes: `file_path=${file_path//\\//}` after the jq parse. Also clarify in the trailing comment that `*` in case patterns matches across slashes, so subdirectories are covered. |
| 3 | `src/myproject/utils/logger.py` + `pyproject.toml` | On Windows + Python 3.9+ without `tzdata`, `ZoneInfo("America/Chicago")` raises `ZoneInfoNotFoundError` (a `KeyError` subclass — NOT `ImportError`/`ValueError`). The existing except clause didn't catch it; every caller of `get_logger()` crashed at import time. | Import `ZoneInfoNotFoundError` and add it to the `except` tuple. Also add `tzdata; sys_platform == 'win32'` to `pyproject.toml` base deps so timezones actually work, with the fallback as a belt-and-braces guard. |

### Bonus: two pre-existing Windows test failures fixed

While running the utils test suite to validate the fixes, two pre-existing Windows-only test failures surfaced in `tests/unit/test_adopt_doctrine.py`:

| Test | Symptom | Fix |
|---|---|---|
| `TestPlanCopies::test_sources_rooted_at_upstream` | `assert str(src).startswith("/fake/upstream/")` fails because `Path("/fake/upstream") / "x"` produces `\fake\upstream\x` on Windows. | Use `Path(src).is_relative_to(upstream)` instead of string-prefix comparison. |
| `TestSubstituteHook::test_executable_bit_preserved` | NTFS has no POSIX `+x` bit; `chmod(0o755)` is a no-op. The assertion `dst.stat().st_mode & 0o111` is `0`. | Skip on `sys.platform == "win32"` with an explanatory reason. |

### Files changed

```
scripts/adopt_doctrine.py                              (UTF-8 stdio reconfigure block at top of imports)
.claude/hooks/post-tool-shift-left-audit.sh            (path normalization + clarifying comment)
src/myproject/utils/logger.py                          (import ZoneInfoNotFoundError + add to except)
pyproject.toml                                         (+ tzdata; sys_platform == 'win32')
tests/unit/test_logger.py                              (+ TestTimezoneFallback regression test)
tests/unit/test_adopt_doctrine.py                      (Path.is_relative_to + skipif on win32)
```

### Verification

- Full utils logger + adopt_doctrine test suites: **45 passed, 1 skipped** (the +x test, now correctly skipping on Windows).
- `adopt_doctrine.py --dry-run` from a Windows shell **without** `PYTHONUTF8=1`: succeeds and prints `→` correctly.
- Patched hook fed a Windows backslash `file_path`: matches `*/src/myproject/*.py` and exits cleanly. No-op behavior on out-of-scope paths preserved.

### Provenance

- Discovery: `heimdall-darkroom` 2026-05-28 doctrine-adoption session — see [`docs/sessions/20260528_doctrine_adoption.md`](https://github.com/jhutchison0/heimdall-darkroom/blob/main/docs/sessions/20260528_doctrine_adoption.md) §6.
- Fix and propagation: this entry, utils 2026-05-29.
- The `tzdata` + `ZoneInfoNotFoundError` portion has actually been a known issue in heimdall-darkroom since 2026-04-22 (Phase 1 pivot session) but was never propagated upstream until now. Carried in heimdall's task list as "port back to utils template" for over a month.

---

## 2026-05-19: Doctrine Artifact Buildout + Skills Framework v2 + TDD Enforcement Hook

This is the largest propagation cycle to date. It bundles work from three sessions:
the doctrine-artifact buildout (LANGUAGE.md, CONTEXT.md, ADR system, propagation protocol),
the Wave 2 refactor of three legacy single-file skills into Anthropic's December 2025 open-standard directory form,
and the Pass 4 enforcement-layer build — a deterministic PostToolUse hook that audits shift-left-testing discipline on every Write/Edit to production code.

The cycle also catches up on the **Python 3.11 minimum bump** that was committed 2026-04-21 but never propagated.

Read this entry in full before merging anything — adoption mode varies per artifact.

### Files added (utils)

```
LANGUAGE.md
CONTEXT.md
docs/propagation-protocol.md
docs/session-doc-format.md
docs/adr/ADR-FORMAT.md
docs/adr/.gitkeep
docs/adr/0001-directory-form-mandatory-for-new-skills.md
.claude/skills/maintaining-ubiquitous-language/SKILL.md
.claude/skills/maintaining-project-context/SKILL.md
.claude/skills/recording-architecture-decisions/SKILL.md
.claude/skills/shift-left-testing/                       (directory replaces former single-file)
  SKILL.md
  TIERS.md
  PATTERNS.md
  MOCKS.md
  FIXTURES.md
  VERTICAL-SLICING.md
  ENFORCEMENT.md
  CI.md
  ANTIPATTERNS.md
.claude/skills/configuration-management/                 (directory replaces former single-file)
  SKILL.md + 5 sidecars
.claude/skills/python-venv-management/                   (directory replaces former single-file)
  SKILL.md + 2 sidecars
.claude/hooks/post-tool-shift-left-audit.sh              (executable; A5 PostToolUse audit)
scripts/adopt_doctrine.py                                (optional downstream-side adoption helper; see §23)
tests/unit/test_adopt_doctrine.py                        (35 tests for the helper)
```

### Files changed (utils)

```
CLAUDE.md                                                (Shift-Left Testing principle strengthened to test-first vertical-slice; hook reference)
.claude/agents/python-prototyper.md                      (workflow inverted to test-first; stale pillars.md ref repointed)
.claude/skills/SKILLS_FRAMEWORK.md                       (v2 — Anthropic Dec 18 open standard; YAML frontmatter; directory form; progressive disclosure)
.claude/README.md                                        (skills tree refreshed)
.claude/commands/session-end.md                          (Step 5 slimmed to reference docs/session-doc-format.md)
.claude/settings.json                                    (PostToolUse hook block added)
.gitignore                                               (added docs/design/hold/ and .claude/audits/)
pyproject.toml                                           (Python 3.11 min — bumped 2026-04-21)
config/project.yaml                                      (python.min_version 3.11 — bumped 2026-04-21)
```

### Files deleted (utils)

```
.claude/skills/session-end.md                            (reference content demoted to docs/session-doc-format.md)
.claude/skills/shift-left-testing.md                     (replaced by directory form)
.claude/skills/configuration-management.md               (replaced by directory form)
.claude/skills/python-venv-management.md                 (replaced by directory form)
```

### Files renamed (utils)

```
.claude/settings.local.json → .claude/settings.json      (Anthropic convention; settings.local.json now per-user override only, gitignored)
```

---

### Adoption-Mode Table (master)

Each artifact in this propagation has one of four adoption modes. Downstream maintainers — **read this table before merging anything**.

| # | Artifact | Mode | Notes |
|---|---|---|---|
| 1 | `LANGUAGE.md` (repo root) | **CUSTOMIZE** | Copy as starter template, then rewrite per your project's domains. Our terms (decision-science, escalation ladder, governance) likely do not apply verbatim. |
| 2 | `.claude/skills/maintaining-ubiquitous-language/` | **TEMPLATE-COPY** | Skill mechanics are universal. |
| 3 | `CONTEXT.md` (repo root) | **CUSTOMIZE** | Copy as starter template, then rewrite per your project's identity, mission, and constraints. The structure stays; the content is yours. |
| 4 | `.claude/skills/maintaining-project-context/` | **TEMPLATE-COPY** | Skill mechanics are universal. |
| 5 | `docs/adr/ADR-FORMAT.md` + `.gitkeep` | **TEMPLATE-COPY** | Format spec is universal. |
| 6 | `.claude/skills/recording-architecture-decisions/` | **TEMPLATE-COPY** | Skill mechanics are universal. |
| 7 | `docs/adr/0001-directory-form-mandatory-for-new-skills.md` | **TEMPLATE-COPY-WITH-NOTE** | The decision applies downstream because you're adopting the same SKILLS_FRAMEWORK v2. Copy it as your own ADR-0001 (or as ADR-NNNN if you already have ADRs). Update Decision-maker(s) field to attribute the local adoption. |
| 8 | `.claude/skills/SKILLS_FRAMEWORK.md` v2 | **TEMPLATE-COPY** | Universal. The military/civilian vocab crosswalk section stays as-is; you choose which side to use locally. |
| 9 | `.claude/skills/shift-left-testing/` (entire directory) | **TEMPLATE-COPY** | Replaces any prior single-file `shift-left-testing.md`. Discipline universal; sidecar paths reference `src/myproject/` only inside the hook script (see #12). |
| 10 | `.claude/skills/configuration-management/` | **TEMPLATE-COPY** | Replaces any prior single-file `configuration-management.md`. |
| 11 | `.claude/skills/python-venv-management/` | **TEMPLATE-COPY** | Replaces any prior single-file `python-venv-management.md`. |
| 12 | `.claude/hooks/post-tool-shift-left-audit.sh` | **CUSTOMIZE** | Copy script, **substitute the package path glob** `*/src/myproject/*.py` to match your repo's package (e.g., `*/src/yourpkg/*.py`). Everything else is portable. Run `chmod +x` after copying. |
| 13 | `.claude/settings.json` `hooks.PostToolUse` block | **TEMPLATE-COPY** | Merge into your existing settings.json (do not replace; preserve your env/permissions). Uses `$CLAUDE_PROJECT_DIR` so the path is portable. |
| 14 | `.gitignore` lines: `.claude/audits/` and `docs/design/hold/` | **TEMPLATE-COPY** | Append to your existing `.gitignore`. |
| 15 | `docs/session-doc-format.md` | **TEMPLATE-COPY** | Universal session-doc format spec. |
| 16 | `.claude/skills/session-end.md` **deletion** | **CONDITIONAL** | Only if your repo currently has it. Move the reference content out first (we put it in `docs/session-doc-format.md`); then delete. |
| 17 | `.claude/commands/session-end.md` (slimmed) | **TEMPLATE-COPY** | Replaces your existing one; Step 5 now references `docs/session-doc-format.md` instead of duplicating the body. |
| 18 | `docs/propagation-protocol.md` | **SKIP-OR-CUSTOMIZE** | Only relevant to **propagation hubs** (currently `utils` only). Skip unless your repo also serves doctrine to other repos. |
| 19 | Python 3.11 min bump (`pyproject.toml`, `config/project.yaml`, CLAUDE.md) | **TEMPLATE-COPY** | This is the catch-up from 2026-04-21. Verify your CI/local env supports 3.11 before merging. |
| 20 | `.claude/agents/python-prototyper.md` (test-first workflow + pillars ref fix) | **CUSTOMIZE** | Workflow change is universal, but the agent file contains hard-coded `src/myproject/` references in the Project Layout and Scope sections. Substitute to your package name. If you've previously customized this agent locally, diff first — see §9. |
| 21 | `CLAUDE.md` Development Principles strengthening (test-first vertical-slice) | **CUSTOMIZE** | Copy the wording template; adapt path references to your repo's package layout. |
| 22 | `.claude/settings.local.json` → `.claude/settings.json` rename | **TEMPLATE-COPY** | Anthropic convention. Your existing settings.local.json (if any) becomes per-user-override-only, gitignored. |
| 23 | `scripts/adopt_doctrine.py` + tests | **TEMPLATE-COPY** | Optional adoption helper. Automates the mechanical parts of this bundle (verbatim copies, hook substitution, settings.json merge, .gitignore append). See §23 for the action and the explicit non-goals. |

---

### 1. LANGUAGE.md and the `maintaining-ubiquitous-language` skill

A glossary of project-specific terms lives at the repo root. One-line definitions, no synonyms. Companion to `CONTEXT.md` (narrative) and `config/project.yaml` (structured state).

**Pattern source**: Matt Pocock's `grill-with-docs` skill (`CONTEXT-FORMAT.md`). Adopted as a pattern, **not adopted verbatim** — Pocock's vocabulary disambiguates TypeScript-ecosystem overloads. Yours needs to disambiguate the terms your project actually uses.

**Skill**: `.claude/skills/maintaining-ubiquitous-language/` is invoked when a new term emerges, when a definition becomes stale, or when an agent uses two words for the same thing.

**Action required**:
1. Copy `.claude/skills/maintaining-ubiquitous-language/` verbatim into your repo.
2. Copy `LANGUAGE.md` as a **starter template**. Replace the example sections (Decision Science, Agent Framework, Escalation Ladder, Governance & Propagation, Workflow Artifacts, Vocabulary Crosswalk, Anti-Glossary) with your project's actual domains. Keep the meta-structure: bold term, one-line definition, `_Avoid:_` synonyms when ambiguity exists.
3. Add LANGUAGE.md to your CONTEXT.md reading order (see §2) once both exist.

---

### 2. CONTEXT.md and the `maintaining-project-context` skill

A one-page narrative of the project's identity, mission, current state, and key constraints. Uses terms defined in LANGUAGE.md. For machine-readable state, defers to `config/project.yaml`.

**Pattern source**: Pocock's `CONTEXT-FORMAT.md`. Same adoption stance as LANGUAGE.md — pattern only, content yours.

**Skill**: `.claude/skills/maintaining-project-context/` — invoked at the start of significant new work, when the project mission changes, or when an agent needs to orient quickly.

**Action required**:
1. Copy `.claude/skills/maintaining-project-context/` verbatim.
2. Copy `CONTEXT.md` as a **starter template**. Replace Identity/Mission/Current State/Constraints/Key Relationships/Reading Order with your project's. Preserve the "Distinguishing This File from Adjacent Artifacts" table at the bottom — it prevents content from drifting into the wrong file.
3. Wire CONTEXT.md into onboarding: it should be the first file agents and humans read. Update your README (or equivalent) to point at it.

---

### 3. ADR System

Architecture Decision Records live at `docs/adr/NNNN-slug.md`. The triple-filter gate is the central discipline: write an ADR **only when** the decision is (1) hard to reverse, (2) surprising without context, and (3) the result of a real trade-off between genuine alternatives. If any one filter fails, document it elsewhere (commit message, session doc, inline comment).

**Pattern source**: Pocock's `ADR-FORMAT.md`. The triple filter is adopted verbatim.

**Files**:
- `docs/adr/ADR-FORMAT.md` — the template and the gate.
- `docs/adr/.gitkeep` — preserves the empty directory.
- `docs/adr/0001-directory-form-mandatory-for-new-skills.md` — first ADR, exercises the format. Captures the same decision you adopt when you adopt SKILLS_FRAMEWORK v2 (§5), so propagating it gives downstream a worked example and a real anchoring decision.
- `.claude/skills/recording-architecture-decisions/SKILL.md` — invocation rules; refuses to write an ADR when any filter fails.

**Action required**:
1. `mkdir -p docs/adr` and copy `docs/adr/ADR-FORMAT.md`. (Once ADR-FORMAT.md is in the directory it preserves itself in git — no `.gitkeep` needed. Copy `.gitkeep` only if you intend to leave the directory empty for a while.)
2. Copy `.claude/skills/recording-architecture-decisions/` verbatim.
3. Copy `docs/adr/0001-directory-form-mandatory-for-new-skills.md` as your own ADR-0001 (or as ADR-NNNN if you already have ADRs). Edit the Decision-maker(s) field to attribute local adoption. The decision applies in your repo because you're adopting SKILLS_FRAMEWORK v2 — so this is genuinely your decision too.
4. Add `docs/adr/` to your CONTEXT.md reading order (between propagation-protocol.md and docs/sessions/).

---

### 4. Propagation Protocol (`docs/propagation-protocol.md`)

Formalizes the doctrine-propagation governance: what counts as doctrine, the 5-question evaluation gate, batching rules, the cycle anatomy, downstream discovery, append mode, and rollback.

**Adoption mode: SKIP-OR-CUSTOMIZE.** This file is relevant only to repos that serve doctrine to other repos. Currently only `utils` does this. Most downstream repos can ignore it.

If your repo is also a hub (you propagate doctrine to other repos), copy `docs/propagation-protocol.md` and customize the "Discoverable Roster" section to match your downstream set.

---

### 5. SKILLS_FRAMEWORK v2 + Directory-Form Mandate

`.claude/skills/SKILLS_FRAMEWORK.md` is rewritten to v2. The substantive changes:

- **YAML frontmatter spec** — every SKILL.md starts with `name`, `description`, `version` (and optional `allowed-tools`, `model`, `memory`). Aligns with Anthropic's Dec 2025 open standard.
- **Directory form is now the default and mandatory for all new skills** — see ADR-0001. A skill is a directory containing `SKILL.md` and optional sidecar files. Single-file form is retained only for skills already migrated.
- **Progressive disclosure rule** — SKILL.md is the entry point and stays small (target <150 lines). Topical content moves into sidecar files (`PATTERNS.md`, `MOCKS.md`, etc.) loaded on demand. This protects the context budget when many skills exist.
- **Military/civilian vocabulary crosswalk** — for content that crosses to external audiences, substitute the civilian terms (PCC → pre-commit-check, OPORD → operations-order, etc.). Internal files keep military terms. Crosswalk lives in LANGUAGE.md.

Three legacy single-file skills were refactored to directory form in this cycle:

| Skill | Before | After | Sidecars |
|---|---|---|---|
| `shift-left-testing` | 1242 lines, single file | 9 files total: SKILL.md (103 lines) + 8 sidecars | TIERS, PATTERNS, MOCKS, FIXTURES, **VERTICAL-SLICING**, **ENFORCEMENT**, CI, ANTIPATTERNS |
| `configuration-management` | 1533 lines, single file | 6 files total: SKILL.md (88 lines) + 5 sidecars | STRUCTURE-AND-FILES, LOADER, SECRETS, VALIDATION, TESTING-AND-PATTERNS |
| `python-venv-management` | 623 lines, single file | 3 files total: SKILL.md (105 lines) + 2 sidecars | SETUP, TROUBLESHOOTING |

**Action required**:
1. Copy `.claude/skills/SKILLS_FRAMEWORK.md` verbatim — this is the spec for everything else in this section.
2. For each of the three legacy skills above, if your repo has the single-file version: **diff your local file against `utils` first** to surface customizations:
   ```bash
   diff .claude/skills/<name>.md <utils-path>/.claude/skills/<name>/SKILL.md
   diff .claude/skills/<name>.md <utils-path>/.claude/skills/<name>/PATTERNS.md     # repeat per sidecar
   ```
   If you find local-only content (project-specific examples, repo-customized commands, embedded fixture paths), copy it into the appropriate sidecar of the new directory form before deleting your single-file. Then: delete the old `.claude/skills/<name>.md`; copy the entire `.claude/skills/<name>/` directory in its place.
3. Copy ADR-0001 (§3) as your local record of the mandatory-directory-form decision.

---

### 6. Shift-Left-Testing Discipline: Vertical Slicing (`VERTICAL-SLICING.md`)

A new sidecar in the shift-left-testing skill encodes the **tracer-bullet TDD** discipline: write a failing test, then the minimum implementation that passes it, then move to the next slice. Adapted from Pocock's `tdd` skill; the rules are quoted verbatim where attributed.

The failure mode this prevents is the "horizontal slice" — writing all tests first, then all implementation — which looks productive but produces brittle code shaped by what the author *thought* the tests would need, not by what each test actually required.

**Rules** (verbatim from Pocock):
- One test at a time. Only enough code to pass the current test.
- Don't anticipate future tests.
- Never refactor while RED. Get to GREEN first. Refactor only when all tests pass.

**Action required**:
1. Already included if you adopt the new `.claude/skills/shift-left-testing/` directory (§5 step 2).
2. Surface the discipline in agent instructions — the `python-prototyper` agent update (§9) does this; mirror similar changes in any other code-writing agents you have.

---

### 7. Shift-Left-Testing Enforcement Layer (`ENFORCEMENT.md` + PostToolUse Hook)

**This is the most novel artifact in the cycle.** The skill alone is *probabilistic* — an agent may or may not invoke it on any given turn. The enforcement layer adds *deterministic* mechanisms so the discipline survives contact with agents that don't read the skill.

The enforcement gradient (documented in `.claude/skills/shift-left-testing/ENFORCEMENT.md`):

| Layer | Determinism | Blocking? | Mechanism |
|---|---|---|---|
| 1. The skill itself | Probabilistic | No | Agent reads when relevant |
| 2. CLAUDE.md Development Principle | Probabilistic | No | Agent reads at session start |
| 3. `python-prototyper.md` workflow | Probabilistic | No | Agent definition prescribes order |
| 4. **PostToolUse audit hook** | **Deterministic** | **No (logs + warns)** | Harness runs after every Write/Edit |
| 5. Stop hook diff audit | Deterministic | No | Not configured (next iteration) |
| 6. PreToolUse block hook | Deterministic | Yes | **Intentionally not configured** — see ENFORCEMENT.md |

Layers 1–4 are what this propagation ships. Layer 6 (hard-block) was MAUT-evaluated and rejected because false-positive risk on legitimate refactors / config edits outweighs the determinism gain. See `docs/reviews/20260519_pass4_enforcement_maut.md` if you want the analysis.

**What the hook does** (`.claude/hooks/post-tool-shift-left-audit.sh`):
- Fires after every `Write` or `Edit`.
- Exits silently for tools that aren't Write/Edit, paths outside `src/myproject/**/*.py`, and `__init__.py` / `conftest.py` / `test_*.py`.
- For everything else: looks for a `tests/**/test_<basename>.py` partner via `find`.
- If no partner: appends `MISSING_TEST` to `.claude/audits/shift-left-violations.log` and emits a one-line stderr warning the agent sees.
- If partner: appends `OK_TEST_EXISTS` log line.
- **Never blocks**. `set -uo pipefail` (not `-e`); always exits 0.

**Action required**:
1. Create `.claude/hooks/` directory in your repo.
2. Copy `.claude/hooks/post-tool-shift-left-audit.sh`.
3. **Substitute the path glob** — find this block in the script:
   ```bash
   case "$file_path" in
       */src/myproject/*.py) ;;
       *) exit 0 ;;
   esac
   ```
   Replace `myproject` with your repo's package name. **Bash `case` syntax notes**:
   - Single package: `*/src/yourpkg/*.py)`
   - Wildcard (any package under `src/`): `*/src/*/*.py)`
   - Multi-package alternation: list the full patterns joined by `|` — **not** parentheses. Correct: `*/src/pkg1/*.py|*/src/pkg2/*.py)`. **Wrong**: `*/src/(pkg1|pkg2)/*.py)` — that is regex/extglob syntax and is invalid in a plain bash `case` pattern. The script does not enable `extglob`, so the wrong form silently never matches and the hook does nothing (it still `exit 0`s, so you get no error — just empty audit logs).
4. `chmod +x .claude/hooks/post-tool-shift-left-audit.sh`
5. **Merge the hook block into your `.claude/settings.json`** — DO NOT REPLACE the whole file. Preserve your existing `env`, `permissions`, and any other top-level keys.

   **Case A — your settings.json has no `hooks` block**: add this as a new top-level key alongside `env` / `permissions`:
   ```json
   "hooks": {
     "PostToolUse": [
       {
         "matcher": "Write|Edit",
         "hooks": [
           {
             "type": "command",
             "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-shift-left-audit.sh",
             "timeout": 10
           }
         ]
       }
     ]
   }
   ```

   **Case B — your settings.json already has a `hooks` block** (e.g., you already configured a formatter or logger):

   - If your existing `hooks.PostToolUse` array does NOT include a `"matcher": "Write|Edit"` entry: append the entry object above (the inner object containing `matcher` and `hooks`) to the existing PostToolUse array.
   - If your existing `hooks.PostToolUse` ALREADY has a `"matcher": "Write|Edit"` entry: append the `{ "type": "command", "command": "$CLAUDE_PROJECT_DIR/...", "timeout": 10 }` object to that matcher's inner `hooks` array. Multiple commands run sequentially under the same matcher.
   - Validate after editing with `jq -e '.hooks.PostToolUse[] | select(.matcher == "Write|Edit") | .hooks[] | select(.command | endswith("post-tool-shift-left-audit.sh"))' .claude/settings.json` — exit 0 + prints your command = correct merge.
6. Add `.claude/audits/` to your `.gitignore` (the log file lives there).
7. Copy `.claude/skills/shift-left-testing/ENFORCEMENT.md` (included if you copy the whole directory in §5).
8. **Verify the hook is installed and fires**:
   ```bash
   # (a) jq is required by the hook script — verify it's available:
   command -v jq || echo "INSTALL JQ: the hook script needs it to parse stdin"

   # (b) The script must be executable. Windows / git config core.fileMode=false can lose this:
   test -x .claude/hooks/post-tool-shift-left-audit.sh || chmod +x .claude/hooks/post-tool-shift-left-audit.sh

   # (c) Pipe-test the script directly (simulates what the harness will send):
   echo '{"tool_name":"Edit","tool_input":{"file_path":"'"$PWD"'/src/<yourpkg>/<some_existing_file>.py"}}' \
     | .claude/hooks/post-tool-shift-left-audit.sh; echo "exit=$?"
   # Expected: exit=0; if the test partner exists, no stderr; if not, a [shift-left-audit] warning.

   # (d) End-to-end: Edit a real file in src/<yourpkg>/ via Claude Code, then:
   tail -1 .claude/audits/shift-left-violations.log
   # Expected: a fresh entry timestamped within the last minute.
   ```
   If (d) shows no fresh entry but (c) worked, the settings watcher hasn't reloaded — open the `/hooks` menu in Claude Code to refresh, or restart the session.
9. **Per-developer override**: anyone who wants to disable the hook can override in `.claude/settings.local.json` (gitignored). The shipped `.claude/settings.json` is team-wide.

**What the hook does NOT catch** (be honest with your team):
- Temporal vertical-slicing violations (all tests first, then all impl — both have test partners).
- Empty test stubs that exist but contain no assertions.
- Tests in non-standard locations (the inference is strictly `tests/**/test_<basename>.py`).
- Commits made outside Claude Code.

The skill is for what hooks can't catch.

---

### 8. Session-End Skill/Command Deduplication

`.claude/commands/session-end.md` and `.claude/skills/session-end.md` previously duplicated each other. We **removed the skill** and **slimmed the command** to reference a new doc:

- `.claude/skills/session-end.md` — **deleted**. The reference content (knowledge-graph edge types, body template, diagram guidelines) moved out.
- `docs/session-doc-format.md` — **new**. Holds the reference content.
- `.claude/commands/session-end.md` — Step 5 now reads "see `docs/session-doc-format.md`" instead of duplicating the body.

Rationale: session-end is user-invoked (it has side effects — commits files). Skills with side effects that auto-trigger are wrong by construction. Per Anthropic's own docs, command and skill with the same name are equivalent — keeping both is redundant.

**Action required**:
1. Copy `docs/session-doc-format.md` verbatim.
2. **Before deleting `.claude/skills/session-end.md`**, diff it against ours to surface any local customizations:
   ```bash
   diff .claude/skills/session-end.md <utils-path>/.claude/skills/session-end.md  # before utils deleted it; compare against the prior tagged commit if needed: git -C <utils-path> show cf946b5:.claude/skills/session-end.md
   ```
   If your file has local-only content (e.g., custom edge types, repo-specific body templates, embedded checklists), copy that content into `docs/session-doc-format.md` first. Only delete the skill file once nothing of value is lost.
3. Replace `.claude/commands/session-end.md` with the slimmed version that references `docs/session-doc-format.md`. If your command had local customizations, merge them in rather than overwriting.

---

### 9. `python-prototyper` Agent Workflow Inverted to Test-First

Previous workflow:
```
3. Implement the code
4. Write tests alongside the code in tests/
```

This was code-first-tests-second; the agent definition itself was actively undermining shift-left at the enforcement surface. Now:

```
3. Plan the vertical slices (list behaviors to test in priority order)
4. For each slice, in order:
   a. Write the next failing test in tests/ — confirm RED
   b. Write minimum code in src/ that passes it — confirm GREEN
   c. Do not refactor while RED; refactor only when all tests pass
5. Run full pytest
```

Also fixed: stale reference to `docs/design/pillars.md` (which doesn't exist in `utils`); now points to `CONTEXT.md` + `config/project.yaml`.

**Adoption mode: CUSTOMIZE** (master table row 20). The file contains hard-coded `src/myproject/` references in the **Project Layout** and **Scope** sections — substitute to your package name. There is also a reference to the audit-hook log path in the Design Principles section that mentions `src/myproject/`.

**Action required**:
1. **If you have not customized this agent locally**: copy `.claude/agents/python-prototyper.md` from `utils`, then find/replace every occurrence of `myproject` with your package name. Three sections contain it: Project Layout, Scope, and the Shift-Left Testing design principle.
2. **If you have customized this agent locally**: diff first.
   ```bash
   diff .claude/agents/python-prototyper.md <utils-path>/.claude/agents/python-prototyper.md
   ```
   Merge in: (a) the workflow inversion (steps 3–5 are now test-first vertical-slice), (b) the pillars-ref fix (CONTEXT.md + config/project.yaml instead of docs/design/pillars.md), (c) the strengthened Shift-Left Testing design principle (including the hook reference). Preserve your local customizations.
3. Verify after merging: the workflow section MUST list "write failing test" before "write minimum code." If any of your local edits restore code-first ordering, the agent will undermine the rest of this propagation.

---

### 10. CLAUDE.md — Test-First Development Principle

The Shift-Left Testing principle in CLAUDE.md is strengthened from "write tests alongside code" to a mandate for test-first vertical-slice with explicit reference to the hook.

**Action required**:
1. Update your CLAUDE.md Development Principles section. Wording template:

```markdown
### Shift-Left Testing (test-first, vertical-slice)
Every new behavior in `src/<yourpkg>/` is driven by a **failing test written first**, followed by the **minimum implementation** that makes it pass, then the next slice. This is vertical-slice (tracer-bullet) TDD; see [`.claude/skills/shift-left-testing/VERTICAL-SLICING.md`](.claude/skills/shift-left-testing/VERTICAL-SLICING.md).

Do not write a horizontal slice (all tests first, then all impl). Do not write production code without a failing test driving it.

A `PostToolUse` audit hook (`.claude/hooks/post-tool-shift-left-audit.sh`) fires after every `Write`/`Edit` to `src/<yourpkg>/**/*.py` and logs evidence to `.claude/audits/shift-left-violations.log`. The hook does not block; it produces an audit trail. See [`.claude/skills/shift-left-testing/ENFORCEMENT.md`](.claude/skills/shift-left-testing/ENFORCEMENT.md) for the full enforcement gradient.
```

Substitute `<yourpkg>` to match your package name.

---

### 11. Python 3.11 Minimum (catch-up from 2026-04-21)

Bumped from 3.10 in `utils` on 2026-04-21 but the propagation cycle that day was scoped to the docs/reviews convention and didn't carry this. Catching up now.

**Files affected**:
- `pyproject.toml` — `requires-python = ">=3.11"` (utils' pyproject does not declare a classifiers table; if yours does, update the `Programming Language :: Python :: 3.X` entries to remove 3.10 and add 3.11+)
- `config/project.yaml` — `python.min_version: "3.11"`, `python_requires: ">=3.11"`
- `CLAUDE.md` — "Language: Python (3.11+)"

Rationale: `zoneinfo` is in stdlib at 3.9+, `match` is 3.10+, but 3.11 brings tomllib (stdlib TOML parsing), Exception Groups, faster startup. Most CI images and local environments are at 3.11+ already.

**Action required**:
1. Verify your local environment and CI use Python 3.11+. `python --version`.
2. If yes: update your `pyproject.toml`, `config/project.yaml`, and CLAUDE.md to declare 3.11 minimum.
3. If no: defer this part of the propagation until your environment is upgraded. The other artifacts in this cycle do not depend on Python 3.11.

---

### 12. `.gitignore` Additions

```
# Scratch / hold area (per-repo thinking workspace)
docs/design/hold/

# Claude Code
.claude/audits/
```

`docs/design/hold/` is a per-repo workspace for strategic memos, attached docs, and scratch — tracked locally on the filesystem, gitignored. `.claude/audits/` is where the shift-left audit log lives.

**Action required**: append both to your `.gitignore` (after the existing `.claude/agent-memory/` and `.claude/settings.local.json` lines if you have them).

---

### 13. `settings.local.json` → `settings.json` Rename

Anthropic's convention: `.claude/settings.json` is the team-wide checked-in file, `.claude/settings.local.json` is the per-user override (gitignored). The previous filename used `settings.local.json` for team-wide content — backwards.

**Action required**:
1. If your repo has `.claude/settings.local.json` with team-wide content: `git mv .claude/settings.local.json .claude/settings.json` so the rename is tracked. (Plain `mv` won't work cleanly if `.claude/settings.local.json` was previously gitignored — the rename needs to enter git's tracking; verify with `git status` afterward.)
2. Confirm `.claude/settings.local.json` is listed in `.gitignore` going forward. Anything in it is now per-developer-override and not committed.
3. The hook configuration from §7 lives in `.claude/settings.json` (team-wide, checked in). Per-developer disable goes in `.claude/settings.local.json` (gitignored).

---

### 23. Optional Adoption Helper (`scripts/adopt_doctrine.py`)

A downstream-side helper that applies the **mechanical** parts of this bundle for you: the 10 verbatim copies, the hook-script `myproject` → `<yourpkg>` substitution, the `.claude/settings.json` `PostToolUse` merge, and the `.gitignore` append. Everything that requires human judgment (LANGUAGE.md content, CONTEXT.md content, CLAUDE.md merge, ADR-0001 attribution, python-prototyper customization, Python 3.11 bump, hub-only propagation-protocol, legacy single-file skill deletions, `settings.local.json` rename) is **deliberately left for you** — the script prints a checklist of those items with section references back to this entry.

**Explicit non-goals**: the helper does not delete anything, does not edit `LANGUAGE.md` / `CONTEXT.md` / `CLAUDE.md` / `pyproject.toml`, does not rename `settings.local.json`, and does not overwrite existing target files (any pre-existing target is skipped with a "review by hand" status). The settings.json merge preserves all existing top-level keys and any existing `PostToolUse` matchers; it appends ours as an additional entry and is idempotent on re-run.

**Action required**:
1. Copy `scripts/adopt_doctrine.py` into your repo's `scripts/` directory. (You can also run it from a local utils clone without copying — `python ~/projects/github/utils/scripts/adopt_doctrine.py` from your repo root.)
2. Optionally copy `tests/unit/test_adopt_doctrine.py` if you want the test partner local; otherwise the upstream tests are authoritative.
3. From your repo root, dry-run first: `python scripts/adopt_doctrine.py --dry-run`. Review the printed plan and the "MANUAL ATTENTION REQUIRED" checklist.
4. Re-run without `--dry-run` to apply: `python scripts/adopt_doctrine.py`. You will be prompted `Apply changes? [y/N]` unless you pass `--yes`.
5. Apply the manual-attention items by hand using this doctrine entry as your reference.

**Flags**:
- `--upstream PATH` — local utils clone (default `~/projects/github/utils/`).
- `--package NAME` — your downstream package name (default: auto-detect from `src/<pkg>/` if exactly one subdirectory exists).
- `--dry-run` — print the plan, write nothing.
- `--yes` — skip the confirmation prompt.

**Operational safety**: dry-run is the default mental model — the explicit prompt before any write is non-negotiable in the interactive path. The helper is idempotent: re-running after a partial adoption skips already-applied items.

**The risk of using the helper vs. by-hand adoption**: the helper itself is a single point of failure — a bug in the script applies the bug to every repo that runs it. Mitigations: (a) 35 tests covering all 9 functions including settings-merge edge cases (empty / other-matcher / our-matcher-already-present); (b) skip-don't-overwrite semantics on every target; (c) the helper deliberately refuses CUSTOMIZE artifacts so the human still applies the judgment-heavy ones. If you are uncomfortable with the helper, the manual adoption path below remains fully supported.

---

### Suggested Adoption Order

**Fast path (helper-assisted, see §23)**: dry-run `scripts/adopt_doctrine.py` from your repo root, review the plan and the manual-attention checklist, re-run to apply the mechanical 13 artifacts in one step, then work through the printed checklist for the 10 judgment-required items by hand.

**Slow path (fully by hand)** — within one merge session per repo:

1. **First — the framework spec**: copy SKILLS_FRAMEWORK.md v2 (§5). Everything else makes sense against it.
2. **Refactor the three legacy skills to directory form**: shift-left-testing, configuration-management, python-venv-management (§5).
3. **Add the ADR system**: ADR-FORMAT.md, .gitkeep, the skill, ADR-0001 (§3).
4. **Add the doctrine artifacts**: LANGUAGE.md + skill (§1), CONTEXT.md + skill (§2). Customize the content as you go.
5. **Resolve session-end dedup**: docs/session-doc-format.md, delete the skill, slim the command (§8).
6. **Update python-prototyper agent**: test-first workflow + pillars ref fix (§9).
7. **Update CLAUDE.md** Development Principles (§10).
8. **Wire the enforcement layer**: copy the hook script with path substitution, merge the settings.json block, update .gitignore (§7, §12, §13).
9. **Verify**: run your test suite (should be unaffected); edit any src/ file and check `.claude/audits/shift-left-violations.log` for a fresh entry.
10. **Python 3.11 bump** (§11) — only if your environment supports it.

---

### Rollback

If anything in this cycle breaks your repo, each artifact reverts independently:

- The **PostToolUse hook** never blocks tool calls — at worst it produces noisy stderr. Disable by removing the `hooks` block from `.claude/settings.json` (or override in `.claude/settings.local.json` with `"hooks": {}`).
- The **hook script** at `.claude/hooks/post-tool-shift-left-audit.sh` is referenced only by `.claude/settings.json`. After the settings-block removal above, the script file is inert. Delete or leave it; either is fine.
- The **directory-form skill refactors** are functionally equivalent to the single-file versions — Claude Code's skill discovery picks up both forms. If a refactored skill misbehaves, revert by restoring the prior single-file from git history and removing the new directory.
- **LANGUAGE.md / CONTEXT.md** are docs only — no code consumes them. Delete the files if they're not useful yet; the skills will simply not find a glossary/context to maintain.
- **ADR system** is docs only. Delete `docs/adr/` and `.claude/skills/recording-architecture-decisions/` if not useful.
- **`.gitignore` additions** (`docs/design/hold/`, `.claude/audits/`) — remove the lines if you want either path tracked. The `.claude/audits/` line is load-bearing for the hook (without it, the audit log would be committed and noisy); only remove if you've also removed the hook.
- **`settings.local.json` → `settings.json` rename** — `git mv` back if needed. Confirm `.gitignore` matches the choice.
- **Python 3.11 bump** is in `pyproject.toml`, `config/project.yaml`, CLAUDE.md — revert these three files to restore 3.10 minimum.
- **`python-prototyper.md` workflow inversion** — `git revert` the agent file; the previous code-first workflow returns. The Pass 4 audit notes that the previous workflow was actively undermining shift-left, so revert only if you've decided not to adopt the enforcement layer at all.
- **CLAUDE.md test-first principle** — revert that section if you've decided not to adopt the enforcement layer.

---

### Source Material and Attribution

- **Matt Pocock's [`mattpocock/skills`](https://github.com/mattpocock/skills)** — pattern source for `LANGUAGE.md` (CONTEXT-FORMAT.md adapted), `CONTEXT.md` (CONTEXT-FORMAT.md adapted), `ADR-FORMAT.md` (triple filter adopted verbatim), and `VERTICAL-SLICING.md` (tracer-bullet rules adopted verbatim where attributed). **Patterns adopted, vocabulary not** — Pocock's vocab is TypeScript-ecosystem-specific.
- **Anthropic's December 2025 skills open standard** — directory form with YAML frontmatter, progressive disclosure.
- **Pass 4 reviews** — `docs/reviews/20260519_pass4_doctrine_audit.md` (code-reviewer), `docs/reviews/20260519_pass4_enforcement_maut.md` (decision-scientist), `docs/reviews/20260519_pass4_enforcement_grill.md` (proposer). Read these if you want to understand why the enforcement layer is soft-deterministic rather than hard-block.
- **utils sessions** — `docs/sessions/20260519_doctrine_artifact_buildout.md` documents the original build; the current session doc (the one in this propagation's commit) documents the Pass 4 + enforcement-layer additions.

---

## 2026-04-21: Agent Output Convention — docs/reviews/ and YYYYMMDD_<subject>.md

**Files changed**: `.claude/agents/decision-scientist.md`, `.claude/agents/code-reviewer.md`, `.claude/agents/proposer.md`, `.claude/agents/python-prototyper.md`, `.claude/README.md`, `.claude/teams/decision-science.md`, `.claude/teams/feature-development.md`, `CLAUDE.md`, `config/project.yaml`

**Files added**: `docs/reviews/` directory

### Change

Agents that write reports, audits, or analysis now share a single output convention:
- **Directory**: `docs/reviews/` (dedicated, not the `docs/` root)
- **Filename**: `YYYYMMDD_<subject>.md` (date first, sorts chronologically)
- **Author**: goes in the file header, not the filename

Previously, agents wrote to `docs/` with inconsistent filenames (e.g., `decision_audit_YYYYMMDD.md` — date buried, no subject, not sortable). The new convention matches the session doc pattern and makes it easy to find the most recent review across all agents.

Each agent definition now includes a standard report header template:

```markdown
# [Report title]

**Author**: [agent-name]
**Date**: YYYY-MM-DD
**Type**: [MAUT audit / Code review / Config review / ...]
```

### Scope changes per agent

| Agent | Write scope (before) | Write scope (after) |
|-------|---------------------|---------------------|
| `decision-scientist` | `docs/` | `docs/reviews/` |
| `code-reviewer` | `docs/` | `docs/reviews/` |
| `proposer` | `docs/` | `docs/plans/` (proposals), `docs/reviews/` (analysis) |
| `python-prototyper` | `docs/` | `docs/sessions/`, `docs/plans/` (explicitly, no `docs/reviews/`) |

The `.claude/README.md` scope matrix was updated to reflect explicit per-directory rows (`docs/sessions/`, `docs/plans/`, `docs/reviews/`) instead of a single `docs/` column.

`config/project.yaml` `paths:` section now includes `reviews: "docs/reviews/"`.

### Action Required

**For all repos with agent definitions** — update each agent that writes reports:

1. **`decision-scientist.md`** (if present): change output path to `docs/reviews/YYYYMMDD_<subject>.md`. Add the standard header template to the Output Format section.

2. **`code-reviewer.md`** (or equivalent auditor): change output path to `docs/reviews/YYYYMMDD_<subject>.md`. Add the standard header template.

3. **`proposer.md`** (if present): no change to proposal location (`docs/plans/` was already correct). Add `docs/reviews/YYYYMMDD_<subject>.md` as the output for investigation-only reports. Update Scope Write to enumerate `docs/plans/` and `docs/reviews/` explicitly instead of the broad `docs/` grant.

4. **`python-prototyper.md`** (if present): narrow `docs/` Write grant to `docs/sessions/`, `docs/plans/` explicitly — prototypers should not write to `docs/reviews/`.

5. **`.claude/README.md` scope matrix**: replace single `docs/` row with three rows: `docs/sessions/`, `docs/plans/`, `docs/reviews/`. Assign Write access only to the agents that own each directory.

6. **`config/project.yaml`**: add `reviews: "docs/reviews/"` under `paths:`.

7. **Create `docs/reviews/`**: `mkdir -p docs/reviews && touch docs/reviews/.gitkeep`

8. **Team templates** (`.claude/teams/*.md`): update any role description that says "write to `docs/`" to name the specific subdirectory.

9. **`CLAUDE.md` agent table**: if `decision-scientist` is listed, confirm it shows `docs/reviews/` as its output. If it is absent, add it.

---

## 2026-03-31: Session-Start — Add Git Sync

**Files changed**: `.claude/commands/session-start.md`

### Change

Added `git fetch && git pull` as the first command in Step 4 (Verify Health). Session-start now syncs with remote before running tests or checking status.

### Action Required

Update your `.claude/commands/session-start.md` Step 4 to include the fetch/pull before other health checks:

```bash
git fetch && git pull # Sync with remote before anything else
pytest                # Verify all tests pass
git status            # Check for uncommitted changes
git branch -v         # Current branch state
```

---

## 2026-03-26: Decision Science Module — Shared MAUT/MCDA Utility

**Files added**: `src/myproject/decision_science/` (4 modules), `.claude/agents/decision-scientist.md` (new), `.claude/teams/decision-science.md` (new)

### 1. Shared MAUT Scorer

A new `decision_science` subpackage provides the infrastructure that 6+ repos were building independently:

- **`value_functions.py`** — 7 pluggable value functions: `linear`, `exponential`, `logarithmic`, `logistic`, `step`, `gaussian`, `piecewise_linear`. All return `float` in `[0, 1]`.
- **`scorer.py`** — `MAUTScorer` class with additive aggregation `U = Σ w×u`. Includes:
  - `from_yaml()` — config-driven model loading (mandatory, not optional)
  - `from_weights()` — bridge to `weights.py` `generate_weights()` output
  - `score()` / `rank()` — with weight validation and value function output bounds checking
  - `explain()` on `DecisionResult` — structured dict for programmatic consumption
  - `dominance_check()` — weight-independent dominated alternative detection
- **`sensitivity.py`** — `one_at_a_time()`, `monte_carlo()` (Dirichlet sampling), `scenario_compare()`, `robustness_report()` (single confidence metric)
- **`visualization.py`** — `radar_chart()`, `tornado_plot()`, `rank_stability_heatmap()` (matplotlib optional)

### 2. Decision-Scientist Agent

New Level 1 agent that audits decision models for MAUT correctness:
- Validates weights sum to 1.0, no negatives, value functions output in [0,1]
- Flags missing sensitivity analysis, inappropriate value function shapes
- Audit-only scope: reads everything, writes only to `docs/`

### 3. Decision-Science Team

New 5-agent team template: proposer + decision-scientist + python-prototyper + test-runner + code-reviewer. Use for any MAUT/MCDA work.

### 4. YAML Config Schema

Decision models are defined in YAML:

```yaml
criteria:
  - name: effectiveness
    weight: 0.35
    value_fn: linear
    params: {low: 0, high: 100}
  - name: risk
    weight: 0.40
    value_fn: gaussian
    params: {center: 0, sigma: 50}
  - name: survival
    weight: 0.25
    value_fn: logistic
    params: {midpoint: 0.5, steepness: 8}
```

### Action Required

**If your repo does MAUT/MCDA scoring** (tactics-game, quest-engine, project-megan, agent-eval, paperboy, elephant-graveyard):
- Review the shared module — it can replace your local scorer implementation
- Your domain-specific criteria, value function parameters, and profiles stay in your repo
- The scoring infrastructure, sensitivity analysis, and visualization come from utils
- Migration is opt-in and additive — nothing breaks if you don't adopt

**If your repo does NOT do MAUT/MCDA**:
- No action required — ignore this update
- The module exists if you ever need weighted multi-criteria decision analysis

**Agent/team adoption** (all repos):
- Copy `.claude/agents/decision-scientist.md` if you do any form of weighted scoring
- Copy `.claude/teams/decision-science.md` for MAUT/MCDA workflow support
- Update `.claude/README.md` agent roster and scope matrix if you adopt either

---

## 2026-03-24: Planning Framework, Proposer Agent, and Doctrine Propagation

**Files changed**: `.claude/commands/task.md`, `.claude/commands/session-start.md`, `.claude/agents/proposer.md` (new), `.claude/README.md`, `.claude/teams/feature-development.md`, `CLAUDE.md`

### 1. TCS Universal + Wave Terminology

- **TCS is now the universal task detail standard** — every task within a CONOP or OPORD is written at TCS (Task, Condition, Standard) level. The document type escalates the frame; the task granularity stays consistent.
- **"Wave" terminology adopted for tactical execution** — agent teams deploy in *waves* within CONOPs and OPORDs. "Phase" is reserved for strategic roadmap milestones (`project.yaml` build_phases). A campaign-level OPORD may contain phases of waves, but this is deliberate and infrequent.
- **New section added**: "Terminology: Phases vs Waves" in the escalation ladder.

### 2. Proposer Agent

- **New `proposer` agent** — analyzes problems and proposes bold approaches before implementation. Reads the full codebase, writes proposals to `docs/`. Instructed not to write code — same access pattern as `code-reviewer`.
- **Feature-development team updated** — workflow is now: proposer explores and proposes → code-reviewer challenges → user decides → python-prototyper builds → test-runner verifies.
- **Agent roster is now 4 agents** — test-runner, code-reviewer, proposer, python-prototyper.
- Inspired by the AgenticSciML paper (arxiv.org/html/2511.07262v2) — structured debate before implementation produces better solutions than jumping straight to code.

### 3. Doctrine Propagation System

- **Upstream doctrine notifications** — utils now maintains this changelog and can propagate notifications to downstream repos via `.claude/upstream-update.md`.
- **Session-start check (Step 3.6)** — `/session-start` now checks for `.claude/upstream-update.md` and surfaces it if present. This is how you'll receive future updates.

### Action Required

**Planning framework**:
- Review your `.claude/commands/task.md` escalation ladder against `utils/.claude/commands/task.md`
- Update "phase" references within CONOP/OPORD descriptions to "wave"
- Add TCS detail requirement to CONOP and OPORD level descriptions
- Add the "Terminology: Phases vs Waves" section
- Update your `CLAUDE.md` planning escalation summary to match

**Proposer agent**:
- Copy `.claude/agents/proposer.md` from utils (or create your own adapted version)
- Add proposer to your agent catalog and scope matrix in `.claude/README.md`
- Update `.claude/teams/feature-development.md` to include the propose → challenge → implement workflow
- Add proposer to your `CLAUDE.md` agent table
- Update any "3-agent" references to "4-agent"

**Doctrine propagation** (do this first so you receive future updates):
- Add Step 3.6 to your `.claude/commands/session-start.md`:

```markdown
## Step 3.6: Check Upstream Doctrine Updates

Check if `.claude/upstream-update.md` exists. If it does:
- Read and surface the contents to the user
- Flag it prominently: **"Upstream doctrine update available — review before proceeding"**
- Do NOT delete the file — the user decides when to act on it
```

- After reviewing all updates, delete `.claude/upstream-update.md` from your repo
