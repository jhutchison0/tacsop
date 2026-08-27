# Review: Figure Style Doctrine Propagation, Pre-Flight

**Author**: code-reviewer
**Date**: 2026-08-27
**Type**: Config review (doctrine entry, lessons harvest, working-tree diff, copied skill bundle)

## Verdict

**GO-WITH-FIXES.** BLOCKER 0, HIGH 2, CONCERN 6, Minor 4.

The entry answers the five gate questions, batches per the 2026-07-20 precedent, uses civilian vocabulary, and names only files that exist. The hook patch parses (`bash -n`), the three tests pass, the full suite reports 272 passed, and the skill bundle is byte-identical to `stx-server` at `307d195` (its HEAD, working tree clean). Two claims in the entry are wrong by count and by status label; both fixes are one-line edits in three files. Nothing here needs a redesign.

## What was verified

| Claim | Method | Result |
|---|---|---|
| Every path in the entry and harvest exists in the hub | `ls` on 34 paths | All present |
| Skill bundle: five files, 409 lines, no repo names | `wc -l`, `grep -i` for stx-server/tacsop/veil/tactics/fll | 409, zero repo names |
| Skill bundle byte-identical to stx-server | `diff -r` | Identical; stx-server HEAD is `307d195`, status clean |
| `writing-simple-and-direct` 1.0.1, `designing-clear-data-displays` 1.1.0 | frontmatter | Both correct |
| `tools:` lines on proposer and code-reviewer | grep | Both carry `WebSearch, WebFetch` |
| CLAUDE.md Figure Style block equals ADOPTION.md step 1 block | `diff` | Identical |
| Hook exec bit | `git ls-files --stage` | 100755 |
| Hook syntax | `bash -n` | Clean |
| Hook tests | `.venv/bin/pytest tests/unit/test_shift_left_hook.py -q` | 3 passed |
| Full suite | `.venv/bin/pytest -q` | 272 passed, 1 warning |
| Hook run on `src/myproject/utils/math_utils.py` and `src/myproject/math_utils.py` | stdin JSON payload | exit 0, `OK_TEST_EXISTS partner=tests/unit/test_math_utils.py` for both |
| Hook run on a throwaway path in an existing directory | same | exit 0, `MISSING_TEST` logged, stderr warning |
| Hook run on a path whose directory does not exist | same | exit 0, nothing logged |
| Em dashes in the entry (lines 7 to 175) | grep | Zero |
| Military vocabulary in the entry | grep for PCC, PCI, SITREP, OPORD, CONOP, TCS, wave | Only inside file names (`CONOP-FORMAT.md`, `OPORD-FORMAT.md`); "execution-phase" used in prose |
| First-person plural in the entry | grep | Zero |
| Harvest: 33 lessons, 32 fleet, 8 + 21 + 4, four repo-scope notes | count of numbered lines and section E bullets | Counts match; lesson 8 is the one `scope: repo` |
| Harvest evidence paths under stx-server | `ls` on 16 paths | All present |
| Harvest citations by label (HIGH-1/2/4, CONCERN-1/3/4, C2, C8, C9, D24, session lesson numbers) | grep in the stx-server docs | All resolve to the claimed content |
| stx-server: 8 session docs, 135 commits, no Step 5.5, three "Hub upward" task lines | `ls`, `rev-list --count`, grep | All match |
| Remaining em dashes in the four swept docs | grep with line numbers | All in headings, table cells, list-label separators, or the header template specimen |

## HIGH

### HIGH-1: The em-dash count is 27, not 26, and the README count is 3, not 2

`docs/doctrine-updates.md` line 125 ("26 replaced"), line 165 (`.claude/README.md ... 2 dashes`), `CHANGELOG.md` Fixed section ("26 in-sentence dashes"), and `docs/reviews/20260827_stx_server_lessons_harvest.md` lesson 6 ("26 in-sentence dashes") all carry the wrong number.

Measured from the diff (`git diff -U0 <file> | grep '^-' | grep -v '^---' | grep -o '—' | wc -l`): CONOP-FORMAT 9, OPORD-FORMAT 9, session-doc-format 6, README 3. Total 27. The README replacements are at lines 105, 143, and 149.

Why it matters: the entry is the downstream contract, and a maintainer who counts will find the hub's number wrong on the first check. The stx-server audit's own text (CONCERN-4) gives four example lines, not a count, so 26 has no source.

Fix: replace "26" with "27" in the three files; replace "2 dashes" with "3 dashes" at line 165.

### HIGH-2: Eight lessons carry `LEARNED` without meeting the D1 definition

`docs/reviews/20260827_stx_server_lessons_harvest.md`, Verdict paragraph and section A (lessons 1 to 8), and the legend line "`LEARNED` means applied in the hub this session."

WHETSTONE D1 (`docs/plans/conop_whetstone_recursive_doctrine_loop.md` line 105) defines `LEARNED` as "the artifact changed AND the change verified in use" and states "Only a human flips status." The harvest redefines the term to mean "applied this session." No hub artifact has been used with the change yet, and the human gate is this pre-flight, not the past. No prior hub session or review uses `LEARNED`, so this harvest sets the precedent for the greppable state machine.

Why it matters: E6 (upward lesson flow, latency to `LEARNED`) is a metric the CONOP intends to measure by grepping these lines. A redefined status corrupts the measure at its first data point.

Fix: label lessons 1 to 8 `IDENTIFIED` (routed to a named owner, artifact changed, awaiting the human's endorsement at session-end and one verified use). Delete the legend sentence that redefines `LEARNED`. Change the Verdict paragraph's "(LEARNED)" to "(IDENTIFIED; applied, awaiting verification in use)". The human flips them to `LEARNED` when the reviewer first produces a figure finding, the hook first logs a fallback `OK_TEST_EXISTS` in real use, and so on.

## CONCERN

### CONCERN-1: The hook's third import form matches only because of a GNU grep quirk, and no test covers it

`.claude/hooks/post-tool-shift-left-audit.sh` lines 87 to 89, the third alternative:

```
from ${module_parent} import .*([^a-zA-Z0-9_]|^)${module_leaf}([^a-zA-Z0-9_]|$)
```

For the plain form `from myproject import widgets`, only the `^` branch can match, and `^` mid-pattern is an anchor under POSIX ERE. GNU grep matches it anyway (verified: `echo ab | grep -E 'a(^|x)b'` returns 1 match, with and without `POSIXLY_CORRECT`). Python `re` returns False on the same pattern. A downstream on BSD grep (macOS) would silently lose the form that ENFORCEMENT.md step 4 and the entry's Part 3 both document.

`tests/unit/test_shift_left_hook.py` tests only `from pkg.mod import` (test 1). The documented `import pkg.mod` and `from pkg import mod` forms have no test.

Fix, hook line 88: replace `.*([^a-zA-Z0-9_]|^)` with `(.*[^a-zA-Z0-9_])?`. Verified: the rewritten pattern matches `from myproject import widgets`, `from myproject import thing, widgets`, `import myproject.widgets`, and `from myproject.widgets import thing`, and rejects `from myproject import widgetsx` and `import myproject.widgets_extra`, in both GNU grep and Python `re`.

Fix, tests: parametrize test 1 over the three forms:

```python
@pytest.mark.parametrize("line", [
    "from myproject.widgets import thing\n",
    "import myproject.widgets\n",
    "from myproject import widgets\n",
])
def test_feature_named_test_that_imports_the_module_counts_as_partner(tmp_path, line):
```

### CONCERN-2: `${file_path#*/src/}` strips to the first `/src/`, not the project's

`.claude/hooks/post-tool-shift-left-audit.sh` line 80. On a box where the repo lives under a path containing `/src/` (for example `/home/x/src/github/tacsop/src/myproject/foo.py`), `module_rel` becomes `github/tacsop/src/myproject/foo.py`, the dotted name is wrong, and the fallback never matches. The result is the same `MISSING_TEST` noise the patch exists to remove, with no signal that the derivation failed.

Fix: derive from the root the script already computed:

```bash
module_rel="${file_path#"$project_root"/src/}"
```

### CONCERN-3: The harvest routing table omits lessons 30 and 32, and lesson 32's owner is off-schema

`docs/reviews/20260827_stx_server_lessons_harvest.md`, Routing summary table and lesson 32.

The table's Lessons column covers 1 to 29, 31, and 33. Lessons 30 (`.claude/commands/pcc.md` check 6, NOOP) and 32 (owner `none`, NOOP) have no row. Lesson 12 names two owners (`from_template_to_project.md` and `shift-left-testing/CI.md`); the table lists only the first. D9 gives the owner field as `<artifact path or PARKED(n)>`; `none` is neither.

Fix: add two rows (`.claude/commands/pcc.md` | 30 | NOOP; `PARKED` | 32 | NOOP), append `CI.md` to the lesson 12 row, and change lesson 32's owner to `PARKED(32)` or to the artifact the reason names (`.claude/skills/writing-simple-and-direct/RULES.md`, rule 8 scope).

### CONCERN-4: SKILLS_FRAMEWORK.md's per-skill inventory lists 7 of 10 skills; CHANGELOG says the inventory was fixed

`.claude/skills/SKILLS_FRAMEWORK.md` `### <skill> (directory form)` sections: configuration-management, shift-left-testing, python-venv-management, maintaining-ubiquitous-language, maintaining-project-context, recording-architecture-decisions, designing-clear-data-displays. Missing: using-topic-branches, writing-simple-and-direct, traversing-the-knowledge-base. The directory tree at lines 340 to 365 now lists all ten; the inventory sections do not.

`CHANGELOG.md` Fixed: "`SKILLS_FRAMEWORK.md`'s inventory omitted `traversing-the-knowledge-base`. Both trees now match the directory." The first sentence names the inventory; only the tree changed. The doctrine entry (line 130) says "skills trees", which is accurate.

Fix: either add the three inventory sections (path, focus, key concepts, use when; the same shape as the new designing-clear-data-displays section) in this change, or reword CHANGELOG to "tree" and file the inventory gap as a task. The entry's Part 1 row 4 tells downstream to add an "Index entry"; the hub should model the complete index.

### CONCERN-5: Three em-dash replacements read wrong

Per REVIEWING.md severity mapping these are Minor prose findings; grouped here because the parent asked for them by name.

`docs/plans/CONOP-FORMAT.md` line 76: "is a risk being ignored, not a fact; and naming a risk while deferring its mitigation to 'a test later' is decoration, not mitigation." A semicolon before a coordinating "and" joins what the dash separated.
Rewrite: "is a risk being ignored, not a fact. Naming a risk while deferring its mitigation to 'a test later' is decoration, not mitigation."

`docs/plans/OPORD-FORMAT.md` line 60: "**End state**: what done looks like: code, tests, docs, config". Two colons on one line; the first is the list label.
Rewrite: "**End state**: what done looks like in code, tests, docs, and config".

`docs/plans/OPORD-FORMAT.md` line 126: "**Reporting**: where artifacts land: reviews to `docs/reviews/`, ...". Same double colon.
Rewrite: "**Reporting**: where artifacts land (reviews to `docs/reviews/`, proposals to `docs/plans/`, status via `/sitrep`, tasks in `docs/tasks.md`)."

The other 24 replacements state the relationship the dash implied; no finding.

### CONCERN-6: Gate question 3 (audience) is answered by implication only

`docs/doctrine-updates.md` lines 9 to 13. The protocol asks "All downstream repos, or a specific subset?" The entry says "All three are additive" and "each independently adoptable" but never names the audience. Part 2 has an opt-out ("Skip this part if your repo forbids network access"), and Part 3 row 11 is HUB-ONLY, so a reader may wonder whether Part 1 has a subset too.

Fix: add one sentence to the lead paragraph: "Audience: every downstream repo; Part 2 has one stated opt-out."

## Minor

- `docs/doctrine-updates.md` line 85: the Level 0 rule is quoted ("keep these agents unchanged; they should not accumulate project-specific knowledge") but `.claude/README.md` line 150 reads "Keep Level 0 agents (...) unchanged: they are portable across projects and should not accumulate project-specific knowledge." Either quote verbatim or drop the quotation marks.
- `.claude/hooks/post-tool-shift-left-audit.sh` line 87: dots in `${module_dotted}` are unescaped in the ERE, so `import myprojectXwidgets` matches `myproject.widgets` (verified). Escape once: `module_re="${module_dotted//./\\.}"` and use `$module_re` in the pattern. Low risk; noted because the fallback is now the hook's precision boundary.
- `docs/doctrine-updates.md` Part 3 verification step 2: when the payload path's directory does not exist, the hook exits 0 and logs nothing, so `tail -1` shows a stale line. Add "the path must exist" or "use a module you have" to the instruction.
- `docs/session-doc-format.md` line 3: "on 2026-05-19; the workflow stays at `.claude/commands/session-end.md`, this file holds the format details." The comma splice predates this change. Rewrite: "; the workflow stays at `.claude/commands/session-end.md` and this file holds the format details."

## Checks that passed without finding

- Evaluation Gate: Q1 (first sentence names the three parts), Q2 (a new Level 0 skill and a `SKILLS_FRAMEWORK.md` change are doctrine by the protocol's own examples), Q4 (three Action Required blocks, numbered where multi-step, imperative, full paths), Q5 (Rollback section, each part reversible by deletion).
- Batching: three-part shape matches the 2026-07-20 precedent; each part has its own table so a maintainer can apply one and skip another (Rule 2); the em-dash sweep and SCRIPTS.md line ride as trivial bumps (Rule 3); nothing breaks (Rule 4 not triggered).
- Authoring Tone: leads with verbs, numbered, before/after shown for the hook (the `if [ -z "$test_partners" ]` block is named), no session references, no "we".
- Part 1 table rows map to ADOPTION.md steps 1 to 4 correctly; step 5 (Propagation) is the entry itself.
- The hook exits 0 on all four probe paths; the audit log is gitignored, so the probe lines written during this review touch no tracked file.
- `docs/tasks.md` additions: the veil-engine harvest task points at a real file (`veil-engine/.claude/upstream-lesson.md`, 6 LESSON lines, dated 2026-08-22); the corrected March-docs task matches `git status`.
- Harvest KB-graph lines and References resolve; the six `20260827_*` stx-server reviews exist.

## Fix order

1. HIGH-1 (four numbers, three files), HIGH-2 (relabel 1 to 8, delete the legend sentence).
2. CONCERN-1 (one regex edit, one parametrize), CONCERN-2 (one line).
3. CONCERN-3, CONCERN-4, CONCERN-6 (table rows, CHANGELOG wording or three inventory sections, one audience sentence).
4. CONCERN-5 and Minor as time allows; none blocks propagation.

Re-run `.venv/bin/pytest -q` after the hook edit; expect 272 passed (or 274 if the parametrize adds two cases).
