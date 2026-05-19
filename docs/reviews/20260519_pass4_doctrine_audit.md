# Review: Pass 4 Doctrine Artifact Audit (Pre-Propagation Fresh-Eyes)

**Author**: code-reviewer
**Date**: 2026-05-19
**Type**: Doctrine audit / Enforceability audit / Pre-propagation gate

---

## Scope

Two jobs:

1. **Re-audit the doctrine artifacts** committed in `cf946b5` and `54c0022` (LANGUAGE.md, CONTEXT.md, ADR system, three new skills, three refactored skills, SKILLS_FRAMEWORK v2, propagation-protocol.md, session-doc-format.md, slimmed session-end command) against the 5-question propagation gate.
2. **Enforceability audit of shift-left-testing** — does anything in this repo deterministically force test-first work, or is the skill purely advisory?

Trust-but-verify discipline applied to the prior-session Pass 2 audit, which itself flagged a false positive (the PROJECTS_DIR concern). I re-verified that one myself.

This audit modifies nothing.

---

## Summary

- **Doctrine artifacts**: structurally sound. Pass 2's pre-commit fixes all landed. The three "material" findings from Pass 2 (README drift, configuration-management duplicate, shift-left-testing version) are resolved.
- **Two carry-overs remain**: the per-artifact **adoption-mode table** still does not exist (because the doctrine entry has not yet been written), and the **11-vs-18 count** is resolved in prose but the protocol's roster still says 18 with no caveat about the 11.
- **One newly-introduced inconsistency**: `shift-left-testing` jumped from 1.0.0 → 2.0.0, skipping the 1.1.0 version that the Pass 2 audit recommended for the vertical-slicing add. The audit trail in `**Previous version**: 1.1.0` (SKILL.md:102) is now historically incorrect — 1.1.0 was never committed.
- **Enforceability**: the discipline gradient is GAP-heavy. Nothing in the repo today would prevent a python-prototyper subagent from writing `src/myproject/foo.py` without a failing test for it. CLAUDE.md, pcc.md, pci.md, and the python-prototyper agent definition all mention testing in general terms but none mandate test-first.
- **Pre-propagation verdict**: **GO-WITH-FIXES**. Three fixes blocking propagation (one of them just-write-the-entry); two enforceability gaps recommended-but-not-blocking; ~10 surface findings that can ship with the entry or in a follow-up commit.

---

## Findings — Doctrine Artifacts

### FAIL — 0

(None.)

### CONCERN

**1. `shift-left-testing` version history is now broken (CONCERN)** — `.claude/skills/shift-left-testing/SKILL.md:4` declares `version: "2.0.0"`; line 102 says `**Previous version**: 1.1.0 single-file at .claude/skills/shift-left-testing.md`. But 1.1.0 was never committed — git history goes from a 1.0.0-era single file directly to the 2.0.0 directory form. Pass 2 audit recommended the bump to 1.1.0 for the vertical-slicing section; instead, that change rolled into the 2.0.0 directory refactor in Wave 2. The "Previous version: 1.1.0" claim is historically misleading. Fix: either change line 102 to "Previous version: 1.0.0 (vertical-slicing section added in the same change that restructured to directory form)" or add an explanatory note.

**2. Doctrine entry for the Pass 2 + Wave 2 sprint has not been drafted (CONCERN — propagation blocker)** — `docs/doctrine-updates.md` ends at the 2026-04-21 entry. No 2026-05-19 entry exists. Per the propagation protocol's Batching Rule 1 ("One propagation cycle = one entry") and the Pass 2 audit's blocker 7.A (per-artifact adoption-mode table), this entry has to be written before propagation. Nothing about the artifacts themselves is wrong — the entry is just missing. Until it exists, propagation cannot proceed.

**3. Adoption-mode table still has no home (CONCERN)** — The protocol's Evaluation Gate (lines 30–38) does not require the proposer to classify each affected artifact as template-copy / customize-per-repo / skip. Pass 2 flagged this; Pass 2 also implicitly punted it to "the doctrine entry will include the table". Since the entry doesn't exist yet, there's still no enforcement that the table will exist. Recommend amending propagation-protocol.md to add a 6th question: *"For each artifact this entry affects, what is the adoption mode (template-copy / customize-per-repo / skip)?"*

**4. 11-vs-18 count: resolved in prose, but the protocol still leaves the reader to do math (CONCERN)** — CONTEXT.md:34, CONTEXT.md:67, and LANGUAGE.md:81 now read "most recent cycle (2026-04-21) reached 11 repos; the current discoverable roster is larger" and point to the protocol. The protocol (lines 169–172) lists 18 names but **does not say** "11 of these have consumed prior updates; 7 are newly-discovered." A downstream maintainer reading the protocol still sees 18 names with no indication of consumption history. Fix: add one sentence at protocol:168 — "Of these, ~11 have consumed prior updates; the remainder are newly discovered and unread."

**5. Crosswalk table still triplicated (CONCERN)** — Pass 2 flagged this; no fix landed. The Military↔Civilian table appears in LANGUAGE.md (113–124, 9 rows), SKILLS_FRAMEWORK.md (242–253, 9 rows), and propagation-protocol.md (143–149, **7 rows — missing `backbrief` and `METL`**). Three copies will drift. Recommendation unchanged: protocol's `## Civilian/Military Vocabulary` should be a one-line pointer to LANGUAGE.md.

**6. Skill descriptions still two-sentence despite "one sentence" rule (CONCERN)** — Pass 2 flagged this. `maintaining-ubiquitous-language/SKILL.md:3` is two sentences. `maintaining-project-context/SKILL.md:3` is two sentences. `recording-architecture-decisions/SKILL.md:3` is two sentences. SKILLS_FRAMEWORK.md:80 still says "**One sentence.**" Soften the rule (recommended — the descriptions read well) or compress the descriptions. Pick one.

**7. `recording-architecture-decisions` skill cross-link assumes a co-propagated file (CONCERN)** — SKILL.md:51 and SKILL.md:78 both link to `../../../docs/adr/ADR-FORMAT.md`. If the skill is propagated without the format doc, those links break. The Pass 2 audit raised this as 7.D; it remains true. The doctrine entry (when written) must instruct downstreams to install both as a bundle. Add to the adoption-mode table.

**8. `recording-architecture-decisions/SKILL.md:60` find-next-number command still fragile (CONCERN)** — `ls docs/adr/ | tail -1` returns `ADR-FORMAT.md` for an empty repo (no real ADRs yet), since `ADR-FORMAT.md` sorts after the hypothetical `0001-*`. Same issue Pass 2 flagged on ADR-FORMAT.md:113. Fix: `ls docs/adr/ | grep -E '^[0-9]{4}-' | tail -1 || echo "0000"`. Two files have this same fragile command; one fix can land in both.

**9. `recording-architecture-decisions/SKILL.md:31` example incorrectly uses append-mode as an ADR-worthy example before the actual ADR exists (CONCERN, minor)** — The skill says "Adopting append-mode in the doctrine propagation script over overwrite-mode" passes the triple filter and warrants an ADR. The propagation-protocol.md:90 confirms "Adopted 2026-03-30." But there is no `docs/adr/0001-append-mode.md` in the repo. The skill's worked example pointedly references a decision that should have been an ADR but isn't. Two possible fixes: (a) actually write ADR-0001 for append-mode (the Pass 2 audit's "First ADR" next-step said this was a better first candidate than the single-commit-vs-split-commits question); or (b) change the example to a hypothetical decision so the skill doesn't advertise a missing ADR. Recommend (a) — it's small and demonstrates the discipline.

**10. SKILLS_FRAMEWORK.md "task management" still under Level 0 (CONCERN)** — Pass 2 flagged this as 9.D; not fixed. SKILLS_FRAMEWORK.md:159–165 has "### task management (command: `/task`)" inside the `## Level 0: Universal Foundation Skills` section, contradicting line 287 which says task is a command not a skill. Either move it out of the Level 0 section into a "Commands referenced for completeness" subsection, or remove the entry entirely (it's already covered by `.claude/commands/task.md`).

**11. CONTEXT.md "Reading Order" still omits `docs/adr/` (CONCERN, minor)** — Pass 2 raised this as 3.B. CONTEXT.md:84–92 lists 7 reading-order entries; `docs/adr/` is missing despite being referenced in the artifact-distinguisher table on line 105. Either add as #8 ("only when proposing a hard-to-reverse decision") or accept the omission. Minor.

**12. `_Avoid:_` line ends inconsistently across LANGUAGE.md entries (CONCERN, stylistic)** — Most entries follow `_Avoid:_ word1, word2, word3.` with a trailing period. `Scenario` (line 33) ends without trailing period after `profile (already used for environment config).` — wait, that one does close-paren-period correctly. Re-checked: the convention is consistent. Withdrawn.

**13. `.claude/README.md:46` lists three new directory-form skills but not their sidecars (CONCERN, minor)** — The tree at .claude/README.md:39–45 names the directory-form skills with sidecar counts ("+ 5 sidecars", "+ 7 sidecars") for the three refactored skills, but doesn't note that the three new skills (`maintaining-*`, `recording-*`) have **no** sidecars yet. That's accurate but a reader can't tell from the tree whether sidecars are missing-by-design or just not-yet-written. One-line note: "(no sidecars — SKILL.md self-contained at <110 lines each)" would resolve.

**14. `docs/session-doc-format.md` not in propagation-protocol roster of artifacts (CONCERN, minor)** — When the doctrine entry is written, `docs/session-doc-format.md` needs to ship as part of the bundle (otherwise `.claude/commands/session-end.md:61` breaks downstream — the command points at the format doc, which won't exist if propagation skips it). Add to the adoption-mode table as template-copy.

### OK / PASS

**15. PROJECTS_DIR description in propagation-protocol.md is CORRECT (OK)** — Re-verified manually: `PROJECTS_DIR = UTILS_ROOT.parent.parent` resolves to `/home/jhutchison/projects/` from this checkout at `/home/jhutchison/projects/github/utils/`. The protocol's "recursive scan of `~/projects/`" is accurate. The Pass 2 auditor mis-counted `.parent` calls (correctly self-corrected in their own report). Do not "fix" what isn't broken. Repeating the correction here so the next audit doesn't reopen it.

**16. `.claude/README.md` skills tree updated for new layout (OK)** — Pass 2's pre-commit fix landed cleanly. The deleted `session-end.md` is gone from the skills tree; the three new directory-form skills are listed; the retirement note at line 48 explains the move.

**17. SKILLS_FRAMEWORK.md `configuration-management.md` duplication fixed (OK)** — Pass 2 flagged the doubled name in the Level 0 paragraph; verified resolved. The name now appears once at line 336 in the retired-skills list.

**18. session-end deduplication clean across all surfaces (OK)** — Skill file gone, command file updated, format reference moved to docs, SKILLS_FRAMEWORK.md inventory and README skills tree both updated. Provenance documented in `docs/session-doc-format.md:197`.

**19. settings.local.json → settings.json rename complete (OK)** — Only reference remaining is the historical mention in the session doc. No live references to settings.local.json anywhere in `.claude/`, `docs/`, or `CLAUDE.md` (other than the session doc itself, which is the right place for the history).

**20. ADR triple-filter present in three places (defense in depth) (OK)** — `recording-architecture-decisions/SKILL.md:15–19`, `docs/adr/ADR-FORMAT.md:14–19` (block quote), and `docs/adr/ADR-FORMAT.md:36–44` (checklist in the ADR template itself). Defense in depth as designed.

---

## Enforceability of shift-left-testing

This section addresses the user's central concern: VERTICAL-SLICING.md says "without explicit discipline, both agents and humans tend to write horizontal slices." The skill exists. What forces it to be used?

**E1. Does the skill state its enforcement gradient honestly? — WEAK** — `VERTICAL-SLICING.md:8–10` acknowledges the failure mode in clear terms but stops there. The skill does not say "this skill is advisory; nothing in this repo enforces it." A reader could plausibly believe the skill is binding. Recommend adding to SKILL.md or VERTICAL-SLICING.md: "**Enforcement gradient**: this skill is *probabilistic* — Claude loads the description into context at session start, but whether the body and rules actually shape an implementation turn depends on Claude noticing the trigger. There are no hooks or pre-commit gates that block code-without-test commits today. See `docs/tasks.md` if you want this upgraded to deterministic enforcement."

**E2. Anything in repo that prevents python-prototyper from writing `src/foo.py` with no failing test? — GAP** — Read `.claude/agents/python-prototyper.md`. Line 36 says "Write tests alongside the code in `tests/`." No `test-first`, no "RED-GREEN", no refusal clause. The agent has Write access to `src/myproject/`, `tests/`, and `config/` with no precondition that the test must exist first. There is no hook in `.claude/settings.json` (which contains zero hooks — only permissions and env). There is no git pre-commit hook. There is no CI gate (no `.github/workflows/` directory at all). A python-prototyper subagent can — and the repo will let it — write the implementation first.

**E3. Does CLAUDE.md mandate TDD? — GAP** — CLAUDE.md:6–9 (`### Shift-Left Testing`) says "Every new component must include a test plan. Tests are written alongside code, not as an afterthought." "Alongside" is intentionally ambiguous. Neither "test-first" nor "TDD" appears anywhere in CLAUDE.md. The user's recurring concern (probabilistic enforcement) is not addressed at the most-loaded surface in the repo.

**E4. Does pcc.md enforce test-first ordering? — GAP** — `.claude/commands/pcc.md:33–38` runs pytest as Step 2 and fails if any test fails. That enforces "tests must pass before push" — not "tests must exist before code". A commit with no tests at all passes PCC trivially (no failing tests). The check is symmetric: code with no tests is indistinguishable from no code with no tests.

**E5. Does pci.md enforce test-first ordering? — WEAK** — `.claude/commands/pci.md:65–67` says "New functions/classes have corresponding tests?" as a manual checklist item. That's a question Claude has to answer truthfully, not an automated check. The pillar gets verbal lip service ("Coverage for new code"); there is no diff-aware enforcement (e.g., "every new `def` in `src/` must have at least one matching `test_*` reference"). A motivated-to-skip subagent or human can check this box without it being true.

**E6. python-prototyper agent definition does NOT instruct test-first — GAP** — Re-read `.claude/agents/python-prototyper.md:28–37` ("Your Workflow"): step 3 is "Implement the code", step 4 is "Write tests alongside the code". The order in the agent's own documentation is **code first, tests second**. This actively undermines the shift-left pillar at its enforcement surface. Fix: invert steps 3 and 4, or rewrite as a unified red-green loop. Cite `.claude/skills/shift-left-testing/VERTICAL-SLICING.md` explicitly.

**E7. No hooks in `.claude/settings.json` — GAP (deterministic-enforcement gap)** — The Anthropic settings schema supports `hooks` (e.g., `PreToolUse` matchers that can block tool calls). The current `.claude/settings.json` has `env` and `permissions` only. A `PreToolUse` hook keyed on `Write` to `src/myproject/**` could in principle check for a corresponding `tests/**/test_*.py` and block if absent. The repo does not use this capability. This is the only available path to deterministic enforcement of test-first discipline within the agent runtime, and it is unused.

**E8. No git pre-commit hook either — GAP** — No `.git/hooks/pre-commit` script, no `.pre-commit-config.yaml`, no Husky/lefthook config. PCC (`/pcc`) is a slash command that the user has to invoke; it is not automatically run by git.

**E9. No CI workflow — GAP** — No `.github/workflows/` directory exists (`Next Steps` in the session doc carries "GitHub Actions CI workflow (P3, carried from 2026-04-21)" — this work has been deferred since April). Without CI, the only place a missing-test condition could be detected outside the user's local PCC invocation is in the next session's `/session-start` health check, which currently doesn't include this check either.

### Enforceability summary

| Surface | What it does today | Enforcement class |
|---|---|---|
| `shift-left-testing` skill | Describes discipline | WEAK (probabilistic) |
| `VERTICAL-SLICING.md` | States the rule explicitly | WEAK (probabilistic) |
| CLAUDE.md | "Tests alongside code" | GAP (no ordering rule) |
| python-prototyper agent | Workflow lists code-then-tests | GAP (actively wrong) |
| `/pcc` | Runs tests, fails if any fail | GAP (silent on missing tests) |
| `/pci` | Asks manual question | WEAK (self-report) |
| `.claude/settings.json` hooks | None defined | GAP (capability unused) |
| Git pre-commit hooks | None | GAP |
| CI workflow | Doesn't exist | GAP |

**Material conclusion**: The skill exists and reads well. Nothing in the repo causes it to be applied. The combination of E2 + E6 + E7 is the load-bearing finding — to move from probabilistic to deterministic enforcement, the minimum-viable change set is: (a) invert the python-prototyper workflow to test-first; (b) add a `PreToolUse` hook in settings.json that, when Write or Edit targets `src/myproject/**/*.py`, checks for a corresponding test file and blocks if absent; (c) update CLAUDE.md to state the ordering rule.

This is **not** scoped into the propagation; it's surfaced here because the user asked, and because shipping the shift-left-testing skill to 11 downstreams while it is probabilistic-only at upstream is honest only if the skill itself says so.

---

## Pre-Propagation Verdict

**GO-WITH-FIXES.** Three blocking fixes, all narrow. Two recommended-but-not-blocking. Everything else can ship in the doctrine entry or in a follow-up commit.

### Blocking (must land before propagation)

1. **Write the 2026-05-19 doctrine entry in `docs/doctrine-updates.md`.** Without it the propagation script has nothing to extract. The entry must include:
   - Per-artifact adoption-mode table (template-copy / customize-per-repo / skip), specifically:
     - LANGUAGE.md, CONTEXT.md → customize-per-repo (keep structure, replace content)
     - propagation-protocol.md → skip (utils-only)
     - session-doc-format.md, ADR-FORMAT.md, the three new skills, SKILLS_FRAMEWORK v2 → template-copy
     - shift-left-testing v2 directory restructure → template-copy (replace, not append — the file structure changed)
     - configuration-management, python-venv-management v2 → template-copy (replace)
     - session-end skill deletion → mirror the dedup
   - Bundle constraint: `recording-architecture-decisions` skill and `docs/adr/ADR-FORMAT.md` ship together or neither (broken cross-link otherwise).
2. **Fix shift-left-testing/SKILL.md:102** — the "Previous version: 1.1.0" claim is historically false. 1.1.0 was never committed. Either correct the line or add a parenthetical clarifying that vertical-slicing was added in the same change that restructured to directory form.
3. **Add the 6th question to the Evaluation Gate** in `docs/propagation-protocol.md` requiring per-artifact adoption-mode classification on every future doctrine entry. This is what closes the F3 propagation-cost gap structurally rather than per-entry.

### Recommended (not blocking)

4. Add an enforcement-gradient note to `shift-left-testing/SKILL.md` or `VERTICAL-SLICING.md` so the skill does not silently overpromise.
5. Invert the python-prototyper workflow to test-first and cite the skill — small change, large signal.

### Surface fixes (can ship in the entry or as a follow-up commit)

6. Crosswalk consolidation (LANGUAGE.md canonical; protocol and framework reference it).
7. Skill description rule reconciliation (one sentence vs two-sentence reality).
8. `ls docs/adr/ | tail -1` fragile-command fix in both ADR-FORMAT.md and the skill.
9. Move "task management" out of the Level 0 skill section in SKILLS_FRAMEWORK.md.
10. Add `docs/adr/` to CONTEXT.md reading order (#8, conditional).
11. Add the 11-vs-18 caveat to the protocol's roster section.
12. Write ADR-0001 for append-mode (or update the skill example to not reference an unwritten ADR).
13. One-line note on the new-skills-have-no-sidecars-by-design in `.claude/README.md`.

---

## Patterns Carried Forward (Agent Memory)

- **Doctrine entry is the load-bearing artifact for propagation**. The artifacts themselves can be perfect; without the entry the script propagates nothing. A future audit should always check `docs/doctrine-updates.md` head before pronouncing propagation-ready.
- **"Probabilistic vs deterministic" enforcement is now a vocabulary distinction worth carrying**. Several skills in this repo (and others) describe disciplines that are not enforced. Surfacing the gradient explicitly in the skill itself prevents over-promising.
- **Trust-but-verify checked out**: the prior auditor's self-corrected error on PROJECTS_DIR really was wrong. Recurring lesson: when a script uses `.parent.parent`, count the path segments explicitly before flagging.

---

**End of audit.**
