# Displays in a Notebook

A notebook's displays answer three questions: what does the data look like at this level, how far apart are these two answers, and how sure is this number? Every figure follows the designing-clear-data-displays skill. This file says which display suits which question, and where the figure's code lives.

## Where a Figure Lives

A notebook imports no charting library, and `test_notebooks.py` fails one that does. A figure is a function in the package, with its own tests, and the notebook calls it. Three reasons:

- Every notebook, report and page in the repo draws the figure the same way.
- The figure's rules (labels placed, one scale, a source line) are held by tests that fail, as the notebook's cells are.
- A reader's own data gets the same figure by passing it to the same function.

So a new figure costs a function and its tests. That cost is the check on rule 7 of the kernel: if a table carries the numbers, print the table. About twenty numbers is the line (VDQI p. 56).

In the rollout to thirteen repos no builder added a figure, and each proposed one in its report. Most packages draw nothing and have no drawing dependency, and a builder was not allowed to add one. Nearly every proposal ended "a table carries it today". A repo whose subject is visual is the likely exception.

## By Level

| Level | The display that suits it | Avoid |
|---|---|---|
| **Arrives** | The raw record printed whole, in its own format. A short table of the fixture's rows | A summary of the input. The reader has not seen the input yet |
| **Handled** | The same record before and after each step, side by side. For a transformation applied to many items, small multiples: one panel per step or per field, one scale | A flow diagram of boxes and arrows with no data in it |
| **Reported** | The product's own page, table or figure, drawn by the function the product calls, in every form the product ships | A chart made for the notebook that the product never ships |

The passage through all three is worth one figure when the levels share a scale. The hub's `passage_chart` is the example: one panel per criterion with the raw measurement across and the utility up, each alternative a labelled point on the criterion's curve, every panel on the utility scale, and a last panel for the total. A panel's width is its weight, so the weights need no key.

Where the levels share no scale, print them as three tables in one cell, each under a one-line label.

## By Comparison

A case sets two answers side by side. Rule 6 of the display skill asks "compared to what?", and a case answers it by construction.

| The comparison | Display |
|---|---|
| Two rules, one number each | A two-row table, each row labelled with its rule. A figure adds nothing |
| Two rules, several items, order matters | A slopegraph per rule, panels side by side on one scale, each item labelled with its value at both ends |
| Two rules, one report | The report drawn twice by the product's own function, the naive one first. Its source line says which rule fed it |
| One rule, a parameter moving | Small multiples on one scale, or a table with the changing row marked |
| A value across magnitudes | A table. Six rows of a value collapsing need no axis |

Every case prints its fixture record first, then both answers as two labelled rows of one table. A one-line `naive: [] | repo: [...]` is not a display.

The hub's `slope_chart` is the slopegraph: no axis, no grid, no legend, since the labels are the scale. An item present in one column is a point with no line.

**One scale across the two rules.** Draw the naive panel and the repo's panel on the same scale even when the naive numbers fill a small part of it. The white space is the comparison (display rule 5).

**Quiet the items the reader is not following.** Both hub displays take a `highlight` list; the rest are drawn in grey. Use the smallest difference that still separates them (display rule 3), and keep the quiet items labelled.

## Showing Doubt

For the confidence section (`CONFIDENCE.md`), and for any number a case reports.

| The doubt | Display |
|---|---|
| One input uncertain across a range | A table: the input down the side, the report's value across. Mark the row where the answer changes |
| One draw against the spread of many (a seed, a sample) | A table of outcome against count, with the one draw's row marked. A dot per draw on the outcome's own scale once the table passes about twenty rows |
| A judgment sampled many times | A table of how often each item took each place. A heatmap only past about twenty cells |
| An order among several items | Each item's range of places, from every pair compared. Never adjacent pairs alone |
| Two near-tied results | Print them as tied. "2 or 3: River Bend, Rail Yard" is a display |
| A range around a value | The range as a line and the value as a point on it, on the report's own scale, labelled at both ends. A rate of 0 or 1 has no normal interval: use the rule of three and say so |
| A direction the method leans | A table of the report's value against the input's size, with the direction stated in words |
| Two sources in conflict | Both values, side by side, each with its source. Never their mean alone |

Named failures, each an instance of display rule 5 (the effect at its true size):

- **False precision.** Digits past what the inputs bear. Print as many places as survive the doubt the section ran.
- **An order among ties.** A ranked list imposes one. "Each is within two standard errors of the next" does not mean "no settled order": adjacent ties chain.
- **An error bar that names nothing.** A bar is a range, a standard error, or a spread of draws; the note says which, over how many draws, and what the number is conditional on.
- **A confidence word with no number.** "Likely", "fairly sure", "usually". Hedge with numbers or not at all.
- **A mean of sources that disagree.** The disagreement was the data.
- **A bias shown as a spread.** A value that moves one way as its input shrinks has a direction, and a range hides it.
- **A yardstick scored another way.** A range used for scale is computed by the same procedure as the number set beside it.

## For Two Readers

Rule 8 of the kernel, applied to a display. A reader new to the repo should get the section's point from its heading and the display. A reader who doubts it should find everything needed to check it one layer down.

| Layer | Carries |
|---|---|
| The section heading and the figure's title | The finding as a sentence, not the name of the case or the chart |
| The marks and their labels | The data, with each item named where it sits |
| The note under the figure | Units, the scale, the source, and that the fixture is invented |
| The table printed beside it | Every number in the figure, to the precision the asserts use |
| The asserts | The claim the title makes, as a check that can fail |

A figure whose numbers appear nowhere as text fails the second reader. Print the table.

## Before a Figure Is Kept

- Render it and look at it. A figure's tests hold its structure; they cannot see a label lying across a curve.
- Run the display skill's `REVIEWING.md` protocol on it, as for any figure.
- Test that labels in one column do not overlap, with the renderer's own text extents. Move a crowded label; do not shrink the type (display rule 4).
- Assert in the notebook cell that the figure has what the text says it has: the count of panels, or of marks.

## What Is Not Settled

- The two hub displays were reviewed by their author alone.
- Whether a figure that only a notebook calls belongs in the package at all. Today it does, because rule 7 leaves it nowhere else, and the cost has meant no repo in the rollout gained one.
- No notebook has yet shown the handled level for a pipeline with more than two steps as anything but text.
