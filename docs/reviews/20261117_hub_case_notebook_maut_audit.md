# Decision Audit: the Case Notebook as MAUT Teaching

**Author**: decision-scientist
**Date**: 2026-11-17
**Type**: Decision audit (domain correctness of `notebooks/cases_how_a_ranking_goes_wrong.ipynb`, with `src/myproject/decision_science/` behind it)

**Verdict: MERGE AS A DRAFT AFTER TWO FIXES.** The decision model is valid and the four cases teach true things about additive MAUT. Two statements about uncertainty are not ones a decision scientist would accept. Both sit in the Limit and are repeated in the confidence table. The Limit says the Monte Carlo draws weights "near the stated ones"; it draws them from almost the whole simplex. The Limit asserts that the site first most often is not the stated leader; that holds on seed 7 and on 93 of 200 seeds. Both are fixed by changing text and one assert, with no change to `src/`. Three warnings follow; W1 and W2 are one sentence each.

Code and sources were reviewed elsewhere. This audit covers what the notebook tells a reader about MAUT and about doubt.

## What was run

All probes ran in a local clone of the repo at `100dfb3` under a scratch directory, with the hub's `.venv` interpreter. Nothing in the working tree was written except this report. The clone was removed afterwards.

| Check | Result |
|---|---|
| Weights in `tests/fixtures/tour/depot_model.yaml` | 0.30, 0.30, 0.20, 0.20: sum 1.00, none negative, all in config |
| Value functions | Four monotone curves, each in the direction its comment states; `score` refuses a utility outside 0 to 1 |
| Baseline ranking | Airport Road 0.763, River Bend 0.696, Rail Yard 0.692, Old Mill 0.640 |
| `monte_carlo(..., n_samples=2000, seed=s)` for s = 7 and 100 to 119 | River Bend first most often on seed 7 and on 5 of the 20 others |
| The same sampler, seeds 0 to 199, 2,000 draws each | River Bend first most often on 93 of 200 |
| The same sampler, 1,000,000 draws | Airport Road first in 39.02%, River Bend in 39.09%, Rail Yard in 21.89%, Old Mill in 0 |
| Dirichlet draws on seed 7, distance from the stated weights | 2.5% of draws within 0.10 on all four weights; 54.5% hold a weight under 0.05 |
| Each weight swept from 0 to 1, the others rescaled in proportion | Leader changes at flood 0.134, cost 0.132 and 0.409, storage 0.404, drive 0.579 |
| `one_at_a_time` at delta 0.02, 0.05, 0.10 | Leader unchanged in 8 of 8, 8 of 8, 7 of 8 |
| River Bend's flood-free years swept 10 to 30 | Airport Road leads to 23; River Bend leads from 24 |
| All four sites' flood-free years moved 3 either way together (capped at 30) | Airport Road leads in 1,372 of 1,372 combinations |
| Signed contribution of each criterion to each pair's gap, three sites | Table under W2 |
| Textbook exponential against the package and an `expm1` form, 20 rates | Table under S2 |

## Is each statement true of additive MAUT, or of this fixture?

| Section | What it says | General or fixture | Verdict |
|---|---|---|---|
| Case 1 | A weighted sum of raw measurements is not a utility; the largest unit dominates | General | Correct. See S1 for the sentence that would make it complete |
| Case 2 | Scaling to the alternatives present lets a dominated option change the leader; scaling by the model does not | General for "can change"; the flip itself is this fixture's, on a naive margin of 0.005 | Correct. "Rank reversal" is the right name. See W3 |
| Case 3 | The exponential's limit at a zero rate is the straight line; the textbook form loses its digits first and divides by zero later | General: floating point, no fixture involved | Correct. See S2 |
| Case 4 | A criterion separates alternatives by at most its weight times the range of utility it gives them | General, and exact | Correct as a bound. The closing sentence misstates what a weight is. See W2 |
| Limit | The package cannot check a weight | General | Correct. What the cell shows about these weights is not. See C1, C2 |
| Confidence | Leader holds across River Bend's flood record; second and third swap | Fixture, over a range the cell chose | The run is right. The closing sentence drops the range. See W1 |

## Critical

### C1. The Monte Carlo does not draw weights "near the stated ones"

**Location**: cell 17 ("draws 2,000 weight sets near the stated ones ... Here it does not hold"), cell 19 row "Handled" ("estimated, by `monte_carlo` over 2,000 weight sets near the stated ones"). The claim comes from `sensitivity.py:154-155` and its docstring ("clusters near the original weights"). The tour repeats it.

**Issue**: `monte_carlo` uses `alpha = weights * n_criteria`. The total concentration is then the number of criteria, which is the concentration of the uniform distribution on the simplex. With equal weights the sampler is exactly uniform. Here alpha is (1.2, 1.2, 0.8, 0.8): the draws are centred on the stated weights and spread across nearly all of them. A stated weight of 0.20 has a standard deviation of 0.18. On seed 7 the flood weight runs from 0.008 to 0.547 between its 5th and 95th percentiles, 54.5% of draws put some criterion under 0.05, and 2.5% of draws sit within 0.10 of the stated weights on all four.

**Why it matters**: the Limit reads the result as "the judgment matters, since the leader does not hold near the stated weights". The run supports a different sentence: the leader does not hold when the weights are unknown. Near the stated weights it holds. Airport Road keeps the lead while the flood weight stays above 0.134 (stated 0.20) and the cost weight stays between 0.132 and 0.409 (stated 0.30). No single weight moved by 0.05 changes the leader. With a Dirichlet whose flood weight has a standard deviation of 0.04, Airport Road is first in 94% of draws; at 0.09, in 69%; at the package's 0.18, in 39%. The verdict "not robust" is a statement about the sampler's width, and the notebook does not give the width. This is true of every model the package scores.

**Suggested fix, notebook, today**: say what is drawn and how wide. For cell 17: "`monte_carlo` draws 2,000 weight sets centred on the stated ones and spread over most of the simplex: a stated weight of 0.20 has a standard deviation of 0.18. It asks what the ranking is worth if the weights are close to unknown." Give the break-even weights beside it, since they are the form of this result an owner can act on: "Airport Road leads while flooding carries more than 0.13 of the weight and cost less than 0.41." Then "What would settle it" is no longer "no further computation will": the computation has turned an open question into "is flooding worth at least 0.13?", which owners can answer. In cell 19, change the kind to "measured over an assumed distribution", and give the count and the condition: 764 of 2,000 (38%, interval 36% to 40%), under a sampler of that width.

**Suggested fix, package, a task**: give `monte_carlo` a concentration parameter, state the default's spread in the docstring, and correct "clusters near".

Evidence: scratch clone; `rng.dirichlet([1.2, 1.2, 0.8, 0.8], 2000)` on seed 7 → share within 0.10 on every weight 0.0245; share with a weight under 0.05 0.545; flood weight quantiles 0.008, 0.148, 0.547. Weight sweeps in steps of 0.001 → leader changes listed in the table above. Dirichlet at concentration 100, 20 and 4, 4,000 draws → Airport Road first in 0.942, 0.692, 0.378.

### C2. "The site first most often is not the site first on the stated weights" passes on seed 7 by luck

**Location**: cell 18, `assert report.winner == "River Bend" != leader`.

**Issue**: over 1,000,000 draws from the same sampler, Airport Road is first in 39.02% and River Bend in 39.09%. At 2,000 draws the standard error of their difference is 2.0 points, so which of the two comes out ahead is a coin flip. River Bend is ahead on seed 7 (797 draws against 764), on 5 of seeds 100 to 119, and on 93 of seeds 0 to 199. The house rule for a statistic over draws asks for a second, disjoint block and a claim that holds in both. This claim does not.

**Why it matters**: the sentence tells a reader that the weights' doubt overturns the leader. It ties the leader with one other site. The assert also fails on the day numpy changes its Dirichlet stream, for a reason that has nothing to do with the model.

**Suggested fix**: claim what every block shows. "Airport Road and River Bend each come first in about 39% of draws, too close to order at 2,000; Rail Yard in about 22%; Old Mill in none." Assert that both shares lie between 0.35 and 0.43, that `report.is_robust` is false, and that Old Mill's share is 0.0; run a second seed in the cell and assert the same there. Drop the comparison of `report.winner` with the leader.

Evidence: scratch clone; `monte_carlo(scorer, sites, n_samples=2000, seed=7)` → first-place counts Airport Road 764, River Bend 797, Rail Yard 439, Old Mill 0. Seeds 0 to 199 → River Bend ahead on 93; Airport Road's share between 0.354 and 0.414.

## Warnings

### W1. "Who leads does not depend on River Bend's flood record" holds for three years either way and fails at five

**Location**: cell 21, first sentence; cell 20, `assert set(leader_at.values()) == {"Airport Road"}`.

**Issue**: the cell varies the count from 16 to 22 and the leader holds. At 24 River Bend leads, 0.781 against 0.763. The range is the cell's assumption, and the closing sentence leaves it out. The table gives the range no basis. One exists: if each year floods independently at the rate the record shows, a count of 19 in 30 has a standard deviation of 2.6 years, so 16 to 22 covers 82% of such records and 4% reach 24.

**Why it matters**: the sentence as written is a claim about any error in the record. A reader who doubts the record by more than three years is told the wrong thing.

**Suggested fix**: "Within three years either way, who leads does not depend on River Bend's flood record; five more flood-free years would give River Bend the lead." Extend the sweep to 24 and assert the change. The cell can also claim more than it does on a second axis: with all four sites' counts moved three years either way together, Airport Road leads in all 1,372 combinations.

Evidence: scratch clone; `scorer.rank` with River Bend's `flood_free_years` at 23 and 24 → leader Airport Road, then River Bend (0.7809). Binomial(30, 19/30): P(16 to 22) = 0.816, P(24 or more) = 0.040.

### W2. Case 4's closing sentence reads a weight as general importance, and "share" is a bound, not a verdict

**Location**: cell 16, "the weights describe what the owners care about in general"; cell 15, the column "share of what separates them".

**Issue 1**: in additive MAUT a weight is not general importance. It is the value of moving that criterion from the bottom of its stated scale to the top: 0.30 is what the swing from 90 minutes to 10 is worth against the other three swings. Case 2 exists to say the scale is part of the model. Case 4's last sentence then describes the weights as if they had no scale. Swing weights are the right frame for this case, and the cell already computes them. The three sites use 0.101 of the drive-time swing, so the criterion can spend 0.030 of its 0.300. The "share" column is the weight vector a modeller would elicit for these three sites' own ranges: rescale each utility to the three sites' range, apply the share column as weights, and the package's order comes back (0.635, 0.501, 0.493) with every gap in proportion. Apply the stated weights to the same rescaled utilities and Rail Yard leads, which is case 2's naive rule again. That is the link between the two cases, and the notebook does not draw it.

**Issue 2**: the bound is exact and general. It does not follow that a criterion with a narrow range decides nothing, and the notebook should not let a reader leave with that. Influence on a comparison is pairwise and signed. Drive time carries 6% of the range-share and still decides second place:

| Pair | Gap | Cost | Drive | Pallets | Flood |
|---|---|---|---|---|---|
| Airport Road over River Bend | +0.067 | -0.110 | -0.030 | +0.032 | +0.175 |
| Airport Road over Rail Yard | +0.071 | +0.110 | -0.024 | -0.042 | +0.027 |
| River Bend over Rail Yard | +0.004 | +0.220 | +0.006 | -0.074 | -0.148 |

River Bend's margin over Rail Yard is 0.0041 and drive time supplies 0.0060 of it. Without the criterion the warning calls largely unspent, Rail Yard is second. In both of the leader's pairs drive time counts against the leader.

**Why it matters**: "weight is importance" is the most common error in applied MAUT, and it is the error that makes case 2's naive rule look reasonable. A reader who takes "narrow range means no influence" will drop a criterion that settles a close call.

**Suggested fix**: replace the closing sentence with "the weight prices the whole swing from 90 minutes to 10, and these three sites use a tenth of it." Add one sentence: "A small spread can still settle a close pair: drive time supplies 0.006 of River Bend's 0.004 lead over Rail Yard." Add an assert for it.

Evidence: scratch clone; per-pair `weight * (u_a - u_b)` from `DecisionResult.raw_utilities` → the table above. Local rescaling with share weights → Airport Road 0.635, River Bend 0.501, Rail Yard 0.493; with stated weights → Rail Yard 0.610, River Bend 0.600, Airport Road 0.437.

### W3. Case 2 names the literature and cites none of it

**Location**: cell 8, Source: "The decision literature calls the naive result rank reversal; this notebook cites no paper for it."

**Issue**: the statement is correct. A change in the order of two alternatives when a third is added or removed is rank reversal, and normalising to the alternatives present is its usual cause in a weighted sum. The source is marked `Design:` and a test holds the rule, so the case stands without a paper. The sentence itself is held by no assert and no reference, and kernel rule 6 says such a sentence is cut or cited. Saying that nothing is cited is honest; it is not a citation.

**Is the gap acceptable?** For a draft, yes. Before the skill leaves draft, cite or cut. The hub's notebook is the example other notebooks copy, and "the literature says, no paper given" is a pattern that should not travel.

**Suggested fix**: cite two references. These are given from memory and were not looked up; check each before it goes in.

- Belton, V. and Gear, T. (1983), "On a short-coming of Saaty's method of analytic hierarchies", *Omega* 11(3), 228 to 230. The paper that started the rank reversal debate, for a method that normalises to the alternatives present.
- Wang, Y.-M. and Luo, Y. (2009), "On rank reversal in decision analysis", *Mathematical and Computer Modelling* 49, 1221 to 1229. Shows the same effect in the simple weighted sum.

For W2's point that a weight belongs to a range: von Winterfeldt, D. and Edwards, W. (1986), *Decision Analysis and Behavioral Research*, on swing weights; Keeney, R. (2002), "Common mistakes in making value trade-offs", *Operations Research* 50(6), 935 to 945.

**Two additions to the case, both one sentence**: the closing cell says someone must state the scale before the data arrives. Add that the weights belong to that scale: change `low` and `high` and the weights must be asked for again. And say where the fixture sits: under the naive rule Rail Yard leads River Bend by 0.005 with four sites, so the flip is a near-tie's. The general claim, "can be changed", needs no such margin.

## Suggestions

### S1. Case 1: say that the naive total changes with the unit

The closing cell says pallets dominate because they run to the thousands. The general statement is one step further: the naive ranking depends on the units chosen. With cost in dollars in place of thousand dollars, the same rule moves Old Mill from third to second. A weighted sum of raw numbers is a valid value model only when each weight is an exchange rate per unit and value is linear in each measurement. A weight elicited as a share of 1 is not that.

Evidence: scratch clone; naive sum with `annual_cost` times 1,000 → Rail Yard, Old Mill, Airport Road, River Bend; as committed → Rail Yard, Airport Road, Old Mill, River Bend.

### S2. Case 3: the quiet failure is wider than the table shows, and `expm1` removes the threshold

The case is correct. Three notes.

| Rate | Textbook form | Package | True value |
|---|---|---|---|
| 1e-12 | 0.500055512 | 0.5 | 0.5 |
| 1e-15 | 0.555555556 | 0.5 | 0.5 |
| 3e-16 | 0.333333333 | 0.5 | 0.5 |
| 1.2e-16 | 1.000000000 | 0.5 | 0.5 |
| 1e-16 | 0.000000000 | 0.5 | 0.5 |
| 5.5e-17 | ZeroDivisionError | 0.5 | 0.5 |

- The textbook form returns 0.000 at 1e-16 and 1.000 at 1.2e-16, with no error. A row at 1e-16 would show the case more plainly than the row at 1e-15 does.
- The error starts at 5.5e-17 for a positive rate. The commit message the Source quotes says "about 2.2e-16". The quotation is accurate; the record's figure is four times too high.
- Above the threshold the package is the textbook form and keeps its cancellation: for rates from 1e-8 to 1e-4 the worst error against an `expm1` form is 9.7e-9, larger than the 1.25e-9 the straight line costs at the threshold. Neither moves a ranking. `math.expm1(-rate * t) / math.expm1(-rate)` needs no threshold and loses no digits.

"Never from a person typing one" is held by no assert. Write "rarely", or cut the sentence.

### S3. Case 4: half the narrow range is the curve's, and the warning ignores the weight

"All three sites are a short drive" credits the data alone. With a straight line over the same scale the three sites span 0.213 of utility and the warning does not fire; the curve's rate of 2.0 brings it to 0.101. The rate is a judgment, and the confidence table says nothing varies it. The warning's threshold of 0.2 is also blind to the weight: a criterion at weight 0.60 and range 0.19 separates by more than one at weight 0.10 and full range, and only the first is warned about. The cell's `can_separate` is the better measure.

### S4. Limit: the weights are not the only unchecked input

The Limit names the weights. The confidence table adds the curve shapes. Neither names the additive form, which holds only if preference on one criterion does not depend on the level of another. One sentence in the Limit would cover all three. For scale, on the shapes: across 21 variants of the flood curve (midpoint 20 to 26, steepness 0.3, 0.5, 1.0) Airport Road leads in 20, and second place goes to a different site in 6.

### S5. The flood curve never reaches 1

The logistic gives 30 flood-free years of 30 a utility of 0.953. The 0.20 weight on flooding can spend 0.19 at most. A `piecewise_linear` or a rescaled curve would let the weight mean what the other three mean: the value of the full swing.

## What is sound

- The model: weights sum to 1.00, none negative, all in YAML; four monotone curves; `score` validates weights and refuses a utility outside 0 to 1.
- Case 1's assert that one criterion at weight 0.20 supplies over two thirds of every naive total.
- Case 2's rule and its test: a site's utility depends on that site alone. Dominance is checked on utilities, and the dominated site never comes first in any draw, which is exact.
- Case 3's limit and both failure modes.
- Case 4's bound, and its advice to read the warning.
- The confidence cell's finding that second and third place swap across one year of record, and its assert that one input's doubt is over ten times the margin the ranking prints. "2 or 3: River Bend, Rail Yard" is the right report.
- The Limit's last assert: no weights make the dominated site win.

## Not done

- No test, cell or file in the repo was changed. `src/` and the tour were read, not audited line by line.
- The four references in W3 were not looked up.
- The own-data cell was read and not run on a second model.
