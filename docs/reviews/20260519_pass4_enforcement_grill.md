# Review: Pass 4 — Fresh-Eyes Grill + Shift-Left Enforcement Proposals

**Author**: proposer
**Date**: 2026-05-19
**Type**: Doctrine grill + enforcement proposals
**Scope**: All doctrine artifacts built in the prior session. Fresh context — prior grill (`20260519_plan1_proposer_grill.md`) is referenced for methodology continuity, not carried forward as assumption.

---

## Job 1 — Doctrine Grill

### 1.1 Doctrine Debt: Things We Claim But Don't Have

**ADR system exists, zero ADRs written.** `docs/adr/` contains only `ADR-FORMAT.md` and `.gitkeep`. Session doc `Next Steps` notes two candidate decisions: "single Sprint-3 commit vs split commits" (rejected by triple filter — reversible) and "directory form mandatory for all new skills" (candidate, not filed). The debt is not the zero count per se — the triple filter correctly blocks routine choices — but the *absence of a written first ADR* means the workflow is untested. The format doc is doctrine about a process that has never run. Correct action: apply the triple filter to "directory-form mandatory" explicitly, write ADR-0001 if it passes, and note in this session doc that the filter was applied. Before propagation, at minimum one ADR should exist so downstream maintainers see a real example alongside the format.

**Propagation-protocol references a skill that doesn't exist.** Line 178 of `docs/propagation-protocol.md`: "Authoring Skill: none yet (candidate: future `propagating-doctrine` skill if this protocol gets enough use)." Not a hard error, but the parenthetical leaves the protocol without a LANGUAGE.md-registered skill to invoke. Contrast with every other artifact, which names a skill in its header. Minor, but inconsistent.

**`python-prototyper.md` references `docs/design/pillars.md`, which likely does not exist.** The agent says "Follow the project's design pillars (see `docs/design/pillars.md`)." The session doc makes no reference to this file being created or existing. The three pillars are defined in `CONTEXT.md` and `config/project.yaml` — not in a `pillars.md`. This is a stale reference that will silently fail any agent that tries to load it.

### 1.2 Vocabulary Drift

**"Downstream Repo" definition in LANGUAGE.md lists the 2026-04-21 cycle count as "11 repos" but `propagation-protocol.md` lists 18 repo names.** LANGUAGE.md: "The most recent cycle (2026-04-21) reached 11 repos." Propagation protocol Roster section lists 18 names as of 2026-05-19. Both documents acknowledge the discrepancy differently: LANGUAGE.md anchors on the last cycle count; the protocol anchors on current discovery. This is the same 11-vs-18 issue the code-reviewer flagged in Pass 3 — it was acknowledged but the LANGUAGE.md definition was not updated to reflect that the roster has grown since that cycle. The definition is not wrong, but it will confuse anyone reading LANGUAGE.md today.

**"Skill" definition in LANGUAGE.md uses "preferred" for directory form but the Skills vs Commands table in SKILLS_FRAMEWORK.md says "all current Level 0 skills have migrated to directory form."** The LANGUAGE.md definition is correctly qualified; the framework text implies directory form is now effectively required for Level 0. These are consistent in intent but a future author might read them as "preferred is optional" when the actual rule is "mandatory for new skills at Level 0."

**"Roster" in LANGUAGE.md is defined as "Five at the time of writing."** That phrase will age badly across downstream repos and future sessions. This is a snapshot embedded in what is supposed to be a stable definition. Definitions should state what the term means, not what the count happened to be. Recommend: remove the count from the definition body; the count belongs in CONTEXT.md's Key Relationships section.

### 1.3 Sequencing Problems

**`CONTEXT.md` reading order points agents to `docs/sessions/` before `docs/propagation-protocol.md`.** Step 6 says "recent session for live context." But the session doc (`20260519_doctrine_artifact_buildout.md`) references the propagation protocol repeatedly and contains decisions about doctrine. An agent reading CONTEXT.md's reading order gets the session doc *before* the propagation protocol — so when the session doc says "see propagation-protocol.md" the agent has already formed a picture without that context. This is not severe but it's backwards: the propagation protocol is architecture; the session doc is history. Architecture should precede history.

**ANTIPATTERNS.md is a sidecar to SKILL.md, but it is not referenced from SKILL.md's Sidecar Files section explicitly enough for the anti-patterns 4 and 5.** SKILL.md lists ANTIPATTERNS.md as "the broader set of testing anti-patterns this discipline avoids" — but Anti-Pattern 5 (Implicit): Mock-the-Thing-You're-Testing is marked as implicit, meaning it's not even numbered consistently. An agent told to avoid anti-patterns will find four numbered anti-patterns and one implicit one in the same document. The implicit one is arguably the most common failure mode with mocked tests.

### 1.4 Hidden Coupling

**The propagation-protocol's "Civilian/Military Vocabulary" section duplicates the crosswalk table from LANGUAGE.md.** Both documents carry the full military→civilian table. This is duplication, not reference. If the crosswalk changes, it must be updated in two places. The correct form is: propagation-protocol.md says "Use the civilian vocabulary per the crosswalk in LANGUAGE.md" with a link, and carries only the note that "this is enforced at review time." Same coupling exists in SKILLS_FRAMEWORK.md (which also carries the full table). Three copies of the same table is maintenance debt.

**`CONTEXT.md` Anti-rules section includes "Do not migrate side-effect-carrying commands to auto-triggering skills" but SKILLS_FRAMEWORK.md expresses the same rule.** Two canonical statements of the same doctrine means a future dispute about which is authoritative. CONTEXT.md should own the *rule*; SKILLS_FRAMEWORK.md should reference it, not restate it.

### 1.5 Adoption Ambiguity

The session doc's Next Steps item notes: "The doctrine entry must include a per-artifact adoption-mode table (which artifacts are template-copy vs project-customize) per the code-reviewer's flagged pre-propagate fix." That fix was **not made before the commits landed on main**. The propagation-protocol.md `Cycle Anatomy` and the `Porting Skills to New Projects` section in SKILLS_FRAMEWORK.md both describe *how* to propagate but neither says, for each artifact, which of these modes applies:

| Mode | Meaning |
|---|---|
| Copy-as-is | Downstream takes the file verbatim |
| Copy-and-customize | Downstream copies the template and edits project-specific fields |
| Reference-only | Downstream links to upstream; does not carry a local copy |
| Do-not-propagate | Not meant for downstream (utility code, local quality) |

This table is missing for the 6 doctrine artifacts built in this session. It must exist before the 6th propagation cycle runs, or downstream maintainers will have to guess. This is the single most load-bearing pre-propagate fix.

### 1.6 Anti-Doctrine Omissions

The doctrine needs explicit "do not do X" statements in two places that are currently silent:

**VERTICAL-SLICING.md names the horizontal-slice failure mode but does not say "never commit a test file without a corresponding implementation change in the same commit."** The skill describes what the failure looks like; it does not prohibit it. A commit that adds 6 tests and no implementation is indistinguishable to git from a commit that adds 6 placeholder test stubs. The doctrine needs a prohibition, not just a description.

**ADR-FORMAT.md says "Honesty matters — if an ADR has only positive consequences, the rigor is missing."** But it does not say "do not write ADRs for decisions that failed the triple filter." The format file and the recording-architecture-decisions skill both say "write one when the triple filter passes" — but neither says "if you are about to write an ADR and the triple filter fails, stop and document it as a commit message instead." The anti-rule is implied but unwritten.

---

## Job 2 — Deterministic Enforcement of Shift-Left Testing

### The Core Problem

Skills are probabilistic. An agent may or may not load `shift-left-testing` before writing code. Even when loaded, the vertical-slicing discipline is a norm described in text, not a constraint enforced by the environment. The failure mode named in VERTICAL-SLICING.md — write all tests, then all implementation — is invisible to any current tooling. Hooks are the only mechanism that fires outside of Claude's judgment.

The `.claude/settings.json` currently has **zero hooks configured**. The enforcement layer is completely absent.

---

### Proposed Enforcement Mechanisms

#### Hook A — ImplWithoutTest Guard (PreToolUse on Write/Edit)

**Mechanism**: `PreToolUse` hook fires before every `Write` or `Edit` call. The hook checks if the target file is under `src/`. If yes, it checks whether a corresponding test file has been modified in the current turn (via `git diff --name-only`). If a test partner does not exist or has not been modified, the hook emits a warning to stderr and logs the violation to `.claude/audits/violations.log`. It does **not** block the write — blocking is too aggressive for legitimate refactors.

**Sample bash**:

```bash
#!/usr/bin/env bash
# .claude/hooks/impl_without_test.sh
# Called by PreToolUse. $1 = tool name, $2 = file path being written.
set -euo pipefail

TOOL="$1"
TARGET="$2"
AUDIT_LOG=".claude/audits/violations.log"
mkdir -p .claude/audits

# Only care about src/ writes
if [[ "$TARGET" != src/* ]]; then exit 0; fi

# Derive expected test file path
# src/myproject/utils/foo.py -> tests/unit/test_foo.py (heuristic)
BASENAME=$(basename "$TARGET" .py)
TEST_CANDIDATE=$(git diff --name-only 2>/dev/null | grep -E "test_${BASENAME}|${BASENAME}_test" || true)

if [[ -z "$TEST_CANDIDATE" ]]; then
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "${TIMESTAMP} WARN impl-without-test: ${TARGET}" >> "$AUDIT_LOG"
  echo "WARN: Writing to ${TARGET} with no test file modified this turn. Vertical-slicing doctrine requires test-first. See VERTICAL-SLICING.md." >&2
fi
exit 0
```

**What it catches**: Implementation writes that occur without a corresponding test modification in the same agent turn.

**What it misses**: Multi-turn sequences where tests are written in turn 1 and implementation in turn 3 (the hook sees only the current diff, not the conversation history). Also misses pure-refactor commits where behavior does not change.

**False positives**: Legitimate cases — fixing a docstring, renaming a parameter with no behavioral change, updating a config import. Scope around by checking `git diff --cached` for whether the change is trivially small (<5 lines added to impl).

**Boldness vs feasibility**: Medium boldness, high feasibility. Does not block the agent, only logs and warns. Real cost is near-zero. Highest-value hook in the set. **Ship first.**

---

#### Hook B — Horizontal-Slice Detector (PostToolUse on Write/Edit)

**Mechanism**: `PostToolUse` hook fires after every batch of Write/Edit calls. It computes, for the current git working tree: (number of lines added to `tests/`) vs (number of lines added to `src/`). If the ratio exceeds 3:1 (test lines to impl lines) with no impl write yet, this is the signature of "writing all tests first." The hook logs a structured violation and emits a warning.

**Sample bash**:

```bash
#!/usr/bin/env bash
# .claude/hooks/horizontal_slice_detector.sh
set -euo pipefail

AUDIT_LOG=".claude/audits/violations.log"
mkdir -p .claude/audits

TEST_LINES=$(git diff --unified=0 -- 'tests/' 2>/dev/null | grep '^+' | grep -v '^+++' | wc -l || echo 0)
IMPL_LINES=$(git diff --unified=0 -- 'src/' 2>/dev/null | grep '^+' | grep -v '^+++' | wc -l || echo 0)

# Threshold: 5+ test lines added, impl lines are 0 (pure test batch)
if [[ "$TEST_LINES" -ge 5 && "$IMPL_LINES" -eq 0 ]]; then
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "${TIMESTAMP} WARN horizontal-slice: ${TEST_LINES} test lines, ${IMPL_LINES} impl lines" >> "$AUDIT_LOG"
  echo "WARN: ${TEST_LINES} test lines added with 0 impl lines. Possible horizontal slice. See VERTICAL-SLICING.md." >&2
fi
exit 0
```

**What it catches**: Bulk test-writing sessions before any implementation. The anti-pattern described explicitly in VERTICAL-SLICING.md.

**What it misses**: Staggered sessions where tests are committed first (this hook sees the working tree, not git history). Also does not catch the reverse (all impl, no tests) — Hook A covers that.

**False positives**: Legitimate test-only sessions — fixing existing failing tests, adding regression tests for a bug, writing integration tests against existing stable code. These are not anti-patterns. Mitigation: narrow the hook to only fire when `tests/` is under active feature development (heuristic: check if `src/` was modified in the last 5 commits).

**Boldness vs feasibility**: Medium boldness, medium feasibility. The line-count heuristic is coarse. A smarter version would look at function-level additions. Start coarse; tune from audit log data. **Ship after Hook A.**

---

#### Hook C — Test Partner Existence Check (Stop hook)

**Mechanism**: `Stop` hook fires at the end of every agent turn. It diffs all files written during the turn. For every `src/myproject/**/*.py` file written, it checks whether a corresponding `tests/**/test_*.py` exists on disk (not just modified — exists). If an impl file has no test partner at all, it emits a structured block: "VIOLATION: {file} has no test partner. Create tests/{tier}/test_{name}.py before this turn closes." The Stop hook CAN block — it returns a non-zero exit code.

**Sample bash**:

```bash
#!/usr/bin/env bash
# .claude/hooks/test_partner_exists.sh
set -euo pipefail

VIOLATIONS=0
AUDIT_LOG=".claude/audits/violations.log"
mkdir -p .claude/audits

for SRC_FILE in $(git diff --name-only HEAD 2>/dev/null | grep '^src/myproject/' | grep '\.py$'); do
  BASENAME=$(basename "$SRC_FILE" .py)
  # Search for any test file matching test_{name}.py or {name}_test.py
  PARTNER=$(find tests/ -name "test_${BASENAME}.py" -o -name "${BASENAME}_test.py" 2>/dev/null | head -1)
  if [[ -z "$PARTNER" ]]; then
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "${TIMESTAMP} BLOCK no-test-partner: ${SRC_FILE}" >> "$AUDIT_LOG"
    echo "BLOCK: ${SRC_FILE} has no test partner. Create tests/.../test_${BASENAME}.py." >&2
    VIOLATIONS=$((VIOLATIONS + 1))
  fi
done

exit "$VIOLATIONS"
```

**What it catches**: Net-new implementation files with zero test coverage — the most egregious violation of shift-left testing.

**What it misses**: Impl files that have a test file but the test file is empty or only stubs. Hook A catches the in-turn case; this hook catches the zero-partner case across the whole repo.

**False positives**: `__init__.py`, `conftest.py`, utility shims with no testable behavior (e.g., `src/myproject/utils/_compat.py`). Scope by excluding files under 20 lines or matching `__init__.py` / `conftest.py`.

**Boldness vs feasibility**: High boldness — this one blocks. Feasibility depends on consistent test-file naming. The naming conventions in `SKILL.md` are `test_*.py` or `*_test.py`, which this hook uses. **Ship after Hook A validates the naming assumptions.**

---

#### Hook D — Audit Aggregator (Stop hook, non-blocking)

**Mechanism**: A lightweight Stop hook that, at end of every turn, reads `.claude/audits/violations.log` and computes a running violation rate: "X impl-without-test / Y total src writes this session." Emits the rate to stdout as a structured line. Does not block. Gives the human a dashboard view without scrolling through individual warnings.

**Sample bash**:

```bash
#!/usr/bin/env bash
# .claude/hooks/audit_summary.sh
LOG=".claude/audits/violations.log"
if [[ ! -f "$LOG" ]]; then exit 0; fi

IMPL_WARN=$(grep -c "impl-without-test" "$LOG" 2>/dev/null || echo 0)
HORIZ_WARN=$(grep -c "horizontal-slice" "$LOG" 2>/dev/null || echo 0)
BLOCKS=$(grep -c "BLOCK" "$LOG" 2>/dev/null || echo 0)

if [[ "$((IMPL_WARN + HORIZ_WARN + BLOCKS))" -gt 0 ]]; then
  echo "Shift-Left Audit: ${IMPL_WARN} impl-without-test | ${HORIZ_WARN} horizontal-slice | ${BLOCKS} blocks" >&2
fi
exit 0
```

**What it catches**: Nothing new — it aggregates from the other hooks. Value is visibility without action: the human sees the cumulative rate and can decide whether to tighten the rules.

**Boldness vs feasibility**: Low boldness, high feasibility. Zero risk. **Ship with Hook A as a pair.**

---

#### Hook E — PCC Integration (PreToolUse on Bash git commit)

**Mechanism**: `PreToolUse` hook on `Bash` calls that match `git commit`. Before the commit lands, it runs `pytest -x --tb=no -q` (fast fail, no traceback). If any test fails, it blocks the commit with a non-zero exit and logs the failure.

**Sample bash**:

```bash
#!/usr/bin/env bash
# .claude/hooks/precommit_test_guard.sh
# $1 = "Bash", $2 = full bash command string
COMMAND="$2"
if [[ "$COMMAND" != *"git commit"* ]]; then exit 0; fi

echo "Running pre-commit test guard..." >&2
if ! .venv/bin/pytest -x --tb=short -q 2>&1; then
  echo "BLOCK: Tests failing. Resolve before committing." >&2
  exit 1
fi
exit 0
```

**What it catches**: Commits with failing tests — the hardest PCC check, made deterministic.

**What it misses**: Commits made outside the agent (CLI, IDE). This is a Claude Code hook, not a git pre-commit hook. For full coverage, also configure `.git/hooks/pre-commit`.

**False positives**: Almost none — tests should always pass at commit time. Exception: intentional WIP commits with `--no-verify`. Those should stay explicit.

**Boldness vs feasibility**: High boldness (blocks commits), high value, zero ambiguity. This is the clearest candidate. **Ship this before any other hook** if only one ships.

---

### How-To Guide Placement

The user asked: sidecar in `shift-left-testing/`, agent-team workflow doc, or new artifact?

Recommendation: **sidecar named `ENFORCEMENT.md` inside `.claude/skills/shift-left-testing/`**. Rationale:

1. It co-locates enforcement doctrine with the testing doctrine it enforces. An agent that loads `SKILL.md` sees it in the Sidecar Files list and can load it when enforcement configuration is the task.
2. It does not require a new artifact type — it follows the established sidecar pattern.
3. It does not require a new agent — enforcement is configuration, not agency.
4. A cross-link from `ANTIPATTERNS.md` ("the deterministic prevention of these anti-patterns is documented in `ENFORCEMENT.md`") completes the loop.

The `ENFORCEMENT.md` sidecar should contain: the five hooks above (mechanism + bash + when to activate), the `.claude/settings.json` hook configuration template, and a note that `settings.json` is the canonical activation point. It should NOT be a how-to for users; it should be a spec for the agent that is tasked with setting up enforcement.

A separate user-facing "how to use shift-left-testing" guide is lower priority. The skill's existing Quick Reference and Sidecar Files section already provide an entry point. If the user wants a guide, a `GUIDE.md` sidecar (not `ENFORCEMENT.md`) is the right home — it would describe how to invoke the skill, what to do at planning time, and what the vertical-slicing rhythm looks like in practice. But that is a separate task from enforcement.

---

## What We Should NOT Do

**Do not add a hook that blocks ALL src/ writes.** A blanket block on implementation writes without tests would break legitimate work: config-only changes, pure refactors where behavior does not change, migration scripts, `__init__.py`. The hook scope must be bounded.

**Do not make VERTICAL-SLICING.md more elaborate.** The document is correct and well-illustrated. The failure mode is not that agents don't understand vertical slicing — it's that they don't apply it when unsupervised. More documentation does not fix a behavioral problem; hooks do.

**Do not introduce a new agent role to police TDD.** A "test-enforcer" agent adds turns without adding determinism. It would need to be invoked by someone, which reintroduces the probabilistic invocation problem. Hooks fire regardless of agent judgment.

**Do not configure hooks to block on the horizontal-slice detector (Hook B) yet.** The line-count heuristic is too coarse for a blocking hook. Start with warn-and-log; tune from data. Premature blocking on a coarse heuristic will frustrate legitimate test-writing sessions.

**Do not put enforcement documentation in CONTEXT.md or LANGUAGE.md.** Those files define what the project is and what terms mean. Enforcement configuration is operational, not definitional. It belongs in the skill that owns the behavior.

---

## Priority Order for Pre-Propagation Fixes

| Priority | Fix | Who |
|---|---|---|
| 1 | Add per-artifact adoption-mode table to propagation entry draft | lead |
| 2 | Fix stale `docs/design/pillars.md` reference in `python-prototyper.md` | lead |
| 3 | Apply triple filter explicitly to "directory-form mandatory" — write ADR-0001 if it passes | lead |
| 4 | Remove crosswalk table duplication — propagation-protocol.md and SKILLS_FRAMEWORK.md reference LANGUAGE.md instead of re-carrying the table | lead |
| 5 | Update "Roster" definition in LANGUAGE.md to remove snapshot count from definition body | lead |
| 6 | Configure Hook A + Hook D in `.claude/settings.json` before propagation | lead or python-prototyper |
| 7 | Add `ENFORCEMENT.md` sidecar to `shift-left-testing/` | python-prototyper |
