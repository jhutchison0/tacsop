# Session: Shift-Left Enforcement Layer + Doctrine Propagation Prep

**Date**: 2026-05-19
**Branch**: main
**Tags**: #session #doctrine #agents #infra #skills #hooks #enforcement #adr #propagation-prep

**Documents**: [CLAUDE.md](../../CLAUDE.md) — Shift-Left Testing Development Principle strengthened to test-first
**Documents**: [.claude/skills/shift-left-testing/ENFORCEMENT.md](../../.claude/skills/shift-left-testing/ENFORCEMENT.md) — new sidecar built this session
**Documents**: [.claude/hooks/post-tool-shift-left-audit.sh](../../.claude/hooks/post-tool-shift-left-audit.sh) — the new PostToolUse audit hook
**Documents**: [docs/adr/0001-directory-form-mandatory-for-new-skills.md](../adr/0001-directory-form-mandatory-for-new-skills.md) — first real ADR
**Documents**: [docs/doctrine-updates.md](../doctrine-updates.md) — 2026-05-19 entry authored this session (469 lines, 22-artifact bundle)
**Documents**: [docs/design/from_template_to_project.md](../design/from_template_to_project.md) — Day-1 playbook rewritten 10 → 12 sections
**References**: [docs/reviews/20260519_pass4_doctrine_audit.md](../reviews/20260519_pass4_doctrine_audit.md) — code-reviewer Pass 4
**References**: [docs/reviews/20260519_pass4_enforcement_maut.md](../reviews/20260519_pass4_enforcement_maut.md) — decision-scientist Pass 4 (selected A5 PostToolUse)
**References**: [docs/reviews/20260519_pass4_enforcement_grill.md](../reviews/20260519_pass4_enforcement_grill.md) — proposer Pass 4
**References**: [docs/reviews/20260519_pass5_entry_audit.md](../reviews/20260519_pass5_entry_audit.md) — code-reviewer Pass 5
**References**: [docs/reviews/20260519_pass5_propagation_maut.md](../reviews/20260519_pass5_propagation_maut.md) — decision-scientist Pass 5 (A6 vs A4)
**References**: [docs/reviews/20260519_pass5_grill.md](../reviews/20260519_pass5_grill.md) — proposer Pass 5
**References**: [docs/reviews/20260519_pass6_day1_playbook_audit.md](../reviews/20260519_pass6_day1_playbook_audit.md) — code-reviewer Pass 6
**References**: [docs/reviews/20260519_pass6_day1_playbook_rewrite.md](../reviews/20260519_pass6_day1_playbook_rewrite.md) — proposer Pass 6
**Follows**: [20260519_doctrine_artifact_buildout.md](20260519_doctrine_artifact_buildout.md) — same-day predecessor session
**Cites**: Matt Pocock's `mattpocock/skills` — triple-filter ADR gate (ADR-0001), tracer-bullet TDD discipline (already in shift-left-testing/VERTICAL-SLICING.md, reinforced by the new enforcement layer)

---

## Summary

Three review passes (Pass 4, 5, 6) interleaved with three build phases (enforcement layer, doctrine-updates entry, Day-1 playbook rewrite). The previous session built the doctrine artifacts; this session validated them, added deterministic enforcement, authored the propagation entry, and updated the public-facing Day-1 playbook. Propagation itself was deliberately deferred — the user's stated preference at each fork was *fix everything thoroughly, decide the propagation path with fresh eyes next session*.

The most novel artifact is the PostToolUse audit hook at `.claude/hooks/post-tool-shift-left-audit.sh`. It is the project's first deterministic doctrine-enforcement mechanism — the shift-left-testing skill is now backed by a harness-level audit that logs `MISSING_TEST` / `OK_TEST_EXISTS` on every Write/Edit to `src/myproject/**/*.py`. It never blocks; it produces evidence. The MAUT that selected this design (decision-scientist Pass 4) explicitly rejected hard-block PreToolUse hooks because of false-positive risk on legitimate refactors.

## Work Completed

### Pass 4 — Pre-propagation review of the prior session's doctrine artifacts

Three agents in parallel with the brief "audit before propagation":

| Agent | Headline finding |
|---|---|
| **code-reviewer** | GO-WITH-FIXES verdict. Six pre-propagation blockers including the missing doctrine-updates entry, python-prototyper's code-first workflow (the agent definition itself was undermining shift-left), and the stale `docs/design/pillars.md` reference. Audit also surfaced 5 GAPs and 3 WEAKs on shift-left-testing enforceability — *nothing in the repo deterministically enforces TDD*. |
| **decision-scientist** | MAUT-ranked 10 enforcement alternatives. A5 (PostToolUse soft-audit hook) at 0.778; A6 (Stop hook) at 0.775 — statistical tie. A4 (PreToolUse hard-block) dominated by A8 because false-positive risk is asymmetric: refactors, doc edits, exploratory prototyping all trip a naive block. |
| **proposer** | Bold grill identifying 3 missing pieces (ADR-0001 unwritten, propagation-protocol's missing skill reference, the unfilled `pillars.md` stub). Proposed 5 concrete hook designs with bash sketches; specifically warned *do not block ALL src/ edits* and *do not introduce a new agent to police TDD*. |

User chose A5 (recommended) + ENFORCEMENT.md sidecar in `shift-left-testing/` + defer propagation per scope question.

### Enforcement layer build

Following the Pass 4 synthesis:

| Artifact | Lines | Notes |
|---|---|---|
| `.claude/hooks/post-tool-shift-left-audit.sh` | 95 | `set -uo pipefail` (NOT `-e`); jq-tolerant; matches `*/src/myproject/*.py`; appends to `.claude/audits/shift-left-violations.log`; emits stderr warning the agent sees; always `exit 0`. |
| `.claude/skills/shift-left-testing/ENFORCEMENT.md` | 120 | Documents the 6-layer enforcement gradient (probabilistic → deterministic); explains why we don't hard-block; lists what the hook catches and misses; reading recipes for the audit log; escalation criteria. |
| `.claude/settings.json` (modified) | +14 | `hooks.PostToolUse` block with `$CLAUDE_PROJECT_DIR` for portability; configured via `update-config` skill; env/permissions blocks preserved. |
| `.gitignore` (modified) | +1 | `.claude/audits/` added. |

Pre-propagation fixes from Pass 4:
- `.claude/agents/python-prototyper.md` — workflow inverted to test-first vertical-slice (step 3 = write failing test, step 4 = minimum impl); stale `docs/design/pillars.md` reference repointed to `CONTEXT.md` + `config/project.yaml`.
- `.claude/skills/shift-left-testing/SKILL.md` — corrected false "v1.1.0" version-history line (1.1.0 was never committed); ENFORCEMENT.md added to sidecar list.
- `.claude/skills/shift-left-testing/ANTIPATTERNS.md` — cross-linked to ENFORCEMENT.md.
- `LANGUAGE.md` — removed snapshot agent count from Roster definition (definitions should be stable; counts live in CONTEXT.md).
- `CONTEXT.md` — added `docs/adr/` to the reading order between propagation-protocol.md and sessions/.
- `CLAUDE.md` — Shift-Left Testing Development Principle strengthened to mandate test-first vertical-slice with explicit hook reference.

ADR-0001 written: *directory-form mandatory for all new skills*. First ADR exercising the format established in the prior session. Triple-filter check passes (hard to reverse across 11+ downstream repos; surprising for small skills; real trade-off vs simpler single-file).

**Hook verification in-session**: edited `src/myproject/utils/logger.py` after wiring the hook; `.claude/audits/shift-left-violations.log` got a fresh `OK_TEST_EXISTS` entry within seconds. Settings watcher reloaded without manual intervention.

### Pass 5 — Final gate review of the doctrine-updates entry

User asked for `.claude/agents` to review the propagation entry through the CONTEXT.md *multiplicative-downstream-impact* lens before shipping. Three agents in parallel:

| Agent | Headline finding |
|---|---|
| **code-reviewer** | SHIP-WITH-FIXES verdict. 1 FAIL (the bash `case` blocker), 6 CONCERNs, 8 OKs explicitly verified accurate (settings.json snippet matches the live file byte-for-byte; propagation-script regex extraction simulated and clean; ADR contents match the entry's description; etc.). |
| **decision-scientist** | MAUT on propagation strategy itself, not artifacts. A6 (bundle + author `scripts/adopt_doctrine.py` helper) at 0.760; A4 (pilot to 2–3 friendly repos first) at 0.743. Both within sensitivity noise. Tiebreaker: ship A6 if helper can be authored test-first tonight; ship A4 if not. A3 (three-cycle split) Pareto-dominated; dropped. A1 (status quo) strictly dominated by A6. |
| **proposer** | Confirmed the bash blocker independently by running it (`*/src/(pkg1\|pkg2)/*.py` fails with `syntax error near unexpected token '('` — and because the hook script's `set -uo pipefail` omits `-e`, it silently exits 0). Three HIGH-severity footguns and four structural omissions surfaced. Anti-recommendation: *don't ship 22 artifacts plus a new adoption script in the same cycle*. |

User chose ALL fixes (BLOCKER + HIGH + CONCERN) + commit via /session-end + defer propagation decision per scope question. All fixes applied to the entry. Propagation script regex re-verified after edits (469 lines, clean termination at the 2026-04-21 entry boundary, no internal `## ` collisions).

### Pass 6 — Day-1 playbook rewrite

The `docs/design/from_template_to_project.md` playbook is what someone reads when they clone the template. It predated the entire doctrine cycle. Two agents in parallel:

| Agent | Headline finding |
|---|---|
| **code-reviewer** | 11 FAILs / 10 CONCERNs / 2 OK. Worst-impact: agent count "four" (actual 5), test count "189/8" (actual 192/9), substitution table missing the hook script (silent failure if missed), §7 Testing completely silent on the new test-first mandate. |
| **proposer** | Diagnosed 3 root structural problems: no home for the doctrine artifacts, undocumented hook path substitution (the worst failure mode), §4 sending readers to an unfilled `pillars.md` stub. Proposed 11-section outline with NEW §3 Doctrine Infrastructure and NEW §4 Test-First Enforcement Layer. Drafted both new sections in full. |

Comprehensive rewrite applied. Net result: 569 → 791 lines, 10 → 12 sections, Day-1 Checklist expanded 7 → 9 steps. Tests still green.

## Key Decisions

| Decision | Rationale |
|---|---|
| A5 (PostToolUse soft-audit) over A4 (PreToolUse hard-block) for enforcement | MAUT-dominated outcome. False-positive risk on legitimate refactors/config-edits is asymmetric; soft-deterministic produces evidence over time, hard-block produces only resistance. |
| Author `ENFORCEMENT.md` as a sidecar in `shift-left-testing/` (not a top-level doctrine file) | The sidecar pattern (Skills Framework v2) is the right home. Cross-linked from ANTIPATTERNS.md so it surfaces during related skill use. |
| Defer propagation, fix everything thoroughly | User's explicit choice at three forks (Pass 4 scope, Pass 5 scope, end-of-session strategy). The 22-artifact bundle is the largest cycle ever — Pass 6 wouldn't have surfaced the playbook gap if we'd rushed. |
| ADR-0001 = directory-form mandatory (no line-count trigger) | The prior session's draft SKILLS_FRAMEWORK had a >500-line trigger that every legacy skill in the repo had silently violated. A categorical rule eliminates the per-PR debate; the cost of premature directory form is trivial vs the cost of recurring 1500-line monoliths. |
| Split commit into 3 bundles (enforcement / doctrine-update / playbook) | Bisectability. Each commit is a coherent unit; reverting any one is clean. Matches the prior session's pattern (cf946b5 + 54c0022 + 6bcbb6f). |
| `python-prototyper.md` reclassified TEMPLATE-COPY → CUSTOMIZE | Pass 5 proposer caught hard-coded `src/myproject/` in Project Layout, Scope, and the Shift-Left Testing principle. Downstream repos must substitute. The other agents are TEMPLATE-COPY because they don't have package-path references. |
| Hook script uses `set -uo pipefail` not `-e` | A non-zero exit from the hook is interpreted by the harness as a hook failure, which can suppress or fail the tool call — the opposite of the soft-deterministic stance. Script must always `exit 0`. |
| Day-1 playbook gets NEW §3 Doctrine Infrastructure as its own section, not merged into §5 What to Keep | Doctrine artifacts are "fill in for your project," not "keep or remove." Mixing them with optional utility modules confuses the reader about what's optional. |

## Pillar Compliance

| Pillar | Status | Notes |
|---|---|---|
| **Simplicity First** | PASS | Rejected speculation at three forks (no `scripts/adopt_doctrine.py` this cycle per proposer anti-recommendation; no new agent to police TDD; no hard-block hook). The enforcement layer is one shell script + one settings.json block + one sidecar — minimal surface area for the value delivered. |
| **Shift-Left Testing** | PASS | Three review passes interleaved with three build phases; no commit landed until tests were green. The new enforcement layer literally eats its own dog food — the audit hook fires on every Edit to `src/myproject/`, including edits made during this session. |
| **Config-Driven** | PASS | All hook behavior controlled by `.claude/settings.json`. Per-developer override path via `.claude/settings.local.json`. Audit log path standardized at `.claude/audits/`. No hardcoded paths in the doctrine itself. |

## Three-Pass Agent Disagreements (Surfaced for the Record)

- **Pass 5 MAUT (A6 bundle+helper) vs Pass 5 proposer anti-rec (don't ship helper in same cycle)**: Reconciled by reading A6 as "bundle + helper in follow-on cycle within days" rather than same commit. Both can be true.
- **Pass 4 code-reviewer (recommended minimum-viable A4 PreToolUse + agent rewrite + CLAUDE.md) vs Pass 4 decision-scientist (A5 PostToolUse soft-deterministic)**: Resolved by the MAUT's explicit false-positive scoring — code-reviewer's recommendation was structurally similar but didn't weight the false-positive cost, which the MAUT made central.
- **Pass 6 code-reviewer "11 FAILs" framing vs Pass 6 proposer "3 root problems" framing**: Both correct at different altitudes. The 11 line-level fails roll up into the 3 structural problems the proposer named. The rewrite addressed both.

## Commits

| Hash | Subject | Files | Lines |
|---|---|---|---|
| `c27e1a5` | [infra] Pass 4 + shift-left enforcement layer + ADR-0001 + 5 pre-propagation fixes | 14 | +1005 / −18 |
| `9f2c73b` | [doc] Doctrine update entry for 2026-05-19 cycle + Pass 5 review fixes | 4 | +1098 |
| `395d9e8` | [doc] Day-1 playbook rewrite to reflect 2026-05-19 doctrine cycle (Pass 6) | 3 | +839 / −90 |

Plus this session doc + tasks.md + project.yaml as the fourth commit.

## Next Steps

- [ ] **Sixth doctrine propagation cycle — A4 vs A6 decision**. The MAUT recommendation is A6 (ship bundle + author `scripts/adopt_doctrine.py` helper) if the helper can be authored test-first in one session; A4 (pilot to 2–3 friendly repos first, e.g. rmi-reboot) otherwise. Either way, the doctrine-updates entry is ready; nothing blocks the script run except the human decision.
- [ ] **(If A6 chosen)** Build `scripts/adopt_doctrine.py` test-first under the new shift-left enforcement layer. The helper should: (a) substitute `myproject` → `<yourpkg>` in `.claude/hooks/post-tool-shift-left-audit.sh` and other hard-coded sites; (b) detect existing `.claude/settings.json` and merge the hooks block correctly; (c) report what it changed for human review.
- [ ] **(If A4 chosen)** Run `scripts/propagate_doctrine.py` against the 2–3 pilot repos only; wait 1 week for breakage signals; then propagate to remaining 8.
- [ ] **GitHub Actions CI workflow** (P3, carried). The audit hook only fires inside Claude Code sessions — CI is independent and catches commits made outside the harness.
- [ ] **`from_yaml` round-trip tests for 4 value functions** (P3, carried).
- [ ] **After 1–2 sessions of audit-log data**, decide whether to add a Stop hook (Layer 5) or escalate to PreToolUse hard-block (Layer 6) per `.claude/skills/shift-left-testing/ENFORCEMENT.md` escalation criteria.

## Notes

- The "claude dice" framing the user introduced this session — describing skills as probabilistically invoked and asking for deterministic alternatives — is now first-class doctrine vocabulary. ENFORCEMENT.md uses it explicitly.
- The audit hook caught its first real-world signal already: during Pass 6 verification, an edit to `logger.py` produced an immediate `OK_TEST_EXISTS` log line, proving end-to-end wiring works without a session restart. The settings watcher is reactive.
- Three agent-review passes interleaved with build work is a heavier workflow than usual. It produced 8 review artifacts in `docs/reviews/` for one cycle's worth of build work. The cost was real (long session) and the value was real (one BLOCKER caught at Pass 5 that would have broken the hook in any downstream repo with two packages; one structural gap caught at Pass 6 that would have misdirected every Day-1 clone). For doctrine cycles of this size, the multi-pass pattern is worth the cost. For smaller cycles, a single Pass is fine.
- The Pass 5 decision-scientist explicitly noted the shift-left irony: writing `scripts/adopt_doctrine.py` under our own new TDD mandate means the helper itself must be authored test-first. The audit log will record whether we honored the discipline when we get around to building it.
