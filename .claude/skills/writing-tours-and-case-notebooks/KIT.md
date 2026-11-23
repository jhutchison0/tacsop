# Building a Display Kit

A repo that carries notebooks builds one module of displays, and this file is the recipe. [DISPLAYS.md](DISPLAYS.md) says which display answers which question; this says how to build each one so a notebook's figure costs a call.

The first kit was built in a sibling repo on 2026-11-22: one module of about 1,070 lines, one test file of 146 tests, eight notebooks calling it. This file describes that kit. The hub does not hold its code. A repo that can read the sibling copies the module and its tests and deletes the two displays that import the sibling's solvers; a repo that cannot builds from the contracts below.

## The Module

One file, `src/<package>/viz/displays.py`, and one test file, `tests/unit/test_displays.py`. The only charting dependency is matplotlib, with numpy for arithmetic.

- **Each display is a function that returns a `matplotlib.figure.Figure`.** It builds the figure with `plt.subplots` and returns it. It never calls `plt.show`. A notebook shows a figure by leaving it as the last line of a cell.
- **Data comes first; everything else is keyword-only.** `title` and `note` are required on every figure and have no default. The title is the finding, as a sentence. The note gives units, source, and what is invented.
- **A display refuses bad input with `ValueError`.** A value off the scale, a count that is not whole, a colour for a name that is not drawn: each raises, and each has a test.
- **Every drawn part can be found by a test.** Give each artist a gid (`series:<name>`, `crossing:<words>`, `range:<name>`) or put each group in its own collection with the group's name as its label. A test that cannot find a mark cannot hold it.

Three constants carry the field: `INK = "#222222"` for data and its labels, `QUIET = "#8a8a8a"` for notes, rules and marks the reader is not following, `PAPER = "#ffffff"`. Three more imitate what they mark: `FLAME = "#d9480f"`, `WATER = "#1c6ea4"`, `BLOOD = "#a61e2a"`. A repo names its own; the rule is in DISPLAYS.md, under Colour.

## Five Helpers

| Helper | Does |
|---|---|
| `_document(fig, title, note)` | Sets the title above the figure, left-aligned in ink, and the note below it in the quiet grey |
| `_fit(fig, panel_inches)` | Sizes the figure to its panel plus one title line and one note line, so no figure holds an empty band |
| `_bare(ax)` | Removes spines and ticks; the labels on the marks are the scale |
| `_refuse_stray_colours(colors, drawn)` | Returns the colours by name, and raises for a name that is not on the figure |
| `_fills(names, tint)` | Gives each coloured name its colour and shares a ramp of greys, ink to paper, among the uncoloured names only. Raises when a colour would print within 0.12 of a neighbouring grey in luma (0.299 R + 0.587 G + 0.114 B), so the figure still reads in black and white |

## The Displays

Signatures are abridged: every display also takes `title`, `note`, and `colors` (a colour by name, optional).

| Display | Call | Draws |
|---|---|---|
| Unit chart | `unit_chart(groups, *, brackets=None, per_row=20)` | One square per unit in rows of `per_row`, each group starting a new row and named at its left with its count. A bracket at the right names a set of adjacent groups and their total: the denominator a rate divides by |
| Points on a scale | `points_on_a_scale(values, *, scale, unit, hollow=(), fmt="{:.2f}", ranges=None)` | One line that is the whole `scale`, named at both ends. Each value is a point with its name and number on a row of its own, joined by a thin rule, so ties never crowd. `hollow` names draw open: assumed, not an outcome. `ranges` draws the spread of single outcomes behind a mean as a grey line in its own lane |
| Counts by group | `counts_by_group(draws, *, scale, unit)` | Small multiples, one row per group, every row on one outcome scale and one count scale. A needle per whole-number outcome, as tall as its count and labelled with it. Each row prints the summary below |
| Region map | `region_map(cells, *, boundaries, point, xlabel, ylabel, same_unit=False)` | `cells` maps `(x, y)` to the name of the answer there. One small mark per solved case at its own inputs, shaded by answer; each answer named once among its marks; each boundary a line computed some other way and named at its end; the fixture ringed. Ticks only where cases were solved |
| Lines over an input | `lines_over_an_input(xs, series, *, xlabel, ylabel, crossings=None, fixture=None, log=False, scale=None)` | A line per result, named at its right end with its last value, a mark at each solved value, a break where the value is `None`. A thin rule with its words at each crossing; the fixture ringed on every line. With `scale`, the vertical axis is the range the result could take and not the data's own |
| Word-sized line | `sparkline(values, *, at=None, mark=None)` | SVG markup one text line high, in the colour of the text (`currentColor`), heights in proportion, no axis and no label. `mark` puts a dot at one index |
| A sentence that holds it | `prose(sentence, **parts)` | Fills the braces in `sentence`. A graphic goes in as markup; anything else is escaped as text. The result has `_repr_html_`, so a notebook shows it as a paragraph, and `__str__` gives the sentence without graphics for a test |
| The product's own diagram | the repo's own | Takes the product's object and calls the product's solver for every mark, so the figure cannot disagree with the product. The first kit has two: a payoff table with best replies underlined and equilibria boxed, and a two-move tree with the path of play heaviest |

The sentence that sets a line inside itself is written this way in a notebook cell:

```python
prose(
    "As the share goes from {lo} to {hi}, the chance falls from {a} {line} to {b}.",
    lo=shares[0], hi=shares[-1], a=f"{chance[0]:.3f}", b=f"{chance[-1]:.3f}",
    line=sparkline(chance, at=shares, mark=shares.index(0.25)),
)
```

## The Summary a Row of Draws Prints

`counts_by_group` computes one summary per row from the draws, and the caller cannot override it. Two lines, each named for what it is:

1. The number of draws and the range that holds 95% of them (the 2.5th and 97.5th percentiles). More draws do not shrink this.
2. The mean and the 95% interval of the mean (1.96 standard errors). More draws do shrink this.

The interval is withheld under 30 draws, and where either end would leave the scale. Draws that all agree claim no interval; the row states the rate of any other outcome they could not have seen, by the rule of three (3 over the number of draws). The reasons are in [CONFIDENCE.md](CONFIDENCE.md).

## What the Tests Hold

Build each display test-first, one behaviour at a time. The first kit's tests hold these, and each line was once a fault in a render:

- **One mark per datum.** A unit chart of 100 holds 100 marks, no two in one place. A map holds one mark per solved case at its true inputs.
- **One scale, named.** Both ends of a scale carry their value; rows of small multiples share their limits.
- **No label over another, and none over a mark.** Draw the canvas (`fig.canvas.draw()`), take each text's `get_window_extent()`, and assert no two boxes overlap. Include ties and close values in the cases.
- **Each name is drawn once, where its data sit.** No legend.
- **A title and a note on every figure.**
- **Colour.** A colour for a name not drawn raises. A colour within 0.12 luma of a neighbouring grey raises. An uncoloured figure holds only ink, grey and paper.
- **The summary.** Its two lines are named apart; no interval under 30 draws or past the scale; agreeing draws state the rule of three.
- **No empty band.** The figure's height follows its rows.

The tests see structure. They cannot see whether a figure reads well. Render every figure and look at it before it is kept, by DISPLAYS.md, "Before a Figure Is Kept".

## The Notebook's Side

- A notebook imports the kit and no charting library. The suite's notebook test fails one that does, and names matplotlib among what running the notebooks needs.
- The figure's numbers print as a table in the same cell or the next, and an assert holds each number the title states.
- Notebooks commit without outputs. A reader runs the notebook to see its figures; the maintainer ruled so on 2026-11-23.
- To look at a notebook's figures without a front end, run it with nbclient and write the outputs outside the repo. Do not set `MPLBACKEND`: under Agg the inline figures never appear.

## Not Built

The first kit draws a crossing where the caller says, and does not compute it. Its region map still sets a region's name over marks when both inputs share one scale. The displays DISPLAYS.md lists under "What Is Not Settled" are not in it.
