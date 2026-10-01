# Proposal: Decision Science Module — Gap Analysis and Next Additions

**Status**: Proposed — awaiting code-reviewer challenge and lead decision
**Author**: proposer
**Date**: 2026-03-26
**Priority**: P1 — decision science is core professional domain; six downstream repos affected
**Context**: Waves 1–3 shipped 2026-03-26. This proposal identifies what remains before the module is
defensibly "complete" for production deployment across downstream repos.

---

## Problem

Waves 1–3 delivered a solid MAUT core: seven value functions, an additive scorer, three sensitivity
methods, three visualization helpers, and 145+ tests. That is infrastructure. What is missing is
*completeness* — the set of capabilities a practitioner would reach for before making a real
decision and would find absent. A library that stops at "produce a utility score" leaves the hardest
practitioner questions unanswered.

This proposal answers four specific questions:

1. What would a practitioner expect that is not here?
2. What biases does the current design leave unguarded?
3. What integration gaps exist for the six downstream repos?
4. What should we NOT add?

---

## What Is Already Here (Baseline)

- `value_functions.py`: 7 functions (linear, exponential, logarithmic, logistic, step, gaussian,
  piecewise_linear)
- `scorer.py`: MAUTScorer — additive aggregation, `from_yaml()`, `validate_weights()`
- `sensitivity.py`: `one_at_a_time()`, `monte_carlo()`, `scenario_compare()`
- `visualization.py`: radar chart, tornado plot, rank stability heatmap
- `DecisionResult`: alternative name, aggregate utility, per-criterion weighted breakdown
- One integration test confirming the end-to-end pipeline

Notable: `monte_carlo()` returns a rank frequency matrix but no derived scalar. `scenario_compare()`
requires complete weight vectors. `score()` requires all criterion values to be present.

---

## Question 1: What Would a Practitioner Expect?

### Gap A: Dominance Analysis

**What it is**: A formal check — is alternative A at least as good as B on every criterion, and
strictly better on at least one? If so, A dominates B and B can be eliminated regardless of weights.

**Why it matters**: Dominance is weight-independent. It is the one analytical result that does not
require the practitioner to have committed to a weight vector. In any real decision briefing, this is
the first question asked: "Is there an option we can eliminate without any assumptions?"

**Current gap**: Not present. The scorer produces utilities but never compares alternatives
head-to-head at the criterion level in raw-score space. Dominance operates on utilities (after value
function transformation), not raw scores, so it is a natural extension of the existing scorer output.

**Implementation surface**: A function `dominance_matrix(results: list[DecisionResult]) ->
dict[str, list[str]]` returning `{alternative: [alternatives it dominates]}`. Operates on the
`breakdown` dict already present in `DecisionResult` — no new scoring required. Approximately 20
lines of logic, one test file.

**Risk level**: Low. Pure data manipulation on existing outputs.

---

### Gap B: Rank Reversal Detection

**What it is**: Does adding or removing an alternative change the ranking of the remaining
alternatives? In additive MAUT, rank reversal should not occur — the score of A is independent of
whether B exists. But value function normalization creates a hidden coupling: if the practitioner
chose `low` and `high` parameters relative to the current alternative set (a common mistake),
adding a new extreme alternative will rescale utility and can flip ranks.

**Why it matters**: Rank reversal is the single most common methodological flaw caught during peer
review of MAUT analyses. A practitioner who does not check for it is exposed. In our context,
quest-engine and tactics-game both define value function bounds relative to observed data ranges —
which creates exactly this risk.

**Current gap**: `validate_weights()` catches weight errors. Nothing catches value function
normalization scope-coupling. The current `from_yaml()` lets a practitioner encode relative bounds
without any warning.

**Two sub-proposals**:

**B1 (detection, bold)**: A `rank_reversal_check(scorer, alternatives, candidate) ->
bool` function: add the candidate to the set, re-score, compare original ranking. Warn if ranks
changed. This is purely analytical — it does not prevent the problem, but it makes the symptom
observable. ~30 lines.

**B2 (prevention, bolder)**: Add a docstring warning to `from_yaml()` and `MAUTScorer.score()` that
absolute bounds (not relative-to-alternatives) are required for rank-reversal safety. This is zero
code, but it encodes the domain constraint where practitioners will see it. Should be done regardless
of B1.

**Recommendation**: Do B2 immediately (zero-cost). Defer B1 until a downstream repo actually
encounters rank reversal — that is the signal that detection logic earns its keep.

**Risk level**: B2 is zero risk. B1 is low risk, medium value.

---

### Gap C: Decision Robustness Metric (single scalar)

**What it is**: A single number summarizing how stable the #1 ranking is. The most natural
derivation from what already exists: the rank-1 frequency from `monte_carlo()` for the top-ranked
alternative. A value of 0.91 means "under Dirichlet-sampled weights, the winner holds 91% of the
time." That is a briefable number.

**Why it matters**: Practitioners and decision-makers do not read heatmaps in briefings. They ask
"how confident are you?" The current API requires the caller to run `monte_carlo()`, inspect the
frequency matrix, and extract `freq["winner"]["1"]` themselves. That calculation is 3 lines of
caller code — but it is code that every downstream repo will re-write independently.

**Current gap**: `monte_carlo()` returns the full frequency matrix. There is no derived scalar. The
`rank_stability_heatmap()` visualization helps but requires matplotlib and is not programmable.

**Proposed addition**: A function `robustness_score(scorer, alternatives, n_samples, seed) ->
float` that runs Monte Carlo internally and returns the rank-1 frequency of the baseline winner.
Optionally returns `tuple[float, str]` — (score, winner_name) — to make it self-contained. This is
~10 lines wrapping `monte_carlo()`.

**Alternative (bolder)**: Return a structured `RobustnessReport` dataclass: `{winner: str, score:
float, runner_up_score: float, margin: float}`. The margin (winner's rank-1 frequency minus
runner-up's rank-1 frequency) is more informative than the raw score alone.

**Recommendation**: The `RobustnessReport` dataclass. It is only ~15 lines more than the scalar
version but it gives the practitioner the margin without requiring them to inspect the matrix. The
margin is the operationally relevant number: a winner at 70% with a runner-up at 65% is fragile; a
winner at 70% with a runner-up at 20% is not.

**Risk level**: Low. Thin wrapper over existing `monte_carlo()`.

---

### Gap D: Explain/Justify Output (human-readable narrative)

**What it is**: A function that produces a plain-English statement of why alternative A won — which
criteria drove the result, what the margin was, and where the runner-up was competitive.

**Why it matters**: Every OR analysis ends in a briefing. "Alpha scored 0.721" is not a briefable
result. "Alpha leads on effectiveness (0.298 of 0.350 possible) and risk (0.215 of 0.250 possible).
Bravo is competitive on cost but trails by 0.124 overall" is a briefable result. Currently, the
caller must construct this narrative themselves from the `breakdown` dict.

**Current gap**: `DecisionResult` has all the data needed but no narrative layer.

**Proposed addition**: A function `explain(results: list[DecisionResult], scorer: MAUTScorer) ->
str` that returns a multi-line narrative. Inputs are the ranked result list (already available from
`scorer.rank()`) and the scorer (for criterion weights, to know what was theoretically achievable).
Key content per alternative: actual weighted contribution vs. theoretical maximum for each criterion.

**The bold alternative**: Make `explain()` return a structured dict (JSON-serializable) rather than
a plain string, so downstream repos can format it themselves or pass it to an LLM for further
elaboration. Structure: `{winner: str, why: [{criterion: str, contribution: float, max_possible:
float, pct_captured: float}], margin_over_runner_up: float, runner_up: str}`. This is the
agent-friendly interface the CONOP identified as Wave 4 territory — but the data structure costs
nothing to add now, and it avoids string parsing by downstream callers.

**Recommendation**: Return the structured dict. The string representation is trivially derived from
the dict. The dict is infinitely more useful for programmatic consumers, which is the primary use
case for all six downstream repos.

**Risk level**: Low-medium. The dict output is a new API surface. Needs careful design of the dict
schema before implementation.

---

## Question 2: What Biases Does the Current Design Leave Unguarded?

### Bias A: Anchoring from Default `from_yaml()` Parameters

**The problem**: `from_yaml()` silently accepts any `low` and `high` values for `linear()` and
`exponential()`. There is no check that these bounds are plausible given the alternatives being
scored. If a practitioner sets `low: 0, high: 100` for a criterion where all alternatives score
between 40 and 60, the value function compresses the discrimination into a narrow middle band and
suppresses criterion influence — but the weight still says it matters 35%. The criterion is
effectively deweighted through the back door of poorly chosen bounds.

**What this does**: It amplifies the anchoring effect. The practitioner chose 0 and 100 because
those are round numbers, not because they represent meaningful anchor points. The result: a criterion
that looks like it has 35% weight but functionally contributes less because all alternatives score
near 0.5 utility.

**Mitigation options**:

**Option 1 (documentation)**: Docstring warning in `from_yaml()` and `linear()`: "bounds should
represent the best/worst plausible outcome for your decision context, not the min/max of the current
alternative set."

**Option 2 (runtime warning)**: After `rank()`, compute the actual utility range each criterion
achieved across the alternative set. If any criterion's utility range is less than 0.2 (all
alternatives score between 0.4–0.6 utility), emit a `warnings.warn()` about suppressed
discrimination. This is ~15 lines in `MAUTScorer.rank()`.

**Option 3 (no action)**: This is a practitioner responsibility. The library should not second-guess
parameter choices.

**Recommendation**: Option 2. The `warnings.warn()` pattern is non-intrusive — it does not break
any existing caller, it does not require a new API, and it surfaces a real methodological risk at
exactly the right moment (when scoring is run). This is the one bias mitigation that earns its keep
without adding complexity.

---

### Bias B: Framing Effect from Maximize/Minimize Convention

**The problem**: The current design encodes direction implicitly via `low` and `high` parameter
order. `linear(x, low=100, high=0)` means "lower is better." This works but is invisible. A
practitioner reviewing a YAML file sees `low: 100, high: 0` and must reason through what that means.
A reviewer who misreads it as a typo and "fixes" it has just inverted the criterion direction without
any error being raised.

**The test suite catches this correctly** (see e2e test: `low: 100, high: 0` for cost). But the
design relies on the practitioner knowing the convention.

**Mitigation**: Add an optional `direction: minimize` field to the YAML schema and have `from_yaml()`
swap `low` and `high` when `direction: minimize` is specified. This is explicit, self-documenting,
and makes the criterion intent visible in config. It does not change any existing behavior — it is
additive.

**Risk level**: Low. Schema extension, backwards-compatible.

**Recommendation**: Worth doing in the next session. Three lines in `from_yaml()`, one YAML field,
one test case. The documentation value outweighs the implementation cost.

---

### Bias C: Selection Bias in Criteria Choice

**The problem**: The current library has no mechanism to surface whether the criteria set is
complete or appropriately independent. A practitioner can define overlapping criteria (e.g., both
"effectiveness" and "damage_output" for the same underlying attribute) and double-count that
dimension without any signal. This is a structural bias, not a numerical one.

**Assessment**: This is genuinely hard to solve in a utility library. Criteria independence
(preferential independence, utility independence) is a property the practitioner must assert, not
something a library can verify algorithmically. Even human experts regularly fail this check.

**Recommendation**: Document the assumption explicitly in the `MAUTScorer` class docstring. Add a
note to `from_yaml()` that criteria are assumed to be preferentially independent. This sets the
right expectation without creating false safety theater.

**No code needed.** This is a documentation task.

---

### Bias D: Equal-Weight Assumption as Implicit Default

**The problem**: The current API has no default weights. `validate_weights()` enforces that weights
are provided and sum to 1.0. But it does not warn when weights are suspiciously equal (e.g., all
criteria weighted 0.25). Equal weighting is a common anchoring default that often gets used because
it "feels balanced" rather than because preference elicitation was done.

**Assessment**: Equal weights may be correct. This is not always a bias. A `warnings.warn()` when
all weights are within a tolerance of 1/N would be noisy and annoying.

**Recommendation**: No action. The right mitigation for equal-weight bias is the `weights.py`
module — practitioners should use SMARTER/rank-reciprocal instead of assigning raw weights. The
docstring on `MAUTScorer` and `from_yaml()` should point to `weights.py` as the preferred weight
elicitation path. This is already implied by the CONOP architecture but not explicitly stated in
the code.

---

## Question 3: Integration Gaps for the Six Downstream Repos

### Gap 1: quest-engine — Missing-Attribute Weight Redistribution

**The situation**: quest-engine sometimes evaluates alternatives where one or more criteria have no
available score (attribute is absent). Their current approach: skip the criterion and score with
whatever criteria are available. The result is an unnormalized utility — a `U` that does not sum over
a full weight budget.

**Current behavior in MAUTScorer**: `score()` raises `ValueError` if any criterion value is missing
from `raw_scores`. This is the correct behavior for a complete model. It is the wrong behavior for
quest-engine's use case.

**Should we support this?**

This is the core question. Two approaches:

**Approach A (strict, current)**: Require all criterion values. Downstream repos handle missing
attributes before calling the scorer. quest-engine redistributes weights in their domain layer and
passes a complete (reduced) criterion set.

Pros: Clean contract. The scorer does one thing. Weight redistribution is domain logic, not scorer
logic.
Cons: quest-engine must re-implement weight redistribution logic. If multiple repos need this, it
gets re-implemented multiple times.

**Approach B (permissive, bold)**: Add an optional `allow_missing: bool = False` parameter to
`score()`. When True, missing criteria are dropped and remaining weights are renormalized
proportionally before scoring. Emit a `warnings.warn()` identifying which criteria were dropped.

Pros: Handles the real-world case. All the weight redistribution logic is in one place.
Cons: Widens the scorer's contract. A `score()` with `allow_missing=True` returns a utility that is
not comparable to one with `allow_missing=False` unless the same criteria were missing in both — a
subtle trap for ranking across heterogeneous alternatives.

**Recommendation**: Approach B, with a constraint: `allow_missing` is only valid on `score()`, not
on `rank()`. `rank()` requires all alternatives to have the same criteria — comparing utilities
across alternatives with different criterion sets is not valid MAUT and should remain an error. This
gives quest-engine the capability they need without enabling the unsafe cross-alternative comparison.

**Risk level**: Medium. New API surface. Needs careful documentation of the constraint.

---

### Gap 2: tactics-game — DoctrineProfile Constraints (enabled/disabled tactics)

**The situation**: tactics-game has a `DoctrineProfile` concept: certain tactics are categorically
disabled based on doctrine (e.g., a doctrine may prohibit indirect fire in civilian areas). A
disabled tactic should score 0 regardless of its utility. This is a hard constraint, not a soft
preference.

**Is this in scope?**

No. This is not a scoring library concern. DoctrineProfile is a domain concept — it controls which
alternatives enter the scoring set, not how they are scored. The correct pattern: tactics-game
filters alternatives before calling `MAUTScorer.rank()`. Disabled tactics are simply absent from the
`alternatives` dict.

The library should not model eligibility constraints. Eligibility filtering is the caller's
responsibility. Adding it here would be the clearest example of the utility/framework line being
crossed.

**What the library should do**: Nothing for DoctrineProfile itself. The documentation should
explicitly note that pre-scoring eligibility filtering is the caller's responsibility and give a
one-line example. This manages the expectation without adding code.

**Risk level**: Zero — the correct answer is no code.

---

### Gap 3: agent-eval — Tiered Scoring (floor + ceiling) and scenario_compare

**The situation**: agent-eval uses a crawl/walk/run tier system where each tier has a floor score
(minimum acceptable) and ceiling score (aspirational). An alternative that meets the floor but not
the ceiling for a tier gets partial credit. This is a bounded scoring pattern within a tier, then a
tier-selection decision across tiers.

**Can scenario_compare handle this?**

Partially. `scenario_compare()` handles the "which tier's weights should I use?" question — it runs
the same alternatives under each tier's weight profile. But it does not handle the floor/ceiling
pattern within a tier. The floor is effectively a hard constraint (below floor = disqualified); the
ceiling is the aspirational bound for the value function normalization.

**Proposed composition pattern**:

The correct approach is not a new scorer method — it is a composition pattern that the library
documents:

1. Use `step()` value function with the floor as threshold, `below=0.0` — disqualifies alternatives
   below floor
2. Use `linear()` value function with `low=floor, high=ceiling` — scores within the tier range
3. The combination is expressed in the YAML model: two criteria can represent floor-check and
   within-tier score separately, or a single `piecewise_linear()` can encode both

The `piecewise_linear()` value function already supports this: a single breakpoint at the floor with
`y=0`, a breakpoint at the ceiling with `y=1`. The library has the capability; agent-eval needs
documentation of the pattern.

**What the library should do**: Add a worked example to the YAML schema documentation showing the
tiered scoring composition. No new code.

**Risk level**: Zero — documentation only.

---

### Gap 4: Missing weights.py — MAUTScorer Integration Bridge

**The situation**: `weights.py` produces a DataFrame. `MAUTScorer` consumes a `list[Criterion]`
where each criterion has a `float` weight. These two live in different submodules. A practitioner
who wants SMARTER weights feeding a scorer must manually extract the weight column from the DataFrame
and map it to criterion names.

**Current gap**: There is no bridge function. Every downstream repo that wants to use SMARTER
weights with MAUTScorer must write their own translation.

**Proposed addition**: A factory function `MAUTScorer.from_weights_dataframe(df, criteria_spec)`
or a standalone function `weights_to_criteria(df, method, criteria_spec)` where `criteria_spec`
provides the value function for each criterion. This converts `weights.generate_weights()` output
directly into a list of `Criterion` objects ready for `MAUTScorer`.

This is the most concrete integration gap: it completes the architecture diagram from the CONOP
where `weights.py` feeds `scorer.py`. Right now that connection is described but not implemented.

**Risk level**: Low. ~20 lines. New API surface in `scorer.py` (or a new `bridge.py` module).

**Recommendation**: High priority. This is the most impactful missing piece for downstream adoption.

---

## Question 4: What Should We NOT Add

This section is as important as the additions. Scope discipline is what separates a utility from a
framework.

### Do NOT add: Alternative ranking methods (TOPSIS, VIKOR, ELECTRE)

The CONOP already excluded these. Reinforcing: the value of this library is not breadth of ranking
methods. It is the combination of SMARTER weighting + value functions + config-driven models.
TOPSIS has no value function layer and assumes interval-scale raw scores. Adding it would require
a different data model. Use pymcdm if you need TOPSIS.

### Do NOT add: Preference elicitation UI or interactive questioning

Wave 4 (agent-assisted elicitation) has a gate: two downstream repos must request it explicitly.
That gate exists for good reason. Elicitation is a research-active area. No amount of clever
structuring will make it simple to do correctly. Do not pre-invest in an elicitation framework.

### Do NOT add: Fuzzy MAUT or uncertainty propagation over raw scores

Fuzzy MAUT (interval-valued utilities) doubles the complexity of every component. The sensitivity
analysis in Wave 2 already handles parametric uncertainty in weights, which is the dominant source
of uncertainty in practice. Raw score uncertainty (e.g., "effectiveness is somewhere between 70 and
90") is a valid extension but belongs in a separate module if it ever lands, not in the scorer.

### Do NOT add: Persistence or database integration

Several downstream repos (elephant-graveyard, database.py) have persistence concerns. The decision
science module should return Python objects. Serialization, storage, and retrieval are the caller's
responsibility. The library should remain stateless and side-effect-free.

### Do NOT add: Domain-specific criterion definitions

The CONOP correctly identified that "domain-specific criterion definitions" belong in downstream
repos. This means: no pre-built "effectiveness", "cost", or "risk" criterion templates. Every
downstream repo defines its own criteria. The library provides the infrastructure, not the
vocabulary.

### The line between utility and framework

A utility: gives you a function and gets out of your way.
A framework: owns the control flow and calls your code.

This library is a utility. The caller builds the scorer, calls rank(), and decides what to do with
the result. The moment this library starts managing lifecycle (scoring sessions, decision logs,
comparison history) it becomes a framework. That line is at: anything that requires the library to
hold state across multiple calls to `rank()`.

---

## Ranked Proposals by Impact

Ranked by impact-to-effort ratio for the next implementation session:

| Rank | Proposal | Impact | Effort | Type |
|------|----------|--------|--------|------|
| 1 | weights.py bridge (`weights_to_criteria()`) | High | Low | Code |
| 2 | `RobustnessReport` scalar from monte_carlo | High | Low | Code |
| 3 | `explain()` structured dict output | High | Medium | Code |
| 4 | `allow_missing` in `score()` (quest-engine) | Medium | Medium | Code |
| 5 | Bias A: utility range warning in `rank()` | Medium | Low | Code |
| 6 | Bias B: `direction: minimize` in YAML schema | Low | Low | Code |
| 7 | Rank reversal check (B1) | Medium | Low | Code |
| 8 | Dominance analysis | Medium | Low | Code |
| 9 | Bias C/D: docstring-only documentation fixes | Low | Very Low | Docs |
| 10 | agent-eval tiered scoring example | Low | Very Low | Docs |

---

## Approaches Considered for the Top Proposals

### Approach A: Add all four code proposals as Wave 4

Bundle the weights bridge, robustness scalar, explain output, and allow_missing as a Wave 4 that
completes the library.

Pros: Clean wave structure. All shipped together.
Cons: The weights bridge and robustness scalar are genuinely trivial — holding them for a wave bundle
delays value for no reason.

### Approach B (recommended): Ship the easy wins immediately, stage the rest

Ship the weights bridge and RobustnessReport in the same session (each is ~20 lines). Plan explain()
and allow_missing as a small Wave 4 — they require API design before implementation.

Pros: Fastest path to value. Respects the "simplest thing that works" principle.
Cons: Two separate sessions instead of one. Acceptable cost.

### Approach C: Skip all additions except documentation

Accept that Waves 1–3 are complete for the library's stated goal. The gaps identified are real but
not blocking — downstream repos can work around them.

Pros: Maximum simplicity. Zero scope creep.
Cons: Leaves the most impactful gap (weights bridge) unfilled despite trivial implementation cost.
Leaves practitioners writing robustness scalar extraction code in every repo independently.

**Recommendation**: Approach B. The weights bridge and RobustnessReport are the two changes
with the highest impact-to-effort ratio in the codebase. Everything else can be evaluated after
those two land.

---

## Open Questions

1. **weights_to_criteria location**: Should the bridge live in `scorer.py` as a classmethod
   (`MAUTScorer.from_smarter_weights()`), as a standalone function in a new `bridge.py`, or as a
   function in `weights.py`? The correct answer depends on which direction the dependency should
   run. `scorer.py` importing `weights.py` creates a circular dependency risk if `weights.py` ever
   needs `DecisionResult`. A standalone `bridge.py` or a factory on `MAUTScorer` is safer.

2. **RobustnessReport placement**: Should `robustness_score()` live in `sensitivity.py` (where
   `monte_carlo()` lives) or be a method on `MAUTScorer`? Functionally it belongs in
   `sensitivity.py` — it is a derived sensitivity metric.

3. **explain() dict schema**: What is the right level of detail? At minimum: winner, margin over
   runner-up, per-criterion contribution vs. theoretical maximum. The decision before implementation
   is whether to include raw scores in the output (requires passing them through the scorer, which
   currently does not retain them) or only utility-space values (which are already in `breakdown`).

4. **Docstring updates vs. new wave**: The documentation-only proposals (Bias C/D, framing
   convention, criteria independence warning) could be done as a standalone commit without a full
   wave structure. Should they be bundled into Wave 4 or done immediately as a documentation pass?

5. **allow_missing gate condition**: Before implementing `allow_missing`, validate that quest-engine
   actually needs it by reading their current implementation. The migration analysis assumed they
   do, but the CONOP was written before reading their code. Confirm before building.
