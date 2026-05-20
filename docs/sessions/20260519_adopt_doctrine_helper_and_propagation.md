# Session: Adopt-Doctrine Helper + Sixth Propagation Cycle

**Date**: 2026-05-19
**Branch**: main
**Tags**: #session #doctrine #infra #scripts #propagation #shift-left #test-first #complete

**Documents**: [scripts/adopt_doctrine.py](../../scripts/adopt_doctrine.py) — the A6 helper built this session
**Documents**: [docs/doctrine-updates.md](../doctrine-updates.md) — new §23 + artifact #23 in master table
**Implements**: [plans/peppy-stirring-llama.md](~/.claude/plans/peppy-stirring-llama.md) — approved plan for this build
**References**: [docs/reviews/20260519_pass5_propagation_maut.md](../reviews/20260519_pass5_propagation_maut.md) — MAUT that picked A6 over A4
**References**: [docs/reviews/20260519_pass5_grill.md](../reviews/20260519_pass5_grill.md) — proposer Pass 5 with scope-ceiling footguns
**Follows**: [20260519_enforcement_layer_and_propagation_prep.md](20260519_enforcement_layer_and_propagation_prep.md) — same-day predecessor; built the doctrine bundle, deferred A6 vs A4 decision
**Cites**: Matt Pocock's `mattpocock/skills` — tracer-bullet TDD discipline (followed verbatim across all 9 build slices)

---

## Summary

A6 chosen, helper built, propagated. The user's framing — *more water for the horses, the script makes drinking much easier on this massive update* — captured the design constraint exactly: the helper lowers downstream adoption friction without ever pushing files into downstream repos. Built `scripts/adopt_doctrine.py` test-first in 9 vertical slices (35 tests, all green), added as artifact #23 in the 2026-05-19 doctrine entry, then immediately ran `propagate_doctrine.py` to ship the now-23-artifact bundle to 12 downstream repos (5 new notifications, 7 appended).

The helper is the first deliverable in this repo that was authored entirely under the new shift-left enforcement layer's discipline. The audit hook itself does not watch `scripts/`, so there is no audit-log proof — but the slice-by-slice test-first cadence is visible in the commit history and in the test partner's existence.

## Work Completed

### Plan and scope alignment

User asked for clarification on A4 vs A6 from the prior session. Walked through the propagation model (we only ever ship the `doctrine-updates.md` entry; downstream maintainers decide adoption). User confirmed: *"all we are ever shipping is the doctrine update, but it points to the adopt doctrine script; it should always be up to the downstream repos what to adopt … having the script might make drinking much easier on this massive update."* Decision: A6, with the explicit understanding that the script lives in the bundle but the bundle itself is just a notification.

EnterPlanMode → Explore agent mapped four critical inputs (10 `myproject` substitution sites, `.claude/settings.json` structure, existing `propagate_doctrine.py` test patterns, Pass 5 footgun warnings verbatim) → drafted plan with vertical slices and explicit non-goals → ExitPlanMode after the single decision point (same-cycle vs follow-on-cycle ship) was answered "same cycle."

### Build (9 vertical slices, test-first)

Each slice: write failing test, run, observe failure, write minimum implementation, run again, observe green. Then next slice.

| # | Function | Tests | Notes |
|---|---|---|---|
| 1 | `_detect_package` | 4 | Auto-detects from `src/<pkg>/` if exactly one subdir; raises `DetectionError` otherwise |
| 2 | `_plan_copies` | 3 | Returns list of `(src_path, dst_relative, kind)` tuples for 10 verbatim artifacts |
| 3 | `_apply_copies` | 4 | Never overwrites existing targets; dry-run prints only; missing source recorded as error |
| 4 | `_substitute_hook` | 5 | Plain string replace `myproject` → `<pkg>` at 3 known sites; preserves bash `case` syntax; executable bit copied |
| 5 | `_merge_settings` | 5 | The fragile one. Idempotent re-run via `_matcher_already_present`; preserves existing top-level keys and other PostToolUse matchers |
| 6 | `_append_gitignore` | 5 | Whole-line comparison after `.strip()`; partial-add status when some lines pre-exist |
| 7 | `_print_manual_checklist` | 1 | 12 items with `§N` refs back to `docs/doctrine-updates.md` |
| 8 | `adopt()` orchestrator | 4 | `input()` mocked via `monkeypatch.setattr("builtins.input", ...)`; `--yes` skips prompt; declined prompt writes nothing |
| 9 | `main()` CLI | 4 | argparse + `sys.exit(2)` on bad upstream / undetectable package |

Total: 35 tests, 224 in the full repo (was 189). Mirrored `test_propagate_doctrine.py` conventions (class-based organization, `tmp_path` + `monkeypatch`, `capsys` for stdout).

### Sandbox verification

End-to-end run against `/tmp/adopt_sandbox/` with `src/sandboxpkg/`. Sequence:

1. **Dry-run** — printed the full 13-step plan and the 12-item manual-attention checklist with `§N` refs. No writes.
2. **Live run** — copied 10 artifacts, substituted hook glob (`3` sandboxpkg occurrences, `0` myproject), created `.claude/settings.json` with `Write|Edit` matcher pointing at `$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-shift-left-audit.sh`, appended `.claude/audits/` and `docs/design/hold/` to `.gitignore`.
3. **Idempotent re-run** — every artifact returned `[skip] ... already exists / hook already wired / all target lines already present`. No double-writes.

### Doctrine entry update

- Master adoption-mode table grew from 22 to 23 rows; helper marked TEMPLATE-COPY.
- New §23 subsection covers explicit non-goals (never deletes, never edits CUSTOMIZE artifacts, never overwrites existing targets, dry-run is the default mental model), CLI flags, idempotent semantics, and the helper-vs-by-hand risk trade-off with mitigations enumerated.
- "Suggested Adoption Order" got a fast-path note pointing at the helper as the first option, with the by-hand 10-step list preserved underneath.
- "Files added (utils)" updated to include the helper and its test partner.
- Propagation script extraction re-verified post-edit: 498 lines, terminates correctly at the 2026-04-21 entry boundary, no internal `## ` collisions (the five `2026-04-21` mentions are all inline references to the Python 3.11 catch-up, not entry bleed).

### Propagation (sixth doctrine cycle)

Ran `python scripts/propagate_doctrine.py` after the user confirmed "we are set" on the dry-run review. 12 downstream repos received the 2026-05-19 entry:

| Mode | Count | Repos |
|---|---|---|
| Notified (new) | 5 | contract-knowledge-graph, velocity-scoring, fema_cria, launch-control, tc_hurr_risk_modeling |
| Appended (existing notification) | 7 | paperboy, flood_model, maut_platform, aar_ai_pipeline, agent-eval, ldrd2025_ai_pipeline, rmi-reboot |

Spot-checked rmi-reboot (now carries 4 unread cycles: Mar-24, Mar-26, Apr-21, May-19) and contract-knowledge-graph (506-line notification, §23 present).

## Key Decisions

| Decision | Rationale |
|---|---|
| Ship A6 (helper) over A4 (pilot to 2–3 repos first) | User chose A6 after walkthrough confirmed the "horse to water" model — script lowers adoption friction without changing the consent model. MAUT had A6 at 0.760 vs A4 at 0.743 with the explicit tiebreaker *"ship A6 if helper can be authored test-first tonight"* — discipline followed, condition met. |
| Same-cycle ship (helper in 2026-05-19 entry) over follow-on cycle | User chose same-cycle, accepting the Pass 5 proposer's anti-recommendation against shipping 22+1 atomically. Mitigation: 35-test partner + skip-don't-overwrite semantics + dry-run-as-default + helper refuses CUSTOMIZE artifacts. |
| Scope ceiling: TEMPLATE-COPY + 2 safe CUSTOMIZE exceptions | Proposer §B1 explicit constraint. The helper does the mechanical 13 things; the human still does the 10 judgment-heavy things. No file deletions, no edits to `LANGUAGE.md` / `CONTEXT.md` / `CLAUDE.md` / `pyproject.toml` / `settings.local.json`. |
| Never overwrite existing targets | Pass 5 footgun: "diff-before-replace on directory-form skills (downstream may have customized)." Helper skips with status; downstream maintainer reviews by hand. |
| Auto-detect package from `src/<pkg>/`; require `--package` if ambiguous | Most downstream repos have one `src/<pkg>/`. Auto-detect makes the common case zero-friction; the explicit flag handles the edge cases without making them silently wrong. |
| Settings.json merge idempotency keyed on command suffix | Re-run safety. `_matcher_already_present` checks if any existing matcher's hooks array already wires a command ending in `post-tool-shift-left-audit.sh`. Avoids false positives with other matchers (e.g., a downstream Bash linter hook on Write\|Edit). |
| Two bisectable commits, not one | Same pattern as prior session (cf946b5/54c0022/6bcbb6f). `[infra]` for the helper + tests is one coherent unit; `[doc]` for the doctrine entry + tasks + project.yaml is another. Reverting either is clean. |

## Pillar Compliance

| Pillar | Status | Notes |
|---|---|---|
| **Simplicity First** | PASS | Helper scope deliberately narrowed by the Pass 5 ceiling. ~235 LOC + 35 tests; no CLI framework dependency (argparse only); no config file; auto-detect with explicit override is the only smart thing it does. Refused all six "could the helper also do X" thoughts during build. |
| **Shift-Left Testing** | PASS | First deliverable authored end-to-end under the new test-first vertical-slice mandate. Every slice followed the cadence — failing test, observe red, minimum impl, observe green, commit-mentally, next slice. The audit hook does not watch `scripts/`, so there is no audit-log proof; the discipline is verifiable from the commit history and the 35-test partner's structure (one test class per function). |
| **Config-Driven** | PASS | Helper has no config file (it would be overkill for a 235-LOC script with 4 flags). Constants `HOOK_RELATIVE`, `SETTINGS_RELATIVE`, `HOOK_COMMAND`, `HOOK_MATCHER`, `HOOK_TIMEOUT_SECONDS`, `GITIGNORE_LINES`, `VERBATIM_COPIES`, `MANUAL_CHECKLIST_ITEMS` are all module-level — explicit, greppable, modifiable without code logic changes. |

## Commits

| Hash | Subject | Files | Lines |
|---|---|---|---|
| `a6e5bd3` | [infra] Add scripts/adopt_doctrine.py — A6 adoption helper (test-first, 35 tests) | 2 | +940 |
| `ac71569` | [doc] Add artifact #23 to 2026-05-19 doctrine entry + §23 helper docs | 3 | +35 / −4 |

Plus this session doc as the third commit.

## Next Steps

- [ ] **Downstream pickup signals**. Watch for `.claude/upstream-update.md` deletions or session docs in downstream repos that reference adopting the bundle. The 7 repos with `(append)` mode now carry up to 4 unread cycles — visible debt by design.
- [ ] **(P3, carried)** GitHub Actions CI workflow. The audit hook only fires inside Claude Code sessions; CI catches non-harness commits.
- [ ] **(P3, carried)** `from_yaml` round-trip tests for 4 value functions (exponential, logarithmic, step, piecewise_linear).
- [ ] **(P3, carried)** After 1–2 sessions of audit-log data, decide whether to add a Stop hook (Layer 5) or escalate to a PreToolUse hard block (Layer 6) per `.claude/skills/shift-left-testing/ENFORCEMENT.md` escalation criteria.
- [ ] **Push.** 6 local commits ahead of origin/main (4 prior + 2 from this session + this session doc when committed). User's call on timing.

## Notes

- The helper's `_print_manual_checklist` has 12 items, not 11 as planned — the three legacy single-file skill deletions (`shift-left-testing.md`, `configuration-management.md`, `python-venv-management.md`) became three individual entries instead of one collapsed line because the per-skill conditional check is the action the downstream maintainer needs to do, not "delete legacy skills" generically. Minor scope expansion within the same intent.
- The Pass 5 proposer's anti-recommendation against same-cycle 22+1 shipping was overridden by the user. The mitigations (35 tests + skip-don't-overwrite + dry-run default + CUSTOMIZE refusal) are what made the override defensible, not the override itself. If downstream consumption surfaces a bug in the helper that affects multiple repos, that confirms the proposer's concern was warranted; if downstream consumption goes cleanly, that confirms the test partner was sufficient. Either signal updates the cost-of-helper estimate for future cycles.
- "Claude dice" framing continues to bear weight: the script is the deterministic counterpart to the probabilistic skill-invocation that gets us 70%–90% adherence to shift-left discipline. Same pattern as the audit hook — give the agent the *option* to do the right thing easily, then audit whether it actually did.
- Two same-day session docs (predecessor + this one) is unusual but appropriate. Splitting at the A4/A6 decision keeps each session doc coherently scoped — the predecessor documents the bundle and the deferred decision; this one documents the decision, the build, and the propagation.
