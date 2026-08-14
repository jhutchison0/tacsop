# MAUT Audit: Adopt vs Build vs Skill for Knowledge-Base Traversal

**Date:** 2026-08-13
**Auditor:** decision-scientist
**Subject:** How agents traverse local knowledge bases: adopt graphify, build a utility, ship a skill, or combinations
**Branch:** `topic/kb-graph-traversal`
**Inputs:** [`docs/reviews/20260813_kb_graph_tool_evaluation.md`](20260813_kb_graph_tool_evaluation.md) (cited below as **eval**, findings F1 to F9), [`docs/plans/20260813_kb_graph_traversal_proposal.md`](../plans/20260813_kb_graph_traversal_proposal.md) (cited as **prop**), `.claude/skills/shift-left-testing/ENFORCEMENT.md` (cited as **enf**), `src/myproject/utils/weights.py`, `docs/plans/decision_science_utility.md` (YAML vocabulary).

**Headline:** D (skill-first, deferred build) wins at 0.860, ahead of the audit-added E (skill plus validate/orphans slice) at 0.773 and B (build now) at 0.667. The ranking is stable under every sensitivity test run. A (adopt graphify) cannot win at any egress weight, including zero: its elimination is overdetermined by Simplicity First. No Critical findings; the model is valid and the proposer's recommendation survives quantitative audit.

---

## 1. Decision Frame

The decision: which mechanism gives agents reliable traversal of this repo's knowledge base (103 markdown files, 1.0 MB, seven typed header relations, 157 proper links, 816 bare path mentions per prop's corpus table). The user's stated primary concern is private data leaving the machine. The decision is about to be operationalized as fleet doctrine inherited by 15 downstream repos (prop §Problem), which is exactly the posture where my checklist makes sensitivity analysis mandatory. Neither prior document ran one; both argued to conclusions in prose. This audit supplies the missing quantitative layer.

## 2. Alternatives

Four given, names sharpened; one added.

- **A. adopt-graphify-pinned**: `uv tool install graphifyy==0.9.42`, never vendored, docs-only corpus, in-session or Ollama backends, no read-gating hooks, query log disabled, upgrade only by diff review (eval Option A).
- **B. build-utility-now**: the full deterministic kb-graph utility, ~300 production lines plus 15 test slices, stdlib only, six query functions, fleet doctrine (eval Option B, specified in prop Approach A).
- **C. hybrid-doctrine**: B in-repo as fleet doctrine; graphify formally held available off-repo for downstream code-graph needs, revisited at its 1.0 (eval Option C).
- **D. skill-first-deferred-build**: `.claude/skills/traversing-the-knowledge-base/`, zero code now; the validate/orphans slice (~100 to 150 lines) built only when a demonstrated miss fires the explicit trigger (prop Recommendation).
- **E. skill-plus-slice** (added by this audit): D's skill plus the validate/orphans slice built now, not deferred. Added because it tests whether D's deferral is load-bearing or decorative, the same reason the 20260519 enforcement MAUT added A11 to change the shape of the option space. E is the only alternative that delivers the two grep-impossible query shapes this session at near-zero egress.

## 3. Criteria, Weights, Value Functions

Declared as an executable decision model in the `decision_science_utility.md` YAML vocabulary. Weights sum: 0.30 + 0.20 + 0.15 + 0.15 + 0.10 + 0.10 = **1.00**.

```yaml
decision: kb_traversal_adopt_vs_build
date: 2026-08-13
stated_primary_concern: data_egress        # user's words; holds the top weight
weighting_method: direct                   # deliberately not SMARTER; see below
criteria:
  - name: data_egress_containment
    weight: 0.30
    direction: minimize_exposure_scored_as_benefit
    scale: >
      exposure 0-100. 0 = no egress path by construction; 35 = a new-party
      vector exists but requires misconfiguration to fire; 100 = active
      silent egress to a party beyond the session baseline.
    value_fn: logistic
    params: {midpoint: 35, steepness: -0.08}   # normalized to span [0,1] on 0-100
  - name: simplicity_maintenance
    weight: 0.20
    direction: minimize_surface_scored_as_benefit
    scale: >
      effective LOC the fleet must maintain or trust. Own code at full
      weight; pinned third-party at 0.1 (diff-review-gated upgrades mean
      reviewing diffs, not owning lines).
    value_fn: logarithmic
    params: {S_max: 60000}                     # u = 1 - log10(1+S)/log10(1+S_max)
  - name: traversal_capability
    weight: 0.15
    direction: maximize
    scale: query shapes reliably delivered, 0-8 (six named shapes plus extras)
    value_fn: piecewise_linear
    params: {breakpoints: [[0, 0.0], [4, 0.50], [6, 0.90], [8, 1.0]]}
  - name: behavior_change_reliability
    weight: 0.15
    direction: maximize
    scale: adoption probability 0-100 (will agents actually route through it)
    value_fn: logistic
    params: {midpoint: 50, steepness: 0.08}    # normalized to span [0,1] on 0-100
  - name: time_to_value
    weight: 0.10
    direction: minimize_delay_scored_as_benefit
    scale: sessions until agents have working traversal guidance, 0-6
    value_fn: exponential
    params: {rate: 0.5}                        # u = (e^-0.5t - e^-3) / (1 - e^-3)
  - name: reversibility_optionality
    weight: 0.10
    direction: maximize
    scale: >
      constructed direct rating 0-100 with anchors. 100 = delete one
      directory; 75 = revert code, tests, one doctrine entry; 50 = uninstall
      plus unwind fleet doctrine; 25 = unwind fleet-adopted habits and
      third-party expectations; 0 = effectively stuck.
    value_fn: linear
    params: {low: 0, high: 100}
alternatives:
  A_adopt_graphify_pinned:
    raw: {data_egress_containment: 40, simplicity_maintenance: 5900,
          traversal_capability: 5.75, behavior_change_reliability: 60,
          time_to_value: 1.0, reversibility_optionality: 40}
  B_build_utility_now:
    raw: {data_egress_containment: 2, simplicity_maintenance: 650,
          traversal_capability: 6.0, behavior_change_reliability: 45,
          time_to_value: 2.0, reversibility_optionality: 60}
  C_hybrid_doctrine:
    raw: {data_egress_containment: 15, simplicity_maintenance: 1830,
          traversal_capability: 6.6, behavior_change_reliability: 40,
          time_to_value: 2.5, reversibility_optionality: 35}
  D_skill_first_deferred_build:
    raw: {data_egress_containment: 0, simplicity_maintenance: 0,
          traversal_capability: 4.0, behavior_change_reliability: 55,
          time_to_value: 0.0, reversibility_optionality: 95}
  E_skill_plus_slice:
    raw: {data_egress_containment: 2, simplicity_maintenance: 270,
          traversal_capability: 5.4, behavior_change_reliability: 60,
          time_to_value: 0.5, reversibility_optionality: 80}
```

### Weight justification

| Criterion | Weight | Why this weight |
|---|---:|---|
| data_egress_containment | 0.30 | The user's stated primary concern, so it holds the top weight by construction, mirroring how the 20260519 enforcement MAUT gave determinism 0.30 for the same reason. Not higher: the eval's exposure analysis shows in-session use adds no new party, so the concern is specific (silent new-party routing), not total. |
| simplicity_maintenance | 0.20 | Simplicity First is a written pillar, and the 15-downstream-repo fleet multiplies every maintained line (prop §Problem: "the bar for adding new machinery should be correspondingly high"). |
| traversal_capability | 0.15 | The point of the exercise; a choice that delivers nothing loses regardless of hygiene. Below the top two because four of six query shapes are already achievable manually (prop Approach A cons). |
| behavior_change_reliability | 0.15 | Realized value is capability times adoption. In-repo evidence: shift-left existed as prose "for months before anyone wrote a hook" (prop Approach B) and needed a four-layer enforcement gradient to hold (enf §Enforcement Gradient). Weighted equal to capability because unused capability is worth zero. |
| time_to_value | 0.10 | Real but least durable: the open topic branch argues for closing this session, yet nothing external deadlines the decision. |
| reversibility_optionality | 0.10 | Graphify is pre-1.0 and fast-moving (eval F3, F9) and the corpus conventions are still evolving, so option preservation has value, but it is second-order next to egress and simplicity. |

**Why direct weights, not SMARTER.** `weights.py` provides SMARTER, and the temptation is to use house machinery. SMARTER is valid for rank-ordered criteria; the user here expressed cardinal intensity ("primary concern"), which per this agent's own audit checklist calls for direct elicitation. Cross-check: ROC weights for six ranked criteria would give 0.41 / 0.24 / 0.16 / 0.10 / 0.06 / 0.03. That is steeper than the elicited intensity supports; egress is primary but not "worth all other criteria combined." The direct vector is deliberately flatter.

**Stated-priority cross-check.** Egress is named primary and carries the top weight. Aligned. Section 6 shows the decision does not in fact hinge on it, which is a finding, not an error.

### Value function justification (no silent linear defaults)

| Criterion | Function | Why this shape and not linear |
|---|---|---|
| data_egress_containment | logistic (midpoint 35) | Threshold phenomenon. The category boundary the user's concern draws is "does a new-party vector exist at all"; the gap between no-path-by-construction and vector-exists-behind-a-misconfiguration is categorically larger than gradations among bad states. Midpoint 35 sits at that boundary. Linear would underprice crossing it. |
| simplicity_maintenance | logarithmic | Maintenance burden tracks orders of magnitude, not raw counts: the fleet-relevant comparison is 0 vs 300 vs 59,000 lines, and prop itself argues in ratios ("roughly 1/200th the code size"). Diminishing-returns shape per the selection guide. This shape is load-bearing for B vs D; noted in Limitations. |
| traversal_capability | piecewise_linear | Discrete capability bands with domain-specified breakpoints: 4 shapes manual (0.50), 6 shapes deterministic (0.90), engine-grade extras (1.0). The final segment is nearly flat because graphify's differentiators "target problems we do not have in this repo" (eval §Fit). Linear would overpay for beyond-corpus capability. |
| behavior_change_reliability | logistic (midpoint 50) | Threshold behavior with evidence: below some adoption rate an artifact functionally does not exist ("it ships and sits unused," prop Approach A risk), and sub-threshold compliance historically triggered extra machinery cost (the shift-left hook, enf §The Problem). Above threshold, usage begets usage. |
| time_to_value | exponential (decay, rate 0.5) | Urgency shape per the guide. Value of guidance compounds while the branch and debate are live; each deferred session decays it. Mild rate: this is doctrine, not an incident. |
| reversibility_optionality | linear, justified | Not a silent default. The scale is a constructed direct-rating scale with defined anchor points at approximately equal preference increments (standard MAUT practice for constructed attributes); linear is then the faithful mapping. |

All six functions are monotone. No non-monotone shapes were needed, so no ideal-range justifications are required.

## 4. Scoring

Raw scores per the YAML above; u after the value function. Tags: [E] evidence-anchored, [J] judgment. One-line evidence per cell.

**C1 data_egress_containment** (w 0.30)

| Alt | Raw | u | Evidence |
|---|---:|---:|---|
| A | 40 | 0.42 | [E] Vector class survives constraint: ambient-key routing (eval F2), shipped-regression precedent (F3), CDN loads (F5); constraints are written policy, which this repo's own evidence says is probabilistic (enf layers 1-2). |
| B | 2 | 0.99 | [E] Stdlib only, no network imports; "zero egress by construction" (eval Option B; prop Approach A pros). Residual 2 is baseline supply chain. |
| C | 15 | 0.88 | [J] In-repo zero (B's machinery); doctrine pre-approval makes conditional downstream graphify adoption more likely, importing a fraction of A's exposure fleet-wide. |
| D | 0 | 1.00 | [E] No code, no new paths; "no egress risk beyond the baseline every session already has" (prop Approach B pros; eval exposure analysis point 1). |
| E | 2 | 0.99 | [E] Slice is stdlib subset of B's construction; skill adds none. |

**C2 simplicity_maintenance** (w 0.20). S = effective LOC (own x1.0, pinned third-party x0.1).

| Alt | S | u | Evidence |
|---|---:|---:|---|
| A | 5,900 | 0.21 | [J] 59,000 third-party lines (eval §What graphify is) at 0.1 diff-review discount; "upgrade only by diff review" (eval Option A) is the recurring maintenance act. Undiscounted scoring gives u 0.00; ranking unchanged either way. |
| B | 650 | 0.41 | [E] ~300 production plus ~350 test lines (prop §Rough size); TEMPLATE-COPY so fleet cost is adoption plus sync, not divergence (prop §Doctrine artifact). |
| C | 1,830 | 0.32 | [J] B's 650 plus expected-value graphify exposure (0.2 probability of one-to-three downstream adoptions times 5,900) plus dual-track doctrine text. |
| D | 0 | 1.00 | [E] "No new dependency, no new test surface" (prop Approach B pros); prose is the repo's native maintained medium. |
| E | 270 | 0.49 | [E] Slice sized 100 to 150 production lines plus tests (prop Recommendation: "roughly 100 to 150 lines"). |

**C3 traversal_capability** (w 0.15). x = query shapes reliably delivered.

| Alt | x | u | Evidence |
|---|---:|---:|---|
| A | 5.75 | 0.85 | [J] Rich engine, but corpus-fit discount: 816 bare backtick mentions (5:1 over proper links) would ride non-deterministic LLM-inferred edges (prop finding 1; eval F2 doc path), and deterministic dangling-reference validation is not a listed feature (eval F1-F9 silent on it). |
| B | 6.0 | 0.90 | [E] All six shapes deterministic; validate() reproduces the live tasks.md P3 dangling-reference find (prop §Traversal queries). |
| C | 6.6 | 0.93 | [J] B in-repo plus a downstream code-graph option no repo has requested (prop Approach C: "no downstream repo has asked"). |
| D | 4.0 | 0.50 | [E] Skill delivers 4 shapes via manual grep recipes; "states plainly which two shapes grep cannot do reliably, orphans and validate, and defers them" (prop Approach B). |
| E | 5.4 | 0.78 | [J] 4 manual shapes plus the two deterministic ones; those two are the highest-marginal-value pair (only shapes with a live verified failure, prop finding 2). |

**C4 behavior_change_reliability** (w 0.15)

| Alt | Raw | u | Evidence |
|---|---:|---:|---|
| A | 60 | 0.70 | [J] Purpose-built assistant integration (skill for 20+ assistants, eval §What graphify is), but constrained-A forgoes the read-gating hooks that made it deterministic (eval F7 declined), leaving probabilistic layers. |
| B | 45 | 0.40 | [E] "Untested assumption: that agents call a CLI tool proactively... Nothing today routes an agent toward it"; "Medium adoption risk... ships and sits unused" (prop Approach A cons and risk). |
| C | 40 | 0.30 | [J] B's gap plus dual-track doctrine dilutes the instruction (which tool, when). |
| D | 55 | 0.60 | [J] Skills are the harness's native surfacing mechanism, plus an explicit falsifier check after 3 to 5 sessions (prop open question 1); still Layer 1-2 probabilistic with "no audit log if it fails quietly" (prop Approach B cons; enf gradient). |
| E | 60 | 0.70 | [J] Skill routes, and one-command recipes (`kb_graph.py validate`) lower per-use activation energy versus multi-step grep chases. |

**C5 time_to_value** (w 0.10). t = sessions until working guidance.

| Alt | t | u | Evidence |
|---|---:|---:|---|
| A | 1.0 | 0.59 | [J] Install is minutes; constraint doctrine, corpus config, and fleet documentation are the session of work (eval Option A's six constraint clauses). |
| B | 2.0 | 0.33 | [E] Full slice count plus prop's own escalation note that the build "likely does warrant a CONOP" (prop §Escalation). |
| C | 2.5 | 0.25 | [J] B plus hybrid doctrine authoring. |
| D | 0.0 | 1.00 | [E] "Ships this session" (prop Approach B pros). |
| E | 0.5 | 0.77 | [J] Skill lands now; 150-line slice is one feature-development engagement (prop's propagate_doctrine.py analog: 124 lines, 14 tests, built test-first). |

**C6 reversibility_optionality** (w 0.10)

| Alt | Raw | u | Evidence |
|---|---:|---:|---|
| A | 40 | 0.40 | [J] Uninstall plus unwind doctrine plus retrain habits; commercial trajectory risk prices in a forced future migration (eval F9). |
| B | 60 | 0.60 | [E] Revert code, tests, doctrine entry; harder once 15 repos adopt TEMPLATE-COPY (prop Approach A cons, fleet-multiplication). |
| C | 35 | 0.35 | [J] Both artifacts plus a pre-approval that is hard to un-say once a downstream repo acts on it (prop Approach C). |
| D | 95 | 0.95 | [E] "Trivially reversible: delete one directory" (prop Approach B pros); full build spec preserved for later exercise. |
| E | 80 | 0.80 | [J] Directory plus one small slice to revert; propagation exposure begins. |

## 5. Ranking

U(a) = Σ wᵢ uᵢ. Verified programmatically; weights sum 1.00; all u in [0, 1].

| Rank | Alternative | C1 0.30 | C2 0.20 | C3 0.15 | C4 0.15 | C5 0.10 | C6 0.10 | **Utility** |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **D skill-first-deferred-build** | 1.00 | 1.00 | 0.50 | 0.60 | 1.00 | 0.95 | **0.860** |
| 2 | **E skill-plus-slice** | 0.99 | 0.49 | 0.78 | 0.70 | 0.77 | 0.80 | **0.773** |
| 3 | **B build-utility-now** | 0.99 | 0.41 | 0.90 | 0.40 | 0.33 | 0.60 | **0.667** |
| 4 | **C hybrid-doctrine** | 0.88 | 0.32 | 0.93 | 0.30 | 0.25 | 0.35 | **0.573** |
| 5 | **A adopt-graphify-pinned** | 0.42 | 0.21 | 0.85 | 0.70 | 0.59 | 0.40 | **0.500** |

D wins on five of six criteria and loses only capability. The D-to-E gap (0.087) exceeds any single judgment-cell swing (a full 0.15 u-swing on a 0.15-weight criterion moves 0.023); overturning it needs four or more judgment cells moving together against D.

## 6. Sensitivity Analysis

OAT on the top two weights, plus the two targeted threshold questions, plus one beyond-OAT scenario for the model's known independence violation. All runs renormalize remaining weights proportionally.

**OAT, egress weight 0.30 varied to 0.20 and 0.40:**

| w_egress | Order | Utilities |
|---:|---|---|
| 0.20 | D E B C A | 0.840 / 0.743 / 0.621 / 0.529 / 0.511 |
| 0.30 (base) | D E B C A | 0.860 / 0.773 / 0.667 / 0.573 / 0.500 |
| 0.40 | D E B C A | 0.880 / 0.804 / 0.713 / 0.617 / 0.488 |

No rank change anywhere in the range.

**OAT, simplicity weight 0.20 varied to 0.10 and 0.30:**

| w_simplicity | Order | Note |
|---:|---|---|
| 0.10 | D E B C A | D-to-E gap narrows to 0.034 |
| 0.20 (base) | D E B C A | gap 0.087 |
| 0.30 | D E B C A | gap 0.140 |

No rank change. The only reachable flip in the whole weight space: **E overtakes D when the simplicity weight falls below about 0.035**, an 83 percent cut to a weight that carries a written pillar plus a 15-repo multiplier. Not a defensible weighting for this repo.

**Q1: how far must the egress weight drop before A wins?** There is no such weight. Sweeping w_egress from 0.30 to exactly 0: A rises only from 0.500 to 0.533 while D stays above 0.80. A's deficit is overdetermined: even with the privacy concern deleted from the model, A still loses 0.21 to 1.00 on simplicity and 0.40 to 0.95 on reversibility. Pushing further, with egress at zero and capability weight raised at simplicity's expense, A still never reaches rank 1; at w_capability = 0.41 the winner flips to E, not A. To make A win you must simultaneously zero the egress weight, cut simplicity below about 0.07, and push capability past 0.45: a weighting that contradicts the user's stated concern and the repo's written pillar at the same time. This quantifies prop's claim that "the size mismatch is a reason not to adopt it at all, independent of the privacy question."

**Q2: how far must behavior-change reliability drop before D loses to B?** Within the additive model, no distance suffices. Even at u_behavior(D) = 0 (the skill is never read by anyone), D scores 0.770 against B's 0.667, carried by egress, simplicity, time, and reversibility. The honest version of this question requires breaking additive independence, because if the skill goes unread, D's capability score (conditional on the skill being used) collapses too. Modeled jointly: skill adoption raw 20 (u 0.07) and capability u 0.10 gives **D_joint = 0.720, still above B's 0.667**. B does not gain from D's failure because B carries the same unresolved routing gap (prop: "nothing today routes an agent toward it"); B's own capability is equally conditional on its 0.40 adoption score, which the additive model does not discount. For B to beat D you must believe agents will reliably invoke an unadvertised CLI while reliably ignoring a skill, an asymmetry with no in-repo evidence; the shift-left history (enf) shows both prose layers underperforming, not one. And the D design already prices this branch: its trigger converts D into E when a miss is demonstrated.

**Joint-failure corollary for E:** in the same skill-failure world, E_joint = 0.607, below D_joint = 0.720. E's insurance premium buys deterministic capability that is only realized if the routing layer works; but if the routing layer works, D's trigger buys the same capability later at the same price. Within this model, deferral is optimal on both branches. The one world where E beats D is a costly dangling-reference incident landing inside D's 3-to-5-session observation window; the model prices that window only through time_to_value (see Limitations).

**Ranking stability statement:** the full order D > E > B > C > A is unchanged across every OAT run and both threshold sweeps. The top choice is robust under all realistic re-weightings; the only flip anywhere in reach (D to E) requires abandoning the Simplicity First weight.

## 7. Dominance Check

No strict dominance anywhere. One practical elimination: **C is near-dominated by B**. C's sole edge is +0.03 capability, a judgment increment smaller than that cell's uncertainty, while it loses concretely on egress (0.88 vs 0.99), simplicity (0.32 vs 0.41), behavior (0.30 vs 0.40), time (0.25 vs 0.33), and reversibility (0.35 vs 0.60). C should exit the option set unless a downstream repo actually requests code-graph traversal, which matches prop's narrower point that the hybrid decides "a hypothetical for repos that are not in this session."

## 8. Findings

### Critical

None. Weights sum to 1.00, no negative weights, all utilities in [0, 1], value functions all monotone and justified, top weight matches the stated primary concern. The model is valid and the leading option survives its audit.

### Warnings

- **W1. Sensitivity analysis was absent from both prior documents for a decision being operationalized as fleet doctrine.** Location: eval §Lead assessment; prop §Recommendation. Both recommend in prose with no perturbation test. Why it matters: a ranking that flips under small weight changes is a different decision object than a stable one, and doctrine inherited by 15 repos is the definition of operationalized. Fix: supplied by this audit; carry the YAML model above into the eventual ADR so the graphify-1.0 revisit re-runs weights instead of re-arguing prose.
- **W2. Additive independence is violated between traversal_capability and behavior_change_reliability.** Location: this model, C3 and C4. Realized value is closer to capability times adoption than a weighted sum; the additive form overstates high-capability low-adoption options (A, B, C). Why it matters: the bias direction favors the losers and the winner still wins (D_joint 0.720 vs B 0.667), so the conclusion stands, but any re-scoring that narrows the gap must re-run the joint scenario, not just OAT. Fix: at re-run, use a multiplicative aggregation for these two criteria or keep the joint-failure scenario as a mandatory companion test.
- **W3. The egress criterion may be lexicographic rather than compensatory.** Location: task framing ("stated primary concern"). If the user's true rule is "any new-party vector is unacceptable at any capability gain," MAUT trade-off aggregation is the wrong frame and A and C are eliminated before scoring. Why it matters: frame choice, not arithmetic, would then drive the decision. The conclusion is unchanged either way (A and C lose under both frames), which is why this is a warning, not critical. Fix: confirm with the user; if lexicographic, record egress as a screening constraint in the ADR, not a weighted criterion.
- **W4. C makes a fleet-level commitment nobody requested.** Location: eval Option C. A doctrine entry pre-approving graphify downstream lowers the adoption barrier fleet-wide (raising C1 exposure) in exchange for a +0.03 judgment-level capability edge. Why it matters: it spends real egress and reversibility budget on a hypothetical. Fix: drop C; a downstream repo with a genuine code-graph need runs its own evaluation then (prop Approach C reasoning).

### Suggestions

- **S1. The decision_science module this model is written against does not exist.** `docs/plans/decision_science_utility.md` (2026-03-26) specifies scorer, value functions, and sensitivity; only `weights.py` was ever built, and this is at least the fourth hand-computed MAUT in `docs/reviews/` (plan1, pass4, pass5, this). At this cadence, Waves 1 and 2 of that CONOP would let the YAML block above execute directly and make audits reproducible. Related: the five dangling decision-science doc references in `docs/tasks.md` P3 that prop's validate() example found belong to this same plan family.
- **S2. Set the re-run triggers now.** Re-score C3 and C4 with observed data at the 3-to-5-session skill check (prop open question 1), at graphify 1.0 (eval Option C), or when D's demonstrated-miss trigger fires. The model's judgment cells become evidence cells at those points.
- **S3. If D ships, write the ADR prop sketched and embed this YAML model in it.** The ADR's "surprising without context" test is met precisely because a 106k-star tool was declined; the numbers above are the context.

## 9. What the Model Cannot Capture

1. **Capability-adoption correlation** (W2): additive form overstates A, B, C. Direction of bias runs against the winner; D wins anyway.
2. **Option value of D's trigger.** D embeds a real option (build the slice when evidence arrives) that static MAUT prices only partly through reversibility. A decision-tree valuation would raise D. Conservative: biases against the winner.
3. **Cost of a miss inside the observation window.** If a dangling-reference failure with real cost lands during D's 3-to-5-session watch, E was the better choice ex post. The model prices delay through time_to_value only; it does not price incident severity. This is the one identified world where E beats D.
4. **Log-shape dependence on C2.** The logarithmic value function is load-bearing for D's margin over E and B on simplicity; a linear shape on raw LOC would compress D's edge (though not the ranking; verified: order holds because D also wins C1, C5, C6).
5. **Judgment density.** 14 of 30 cells are [J]. The D-to-E gap (0.087) survives any single-cell swing and needs 4 or more coordinated swings to close, but a reader who scores the [J] cells differently should re-run the script pattern in section 6, not eyeball it.

## 10. Recommendation

Adopt **D, skill-first-deferred-build**, as the proposer specified: ship the skill this session, track the trigger in `docs/tasks.md`, build only the validate/orphans slice when the trigger fires. The quantitative case adds two things the prose debate could not: A's rejection does not depend on the privacy concern at all (it loses at egress weight zero), and D's win does not depend on optimism about skill adoption (it survives skill-failure scenarios that also drag its capability to near zero). Runner-up E is the hedge to take only if the user judges the cost of one more months-long dangling-reference blind spot as unacceptable; that judgment is about incident severity, which sits outside this model (Limitations 3).

---

**What I checked:** weights sum to 1.00; no negative weights; all value function outputs within [0, 1] (logistic and exponential normalized over their scales); all six functions monotone, so no non-monotone justifications required; no silent linear defaults (one linear, justified via constructed equal-interval scale); minimize criteria scored as benefit per house convention (20260519 MAUTs); SMARTER deliberately not used for cardinal intensities, with ROC cross-check; stated priority carries the top weight; evidence or judgment tag on every cell; OAT on the top two weights plus two targeted flip-threshold sweeps plus one joint-failure scenario; dominance check; arithmetic verified by script, not by hand.
