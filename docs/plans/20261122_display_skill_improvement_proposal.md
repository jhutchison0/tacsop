# Proposal: Improving the Hub's Figure Doctrine

## Problem

The maintainer wants notebooks that work as communication tools: words, numbers and pictures in one reading, with the raw, staged and production data shown and with results, confidence and uncertainty drawn. He asked three things. Can the skills improve? Would Tufte approve? Do they use all that Tufte offers?

Short answers. Yes, in eight specific places. Mostly yes on the eight rules, with seven objections to the rendered figures and six to `DISPLAYS.md` (below). No: colour, tables as displays, annotation layering, and lineup tests for uncertainty are in Tufte and not in the skills.

Material read: `designing-clear-data-displays` 1.1.0 (all five files), `writing-tours-and-case-notebooks/DISPLAYS.md` 0.4.0 and `CONFIDENCE.md`, `schelling-point/src/schelling_point/viz/displays.py` (845 lines, colour handling only), and the seven rendered figures in the scratchpad `kit/` folder. Figure observations come from the PNGs; I measured no pixels, so each overlap claim says "appears".

## 1. Citation Verdicts

"Primary" means Tufte's own words: his site, or the book text. "Secondary" means another page quoting him. Page numbers appear only where a source showed one.

Evidence for the VDQI rows: the second edition's text layer (a scan of the book at archive.org, extracted with a script, read in the scratchpad) carries the running heads "56 GRAPHICAL PRACTICE", "30 GRAPHICAL PRACTICE", "178 THEORY OF DATA GRAPHICS" and "180 THEORY OF DATA GRAPHICS" over the passages quoted. Cite the book, not the scan.

| Claim in the doctrine | Verdict | Basis and what I could not find |
|---|---|---|
| Galileo's Saturn drawing sits inside a sentence | Primary for the fact, nothing for the date "1612 manuscript" | Tufte's notebook thread "Saturn embedded in Galileo's text, best work of analytical design ever?" (edwardtufte.com). In it Tufte writes that the two Saturn images "were almost certainly printed right along with the type" (comment of 2002-01-25). The work is *Istoria e dimostrazioni intorno alle macchie solari*, Rome, 1613 (secondary: MIT gallery page; Design Observer 2004-07-06, which calls the drawing "a visual noun"). The first of its three letters is dated 4 May 1612 and carries "two simple in-line sketches" of Saturn (secondary: Wikipedia, Letters on Sunspots). So "written in 1612, printed in 1613" holds; "a 1612 manuscript" has no source, and the drawing Tufte praises is the printed one. |
| Reproduced in *Seeing with Fresh Eyes* p. 59 | UNVERIFIED | Searched the book's page on edwardtufte.com and four web searches. No source gives a page, or says the book reproduces it. |
| Reproduced in *Beautiful Evidence* | Secondary | Tufte's thread comment of 2005-06-09 says his *Beautiful Evidence* comments on "Galileo's 2 saturns, along with references". The references were an image I could not read. Tufte's site gives the sparklines chapter as pp. 46 to 63; I found no page for Saturn. Tufte files Saturn under sparklines, which matters for proposal 4 below. |
| Envisioning Information, "Color and Information" (ch. 5) | Secondary | The chapter's existence and title: the book's page on edwardtufte.com lists "color and information". The full book scan (38 MB) has no text layer and I could not render it. |
| "Above all, do no harm" | Secondary, Tufte quoted | WIRED review by Peter Myers (January 1999), reposted on edwardtufte.com: "Above all," he pleads, "do no harm." Student notes and Georgia Tech slides give the same line. No page. |
| Four uses of colour: label, measure, represent or imitate reality, enliven or decorate | Secondary | A 2017 student post lists all four. A course-notes page lists only three (labels, measures, imitate reality). I found the fourth only in the student post. No page. |
| Small spots of strong colour on muted fields | Secondary | Course notes: "Pure bright colors should be reserved for small highlight areas and almost never used as backgrounds" (chnm.gmu.edu, citing EI pp. 92 to 94 for related points). A UBC handout cites EI p. 82 for pastels over large areas ("excessively exuberant"). I could not confirm either as Tufte's sentence. |
| Colours found in nature | Secondary | Eye magazine review (Autumn 1990) quotes Tufte: "Nature's colours are familiar and coherent, possessing a widely accepted harmony to the human eye." The reviewer calls the advice weak: it "does not narrow the choice very much". |
| Sparklines: "data-intense, design-simple, word-sized graphics" | Primary | edwardtufte.com, "Sparkline theory and practice": "Sparklines are datawords: data-intense, design-simple, word-sized graphics." Also "A sparkline is a small intense, simple, word-sized graphic with typographic resolution." The book's chapter is titled "Sparklines: intense, simple, word-sized graphics". |
| VDQI p. 56, the "about twenty numbers" line | Primary | Page 56: "Tables usually outperform graphics in reporting on small data sets of 20 numbers or less. The special power of graphics comes in the display of large data sets." The doctrine's "about twenty" paraphrases; quote the source. |
| Words and pictures together (RULES.md rule 2) | Primary, upgrade from secondary | VDQI p. 180: "Words and pictures belong together." Next sentence: "Words on graphics are data-ink". The "dart back and forth" clause is on the same page. RULES.md lists these as secondary. |
| Lie factor and the 0.95 to 1.05 band (rule 5) | Primary, upgrade from secondary | The lie-factor page follows p. 56 by sequence: "Lie Factors greater than 1.05 or less than .95 indicate substantial distortion". |
| Online course on text and image, or on uncertainty | Nothing on the course page | The course page (edwardtufte.com/online-course/) lists sentences, tables, diagrams, maps, charts, credibility, cherry-picking, alternative explanations and standards of comparison. It does not name text-image integration, uncertainty, colour or sparklines. |
| (Found, not asked) Tufte on showing that a pattern may be chance | Primary | edwardtufte.com/?p=92, "Making better inferences from statistical graphics": ten randomized sparklines set beside the real one, "an 'Interocular Trauma Test'"; "Good statistical analysis seeks to calm down the rage to conclude". This is proposal 7. |
| (Found, not asked) ordering | Primary | VDQI p. 178: "There are nearly always better sequences than alphabetical—for example, ordering by content or by data values." Same page: "Tables are preferable to graphics for many small data sets." |
| (Named by the maintainer) "data paragraph" | Nothing | Searched Tufte's site and the web for "data paragraph" and variants. Tufte's term is "dataword" for a sparkline. Treat "data paragraph" as the house's own word for a computed sentence with graphics in it, and say so. |

Two page-level facts the doctrine should also carry. VDQI p. 30: "Why waste the power of data graphics on simple linear changes, which can usually be better summarized in one or two numbers?" This is the counterweight to `DISPLAYS.md` 0.4.0, which says a shape claim is drawn "whatever the count". And VDQI p. 159 shows a "table-graphic": a ranked table whose name spacing is proportional to the values, which Tufte uses as a display in its own right.

## 2. What the Skills Leave Out, Ranked

Rank is by what the rule would change in notebooks the house actually writes. "Where" names the skill that should carry it.

| Rank | Tufte material | The rule it becomes | Its test | Where |
|---|---|---|---|---|
| 1 | Colour (secondary sources, section 1) | Colour is a distinction, so rule 3 governs it: grey is the field; a strong hue is one small spot that names the thing the sentence is about; a hue means one thing everywhere; large areas stay muted | Print the figure in greyscale: every claim still reads. Name each hue in one phrase; a hue you cannot name goes. Count hues; each needs a name drawn on the figure | Display skill (RULES.md under rule 3). The notebook skill keeps its two-colour cap and "imitates the thing" advice as house policy |
| 2 | Tables as displays; order by value (VDQI pp. 56, 159, 178) | A table is a display. Rows are ordered by the value the claim names, not by name or id. A table may carry marks (semi-graphic) | Sort test: sort by the claim's value. If the claim shows in the top, the bottom or a gap, a table carries it. If rows are in input order, say why | Display skill (new paragraph in RULES.md rule 6, since ordering enforces comparison); notebook skill's choice table |
| 3 | Words on graphics are data-ink (VDQI p. 180); title numbers belong on the figure | Every number in a title or note appears on the figure at its place | Take each number in the title and note; find it as a tick, label or mark. Failures below: `0.545` and `6.90` | Display skill rule 2 test; notebook skill's "Before a Figure Is Kept" and a kit assert |
| 4 | Layering and separation applied to annotation (EI ch. 3, already cited in the terms table, never used as a rule) | An annotation sits in the quietest layer that still reads and touches its mark, or has a leader no longer than its label | Squint: the data layer dominates. For each annotation, name the mark it describes without reading the note | Display skill rule 4 test |
| 5 | Showing uncertainty: the lineup (edwardtufte.com/?p=92) | Where the claim is "this pattern is real", draw the observed data among randomized versions of it | Shuffle the real panel's position; a reader who cannot pick it out has been told the pattern may be chance | Notebook skill (Showing Doubt table) and the kit |
| 6 | Word-sized graphics (BE; Saturn is a sparkline antecedent) | A word-sized graphic goes wherever a word or number goes: in a sentence, in a table cell | The graphic is one text line high, carries no axis, and the sentence gives its end values | Notebook skill; display skill already defines the term |
| 7 | Micro/macro readings (EI ch. 2; only the chapter title found, wording UNVERIFIED) | One display gives an overview and, in the same ink, the single case | Name the overview in a sentence and name one mark's meaning: both from the figure alone | Notebook skill ("For Two Readers" already reaches for it) |
| 8 | Parallelism in small multiples (VE; the TOC lists "Parallelism: Repetition and Change, Comparison and Surprise", p. 79, secondary) | Panels share design and scale, and their order is a stated variable | Name the variable the panels are ordered by | Display skill rule 6 test, one clause |
| 9 | Narrative and causality (BE principle 2) | A causal claim draws its mechanism's own numbers | Already in `DISPLAYS.md` ("draw the formula and plot the cases over it") | No change |
| 10 | Documentation and credibility (course; BE principle 5) | Rule 7 | Already in kernel and `DISPLAYS.md` ("fixture is invented") | No change |
| 11 | Confections (VE p. 121, secondary) | Composite displays that mix dissimilar images | None proposed: no notebook need found | Skip |

## 3. Approaches

### Approach A: Patch the text, keep the eight (conservative)

Edit `RULES.md`, `SKILL.md`, `REVIEWING.md` and `DISPLAYS.md` with the eight changes in section 6. The kernel in CLAUDE.md stays at eight lines, so nothing propagates to the downstream repos.

- Pro: one evening; every change has a source or a rendered failure behind it; no kit change is required to be correct.
- Con: rules in prose do not fail a build. By my reading, six of the seven rendered figures break rule 2, 4 or 7 today (section 5), with the kit's 104 tests reported as passing, so the tests hold structure and not these rules.
- Risk: low.

### Approach B: Put the rules in the kit (bold)

Move the new tests into `displays.py`, where "a rule is held by a test that fails" already works.

- A `Notebook` style object holds the colour registry: a name gets one hue for the whole notebook, and a call with a second hue for the same name raises. Today `_refuse_stray_colours` checks each call alone. The payoff table and game tree both give the flame hue to "Sabotage", while the points-on-a-scale figure gives it to "Burn the suspects". If those figures share a notebook, one hue has two meanings and nothing in the kit sees it.
- Every display takes its title as a template plus values, and a shared test asserts each number in the title is drawn as text on the figure. This catches `0.545` in the region map today.
- A shared test reads each annotation's bounding box and its mark's, and fails when the gap is wider than the label.
- Trade-off: this is code in the repo that is not the hub, with no second user yet. `DISPLAYS.md` already says so under "What Is Not Settled". Put the doctrine first and the kit change in the same sitting only where a failure is rendered.
- Risk: medium; the kit's 104 tests need extending, and the renderer's text extents are the fragile part.

### Approach C: Invert the default toward the word-sized table (bold alternative)

Challenge: the eight displays all assume a figure is the answer to a shape claim. Tufte's own small-data answer is the table, and his own hybrid is the table with marks in it (VDQI pp. 159, 178; sparklines in tables, per his site). Make the sorted semi-graphic table the first display a case reaches for, with a sparkline column for any row that has a trajectory, and let the eight figures be the escalation when the data behind the claim exceed twenty or the claim is about position or structure.

- Pro: one object serves all three of the maintainer's aims at once. Words, numbers and picture share a row, the raw and the reported numbers print in the same table, and the second reader needs no beside-table because the table is the figure.
- Pro: fixes the points-on-a-scale figure (below): four numbers and four long labels are a table that needs one bar per row.
- Con: a notebook of tables risks the failure DISPLAYS 0.3.0 had, thirteen notebooks that drew nothing. The 0.4.0 rule exists because a table was the cheap answer. The fix is the count rule in change 1, which sends large data to a figure.
- Con: new kit function, a front-end render test, and the "how a word-sized graphic renders outside a notebook" gap that `DISPLAYS.md` lists as untested.
- Risk: medium.

### Approach D: The lineup as the doubt display (bold, narrow)

Add one display: the observed result among nine randomized ones, positions shuffled, the answer printed in the table beside it. The notebook already simulates (20,000 nights), so the randomized versions are free. It replaces "a mean with its draws left out" and "an error bar that names nothing" with a picture a reader judges for themselves.

- Pro: Tufte's own method (edwardtufte.com/?p=92), and it answers the maintainer's wish to show confidence and uncertainty without a number the reader must trust.
- Con: it fits claims of the form "this pattern is not chance" and not "this boundary sits at 0.545". It covers one row of the Showing Doubt table.
- Risk: low to medium.

## 4. Recommendation

Do A tonight. Add C's table rule (change 5) and D's table row (change 7) as text. Defer B until a second repo uses the kit, except the title-number assert, which is cheap and catches a defect that is on screen now. Tufte's sources support A directly; B and C are the house's own extensions of them.

**Do not add a ninth display rule.** Colour is a distinction, so rule 3 covers it. Words and images are rule 2 (VDQI p. 180) and the principle 4 quotation it already carries. A ninth line also costs every downstream CLAUDE.md a propagation, and "rule 9" is already the confidence section's name in `CONFIDENCE.md`, which invites a citation mix-up between the two kernels. Put colour and the title-number test in `RULES.md` and leave the eight lines alone. If colour proves to need its own line after a quarter of use, add it then, with the evidence.

**The pre-question should change.** `DISPLAYS.md` 0.4.0 is right that the gate was applied to the summary and not to the data. It overcorrects with "a claim about a shape is drawn whatever the count". Tufte's page 30 says graphics are wasted on changes "better summarized in one or two numbers". Six cases of a value collapsing are a table; a figure of six marks has a lie factor in its ink and no more information. The rule should count the data and test the table.

**Kit contents beyond the eight.** Ranked by notebooks affected:

| Display | Answers | Its tests hold |
|---|---|---|
| Sorted table with marks | Which is highest, and by how much, for a handful of items | Rows ordered by value; one mark per row, proportional; units in the header once |
| Difference panel for points on a scale | How far apart, when the gap is 9 percent of the scale | The difference drawn in its own panel and labelled as a difference (this is rule 5's existing test, applied) |
| Interval on the report's scale | How wide is the doubt, around one value | Range as a line, value as a point, both ends named; a rate of 0 or 1 uses the rule of three and says so |
| Place ranges | Where can each item land, from every pair compared | A line per item from its best to worst place; ties shown as ties |
| Lineup | Is the pattern chance | The real panel at a shuffled position; the answer in the table |
| Small multiples wrapper | The same display over cases | One scale across panels, asserted; a stated order |
| Before and after per step | What did each step do (the "handled level with more than two steps" that `DISPLAYS.md` says has only text) | One panel per step on one scale |
| Slopegraph, passage chart | Already in the hub | Move into the kit, as `DISPLAYS.md` hints |

`CONFIDENCE.md`'s Showing Doubt table already names interval, place ranges and the lineup's cousin, so the kit would catch up with the doctrine on these.

## 5. Where Tufte Would Object

### The seven figures

Tufte would approve of the counts figure (needles labelled with their counts; every draw shown), the region map's formula lines drawn separately from the marks, the titles that state findings, the greyscale default, and the single flame point on the points-on-a-scale figure (small, strong, imitative, labelled). The objections:

1. **Unit chart.** The 60 hollow boxes carry the same dark outline as the filled ones. Rule 3 asks for the lightest outline that still separates. Roughly 100 pixels of blank space sit above and below the rows. The label "Things, who all fail" puts an assumption inside a row name.
2. **Points on a scale.** Four numbers are a table under VDQI p. 56. The title claims gaps of 0.89 and 0.91 on a ten-unit line, so each gap is about 9 percent of the width; the reader cannot see what the title says. The open circle is explained in the note ("The open point is what the naive rule counts on"), which is a key. The leader lines are ink for locating, not for measuring; a row per item with the label at the mark would need none.
3. **Counts by group.** The title gives "their mean is 6.90" and no mark on the figure shows 6.90 or any mean; the means appear only in the right-hand text, which also runs to the figure's edge (the longest line ends near x 894 of about 900). Mark each row's mean on its axis.
4. **Region map.** The title's `0.545` is not marked on the figure. The label "the fixture" appears to run over the mark at (0.6, 0.10). Region names are set large and bold over the marks they name, while the data are small; label weight outranks data weight. The y ticks are uneven (0.05 steps low, 0.10 to 0.30 steps higher), which is honest to the cases and still reads as a scale.
5. **Lines over an input.** The red hue goes to "with an alibi", a name that imitates nothing; the doctrine's own rule says a hue means a thing in the story, and this is a second hue unrelated to the flame one. The vertical rule at 0.25 is labelled "an alibi stops clearing", while the two lines visibly cross near 0.67; I cannot tell from the figure what 0.25 marks. The rings at 0.5 are named nowhere on the figure (the note says only "Invented fixture."). The y axis has two ticks.
6. **Payoff table.** "Each cell: Ripley's payoff, then Burke's" is a key in the note; the cell has no border and the two numbers sit apart, so "6  -8" reads as two columns of one row. "what she hopes for" is black italic and floats midway between row 1 and row 2, so it can attach to either the 6 or the 5. Annotation belongs in the quiet layer, with a leader.
7. **Game tree.** "Ripley" and "Burke" repeat on all six leaves; label the two columns of numbers once. "what she hopes for" sits about 100 pixels right of its leaf. Line weight has three levels and the note names one ("Heavy line: the path of play"); the medium weights, which appear to be each reply Burke prefers, are decoded by the reader. Flame on "Sabotage" repeats the one-hue-two-meanings risk from approach B.

Every note sits at about 8 pt in grey. Rule 4's legibility floor is "what the target screen can read"; I did not test that on the target screen.

### `DISPLAYS.md` 0.4.0

1. **"A claim about a shape is drawn whatever the count."** Tufte's p. 56 and p. 30 say otherwise for small sets (section 1). The count-the-data move is right; "whatever" is not.
2. **"Two or three numbers set side by side: not a shape, a table. Points on one scale if the gaps are the point."** The kit's own figure has four, and 0.9 on 10 is a small gap on a long line. Tufte's range-frame (VDQI p. 130) trims the frame to the measured limits and labels the maximum and minimum. The doctrine's "whole range named at both ends" and the range-frame pull opposite ways. Resolution: the whole range for a share or a chance; a difference panel when the gap is the claim.
3. **"No colour for emphasis."** Course notes attribute to Tufte the opposite for one case: a bright colour kept for small highlight areas on a muted field. The doctrine allows colour for a named thing, so flame on "Burn the suspects" passes, but it bans the same hue used to pick out the one mark a sentence is about. Both should be licensed, with the ban kept for good-and-bad pairs (red and green) and decoration.
4. **"At most two colours."** A house cap, useful, not Tufte's; Tufte's cautions are about area, saturation and harmony with nature. Say it is the house's.
5. **"A figure never stands alone. Print the table beside it."** Sound for the second reader, but Tufte's way is one display that carries both (p. 159 table-graphic; the counts figure already labels every count). Keep the table where the figure holds more than about twenty marks, and put the numbers on the marks where it holds fewer.
6. **The Galileo paragraph** has three problems. "Written in 1612" is true for the first letter (4 May 1612) and the drawing Tufte praises is the 1613 print. "(Seeing with Fresh Eyes, p. 59)" is UNVERIFIED. It also files the example under integration of words and images but does not say that Tufte treats Saturn as a sparkline's ancestor, which is the stronger support for "set a word-sized graphic in the sentence".

## 6. Top Eight Changes, Ranked, With Wording

Each is exact enough to paste. Files are under `.claude/skills/`.

**1. The count rule, in three places.**

`designing-clear-data-displays/SKILL.md`, replace the sentence beginning "Before the eight":

> Before the eight: count the numbers behind the claim, not behind its summary. At twenty or fewer, a table sorted by the value the claim names usually carries them (VDQI p. 56: "Tables usually outperform graphics in reporting on small data sets of 20 numbers or less. The special power of graphics comes in the display of large data sets."). Past twenty, or where the claim is a boundary or a structure that no sorted table shows, draw.

`designing-clear-data-displays/REVIEWING.md`, pass 1, same replacement for "Under about twenty numbers a table usually does (VDQI p. 56)".

`writing-tours-and-case-notebooks/DISPLAYS.md`, replace "and a claim about a shape is drawn whatever the count" with:

> A claim about a shape is drawn when the data behind it exceed twenty, or when no table sorted by the claim's value shows it. Six cases of a value collapsing are a table, and VDQI p. 30 asks why graphics should be spent on changes "better summarized in one or two numbers".

**2. Colour, in `designing-clear-data-displays/RULES.md`, as a subsection of rule 3, with sources marked secondary.**

> **Colour is a distinction.** Rule 3 governs it. Tufte's first rule for colour is "Above all, do no harm" (*Envisioning Information*, ch. 5, "Color and Information"; page not found; secondary: WIRED review reposted on edwardtufte.com). He gives four uses: to label, to measure, to represent or imitate reality, and to enliven or decorate (secondary: student notes; the fourth use is the one to check against the book). Course notes attribute to him two habits: keep pure, bright colours for small highlight areas, and use muted colours for large ones; and prefer colours found in nature (secondary: chnm.gmu.edu; Eye, Autumn 1990).
>
> **Test**: print the figure in greyscale; every claim must still read. Name each hue in one phrase; a hue with no name goes. Count the hues, and each must be named by a label on the figure. A hue that imitates its subject (flame, water) beats one that must be learned.

Add to `SKILL.md`'s terms table: `| Colour | A distinction at its strongest. Grey is the field; a strong hue is one small spot that names a thing. | 3 |`

**3. Title numbers on the figure, in `RULES.md` rule 2 and `DISPLAYS.md` "Before a Figure Is Kept".**

> **Test (added)**: take every number in the title and the note. Each appears on the figure as a tick, a label or a mark, at its place. The region map's title names 0.545 and no mark shows it.

`DISPLAYS.md`, new bullet:

> - Assert that every number in the title is drawn as text on the figure. A title built from values (`f"... {share:.3f}"`) can drift from the picture as easily as from the cell.

**4. Annotation layer and proximity, `RULES.md` rule 4, appended to the Test.**

> An annotation is also a layer (Layering and Separation, *Envisioning Information* ch. 3). Set it in the quietest ink that still reads, and keep it touching the mark it describes, or joined by a leader no longer than the label. A note that floats between two marks fails. Squint: the data layer must dominate.

**5. Tables as displays, `RULES.md` rule 6, and the choice table in `DISPLAYS.md`.**

`RULES.md`, rule 6, append:

> A table is a display and answers to the same question. Order rows by the value the claim names: "There are nearly always better sequences than alphabetical" (VDQI p. 178). A table may carry a mark per row (a semi-graphic, VDQI p. 178; a table-graphic, p. 159). **Test**: sort by the claim's value. If the claim shows in the top, the bottom or a gap, a table carries it.

`DISPLAYS.md`, in the "Draw a Shape" table, replace the last row with:

> | Two to about twenty numbers set side by side | Not a shape | A table sorted by the value the claim names, with a bar per row if the gaps are the point. When one gap is the claim, a panel that draws the difference |

**6. One hue, one meaning; one licensed spot. `DISPLAYS.md` "Colour".** Replace the "No colour for emphasis, rank or mood" bullet with:

> - **A colour may pick out the one mark the sentence is about**, as one small spot on grey, with its label. It does not mark good and bad, rank or mood: not red for the naive rule and green for the repo's. A hue means one name in every figure of a notebook, and the kit checks this where it can.

And append to "At most two colours in a notebook": `(a house cap, not Tufte's)`.

**7. The lineup, a new row in the `DISPLAYS.md` "Showing Doubt" table.**

> | Whether a pattern could be chance | The observed result among nine randomized ones from the notebook's own simulator, positions shuffled, the answer in the table beside it (Tufte's "Interocular Trauma Test", edwardtufte.com, "Making better inferences from statistical graphics") |

**8. Citation corrections, apply regardless of the rest.**

`DISPLAYS.md`, replace the first sentence of "Words and Pictures Together":

> Galileo's first letter on sunspots, dated 4 May 1612 and printed in Rome in 1613 (*Istoria e dimostrazioni intorno alle macchie solari*), set two small drawings of Saturn inside the sentences that described it. Tufte discusses the page as a forerunner of the sparkline, a word-sized graphic (edwardtufte.com, "Saturn embedded in Galileo's text"; *Beautiful Evidence*, sparklines chapter, pp. 46 to 63).

Drop the "(Seeing with Fresh Eyes, p. 59)" reference until someone checks the book. In `RULES.md` rule 2, add "Words on graphics are data-ink (VDQI p. 180)." In `RULES.md` Sources, upgrade p. 180, p. 56 and the lie-factor page (p. 57, 0.95 to 1.05) to primary, naming the second edition's text.
## 7. Open Questions

1. **Colour sources.** The *Envisioning Information* text is unread by me. Someone with the book should confirm the four uses, the "do no harm" sentence and its page, and the muted-field passage, then move those rows from secondary to primary. If the book words differ, the wording in change 2 follows the book.
2. **Do the payoff table and game tree share a notebook with the points-on-a-scale figure?** If so, the flame hue has two meanings today. I did not open the notebooks.
3. **Does the unit chart's grey squares carry meaning beyond "humans who fail"?** If not, the dark outline on the hollow squares is the whole of objection 1.
4. **Saved outputs** (still undecided in `DISPLAYS.md`): the title-number and layering tests are cheaper to enforce if committed outputs exist for a reviewer to look at.
5. **Is the figure at 8 pt note size readable on the maintainer's target screen?** Test it before adopting any size change.
6. **Whether to drop "the table beside it" below twenty marks** (`DISPLAYS.md` objection 5) is the maintainer's call; I recommend keeping the table until a second reader has used a figure with numbers on its marks.
