# The Confidence Section

Kernel rule 9. A notebook that prints a number to three places has told the reader it is good to three places. Most repos have no one whose job is to say otherwise, so the notebook does it: one section, after the cases and limits and before the own-data cell.

This is the newest part of the skill and the part reviews changed most. In the rollout every confidence section needed rework after review, and two had a headline finding that was false while every assert passed. Read "What Reviews Found" before writing one.

## The Heading

`## Confidence`, or `## How sure` in a repo that reserves the word "confidence" for something of its own; the test module accepts both. Either way the section's first line says what it is about: how far the notebook's numbers can be trusted, on invented data, and nothing about any real output.

## The Table

At least one row per level, never blank. A level with two doubts of different kinds gets two rows. The rows are **different doubts**: one doubt shown at three levels is one row and two repeats.

| Level | The doubt to look for |
|---|---|
| **Arrives** | Provenance and source: who measured it, when, with what, and how old it is. Conflict: two sources that disagree. What is missing, and whether missing reads as zero or as current. For a library: what the package refuses, and what it cannot hold (a source, a unit, a range, a NaN) |
| **Handled** | Procedure: a choice the code makes that another competent person would make differently. Bias: a direction the method leans. Representation: what the stored form cannot hold (a range, a tie, a unit, a second run) |
| **Reported** | What the report's form claims beyond the data: digits, an order among near-ties, a single answer where several survive, a rate from one or two runs. In every form the product ships |

Each row states the doubt, its **kind**, its **size**, and **what the repo does about it**.

## The Kinds

These are the house's terms for a line of the common operating picture, applied to a notebook. A kind attaches to a claim, so one row may hold a measured gap and a not-known cause.

| Kind | Means | Carries |
|---|---|---|
| **measured** | The doubt has been run and counted | The number and the cell that gives it. Nothing assumed: a step function's jump at the fixture's own value is measured |
| **measured over an assumed range** | The cell counted over values it chose | The range, marked as an assumption in a comment. Any size computed from invented values is this kind, two invented endpoints included. The row also owes the size on real data, or `not known` |
| **estimated** | A range someone judged, or a statistic under a model | The range, its basis, and what would prove it wrong. A standard error is estimated, and the cell tests it |
| **not known** | Nobody has looked, or nobody can | What would settle it, as a collector someone could run. It needs no range. A standing gap is also a `## Limit` |
| **exact** | There is no doubt at this level | Exact in what, to what tolerance. "Deterministic over a closed input" is a reason |

Eight traps, each sprung in the rollout:

- **`exact` on a formula.** `exact` means no doubt at this level. A row whose doubt is "this number is not what its name says" is `not known` or `estimated`, however exact its arithmetic. A comparison of floats with no tolerance is not exact: it is a measured doubt.
- **`not known` without a search.** Before writing it, search the repo's code, docstrings, schema, tests and docs for the quantity. A `not known` the repo already answers is a false row. One section called a conflict's wrong side not known; the repo's own docstring named it and gave the cause.
- **`measured` against an invented record.** A gap between a calculation and a number the fixture's author typed measures the calculation's path, never the outside source.
- **A search that could find nothing.** An absence found by a search needs a positive control: assert the pattern matches a string that plainly holds the word, then assert the files do not.
- **An exact reference built from a float.** `Fraction(2.2)` is exact about a float, not about 2.2. Build it from integers or from the text typed, and put one value that is not a binary fraction in any assumed grid. A percent over a grid names its denominator: where only some inputs can go wrong, give the share among those.
- **A defect in the table.** A validation gap found while asking what the package refuses is a known defect with a task; the row points to it.
- **Silence about a measurement on record.** Open the section with a search of the repo's records for spread, replicates or noise. One repo had measured the very thing a section left out, a month earlier.
- **A figure from the record.** A number from the repo's history that the notebook cannot re-run is cited with its file, says what it counted and whether that is the quantity the cell varies, and is labelled "from the record, not re-run here".

"What the repo does about it" lists everything the product already prints about doubt: a sensitivity table, a caveat line, a footnote. Where the repo does nothing, "nothing" is a first-class answer. Where a level adds no doubt of its own, the row says "carried from the row above".

## The Cell

After the table, one cell takes one doubt and carries it to the report: vary the doubtful input across its range, or swap the disputed source or procedure, and print what the report does. Assert what survives the doubt and what does not. A counting cell comes first where the table states numbers, to pin each one.

Run it at the shipped settings, through the product's own ordering and the call the product makes. Name each setting changed and each fixture value built to make the result happen. Reversing a list can reach an order the product never produces.

**Which doubt.** The one that could change a decision the report feeds; name the decision. A doubt that moves a third decimal place and nothing else is a row, not the cell. Search the repo's reviews for the quantity before choosing: one cell followed the mild form of a doubt (one row, one frame late) whose severe form (a whole frame flipped) a review had already named.

- If the largest doubt cannot flip anything because the repo ignores the input, that is a defect to report and a row in the table. Run a different doubt.
- At a threshold, "does the verdict change within the tolerance" is always yes. Ask against the requirement the threshold protects.
- Run the same doubt in both directions, and say which direction of error costs more wherever the product advises or decides for a person. Where that is the owner's call, say so. A second doubt that leans the other way is a different row, not the other direction.
- **A structural unknown has a bound from the structure, and no sweep.** Where a value cannot be known until the product runs (a computed link, a runtime target), do not sweep invented values and count: state the bound the structure gives, such as "anywhere from 0 to N". A bound printed about a reader's data is tested on a fixture built to break it. One cell printed a lower bound that a story's own text refuted.
- **Say which way it fails when unsure**, in asserted lines: with no number it refuses, or it acts. In a product that decides, this is the finding.

**What a result belongs to.** A fixture on a decision boundary shows the largest sensitivity there is. Run the doubt on two fixtures, one on the boundary and one off it, or say where the fixture sits. Separate two things one phrase tends to merge:

| | Often | Example |
|---|---|---|
| What the doubt does if it happens | exact, by enumeration | A wrong tap in the window undoes a step-down in 4 of 6 changes |
| How often it happens | measured in the record, or not known | 4 ghost logs of 12 in one recorded week |

Where a threshold is computed from the fixture, say what it equals at this size: with eleven items a 90th percentile is the second-highest value. Say which results belong to the fixture's size and which to the method.

## Statistics Over Draws

Where the doubt is a seed, a sample or a rerun:

- Give the number of draws, the statistic, and what makes the draws independent. Overlapping windows of one text are not independent: say they overlap, and call their range a floor.
- Say what the number is **conditional on**: the policy, the fixture, who plays the other side.
- Give an interval, not "plus or minus" one standard error. A rate of 0 or 1 has no normal interval.
- State the threshold and **how many comparisons share it**.
- **An order among several items needs every pair.** "Each is within two standard errors of the next" does not mean "no settled order": adjacent ties chain. Print each item's range of places and assert the ranges.
- **Check the claim on a second, disjoint block of draws**, in the cell. An assert that holds on seeds 0 to 29 and in two of ten other blocks passed by luck, and negation cannot see that. If a claim needs more draws than the suite can afford, the cell claims less.
- A small count offered as support says what it could tell apart: the rate before, the count after, and the chance of that count with no change.
- A range used for scale is computed the same way as the number set beside it.
- A bias has a direction. A value that moves one way as its input shrinks is shown against the input's size, not as a spread.

## What a Reader May Conclude

The section closes by saying what a reader may and may not take from it. Where the product's output is uncalibrated, that sentence is required: what the score supports, and what it does not. Nothing in the section may read as assurance that a real output is correct, complete or safe.

Tie it to the own-data cell: the doubt run on a fixture is the one the own-data cell runs on the reader's data, as a bound or a count. Where the cell cannot build that from what the reader supplies, it says so.

## On Invented Fixtures

A fixture carries no real provenance, so the mechanism is what is shown: how far a doubt of that size travels. A fixture set is better for holding one record with a doubt in it: a conflicting pair, a missing value, a stale date, a second filing. Where a fixture was tuned until it showed an effect, say so and say how often the effect holds across draws.

## What Reviews Found

Each line is a fault a reviewer found in a built confidence section, with every assert passing.

| The section said | The review found |
|---|---|
| Two sources disagree about moonrise by 384 minutes | The gap was the host's offset from UTC; under `TZ=UTC` it was 24 minutes and the test failed |
| First and second place survive; seven below are in no settled order | The two claims held in 2 of 10 other blocks of draws; 13 of the 21 pairs among the seven were apart |
| 4 of 6 one-tap changes move the suggestion | That was the one fixture on the rule's boundary; others gave 1 of 12 and 1 of 10 |
| Shorter windows spread the distance | It was a bias with a direction, and the doubt that flips a result was left in the table |
| Handled: `exact`, with a formula | The formula's meaning was the doubt |
| No other fund moved | Asserted on an input; an untouched fund lost its level |
| The winner holds across seeds | In 179 of 200, on a scripted policy the section did not name |
| `exact`: a second run replaces the first | Pinned over an input the product never builds; the product's own path pools the runs |
| 13 of 24 single-run changes move the leader | The fixture sat at the smallest margin; of the eight smallest changes none flips it. The repo's own record of replicate spread went uncited |
| The orphan count lies between 2 and 3 | The true lower bound was 0; the link's target was not known, and an unknown cannot bound a count |

What went right is as instructive. One section found that a solver's answer exists at a payoff of 2.0 and not at 2.0 plus 1e-15. One found that nothing reads an observation's age, so a thirty-day-old reading prints as current. One found an amended filing the store keeps and no report reads. Each came from asking, at one level, what the repo does when the data is doubtful, and finding the answer was nothing.
