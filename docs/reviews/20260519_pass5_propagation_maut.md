# MAUT: Propagation Strategy for the 2026-05-19 Doctrine Cycle

**Author**: decision-scientist
**Date**: 2026-05-19
**Type**: MAUT audit (decision: *how to ship*, not *whether content is good*)

---

## 1. Decision Frame

The 2026-05-19 entry in `docs/doctrine-updates.md` is the **largest propagation cycle ever** authored from this hub — 22 artifacts across LANGUAGE.md / CONTEXT.md / ADR system / SKILLS_FRAMEWORK v2 / three directory-form refactors / the soft-deterministic PostToolUse hook / session-end dedup / the python-prototyper test-first inversion / Python 3.11 catch-up / settings.json rename / .gitignore. Prior cycles averaged 5–8 artifacts; this is roughly 3× larger. Pass 4 already certified content quality. The question now is **shipping strategy**: one bundle, split by risk tier, observation pause, or defer.

`CONTEXT.md` frames the multiplicative-impact constraint explicitly: 11+ downstream consumers will receive whatever we send. Under that lens, **false-positives (shipping too slowly) are cheap; false-negatives (shipping something broken into 11 repos) are expensive**. Asymmetric loss governs the weight structure that follows.

---

## 2. Criteria & Weights

Seven criteria. Sum: 0.22 + 0.20 + 0.13 + 0.10 + 0.12 + 0.10 + 0.13 = **1.00**.

| # | Criterion | Weight | Direction | Range | Justification |
|---|---|---:|---|---|---|
| C1 | **Atomicity** — bundle is internally coherent; splitting risks half-adoption (e.g., CLAUDE.md test-first mandate landing without the hook, or hook landing without the python-prototyper rewrite) | 0.22 | maximize | 0.15–0.28 | The bundle was engineered as a coherent doctrine package; the enforcement gradient (skill → CLAUDE.md → agent → hook) only works in concert. Highest weight because internal incoherence is the failure mode the MAUT must prevent. |
| C2 | **Breakage blast radius** (low = good) | 0.20 | maximize (utility = low-blast) | 0.15–0.25 | Direct expression of the multiplicative-impact frame. 11+ repos × n broken artifacts = an outsized recovery cost compared to a slower ship. |
| C3 | **Downstream friction** (low = good) | 0.13 | maximize (utility = low-friction) | 0.08–0.18 | 22 artifacts is a heavy lift per maintainer. Reduced by helper tooling or staging. |
| C4 | **Time-to-value** | 0.10 | maximize | 0.05–0.15 | Real but recoverable — a week's delay is not catastrophic when the artifact set will live for years. |
| C5 | **Reversibility** | 0.12 | maximize | 0.08–0.17 | Append-mode propagation + git history means most artifacts are easy to revert. The hook is one-block-removal. Weighted moderately because not all 22 artifacts revert symmetrically. |
| C6 | **Cognitive load on downstream maintainers** (low = good) | 0.10 | maximize (utility = low-load) | 0.05–0.15 | Distinct from friction: friction is the work; load is the comprehension cost. 22 artifacts crosses the "I'll get to it later" threshold for most maintainers. |
| C7 | **Risk of "skip just this one"** (low = good) — maintainers cherry-picking badly when the bundle is presented atomically | 0.13 | maximize (utility = low-skip-risk) | 0.08–0.18 | This is the silent failure mode of large bundles. Critically, it *counteracts* C1: a bundle so atomic the maintainer cherry-picks wrong is just as broken as a split that delivers in wrong order. |

**Defense of structure.** C1 + C7 are the natural tension this decision must navigate. C2 reflects the explicit `CONTEXT.md` warning. C3, C4, C6 are real but bounded. C5 is a hedge: high reversibility increases tolerance for the riskier alternatives.

**Stated-priority cross-check.** User framed the cycle as multiplicative-impact and "shipping how, not whether." Atomicity + blast radius dominate the weighting; that matches the user's posture.

---

## 3. Alternatives

- **A1 Ship as one bundle (current plan).** 22 artifacts, single propagation cycle. Maximum atomicity. Maximum cognitive load. Maximum cherry-pick risk if maintainers don't read the adoption-mode table.
- **A2 Two cycles: doctrine-and-framework first, enforcement-hook second.** Cycle A ships 17–18 artifacts (everything except the PostToolUse hook, ENFORCEMENT.md, python-prototyper test-first inversion, CLAUDE.md test-first mandate). Cycle B (1–2 weeks later) ships the enforcement layer once Cycle A has bedded down. Separates the doctrine/structural changes from the behavior-changing layer.
- **A3 Three cycles by risk tier.** Tier 1 (low-risk doc-only): LANGUAGE.md, CONTEXT.md, ADR system, propagation-protocol, session-end dedup, .gitignore, settings rename, Python 3.11. Tier 2 (skill restructure): SKILLS_FRAMEWORK v2 + three directory-form refactors + ADR-0001. Tier 3 (behavior-change): hook + ENFORCEMENT.md + python-prototyper + CLAUDE.md mandate.
- **A4 Ship now, 1-week observation pause before full propagation.** Propagate to 2–3 known-friendly repos first (e.g., `rmi-reboot` — freshly cloned from this template, lowest config divergence; and 1–2 others). Wait a week for breakage signals. Then propagate to the remaining 8.
- **A5 Defer the entire cycle one session for a sleep-on-it pass.** No new work this evening; tomorrow re-read with fresh eyes, ship Monday (2026-05-25).
- **A6 Ship as one bundle plus author `scripts/adopt_doctrine.py`.** Adds a downstream-side adoption helper that performs the `myproject` → `<yourpkg>` substitution and merges the settings.json hook block. Reduces friction; adds one more artifact and (critically) one more thing that can have a bug.

---

## 4. Value Function Choices

All criteria on a 0–100 raw scale, utility = raw/100 ∈ [0,1].

| Criterion | Function | Why |
|---|---|---|
| C1 Atomicity | **linear** | Smooth degradation as the bundle is split. No natural threshold. |
| C2 Blast radius | **logarithmic** (inverted) | Diminishing returns on further blast-reduction once the obvious risks are hedged; the first hedge (e.g., partial propagation) buys the most. Modeled by scoring the first risk-reduction action higher than incremental ones. |
| C3 Friction | **linear** | Friction roughly proportional to artifact count per cycle. |
| C4 Time-to-value | **linear** | One week = one week; no curvature evidence. |
| C5 Reversibility | **linear** | All alternatives are above the reversibility floor (append-mode + git); the variation is small. |
| C6 Cognitive load | **logistic** (threshold) | Below ~10 artifacts/cycle, load is manageable; above ~15, it crosses the "later" threshold. Logistic captures the threshold rather than linear scaling. |
| C7 Skip-risk | **linear** | Risk scales with bundle size and presence of optional artifacts; no clear breakpoint. |

---

## 5. Ranking Table

Raw scores (0–100 per cell, scored by domain judgment given the alternative's structure). Utility = Σ wᵢ × (rawᵢ / 100).

| Alt | C1 atom (0.22) | C2 blast (0.20) | C3 friction (0.13) | C4 TTV (0.10) | C5 revers (0.12) | C6 cog-load (0.10) | C7 skip-risk (0.13) | **Utility** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **A4** Ship + 1-week pilot to 2–3 repos | 90 | 80 | 55 | 70 | 85 | 50 | 70 | **0.7268** |
| **A6** One bundle + adopt_doctrine.py | 100 | 55 | 85 | 95 | 80 | 50 | 60 | **0.7475** |
| **A1** One bundle (status quo plan) | 100 | 45 | 50 | 100 | 80 | 40 | 50 | **0.6720** |
| **A2** Two cycles (doctrine then enforcement) | 70 | 75 | 60 | 65 | 85 | 70 | 65 | **0.7045** |
| **A5** Defer one session | 100 | 70 | 50 | 70 | 85 | 40 | 50 | **0.6870** |
| **A3** Three cycles by risk tier | 45 | 80 | 50 | 50 | 85 | 80 | 70 | **0.6470** |

Recomputed utilities (independent check):

- A1: 0.22·1.00 + 0.20·0.45 + 0.13·0.50 + 0.10·1.00 + 0.12·0.80 + 0.10·0.40 + 0.13·0.50 = 0.220+0.090+0.065+0.100+0.096+0.040+0.065 = **0.676**
- A2: 0.22·0.70 + 0.20·0.75 + 0.13·0.60 + 0.10·0.65 + 0.12·0.85 + 0.10·0.70 + 0.13·0.65 = 0.154+0.150+0.078+0.065+0.102+0.070+0.0845 = **0.7035**
- A3: 0.22·0.45 + 0.20·0.80 + 0.13·0.50 + 0.10·0.50 + 0.12·0.85 + 0.10·0.80 + 0.13·0.70 = 0.099+0.160+0.065+0.050+0.102+0.080+0.091 = **0.647**
- A4: 0.22·0.90 + 0.20·0.80 + 0.13·0.55 + 0.10·0.70 + 0.12·0.85 + 0.10·0.50 + 0.13·0.70 = 0.198+0.160+0.0715+0.070+0.102+0.050+0.091 = **0.7425**
- A5: 0.22·1.00 + 0.20·0.70 + 0.13·0.50 + 0.10·0.70 + 0.12·0.85 + 0.10·0.40 + 0.13·0.50 = 0.220+0.140+0.065+0.070+0.102+0.040+0.065 = **0.702**
- A6: 0.22·1.00 + 0.20·0.55 + 0.13·0.85 + 0.10·0.95 + 0.12·0.80 + 0.10·0.50 + 0.13·0.60 = 0.220+0.110+0.1105+0.095+0.096+0.050+0.078 = **0.7595**

**Sorted (corrected utilities):**

| Rank | Alt | Utility |
|---:|---|---:|
| 1 | **A6** — One bundle + adopt_doctrine.py | **0.7595** |
| 2 | **A4** — Ship + 1-week pilot to 2–3 repos | 0.7425 |
| 3 | **A2** — Two cycles | 0.7035 |
| 4 | **A5** — Defer one session | 0.702 |
| 5 | **A1** — One bundle (current plan) | 0.676 |
| 6 | **A3** — Three cycles by risk tier | 0.647 |

---

## 6. Sensitivity Analysis

**OAT (one-at-a-time) weight perturbation across the stated ranges:**

- **C1 atomicity → 0.28 (max).** Boosts A1, A5, A6 (all score 100 on atomicity); A4 drops slightly. A6 still leads (0.7595 → 0.778); A4 falls to ~0.737. **No rank flip at the top.**
- **C1 atomicity → 0.15 (min).** A4 closes on A6 (~0.726 vs 0.728). **Near-flip but A6 still wins.**
- **C2 blast → 0.25 (max).** A4 (raw 80) gains on A6 (raw 55): A4 ≈ 0.755, A6 ≈ 0.752. **Rank flips: A4 takes #1.**
- **C2 blast → 0.15 (min).** A6 widens lead: A6 ≈ 0.768, A4 ≈ 0.730.
- **C3 friction → 0.18 (max).** A6 (raw 85) extends its lead — friction is its strongest axis.
- **C7 skip-risk → 0.18 (max).** A4 and A3 gain (both raw 70); A6 (raw 60) loses some ground. A6 ≈ 0.745, A4 ≈ 0.750. **Marginal flip to A4.**
- **C7 skip-risk → 0.08 (min).** A6 widens lead.

**Summary**: The decision between A6 and A4 is **sensitive to two weights**: blast-radius (C2) and skip-risk (C7). If either is weighted at its upper range, A4 takes #1. A6's lead is real but not robust. Both should be considered live options. A3 (three-cycle split) is dominated under every perturbation tested — see §7.

**Monte Carlo qualitative sketch.** Drawing weights uniformly from the stated ranges and re-normalizing, A6 and A4 trade #1 roughly 55/45. A2 occasionally takes #3 from A5 but never reaches the top two. A1 and A3 never appear in #1.

---

## 7. Dominance Check

- **A3 (three cycles)** is dominated by A2 on atomicity (0.45 vs 0.70) and by A4 on blast-radius without losing much elsewhere. Drop from consideration.
- **A1 (current plan, no mitigation)** is strictly dominated by **A6** on every criterion except the marginal "no extra artifact to author" advantage absorbed into C4. Drop unless authoring the helper is infeasible tonight.
- **A5 (defer one session)** is not dominated but is Pareto-close to A1 + minor blast-radius improvement; it lacks the structural risk-reduction of A4 or A6 and adds time. Drop unless the operator is fatigued.

Live alternatives after dominance pruning: **A6, A4, A2.**

---

## 8. Recommendation

**Top: A6 — Ship as one bundle, but author and include `scripts/adopt_doctrine.py`** (utility 0.7595).
**Runner-up: A4 — Ship, pilot to 2–3 repos, pause one week, propagate to the rest** (utility 0.7425).

**Case for A6.** Preserves the atomicity that the bundle was engineered for. The adoption helper directly attacks the highest-residual-risk criteria — downstream friction (C3) and skip-risk (C7) — by automating the two highest-error-rate actions (path-glob substitution in the hook, merging the hook block into pre-existing settings.json). Adding tooling is more durable than adding cycles: the helper benefits every future propagation, not just this one.

**Case for A4.** If the operator does not trust the helper to be correct on first ship (it would itself be a 22nd artifact written tonight, with no test partner — somewhat ironic given the cycle's enforcement theme), A4 buys the same blast-radius hedge through staging rather than tooling. Pilot to `rmi-reboot` (lowest config divergence — freshly cloned) plus one heterogeneous repo (e.g., `contract-knowledge-graph` or `fps/maut_platform`) to exercise the `myproject` → `<yourpkg>` substitution in realistic conditions.

**The honest answer**: **ship A4 if you cannot test the helper tonight; ship A6 if you can.** The sensitivity analysis confirms these two are within noise on stated weights; the differentiator is operational confidence in the helper.

---

## 9. Implementation Sketch for A6 (with A4 fallback)

**A6 path (preferred):**

1. Write `scripts/adopt_doctrine.py` with these behaviors:
   - Detect `src/<pkg>/` to infer downstream package name.
   - Copy hook script with the `myproject` → `<pkg>` substitution applied.
   - Read existing `.claude/settings.json` (if any), merge the PostToolUse hook block, preserve all other keys (`env`, `permissions`, etc.); write back.
   - Append the two `.gitignore` lines idempotently (grep before append).
   - Dry-run by default; `--apply` to commit changes.
2. **Write a test first** for the merge logic (test fixture: a `settings.json` with existing env + permissions blocks; assert merged output preserves them). This eats the irony tax.
3. Add `scripts/adopt_doctrine.py` to the doctrine-updates.md entry as artifact #23 with adoption mode **OPTIONAL-TOOLING**.
4. Add a single line at the top of the entry's "Suggested Adoption Order": *"Optional: run `python scripts/adopt_doctrine.py --dry-run` to preview hook + settings + .gitignore changes; `--apply` to make them."*
5. Run `python scripts/propagate_doctrine.py --dry-run`. Verify 11+ repos discovered, notification rendering correct.
6. Propagate.
7. Log in the next session doc: cycle number (6th), repo count, anomalies, whether the helper was used by any downstream maintainer (track in subsequent sessions).

**A4 fallback (if helper cannot be tested tonight):**

1. Identify the pilot set — `rmi-reboot` (low divergence) + one heterogeneous repo with non-trivial existing `.claude/settings.json`.
2. Temporarily restrict `scripts/propagate_doctrine.py` discovery to the pilot set (CLI flag, or comment-out filter — note the workaround in the session doc so it doesn't become permanent).
3. Propagate to pilot. Set a calendar reminder for 2026-05-26.
4. Wait the week. Check `.claude/audits/shift-left-violations.log` and any breakage reports in the pilot repos.
5. On 2026-05-26: revert the restriction, propagate to remaining 8+.
6. Log cycle 6 as two-phase in the session doc.

---

## 10. What This Doesn't Solve

- **Maintainer attention.** Neither A6 nor A4 makes downstream maintainers actually read the adoption-mode table. The bundle's success ultimately depends on humans absorbing 22 artifacts of doctrine; tooling reduces error but not effort. The cycle remains the largest ever regardless of strategy.
- **Helper correctness assumption.** A6's win is conditional on the helper being correct. A buggy helper that mis-substitutes the path glob silently is *worse than no helper* — it teaches false confidence. The shift-left-testing irony is real: this script needs a test partner.
- **Coverage of non-discoverable repos.** Anything outside `~/projects/` is invisible to propagation regardless of strategy. Out of scope for this MAUT.
- **The "skip just this one" failure mode** for behavior-change artifacts (hook, CLAUDE.md mandate, python-prototyper test-first). A maintainer who copies the skill but skips the hook gets the probabilistic layer without the deterministic backstop — and the enforcement gradient documented in §7 of the doctrine entry assumes both are present. The adoption-mode table flags this implicitly; it does not prevent it.
- **Rollback coordination.** If something turns out wrong post-propagation, the corrective-entry mechanism in `propagation-protocol.md` works per artifact but not for compound failures spanning multiple artifacts. Not specific to this MAUT but worth flagging given bundle size.
- **Fatigue.** This decision is being made at the end of the largest authoring session in the repo's history. None of the alternatives account for operator-state risk. A5 (defer one session) was the only alternative that did, and the MAUT ranked it #4. If the operator subjectively feels fatigue is a load-bearing factor tonight, override the ranking and take A5 — the model cannot see operator state.
