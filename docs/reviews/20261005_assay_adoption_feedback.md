# Consumer report: `assay` adopts the common operating picture

**Date**: 2026-10-05
**From**: `assay` (work repo, `~/projects/gitlab/ops_research/assay`, titanx)
**Covers**: both 2026-10-04 doctrine entries, "The Common Operating Picture" and "The State Block Leaves the Config"
**Answers**: `docs/tasks.md` Focus item 1, "the hub then reads its lessons back"
**Consumer session record**: `docs/sessions/20261005_adopting_the_common_operating_picture.md` in `assay`

---

## Outcome

Both slices adopted in one session, on two topic branches, each through a `code-reviewer`
gate. Suite 651 to 728. Both Detect blocks print nothing; the rule-1 count went 3 to 0.

The repo was a hard case and that is why the report is worth reading. `config/project.yaml`
was 50,764 characters with 45,980 of them a `state:` block, and `known_issues` alone was
51 entries and 38,460 characters. The hub's was eight entries.

## 1. Correction 1 in the hand-delivery is wrong, and following it causes the failure it warns about

The note says `assay`'s package is flat, "`src/assay/`, with no `utils/` subpackage", and
prescribes `REGISTER = Path(__file__).resolve().parents[2]`.

**`src/assay/utils/` exists** and holds `logger.py` and `machine.py`. The correct landing
site is `src/assay/utils/gaps.py` with `parents[3]`, which is the hub's file copied
byte-identical, no edit at all.

Reproduced: at `parents[2]` the module resolves its register to a path one directory above
the repo root and five tests fail with `FileNotFoundError`. A reader who took the note on
trust and did not run the tests would ship a gap register that always passes because it
reads a file that is not there. That is precisely the silent-no-op failure the correction
was written to prevent.

**Suggested fix**: have the pre-delivery read state the measurement rather than the
inference. "`ls -d src/*/*/` in the target; set `parents[N]` so that
`REGISTER.parents[1]` is the repo root, and assert it in the test."

## 2. `FILLERS` misses "nothing exists", one word from its own documented filler

`src/myproject/utils/gaps.py` ships `FILLERS = {"tbd", "none", "none exists", "n/a",
"unknown", "nothing"}`. A reviewer asked to defeat the check produced `Nothing exists.` on
the first attempt, and it passes: `_says_nothing` strips to `"nothing exists"`, which is
not in the set, while both `"none exists"` and `"nothing"` are.

`assay` now ships a widened set. Carry back whichever of these you want:

```python
FILLERS = {"tbd", "none", "none exists", "n/a", "unknown", "nothing",
           "nothing exists", "nothing yet", "none yet", "no collector",
           "no collector exists", "not known", "not measured"}
```

## 3. Two register rows may share an ID, which makes every pointer at that ID ambiguous

Nothing in `problems()` checks ID uniqueness. A second row carrying `G1` passes, and rule
4's supersession pointer then names two rows. Four lines after the `rows = [...]` line:

```python
    seen: set[str] = set()
    for row in rows:
        if row["id"] in seen:
            found.append(f"{row['id']}: a second row carries this id; ids must be unique")
        seen.add(row["id"])
```

## 4. A bare file pointer is satisfied by the file existing, and that let two false records through

This is the one worth acting on fleet-wide.

`test_known_unknowns_live_only_in_the_register` asserts that `docs/gaps.md` appears on a
list item in the two commands. That shape, a pointer satisfied by mere existence, repeated
in `assay`'s migration: 28 `known_issues` entries were superseded in place, each prefixed
with where its open item had gone, and 18 of those pointers read `docs/tasks.md`.

The gate found that **two of the 18 named a move that had never happened**. The entries
said "the open item moved there" and nothing was there. Because the hub's own rule 8
protects a `known_issues` entry as a record, both false sentences would have become
immune to correction the moment they merged.

The fix, now enforced in `assay`: a pointer into a file must quote the phrase it moved to,
and the phrase must occur exactly once.

```
SUPERSEDED 2026-10-05 by docs/tasks.md "Replace Wave 1's acceptance criterion"; ...
```

Also worth a line in the skill: `assay`'s register rows needed their own pointer test.
`closed 2026-10-05 by tests/unit/test_nothing_here.py` and `superseded 2026-10-05 by G99`
both passed the shipped checker.

## 5. The archive-only key, as an option for the `known_issues` move

Row 4 of the skill entry says to move the list and **delete the key**. In `assay` that
collided with its own `CLAUDE.md` rule 8: "A session doc, a review and a `known_issues`
entry are records of what was true when written, and rewriting them destroys the reasoning
they carry." Twenty-three of the 51 entries were closed history carrying the argument for
decisions still in force.

What `assay` did instead, offered as a second adoption mode rather than a correction:

- the key survives, promoted out of the deleted `state:` block, documented as closed
  history and not a status surface;
- all 51 entries keep their text, 23 untouched and 28 superseded in place;
- a test fails on any entry that does not open with `FIXED|SETTLED|CLOSED|SUPERSEDED|EXPLAINED`.

The two-homes drift pitfall 1 names is closed by making the boundary executable rather than
by emptying the file. **Known limit, accepted and recorded in the test**: a status word is
a declaration, so `SETTLED 2026-10-06: ... actually P1, OPEN` passes. No semantic check is
buildable, because every superseded entry legitimately quotes its own original `OPEN` text.

## 6. Score a mutation battery on the failure count. The hub's loop makes this trap easy

`ADOPTION.md` and the hub's narrative both say to mutate in a scratch export,
`git archive HEAD | tar -x -C <scratch>`.

**That export has no `.git`**, so a `git checkout -- .` revert between mutants silently
fails and mutations accumulate. In `assay` the first battery ran nine mutants that way, all
reported KILLED, and every attribution was worthless. This is pitfall 14's family (a shell
command that silently does not do what it looks like) and the fifth recorded recurrence in
that repo of "a silent no-op reads as a caught mutant".

Two more scoring rules were then wrong, in opposite directions:

| Scoring rule | Fails how |
|---|---|
| grep for the word `failed` | In a fresh clone `assay` runs `2 failed, 679 passed` because two tests need a gitignored config. Every mutant scores KILLED. |
| assert the exact baseline string `N passed` | A mutant that **deletes** a test returns `N-1 passed` and scores KILLED. |
| **count `^FAILED` lines against the extract's own baseline** | What works. |

Also worth adding to the loop: **assert the mutant applied**. A substitution whose anchor
has drifted writes nothing, the suite stays green, and that reads as SURVIVED rather than
as a battery that never ran.

## 7. Two smaller notes

**`_section` has no `None` guard.** A renamed heading raises `AttributeError` rather than
failing with a message. `assay` added `assert found, f"no '## {heading}' section"`.

**`DRIFTING_COUNT` does not catch what its motivating examples are.** The hub's docstring
cites README's "189 tests" and "53% coverage", which it does catch. But in `assay` the two
offenders were `CLAUDE.md`'s "There are ten of them" and `/session-start`'s "23 of 48
`known_issues` entries", and the regex matches **neither**: "ten" is a word, and "entries"
is not one of its count nouns. A consumer reading the docstring will believe the regex
covers the shapes that motivated it.

`assay` added a stricter `FOCUS_COUNT` (word numerals plus a wider noun list) applied to
the Focus section only. **Do not apply it to `CLAUDE.md`**: word numerals turn it red on
rule 8's deliberately quoted bad example, "three hosts are still unswept". Tried and
reverted.

## What `assay` could not adopt, and why

`ORIENTATION` enforces `CLAUDE.md` and `.claude/README.md` only. `README.md`, `CONTEXT.md`
and `LANGUAGE.md` carry the project's own subject-matter measurements (a coverage bound, a
month table, token totals) rather than counts of the repo about itself, and no command
renders them on demand. They are an explicit `EXEMPT` list, with a test asserting that the
open task which would lift the exemption still exists, so the exemption cannot quietly
become permanent.

This may be general: a repo whose *product* is measurement has numbers in its orientation
surfaces that are neither drift nor repo-meta. The skill currently has no vocabulary for
them.

## Two hub tasks this bears on

- **P3, narrowing the plan-gate Detect grep.** `assay`'s run of that grep returned one hit,
  and it was a false positive of the same family you found: a parenthetical in an OPORD
  explaining that `Preconditions: suite green at 482` had been *removed*. A record of a
  corrected gate reads as a gate.
- **Focus item 2, propagating the unsent entries.** Items 1 to 4 above are each a one-line
  or one-paragraph change to the entries or to `gaps.py`, and all four were found by one
  consumer. Worth folding in before the cycle rather than shipping a correction after.
