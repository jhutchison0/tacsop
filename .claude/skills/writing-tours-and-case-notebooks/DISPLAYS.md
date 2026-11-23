# Displays in a Notebook

A notebook is a tool for telling a reader something, and its displays do the telling. They answer three questions: what does the data look like at this level, how far apart are these two answers, and how sure is this number? Every figure follows the designing-clear-data-displays skill. This file says when to draw, what to draw, where the code lives, and how words, numbers and pictures sit together.

Through 0.3.0 this file talked builders out of figures. A figure cost a new package function and its tests, a gate of twenty numbers was applied to the summary and not to the data behind it, and thirteen repos built notebooks that drew nothing. One of them simulated 20,000 nights and printed two means. From 0.4.0 the default is reversed for one kind of claim, below.

## Draw a Shape

Before the display skill's question (could a table carry these numbers?), ask what the sentence claims.

| The claim is about | It is a shape | Draw |
|---|---|---|
| A share of a group, or which group a rate is taken over | A proportion | A unit chart |
| How outcomes spread, or what a mean hides | A distribution | Counts by group |
| Where an answer changes as inputs move | A boundary | A region map, or lines over an input |
| How a value moves as one input moves | A trajectory | A line, word-sized if the sentence can hold it |
| Who moves, who replies, and what is refused | A structure | The product's own diagram: a tree, a table with its best replies |
| Two or three numbers set side by side | Not a shape | A table. Points on one scale if the gaps are the point |

**Count the data behind the claim, not the summary.** Twenty thousand draws reduced to a mean and an interval are twenty thousand numbers. Eighty-one solved cases reduced to three counts are eighty-one. The line of about twenty numbers (VDQI p. 56) applies to what was computed, and a claim about a shape is drawn whatever the count.

A figure never stands alone. Print the table beside it, to the precision the asserts use, so the second reader can check every mark.

## Where a Figure Lives

A notebook imports no charting library, and `test_notebooks.py` fails one that does. A figure is a function in the package, with its own tests, and the notebook calls it. Three reasons:

- Every notebook, report and page in the repo draws the figure the same way.
- The figure's rules (labels placed, one scale, a note) are held by tests that fail, as the notebook's cells are.
- A reader's own data gets the same figure by passing it to the same function.

**A figure costs a call.** A repo that carries notebooks carries a display kit: one module of general displays, each tested once, that any notebook calls with its own numbers. A new kind of display still costs a function and its tests; a new figure of an existing kind costs one call and one assert. The first kit was built in `schelling-point` on 2026-11-22 (`viz/displays.py`, 104 tests); the hub's `passage_chart` and `slope_chart` are two more of the same kind.

| Display | Answers | Its tests hold |
|---|---|---|
| Unit chart | Of whom? One mark per unit, a row per group, a bracket over the groups a rate divides by | One mark per unit, no two in one place, each group and bracket named with its count |
| Points on a scale | How far apart? Named points on one line that is the whole range | Each point at its value, both ends of the scale named, no label over another, ties included |
| Counts by group | What does the mean hide? A row of needles per group, one outcome scale, one count scale | A needle per outcome as tall as its count; each row states its draws, mean and 95% interval; no interval where nothing varies |
| Region map | Where does the answer change? Each solved case at its own inputs, boundaries drawn from the formula, the fixture ringed | One mark per case at its true place, ticks only where cases were solved, each region named once among its marks |
| Lines over an input | How does a result move? A line per result named at its end, a rule at each crossing, the fixture ringed on every line | Each line through its points, ticks at the data's ends, the crossings and the fixture |
| Word-sized line | The same, inside a sentence | One vertex per value, heights in proportion, the size of a word, the colour of the text |
| The product's own diagram | What does the product say? For a game: its table with best replies underlined, its tree with the path of play | The marks come from the solver the product calls, so the figure cannot disagree with it |

A display takes the product's object where it can and derives the rest. A tree that asks the caller for the path of play can be handed the wrong one; a tree that calls the solver cannot.

## A Look at Every Level

Kernel rule 2 asks for the data at three levels. Each level owes the reader one look, as a display.

| Level | Also called | The look it owes | Avoid |
|---|---|---|---|
| **Arrives** | raw | The raw record printed whole, in its own format. Where the raw data is many draws or cases, every one of them, counted or placed, before any mean | A summary of an input the reader has not seen |
| **Handled** | staged | The same record before and after each step, on one scale. For a step applied to many items, small multiples: one panel per step or per group | A flow diagram of boxes and arrows with no data in it |
| **Reported** | production | The product's own page, table or figure, drawn by the function the product calls, in every form the product ships | A chart made for the notebook that the product never ships |

The passage through all three is worth one figure when the levels share a scale. The hub's `passage_chart` is the example: one panel per criterion with the raw measurement across and the utility up, every panel on the utility scale, and a last panel for the total. Where the levels share no scale, print them as three tables in one cell, each under a one-line label.

## By Comparison

A case sets two answers side by side. Rule 6 of the display skill asks "compared to what?", and a case answers it by construction.

| The comparison | Display |
|---|---|
| Two rules, one number each | A two-row table, each row labelled with its rule. Points on one scale when a third value (a hope, a worst case) belongs beside them |
| Two rules, a group each divides by | A unit chart with the repo's denominator bracketed |
| Two rules, several items, order matters | A slopegraph per rule, panels side by side on one scale, each item labelled at both ends |
| Two rules, one report | The report drawn twice by the product's own function, the naive one first |
| What one side hopes for against what the other side does | The product's diagram with the hoped-for outcome marked in words beside the outcome played |
| One rule, a parameter moving | Lines over the input, or small multiples on one scale |
| A value across magnitudes | A table. Six rows of a value collapsing need no axis |

Every case prints its fixture record first, then both answers as two labelled rows of one table. A one-line `naive: [] | repo: [...]` is not a display.

**One scale across the two rules.** Draw the naive answer and the repo's on the same scale even when one fills a small part of it. The scale is the whole range the value could take, named at both ends: ten people at a station, 0 to 1 for a chance. The white space is the comparison (display rule 5).

**Quiet what the reader is not following.** Draw it in grey, labelled. Use the smallest difference that still separates (display rule 3).

## Showing Doubt

For the confidence section (`CONFIDENCE.md`), and for any number a case reports. The section's one cell carries one doubt to the report; its display shows **how far the fixture sits from the place where the answer changes**. That distance is the finding, and a paragraph that states it as a number has left the picture out.

| The doubt | Display |
|---|---|
| One input uncertain across a range | Lines over the input, a rule at the value where the answer changes, the fixture ringed. A table beside it with the changing row marked |
| Two inputs uncertain | A region map: every solved case at its own inputs, the boundaries drawn from the formula and not from the marks, the fixture ringed |
| One draw against the spread of many (a seed, a sample) | Counts by group: every draw, counted. A table of outcome against count beside it |
| A mean from a simulation | The draws behind it, by the condition that splits them, each row with its draws, mean and interval. Then the mean |
| A judgment sampled many times | A table of how often each item took each place. A heatmap only past about twenty cells |
| An order among several items | Each item's range of places, from every pair compared. Never adjacent pairs alone |
| Two near-tied results | Print them as tied. "2 or 3: River Bend, Rail Yard" is a display |
| A range around a value | The range as a line and the value as a point on it, on the report's own scale, labelled at both ends. A rate of 0 or 1 has no normal interval: use the rule of three and say so |
| A direction the method leans | A line of the report's value against the input's size, with the direction stated in words |
| Two sources in conflict | Both values, side by side, each with its source. Never their mean alone |

A map or a line over an assumed grid is `measured over an assumed range`, and its note says so. Place each case at its true input values: a grid of uneven steps drawn as even steps misstates every distance on it. Where the boundary has a formula, draw the formula and plot the cases over it; the two agreeing is a check, and an assert makes it one.

Named failures, each an instance of display rule 5 (the effect at its true size):

- **False precision.** Digits past what the inputs bear. Print as many places as survive the doubt the section ran.
- **An order among ties.** A ranked list imposes one. "Each is within two standard errors of the next" does not mean "no settled order": adjacent ties chain.
- **An error bar that names nothing.** A bar is a range, a standard error, or a spread of draws; the note says which, over how many draws, and what the number is conditional on.
- **A confidence word with no number.** "Likely", "fairly sure", "usually". Hedge with numbers or not at all.
- **A mean of sources that disagree.** The disagreement was the data.
- **A bias shown as a spread.** A value that moves one way as its input shrinks has a direction, and a range hides it.
- **A yardstick scored another way.** A range used for scale is computed by the same procedure as the number set beside it.
- **A mean with its draws left out.** A simulated mean beside an exact value shows the two agree. It does not show that single outcomes lie far from both.
- **An interval too thin to see, drawn anyway.** Where the interval is narrower than the mark, say so in the note and give it in the table.

## Words and Pictures Together

Galileo's report of Saturn, written in 1612, set a small drawing of the planet inside the sentence that described it, and his publisher kept word and image together in print. Tufte reproduces the page (Seeing with Fresh Eyes, p. 59) and makes the integration of words, numbers and images a principle of analytical design (Beautiful Evidence). A notebook's cell boundary works against this: prose in one cell, code in the next, output under that. Four habits close the gap.

- **A figure cell follows its sentence and holds little else.** Keep the asserts that pin a case in the case's cell; give the figure a short cell of its own with the one or two asserts that say what the figure holds.
- **The title is the finding, built from the values.** `title=f"Of the {failing} who fail the check, {things} are Things"` cannot drift from the cell. A title typed as a string is a sentence no assert reaches (kernel rule 6).
- **Set a word-sized graphic in the sentence.** A cell's last line can be a computed sentence with a small line in it: "falls from 1.0 ⟍ to 0.2, which is the prior". The sentence gives the numbers at the line's ends, so the line needs no axis. Print the same sentence as plain text for a reader without a front end.
- **No decoration.** No emoji, no icon, no picture that carries no datum. A word-sized graphic is data at the size of a word.

Shorten the prose a figure replaces. A paragraph that walks through numbers the figure now shows is said twice.

## Colour

Grey is the default: ink for the data, grey for what the reader is not following. Colour is an added layer of meaning, used when it says something grey cannot. Tufte's first rule for it is to do no harm (Envisioning Information, "Color and Information").

- **A colour names one thing.** It goes to a name drawn on the figure (a plan, a group, an action), and that name wears it in every figure of the notebook. The kit refuses a colour for a name that is not drawn.
- **Prefer a colour that imitates the thing.** Flame for a plan that burns, water for a beach, blood for a killing. A reader decodes nothing: the colour is the thing's own. The kit carries a few such colours by name.
- **At most two colours in a notebook**, on a field of ink and grey. A third meaning takes a label, not a hue.
- **Never colour alone.** Every coloured mark keeps its label, and the figure still reads printed in black and white: a kit colour is darker than the mid grey beside it. This also serves a reader who cannot tell red from green.
- **No colour for emphasis, rank or mood.** Not red for the naive rule and green for the repo's. Weight and position carry emphasis; a colour here means a thing in the story.
- **No colour key.** A colour explained in a legend is an encoded key (display rule 2).

## Reference Images

A notebook about a scene, a site or a device may be easier to write with a reference image at hand. Keep such images in `notebooks/img/`, ignored by git. Three rules keep them out of the repo and the notebook whole:

- A cell that reads an image runs without it. The suite and a fresh clone have no such file.
- No saved output, as for every notebook: a displayed image is embedded in the `.ipynb`, and a committed output would publish it.
- An image the repo may not redistribute is never drawn by a cell. Cite it in words.

## For Two Readers

Rule 8 of the kernel, applied to a display. A reader new to the repo should get the section's point from its heading and the display. A reader who doubts it should find everything needed to check it one layer down.

| Layer | Carries |
|---|---|
| The section heading and the figure's title | The finding as a sentence, not the name of the case or the chart |
| The marks and their labels | The data, with each item named where it sits |
| The note under the figure | Units, the scale, the source, what a mark is, and that the fixture is invented |
| The table printed beside it | Every number in the figure, to the precision the asserts use |
| The asserts | The claim the title makes, as a check that can fail |

A figure whose numbers appear nowhere as text fails the second reader. Print the table.

## Before a Figure Is Kept

- Render it and look at it, in a real kernel as well as from a script: a front end crops and scales a figure its own way. A figure's tests hold its structure; they cannot see a label lying across a curve, or two fills too close to tell apart.
- Run the display skill's `REVIEWING.md` protocol on it, as for any figure.
- Test that no label overlaps another, with the renderer's own text extents, ties included. Move a crowded label; do not shrink the type (display rule 4).
- Assert in the notebook cell that the figure has what the text says it has: the count of panels, or of marks in each group.
- Check that every item has its own form. Two regions marked O and Q are one region to the eye.

## What Is Not Settled

- **Saved outputs.** A notebook is committed without outputs, so a reader on a code host sees no figure and no table until the notebook is run. Whether a notebook whose fixtures are all invented may commit its outputs, or a rendered copy beside it, is the maintainer's decision and is not made.
- **The kit's home.** It was built in one repo. Its general displays are not yet in the hub's package, and a second repo has not used it.
- **Second readers.** The kit and its first notebook were reviewed by their author and the maintainer's eye. The two hub displays were reviewed by their author alone.
- **A handled level with more than two steps** has not yet been shown as anything but text.
- **How a word-sized graphic renders** outside a notebook front end (a code host, a PDF export) is untested.
