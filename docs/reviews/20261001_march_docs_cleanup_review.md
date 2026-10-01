# Review: March decision-science docs cleanup (cdec90f, 246052f, fa1a365)

**Author**: code-reviewer
**Date**: 2026-10-01
**Type**: Config review (doc commits plus one `[gate]` commit; non-author review under WHETSTONE D4)

> **Lead's note, added 2026-10-01 before this report was committed.** The three commits reviewed here never reached `origin`. At the user's direction the heading flagged in S2 was reworded, and the commits were rebuilt on the new `origin/main`: `cdec90f` became `7968ee0`, `246052f` became `eede414`, and `fa1a365` became `68486c9`. Rebuilding on the new tip took the place of the merge W1 asks for; the gate resolution is the one W1 specifies. W2 and W3 are applied (`eede414`, `2c24821`). The old SHAs below exist only in one machine's reflog. S2's quoted label is redacted in this file; nothing else in the report is changed.

## Verdict

**GO-WITH-FIXES.** The five files are safe to publish: no publication-safety hit. The three commits cannot be pushed as they stand, because `origin/main` has moved and the merge conflicts inside `/pcc` check 5. Fix W1 before the push. W2 to W4 can ride in a follow-up `[doc]` commit in the same push.

| Severity | Count |
|---|---|
| Critical | 0 |
| Warning | 4 |
| Suggestion | 4 |

Claims: 18 HOLD, 4 REFUTED, 1 UNVERIFIABLE (table at the end).

## 1. Publication safety

I read all five files in full at `fa1a365` (1,368 lines). Nothing in them should stay private.

- **Secrets, addresses, paths.** A grep for key, token, and password patterns, email addresses, URLs, IP addresses, home paths, the user's name, and the employer's name matched nothing (`grep` exit 1).
- **Work-system terms.** A whole-word, case-insensitive grep of 23 terms drawn from the gitignored `docs/design/hold/overwatch_sources.md` counted 0 in each of the five files.
- **People, employers, clients, datasets.** None named. The content is value-function math, test counts, and API design for `src/myproject/decision_science/`.
- **Repositories named.** Five, each already named in files tracked at `d1deddc` (`git grep -l <name> d1deddc | wc -l`, case-sensitive):

| Repository | Tracked files at `d1deddc` |
|---|---|
| quest-engine | 10 |
| tactics-game | 15 |
| agent-eval | 10 |
| elephant-graveyard | 14 |
| project-megan | 8 |

The files also name `pymcdm` (a public package) and "the utils library" (this repo's old name, already in `docs/tasks.md`). See S2 for one phrase that is new to the public tree.

## 2. Hashes

All five prefixes match the commit message. No file holds a CR byte, so `.gitattributes` normalized nothing, and each working-tree file hashes the same as its blob.

```
09fe3930f22c34f2  docs/plans/decision_science_gaps.md                             crlf=0 lines=523
495028a516912702  docs/reviews/20260326_decision_science_domain_audit.md          crlf=0 lines=251
acc4c090888bb075  docs/reviews/20260326_decision_science_quality_review.md        crlf=0 lines=218
8ad44b63af553d60  docs/reviews/20260326_decision_science_wave1_review.md          crlf=0 lines=232
75de5ee8e78cc998  docs/reviews/20260326_decision_science_waves_2_3_review.md      crlf=0 lines=144
```

The "before the move" half of the claim is UNVERIFIABLE: the untracked originals are gone. One thing corroborates it. `stat` shows all five working-tree files with modification times on 2026-03-26 (11:18 to 13:09). A move keeps the time; a rewrite would not.

## 3. The gate change

The removed line changes nothing for any other path. Its pattern is anchored at both ends (`^docs/(...)$`) and can match only three exact strings.

Both bash blocks of section 5, extracted from `git show fa1a365:.claude/commands/pcc.md` and run from the repo root:

```
=== block1 (file pass)      (no output)  exit=0
=== block2 (dir pass)       (no output)  exit=0
paths checked, file pass:   33
dirs checked, dir pass:     15
```

MISSING: 0. MISSING-DIR: 0. All six surfaces exist, so blind spot 3 does not apply.

- **Living docs.** No surface the check reads cites an old path: a grep of the five surfaces plus the Active section for the four old names and `decision_science_gaps` exits 1.
- **Copies of the line.** `git grep -F 'decision_audit_20260326\.md' fa1a365` finds none. `pcc.md` is the only file that holds the check's code.
- **Surrounding prose.** Coherent. The block comment's "Allowlist covers runtime artifacts that are legitimately absent" now describes the only allowlist line left. The "March-2026 case" comment is history and still true.
- **The check still fires.** One old path and one real path fed through the file pass printed `MISSING: docs/decision_audit_20260326.md`.

The check is clean on this tree. It is not the tree that will be published; see W1.

## Findings

### Warning

**W1. Local `main` has diverged from `origin/main`; the merge conflicts inside check 5.**

- Where: `.claude/commands/pcc.md`, section 5, the two lines directly above the removed line.
- What: the brief says `d1deddc` is `origin/main`. It is not.

```
$ git rev-parse origin/main d1deddc
952c7b37899fed1fad9864dc38144516974087cb
d1deddc44f082f8fdcf7c0aeecce24e6910e6258
$ git reflog show origin/main -2 --date=iso
952c7b3 refs/remotes/origin/main@{2026-10-01 17:43:37 -0500}: fetch: fast-forward
d1deddc refs/remotes/origin/main@{2026-10-01 17:40:11 -0500}: update by push
```

  The three commits are dated 17:46:01, after that fetch, and sit on `d1deddc`. `origin/main` carries eight commits `main` lacks, among them `dd5b023` (`[gate]`), which edits the same block: the extension bound goes from `{2,4}` to `{2,8}` and `upstream-lesson.md` joins the first allowlist line. Both sides change `pcc.md` and `docs/tasks.md`. A three-way `git merge-file` in scratch gives:

```
.claude/commands/pcc.md: merge-file exit=1      (one conflict)
docs/tasks.md:           merge-file exit=0      (clean; the old P3 line is gone, the Completed line is present)

<<<<<<< ours
  | grep -oE '(docs|...)/[A-Za-z0-9_./-]+\.[A-Za-z0-9]{2,4}' \
  | grep -vE '^\.claude/(upstream-update\.md|audits/)' \
=======
  | grep -oE '(docs|...)/[A-Za-z0-9_./-]+\.[A-Za-z0-9]{2,8}' \
  | grep -vE '^\.claude/(upstream-update\.md|upstream-lesson\.md|audits/)' \
  | grep -vE '^docs/(decision_audit_20260326\.md|plans/decision_science_gaps\.md|review_decision_science_waves_2_3\.md)$' \
>>>>>>> theirs
```

- Why it matters: the push will be rejected, and the conflict is resolved by hand on a gate surface. Taking "ours" silently reverts `dd5b023`. Taking "theirs" silently restores the March allowlist line. The gate commit's evidence ("33 paths", the `{2,4}` pipeline) describes a check that will not be the published one.
- Fix: merge `origin/main`. Resolve the hunk to theirs' first two lines and drop theirs' third. I built that tree in scratch (`git archive origin/main`, the five files, the merged `tasks.md`, the resolved `pcc.md`) and ran both blocks there:

```
=== merged file pass   (no output)  exit=0
=== merged dir pass    (no output)  exit=0
paths checked, file pass: 34
```

  After the real merge, re-run both blocks and `.venv/bin/pytest -q`, and put the new numbers (34, not 33) in the merge commit message or the session doc. The resolution is a gate-surface edit inside a merge commit; say so in the message so D4's lineage shows it. I have reviewed the resolution text above; a different resolution needs a second look.
- Not checked: whether the remote has moved past `952c7b3`. This review ran without network.

**W2. Two "never decided" statements are refuted: the weights bridge and bias A's guard shipped in March.**

- Where: `docs/tasks.md:60` ("its four bias items ... were never decided"); `cdec90f` message ("gaps A, C, and D shipped ... and the rest was never decided"); `246052f` message ("four bias items").
- What: the proposal ranks ten items. Five shipped in `1ed6d11` on 2026-03-26, not three.

```
$ git log --reverse -S'def from_weights' --format='%h %ad %s' --date=short -- src/myproject/decision_science/ | head -1
1ed6d11 2026-03-26 [util] Fix 3 bugs, add defensive guards and analysis features to decision_science
```

  `from_weights()` at `src/myproject/decision_science/scorer.py:278` is the proposal's rank-1 item (question 3, gap 4, the `weights.py` bridge). The range warning at `scorer.py:184-195` (`util_range < 0.2`, `warnings.warn`) is bias A's recommended option 2. The March session doc lists both (`docs/sessions/20260326_decision_science_module.md:63` and `:73`).
- Why it matters: `docs/tasks.md` is a living doc. A reader who files tasks from this line files one for work that already exists, and misses that the proposal's top item is done.
- Still open, by grep of `src/myproject/decision_science/` (no match for `allow_missing`, `direction`, rank reversal, or preferential independence): gap B, bias items B to D, and the three downstream gaps.
- Rewrite for `docs/tasks.md:60`: "Its gaps A, C, and D, its `weights.py` bridge (`from_weights()`), and bias A's range warning shipped in March (`1ed6d11`); gap B (rank reversal), bias items B to D, and its three downstream integration gaps were never decided and are not filed as tasks."
- The commit messages are records. Correct the claim in the session doc's Claims table instead of rewriting `cdec90f`, whose hash `docs/tasks.md` and `fa1a365` both cite.

**W3. A living skill still describes the allowlist that `fa1a365` removed.**

- Where: `.claude/skills/traversing-the-knowledge-base/SKILL.md:40`.
- What: "Expected output: empty (the 3 known-missing March paths are allowlisted pending their `docs/tasks.md` disposition)."
- Why it matters: the parenthetical is now false, and the skill ships downstream. It cites no path, so check 5 cannot catch it, and `fa1a365`'s "nothing in a living doc cites the old paths" holds only in that narrow sense.
- Fix: delete the parenthetical. `SKILL.md` is outside D4's gate-surface list, so a `[doc]` commit carries it. No test pins the sentence (`git grep` of `tests/` for "known-missing" finds nothing).

**W4. Four claims a reader will act on carry neither `Evidence:` nor `UNVERIFIED:`.**

1. `cdec90f`: "a grep of the five files for secret patterns, email addresses, URLs, and home paths printed nothing; the five repos they name are each named in at least 8 tracked files already." The probe is named; the command and the counts are not shown. (Both hold on re-run.)
2. `cdec90f`: "its gaps A, C, and D shipped on 2026-03-26 ..., and the rest was never decided." (Refuted in part, W2.)
3. `246052f`: "what was never decided ...: gap B, four bias items, and three downstream integration gaps. None is filed as a task." (Refuted in part, W2.)
4. `docs/tasks.md:60`: "whose nine findings were applied that day." (Holds.)

The two claims that failed are both in this list. Add the probes to the session doc's Claims table.

### Suggestion

**S1. "Open since March" is the files, not the task.** `246052f` says "The P3 task open since March". `git log --reverse -S'untracked March decision-science docs' -- docs/tasks.md` puts the line's first appearance at `e07b49c`, 2026-07-20, and `e07b49c^:docs/tasks.md` has no mention. The files date from March; the task from July. `cdec90f`'s "sat untracked ... for six months" is right. Nothing acts on this; do not repeat it in the session doc.

**S2. One phrase about `project-megan` is new to the public tree.** `docs/reviews/20260326_decision_science_wave1_review.md:191` gives it a two-word label [redacted by the lead, 2026-10-01]; a `git grep` for that label at `d1deddc` finds nothing. The repo name (a first name) and its sensor list (smile, giggle, distance, novelty) are already public at `docs/plans/decision_science_utility.md:366`. I do not rate this a publication-safety hit: it adds no identifier. The user knows whether that project's purpose should stay private.

**S3. A doctrine entry now tells adopters to drop a line that is gone.** `docs/doctrine-updates.md:635`: "Drop tacsop's allowlist line for the three March decision-science paths." The entry is a record; leave it. Say in the next entry that the hub removed the line, so an adopter copying section 5 has two edits to make, not three.

**S4. Record the M2 count after the merge.** `pcc.md` asks for each run's count in the session doc. The count that matters is the post-merge one (W1).

## 5. Convention

- **Names.** The four new names match `YYYYMMDD_<subject>.md` (`.claude/agents/code-reviewer.md:47`, `.claude/agents/decision-scientist.md:21`). Every file in `docs/reviews/` at `fa1a365` except `.gitkeep` matches `^[0-9]{8}_[a-z0-9_]+\.md$` (43 entries).
- **Old paths.** Three tracked files still mention them, all records: `docs/plans/20260813_kb_graph_traversal_proposal.md:33` and `docs/reviews/20260813_kb_graph_adoption_review.md:33` quote the old task line as their example of drift, and `docs/reviews/20261001_overwatch_kernel_wording.md:77-81` pastes a `git status`. None is a markdown link. No living doc cites an old path.
- **The kept name.** `docs/sessions/20260523_proword_convention_for_plans.md:27` cites `decision_science_gaps.md`, as `cdec90f` says.

## Prose and figures

No prose findings. The three commit messages and the tasks line state their point first, use no em dashes, and name files and numbers. The five March files are records and get no findings. No figures.

## Claim tally

| # | Claim | Result | Evidence |
|---|---|---|---|
| 1 | `cdec90f`: five reports untracked, tracked as a P3 task | HOLDS | `git cat-file -e d1deddc:<path>` fails for all five old paths |
| 2 | `cdec90f`: they are the "Team Review + Hardening" reports; the session doc summarizes nine findings | HOLDS | `docs/sessions/20260326_decision_science_module.md:46-48` |
| 3 | `cdec90f`: four renames; the plan keeps its name because a May session doc cites it | HOLDS | old names in `20261001_overwatch_kernel_wording.md:77-81`; `20260523_proword_convention_for_plans.md:27` |
| 4a | `cdec90f`: the committed files carry the five hashes | HOLDS | section 2 |
| 4b | `cdec90f`: the same hashes before the move | UNVERIFIABLE | originals gone; mtimes of 2026-03-26 corroborate |
| 5 | `cdec90f`: the publication grep printed nothing | HOLDS | section 1 |
| 6 | `cdec90f`: five repos, each in at least 8 tracked files | HOLDS | 10, 15, 10, 14, 8 |
| 7 | `cdec90f`: the status line reads "Proposed" | HOLDS | `docs/plans/decision_science_gaps.md:3` |
| 8 | `cdec90f`: gaps A, C, D shipped 2026-03-26 | HOLDS | `-S` for `dominance_check`, `robustness_report`, `explain` all give `1ed6d11` 2026-03-26 |
| 9 | `cdec90f`: "the rest was never decided" | REFUTED | W2 |
| 10 | `246052f`: the task moves to Completed; the line names the four paths | HOLDS | the diff |
| 11 | `246052f`: the task was open since March | REFUTED | S1 |
| 12 | `246052f`, `tasks.md:60`: four bias items never decided | REFUTED | W2: bias A shipped |
| 13 | `246052f`: none is filed as a task | HOLDS | Active-section grep finds no such task |
| 14 | `fa1a365`: the line existed with its own removal note | HOLDS | the diff |
| 15 | `fa1a365`: nothing in a living doc cites the old paths | HOLDS | section 3; but see W3 |
| 16 | `fa1a365`: check 5 clean, exit 0, 33 paths | HOLDS | section 3; 34 after the merge |
| 17 | `fa1a365`: the check still reports a missing path | HOLDS | `MISSING: docs/decision_audit_20260326.md` |
| 18 | `fa1a365`: 432 passed on Python 3.12.13 | HOLDS | `432 passed, 1 warning in 4.55s`, `exit=0`, `Python 3.12.13`; run with `-p no:cacheprovider`, tree status unchanged |
| 19 | `fa1a365`: the gate surface is alone in its commit | HOLDS | `git show --name-only fa1a365` lists `pcc.md` only |
| 20 | `tasks.md:60`: nine findings applied that day | HOLDS | session doc `:48`; `1ed6d11` 2026-03-26 |
| 21 | `tasks.md:60`: check 5 lost its second allowlist line in the same session | HOLDS | `fa1a365` |
| 22 | Brief: `d1deddc` is `origin/main` | REFUTED | W1 |
