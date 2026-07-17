# Review: Pass 6 — Day-1 Playbook Structural Rewrite Proposal

**Author**: proposer
**Date**: 2026-05-19
**Type**: Structural analysis + section drafts
**Scope**: `docs/design/from_template_to_project.md` — organization and new content following the 2026-05-19 doctrine cycle
**Parallel work**: `code-reviewer` Pass 6 is auditing stale facts (test count, agent count, Python version) line-by-line. This doc does NOT duplicate that work. It addresses structure and substance.

---

## Job 1 — Structural Diagnosis

### Current State

The doc's 10-section structure was written before doctrine artifacts existed. Three core problems:

**Problem 1 — The new doctrine artifacts have no home.**
`LANGUAGE.md`, `CONTEXT.md`, the ADR system, and the Skills Framework v2 are not optional modules to "keep or remove" — they're required infrastructure the cloner must fill in. §3 ("What to Keep, Evaluate, or Remove") has no category for them, and no section explains what to do with them.

**Problem 2 — The enforcement layer is invisible.**
The PostToolUse audit hook is the most operationally consequential thing the cloner must configure. Without the path substitution step, the hook silently does nothing (the Pass 5 grill documented this failure mode: hook syntax error → no audit log → no error — worst failure mode). This substitution requirement does not appear anywhere in the current doc.

**Problem 3 — §4 "Defining Your Project" points at `docs/design/pillars.md`.**
That file exists but is a blank template scaffold — no content, no pillars defined. The actual working answer for "what are this project's pillars?" lives in `CONTEXT.md` (Constraints section) and `config/project.yaml`. The section is sending the cloner to an unfilled skeleton.

### Proposed 11-Section Outline

The rewrite adds two new sections, splits one, and relocates one. The net reader experience: doctrine infrastructure is handled right after the rename step, before stripping modules — because you need to know what you're keeping before you strip anything.

```
1.  Overview
2.  Day-1 Checklist              ← updated: adds doctrine + hook steps
3.  Doctrine Infrastructure      ← NEW: LANGUAGE.md, CONTEXT.md, ADRs, Skills Framework
4.  Test-First Enforcement Layer ← NEW: hook, path substitution, ENFORCEMENT.md
5.  What to Keep, Evaluate, or Remove  ← updated: doctrine artifacts reclassified
6.  Defining Your Project        ← updated: redirected from pillars.md → CONTEXT.md
7.  Your First Design Doc        ← updated: reframed vs ADRs
8.  Configuration Deep Dive
9.  Testing Strategy
10. Dev Workflow Guide            ← updated: enforcement layer referenced here
11. Common Pitfalls              ← updated: new pitfalls for hook and doctrine
```

Removed: §9 "Known Issues & First Fixes" ("Previously fixed" sub-section). Rationale: see Job 3.

The order matters. A cloner who strips `geo.py` before reading the doctrine section doesn't know they need to keep the entire `.claude/skills/` tree. The new §3 "Doctrine Infrastructure" runs immediately after the checklist so the cloner understands the full `.claude/` scope before touching anything.

---

## Job 2 — Section Drafts

### New §3: Doctrine Infrastructure

---

**What this section is**: The 2026-05-19 doctrine cycle added four categories of infrastructure that every project cloned from this template inherits. Unlike utility modules (`geo.py`, `excel.py`), these are not optional — they are the foundation for how agents and humans understand your project. You do not remove them; you fill them in for your project.

#### LANGUAGE.md — your project's glossary

`LANGUAGE.md` at the repo root is a one-sentence-per-term glossary of your project's domain vocabulary. It prevents agents from using two words for the same thing and prevents reviewers from disagreeing about terminology in code review.

**What to do**: The template ships with the `utils` project's terms (decision science, escalation ladder, governance). Replace the example sections with your project's actual domains. Keep the meta-structure: bold term, one-line definition, `_Avoid:_` synonyms when ambiguity exists. Remove any section that doesn't apply to your domain.

The `maintaining-ubiquitous-language` skill (`.claude/skills/maintaining-ubiquitous-language/SKILL.md`) handles ongoing maintenance automatically — agents invoke it when new terms emerge.

**Minimum viable LANGUAGE.md on Day 1**: delete every section from the template, add three to five terms that your domain actually uses, and ship it. You can grow it as your project's vocabulary stabilizes.

#### CONTEXT.md — what your project is

`CONTEXT.md` at the repo root is a one-page narrative covering project identity, mission, current state, key constraints, and the reading order for new contributors and agents. It is the first file any agent or human should read when introduced to your project.

**What to do**: Replace every section with your project's content. The structure (Identity, Mission, Current State, Constraints, Key Relationships, Reading Order, Distinguishing Table) is intentionally preserved — it is the template's value, not the `utils`-specific content filling it.

Critical substitution: the Constraints section currently lists `utils`'s three Pillars (Simplicity First, Shift-Left Testing, Config-Driven). Replace with your project's Pillars. See §6 (Defining Your Project) for how to choose them.

The `maintaining-project-context` skill handles ongoing maintenance.

#### ADR system — recording decisions that matter

Architecture Decision Records live in `docs/adr/NNNN-slug.md`. The triple-filter gate is the core discipline: write an ADR **only when** a decision is (1) hard to reverse, (2) surprising without context, and (3) the result of a real trade-off. All three must be true; if any fails, document it in a commit message or session doc instead.

The template ships with `docs/adr/ADR-FORMAT.md` (the format spec) and `docs/adr/0001-directory-form-mandatory-for-new-skills.md` (a worked example). ADR-0001 captures the decision that new skills must use directory form — this applies to your repo too, because you're adopting SKILLS_FRAMEWORK v2. Update the Decision-maker(s) field to attribute it to your team.

The `recording-architecture-decisions` skill refuses to write an ADR when any filter condition fails — it will redirect you to a commit message or session doc instead.

**Day 1 action**: no new ADRs needed. ADR-0001 is your starting record. Write your next ADR when the first genuinely hard-to-reverse, surprising, contested decision arises.

#### Skills Framework v2 — how skills are organized

`.claude/skills/SKILLS_FRAMEWORK.md` defines the current skill layout. All Level 0 skills (shift-left-testing, configuration-management, python-venv-management, maintaining-ubiquitous-language, maintaining-project-context, recording-architecture-decisions) are portable to any project — do not modify them. Add Level 1 project-specific skills in directory form as your domain requires them.

The directory form mandate (ADR-0001) means every new skill, regardless of size, starts as `.claude/skills/<name>/SKILL.md` plus optional sidecars.

---

### New §4: Test-First Enforcement Layer

---

The shift-left-testing skill describes the discipline. The enforcement layer makes it stick even when agents don't read the skill. This section explains the mechanism and the one substitution you must make for it to work.

#### The PostToolUse audit hook

A shell script at `.claude/hooks/post-tool-shift-left-audit.sh` fires after every `Write` or `Edit` tool call. For any edit to a file in `src/<yourpackage>/**/*.py`, the hook checks whether a corresponding test file exists at `tests/**/test_<basename>.py`. If no test partner exists, it logs a `MISSING_TEST` entry to `.claude/audits/shift-left-violations.log` and emits a warning the agent sees in its tool result. The hook never blocks — it produces an audit trail.

The full enforcement gradient (probabilistic → deterministic) is documented in `.claude/skills/shift-left-testing/ENFORCEMENT.md`. The MAUT that chose soft-deterministic (log + warn) over hard-block (reject tool call) is at `docs/reviews/20260519_pass4_enforcement_maut.md`. Short version: hard blocks punish legitimate refactors and exploratory edits, and agents route around them trivially; the soft audit produces durable evidence without false positives.

#### The required path substitution

The hook ships pre-configured for the `utils` template package name: `*/src/myproject/*.py`. **If you do not change this, the hook matches nothing and silently logs nothing.** This is the failure mode the Pass 5 grill flagged as worst-case — the hook appears installed but does nothing.

Find this block in `.claude/hooks/post-tool-shift-left-audit.sh`:

```bash
case "$file_path" in
    */src/myproject/*.py) ;;
    *) exit 0 ;;
esac
```

Replace `myproject` with your package name. Examples:

```bash
# Single package named "myapp"
*/src/myapp/*.py) ;;

# Any package under src/ (wildcard — catches all)
*/src/*/*.py) ;;

# Two specific packages (pipe syntax — no parentheses)
*/src/pkg1/*.py|*/src/pkg2/*.py) ;;
```

**Important**: do not use `(pkg1|pkg2)` parenthesis syntax — that is regex/extglob and is invalid in plain bash `case` patterns. The script does not enable `extglob`. The correct multi-package form uses `|` between full patterns, as shown above.

#### Installation checklist

Do these steps **after** Step 1 (rename) and **before** your first commit:

1. Substitute the package path glob (above).
2. `chmod +x .claude/hooks/post-tool-shift-left-audit.sh`
3. Verify `jq` is installed: `command -v jq || echo "install jq"` — the hook requires it.
4. Merge the hook block into `.claude/settings.json`. Do NOT replace the whole file — merge only the `hooks.PostToolUse` block. See `docs/doctrine-updates.md` §7 step 5 for the exact JSON and the Case A / Case B merge instructions.
5. Add `.claude/audits/` to your `.gitignore`.
6. Smoke-test: edit any real file in `src/<yourpackage>/` via Claude Code, then check `tail -1 .claude/audits/shift-left-violations.log` for a fresh entry.

#### Per-developer override

Any developer who needs to disable the hook locally can add an override to `.claude/settings.local.json` (gitignored). The shipped `.claude/settings.json` is team-wide. Do not remove the hook from the team config to satisfy one person's preference — use the local override.

---

### Updated §2: Day-1 Checklist — new steps to insert

The following steps belong in the checklist. Insert Step 5 (doctrine) between the current "Verify tests pass" and "Update the task list" steps. Insert Step 6 (hook) immediately after.

---

#### Step 5: Fill in doctrine artifacts

These files ship as templates. Fill them in now, before you forget:

| File | Action |
|------|--------|
| `CONTEXT.md` | Replace all `utils`-specific content (Identity, Mission, Constraints, Pillars) with your project's. Keep the section headings and the Distinguishing Table at the bottom. |
| `LANGUAGE.md` | Delete the example sections. Add 3–5 terms your project actually uses. The structure (bold term, one line, `_Avoid:_`) stays. |
| `docs/adr/0001-directory-form-mandatory-for-new-skills.md` | Update the `Decision-maker(s)` field to name your team. The decision itself carries over. |

Do not skip CONTEXT.md — it is the first file agents read when they orient. `utils`-specific content in it will confuse every agent you deploy.

#### Step 6: Configure the enforcement hook

See §4 (Test-First Enforcement Layer) for the full procedure. Minimum steps here:

```bash
# 1. Substitute the path glob (replace "myproject" with your package name)
#    Edit .claude/hooks/post-tool-shift-left-audit.sh — find the case block

# 2. Make it executable
chmod +x .claude/hooks/post-tool-shift-left-audit.sh

# 3. Verify jq is available
command -v jq || echo "install jq first"

# 4. Add audits dir to gitignore
echo ".claude/audits/" >> .gitignore
```

Then merge the `hooks.PostToolUse` block into `.claude/settings.json` per §4.

---

### Updated §5: What to Keep, Evaluate, or Remove — reclassification

Insert the following as a new top-level category before "Standards (follow everywhere)":

---

#### Required: Fill in for your project (not optional, not removable)

These artifacts ship as templates. They do not have optional deps and are not candidates for removal. Removing them degrades agent orientation quality across every session.

| Artifact | What to do |
|----------|------------|
| `CONTEXT.md` | Fill in your project's identity, mission, and Pillars. See §3. |
| `LANGUAGE.md` | Replace with your project's domain terms. See §3. |
| `docs/adr/` | Keep. Update ADR-0001's Decision-maker(s) field. Add new ADRs as warranted. |
| `.claude/skills/` (entire tree) | Keep intact. Level 0 skills are universal — do not modify. Add Level 1 skills as your domain requires. |
| `.claude/hooks/post-tool-shift-left-audit.sh` | Keep. **Substitute the path glob** (see §4). |
| `docs/adr/ADR-FORMAT.md` | Keep. It is the spec your ADRs must follow. |

---

---

## Job 3 — Removals and Rewrites

### §4 "Defining Your Project" — redirect away from `docs/design/pillars.md`

**Current state** (§219): "The template's three pillars (`Simplicity First`, `Shift-Left Testing`, `Config-Driven`) are examples. Replace them with your project's actual constraints. The format in `docs/design/pillars.md` is the right structure..."

**Problem**: `docs/design/pillars.md` exists but is an unfilled template scaffold — it has the heading and instructions but zero pillars. Sending the cloner there gives them a blank file with no examples. The actual filled-in pillar content now lives in `CONTEXT.md` (Constraints section) and `config/project.yaml` (pillars field).

**Proposed rewrite for this paragraph**:

> The template's three Pillars (Simplicity First, Shift-Left Testing, Config-Driven) are placeholders. They are defined in the Constraints section of `CONTEXT.md` and tracked in `config/project.yaml` under `pillars`. Replace them with your project's actual constraints when you fill in `CONTEXT.md` in Step 5 of the checklist. The format: one-sentence rule, "why this matters for this project," two or three concrete guidelines, and a violation example — the violation is the most important part, because without it a Pillar is aspirational rather than enforceable.
> 
> Aim for 3–5 Pillars. More than five means you haven't prioritized. Pillars that survive code review are the ones that have violation examples specific enough to apply at PR time.

`docs/design/pillars.md` should either be filled in as the project's actual pillar document or deleted. It should not be referenced in the playbook in its current unfilled state.

### §5 "Your First Design Doc" — reframe vs ADRs, do not remove

**Current state**: The section teaches a generic design doc format (Problem Statement, Scope, Key Decisions, Architecture Sketch, Success Criteria). This is good and should stay.

**The tension**: The ADR system now handles "Key Decisions" in a formalized way. The playbook needs to clarify the boundary so the cloner doesn't write an ADR for every decision in a design doc.

**Proposed insertion** at the end of §5 (after the current close):

> **Design doc vs ADR**: the Key Decisions table in a design doc captures all the decisions you thought about. An ADR captures only the decisions that pass the triple filter (hard to reverse, surprising without context, real trade-off). Most decisions from a design doc will NOT warrant an ADR — they belong in the design doc, or in commit messages. Write the design doc first; write an ADR only if the decision passes the filter on reflection.

### §9 "Known Issues & First Fixes" — remove the "Previously fixed" sub-section

The three current "Informational" items (no README, no CI, optional-dep coverage) are genuine forward-looking gaps. Keep them.

The "Previously fixed" sub-section (7 bullet points referencing fixes from 2026-03-17 and 2026-03-31) has negative value for a new cloner. It describes problems that no longer exist in the template. A cloner reads it, doesn't recognize the problems, and spends time verifying that none apply to their clone. The git log is the authoritative record of what was fixed and when; the playbook should not duplicate it.

**Proposed action**: delete the "Previously fixed" sub-section entirely. It clutters the page and misleads readers into thinking they need to verify historical issues.

### §10 "Common Pitfalls" — two new pitfalls to add

**Add**:

> **Skipping the path substitution in the audit hook.** If `*/src/myproject/*.py` remains in `.claude/hooks/post-tool-shift-left-audit.sh` after your rename, the hook matches nothing and logs nothing. You will not see an error — the hook still exits 0. Check `tail -5 .claude/audits/shift-left-violations.log` after editing any source file; if the log is empty or stale, the substitution was missed.
>
> **Leaving `CONTEXT.md` with `utils` content.** Every agent you deploy reads `CONTEXT.md` to orient. If it still describes the template's missions and downstream consumers, your agents will operate with the wrong model of what the project is. Fill it in as part of Day-1 cleanup, not "eventually."

---

## What We Should NOT Add

The doctrine cycle introduced several artifacts that do NOT belong in this Day-1 playbook:

**`docs/propagation-protocol.md`** — this governs how a hub repo propagates doctrine to downstream consumers. The `utils` template is the only current hub repo. A cloner's project is a downstream consumer, not a hub. The propagation protocol is irrelevant to their Day-1 experience. Do not explain it in the playbook; do not even mention the file by name. The only acknowledgment needed is "if your project will itself serve as a doctrine source to other repos, consult `docs/propagation-protocol.md`" — and that belongs at the bottom of §3, not as a section.

**The doctrine-updates.md format and append-mode semantics** — these are maintenance artifacts for the hub. A cloner inherits `docs/doctrine-updates.md` as a reference file; they will receive entries into it when the propagation script runs. The Day-1 playbook should not explain how entries are authored.

**The MAUT decision-science subpackage** — §3 already handles this correctly under "Evaluate (domain-dependent)." No structural changes needed here. The decision-scientist agent is already in the agent table in §8. Do not add a separate section for it.

**The full enforcement gradient table** (layers 1–6 from `ENFORCEMENT.md`) — the Day-1 reader needs to know what the hook does and how to configure it. They do not need the full Layer 1–6 gradient on Day 1. Point to `ENFORCEMENT.md` for the full picture; summarize layer 4 only in §4.

**Session doc format details** — `docs/session-doc-format.md` now owns this. Do not replicate the body template or edge-type taxonomy in the playbook. One sentence pointing at the file is enough.

---

## Summary of Changes to Commission

| Section | Action | Who |
|---------|--------|-----|
| §2 Day-1 Checklist | Add Step 5 (doctrine fill-in) and Step 6 (hook config) | Rewrite (this doc has the text) |
| §3 What to Keep | Add "Required: Fill in for your project" category at top | Rewrite (this doc has the text) |
| §4 Defining Your Project | Replace `pillars.md` reference → `CONTEXT.md` + `config/project.yaml` | Rewrite (this doc has the text) |
| §5 Your First Design Doc | Add design-doc-vs-ADR clarification at end | Insertion (this doc has the text) |
| §9 Previously fixed | Delete sub-section entirely | Deletion |
| §10 Common Pitfalls | Add two new pitfalls | Insertion (this doc has the text) |
| New §3 (renumbered) | "Doctrine Infrastructure" — insert after current §2 | New section (this doc has the full draft) |
| New §4 (renumbered) | "Test-First Enforcement Layer" — insert after new §3 | New section (this doc has the full draft) |

Stale facts (test count at 189, agent count, Python version in §1 overview) are deferred to the parallel Pass 6 code-reviewer audit.
