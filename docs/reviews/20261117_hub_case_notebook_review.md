# Review: The Hub's Case Notebook and Its Two Displays

**Author**: code-reviewer
**Date**: 2026-11-17
**Type**: Code review (notebook, two display functions, two test modules), second reader per `.claude/skills/writing-tours-and-case-notebooks/REVIEWING.md`

## Verdict

**Sound after fixes.** The suite passes (688), all 47 negated units die, and the output is identical under two timezones and two hash seeds. Four Criticals sit in sentences and in the own-data cell, where the suite cannot look:

1. **Cell 18** asserts that River Bend is first most often. That holds in 102 of 200 other seeds. The two sites are tied.
2. **Cells 17 and 19** say `monte_carlo` draws weights "near the stated ones". The draws are as wide as a uniform draw over all weights. The Limit's finding belongs to that width.
3. **Cell 11** says the exponential fault was "found by running the tour's cells". The repo's records say a property-test strategy found the crash on 2026-07-20, 117 days before the fix.
4. **Cell 23** prints "none" after checking nothing, and scores cost criteria backwards.

Cases 1 and 2 are sound in what they assert. Case 3's arithmetic is right and its history is wrong. Case 4 is sound. The confidence cell's two results are true on this fixture and belong to the fixture and to the width of the assumed range, and the text does not say so.

Not done: the notebook was not opened in a front end (no `nbformat` or `nbclient` in `.venv`, and the brief forbids installs). No file under `src/`, `tests/`, `notebooks/` or `.claude/` was changed. Every mutation ran in a local clone at `<scratch>/hub/clone`, since removed.

`docs/design/pillars.md` is still the unfilled template, so this review used the principles in `CLAUDE.md` in its place.

## State on Arrival

| Command | Last line |
|---|---|
| `git status --porcelain \| wc -l` | `0` |
| `git rev-parse --short HEAD`; `git branch --show-current` | `100dfb3`; `main` |
| `.venv/bin/python -m pytest -q -p no:cacheprovider` (committed tree) | `688 passed, 1 warning in 22.56s` |

During the review an untracked file appeared that this review did not write: `docs/reviews/20261117_hub_case_notebook_maut_audit.md`. This review did not read it, so the two reports are independent.

Evidence: `git status --porcelain` at the end printed `?? docs/reviews/20261117_hub_case_notebook_maut_audit.md` and, after this file was written, this file.

## Critical

### C1. Cell 18: the Limit's headline assert passed by luck

`assert report.winner == "River Bend" != leader, "the site first most often is not the site first on the stated weights"`.

Evidence, in the clone, `monte_carlo(scorer, sites, n_samples=2000, seed=s)` for `s` in 100 to 299:

```
seed 7: Airport 0.3820 River 0.3985 Rail 0.2195
seeds 100..299, n=2000: winner counts {'River Bend': 102, 'Airport Road': 98, 'Rail Yard': 0}
  each assert holds in (not robust, winner is River Bend, gap < 0.05, Old Mill never first): [200, 102, 194, 200] all four: 98 of 200
n=200000 seed 12345: first-place share {'Rail Yard': 0.2193, 'Airport Road': 0.3896, 'River Bend': 0.3911, 'Old Mill': 0.0}
```

At 200,000 draws the two shares differ by 0.0015 and the standard error of that difference is about 0.002. The sentence is not supported at any sample size the suite can afford.

The same assert depends on numpy's Dirichlet stream. `pyproject.toml:15` pins `numpy>=1.24` with no upper bound, and numpy does not promise a `Generator` method's stream across versions. Installed: numpy 2.5.1. With `np.random.default_rng` patched in the probe to another bit generator at the same seed:

```
seed 7 through Philox: Airport 0.3985 River 0.3850 asserts (True, False, True, True)
seed 7 through SFC64: Airport 0.3950 River 0.3905 asserts (True, False, True, True)
criteria order permuted, seed 7: cell 18's four asserts fail in 2 of 24 orders
```

UNVERIFIED: whether a released numpy changes this stream; no second numpy could be installed. The probe shows the assert has no margin against one.

**Fix.** Assert what holds in 200 of 200: `not report.is_robust`, the dominated site never first, and the stated leader first in under half the draws (measured range over 200 seeds: 0.353 to 0.424). Replace the winner assert with a tie: `abs(frequencies["Airport Road"]["1"] - frequencies["River Bend"]["1"]) < 0.08`. Say "tied for first" in the text. Run a second, disjoint block (a second seed) in the cell, as `CONFIDENCE.md` asks.

### C2. Cells 17 and 19: "near the stated ones" is false, and the Limit's finding is the sampler's

Cell 17: "`monte_carlo` draws 2,000 weight sets near the stated ones." Cell 19 repeats it in the Handled row.

`sensitivity.py` sets `alpha = original_weights * n_criteria`, here `[1.2, 1.2, 0.8, 0.8]`, sum 4. A uniform draw over the simplex is `[1, 1, 1, 1]`.

```
stated weights [0.3 0.3 0.2 0.2] | mean of draws [0.299 0.303 0.2 0.198] | sd of draws [0.205 0.212 0.18 0.175]
5th..95th percentile of each drawn weight: (0.033, 0.68), (0.033, 0.698), (0.007, 0.572), (0.008, 0.547)
draws with every weight within 0.05 of its stated value: 7 of 2000
draws with some weight under 0.02: 522 of 2000; draws where some criterion takes over half: 1047
uniform on the simplex for scale: sd [0.199 0.191 0.198 0.194]
```

The draws centre on the stated weights and range over nearly all weights. The result the Limit reports depends on that width. The same question with `alpha = weights * k`, 20,000 draws, seed 7:

```
concentration    4 (sd of a 0.30 weight 0.205): first-place share Airport Road 0.391, River Bend 0.395
concentration   20 (sd of a 0.30 weight 0.099): first-place share Airport Road 0.677, River Bend 0.256
concentration  100 (sd of a 0.30 weight 0.045): first-place share Airport Road 0.940, River Bend 0.060
```

With weights that stay within about 0.05 of the stated ones the leader holds in 94% of draws and `robustness_report` would say robust. "Here it does not hold" is true of weights drawn from almost anywhere, which is a different finding.

**Fix, notebook.** Cell 17: "`monte_carlo` draws 2,000 weight sets centred on the stated ones and spread nearly as wide as a uniform draw: a 0.30 weight is drawn with a standard deviation of 0.2." Print and assert that spread in the cell. Give the Handled row its condition: "first in 35% to 42% of draws across 200 seeds, under the package's fixed spread". The Limit's point survives: the package cannot say which weights are right. Its evidence becomes "if the owners' weights are no better known than that, the leader is a coin toss between two sites".

**Defect to file (product, not changed here).** `monte_carlo` has no concentration parameter, and its docstring says the distribution "clusters near the original weights". `docs/reviews/20260326_decision_science_quality_review.md:207` records "The Dirichlet alpha scaling is well-designed"; the measurement above contradicts that record. Task: add a `concentration` argument with today's value as the default, correct the docstring, test first.

### C3. Cell 11: the source misdescribes its record

Cell 11: "Incident: commit `acdab6e`, 2026-11-14, found by running the tour's cells while building it."

The quotation is exact. `git show acdab6e` holds, across one line break, "A rate under about 2.2e-16 raised ZeroDivisionError, and at 1e-12 the denominator's cancellation returned a wrong utility without raising." Word for word the same.

The sentence around it is not what the records say:

- `docs/doctrine-updates.md:1681-1686`: "`value_functions.exponential()` raises `ZeroDivisionError` for nonzero `|rate|` below ~2.2e-16 ... Found during property-test strategy design, 2026-07-20. The upstream fix is pending a design call".
- `docs/sessions/20260720_prose_doctrine_hypothesis_relicense.md:55-57`: "Strategy design alone surfaced a real crash ... Filed with repro".
- `docs/reviews/20260814_whetstone_research_archaeology.md:26`: "fix still open at 25 days".
- `docs/plans/20261114_notebook_tour_proposal.md:62`: "Preparing for the tour found a crash and a silent wrong answer".

So the crash was found on 2026-07-20, shipped to downstream repos as a Known Issue, and fixed 117 days later. No record says a tour cell found anything: the tour's model carries `rate: 2.0`, the only rate in a tracked YAML file, and `acdab6e` precedes the tour's commit. The silent wrong answer first appears in the record on 2026-11-14.

Evidence: `git grep -n -i -E "acdab6e|ZeroDivisionError|tiny.rate|1e-12" -- docs` returned 12 lines in 7 files, the four above among them; `git grep -n "rate" -- '*.yaml' '*.yml'` returned 1 line, `tests/fixtures/tour/depot_model.yaml:12`.

**Fix.** "Incident: the crash was found on 2026-07-20 while a property-test strategy was being designed (`docs/doctrine-updates.md`, Known Issue), and stayed open 117 days. Commit `acdab6e`, 2026-11-14, fixed it and records the silent wrong answer: "..."." Keep the quotation. The commit's date is 2026-11-14 at its own offset of -0600 and 2026-11-15 in UTC; say "2026-11-14 (-0600)" or drop the date.

### C4. Cell 23: the own-data cell reports clean after checking nothing, and scores costs backwards

Hand runs in the clone, with `MY_MODEL` and `MY_ALTERNATIVES` set in cell 23 and the depot model as the model unless stated:

| Input | Printed |
|---|---|
| The committed fixtures | `leader, the package: Airport Road   leader, naive scaling: Rail Yard` / `withdrawing one of these changes the naive leader: ['Old Mill']` / figure with 5 axes |
| One site | `withdrawing one of these changes the naive leader: none`, then four `largely unspent:` lines, one per criterion, each with range 0.000 |
| Two sites | `leader, the package: River Bend   leader, naive scaling: Rail Yard` / `withdrawing one of these changes the naive leader: none` |
| Four invented sites (`crude_says_none`) | `... changes the naive leader: none`, where case 2's rule changes the leader when site B withdraws |
| Four invented sites (`crude_says_flip`) | `... changes the naive leader: ['C']`, where case 2's rule changes nothing |
| A missing criterion value (refused) | `ValueError: raw_scores is missing criterion values: ['flood_free_years']` |
| A NaN value (refused) | `ValueError: Value function for 'flood_free_years' returned nan, which is outside [0, 1] (input was nan)` |
| A string value | `TypeError: unsupported operand type(s) for -: 'str' and 'int'` |
| `alternatives: {}` | `ValueError: No alternatives to rank` |
| No `alternatives` key | `KeyError: 'alternatives'` |
| A cost of `.inf` (the scorer accepts it) | both leader lines and `none`, then `ValueError: Axis limits cannot be NaN or Inf` from `passage_chart` |
| A model naming `os.system` as its value function | `ValueError: Unknown value_fn 'os.system'. Valid options: [...]` |
| A model with a `!!python/object/apply` tag | `ConstructorError`; the command did not run (0 marker files) |
| A URL as the model path | `FileNotFoundError: ... 'https:/example.invalid/model.yaml'`; nothing fetched |
| `tests/fixtures/decision_model.yaml` with the depot sites | `ValueError: raw_scores is missing criterion values: [...]` |

Three faults:

- **"none" with nothing examined.** The comprehension carries `len(mine) > 2`, so with one or two alternatives no withdrawal is tried and the cell prints "none". `TOURS.md`: "It never reports clean ... states how many items it looked at, and the cell stops after a count of zero." The rollout ruled the same fault Critical in another notebook.
- **The naive rule is not case 2's.** It treats every criterion as more-is-better. Over 5,000 random four-site inputs under the depot model, its leader or its flip line differs from case 2's rule in 4,635. The text admits "cruder", and then says the cell "asks cases 2 and 4 of your data". It does not ask case 2 of any model with a cost criterion. The direction is in the model already: `passage_chart` reads it as `curve[0] > curve[-1]`.
- **No confidence doubt.** `TOURS.md` asks a case notebook's own-data cell to run the confidence section's doubt on the reader's data or say it cannot. The cell and its text do neither.

**Fix.** Stop with a message under three alternatives. Print the count: "tried N withdrawals; M change the naive leader: [...]". Flip a criterion whose value function falls between the lowest and highest value present. Add one line on the doubt, or a sentence that the cell cannot run it. Lesser points are under Notes.

Safe as built: it reads two local files through `yaml.safe_load`, looks value functions up in a fixed table, executes nothing a reader supplies, fetches nothing, and writes nothing.

## Warning

### W1. Cells 19 to 21: both confidence results belong to the fixture or to the chosen range

Evidence, in the clone:

```
margins 1-2 0.06691, 2-3 0.00409, 3-4 0.05150
River Bend's place by flood-free years 0..30: 3333333333333333333222221111111
  19 give or take 4: leaders ['Airport Road'], River Bend places [2, 3]
  19 give or take 5: leaders ['Airport Road', 'River Bend'], River Bend places [1, 2, 3]
Rail Yard cost 880: margin 2-3 0.054; River Bend places over 16..22: [2, 2, 2, 2, 2, 2, 2]
all four records, each give or take 3 (capped at 30): 1372 combinations; leader counts {'Airport Road': 1372}; distinct orders 3
swing over 16..22 0.0502; leader's margin 0.0669
```

- **"Second place does not survive" belongs to the fixture.** River Bend's 19 years is the lowest count at which it places second. Any downward error at all swaps it. With the second-to-third margin at 0.054 the same doubt swaps nothing. `CONFIDENCE.md`: "Run the doubt on two fixtures, one on the boundary and one off it, or say where the fixture sits."
- **"The leader survives" belongs to the width of an invented range.** It holds to plus 4 years and fails at plus 5. Cell 21's "who leads does not depend on River Bend's flood record" is false at 24 years.
- **The method does give a result**, and the notebook does not state it: one input can move a total by at most its weight times the utility swing across the doubt, here 0.050 against a lead of 0.067. That holds with all four flood records moved together, 1,372 combinations.

**Fix.** Cell 21: "Within three years either way the leader holds, because the doubt can move River Bend's total by 0.050 and the lead is 0.067; at five years more it does not. Second and third swap because the fixture puts River Bend one year above the boundary." Assert the bound and the 1,372-combination result. Name the direction that costs more, or say that is the owners' call.

### W2. The fixture sits on several boundaries at once and the notebook does not say so

One fixture value moved one step (cost 20, minutes 1, pallets 100, years 1), 31 fixtures, in the clone:

```
one value moved one step: 31 fixtures; notebook passes whole in 13; failures by cell {15: 2, 18: 9, 20: 12, 4: 5, 9: 3}
row order of the four sites: 24 orders, notebook fails in 0
```

Cases 1 and 3 never fail. The confidence cell fails in 12 of 31, the Limit in 9, case 2 in 3. `CASES.md`: "A fixture tuned until it shows an effect says so." Cell 0 says only "All are invented."

**Fix.** One sentence in cell 0: the four sites were chosen so that second and third are 0.004 apart, the naive lead in case 2 is 0.005, and River Bend sits one year above a boundary; the cases show that each effect can happen, and no count of how often.

### W3. Case 1: the first cited test passes under the naive rule

In the clone, `u = c.value_fn(raw_scores[c.name])` replaced by `u = raw_scores[c.name]`:

| Command | Last line |
|---|---|
| `pytest tests/unit/test_scorer.py -k "test_additive_aggregation or test_bad_value_function_raises"` | `1 failed, 1 passed, 48 deselected in 0.10s` (the pass is `test_additive_aggregation`) |
| `pytest tests/unit/test_scorer.py` | `4 failed, 46 passed, 1 warning in 0.25s` |
| `pytest` (whole suite) | `22 failed, 666 passed, 1 warning in 21.47s` |

`test_additive_aggregation` scores raw 0.5 through `linear` from 0 to 1, where utility equals the raw number. **Fix.** Cite `test_from_yaml_rank` (it fails under the swap), or write a test whose value function is not the identity.

The other cited tests hold their rules:

| Swap, in the clone | Cited test | Last line |
|---|---|---|
| Refusal outside 0 to 1 removed | `test_bad_value_function_raises` | `1 failed, 49 deselected in 0.10s` |
| `rank` rescales to the alternatives present | `test_a_utility_does_not_depend_on_which_other_alternatives_are_ranked` | `1 failed, 49 deselected in 0.10s` |
| The linear branch removed (differs from `acdab6e^` by 4 comment and docstring lines) | `test_tiny_nonzero_rate_approaches_linear` | `4 failed, 1 passed, 58 deselected in 0.12s` (the pass is `-1e-12`) |
| The warning removed | `test_warns_when_utility_range_is_narrow` | `1 failed, 49 deselected in 0.09s` |

### W4. Case 3: the record's threshold is wrong, the table skips the worst band, and the case stops short of the report

The naive cell equals the code at `acdab6e^` on 20,000 random inputs (0 differ). Across rates, 50 minutes on 90 down to 10:

```
    1e-15  0.5555555555555556
  1.5e-16  1.0
    1e-16  0.0
  5.6e-17  0.0
  5.5e-17  ZeroDivisionError
worst silent pre-fix error at t=0.5 below 1e-8: 0.500 at rate 1.66e-16
largest positive rate that raises: 5.546e-17
largest negative-rate magnitude that raises: 1.109e-16
```

- The quoted "under about 2.2e-16 raised ZeroDivisionError" is refuted. A positive rate raises only at 5.5e-17 and below. Between there and about 3e-16 the old code returned 0.0, 1.0 or 0.333 for a true 0.5, with no error. The comment in `value_functions.py` and the one in `test_value_functions.py` repeat the figure.
- Cell 13 calls 0.556 at 1e-15 the quiet failure. The quiet failure is ten times larger at 1e-16, a rate the table omits.
- `CASES.md` asks for a rule whose alternative "changes what the product ships, on a committed fixture". The case shows one utility. It can reach the ranking: with the depot model's drive-time rate set to 1e-15, the old code ranks `Airport Road, Rail Yard, River Bend, Old Mill` and today's ranks `Airport Road, River Bend, Rail Yard, Old Mill`.

**Fix.** Add 1e-16 to `RATES` and assert `naive_at[1e-16] == 0.0`. After the quotation add: "Measured here, the crash begins at 5.5e-17; from there to 3e-16 the old code returned 0 or 1 without raising." Add the two rankings as a two-row table.

Cell 13 also says a small rate reaches a model "never from a person typing one". Nothing in the cell checks what people type. **Fix:** "A rate this small comes from a fitted parameter or an optimizer's step."

### W5. Case 2: no table, no assert on the figure, and a naive lead of 0.005

Cell 9 prints nothing. Its numbers exist only inside the figure:

```
naive_four  {'Rail Yard': 0.605, 'River Bend': 0.6, 'Airport Road': 0.547, 'Old Mill': 0.27}
naive_three {'River Bend': 0.6, 'Rail Yard': 0.575, 'Airport Road': 0.417}
```

`DISPLAYS.md`: "A figure whose numbers appear nowhere as text fails the second reader. Print the table." The headline, "the naive leader changes", rests on a lead of 0.005, the size of margin the confidence section tells the reader not to believe. The larger effect is in the same data: Airport Road falls from 0.547 to 0.417 and nothing about it changed.

**Fix.** Print the four rows with `table()`. Add `assert len(withdrawal.axes) == 2`. Lead the closing text with Airport Road's fall of 0.130 and give the leader change second, with its margin.

### W6. Numbers in the text that no assert pins

- "38%" (cell 19). Of the 98 seeds in 100 to 299 where all of cell 18's asserts pass, 53 print a different share (37% or 39%, for example).
- "0.696 against 0.692" and "0.004" (cells 19, 21); "0.556" (cell 13); "0.030 out of a possible 0.300" (cell 16). True today (measured: 0.69604, 0.69194, 0.00409, 0.5556, 0.030) and held by no assert.
- The Handled row is labelled `estimated` and gives no range, basis or falsifier. It also holds two doubts of different kinds, the weights (estimated) and the curve shapes (not known: nothing varies them). `CONFIDENCE.md` asks for two rows.
- The Arrives row is labelled `not known` and then gives a size. By `CONFIDENCE.md` a size from invented values is `measured over an assumed range`, and the real size is `not known`.

**Fix.** Assert each number to the places printed, or build the sentence from the value. Split the Handled row.

### W7. Case 4: no test holds the 0.2 in "warns when that range is under 0.2"

In the clone, `util_range < 0.2` changed to `< 0.15`: `pytest` printed `688 passed, 1 warning in 25.49s`. Changed to `< 0.05`: `2 failed, 686 passed`, both failures the notebook itself. **Fix.** A boundary test in `tests/unit/test_scorer.py` (0.19 warns, 0.21 does not), written first; then cite it.

### W8. `passage_chart` (rendered from cell 4 to `out/passage.png`, 2300 by 800, and read)

Pass 1, content: 36 numbers (16 measurements, 16 utilities, 4 totals), so a figure is warranted. The comparison is one site across panels and it reads. Findings:

```
[Major] Rule 4: in the total panel River Bend's point (0.696, full ink) lies under Rail Yard's (0.692, grey).
        Centres 0.62 pt apart, each dot 4.2 pt wide, both zorder 3, drawn in rank order.
        Cell 3 tells the reader to follow River Bend, and its last mark is hidden.
Redraw: draw quiet items first and highlighted items last (zorder 2 and 3), as slope_chart does.

[Minor] Rule 4: in drive_minutes the grey label "Rail Yard" is crossed by the grey curve
        (16 of the curve's 101 points fall inside its box); "Airport Road" by 6, "Old Mill" by 3.
Redraw: offset a label perpendicular to the curve (above-left on a rising curve), or flip its anchor.

[Minor] Rule 7: no unit for annual_cost on the figure; the other three carry theirs in their names.
Redraw: accept a units mapping, or have the notebook pass display names ("annual cost, $k").

[Minor] Rule 8, datum to add: each x axis spans the sites present (780 to 340), so the model's own scale
        (900 to 300) is not shown. Case 2's point is that the scale is the model's.
Redraw: tick the model's low and high where the value function has them.

[Minor] Rule 2: the plotted utilities appear nowhere as text; cell 4's table prints weight times utility.
Redraw: add a utility table to cell 4, or print raw_utilities.

[Minor] Title: "Four depot sites, from raw measurement to utility to total" names the chart.
Redraw: "River Bend is best on cost and drive time, near the floor on flood years, and finishes second".
```

Passing: no legend; 5 axes; panel widths 223, 223, 148, 148 px (ratio 1.507 against 1.5); one utility scale, -0.04 to 1.04, in every panel (lie factor 1.0); source and "invented numbers" on the figure; no two labels overlap by text extents; smallest type 7 pt.

Defect to file: `passage_chart` raises `ValueError: Axis limits cannot be NaN or Inf` on an input the scorer ranks (a cost of `.inf`). Its docstring promises `ValueError` only when the scorer refuses.

### W9. `slope_chart` and `_spread` (rendered from cell 9 to `out/withdrawal.png`, 2080 by 880, and read)

The figure reads. The title states the finding, every item carries its value at both ends, both panels share one scale (0.230 to 0.897), there is no axis, grid or legend, and no labels overlap on this fixture.

```
[Major] Rule 4, in _spread: a group clamped to a bound is never merged again with its neighbour.
        _spread([0, 0, 0, 0.13], 0.06, 0.0, 1.0) -> [0.0, 0.06, 0.12, 0.13]: two labels 0.01 apart.
        20,000 random sets of 2 to 8 values drawn from {0, 1, uniform}: 1,636 place two labels closer than the gap.
        On a chart: slope_chart with five items at 0.0, one at 0.19 and one at 1.0 overprints
        'site E  0.000' and 'near  0.190' by 6.7 px of an 11.1 px line (316 columns searched).
Redraw: clamp inside the merge loop, or repeat the merge pass after clamping until nothing moves.
        Test first: the property "sorted positions differ by at least gap" over values tied at a bound.

[Minor] Rule 7: the note reads "Score from 0 to 1, both panels on one scale. tests/fixtures/tour, invented numbers."
        with no "Source:" label, and the drawn scale is 0.23 to 0.90. passage_chart adds "Source:" itself.
Redraw: slope_chart prefixes "Source: " as passage_chart does; the note says "one shared scale".

[Minor] Rule 4: in the right panel River Bend (0.696) and Rail Yard (0.692) draw as one thick line.
        The labels separate them. No redraw on one scale; "2 or 3" in the title would carry it.
```

`test_labels_in_one_column_never_overlap` checks one fixture. `passage_chart` has no overlap test.

### W10. README.md:97 contradicts the notebook

"four places where the obvious rule ranks the sites differently". Cases 1 and 2 rank the sites differently. Case 3 shows one utility and case 4 shows a share. **Fix:** "four places where the obvious rule gives a different answer".

The tour's "Where next" does not link the case notebook (`grep -c "cases_" notebooks/tour_from_a_model_to_a_ranking.ipynb` printed `0`), though `TOURS.md` lists the case notebooks among a tour's closing links.

## Note

- **N1, redundant conjuncts.** Cell 6: `naive_leader != leader` follows from the two conjuncts before it. Cell 9: `naive_leaders[1] != next(iter(repo_three))` follows from asserts above it. Negation kills both and neither can fail alone.
- **N2, cell 23.** `passage_chart` calls `rank` a second time outside the cell's `catch_warnings`, so each narrow-range warning reaches the reader twice. Error messages carry the reader's path or value, where `TOURS.md` asks for a message with no value. Setting one guard and leaving the other `None` does nothing and says nothing.
- **N3, format.** `nbformat_minor` is 5 and 0 of 25 cells have an `id`; the tour is 4.4. Format 4.5 requires ids. UNVERIFIED: what a front end does on open; no validator is installed. Set the minor version to 4 or add ids.
- **N4, cell 19's first line** does not say the section concerns invented data and no real output, which `CONFIDENCE.md` asks of it.
- **N5, cell 19.** `flood_free_years` "counts floods". The model file says it counts years with no flood.
- **N6, public repo.** A count-only match of the per-machine private-terms list against the notebook, `visualization.py`, `test_visualization.py` and the two fixtures gave 0 matching lines in each of the five files (list of 6 terms). Site names and numbers are invented and labelled so.
- **N7, prose.** 0 em dashes and 0 en dashes in the notebook's text cells. "Fix case 1 the usual way" (cell 8) uses a how-often word for a method's name; "the standard way" is no better; "by min-max normalization" is enough.

## Negation and Hermeticity

| Command, in the clone | Last line |
|---|---|
| The `ast` count from `TOURS.md` on the notebook | `28` |
| Each assert whole, each conjunct alone, each link of a chained comparison alone | `units negated: 47; killed: 47; survived: 0` |
| `TZ=UTC pytest tests/unit/test_notebooks.py tests/unit/test_case_notebooks.py` | `26 passed in 1.14s` |
| `TZ=Asia/Tokyo`, same | `26 passed in 1.16s` |
| `PYTHONHASHSEED=0`, same | `26 passed in 1.18s` |
| `PYTHONHASHSEED=1`, same | `26 passed in 1.15s` |
| `diff` of the 57 printed lines, UTC against Tokyo, seed 0, seed 1 | `identical` three times |
| Twenty runs | `runs printing '26 passed': 20 of 20` |
| `GIT_DIR` pointed at an empty scratch repository | `26 passed in 1.16s`; `commits before 0 after 0` |
| Row order of the four sites, 24 orders | `notebook fails in 0` |

47 is a floor. A negated assert that runs and is true always dies, so the count shows only that every assert executes.

## Knowledge Base

**Lineage.** Commit `acdab6e`: opened, quotation exact, history misdescribed (C3). Chain: `docs/sessions/20260720_prose_doctrine_hypothesis_relicense.md` (found) to `docs/doctrine-updates.md:1681` (Known Issue shipped) to `docs/reviews/20260814_whetstone_research_archaeology.md:26` (still open) to `acdab6e` (fixed) to `docs/sessions/20261114_notebook_tour_rollout.md:31` (recorded). The other three sources are `Design:` and name code and tests that exist; W3 covers which tests hold their rules.

**Surfaces.** `git grep -lE 'cases_how_a_ranking_goes_wrong|tour_from_a_model_to_a_ranking|passage_chart|slope_chart|test_notebooks|test_case_notebooks|test_case_notebook_module_port'` printed 23 of 264 tracked files. One more file names them and is untracked: the audit named under State on Arrival.

| Kind | Files |
|---|---|
| Living docs (a notice belongs here) | `README.md` (2 mentions); `docs/tasks.md` (3); `docs/gaps.md` (1); `docs/doctrine-updates.md` (7); `pyproject.toml` (1, a comment) |
| The skill | `.claude/skills/writing-tours-and-case-notebooks/SKILL.md` (7), `CASES.md` (1), `DISPLAYS.md` (3), `REVIEWING.md` (1) |
| The notebooks | `notebooks/cases_how_a_ranking_goes_wrong.ipynb` (8); `notebooks/tour_from_a_model_to_a_ranking.ipynb` (1) |
| Code | `src/myproject/decision_science/__init__.py` (4); `src/myproject/decision_science/visualization.py` (4) |
| Tests | `tests/unit/test_visualization.py` (20); `tests/unit/test_case_notebooks.py` (2); `tests/unit/test_case_notebook_module_port.py` (9); `tests/unit/test_notebook_module_port.py` (7) |
| Records (never rewritten) | `docs/plans/20261114_notebook_tour_proposal.md` (2); `docs/reviews/20261114_notebook_tour_preflight.md` (11); `docs/reviews/20261116_notebook_module_port_review.md` (4); `docs/sessions/20261114_notebook_tour_rollout.md` (1); `docs/sessions/20261116_case_notebooks_and_the_confidence_section.md` (5); `docs/sessions/20261117_case_notebook_update_in_detail.md` (10) |

Per name: the case notebook 5 files, the tour 7, `passage_chart` 8, `slope_chart` 8, `test_notebooks` 18, `test_case_notebooks` 9. `CLAUDE.md`, `CONTEXT.md`, `LANGUAGE.md` and `.claude/README.md` name none of them.

**Path resolution.** A script took every backticked path and markdown link in the 23 files and tested it against the repo root and the file's own folder: `total paths checked 369 missing 68`. Every path in the skill files, `README.md`, the case notebook and the 2026-11-16 session and review resolves (0 missing in each). The 68 are branch names (`topic/notebook-tour`, `origin/main`), other repositories, test-fixture strings, fractions read as paths in the tour's text, and old paths inside records. One is a broken pointer in a record: `docs/sessions/20261114_notebook_tour_rollout.md:53` names `docs/reviews/20261115_notebook_tour_review.md`, which lives on another repo's branch and says so.

**Contradictions.**

| Where | Says | The notebook |
|---|---|---|
| `README.md:97` | The obvious rule "ranks the sites differently" in four places | Two of four (W10) |
| `docs/doctrine-updates.md:1681-1686` | Crash found 2026-07-20 in property-test strategy design | "found by running the tour's cells" (C3) |
| `sensitivity.py` docstring; `docs/reviews/20260326_decision_science_quality_review.md:207` | Draws cluster near the weights; the scaling is "well-designed" | Repeats "near"; measured sd 0.205 (C2) |
| `docs/tasks.md:19-21`, `docs/gaps.md` G16 and G17 | The notebook has no second reader; own-data output is unchecked | No conflict. C4 is an instance of G17 |

KB-graph: backlinks of the six names, 23 tracked files; lineage of `acdab6e` back to the 2026-07-20 session; found the July record that contradicts cell 11.

## Where the Skill or the Test Module Was Wrong, Silent or Too Strict

**Wrong.**

- `TOURS.md`, Asserts: "a dead conjunct hides behind a live one", found by negating each conjunct. A true conjunct that runs always dies when negated. What hides is a conjunct implied by its neighbours (N1), and negation cannot find it. The rule should say: for each conjunct, name a state of the world in which it alone fails.
- `DISPLAYS.md`: a figure's tests "cannot see a label lying across a curve". They can: sample the curve, transform to pixels, and count points inside each label's text extent. That measure found 16 of 101 here.
- `CASES.md` says the module holds "fifteen things" and its table is cut by a blank line before the last row, so the fifteenth row renders as a loose paragraph.
- `CONFIDENCE.md` defines `measured over an assumed range`; the hub's own Arrives row, the skill's example, uses `not known` with a size.

**Silent.**

- **The width of a sampler.** "Say what the number is conditional on" is there. Nothing tells a builder to measure a product's "near" before repeating it. Add: print the spread of the draws beside any result drawn from them.
- **A library's random stream.** The hermetic table names the timezone, the hash seed and the clock. It does not name the version of the library that draws. Add a row: an assert over a seeded draw holds with margin across seeds, or the cell asserts only what does.
- **A hand-typed fixture on a boundary.** "Sweep its seeds" covers a generated fixture. A typed one has no seeds; moving each value one step is the same check, and here it failed 18 of 31.
- **How a record was found.** The quotation test proves the phrase is in the commit. Nothing sends a builder from a fix commit back to the first report. Add to `CASES.md`: search the docs for the fault's name before writing "found by".
- **A record that is itself wrong.** A quotation can be exact and false (2.2e-16). Add: re-measure any number a quotation carries, and print the measurement beside it.
- **A slopegraph and the two-row table.** `DISPLAYS.md` gives "two rules, several items, order matters" a slopegraph, and also says every case prints both answers as rows of one table. The hub's case 2 took the first and dropped the second. Say that the figure never replaces the table.

**The test module.**

- A cited test that passes under the naive rule is accepted (W3). `docs/tasks.md:20` already lists it.
- A number typed in a text cell is pinned by nothing (W6). A test could collect each decimal and percent in a section's text and require it in the cell's printed output; that would catch "38%" on the day the stream moves.
- `test_the_own_data_branch_runs_over_a_committed_fixture` passes over a branch that prints "none" after zero checks. G17 names this. A second probe with two alternatives, and a check that any line holding "none" also holds a digit, would catch this instance.
- `test_visualization.py` tests label overlap on one slope fixture and never for `passage_chart`.

**Too strict.** Nothing found. Every rule this notebook broke was a rule worth keeping.

## Claims

| Claim | State | Evidence |
|---|---|---|
| Suite passes on the committed tree | tested | `688 passed, 1 warning in 22.56s` |
| No survivor among 47 negated units | tested | `units negated: 47; killed: 47; survived: 0` |
| Output does not depend on timezone or hash seed | tested | three `diff`s identical, 57 lines |
| Cell 18's winner assert is luck | tested | 102 of 200 seeds; Philox and SFC64 fail it |
| "Near the stated ones" is false | tested | sd 0.205 against 0.199 uniform; 7 of 2,000 within 0.05 |
| Cell 11 misdescribes its record | observed | `docs/doctrine-updates.md:1681-1686` |
| Cell 23 reports clean on one and two alternatives | tested | hand runs above |
| `_spread` overprints at a bound | tested | 1,636 of 20,000; one chart with 6.7 px overlap |
| Scratch directory removed; repo holds one new file of mine | observed | `ls <scratch>/hub` fails; `git status --porcelain` lists this file and the audit that is not mine |
| Notebook opens in a front end | UNVERIFIED: no `nbformat` or `nbclient` installed, installs forbidden | |
