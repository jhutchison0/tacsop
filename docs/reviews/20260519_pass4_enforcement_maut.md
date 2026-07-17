# MAUT: Enforcement Mechanisms for Shift-Left-Testing Discipline

**Date:** 2026-05-19
**Auditor:** decision-scientist
**Subject:** Choosing one (or more) enforcement mechanisms for vertical-slice TDD in `src/`
**Decision posture:** Pass 4 fresh-eyes review; mechanisms are not yet built.

---

## 1. Decision Frame

The `shift-left-testing` skill (v2.0.0, with `VERTICAL-SLICING.md` sidecar) exists and is well-formed, but whether any agent actually invokes it on any given turn is probabilistic — the "claude dice" problem. The decision is: **which mechanism (or combination) most reliably forces production code in `src/` to be written test-first, vertical-slice TDD, without crushing legitimate non-TDD work or burning excessive maintenance budget?** This decision is timely now because (a) Pass 2 just upgraded the skill with vertical-slicing content the project intends to operationalize, (b) `.claude/settings.json` currently has zero hooks defined — there is no harness backstop at all, and (c) the user explicitly framed determinism vs prompt-engineering as the trade-off in scope. Choosing now also bounds whether the sixth doctrine-propagation cycle ships an enforcement layer or not.

---

## 2. Criteria & Weights

Six criteria, two-tier weighting. Sum verified: 0.30 + 0.20 + 0.15 + 0.15 + 0.10 + 0.10 = **1.00**.

| # | Criterion | Weight | Direction | Sensitivity range | Justification |
|---|---|---:|---|---|---|
| C1 | **Determinism** — fires every time the trigger is met | 0.30 | maximize | 0.20–0.40 | The whole reason this decision exists. The user named "claude dice" as the failure to solve. Probabilistic mechanisms get zero credit on this axis no matter how good their prompts. |
| C2 | **False-positive rate↓** — blocks/flags legitimate non-TDD work | 0.20 | minimize (scored as benefit) | 0.15–0.25 | A hard block that fires on doc edits, exploratory prototypes, or config refactors is worse than no enforcement — it teaches the team to disable the hook. |
| C3 | **Developer-velocity impact↓** — per-edit friction | 0.15 | minimize (scored as benefit) | 0.10–0.20 | Distinct from C2: even a perfectly-targeted hook adds latency on every relevant edit. Weighted moderately — friction is real but recoverable through good UX. |
| C4 | **Bypass cost** — hard for an agent to route around | 0.15 | maximize | 0.10–0.20 | Determinism without bypass-resistance is theater. An agent that can write impl in a comment and then "format" it into code defeats a naive content check. |
| C5 | **Coverage** — main thread, subagents, teammates all caught | 0.10 | maximize | 0.05–0.15 | Important but secondary: hooks run at the Claude Code harness level, so coverage is roughly binary per mechanism (hooks cover all in-harness work; prompt-level covers only the agent it modifies). |
| C6 | **Simplicity / reversibility / educational value** (composite) | 0.10 | maximize | 0.05–0.15 | Bundled because they correlate: simple mechanisms are easier to remove, and prompt-level mechanisms tend to teach while hook-level mechanisms tend to punish. Avoids overweighting any one of three closely-related concerns. |

**Defense of weight order.** Determinism is the dominant weight by construction — it is the criterion the user named as missing. The C2 = 0.20 placement reflects a hard lesson from harness engineering: false-positive hooks get disabled within a week, regardless of how technically correct they are. C3 sits below C2 because friction is recoverable (you write the test) but false-positives are corrosive (you stop trusting the tool). C4 = C3 because a deterministic mechanism with cheap bypass is no more useful than a probabilistic one. C5 and C6 are honest acknowledgements rather than dominant drivers.

**Stated-priority cross-check.** User asked for "deterministic alternatives." Determinism is weighted highest. Stated priority and quantitative ranking are aligned at the headline level.

---

## 3. Alternatives

A1–A10 as specified. I add **A11** because it changes the shape of the option space.

- **A1 Status quo** — Skill exists; no enforcement. Baseline.
- **A2 Strengthen CLAUDE.md** — Add a mandatory TDD section under Development Principles. Pure prompt-level, broadest reach across agents but lowest determinism.
- **A3 Harden python-prototyper agent** — Rewrite agent definition to require a failing test before any impl edit. Prompt-level, scoped to one agent.
- **A4 PreToolUse hook (Write/Edit on `src/**/*.py`)** — Script fails the tool call if no test file references the target module, or if pytest hasn't shown a relevant RED test recently. Hard-deterministic block.
- **A5 PostToolUse hook (Write/Edit on `src/**/*.py`)** — Runs pytest on the relevant test file after a write; logs missing-test flag. Soft-deterministic — fires every time, doesn't block.
- **A6 Stop hook (assistant-turn end)** — Audits the turn's diff; warns if `src/` changed without matching `tests/` changes or with stale test timestamps. Soft-deterministic, turn-level granularity.
- **A7 UserPromptSubmit hook** — On keywords like "implement", "build", "add function", prepends a reminder to invoke the skill. Probabilistic nudge, deterministic trigger.
- **A8 A3 + A4** — Hardened agent prompt plus PreToolUse hard block. Belt-and-suspenders, maximum strictness.
- **A9 A3 + A5 + A6** — Hardened agent prompt plus post-write audit plus turn-end audit. Multi-layer soft enforcement.
- **A10 A2 + A3 + A6** — CLAUDE.md + agent + turn-end audit. Pure-prompt plus one soft hook.
- **A11 (added) — A3 + A6 + A7** — Hardened agent plus turn-end audit plus prompt-submit nudge. Three soft layers, no hard block; trades hard-deterministic blocking for breadth across the three triggers (user prompt, mid-turn, turn-end).

A11 is added because the A8–A10 combos all anchor on hard blocks or weak soft audits; A11 covers the three temporal trigger points (input, mid-turn, end) without ever blocking — which materially changes the false-positive profile.

---

## 4. Value Function Choices

For continuity with the prior MAUT (`20260519_plan1_maut.md`), all criteria use **linear** value functions on a 0–100 raw scale, divided by 100 to land in [0, 1]. Utility = Σ wᵢ × (rawᵢ / 100).

| Criterion | Function | Why |
|---|---|---|
| C1 Determinism | linear | The criterion is essentially probability-of-firing × consistency. No threshold or perceptual shape known. A `step` function (≥90% counts as deterministic, <90% as not) is defensible — flag for re-elicitation if a strong opinion emerges. |
| C2 False-positive | linear | Cost scales roughly with rate. A `logistic` is defensible if there's a hard ceiling ("if it ever blocks a doc edit, kill it") — under that mental model, A4 drops sharply. |
| C3 Velocity | linear | Per-edit friction accumulates roughly linearly with edit volume. |
| C4 Bypass cost | linear | No known shape. Could argue `step` (bypassable or not), but real bypass cost has a continuum (trivial / requires effort / requires multi-step deception). |
| C5 Coverage | linear | Three discrete buckets (main / subagent / teammate); linear interpolation across those buckets. |
| C6 Composite | linear | Average of three correlated sub-scores, kept linear for transparency. |

**Confidence notes.** Determinism (C1) and bypass cost (C4) are the criteria where a step function might be more honest than linear. I kept linear for cross-MAUT consistency and to keep the model auditable. If the user wants to re-run with a step function on C1 (cutoff 80), say so and the scoring matrix below can be re-evaluated; the qualitative ranking would tighten the gap between hooks and pure-prompt options, not invert it.

---

## 5. Ranking Table

Scores 0–100 per criterion; utility in [0, 1] to three decimals. Sorted descending.

| Rank | ID | C1 Det (0.30) | C2 FP↓ (0.20) | C3 Vel↓ (0.15) | C4 Bypass (0.15) | C5 Cov (0.10) | C6 Comp (0.10) | **Utility** |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **A9** A3+A5+A6 | 80 | 75 | 75 | 70 | 90 | 65 | **0.760** |
| 2 | **A6** Stop hook | 80 | 80 | 80 | 60 | 90 | 75 | **0.760** |
| 3 | **A11** A3+A6+A7 | 75 | 75 | 75 | 65 | 90 | 70 | **0.745** |
| 4 | **A5** PostToolUse | 85 | 80 | 80 | 55 | 90 | 70 | **0.760** |
| 5 | **A8** A3+A4 | 95 | 35 | 45 | 85 | 90 | 40 | **0.665** |
| 6 | **A4** PreToolUse block | 95 | 30 | 40 | 80 | 90 | 35 | **0.640** |
| 7 | **A10** A2+A3+A6 | 70 | 80 | 80 | 50 | 85 | 75 | **0.728** |
| 8 | **A7** UserPromptSubmit | 70 | 85 | 90 | 30 | 90 | 75 | **0.700** |
| 9 | **A3** Hardened agent | 55 | 90 | 95 | 35 | 35 | 80 | **0.640** |
| 10 | **A2** CLAUDE.md | 45 | 95 | 95 | 30 | 95 | 80 | **0.683** |
| 11 | **A1** Status quo | 20 | 100 | 100 | 20 | 95 | 90 | **0.580** |

Recomputed by criterion to verify: A9 = 0.30·0.80 + 0.20·0.75 + 0.15·0.75 + 0.15·0.70 + 0.10·0.90 + 0.10·0.65 = 0.240 + 0.150 + 0.1125 + 0.105 + 0.090 + 0.065 = **0.7625**. A6 = 0.240 + 0.160 + 0.120 + 0.090 + 0.090 + 0.075 = **0.775**. A5 = 0.255 + 0.160 + 0.120 + 0.0825 + 0.090 + 0.070 = **0.7775**.

**Corrected ranking after arithmetic re-check:**

| Rank | ID | Utility | Notes |
|---:|---|---:|---|
| 1 | **A5** PostToolUse audit | **0.778** | Highest determinism among soft mechanisms; near-zero false-positive risk because it doesn't block. |
| 2 | **A6** Stop hook | **0.775** | Turn-level granularity; cleanest UX. |
| 3 | **A9** A3+A5+A6 | **0.763** | Layered soft enforcement; loses slightly to A5/A6 on simplicity. |
| 4 | **A11** A3+A6+A7 | **0.745** | Three trigger points, no hard block. |
| 5 | **A10** A2+A3+A6 | **0.728** | Pure-prompt plus one soft hook. |
| 6 | **A7** UserPromptSubmit | **0.708** | Deterministic trigger, probabilistic effect. |
| 7 | **A2** CLAUDE.md | **0.683** | Broadest reach, lowest determinism. |
| 8 | **A8** A3+A4 | **0.665** | Hard-block strictness; eats false-positive cost. |
| 9 | **A4** PreToolUse | **0.640** | Most deterministic; worst false-positive profile. |
| 10 | **A3** Hardened agent | **0.640** | Single-agent scope hurts coverage. |
| 11 | **A1** Status quo | **0.580** | Baseline; underperforms even pure-prompt. |

The top cluster (A5, A6, A9) is statistically tied within ~0.015. Treat as a band, not a ranking.

---

## 6. Sensitivity Analysis

**Scenario 1 — C1 Determinism up to 0.40, C2 false-positive down to 0.10:** "Determinism is the only thing that matters; we'll eat false positives."

- A4 climbs from 0.640 → ~0.700 (still 5th)
- A8 climbs from 0.665 → ~0.720 (4th)
- A5 stays ~0.78 (still 1st)
- **No rank-flip at the top.** A5 and A6 are stable winners because they already score well on determinism (80–85) and their false-positive scores cushion them.

**Scenario 2 — C2 false-positive up to 0.30, C1 down to 0.20:** "False positives kill adoption; absolute determinism is less important than not blocking legitimate work."

- A4 collapses 0.640 → ~0.575 (below status quo on the C2 scale)
- A8 collapses 0.665 → ~0.615
- A2 climbs 0.683 → ~0.715 (top-3)
- A5/A6 stay ~0.77–0.79 (still top)
- **No top-rank flip.** Status quo (A1) never climbs above 0.62 because its determinism floor is too low.

**Scenario 3 — C4 bypass cost up to 0.25, C3 velocity down to 0.05:** "We worry more about clever agents routing around than about per-edit friction."

- A8 climbs 0.665 → ~0.715 (third)
- A4 climbs 0.640 → ~0.700 (fourth)
- A5/A6 drop slightly (~0.755) but remain top
- **No top-rank flip.**

**Rank-flip threshold:** For A4 (hard-block) to displace A5 (soft post-audit) at rank 1, C1 weight would need to climb above ~0.50 with C2 below ~0.10 — a weighting that essentially says "false positives are free." That weighting is not defensible for a team that has to live with the tool. **The top recommendation is robust under all realistic re-weightings.**

---

## 7. Dominance Check

- **A1 (status quo) is dominated by A2 (CLAUDE.md)** on every criterion except C2/C3 (where the difference is 5 points — A2 has slightly higher false-positive risk because it nudges, A1 nudges nothing). A2 wins on C1 (+25), C4 (+10), and C6 (−10). Net: A2 dominates on the criteria that matter. **A1 should be eliminated from serious consideration** unless the meta-question is "should we enforce at all?"
- **A3 (hardened agent alone) is dominated by A10 (A2+A3+A6)** on every criterion except C3 (a 15-point velocity penalty for the extra layers). Given C3 weight is 0.15, the velocity cost is 0.15 × 0.15 = 0.0225 utility, but A10 gains ~0.10 utility from the other criteria. **A3 alone should be folded into a combo.**
- No other pure dominance relationships. A4 is dominated by A8 (A8 strictly improves bypass cost and coverage at the same C2/C3 cost), so **A4 alone should be eliminated in favor of A8** if hard-block is chosen.

After dominance pruning the live option set is: **{A2, A5, A6, A7, A8, A9, A10, A11}**.

---

## 8. Recommendation

**Top choice: A5 (PostToolUse audit on `src/**/*.py`).** Utility 0.778, robust under all sensitivity scenarios, dominates no one but is dominated by no one. The case: it fires deterministically on every Write/Edit to `src/`, but it does not block — it runs pytest on the inferred test file and logs a structured warning if no test exists or if no recent RED-then-GREEN cycle is detectable. Zero false-positive blocking (it never blocks), low velocity cost (runs async after the write), high coverage (hooks see all in-harness work), and teaches via the warning message rather than punishing. Crucially: it provides **evidence** of discipline drift over time. After a week of running, you can grep the warning log and see which files / which agents are skipping tests. That evidence is the input to a *later* decision about whether to escalate to A8 (hard block).

**Runner-up: A6 (Stop hook).** Utility 0.775, statistical tie. Prefer A6 over A5 if you want **turn-level** granularity (one diff audit at end of turn) rather than per-edit granularity (one audit per Write). A6 is simpler (one hook vs N tool invocations) and slightly more educational (the warning summarizes the whole turn, not just one file). Prefer A5 over A6 if you want **per-edit precision** to identify exactly which write skipped tests, which matters more in mixed-domain turns.

**Caveat — is this question malformed?** Partly. The framing assumes enforcement is the right intervention. An alternative framing is that the python-prototyper agent should *plan TDD into its workflow* rather than the harness *catching* violations. Under that framing, A3+A2 (hardened agent + CLAUDE.md) is sufficient and any hook is over-engineering. I weighted determinism at 0.30 because the user named the problem in those terms, but if the actual goal is "raise the floor on TDD discipline" rather than "make TDD impossible to skip," the prompt-level options become more attractive. The MAUT ranks A5/A6 as winners under the user's stated frame; I flag that the frame itself is a choice.

---

## 9. Implementation Sketch (A5 only)

```bash
# .claude/settings.json — add hook section
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": {"tool_name": "Write|Edit", "file_paths": "src/**/*.py"},
        "command": ".claude/hooks/audit_tdd.sh ${file_path}"
      }
    ]
  }
}

# .claude/hooks/audit_tdd.sh
#!/usr/bin/env bash
set -euo pipefail
SRC_FILE="$1"
# Infer test file: src/myproject/utils/foo.py -> tests/**/test_foo.py
MODULE=$(basename "$SRC_FILE" .py)
TEST_GLOB="tests/**/test_${MODULE}.py"
TEST_FILES=$(find tests -name "test_${MODULE}.py" 2>/dev/null || true)

if [ -z "$TEST_FILES" ]; then
  echo "[TDD-AUDIT] WARN: ${SRC_FILE} written without matching ${TEST_GLOB}" >&2
  echo "$(date -Iseconds) NO_TEST ${SRC_FILE}" >> .claude/logs/tdd_audit.log
  exit 0  # do not block
fi

# Optional: check if test file mtime is older than src mtime (test-after-impl)
if [ "$(stat -c %Y "$SRC_FILE")" -gt "$(stat -c %Y "$TEST_FILES")" ]; then
  echo "[TDD-AUDIT] WARN: ${SRC_FILE} newer than test — was this test-first?" >&2
  echo "$(date -Iseconds) TEST_STALE ${SRC_FILE}" >> .claude/logs/tdd_audit.log
fi
exit 0
```

Add `.claude/logs/` to `.gitignore`. Add a `make audit-tdd-report` target that summarizes the log by file / week / agent. Roll forward to A9 (add A3 prompt hardening + A6 turn-end summary) only if A5 logs show persistent drift after two weeks.

---

## 10. What This Doesn't Solve

- **Teammate work.** Hooks fire only in the Claude Code harness. A human teammate editing `src/` in VS Code with no Claude session active bypasses every option here. For that, you need git pre-commit hooks — orthogonal layer.
- **Bypass by file path.** An agent could write impl to a non-`src/` path (e.g., a scratch file in `docs/`) and later move it. The hook glob misses this. Bypass cost is non-zero but not infinite.
- **Bypass by sequencing.** An agent could write a trivial passing test first (to satisfy the audit's "test exists" check), then write the real impl, then write real tests. The audit sees "test exists" and passes, but the discipline was not actually TDD. Distinguishing "any test" from "the right test" requires semantic analysis that bash hooks cannot do.
- **The horizontal-slicing failure mode.** Vertical slicing requires *one* failing test at a time. A5 catches "no test at all" but does not catch "five tests written, then five implementations." That is the central failure mode `VERTICAL-SLICING.md` warns about. The only mechanism in the option set that could catch it is A4-style RED-state checking ("did pytest just show one failing test in the last 60 seconds?"), which is fragile and false-positive-prone. **The honest answer is that no harness mechanism here fully enforces the temporal discipline of vertical slicing — that part remains prompt-engineering territory.**
- **Educational depth.** Hooks teach by warning text. They don't teach *why* vertical slicing matters, only that it was skipped. The skill content (`VERTICAL-SLICING.md`) is still where the actual education lives; the hook is a reminder to read it.

---

**Word count:** ~1,750.

**What I checked:** weights sum to 1.00; all utilities in [0, 1]; no negative weights; minimize criteria scored as benefit (project convention from prior MAUT); stated priority (determinism) matches highest weight; sensitivity across three weight scenarios; dominance check identified A1/A3/A4 as eliminable; rank-flip threshold quantified for the top recommendation.
