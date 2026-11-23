# Review: Display Skill 1.1.0 and DISPLAYS.md 0.4.0, Second Reading

**Author**: code-reviewer
**Date**: 2026-11-22
**Type**: Doctrine review (skill text, cross-links, and the skill's own protocol run on rendered figures)

## Verdict

Tufte would approve of the eight rules and would object to what the skill leaves out. Version 1.1.0 keeps his sentence that sends small data to a table and declines the principle on the facing side of the argument, that a graphic should carry a large data set densely. That asymmetry is the gate DISPLAYS.md 0.4.0 blames for thirteen notebooks that drew nothing, and it is still in the skill that propagates. The correction lives in a draft that does not.

Counts: 0 Critical, 12 Warnings, 7 Notes. No finding meets the checklist's Critical (a secret, a security fault, a refuted claim a gate rests on). W1 and W2 should land before the notebook skill leaves draft.

Six subjects are missing from the display skill and are now relied on downstream: colour, words with images, tables, showing doubt, density and empty space, and the levels of a reading. Section 3 gives the text for each.

## 1. What Was Read and Run

| Material | State |
|---|---|
| `.claude/skills/designing-clear-data-displays/` (five files) | hub `30e9da1`, version 1.1.0 |
| `.claude/skills/writing-tours-and-case-notebooks/` DISPLAYS.md, CONFIDENCE.md, SKILL.md, REVIEWING.md | hub `30e9da1`, version 0.4.0 |
| The first display kit and its tests | sibling repo, read at `c0fa152`, re-read and mutated at `13cf20d` |
| Seven rendered figures and one sentence | the session scratchpad, `kit/` |

The kit moved under the review: commit `13cf20d` landed at 22:53 while I was reading. Every kit number below names its commit.

The per-figure findings and the kit's test gaps are the sibling repo's material. By this agent's scope rule they are written outside this repo, to `/tmp/claude-1000/-home-jhutchison-projects-github-tacsop/ecf1638e-1d43-44cb-ab96-60799e2f9fb3/scratchpad/reviewer2/20261122_display_kit_second_review.md`, for the repo that owns the kit. This report keeps what those findings say about the hub's two skills.

Sources checked. Every VDQI quotation in RULES.md was compared with the second-edition text the session holds in its scratchpad (`vdqi/v.txt`): all match (N1). The *Envisioning Information* file there is a PDF, and this machine has no text extractor, so every EI page cited below is UNVERIFIABLE here and is marked so. Two pages of Tufte's site were fetched: the sparkline thread and his 2001 reply on baselines.

I did not read the two other untracked files dated today under `docs/plans/` and `docs/reviews/`, so this reading is independent of them. I wrote no memory file and committed nothing.

Severity: the display protocol's Major is a Warning here and its Minor is a Note.

## 2. Where the Skill Misstates, Omits or Weakens Tufte

### W1. The pre-question keeps half of VDQI p. 56 and counts the wrong thing

**Where**: display `SKILL.md:11`, `REVIEWING.md:9`, `ADOPTION.md:24`, `CLAUDE.md:58`. In conflict with notebook `DISPLAYS.md:9` and `:20`.

**Evidence**: the page reads "Tables usually outperform graphics in reporting on small data sets of 20 numbers or less. The special power of graphics comes in the display of large data sets." The skill's four copies say "these numbers", which a reviewer reads as the numbers printed on the display, and none carries the second sentence. Tufte's noun is "data sets". DISPLAYS.md 0.4.0 ("count the data behind the claim, not the summary") is the correct reading of his sentence, so on that point the draft is right and the released skill is wrong.

The conflict is live. Pass 1 of `REVIEWING.md`, run as written on the seven figures, returns "a table, not a chart" for three: the unit chart (3 numbers), points on a scale (4) and lines over an input (10). `DISPLAYS.md:13` to `:16` orders each of them drawn. `REVIEWING.md:38` lists where an override may be stated (CLAUDE.md, the pillars, a decision table) and a skill sidecar is not on the list, so today the reviewer must flag figures the notebook skill requires.

DISPLAYS.md also goes past Tufte without saying so. "A claim about a shape is drawn whatever the count" (`:20`) is a house override: a unit chart of three counts is, by pp. 56 and 178, a text-table. The case for drawing it comes from the risk-communication work on natural frequencies, not from Tufte (cited from memory; not fetched).

**Replacement text**

`SKILL.md:11`, the last two sentences:

> Before the eight: count the data set, not the summary drawn from it. Two numbers fit a sentence (VDQI p. 178). A data set of about twenty numbers or fewer usually reads best as a table (p. 56). Past that, draw: "The special power of graphics comes in the display of large data sets" (p. 56). A mean and an interval from 20,000 draws are a data set of 20,000.

`CLAUDE.md:58` and `ADOPTION.md:24`, one line, changed in the same commit:

> Before the eight: count the data set, not its summary. Two numbers, a sentence; up to about twenty, a table; more, a graphic (VDQI pp. 56, 178).

`REVIEWING.md:9`, from "First, the pre-question" to "passes 2 and 3 run on the table.":

> First, the pre-question: count the data set behind the display, not the numbers printed on it. Two numbers: the finding is "a sentence, not a chart", the redraw is the sentence, and the rest of the review is the prose kernel's. About twenty or fewer: the finding is "a table, not a chart", and passes 2 to 4 run on the table. More than twenty, shown only as a summary (a mean, a count, an interval): the finding is "the data are not shown", and the redraw draws them.

`REVIEWING.md:38`, the sentence that begins "An override is stated when":

> An override is stated when it appears in the repo's ambient rules (CLAUDE.md), its pillars, the decision table of the plan that drew the figure, or a sidecar of a skill the repo has adopted. Cite the line.

`DISPLAYS.md:20`, the whole paragraph:

> **Count the data behind the claim, not the summary.** This is the display skill's pre-question, read as Tufte wrote it: the line of about twenty numbers counts the data set (VDQI p. 56). Twenty thousand draws reduced to a mean and an interval are twenty thousand numbers. Eighty-one solved cases reduced to three counts are eighty-one.
>
> **One override, and it is the house's, not Tufte's.** A claim about a proportion or a structure is drawn even when its data set is small: a unit chart of three counts, a tree of six leaves. The naive reading of such a claim is a wrong picture, and the display sets the right one beside it. The table is printed too, so no exact number is lost. A reviewer running the display skill's pass 1 cites this paragraph and does not issue "a table, not a chart".

`DISPLAYS.md:9`:

> Start with the display skill's pre-question (how large is the data set?), then ask what the sentence claims.

### W2. The skill declines Tufte's density principle, and nothing takes its place

**Where**: display `SKILL.md:68` ("Not a density rule in either direction").

**Evidence**: VDQI p. 168 reads "Maximize data density and the size of the data matrix, within reason." The skill quotes it as "maximize data density ... within reason": the ellipsis removes "and the size of the data matrix", the half that says show more data. The same page says "The simple things belong in tables or in the text; graphics can give a sense of large and complex data sets" and "Low-information designs are suspect: what is left out, what is hidden, why are we shown so little?" Page 169 gives the Shrink Principle: "Graphics can be shrunk way down."

The cost shows in the first kit. Measured on the seven renders at 100 dpi, non-white pixels are 3.0 to 7.2 percent of each figure, and two figures are more than half empty rows: 179 of 336 pixel rows in the unit chart, 215 of 416 in the payoff table. The maintainer saw both by eye. A reviewer following 1.1.0 has no rule number to cite for either.

**Replacement text**, `SKILL.md:68`:

> - **Not a density floor, and not a licence for empty space.** Tufte's principle is "Maximize data density and the size of the data matrix, within reason" (VDQI p. 168), and his Shrink Principle is "Graphics can be shrunk way down" (p. 169). The skill sets no number for either. It adopts their test under rule 8: a display that shows a summary where the data would fit, or holds a band of space that separates nothing, gets a finding with the redraw that fills it or trims it. A repo's own UX rules can require a less dense display for its readers; state the override.

Add to `RULES.md` section 8, after the test:

> **Second test**: shrink the figure until its smallest label reaches the floor rule 4 sets. Space that survives the cut and holds no mark, no label and no comparison is a finding.

Add to `REVIEWING.md:11`, pass 3:

> Find the empty bands: rows or columns of the render with no ink. A band taller than two lines of the figure's label type that separates nothing is a finding, with the size to cut.

### W3. No rule on colour, and a colour source cited for a rule that never states it

**Where**: display skill, all five files. `RULES.md:64` lists "Above all, do no harm" and Imhof's colour rules under the sources for rule 3; rule 3's text (`RULES.md:19`) never mentions colour. Notebook `DISPLAYS.md:120` to `:129` now carries six colour rules with no parent.

**Evidence**: VDQI has primary text the skill does not use. Page 154: "Color often generates graphical puzzles. Despite our experiences with the spectrum in science textbooks and rainbows, the mind's eye does not readily give a visual ordering to colors". Page 183, the friendly-graphic table: "colors, if used, are chosen so that the color-deficient and color-blind (5 to 10 percent of viewers) can make sense", and "(blue can be distinguished from other colors by most color-deficient people)". The EI chapter 5 material (do no harm; the four uses of colour as label, measure, imitation and decoration; Imhof's rules) is UNVERIFIABLE here.

`DISPLAYS.md:127` claims "the figure still reads printed in black and white: a kit colour is darker than the mid grey beside it". Re-run, the claim fails. I converted the region map to grey: the flame marks (luma 0.427) and the mid-grey marks (0.565) are 15 marks each of the same size and cannot be told apart by eye. The grey ramp has a mid grey of 0.565 only for three groups; for four groups its second shade is 0.420, which equals flame in grey. No test holds the claim: a kit colour changed to a pale `#ffd8a8` passes all 112 tests at `13cf20d`.

Two of the six rules in DISPLAYS.md are stricter than Tufte and should say so. "At most two colours in a notebook" is the house's number. "No colour for emphasis" contradicts his own sparklines, where a red dot marks the newest value ("red = the oldest and newest rates in the series", edwardtufte.com, the sparkline thread).

**Replacement text**, a new section in `RULES.md` after section 8. The kernel stays at eight lines.

> ## Colour (rules 2, 3 and 4)
>
> The failure is colour that carries a code, shouts, or carries nothing. "Color often generates graphical puzzles ... the mind's eye does not readily give a visual ordering to colors" (VDQI p. 154). Tufte's list of faults in a default chart names "encoded legends, color without content" (edwardtufte.com, 2003-01-08), and the first principle of *Envisioning Information* ch. 5 is "Above all, do no harm" (secondary source; book text not fetched).
>
> - Grey first. Ink for the data, grey for what the reader is not following. Add a colour only where it says what grey cannot.
> - A colour labels one named thing, and the name is on the figure beside it. A colour explained in a legend is an encoded key (rule 2).
> - An ordered quantity takes shades of one grey or one hue, light to dark. Hues have no order; a grey ramp on groups that have none implies one.
> - Small areas of strong colour on a quiet ground. Never large areas of strong colour side by side (Imhof's first rule, as Tufte gives it; book text not fetched).
> - Never colour alone. Every coloured mark keeps a label or a second difference of form. "Colors, if used, are chosen so that the color-deficient and color-blind (5 to 10 percent of viewers) can make sense" (VDQI p. 183).
>
> **Test**: convert the render to grey. Can a reader still name every mark? Then name what each colour says that a label does not already say.

Add "color without content" to the chartjunk list at `SKILL.md:54`. Add one line to `REVIEWING.md` pass 4: "Convert the render to grey and repeat the cover test."

`DISPLAYS.md:122`, the opening paragraph of Colour:

> The display skill's Colour section governs every figure. This section adds what a notebook needs, and three of its rules are the house's and stricter than Tufte: one colour per name across the notebook, at most two colours, and no colour for emphasis.

`DISPLAYS.md:127`:

> - **Never colour alone.** Every coloured mark keeps its label and a form of its own, and the figure passes the display skill's grey test. A reader who cannot tell red from green loses nothing.

### W4. Rule 2 stops at the legend; Tufte's integration of words and images goes to the page

**Where**: display `RULES.md:13` to `:15`; `SKILL.md:48` (the sparkline row); `SKILL.md:75`.

**Evidence**: VDQI p. 181, on the page after the one rule 2 quotes: "Data graphics are paragraphs about data and should be treated as such." And: "Tables and graphics should be run into the text whenever possible, avoiding the clumsy and diverting segregation of 'See Fig. 2'". Neither is in the skill. The maintainer's reading of a notebook as one piece of words, data and images rests on this page, and only the draft `DISPLAYS.md:109` to `:118` says it.

The sparkline row defines "a word-sized line chart with no axes, set in the sentence it belongs to". Tufte: "a small intense, simple, word-sized graphic with typographic resolution" that "can be everywhere a word or number can be: embedded in a sentence, table, headline, map, spreadsheet, graphic" (the sparkline thread, fetched). The skill's row is narrower twice over: line charts only, sentences only.

`SKILL.md:75` tells the reader to open RULES.md "before drawing anything larger than a sparkline". No file gives a rule for the sparkline, so the one display that sits inside prose is the one display with no rule.

The Saturn citation at `DISPLAYS.md:111` (*Seeing with Fresh Eyes*, p. 59) is UNVERIFIABLE here: the book is not on this machine. Tufte's own site carries a thread on Saturn set in Galileo's text, which supports the substance. Name the 1613 book (*Istoria e dimostrazioni intorno alle macchie solari*) so a reader can find the page.

**Replacement text**, appended to `RULES.md` section 2, before the test:

> The rule reaches past the label to the page. "Data graphics are paragraphs about data and should be treated as such"; "Tables and graphics should be run into the text whenever possible, avoiding the clumsy and diverting segregation of 'See Fig. 2'" (VDQI p. 181). A figure sits at the sentence that makes its claim. A figure small enough goes inside the sentence: a sparkline is "a small intense, simple, word-sized graphic with typographic resolution" and "can be everywhere a word or number can be" (edwardtufte.com, Sparkline theory and practice). The words or numbers beside a sparkline give its scale, so it needs no axis; a dot on it refers to a number the text states.
>
> **Second test**: is the figure within one screen of the sentence that makes its claim? Does any sentence send the reader to a figure by its number?

`SKILL.md:48`:

> | Sparkline | A word-sized graphic at the resolution of type, set where a word or number could go: a sentence, a table, a heading. The text beside it gives its scale. | 2, 6 |

`SKILL.md:75`, the last sentence: "Read before drawing anything, a sparkline included."

### W5. The skill sends small data to a table and has no rule for a table

**Where**: display `SKILL.md:11` and `REVIEWING.md:9` (the gate); no section on tables in any of the five files. Notebook `DISPLAYS.md:22` and `:151` require a table beside every figure.

**Evidence**: VDQI p. 178: "The conventional sentence is a poor way to show more than two numbers because it prevents comparisons within the data." "Tables are clearly the best way to show exact numerical values". "There are nearly always better sequences than alphabetical", for example by content or by data values. Page 179: "One supertable is far better than a hundred little bar charts." The skill uses p. 178 only for the pie chart.

**Replacement text**, a new section in `RULES.md`:

> ## Tables (the pre-question's other half)
>
> The pre-question sends a small data set to a table, so a table is a display and the passes run on it. "The conventional sentence is a poor way to show more than two numbers because it prevents comparisons within the data"; "Tables are clearly the best way to show exact numerical values" (VDQI p. 178).
>
> - Order the rows by the data or by the argument. "There are nearly always better sequences than alphabetical" (p. 178).
> - Set the numbers a reader compares in one column, aligned on the decimal point, to the digits the doubt allows.
> - Units go in the column head, once.
> - Group rows with space. A rule between every row is a grid (rule 3).
> - Two numbers that belong to one cell sit closer to each other than to the next cell (rule 4).
> - Beside a figure, print the table of the values its marks stand for.
>
> **Test**: can the reader compare the numbers that matter by running an eye down one column? Is the row order the data's?

### W6. Nothing on showing doubt, so DISPLAYS.md hangs nine failures on the lie factor

**Where**: display skill, no section. Notebook `DISPLAYS.md:97`: "Named failures, each an instance of display rule 5".

**Evidence**: rule 5 is a ratio of two effects (`RULES.md:31`). False precision, a confidence word with no number, and a mean of sources that disagree are not ratios, and a reviewer cannot "measure both effects and divide" for any of them. The citation gives nine failures a rule number whose test does not apply.

The kit shows the gap. Its distribution display prints "95% interval 8.24 to 8.29" on a row whose marks run from 6 to 9. It is a normal interval for the row's mean, and neither the row nor the note says so. A reader takes it for where the outcomes fall; the central 95 percent of that row's outcomes is 6 to 9 (computed from the same seed). `DISPLAYS.md:101` names this failure, and no display rule holds it.

**Replacement text**, a new section in `RULES.md`:

> ## Showing Doubt (rules 1, 6 and 7)
>
> Tufte gives no rule for uncertainty under that name. This section is the house's, built on three of his: show the data, so the draws and not only their mean ("Low-information designs are suspect: what is left out, what is hidden, why are we shown so little?", VDQI p. 168); document the display (principle 5 asks the designer to "point out relevant issues"); and compared to what.
>
> - Draw the distribution before its summary: every draw counted or placed, then the mean on the same scale.
> - A range is a line with its value as a point on it, on the display's own scale.
> - Every interval says what it is an interval of (the data, a mean, a spread of draws) and over how many draws.
> - An interval narrower than its mark is stated in words, not drawn.
> - Digits stop where the doubt starts. Near-ties are shown as ties.
>
> **Test**: for each number that came from a sample or an assumption, find on the figure what tells a reader how far to trust it. For each interval, cover the note: can the reader say what it is an interval of?

`DISPLAYS.md:97`:

> Named failures. The display skill's Showing Doubt section gives the general rule; these are the forms it took in the rollout:

### W7. The corrections sit in a draft that does not propagate

**Where**: notebook `SKILL.md:15` ("a draft kept out of propagation"); display `ADOPTION.md:46` ("propagates as a bundle").

**Evidence**: `DISPLAYS.md:5` says a gate of twenty numbers "was applied to the summary and not to the data behind it, and thirteen repos built notebooks that drew nothing". The gate's four copies are unchanged at `30e9da1`, and one of them is the block every downstream CLAUDE.md loads each session. Colour, words with pictures and the count-the-data reading are general display doctrine, and all three live only in the draft.

**Fix**: land W1 to W6 in the display skill as 1.2.0 and cut DISPLAYS.md back to what is particular to a notebook: the claim-to-shape table, the kit, the three levels, the comparison table, the doubt table, and the cell habits.

### N1. Every VDQI quotation in RULES.md matches the book; the "not fetched" markers can come off

**Where**: `RULES.md:7`, `:13`, `:31`.

Evidence: `python3 -I find.py vdqi/v.txt <phrase>` over the scratchpad text found, word for word: "Erase non-data-ink, within reason" (p. 96); "Erase redundant data-ink, within reason" (p. 100); the interior-decoration sentence (p. 107); the p. 120 sentence; "Lie Factors greater than 1.05 or less than .95 indicate substantial distortion" (p. 57); the caption-and-legend sentence and "Words and pictures belong together" (p. 180); "labels are placed on the graphic itself; no legend is required" (p. 183); the p. 74 and p. 168 sentences. Replace "(secondary source; book text not fetched)" with "(primary: the book text)" at those three lines. The EI and *Visual Explanations* markers stay.

### N2. Rule 5's test reads as a zero baseline for every chart

**Where**: `RULES.md:33` ("redraw with the whole available series and the baseline at zero"). Notebook `DISPLAYS.md:74` ("The scale is the whole range the value could take").

Tufte's reply of 2001-10-18 on his site says a time series takes a baseline that shows the data, not the zero point, and warns: "don't spend a lot of empty vertical space trying to reach down to the zero point". The rule's test is a check and is defensible. DISPLAYS.md:74 states the whole-range scale as a rule for every comparison, and the kit applies it to two displays and not to its line display, whose vertical scale is the data's range (a series from 0.96 to 1.00 gets an axis from 0.958 to 1.008 at `13cf20d`). Add to `RULES.md:33`: "A bar or an area starts at zero. A line may start where its data do, if the axis says so." Reword `DISPLAYS.md:74`: "The scale is the whole range when the claim is a share of that range: ten people at a station, 0 to 1 for a chance. When the claim is the gap alone, draw the gap."

### N3. The pie chart entry softens Tufte's conclusion

**Where**: `SKILL.md:57` ("A table beats it almost always"). VDQI p. 178 ends: "pie charts should never be used." Quote it.

### N4. Rule 7's kernel line drops authorship and date

**Where**: `SKILL.md:32`; `RULES.md:43` quotes "indicate the authors and sponsors" and the kernel keeps "title, source, units, scale". Add "and date" to the test at `RULES.md:45`, since a figure's source line without a date fails the Picture Style kernel too.

### N5. Three items of the friendly-graphic table are unused

**Where**: `RULES.md:13` quotes the table for legends only. The same table (VDQI p. 183) lists "words run from left to right" against words that "run vertically, particularly along the Y-axis". Two kit displays set a vertical y-axis label. Add to the chartjunk list at `SKILL.md:54`: "words set on their side".

### N6. Terms the kit already practises have no entry

**Where**: `SKILL.md:37` to `:49`. The kit's "ticks only where cases were solved" is Tufte's range-frame (VDQI pp. 130 to 132), and its heaviest line for the path of play follows p. 186 ("The heavier line should be a data measure"). VDQI p. 13 asks a graphic to "reveal the data at several levels of detail, from a broad overview to the fine structure", which is the micro and macro reading the three levels and the two readers of DISPLAYS.md stand on. Add three rows: range-frame (rule 1), line weight as meaning (rule 3), and levels of detail (rule 8). The EI chapter on micro and macro readings is UNVERIFIABLE here.

## 3. Missing Subjects

| Subject | In the display skill today | Relied on by | Fix |
|---|---|---|---|
| Colour | None; one orphan source line (`RULES.md:64`) | `DISPLAYS.md:120` to `:129`; the kit's three named colours | W3 |
| Sparklines and word-sized graphics | One terms row, too narrow (`SKILL.md:48`); exempted from RULES.md (`SKILL.md:75`) | `DISPLAYS.md:16`, `:41`, `:115` | W4 |
| Integration of words and images | Labels and legends only (rule 2) | `DISPLAYS.md:109` to `:118` | W4 |
| Tables as displays | A gate that sends data to a table; no rule for one | `DISPLAYS.md:22`, `:151`; the payoff table | W5 |
| Small multiples | Present and sound (rule 6, pair 4) | `DISPLAYS.md:53`, `:69` | None |
| Showing uncertainty | None | `DISPLAYS.md:78` to `:107`; `CONFIDENCE.md` | W6 |
| Micro and macro readings | None | `DISPLAYS.md:46` to `:56`, `:139` to `:151` | N6 |
| Density and empty space | Declined (`SKILL.md:68`) | Every kit figure | W2 |
| Shape and proportion | None. VDQI p. 186: "Graphics should tend toward the horizontal, greater in length than height" | Kit figure sizes | One line under rule 8 |

## 4. Links Between the Skills

| From | To | State |
|---|---|---|
| display skill | writing-simple-and-direct | Linked (`SKILL.md:88`, `REVIEWING.md:48`) |
| display skill | verifying-claims | Missing (W9) |
| display skill | notebook skill | None, and none needed once W7 lands: the general skill should not cite the particular one |
| notebook `SKILL.md` | display skill, verifying-claims | Linked (`:11`, `:124`) |
| notebook `DISPLAYS.md` | display skill | Linked, with two wrong rule numbers (W10) |
| notebook `REVIEWING.md` | display skill's protocol | Missing (W8) |
| notebook `CONFIDENCE.md` | `DISPLAYS.md` Showing Doubt | Missing (W11) |
| notebook skill | writing-simple-and-direct | Missing; `DISPLAYS.md:102` restates prose rule 6 without naming it (N7) |
| writing-simple-and-direct | display skill | Linked (`SKILL.md:11`); needs no change after W1 |
| verifying-claims | display or notebook skill | None; one line suggested (W9) |

### W8. The notebook review protocol has no step for a figure

**Where**: notebook `REVIEWING.md:31` (step 10) and `:53`.

**Evidence**: `DISPLAYS.md:156` tells the builder to run the display skill's protocol on every figure. The second reader's ten steps do not: step 10 still asks whether a reader would get the point "from its heading and its table alone", and the builder's report still lists "the figure it would add". Both are 0.3.0 wording, from when no notebook drew.

**Replacement text**, `REVIEWING.md:31`:

> 10. **Each figure.** Render it in a real kernel and look at it. Run the display skill's `REVIEWING.md` on the render, pass by pass, and the two checks a test cannot make: a label over a mark, and the render converted to grey. Check the title's numbers against the cell's asserts, and the figure's marks against the table printed beside it.
> 11. **Readability.** Would a reader new to the repo get each case's point from its heading and its display alone?

`REVIEWING.md:53`: replace "the figure it would add" with "each figure it drew, with its render".

### W9. No skill says a figure's title is a claim

**Where**: display `SKILL.md:80` to `:88` (References); `DISPLAYS.md:114`.

**Evidence**: `DISPLAYS.md:114` makes the title the finding. A title typed as a string, and any number drawn on a figure, is then a claim under verifying-claims, and neither skill sends the reader there. Add to display `SKILL.md` References:

> - The verifying-claims skill: a figure's title and every number drawn on it are claims. Build them from the values the figure plots, or check them against those values.

Add to verifying-claims `SKILL.md` When to Use: "Writing a figure's title or note: both are claims about the data drawn."

### W10. DISPLAYS.md cites two display rules for the wrong thing and names two kernels the same way

**Where**: `DISPLAYS.md:74`, `:97`, and `:48`, `:114`, `:141`.

**Evidence**: `:74` cites display rule 5 for one scale across two panels; that is rule 6 (`RULES.md:39`, "side by side, on one scale") and VDQI p. 61, "Show data variation, not design variation." `:97` is W6. Lines `:48`, `:114` and `:141` say "kernel rule 2", "kernel rule 6" and "Rule 8 of the kernel" for the notebook kernel, in a file whose other citations say "display rule N". At `:114` "kernel rule 6", set in a paragraph about figure titles, reads as the display kernel's "compared to what?". Write "notebook rule 2", "notebook rule 6" and "notebook rule 8", and change `:74` to "(display rule 6)".

### W11. CONFIDENCE.md and DISPLAYS.md state four rules twice, and one of them differs

**Where**: `CONFIDENCE.md:79`, `:81`, `:84`, `:85`; `DISPLAYS.md:91`, `:100`, `:104`, `:105`. Also `CONFIDENCE.md:52`.

**Evidence**: the ties-chain sentence is word for word in both files. So are the range-used-for-scale rule and the bias-has-a-direction rule. The zero-or-one rate differs: CONFIDENCE.md says it "has no normal interval" and stops; DISPLAYS.md adds "use the rule of three and say so". A builder who reads only the first writes no interval at all. `CONFIDENCE.md:52` tells the cell to "print what the report does", while `DISPLAYS.md:80` says a paragraph that states the distance as a number "has left the picture out", and CONFIDENCE.md never points there.

**Replacement text**. `CONFIDENCE.md:79`: "Give an interval, not "plus or minus" one standard error. A rate of 0 or 1 has no normal interval: use the rule of three and say so." Append to `CONFIDENCE.md:52`: "Draw it too: `DISPLAYS.md`, Showing Doubt, gives the display for each kind of doubt, and the distance from the fixture to the place where the answer changes is drawn, not only printed." In DISPLAYS.md, cut the three duplicated bullets at `:100`, `:104` and `:105` to a pointer: "Ties, yardsticks and biases: `CONFIDENCE.md`, Statistics Over Draws."

### N7. Smaller link faults

- `DISPLAYS.md:102`: add "(prose rule 6)" after "Hedge with numbers or not at all".
- `DISPLAYS.md:111`: say Galileo's letters were written in 1612 and printed in 1613, and name the book.
- Notebook `SKILL.md:85`, the row for rule 7: add "the kit's tests for its structure" between the import test and the display review, since 0.4.0 moved the cost of a figure into the kit.

## 5. Claims in DISPLAYS.md About the Kit, Re-run

Claims are re-run per the verifying-claims skill. Mutants ran in a scratch copy with the copy's source first on the path; a control mutant (one tick dropped) failed its test, so the harness can fail.

| Claim (`DISPLAYS.md` line) | Result |
|---|---|
| "104 tests" (`:32`) | Stale. Evidence: `pytest tests/unit/test_displays.py -q` gave `104 passed in 1.18s` before 22:53 and `112 passed` at `13cf20d`. A count in a skill file is a standing fact; date it or drop it |
| "A notebook imports no charting library, and `test_notebooks.py` fails one that does" (`:26`) | Holds in the hub. Evidence: `tests/unit/test_notebooks.py:83`, `test_it_imports_no_charting_library` |
| "the hub's `passage_chart` and `slope_chart`" (`:32`) | Exist. Evidence: `src/myproject/decision_science/visualization.py:321` and `:443` |
| "The kit refuses a colour for a name that is not drawn" (`:124`) | Held for six displays; no test holds it for the tree. A mutant that removes the tree's refusal passes 112 tests |
| "a kit colour is darker than the mid grey beside it" (`:127`) | Refuted for four or more groups, and unheld (W3) |
| "At most two colours in a notebook" (`:126`) | Not enforced. The kit drew four colours outside its named set in one figure without refusing |

### W12. Seven statements in the kit table are held by no test

**Where**: `DISPLAYS.md:36` to `:42`, the "Its tests hold" column and the "Answers" column beside it. Run at `13cf20d`.

| Row | Statement | What the tests allow |
|---|---|---|
| Points on a scale | "one line that is the whole range" | A scale line drawn over the upper half only passes. The test checks the limits of an axis that is switched off |
| Counts by group | "each row states its draws, mean and 95% interval" | Asserted for one row of three; a wrong summary on the last row passes |
| Region map | "each region named once among its marks" | "Once" is held. A name set on top of one of its own marks passes; the place is checked for one region against a rectangle |
| Region map | (the class) | It is the one display class with no overlap test, against `DISPLAYS.md:157` |
| Lines over an input | "a rule at each crossing" | The rule goes where the caller says. In the kit's own test data the rule stands at 0.25 and the two lines cross at 0.6875 |
| Word-sized line | "the size of a word" | Height only. A line 40 em wide passes |
| The product's own diagram | "The marks come from the solver the product calls, so the figure cannot disagree with it" | True of the equilibrium boxes and the path of play. The underlines and the ink-or-grey replies are computed inside the kit and tested against typed sets |

Two more gaps sit outside the table's words. No test compares a label with a mark, so the label the maintainer saw over a neighbouring mark passes, and so does a mutant that sets it on its own ring. A unit chart whose first group is drawn with marks three times the area passes, though the display's claim is that area is count.

`DISPLAYS.md:44` states the principle that would have caught the crossing: "A display takes the product's object where it can and derives the rest." The line display is the one that does not follow it.

**Replacement text**, `DISPLAYS.md:155`, a bullet added to Before a Figure Is Kept:

> - Test that no label lies over a mark, with the renderer's extents for both, and that every label lies inside the canvas. Convert one render to grey and look at it.

## 6. What the Protocol Run Says About the Skill

The seven figures and the sentence got the full pass order; the findings, with coordinates and redraws, are in the kit report named in section 1. Totals: 10 Major and 20 Minor across the eight. Their distribution is the evidence for section 2.

| Finding class | Count | Rule the skill gave me |
|---|---|---|
| A title's number that is not on the figure (a gap, a mean, a margin) | 3 | Rule 8, by stretching "name one datum to add" |
| A label or a key that the marks contradict | 3 | Rule 2 |
| A label over a mark, two marks read as one, a label far from its mark | 3 | Rule 4 |
| A mark with no name | 1 | Rule 2 |
| An encoding explained in the note (a positional order, an underline, a line weight) | 3 | Rule 2 |
| Type at 6.5 points | 1 | Rule 4, whose floor has no number |
| Four line weights for three meanings | 1 | Rule 3 |
| A vertical scale cut to the data where DISPLAYS.md asks for the whole range | 1 | Rule 5 against `DISPLAYS.md:74` (N2) |
| Empty bands, and two numbers of one cell set far apart | 5 | None (W2, W5) |
| An interval that does not say what it is | 1 | None (W6) |
| Colour that fails in grey, reads as emphasis, or is worn by the mark and not the name | 3 | None (W3) |
| A sentence whose dot reads against the wrong scale; a word-sized line too flat | 2 | None (W4) |
| Words set on their side; a hyphen for a minus sign | 3 | None (N5) |

Fourteen of the thirty had no rule number in 1.1.0. Lie factors were clean wherever a ratio could be measured: 1.000 on the three gaps of the scale display and equal pixels per count across the five rows of the distribution display.

One lesson for `REVIEWING.md:12`. Pass 4 says "Compute each label's footprint: does any two overlap?" and both the kit's tests and its builders read that as label against label. Rule 4's own title is "two marks too close". Reword pass 4: "Compute each label's footprint and each mark's: does any label overlap another label or a mark it does not name?" The same sentence also needs "do any two" for "does any two".

## 7. Ranked Changes for Display Skill 1.2.0

1. Rewrite the pre-question in its four copies to count the data set and to carry Tufte's second sentence; widen where an override may be stated (W1).
2. Replace "not a density rule in either direction" with the rule 8 test for a summary shown in place of data and for empty bands; add the shrink test and the empty-band check (W2).
3. Add the Colour section to RULES.md with its grey test, and the grey step to pass 4 (W3).
4. Add the Showing Doubt section; an interval says what it is an interval of (W6).
5. Extend rule 2 to the page (VDQI p. 181), redefine the sparkline row, and end the sparkline's exemption from RULES.md (W4).
6. Add the Tables section, so the pre-question's destination has rules (W5).
7. Reword pass 4 to compare labels with marks as well as with labels (section 6).
8. Add the verifying-claims reference: a title and a drawn number are claims (W9).
9. Mark the VDQI quotations as primary; soften rule 5's baseline sentence for lines; quote the pie chart sentence in full (N1, N2, N3).
10. Add three terms (range-frame, line weight as meaning, levels of detail), "words set on their side" and "color without content" to the chartjunk list, and "and date" to rule 7's test (N4, N5, N6).
11. Add two pairs to EXAMPLES.md: a mean printed in place of its draws (grows, as pair 5 does), and a coloured map that fails in grey.
12. Bump ADOPTION.md's kernel block in the same commit as SKILL.md, as `ADOPTION.md:28` requires, and note in the propagation entry that the pre-question changed meaning.

For the notebook skill at the same time: W1's two DISPLAYS.md paragraphs, W8, W10, W11, and the cut-back of DISPLAYS.md that W7 describes.

## 8. Not Done

- The EI pages (colour, layering, small multiples, micro and macro) were not checked against the book: no PDF text extractor on this machine.
- *Seeing with Fresh Eyes* p. 59 and *Beautiful Evidence* were not checked: neither is on this machine.
- The four displays added to the kit at `13cf20d` (a dashed rule for a naive reading, a broken line, several fixtures, a log scale) were read as code and not rendered.
- The hub's own `passage_chart` and `slope_chart` were not reviewed.
