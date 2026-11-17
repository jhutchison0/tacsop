# Tours, and What Every Notebook Owes

A tour is the breadth notebook: the repo's main path walked once, over small committed fixtures, from a raw input to a result a person can see. This file also holds the rules every notebook under `notebooks/` owes, since a case notebook keeps all of them.

The adoption steps, the mutant table and the tour module's commit history are in `docs/doctrine-updates.md` (the three notebook entries of 2026-11-14 and 2026-11-16). This file is the standing rule; those entries are the record of how it was reached.

## The Shape of a Tour

| Part | Holds |
|---|---|
| Opening cell | What the tour shows and what it does not; the fixtures by path, and that they are invented or public; the install line and the front end it expects |
| Path setup, then imports | Two cells, so a linter's import-order rule needs no suppression. An assert, with a message, that the fixtures are where the notebook expects |
| Numbered sections | One per step of the path, in the path's order. Each is a short text cell, then a code cell that ends in asserts |
| The three levels | Somewhere in those sections: one raw record printed whole, the same record after each step, and the report (SKILL.md, "Three Levels") |
| Hands on | A cell to change, a cell that fails on purpose and prints the real error, and a cell for the reader's own data behind a guard |
| Where next | Links: the case notebooks, the config, the tests that hold what the tour showed |

A tour takes one route. Where the path forks, it says so in a sentence and links to the case notebook or the test that covers the other branch.

## What Every Notebook Owes

**It runs in the suite.** Every code cell, in order, in one namespace, from `notebooks/`, with no kernel. Cells are plain Python: no `%` magics, no `!` commands, no top-level `await`, no `display()`. A cell may not skip itself.

**It is committed bare.** No outputs, no attachments, no widget state. An output saved from the own-data cell would publish the reader's data.

**Its fixtures say what they are.** Invented or public, small, committed, labelled in a comment or in the opening cell. A generated fixture ships its generator, unless it was written once and is edited by hand from then on. Where a repo's inputs are made through a tool (a git history, a database), literals in a cell that build a throwaway one are the committed form. No printed line carries an absolute path.

**Its figures come from the package.** The notebook imports no charting library. See `DISPLAYS.md`.

**Its kernel is its own extra.** `notebook`, holding `ipykernel` alone, left out of `all`.

**It passes the repo's own linter and formatter**, at the repo's line length. Where CI formats `tests/`, format the two copied test modules with it; the version in each module's docstring carries comparability with the hub, not byte equality. A repo that ignores `*.ipynb` adds an exception for each kind: `!notebooks/tour_*.ipynb` and `!notebooks/cases_*.ipynb`.

**It follows the repo's own rules.** A repo's `CLAUDE.md` may ask for a changelog line, a task row or a session doc, may reserve a word, or may forbid printing a reader's names. Where it conflicts with this skill, the repo wins and the notebook says so.

## Hermetic

Hermetic is more than offline. The rollout found each of these by a notebook breaking on it.

| A cell's result must not depend on | How it got in | The check |
|---|---|---|
| The network | A lazy first-use download; a name lookup | Block `socket.connect` and `socket.getaddrinfo` and run |
| An inherited `GIT_*` variable | A cell that runs `git` | Run with `GIT_DIR` pointed at a scratch repository; it gains no commit |
| A per-user cache, config file or installed-package metadata | A library's default location | Run with an empty `HOME` |
| **The host's timezone** | A library three calls down called `.timestamp()` on a naive datetime | Run under `TZ=UTC` and `TZ=Asia/Tokyo` |
| **The hash seed** | The product iterated a set of strings | Run under `PYTHONHASHSEED=0` and `=1` and diff the printed output |
| The wall clock, or how fast the machine is | A stamp of `now`; an age checked against a timeout | Set the clock in the cell; where a naive rule reads it, set both clocks |
| The order rows come back in | A store, a dict, a set, a glob | Return rows in a random order and compare printed output across runs |
| A patch from another cell | `patcher.start()` with a later `stop()` | Every patch is a `with` block inside one cell |

A host-dependent number is never pinned in a cell. Where a repo makes commits or timestamps, give each an explicit UTC offset. Every cell is safe to run twice.

A loop of twenty runs is a count. It cannot tell no dependence from a rare one; the shuffle and the two-value runs can.

## Asserts

Rule 6 of the kernel is the one a test cannot hold, and reviews found it broken more often than any other.

- Negate every assert, one at a time, and every conjunct of each `a and b` assert alone: a dead conjunct hides behind a live one. Report survivors. This is the only mechanical check, and it is a floor.
- Negation cannot see a true assert under a false sentence. For each section ask: would this assert fail if the sentence above it were false?
- **A word that says how often carries a count.** "Usual", "ordinary", "rarely", "about one in twenty": the cell prints and asserts the count, or the word goes.
- **"Nothing else changed" is asserted on what the report states** (a level, a rank, a pick) for every untouched item, not on an input to it.
- A claim about when a slip is invisible needs its own assert, on the near side of the threshold as well as the far side.
- A number a table states is pinned by an assert, or the table states only what the asserts hold. A loose band is called a tolerance, never an interval.
- An assert pins behaviour or a record, never a comment or wording in a file someone may improve.
- Where the package turns an exception into a warning, assert that the warnings are clean, or read them as the cell's subject. A test that expects an empty result also shows the thing it read was read.
- A sentence about which settings a notebook survives is a claim: change each one in a scratch copy and see.
- Count asserts from the syntax tree, so a builder's count and a reviewer's are one count:

```bash
python3 -c "import ast,json,sys; nb=json.load(open(sys.argv[1])); print(sum(isinstance(n,ast.Assert) for c in nb['cells'] if c['cell_type']=='code' for n in ast.walk(ast.parse(''.join(c['source'])))))" notebooks/<name>.ipynb
```

## The Own-Data Cell

The last section points the notebook at the reader's own data. It is where a notebook can do harm, and the suite never runs it.

- Its guards are committed as `None`, and `OWN_DATA_GUARDS` in the test module names them.
- It reads data and never executes a string the reader supplies. It writes nothing, except to a temporary store where the product reads only through its own store; the text says so and a clean-up cell removes it.
- **It accepts an existing local file and raises on anything else**, with a message that carries no value. Refusing strings that contain `://` is a deny-list, and a library's list of remote forms is longer. An `assert` there is dead code while the guard is off, and prints the value when it fires.
- **Every name the text tells a reader to change is a guard**, committed as `None` and listed in `OWN_DATA_GUARDS`, or a number with a stated default.
- **It prints the product's report and nothing the report withholds.** Build the report first; any number shown has passed every gate the product applies. One cell printed a score for a text the product's own report abstains on.
- Where a result depends on a reference fitted from the fixtures, the reader's data scored against it is wrong in a known direction. The cell takes the reader's own reference, fenced against the data under comparison, or stops before the score.
- It reads a format the product writes or reads, and the repo commits one file it accepts.
- **It never reports clean.** A line that says "none", "same" or "no difference" states how many items it looked at, and the cell stops after a count of zero. It compares by identity, never by a printed field two items can share, and reads every field the product reads.
- **It counts what it could not use.** A record the cell or the product refuses is counted and the count printed, never a value. Count stored results against inputs, not status codes: a request can succeed and write nothing.
- Where an answer depends on the time of a run, the reader supplies the run time, or the cell states which way its stand-in errs. A question about time is asked at every period the data holds.
- Where a naive rule depends on order, the cell tries each order of the tied rows, capped and counted.
- In a case notebook it compares the two rules' answers, never their counts, and runs the confidence section's doubt on the reader's data. Where it cannot, it says so.
- Its text tells the reader to close without saving, or to clear the output first.

The test module runs this branch once, each guard pointed at the committed file `OWN_DATA_PROBES` names, with output discarded. That catches a crash. It cannot see a wrong line.

**So before a notebook is committed, run this branch by hand** in a scratch copy: on each committed fixture, on one input the product refuses, on an empty input, and on an input built to break any bound the cell prints. Quote the outputs in the report. In ten reviews, most Criticals were in this cell, and a reviewer's hand run found each.
