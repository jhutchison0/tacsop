# Decision Audit: How the Notebook Doctrine Shows Doubt

**Author**: decision-scientist
**Date**: 2026-11-22
**Type**: Decision audit (statistical honesty of `.claude/skills/writing-tours-and-case-notebooks/DISPLAYS.md` at 0.4.0 and `CONFIDENCE.md`, read against `.claude/skills/designing-clear-data-displays/RULES.md` rule 5)

**Verdict: SOUND IN STRUCTURE, WRONG IN ONE PRESCRIPTION, SILENT ON TWO KINDS.** The doctrine's central idea holds up: show how far the fixture sits from the place where the answer changes, draw the draws and not only their mean, and say that a grid is assumed. One prescription is wrong as written. `DISPLAYS.md` tells every row of draws to state "its draws, mean and 95% interval", which puts an unnamed interval of the mean beside a picture of single outcomes (C1). The normal interval's limits are stated too narrowly in both files (W1). Two of the five kinds of doubt, `not known` and `exact`, have no display (W2), and nothing separates chance in the draws from doubt in an invented input (W3).

**Scope.** This file covers the hub's two documents. The first display kit and its first notebook live in a private repository, and their findings, with every number computed from that repository's model, are in a second file held outside this repo for its owner to place. Findings below cite that file as "the kit audit" with its finding number and reproduce none of its numbers. Where a number appears here it comes from a synthetic case stated in full.

## What was checked

| Check | Result |
|---|---|
| Each kind in `CONFIDENCE.md` lines 27 to 33 against the rows of `DISPLAYS.md` lines 82 to 93 | `measured`: 5 rows. `measured over an assumed range`: 2 rows. `estimated`: 1 row. `not known`: none. `exact`: none |
| Each display in the kit table, `DISPLAYS.md` lines 36 to 42, against the doubt rows | No kit display draws a range around a value, though line 91 prescribes one |
| Coverage of the mean plus and minus 1.96 standard errors, outcome 10 with chance 0.98 and 9 with chance 0.02, 40,000 samples per size | 20 draws: 33.5%. 50 draws: 63.9%. 200 draws: 90.7%. 1,000 draws: 94.8% |
| Chance that the same sample holds one value only | 20 draws: 66.8% (0.98 to the 20th). 50 draws: 36.4% |
| The same as a rate of 0.02, Wilson interval | 20 draws: 94.0%. 50 draws: 92.2%. 200 draws: 93.3% |
| Coverage on a skewed four-valued outcome (6, 7, 8, 9 with chances 0.03, 0.14, 0.31, 0.51) | 5 draws: 82.8% with 1.96, 94.8% with Student's t. 10 draws: 91.0% and 92.2%. 50 draws: 94.2% and 94.5% |
| Width of the 95% interval of a mean against the range holding 95% of outcomes, normal case | Narrower by the square root of the draws: 71 times at 5,000 draws |

Evidence: inline scripts with numpy, seeds 7 and 11, run this session; no file written. The 66.8% and 36.4% are also exact arithmetic.

## Critical

### C1. The doctrine prescribes an interval of the mean beside a picture of outcomes, and does not name it

**Location**: `DISPLAYS.md` line 38 ("each row states its draws, mean and 95% interval") and line 87 ("each row with its draws, mean and interval"). `CONFIDENCE.md` line 79 ("Give an interval").

**The issue.** A simulated number carries three different doubts:

1. **Where one outcome falls.** The spread of the draws. More draws do not shrink it.
2. **How well the draws know their own mean.** The interval of the mean. More draws shrink it toward nothing.
3. **Whether the inputs are right.** No number of draws touches it.

Line 38 asks for the second and sets it beside a drawing of the first, under the bare word "interval". The display exists, by its own row in the table, to answer "What does the mean hide?" The answer is the spread of single outcomes. The number printed beside it is narrower than that spread by the square root of the draw count: 71 times at 5,000 draws. A reader who takes the printed interval for the spread sees the effect at one seventy-first of its size. By rule 5's own measure that is a lie factor of 0.014, and nothing on the figure is false.

**Why it matters.** This misreading is documented. Readers shown an interval of a mean underestimate how far single outcomes vary and overstate the effect, compared with readers shown the range of outcomes (Hofman, Goldstein and Hullman 2020). Trained researchers confuse standard-error bars, intervals of a mean and spreads (Belia, Fidler, Williams and Cumming 2005; Hoekstra, Morey, Rouder and Wagenmakers 2014). The doctrine already knows the neighbouring fault: line 101 names "an error bar that names nothing". It then prescribes one in text form. A downstream rule of the form "every stochastic figure shows its 95% confidence interval" is met to the letter by the interval that misleads (kit audit K-C2).

**Fix.** Each row states both, each named: the range that holds 95% of the row's draws, and the mean with the 95% interval of the mean. Exact wording is in "Proposed wording", items D1, D2, D4 and F1.

## Warning

### W1. The normal interval fails long before a rate reaches 0 or 1, and agreeing draws read as certainty

**Location**: `CONFIDENCE.md` line 79 and `DISPLAYS.md` line 91 ("A rate of 0 or 1 has no normal interval"); `DISPLAYS.md` line 38 ("no interval where nothing varies").

**The issue.** The sentence is true and draws the line in the wrong place. With a true rate of 0.02 the normal interval covers the truth in 33.5% of samples of 20 and 63.9% of samples of 50, and the sample rate is not 0 in the ones that miss. The interval can also end outside the range the quantity can take: below 0 for a count, above the group's size for a head count (kit audit K-C1 has two printed cases). At 5 draws of a skewed outcome, 1.96 standard errors covers 82.8% where Student's t covers 94.8%.

"No interval where nothing varies" has the opposite fault. In 66.8% of samples of 20 from that same source every draw is one value, and the row then says so with no bound. Twenty agreeing draws leave room for a rate up to 3 in 20 of something else. The doctrine prescribes the rule of three (line 91) for a rate and does not carry it to this row. A display cannot tell "exact by the structure" from "not seen in n draws"; only the author can, with an assert.

**Fix.** A rate takes a Wilson interval at every count (Wilson 1927; Brown, Cai and DasGupta 2001 recommend it over the normal interval at all sample sizes). A mean takes no normal interval under about 30 draws or where an end would pass the scale. Agreeing draws carry 3/n unless the structure makes them exact. Wording: C1w, C4w, D6, D7.

### W2. Two of the five kinds have no display, and one has a display the kit cannot draw

**Location**: `DISPLAYS.md` lines 82 to 93 against `CONFIDENCE.md` lines 27 to 33.

| Kind | Rows in "Showing Doubt" that serve it | Verdict |
|---|---|---|
| measured | Counts by group; a mean from a simulation; a judgment sampled; an order; near-ties | Served, subject to C1 |
| measured over an assumed range | Lines over the input; a region map | Served, subject to W4 |
| estimated | "A range around a value" (line 91) | A row with no kit function behind it. No display in lines 36 to 42 draws a range |
| not known | None | No display |
| exact | None | No display |

**How to draw `not known`.** The decision-analysis answer is to assign no distribution and treat the input as a parameter: put it on an axis across its whole possible range and show the value at which the answer changes, so the reader asks which side they believe (Morgan and Henrion 1990 call this a switchover value; Manski 2013 argues for reporting a bound in place of a point and calls the point "incredible certitude"; Spiegelhalter and Riesch 2011 set acknowledged ignorance apart from anything a distribution can carry). The doctrine's region map and line over an input already are that display. What is missing is the rule that a `not known` input gets no point and no interval anywhere, and that a fixture's value for it is drawn as an open mark labelled "invented". Tufte's contribution is the Challenger chart in *Visual Explanations*: draw the full range the decision concerns, so the stretch with no data shows as empty space on the scale, and never let the axis stop where the data stops. In a table, the row stays and reads `not known` with what would settle it; a dropped row reads as no doubt and a blank cell reads as zero.

**How to draw `exact`.** A solid mark or a rule with the word "exact" and no interval. Beside draws, the exact value is the rule and the draws are the marks, so the reader sees the simulation checked against the answer and not the other way round.

**Fix.** Three table rows, D3.

### W3. Nothing separates chance in the draws from doubt in an invented input

**Location**: `DISPLAYS.md` lines 86 to 87 and 101; `CONFIDENCE.md` lines 73 to 85 and 93 to 95.

**The issue.** The risk literature keeps two things apart: variability that more data would not reduce, and uncertainty about a quantity that has one true value (Morgan and Henrion 1990; Paté-Cornell 1996; Der Kiureghian and Ditlevsen 2009). A notebook on an invented fixture has both at once, and the second is usually far larger. `CONFIDENCE.md` line 78 asks what a number is "conditional on", which is the right question. No rule says the answer goes on the figure, and no rule says the interval from the draws is silent about the inputs. An interval to two decimal places beside a mean that rests on six invented numbers reads as the size of the doubt. In the kit's first notebook a small move in one invented input shifts the mean by more than the printed half-width (kit audit K-W2).

**How to draw the difference.** Chance is drawn as a distribution: the draws, counted. Doubt in an input is drawn by redrawing the display at other values of the input: small multiples, or a line over the input. The two are never folded into one interval. Where a split variable's weights rest on an invented input and the shape inside each group does not, the note says which part would survive a different input.

**Fix.** One paragraph in `DISPLAYS.md` (D4) and one bullet in `CONFIDENCE.md` (C2w).

### W4. "Its note says so" asks too little of a figure over an assumed grid, and the margin has no rule

**Location**: `DISPLAYS.md` line 80 ("how far the fixture sits from the place where the answer changes. That distance is the finding") and line 95; `CONFIDENCE.md` lines 30 and 43.

**The issue.** Four gaps, each seen in the first map built to this rule (kit audit K-W3, K-W6):

- **The note said less than line 95 requires and nothing caught it.** "Says so" has no test and no list.
- **Inputs held fixed went unnamed.** A map moves two inputs. The model had more, and one of those held fixed moved the answer's lead more than either drawn input.
- **The margin was given along one axis.** The flip along the other axis lay just past the grid's last column. A margin in a derived quantity was not carried back to the inputs that arrive.
- **A count of cells was reported as the size.** Regridding the same model changed the leading region's share of cells from a majority to a minority and back. `CONFIDENCE.md` line 43 says a percent over a grid names its denominator; it does not say the count measures the grid.

A fifth is rule 5's own. Where two axes share a unit, as two chances do, and are drawn at different scales, a distance across and a distance up cannot be compared by eye. The first map's lie factor between its axes was outside the band (kit audit K-W3).

A margin is a breakeven distance: how wrong an input must be, the rest held, before the answer changes. It is not a confidence and carries no chance. Where the input is `not known`, nothing in the notebook says how likely the flip is, and the doctrine should say that plainly so "margin" is not read as "how sure".

**Fix.** D5, D8 and C3w, C5w.

### W5. A point at an expected value is a comparison by mean

**Location**: `DISPLAYS.md` line 18 ("Points on one scale if the gaps are the point"), line 37, line 64.

**The issue.** Points on a scale show gaps at true size, which is right for exact values. When each point is an expectation, the gap between two means is set against nothing. One plan may be certain and another range across most of the scale; a plan with the higher mean may have the worse bad night. Decision analysis compares such plans by their whole distributions: the risk profile, and dominance where one cumulative curve lies at or below the other throughout (Hadar and Russell 1969; Hanoch and Levy 1969; Clemen and Reilly's textbook treatment). Line 106 names the fault for one mean ("A mean with its draws left out"). No rule covers several means side by side (kit audit K-W4).

**Fix.** D9 and a new display, "cumulative curves", below.

### W6. A line over an input has three open ends

**Location**: `DISPLAYS.md` lines 40, 74 and 84.

- **The y scale.** Line 74 requires the whole range a value could take, for a comparison of two rules. Lines 40 and 84 do not repeat it, and the kit's function scales to the data (kit audit K-W5). A rise from 0.50 to 0.52 then fills the frame.
- **The crossing.** Line 44 says a display "derives the rest". A crossing passed in by the caller can be wrong in the way a path of play passed to a tree can.
- **The solved values.** A map marks every solved case. A line marks none, so five cases and five hundred look alike, and a straight segment between two solved values is a claim.

**What its note must say.** That the author moved the input, over what range and at how many values; every other input and its fixed value; that the ring is the fixture's value and is invented; whether each rule comes from a formula or from the lines; and that the lines between solved values are straight.

**Fix.** D10.

## Note

### N1. The unit chart is the textbook device; the rule must say "expected"

Natural frequencies improve reasoning with Bayes' rule across many studies (Gigerenzer and Hoffrage 1995; Hoffrage and Gigerenzer 1998; a meta-analysis by McDowell and Jacobs 2017), and arrays of marks add to the effect for readers with low numeracy (Galesic, Garcia-Retamero and Gigerenzer 2009). The form the risk-communication literature settled on is the expected frequency: "of 100 people like these, we expect 20" (Spiegelhalter, Pearson and Short 2011). The effect depends on counts that nest, one inside the next, which the bracket draws. `DISPLAYS.md` line 36 says none of what the display owes: that the counts are expectations and not a sample, that a real group of that size would differ by chance, that the group size is chosen to make every count whole, and that a count is never rounded to make a mark. Wording: D11.

### N2. Displays the doctrine lacks

| Display | Would it serve a notebook? | What its tests hold | General or specific |
|---|---|---|---|
| **One-way bars (a tornado diagram)**: one bar per input, from the result at the input's low end to its high end, widest first (Howard 1988; Eschenbach 1992) | Yes, wherever a model has more than two doubtful inputs. It is how an author learns which two belong on the map. The kit audit's K-W6 found the input with the widest swing was not on the map | One bar per input; each bar spans the least and greatest result over the range, found at interior values and not only the two ends; bars in order of width; a rule at the fixture's result on every bar; a mark where the answer changes; each end labelled with the input's value | General to any function of several inputs. The flip mark is specific to a decision |
| **A table of flip values**: per input, the fixture's value, the value at which the answer changes, and "none between a and b" where it never does | Yes. It is line 80's finding in the form line 18 prefers: a few numbers are a table | The two plans' results are equal at each stated flip, within a tolerance; a "none" is asserted at both ends and at interior values; every row names what was held fixed | General to any decision with a threshold |
| **Cumulative curves (risk profiles)**: per plan, the chance of ending at or below each outcome, as steps on one scale | Yes, wherever plans are compared by a mean (W5) | Each curve is monotone and ends at 1; a step's height is that outcome's chance; "dominates" is asserted as one curve at or below the other at every outcome; any crossing is reported with its outcome and its size, however small | The curves are general to any two distributions. The word "dominates" is specific to a decision |
| **Value of perfect information** (Raiffa and Schlaifer 1961; Howard 1966) | Sometimes, and as a sentence. It is one number, so line 18 gives it no figure. It needs a distribution over the unknown; on an invented prior it is `measured over an assumed range` and is said to be | Never negative; zero where one plan is best in every state; equal to a hand-worked value on a two-by-two case | Specific to decision models with probabilities |
| **A strategy-region diagram** | The region map is one | Held, subject to W4. For a third input, small multiples of the map | Specific to decisions; the map of a classifier's regions is the same drawing |
| **A range on a point** | Yes: line 91 prescribes it and no display draws it | The value lies inside its range; a zero-width range draws no line; the note says what the range is | General |

### N3. Rule 5 has no clause for doubt

`RULES.md` rule 5 measures the size of an effect shown against its size in the data. Every named failure in `DISPLAYS.md` lines 97 to 107 is called an instance of it. The rule's test, "measure both effects and divide", has an exact form for doubt: the width of the doubt as drawn or printed, over its width in the data. C1's 0.014 is that ratio. One sentence in "Showing Doubt" would give reviewers the test (D7, first item).

### N4. The sources here were not fetched

Every citation in this file is from the auditor's memory and was checked against no source this session. `RULES.md` marks each of its quotations primary or secondary. Before any citation below enters a skill file, fetch it and mark it the same way. The list, for whoever does that: Belia, Fidler, Williams and Cumming, "Researchers misunderstand confidence intervals and standard error bars", *Psychological Methods*, 2005. Brown, Cai and DasGupta, "Interval estimation for a binomial proportion", *Statistical Science*, 2001. Clemen and Reilly, *Making Hard Decisions*. Der Kiureghian and Ditlevsen, "Aleatory or epistemic? Does it matter?", *Structural Safety*, 2009. Eschenbach, "Spiderplots versus tornado diagrams for sensitivity analysis", *Interfaces*, 1992. Galesic, Garcia-Retamero and Gigerenzer, "Using icon arrays to communicate medical risks", *Health Psychology*, 2009. Gigerenzer and Hoffrage, "How to improve Bayesian reasoning without instruction: frequency formats", *Psychological Review*, 1995. Hadar and Russell, "Rules for ordering uncertain prospects", *American Economic Review*, 1969. Hanley and Lippman-Hand, "If nothing goes wrong, is everything all right?", *JAMA*, 1983 (the rule of three). Hanoch and Levy, "The efficiency analysis of choices involving risk", *Review of Economic Studies*, 1969. Hoekstra, Morey, Rouder and Wagenmakers, "Robust misinterpretation of confidence intervals", *Psychonomic Bulletin and Review*, 2014. Hoffrage and Gigerenzer, "Using natural frequencies to improve diagnostic inferences", *Academic Medicine*, 1998. Hofman, Goldstein and Hullman, "How visualizing inferential uncertainty can mislead readers about treatment effects in scientific results", CHI 2020. Howard, "Information value theory", *IEEE Transactions on Systems Science and Cybernetics*, 1966. Howard, "Decision analysis: practice and promise", *Management Science*, 1988. Manski, *Public Policy in an Uncertain World*, 2013. McDowell and Jacobs, "Meta-analysis of the effect of natural frequencies on Bayesian reasoning", *Psychological Bulletin*, 2017. Morgan and Henrion, *Uncertainty*, 1990. Paté-Cornell, "Uncertainties in risk analysis: six levels of treatment", *Reliability Engineering and System Safety*, 1996. Raiffa and Schlaifer, *Applied Statistical Decision Theory*, 1961. Spiegelhalter, Pearson and Short, "Visualizing uncertainty about the future", *Science*, 2011. Spiegelhalter and Riesch, "Don't know, can't know", *Philosophical Transactions of the Royal Society A*, 2011. Tufte, *Visual Explanations*, 1997, the Challenger chapter. Wilson, "Probable inference, the law of succession, and statistical inference", *JASA*, 1927.

## Proposed wording

Each item gives the file, the line at 0.4.0, and the exact text. "Replace" quotes the text to remove.

### DISPLAYS.md

**D1. Line 38, the kit table's row for counts by group, last column.** Replace "each row states its draws, mean and 95% interval; no interval where nothing varies" with:

> each row states its draws, the range that holds 95% of them, and the mean with the 95% interval of the mean, each named for what it is; no interval ends off the scale; a row of agreeing draws claims nothing past its count

**D2. Line 87, the row "A mean from a simulation".** Replace the second column with:

> The draws behind it, by the condition that splits them. Each row states its draws, the range that holds 95% of them, and its mean with the 95% interval of the mean. A last row holds all the draws together. Where an exact value exists, the title states it and the draws are its check

**D3. After line 93, three rows for the table.**

> | An input nobody knows (`not known`) | No point and no interval. Put the input on an axis across its whole possible range and mark the value where the answer changes. The fixture's value is an open mark labelled "invented". In a table, keep the row: it reads `not known` and names what would settle it |
> | A value with no doubt (`exact`) | A solid mark or a rule, the word "exact" in its label, and no interval. Beside draws, the exact value is the rule and the draws are the marks |
> | Several plans, each a mean over chance | Each plan's range of single outcomes as a line through its point, or each plan's cumulative curve on one scale. Say where the curves cross, or that they do not |

**D4. A new paragraph after the table, before line 95.**

> **Three doubts, three marks.** A simulated number carries three doubts, and a display names each one. The spread of single outcomes is drawn as the draws and stated as the range that holds 95% of them; more draws do not shrink it. The simulation's error in its own mean is the 95% interval of the mean; more draws shrink it toward nothing. Doubt in an input the author chose is neither, and no number of draws touches it: show it by drawing the display again at other values of the input, as small multiples or as a line over the input. Never fold the third into an interval. The note names every input the draws hold fixed.

**D5. Line 95, first sentence.** Replace "A map or a line over an assumed grid is `measured over an assumed range`, and its note says so." with:

> A map or a line over an assumed grid is `measured over an assumed range`, and its note says four things: that the author chose the grid, the range of each axis, every input held fixed with its value, and that the ring marks an invented value. A count of cells measures the grid as much as the model. Give the boundary's value as the size, and keep the count as a check on the figure.

**D6. Line 91, last sentence.** Replace "A rate of 0 or 1 has no normal interval: use the rule of three and say so" with:

> A rate takes a Wilson interval at every count, since the normal interval fails near 0 and 1 as well as at them. At 0 of n the bound is 3/n, the rule of three, and the note says so. A mean takes a normal interval only from about 30 draws and only where both ends stay on the scale

**D7. Lines 97 to 107, four named failures to add, and one sentence before the list.** After "each an instance of display rule 5 (the effect at its true size)" add:

> The test is rule 5's own: the width of the doubt as drawn or printed, divided by its width in the data.

> - **An interval of the mean read as the spread.** At 5,000 draws the interval of the mean is 71 times narrower than the range that holds 95% of the outcomes. Print both and name each.
> - **An interval off the scale.** An interval that ends below 0 for a count, or above the group's size, is the wrong interval. Use one that respects the bound, or give the count and no interval.
> - **Agreeing draws read as certainty.** Twenty draws that all give one value leave room for a rate up to 3 in 20 of another. Write `exact` only where the structure gives it, and assert the reason.
> - **An interval on an invented input's result, and nothing else.** The interval measures the draws. Beside it, say how far the result moves when the invented input moves by an amount a reader might believe.

**D8. After line 80, in the opening paragraph of "Showing Doubt".** Add:

> Give the distance in every doubtful input, in the units the input arrives in, and name what was held fixed. A margin along one axis at an invented value of the other is one cut through the map. Where two axes share a unit, draw them at one scale, so a distance reads the same across and up (display rule 5). A margin says how wrong an input must be before the answer changes. It does not say how likely that is, and where the input is `not known`, nothing in the notebook does.

**D9. Line 18, last column.** Replace "A table. Points on one scale if the gaps are the point" with:

> A table. Points on one scale if the gaps are the point. Where a point is a mean over chance, the note says so and each point carries the range of single outcomes behind it

**D10. Line 40, the kit table's row for lines over an input.** Replace both columns after the name with:

> | How does a result move? A line per result named at its end, on the whole range the result could take, a mark at each solved value, a rule at each crossing, the fixture ringed on every line | Each line through its points, the y scale as given and not the data's own, one mark per solved value, each crossing computed from the lines or asserted against them, ticks at the data's ends, the crossings and the fixture |

**D11. Line 36, the kit table's row for the unit chart, or a sentence under the table.** Add:

> A unit chart of expected counts says "expected" in its title, and its note says the group is a reference class and not a sample: a real group of that size would differ by chance. Choose the smallest group that makes every count whole. Never round a count to make a mark.

**D12. Line 147, the note's row in "For Two Readers".** Replace "Units, the scale, the source, what a mark is, and that the fixture is invented" with:

> Units, the scale, the source, what a mark is, the kind of each number (exact, from how many draws, or over a range the author chose), every input held fixed, and that the fixture is invented

**D13. Lines 161 to 167, "What Is Not Settled".** Add:

> - **Displays not yet built.** A range on a point, one-way bars over several inputs, a table of flip values, and cumulative curves for plans compared by a mean. Each is prescribed or implied above and no kit holds it.

### CONFIDENCE.md

**C1w. Line 79.** Replace "Give an interval, not "plus or minus" one standard error. A rate of 0 or 1 has no normal interval." with:

> Give an interval, not "plus or minus" one standard error, and name what it is an interval of. An interval of a mean says how well the draws know the mean. It says nothing about where one outcome falls: give the range that holds 95% of the draws for that. A normal interval needs about 30 draws and both ends on the scale. A rate takes a Wilson interval; at 0 of n the bound is 3/n.

**C2w. A new bullet in "Statistics Over Draws", after line 78.**

> - **Draws do not touch an invented input.** Every draw holds the fixture's inputs fixed. Name them beside the interval, and show how far the statistic moves when the most doubtful one moves by an amount a reader might believe. Where that move is wider than the interval, the interval is not the size of the doubt, and the row says so.

**C3w. Line 30, the "Carries" column of `measured over an assumed range`.** After "two invented endpoints included." add:

> Every input held fixed is named with its value. A count of cells measures the grid: the size is the value at the boundary.

**C4w. Line 33, the "Carries" column of `exact`.** Add:

> Draws that all agree are not `exact`: n agreeing draws bound the rate of anything else at 3/n.

**C5w. Line 32, the "Carries" column of `not known`.** Add:

> In a figure it gets no point and no interval. Where it is an input, the row gives the value at which the answer changes, so a reader can say which side they believe.

**C6w. Line 64, "What a result belongs to", after the first two sentences.** Add:

> Give the margin in each doubtful input, in the units the input arrives in. A margin in a derived quantity (a posterior, a score) is carried back to the inputs that produce it.

### One sentence for downstream repos

**F1.** A repo whose rule reads "every figure of a stochastic result shows its 95% confidence interval" is pushed toward C1. Offer this wording in the skill's adoption notes:

> Every figure of a stochastic result states its replication count, the range that holds 95% of single outcomes, and the 95% interval of any mean it reports, each named for what it is.

## What I did not do

I ran no test suite and changed no file but this one. I fetched no source (N4). I did not review layout, labels or colour; `REVIEWING.md` in the display skill covers those. I did not audit the hub's own `passage_chart` and `slope_chart`, which show no stochastic result.
