# Review: Private-Term Gate (check 7, destination rule, OVERWATCH release draft)

**Author**: code-reviewer
**Date**: 2026-10-02
**Type**: Code review (gate surfaces, tests, release draft); non-author review under CONOP WHETSTONE D4

**Branch**: `topic/overwatch-private-terms`, `0f80aad..680f080`, five commits: `371b5b5` [gate], `37b4250` [infra], `e968dcc` [gate], `874b1d2` [test], `680f080` [doc].

**Method**. Every probe used an invented term (`zq-review-term-9182`). The real list at `~/.config/tacsop/private-terms` was touched only by count-producing commands; no term from it appears in this report. Scratch repos live under the session scratchpad. The hub tree was not modified: `git status --porcelain` printed nothing after the probes.

**Summary**. The check catches what it names: a term in the index, in any case, staged or committed, with a WARN when the list is absent. The tree is clean at every one of the five commits. But the branch's central safety claim, "the output names a file and a count, never the term", fails when the term is in a path name, and `pcc.md:118` then tells the reader to paste that path. Three more cases pass silently: a run from a subdirectory scans only that subdirectory, a term in an unpushed intermediate commit is not scanned, and `-I` skips binaries. The twelve tests pin the heading, the path, and the WARN branch well; they do not pin `--cached`, and the four rule pins hold a phrase that survives deletion or inversion of the rule's operative clause. One Critical, eleven Warnings, eleven Suggestions. Every fix is local to `pcc.md`, the test file, four prose surfaces, or the draft.

---

## 1. Check 7 probes

Block extracted from `.claude/commands/pcc.md:100-115` with the test's own regex (14 lines). Each case ran `bash check7.sh` in a fresh scratch repo holding one clean committed file, with `TACSOP_PRIVATE_TERMS` pointing at a scratch list. "Right" means right for a pre-push gate on a public tree.

| # | Case | exit | stdout | Right? | Output could carry a term? |
|---|---|---|---|---|---|
| 1 | Clean index | 0 | (empty) | Yes | No |
| 2 | Term committed as `ZQ-REVIEW-TERM-9182` (case differs) | 0 | `FAIL private term in: leak.md:1` | Yes | No |
| 3 | Term staged, not committed | 0 | `FAIL private term in: staged.md:1` | Yes | No |
| 4 | Term in an untracked file | 0 | (empty) | Yes: it is not pushed. Check 4 shows the file | No |
| 5 | List missing | 0 | `WARN: no private-term list at <list path>; check 7 did not run` | Yes | No: the list path, not a term |
| 6 | List of blank lines (`\n  \n`) | 0 | same WARN | Yes | No |
| 7 | List line ends CRLF, file is LF | 0 | `FAIL private term in: leak.md:1` | Yes. git's `-f` reader strips the CR (git 2.43.0) | No |
| 7b | CRLF list, CRLF file | 0 | two FAIL lines | Yes | No |
| 8 | Term `zq.review[term]`; files hold `zq.review[term]` and `zqXreview[term]` | 0 | `FAIL private term in: lit.md:1` only | Yes: `-F` holds | No |
| 9 | Term `zq review term` | 0 | `FAIL private term in: sp.md:1` | Yes | No |
| 9b | Same term with two spaces before and after it in the list | 0 | (empty) | **No.** Silent miss. The blank filter drops blank lines, not surrounding whitespace | No |
| 10 | Term `ant`; file holds "important and we want" | 0 | `FAIL private term in: words.md:1` | Acceptable: a false positive is safe, and the term categories (hosts, users, codenames, repo names) are rarely substrings. Document it | No |
| 11 | Term inside a binary file (NUL bytes around it), committed | 0 | (empty). Without `-I`: `blob.bin:1` | **No.** Silent miss. `-I` buys nothing: `-c` already prints path and count for a binary | No |
| 12 | Run from `sub/`; term is in `root-leak.md` at the root | 0 | (empty). From the root: `FAIL private term in: root-leak.md:1` | **No.** `-- .` is a pathspec relative to the cwd | No |
| 13 | Run outside any git repository | 0 | (empty); stderr `fatal: not a git repository ...` | Weak. stdout reads as clean; only stderr says otherwise | No |
| 14 | Term is a directory name: `zq-review-term-9182/readme.md` holds the term | 0 | `FAIL private term in: zq-review-term-9182/readme.md:1` | **No.** The term is in the output | **Yes** |
| 15 | Term only in a file name: `zq-review-term-9182.md` with clean content | 0 | (empty) | **No.** `git grep` reads content, not names | No |
| 16 | Term committed, then removed in the next commit; neither pushed | 0 | (empty). A per-commit scan prints `<sha>:hist.md:1` | **No** for a gate whose row says Block push: the push carries both commits | No |

Evidence: `bash scratchpad/probe.sh`, output as tabulated; `git --version` -> `git version 2.43.0`.

A corrected block (`scratchpad/check7_fixed.sh`, sketched under C1 below) ran against all sixteen cases and against this repo with the real list: cases 1 to 8 unchanged; 9b, 11, 12, 15, 16-with-upstream now FAIL; 13 WARNs; 14 prints `FAIL private term in 2 path name(s); not printed` and never the term; the hub prints nothing, exit 0.

## 2. Mutation test of `tests/unit/test_pcc_private_terms.py`

The seven surfaces (`pcc.md`, `README.md`, three agent files, the test) were copied to a scratch tree; each mutation is one edit to a fresh copy; `.venv/bin/pytest -q -c /dev/null --rootdir <scratch>`. Baseline `12 passed`. Against `main`'s copies of the five surfaces: `6 failed, 6 errors`, matching the red-state claim in `874b1d2`.

| # | Edit | Result | Caught by |
|---|---|---|---|
| M01 | drop `-i` | CAUGHT | test_committed_term... |
| M02 | drop `--cached` (working-tree scan) | **SURVIVED** | |
| M03 | drop `-F` | **SURVIVED** | |
| M04 | drop `-I` | **SURVIVED** | |
| M05 | drop `-- .` | **SURVIVED** | |
| M06 | `--untracked` instead of `--cached` | CAUGHT | test_untracked_file... |
| M07 | drop the `FAIL` prefix | CAUGHT | test_clean, test_committed, test_staged |
| M08 | drop the inner blank-line `sed` | **SURVIVED** (see S3) | |
| M09 | WARN branch never fires (`-eq 0` -> `-lt 0`) | CAUGHT | test_blank_only, test_missing |
| M10 | move the default list path | CAUGHT | test_default_list... |
| M11 | Quick Reference row -> Warn only | CAUGHT | test_quick_reference... |
| M12 | rename the section heading | CAUGHT | 1 failed, 6 errors |
| M13 | WARN printed twice | CAUGHT | test_missing_list... |
| M14 | `exit 1` after the grep | CAUGHT | test_clean, test_committed |
| M15 | scan `HEAD` instead of the index | CAUGHT | test_staged_term... |
| M16 | empty the block body (comments only) | CAUGHT | 5 failed; test_clean and test_untracked pass |
| M17 | code-reviewer: "owns" -> "holds" | CAUGHT | test_surface_carries_the_rule |
| M18 | code-reviewer: delete the second sentence (the operative clause) | **SURVIVED** | |
| M19 | code-reviewer: "never into this repo's" -> "always into this repo's" | **SURVIVED** | |
| M20 | README: "never into this repo's" -> "and also into this repo's" | **SURVIVED** | |

13 of 20 caught. No test is unfailable: each of the twelve failed under at least one edit. The weakest two pass on an empty block (M16): `test_clean_index_prints_nothing_and_exits_0` and `test_untracked_file_is_outside_the_index_and_not_scanned`. The second fails only if someone adds `--untracked`; it pins git's default, not the block's design. The third assertion of `test_committed_term_fails_naming_the_file_and_never_the_term` cannot fail with the fixture's file name; probe 14 shows the property it certifies is false in general.

Evidence: `.venv/bin/python scratchpad/mutate.py`, output as tabulated.

## 3. The four destination sentences

`.claude/agents/code-reviewer.md:68`, `proposer.md:63`, `decision-scientist.md:77`, `.claude/README.md:87`. Same rule, one noun swapped per role (material under review, material analyzed, model under audit, its input); same destination clause (that repository or the scratchpad, never this repo's `docs/`, whatever directory you run in). The README paragraph qualifies the matrix above it; it does not contradict it.

Operational? Not yet. "The repository that owns the sensitivity of its input" asks the agent to judge sensitivity and ownership. In the incident the input was a plan staged in `/tmp`; nothing in the sentence tells the agent which repository that plan belongs to, or what to do when it cannot tell. The scratchpad fallback is the operational half, but it is phrased as a destination, not as the default when the answer is unknown. See W7.

Unconditional write-to-docs instructions remaining: `.claude/README.md:116` (review reports go to `docs/reviews/`), `.claude/teams/feature-development.md:11,19` (proposal to `docs/plans/`), `.claude/teams/decision-science.md:11,12` (proposal to `docs/plans/`, findings to `docs/reviews/`). `SKILLS_FRAMEWORK.md` has none. See W8.

## 4. The draft entries (`docs/plans/20261002_overwatch_release_entries_draft.md`)

Evaluation Gate, five questions each (change, doctrine criteria, audience, action, rollback):

| Entry | Q1 | Q2 | Q3 | Q4 | Q5 | Rule 2 | Rule 4 | Notes |
|---|---|---|---|---|---|---|---|---|
| A | yes | cross-cutting, convention | yes | numbered | yes | ok | **co-mingles** (W9) | |
| B | yes | all three | yes | numbered | yes | open item 1 acknowledged; the F lesson rides along (S9) | n/a | result paragraph FILL |
| C | yes | all three | yes | points at ISOLATION.md steps | yes | ok | n/a | 3.11.15 figure (W10) |
| D | yes | cross-cutting, convention | yes | numbered | yes | ok | n/a | |
| E | yes | cross-cutting, convention | yes | numbered | yes | ok | n/a | |
| F | yes | all three | yes, narrow (S10) | numbered | yes | rows separable | n/a | timeline (W6); new mode word CREATE |
| G | placeholder | | | | | | alone, as required | cannot be gated until filled |

Claims re-run (all against this tree unless stated):

| Claim in the draft | Command | Output | Status |
|---|---|---|---|
| A: `tests/unit/test_session_start_checks.py` 9 pins | `pytest --co -q` | `9 tests collected` | HOLDS |
| A: merged `d98428a`, pinned `2a2e725` | `git show --stat` | both exist and touch the named files | HOLDS |
| A: Step 4 runs `.venv/bin/pytest`, three checks, Step 5 item 9 | `grep -n` | lines 62, 75-79, 104 | HOLDS |
| A: "blocked verification ... in 2 sessions" (:24) | grep CONOP and session docs | no source | UNVERIFIABLE (S11) |
| A Detect | `grep -c 'NO GIT IDENTITY'`; `grep -nE '^pytest\b'` | `1`; nothing | HOLDS |
| B: `verifying-claims` 1.0.0, SKILL.md 105 lines | `grep version`; `wc -l` | `1.0.0`; `105` | HOLDS |
| B: six-rule kernel, four states, five traps, seven pairs plus one clean report | grep | 6 numbered rules; 4 state rows; "Five traps the table cannot hold"; 7 numbered pairs plus "A clean report" | HOLDS |
| B: 26 tests, `ff0d8b2` | `pytest --co -q`; `git show --stat` | `26`; merge touches all listed surfaces | HOLDS |
| B: the six surfaces the tests read | grep paths in `test_verifying_claims.py` | CLAUDE.md, SKILLS_FRAMEWORK.md, code-reviewer.md, session-end.md, session-doc-format.md, README.md (`:212`), plus SKILL.md and EXAMPLES.md | HOLDS; row 8 wording (S8) |
| B: helper copies rows 1 to 4 (from 2026-10-02) | grep `adopt_doctrine.py`; `git log` | the four paths are in the copy list; `2840c0f 2026-10-02` | HOLDS |
| B: 16 refuted, user caught 0 (:75) | grep session doc | `:87` user 0; `:89` reviewer 16 | HOLDS |
| B Detect | four commands | `1`, `1`, `1`, no "skill missing" | HOLDS |
| C: `shift-left-testing` 2.2.0 at `d03e66a`; now 2.2.1 | grep; git show | `2.2.1` in tree; `d03e66a` touches SKILL.md | HOLDS |
| C: 43 tests | `pytest --co -q` | `43` | HOLDS |
| C: "308 existing tests ran armed with 0 catches" | source: `ISOLATION.md:103`; 1a gate review `:264` (325 minus 17) | measured 2026-09-30 | HOLDS as a dated figure |
| C: "the 43 tripwire tests pass on Python 3.11.15" | `git log -S'43 tripwire'` -> `5e7bcac` (the commit that took the file from 36 to 43 collected); last recorded 3.11.15 run: gate review `:397` `37 passed`; `uv python list` has no 3.11 | UNVERIFIABLE (W10) |
| C Detect | `grep -c 'tests.isolation' pyproject.toml` | `1` | HOLDS |
| D: `python-venv-management` 3.1.0, no `VIRTUAL_ENV=` line | grep | `3.1.0`; `0` | HOLDS |
| D: in-code hint P2 at the hub | grep tasks.md | `:59` | HOLDS |
| D Detect | the grep | nothing | HOLDS |
| E: three files carry the header; `d98428a` | grep -c; git show | `1`,`1`,`1`; touches all three | HOLDS |
| F: files list | `ls` | all six exist | HOLDS |
| F Detect | grep -c; test -s | `1`; list present | HOLDS |
| F: "The next day the record ... pasted ... committed and pushed" (:276) | `git log -1 --date=iso 5a04f2b`; `git reflog show origin/main` | author and commit `2026-10-01 17:40:46 -0500`; pushes to origin/main at 17:40 and 18:01 on 2026-10-01 | REFUTED (W6) |

Work-system or private names: `Nidhogg` at `:3` (S7). No term from the real list: the count grep at HEAD printed nothing. Military vocabulary: CONOP x4, TCS x4, OPORD x4, `/pcc` x5, wave x2 (S6).

## 5. The lead's claims

| Claim | Where | Command | Output | Status |
|---|---|---|---|---|
| `12 passed` | `874b1d2` | `.venv/bin/pytest tests/unit/test_pcc_private_terms.py -q` | `12 passed in 0.31s`, exit 0 | HOLDS |
| Red before: 6 failed, 6 errors | `874b1d2` | tests against `main`'s five surfaces in the scratch tree | `6 failed, 6 errors in 0.21s` | HOLDS |
| `445 passed`, with and without `CI=true` | lead's message | `env -u CI .venv/bin/pytest -q`; `CI=true .venv/bin/pytest -q`; `--co -q` | `445 passed, 1 warning in 5.08s` exit 0; `445 passed, 1 warning in 6.18s` exit 0; `445 tests collected` | HOLDS |
| Check 7 prints nothing on this tree | `e968dcc` | `bash check7.sh` at HEAD | no output, exit 0; list has 5 non-blank lines | HOLDS |
| Grep against `5a04f2b` yields 1 file | `e968dcc`, CHANGELOG, tasks | `git grep -c -i -I -F -f <list> 5a04f2b -- .` | `5a04f2b:docs/sessions/20261001_assay_bootstrap_and_agent_output_destination.md:1` | HOLDS |
| HEAD matches 0 files | CHANGELOG `:110`, tasks `:128` | same at `HEAD`, `0f80aad`, and each of the five branch commits | no output, exit 1, every time | HOLDS |
| Quick Reference row: Block push | `e968dcc` | grep | `:156` | HOLDS |
| Block exits 0 either way | `e968dcc` | probes 5, 6 | exit 0 | HOLDS |
| 70 deliveries | tasks `:127` | 16 notification files, mtime `20:10:00`; `grep -c '^## 2026-'` sums to 101; 15 of 16 are untracked in their repos; the format has no per-delivery stamp; paperboy's tracked diff shows 6 headings added since its last commit, which spans earlier cycles | cannot be reconstructed | UNVERIFIABLE |
| 15 repos | tasks `:127` | `find ~/projects -path '*/.claude/upstream-update.md' -newermt '2026-10-02'` | 16 files, all `20:10:00` | REFUTED (16) |
| 18 marks at 15 headings | tasks `:127` | `find ... doctrine-delivered`; `wc -l` each | 19 files; every one 15 lines | REFUTED on 18 (19); 15 HOLDS |
| fist, schelling-point, daily_weather up to date | tasks `:127` | mark line counts and mtimes; notification present? | 15 lines each; `20:08:38`, `20:08:38`, `10:22:31`; no notification file in any of the three | HOLDS |
| Five marks seeded first | tasks `:127`, `680f080` | the three above predate the run; propter and stx-server received one entry each, consistent with seeding | the run rewrote their marks at `20:10:00` | UNVERIFIABLE beyond three |
| Second incident dated 2026-10-02 | `pcc.md:104` | `git log -1 --date=iso 5a04f2b` | `2026-10-01 17:40:46 -0500` | REFUTED (W6) |

Discovery coverage: every `.claude/commands/` directory under `~/projects` at depth 2 has a mark; none is missing. The repos at `~/projects/cad/*` and `~/projects/sony/*` are top-level repos, not nested.

## 6. Gate-surface separation

| Commit | Files | Alone? |
|---|---|---|
| `371b5b5` [gate] | `.claude/agents/code-reviewer.md` | yes |
| `37b4250` [infra] | `README.md`, `proposer.md`, `decision-scientist.md` | n/a (not gate surfaces) |
| `e968dcc` [gate] | `.claude/commands/pcc.md` | yes |
| `874b1d2` [test] | the test file | yes |
| `680f080` [doc] | CHANGELOG, draft, tasks | yes |

Both gate surfaces are alone and tagged. `.claude/agents/code-reviewer.md` is a gate surface by the 2026-10-01 convention (`1edf0d4`, `1b50924`, the Wave 2 session doc `:59`, and this branch's `371b5b5`) and by the draft's own instruction to downstream (entry B row 6, entry F row 2). It is not in D4's deterministic path list (CONOP WHETSTONE `:108`) and check 6's regex does not match it: `echo .claude/agents/code-reviewer.md | grep -E '^\.claude/(hooks/|settings\.json|commands/(pcc|pci)\.md)'` prints nothing. See S5.

---

## Findings

### Critical

**C1. The output can carry a term, and `pcc.md:118` tells the reader to paste it.**
`.claude/commands/pcc.md:103` ("the output names a file and a count, never the term"), `:116-118`, `e968dcc`'s subject line, CHANGELOG `:101`, draft `:281`, and the test's docstring all make the claim. Probe 14 refutes it: a term in a directory name prints as `FAIL private term in: zq-review-term-9182/readme.md:1`. Line `:118` then says "Give the count and the path." One of the four term categories the check names is "sibling repo names", which is what file names in `docs/reviews/` carry (`YYYYMMDD_<subject>.md`). Following the instruction reproduces the `5a04f2b` shape. Probe 15 is the companion: a term only in a file name is not detected at all.
Fix, verified against all sixteen cases and the hub (`scratchpad/check7_fixed.sh`): collect the hits, count the ones whose path holds a term and print only the count, print the rest; add a `git ls-files --cached | grep -c -i -F -f <list>` line for names. Sketch:

```bash
hits=$(git grep -c -i -F -f <(printf '%s\n' "$clean") --cached -- ':/')
n=$(printf '%s\n' "$hits" | cut -d: -f1 | grep -c -i -F -f <(printf '%s\n' "$clean"))
[ "$n" -gt 0 ] && echo "FAIL private term in $n path name(s); not printed"
printf '%s\n' "$hits" | grep -v -i -F -f <(printf '%s\n' "$clean") | sed 's/^/FAIL private term in: /'
m=$(git ls-files --cached | grep -c -i -F -f <(printf '%s\n' "$clean"))
[ "$m" -gt 0 ] && echo "FAIL private term in $m tracked file name(s); not printed"
```

Then change `:118` to "Give the count and the path, unless the path itself is the hit." Add a test with the term in a path and assert the term is absent from stdout (the assertion that cannot fail today becomes load-bearing).

### Warnings

**W1. `-- .` narrows the scan to the current directory.** `pcc.md:112`. Probe 12: from `sub/`, a term at the root is missed; from the root it is found. Fix: `-- ':/'` (verified: prints `../root-leak.md:1` from the subdirectory).

**W2. The index is not what a push carries.** `pcc.md:106`, `:112`, `:116`; Quick Reference `:156` says Block push. Probe 16: a term committed and removed in the next commit, neither pushed, prints nothing; a per-commit scan prints it. Fix: scan `--cached` and each commit in `@{upstream}..HEAD`, falling back to HEAD when no upstream is set (verified, cases 16 and 17). Also reword `:106` and `:116`: `--cached` reads the index, not "HEAD plus staged"; a staged deletion drops HEAD's copy from the scan.

**W3. `-I` skips binaries and buys nothing.** `pcc.md:112`. Probe 11: with `-I`, a term in a NUL-padded file is missed; without it the output is `blob.bin:1`, path and count as before. Fix: drop `-I`. CHANGELOG `:101` already omits it.

**W4. Surrounding whitespace makes a term inert.** `pcc.md:109`, `:112`. Probe 9b: `  zq review term  ` in the list never matches. The filter deletes blank lines only. Fix: `sed -e 's/^[[:space:]]*//;s/[[:space:]]*$//' -e '/^$/d'` (verified).

**W5. The tests do not pin `--cached`, `-F`, `-I`, or the pathspec, and the rule pins hold a phrase, not the rule.** M02, M03, M04, M05, M18, M19, M20 survive. Fix: (a) a test with a tracked file whose index copy holds the term and whose working copy does not (catches M02); (b) a term with `.` and `[` in the fixture list (M03); (c) once C1 lands, a path-name case (M04 can wait); (d) on all four surfaces, pin "never into this repo's `docs/`" and "scratchpad" alongside the phrase (M18 to M20).

**W6. The second incident is misdated on a gate surface and in the draft.** `pcc.md:104` says "Two incidents, 2026-10-01 and 2026-10-02"; draft `:276` says "The next day the record of the containment pasted the five terms". `git log -1 --date=iso 5a04f2b` -> `2026-10-01 17:40:46 -0500`; the reflog shows pushes to `origin/main` at 17:40 and 18:01 that day. The paste was the same day; the redaction (`0f80aad`, 2026-10-02 20:08) was the next day. `docs/tasks.md:128` has it right. Fix `:104` in a `[gate]` commit; fix `:276`.

**W7. The rule has no decision procedure.** Four surfaces (`code-reviewer.md:68`, `proposer.md:63`, `decision-scientist.md:77`, `README.md:87`). "Owns the sensitivity" asks for a judgment the incident's agents could not make from a path in `/tmp`. Fix: add one test an agent can run, on all four surfaces: "If the material is not tracked in this repository (`git ls-files --error-unmatch <path>` fails) or was handed to you from outside it, write to the scratchpad and name the owning repository in your final message." The scratchpad becomes the default when ownership is unknown, not one option of two.

**W8. Three surfaces still say docs/ unconditionally.** `.claude/README.md:116`; `.claude/teams/feature-development.md:11,19`; `.claude/teams/decision-science.md:11,12`. These instruct the lead, who in the incident gave the destination. Fix: one clause each ("in the repository that owns the material; see the Scope Matrix note"), or a pointer.

**W9. Entry A co-mingles a breaking change with additive ones.** Draft `:22-63`. The pytest-line change is breaking; the three read-only checks and Step 5 item 9 are additive. Protocol Rule 4 (`propagation-protocol.md:52`): breaking changes are "not co-mingled with additive changes". Fix: split into A1 (the pytest line, BREAKING) and A2 (the tool checks), or give the checks their own row with their own Detect so a maintainer can take one and not the other.

**W10. Entry C carries a figure whose evidence trail stops short.** Draft `:164`, copied from `ISOLATION.md:103`: "the 43 tripwire tests pass on Python 3.11.15 and 3.12.13". The sentence landed in `5e7bcac` (2026-09-30 23:06), the commit that raised the file from 36 to 43 collected tests. The last recorded 3.11.15 run is the round-3 gate review's `37 passed` (`20260930_overwatch_1a_gate.md:397`). No 3.11 interpreter is installed here (`uv python list`). Fix: before release, re-measure on 3.11.15 and write the number with its Evidence, or write "43 on 3.12.13; 37 on 3.11.15 at `28e8482`". Same fix in `ISOLATION.md:103`.

**W11. Two fleet counts are off by one; one is not reconstructible.** `docs/tasks.md:127`: "70 deliveries to 15 repos ... 18 marks at 15 headings". Observed: 16 notification files written at `20:10:00`, 19 marks of 15 lines each. The 70 cannot be checked: the notification format has no per-delivery stamp and 15 of the 16 files are untracked in their repos. Fix: correct to 16 and 19 or name the repo excluded and why; paste the script's per-repo output into the session doc next cycle (that is the Evidence line the number needs).

### Suggestions

**S1.** `pcc.md:117`: say that a short term matches inside words (probe 10: `ant` hits "important"); a false positive is safe, so choose distinctive terms rather than add `-w`, which would miss `<user>2`.

**S2.** Probe 13: outside a repository, stdout is empty and only stderr says why. Add `git rev-parse --git-dir >/dev/null 2>&1 || echo "WARN: not a git repository; check 7 did not run"` (in the verified block).

**S3.** `test_blank_only_list_warns_rather_than_matching_everything` and the inner `sed` at `:112` rest on a premise git 2.43 does not have: `git grep -F -f` with blank lines matched nothing in probe 6 without the filter (and M08 survived). The outer WARN guard is the real control and M09 pins it. Rename the test ("warns rather than passing silently") or keep the filter and fix the comment.

**S4.** `test_committed_term_fails_naming_the_file_and_never_the_term` `:88`: the term-absence assertion cannot fail while the fixture's file name is term-free. Add the path case from C1.

**S5.** Reconcile check 6 and D4 with the convention this branch follows: add `agents/code-reviewer\.md` to the regex at `pcc.md:92` and to the D4 path list (CONOP WHETSTONE `:108`), both in a `[gate]` commit, or write the convention into D4. Entry F row 2 tells downstream to commit the file alone; their check 6 will not notice if they do not.

**S6.** Vocabulary at release (`propagation-protocol.md:165-177`): CONOP x4, TCS x4, OPORD x4, `/pcc` x5, wave x2 in the draft. Precedent is mixed (published entries carry CONOP x12 and "Pre-commit-check" x4). At least the headings: E "TCS Tables" -> "Task-Condition-Standard Tables"; F "`/pcc` Check 7" -> "Pre-commit-check 7". File names like `CONOP-FORMAT.md` stay.

**S7.** Draft `:3` "Written 2026-10-02 on Nidhogg": a machine name a maintainer cannot act on; already public in `config/project.yaml`, so not a leak, but it does not belong in a doctrine draft. Drop the phrase.

**S8.** Draft `:101` "They read all six surfaces above": seven rows precede, and the tests also read `SKILL.md` and `EXAMPLES.md`. Write "rows 1 to 7".

**S9.** Draft `:110-112` "One lesson that travels" is entry F's incident, told inside entry B. Move it to F, or leave it for the trap the P3 at `tasks.md:139` holds.

**S10.** Draft `:283` audience "every public repo with agents": the rule half applies to any repo whose agents read another repository's material. Two sentences: the rule for every repo with agents, the check for every public repo. Also row 5's mode word CREATE is new to the adoption-mode vocabulary; say "per machine, not an artifact in the repo" or reuse CONDITIONAL.

**S11.** Draft `:24` "blocked verification of merge and CI results in 2 sessions": no source in the CONOP or the 2026-10-01 session docs. Add the Evidence or drop the number.

---

Verdict: GO-WITH-FIXES. The gate catches the index cases it names and every commit on the branch is clean against the real list, but its "never the term" claim fails for path names and three scan gaps pass silently; C1, W1 to W4, and W6 are small edits to `pcc.md` and belong in one `[gate]` commit before merge.

## Claims

| Claim | Command | Output |
|---|---|---|
| The hub tree was not modified by this review | `git -C ~/projects/github/tacsop status --porcelain` (after all probes) | nothing |
| No private term appears in this report | the real list was read only by `sed ... \| wc -l` (`5`), `grep -c $'\r'` (`0`), and `git grep -c ... -f <list>` (paths and counts only) | as stated |
| Check 7 block extracted is the one in `pcc.md` | `python` with the test's regex -> `scratchpad/check7.sh` | `extracted 14 lines` |
| 16 probe cases ran, results as tabulated in section 1 | `bash scratchpad/probe.sh` | section 1 table |
| Corrected block passes all cases and the hub | `bash scratchpad/check7_fixed.sh` in each scratch repo and at the hub root | section 1 closing paragraph; hub: no output, exit 0 |
| 20 mutations, 13 caught, 7 survived | `.venv/bin/python scratchpad/mutate.py` | `BASELINE: ('12 passed in 0.23s', [])` then the section 2 table |
| `main`'s surfaces give 6 failed, 6 errors | tests against `git show main:<file>` copies in the scratch tree | `6 failed, 6 errors in 0.21s` |
| 12 tests pass on this tree | `.venv/bin/pytest tests/unit/test_pcc_private_terms.py -q` | `12 passed in 0.31s`, exit 0 |
| 445 pass with and without CI | `env -u CI .venv/bin/pytest -q`; `CI=true .venv/bin/pytest -q` | `445 passed, 1 warning in 5.08s` exit 0; `445 passed, 1 warning in 6.18s` exit 0 |
| Check 7 as written prints nothing at HEAD | `bash scratchpad/check7.sh` at the hub root | no output, exit 0 |
| `5a04f2b` holds a term in 1 file; HEAD, `0f80aad`, and all five branch commits hold none | `git grep -c -i -I -F -f <list> <rev> -- .` for each rev | `5a04f2b:docs/sessions/20261001_assay_bootstrap_and_agent_output_destination.md:1`; otherwise no output, exit 1 |
| `5a04f2b` was committed 2026-10-01 | `git log -1 --format='%ad %cd' --date=iso 5a04f2b` | `2026-10-01 17:40:46 -0500` both |
| 19 marks, 15 lines each; 16 notification files at 20:10:00; 3 repos with no notification | `find ~/projects -maxdepth 5 -path '*/.claude/doctrine-delivered'` with `wc -l` and `stat`; same for `upstream-update.md` | section 5 rows |
| Detect commands print the adopted values | section 4 commands | `1`; nothing; `1 1 1`; `1`; nothing; `1 1 1`; `1` |
| Test counts 9, 26, 43, 12 | `.venv/bin/pytest --co -q <file>` | `9`, `26`, `43`, `12 tests collected` |
| Skill versions 1.0.0, 2.2.1, 3.1.0; SKILL.md 105 lines | `grep version`; `wc -l` | as stated |
| `43 tripwire` entered ISOLATION.md at `5e7bcac` | `git log -S'43 tripwire' -- .claude/skills/shift-left-testing/ISOLATION.md` | `5e7bcac 2026-09-30` |
| No 3.11 interpreter here | `uv python list --only-installed` | 3.12.13 and 3.12.3 only |
| Each cited SHA exists and touches the files named | `git show --stat --format= <sha>` for `d98428a 2a2e725 ff0d8b2 d03e66a 85342b4 5a04f2b 0f80aad d602c8e` | section 4 and 5 rows |
| No em dash in the branch's added prose | `git diff main..HEAD \| grep '^+' \| grep -c <the em dash character>` | `0` |

Overclaims the user caught this session: 0
Overclaims a reviewer caught this session: 4 (the "never the term" claim; the 2026-10-02 date of the paste; 15 repos; 18 marks)

---

## Round 2

**Scope**: `680f080..755286f`, five commits: `a670f9a` [gate] pcc.md, `b773260` [gate] code-reviewer.md, `f5273b0` [infra] README, two agents, two team templates, `ed25fb8` [test] 25 tests, `755286f` [doc] draft, tasks, CHANGELOG. Same method as round 1: invented term `zq-review-term-9182` (and `abe` for one case), the real list touched only by count-producing commands, hub tree untouched (`git status --porcelain` shows only this report). Gate surfaces are alone in their commits; the check 6 regex at `pcc.md` is unchanged and still does not name `code-reviewer.md` (filed as a P3, per S5).

**Summary**. The round 1 defects are closed: a path that holds a term is withheld and counted, a term only in a file name is a FAIL, the whole tree is scanned from any directory, binaries are scanned, list lines are trimmed, unpushed commits and their messages are scanned when an upstream is set, and the dates are right. The 25 tests catch 30 of 32 mutations; the two survivors are a behavior-neutral edit and a reworded unconditional line. Three things remain. The redaction commit `0f80aad` has not reached the remote: `git ls-remote` puts `refs/heads/main` at `368dd5a`, whose tree still holds the line, so the public tip is not yet redacted and the branch's records say "redacted" without naming the state. A hex-only term that happens to sit inside a commit's seven-character sha prefix vanishes from the output with no count. And the no-upstream fallback scans HEAD alone, which on this very branch is 1 of the 12 commits a push would carry. One Critical, three Warnings, nine Suggestions.

### R2.1 Probe harness against the block as now written

Block re-extracted from `pcc.md` with the test's regex: 31 lines, sha1 prefix `481abbd9`. 22 cases; the round 1 cases plus six new ones. "Term in output" was checked by `grep -i -F` over stdout and stderr for every case.

| # | Case | stdout | Round 1 defect | Term in output |
|---|---|---|---|---|
| 1 | Clean index | (empty), exit 0 | n/a | no |
| 2 | Term committed as upper case, no upstream | `FAIL private term in: <sha7>:leak.md:1` and `FAIL private term in: leak.md:1` | n/a; see S2 (two lines for one file) | no |
| 3 | Staged | `FAIL private term in: staged.md:1` | n/a | no |
| 4 | Untracked | (empty) | n/a | no |
| 5 | List missing | one WARN naming the list path | n/a | no |
| 6 | Blank-only list | one WARN | n/a | no |
| 7, 7b | CRLF list; CRLF file | FAIL lines | n/a | no |
| 8 | `zq.review[term]` vs `zqXreview[term]` | `lit.md` only | n/a | no |
| 9 | Term with a space | FAIL | n/a | no |
| 9b | Two spaces around the term in the list | FAIL `sp.md:1` | **W4 closed** | no |
| 10 | `ant` in "important" | FAIL; bullet now says so | **S1 closed** | no |
| 11 | Term in a binary file | FAIL `blob.bin:1` | **W3 closed** | no |
| 12 | Run from `sub/` | FAIL `../root-leak.md:1` | **W1 closed** | no |
| 12b | Same repo, from the root | FAIL `root-leak.md:1` | n/a | no |
| 13 | Outside any repository | one WARN, exit 0 | **S2 closed** | no |
| 14 | Term in a directory name, content hit too | `FAIL private term in 1 path name(s) with content hits; paths withheld` and `FAIL private term in 1 tracked file name(s); names withheld` | **C1 closed** | no |
| 15 | Term only in a file name | `FAIL private term in 1 tracked file name(s); names withheld` | **C1 closed** | no |
| 16 | Term in an intermediate commit, removed at HEAD, no upstream | (empty); `git rev-list --count HEAD --not --remotes` says 3 | **W2 partial**: by design, see the bullet and R2-W2 | no |
| 17 | Same, with an upstream | `FAIL private term in: <sha7>:new.md:1` | **W2 closed** for this case | no |
| 17b | Same repo after `git push` | (empty) | right: nothing left unpushed | no |
| 18 | Term only in an unpushed commit message | `FAIL private term in 1 unpushed commit message line(s); not printed` | new coverage | no |
| 19 | Term only in a file name in an intermediate commit, deleted at HEAD | `FAIL private term in 1 tracked file name(s); names withheld` | new coverage | no |
| 20 | Term `abe`; content hit only in an intermediate commit whose short sha is `0f33abe` (1,191 amend tries to get it) | **(empty)** | **new defect, R2-W1** | no (a miss, not a leak) |
| 21 | One term-bearing path: 1 hit in HEAD, 2 staged | `FAIL private term in 2 path name(s) ...` for one path | count is not once per path, R2-S1 | no |
| 22 | Unstaged edit to a tracked file | (empty) | right: not pushed | no |

Evidence: `bash scratchpad/probe_r2.sh`, output as tabulated. Case 20 diagnostic: the hits line is `0f33abe:hit.md:1`; the path portion after the sha is stripped holds no term, so `n` is 0; `grep -v` on the whole line drops it because the sha prefix holds `abe`; nothing is printed. Withholding on the path portion only prints `FAIL private term in: 0f33abe:hit.md:1`.

On the no-upstream bullet (`pcc.md`, the first bullet after the block): accurate as disclosure. As a control it covers the common case, a topic branch created without `-u`, by asking the reader to remember a command. This branch is that case: `git rev-parse --abbrev-ref @{upstream}` -> `fatal: no upstream configured`; `git rev-list --count HEAD --not --remotes` -> `12`; the block scanned HEAD alone. See R2-W2.

The block at the hub root and from `docs/`, with the real list: no output, exit 0 both. Count-only greps over each of the five new commits (tree, file names, message): `0 0 0` for all five.

### R2.2 Mutations against the 25 tests

Scratch tree of the seven surfaces and the test; baseline `25 passed`. Against `680f080`'s surfaces: `15 failed, 10 passed`, matching `ed25fb8`.

| # | Edit | Result | Caught by |
|---|---|---|---|
| M01 | drop `-i` | CAUGHT | committed_term |
| M02 | drop `--cached` | CAUGHT (was SURVIVED) | staged_term |
| M03 | drop `-F` | CAUGHT (was SURVIVED) | fixed_strings |
| M04 | add `-I` back | CAUGHT | binary_file |
| M05/N1 | drop `:/` | CAUGHT (was SURVIVED) | subdirectory |
| M06 | `--untracked` for `--cached` | CAUGHT | untracked, unstaged_edit |
| M07 | drop the FAIL prefix | CAUGHT | 7 tests |
| M08/N3 | drop the sed trim | CAUGHT | trimmed, blank_only |
| M09 | WARN never fires | CAUGHT | missing_list, blank_only |
| M10 | move the default path | CAUGHT | default_list |
| M11 | Quick Reference -> Warn only | CAUGHT | quick_reference |
| M12 | rename the heading | CAUGHT | 1 failed, 16 errors |
| M13 | WARN twice | CAUGHT | missing_list |
| M14 | `exit 1` at the end | CAUGHT | clean_index, committed_term |
| M15 | scan HEAD only | CAUGHT | staged_term, unpushed_intermediate |
| M16 | empty the block body | CAUGHT | 14 failed |
| M17 | owns -> holds | CAUGHT | surface_carries |
| M18 | delete the operative sentence | CAUGHT (was SURVIVED) | surface_carries |
| M19 | never -> always | CAUGHT (was SURVIVED) | surface_carries |
| M20 | README never -> and also | CAUGHT (was SURVIVED) | surface_carries |
| N2 | drop the rev-list loop | CAUGHT | unpushed_intermediate, commit_message |
| N4 | drop the names check | CAUGHT | only_in_a_file_name |
| N5 | drop the messages check | CAUGHT | commit_message |
| N6 | drop the path-withholding | CAUGHT | directory_name (the term appeared) |
| N7a | path-count branch -> `[ ] && echo` (not last) | **SURVIVED**, behavior-neutral: exit status comes from the last statement | |
| N7b | message-count branch -> `[ ] && echo` (last) | CAUGHT | clean_index, committed_term |
| N8 | delete the ls-files sentence | CAUGHT | surface_carries |
| N9 | scratchpad "and" -> "or" | CAUGHT | surface_carries |
| N10 | README:116 back to unconditional | CAUGHT | no_surface_sends |
| N11 | feature-development line back | CAUGHT | no_surface_sends |
| N12 | decision-science line back | CAUGHT | no_surface_sends |
| N13 | new line "write the report to `docs/reviews/`" | **SURVIVED**: the pin's regex wants `write(s) (a) (proposal\|findings\|report)` | |

30 of 32 caught. Evidence: `.venv/bin/python scratchpad/mutate2.py`.

### R2.3 Can the output carry a term?

No, in all 22 cases, including the three withheld-count lines, which carry a count and fixed words. The only user-controlled string the block prints is the list's own path in the WARN (case 5). A path that holds a term is withheld whether the hit is in the index or in a commit (case 14). The one defect found is in the other direction: case 20 loses a hit, it does not print one.

### R2.4 The four rule surfaces and the three W8 lines

`code-reviewer.md:68`, `proposer.md:63`, `decision-scientist.md:77`, `README.md:87`: the same three sentences, nouns adapted (material, model), "handed to you" on the agents and "handed over" on the README. Consistent. `README.md:116`, `feature-development.md:11,19`, `decision-science.md:11,12,20` now end in "of the owning repository (Scope Matrix note)". Two new ways to misread, below as R2-W3 and R2-S3.

### R2.5 Claims in the five commit messages, tasks, and CHANGELOG

| Claim | Command | Output | Status |
|---|---|---|---|
| `a670f9a`: closes C1, W1 to W4, W6, S1, S2 | harness cases 14, 15, 12, 17, 11, 9b, 13, 10; `pcc.md` comment line 6 and bullets | as tabulated | HOLDS (W2 for the upstream case; see R2-W2) |
| `a670f9a`: paths withheld counted once per path | case 21 | `2 path name(s)` for one path | REFUTED in the differing-count case (R2-S1) |
| `a670f9a`: three count branches are if/fi, exit 0 when silent | block lines 27, 30, 32; case 1 | exit 0 | HOLDS |
| `a670f9a`: hub root and `docs/` -> no output, exit 0 | re-run | no output, exit 0 both | HOLDS, noting the branch has no upstream so the scan was index plus HEAD |
| `a670f9a`: the harness results for cases 12, 12b, 13, 14, 15, 16 | re-run | as stated | HOLDS |
| `b773260`: the sentence is on code-reviewer.md | grep | `:68` | HOLDS |
| `f5273b0`: same test on two agents and the matrix; three lines say "of the owning repository (Scope Matrix note)" | grep | `:63`, `:77`, `:87`; `:116`, `:11`, `:19`, `:11`, `:12`, `:20` | HOLDS |
| `ed25fb8`: 13 new cases; 25 passed; red 15 failed, 10 passed | `--co`; pytest; scratch run against `680f080` | `25`; `25 passed in 0.76s` exit 0; `15 failed, 10 passed` | HOLDS |
| `ed25fb8`: 458 passed, with and without `CI=true` | pytest | `458 passed, 1 warning in 5.40s` exit 0; `458 passed, 1 warning in 6.21s` exit 0; `--co` 458 | HOLDS |
| `755286f`: A split into A1 and A2 with an open item | draft `:23`, `:61`, open item 3 | present | HOLDS |
| `755286f`: F dates both incidents 2026-10-01 | draft F paragraph | "The same day, the record ... committed and pushed. It was found and redacted on 2026-10-02." | HOLDS |
| `755286f`: audience split, list row's mode word, lesson moved from B to F | draft F `:10`, `:29`, `:37`; B has 0 "lesson that travels" | present | HOLDS |
| `755286f`: C cites the 3.11.15 run at `84dd487`; the 43 have no library skips | session record `:76` (`394 passed, 5 skipped`, 3.11.15, `84dd487`); `test_isolation.py` unchanged since `84dd487`; its six skips are `os.name == "nt"`, `posix_spawn`, `sendmsg`, `/proc` | 432 at `84dd487` = 394 + 35 (two matplotlib modules, 8 + 27, skipped as items) + 3 (pandas tests in `test_scorer.py`); the 43 are in the 394 | HOLDS; I read the evidence as the lead does (W10 closed) |
| `755286f`: E and F headings spell out TCS and `/pcc` | draft `:262`, `:305` | "Task-Condition-Standard", "Pre-Commit Check 7" | HOLDS |
| `755286f`: machine name dropped; "rows 1 to 7"; 2-sessions figure cites the CONOP | grep | no `Nidhogg`; `:136`; `:63` "(CONOP OVERWATCH, approved 2026-09-30)" | HOLDS on the first two; the CONOP does not carry the figure (R2-S7) |
| tasks `:127`: 70 deliveries to 16 repos, 10 appended, 6 new | heading counts of the 16 files: six at 1, 1, 3, 5, 5, 5 (new: 20 entries) and ten above 5 (appended, 5 each: 50) | 20 + 50 = 70 | consistent; still not independently recorded (the lead says so) |
| tasks `:127`: 19 marks at 15 headings, 18 written by the run | mtimes | 16 at `20:10:00`; `fist`, `schelling-point` at `20:08:38`; `daily_weather` at `10:22:31` | 19 and 15 HOLD; 18 is 16 unless the seeding counts as the run (R2-S6) |
| CHANGELOG `:38`, tasks `:8`: redacted at `0f80aad`; HEAD 0 files; `5a04f2b` reachable on `origin/main` | `git ls-remote origin refs/heads/main`; `git rev-list --count origin/main..main`; count-only grep at `origin/main` | `368dd5a`; `2` (`0f80aad`, `2840c0f`); `origin/main: docs/sessions/20261001_assay_bootstrap_and_agent_output_destination.md:1` | the local claims HOLD; the state is committed, not pushed: the public tip still carries the line (R2-C1) |
| CHANGELOG Added line describes the fixed check | read | index and unpushed commits, names, messages, path only when clean, WARN outside a repo | HOLDS |
| A1 and A2 Detect | run | `^pytest\b` nothing; `venv/bin/pytest` 1; `NO GIT IDENTITY` 1 | HOLDS |

### R2.6 Round 1 findings

| Finding | Status | Evidence |
|---|---|---|
| C1 path leak and file-name miss | **Closed** | cases 14, 15; N6 caught |
| W1 `-- .` | **Closed** | case 12; M05 caught |
| W2 unpushed commits | **Partial** | case 17 closed; case 16 and the hub (1 of 12 scanned) remain by design; R2-W2 |
| W3 `-I` | **Closed** | case 11; M04 caught |
| W4 whitespace | **Closed** | case 9b; M08 caught |
| W5 test pins | **Closed** | 30 of 32 caught; every round 1 survivor now caught |
| W6 dates | **Closed** | comment line 6; F paragraph; nit R2-S5 |
| W7 decision procedure | **Closed** | the ls-files sentence on four surfaces; N8, N9 caught; new misread R2-W3 |
| W8 unconditional lines | **Closed** | six lines; N10 to N12 caught; R2-S4 on the pin's reach |
| W9 Rule 4 | **Closed** | A1, A2, open item 3 |
| W10 43 on 3.11.15 | **Closed** | arithmetic above; I agree with the lead |
| W11 fleet counts | **Partial** | 16 and 19 corrected; 70 consistent; "18 written by the run" is 16 by mtime |
| S1 substring | **Closed** | bullet |
| S2 outside a repo | **Closed** | case 13 |
| S3 blank-list rationale | **Closed** | test renamed; inner filter replaced by the trim |
| S4 term-absence assertion | **Closed** | `_no_term_in` on the path cases |
| S5 check 6 regex and D4 | **Deferred** | P3 in `docs/tasks.md`; regex unchanged |
| S6 vocabulary | **Partial** | headings E and F; body still CONOP x5, OPORD x4, TCS x3, `/pcc` x4 |
| S7 machine name | **Closed** | gone from the draft |
| S8 rows 1 to 7 | **Closed** | `:136` |
| S9 lesson in B | **Closed** | moved to F |
| S10 audience | **Closed** | `:10` |
| S11 2-sessions figure | **Partial** | cites the CONOP, which does not carry it |

Closed 18, partial 4, deferred 1.

### Round 2 findings

**Critical**

**R2-C1. The redaction is committed, not pushed; the public tip still carries the line.** `git ls-remote origin refs/heads/main` -> `368dd5a` (2026-10-01 18:01). `git rev-list --count origin/main..main` -> `2` (`0f80aad`, `2840c0f`). Count-only grep at `origin/main` -> `docs/sessions/20261001_assay_bootstrap_and_agent_output_destination.md:1`. CHANGELOG `:38` and tasks `:8` say "redacted" and "git grep over HEAD: 0 files", which is true of the local HEAD and reads as the public state; the P1's "the commit stays reachable on origin/main" understates it, since the tip itself is unredacted about 26 hours after the push. The verifying-claims kernel, rule 1: name the state. Fix: push `main` (the user's action, not mine), then re-run `git ls-remote origin refs/heads/main` and the count-only grep at the new `origin/main` and write both outputs as the Evidence under the CHANGELOG and P1 lines; until then say "redacted locally, not yet pushed". Note for the P1 decision: `2840c0f` predates the redaction and holds the line in its tree, so the push adds one more such commit to history (already there via `5a04f2b` and `368dd5a`).

**Warnings**

**R2-W1. A hex-only term inside a commit's short sha hides the hit.** `pcc.md` block line 28 applies `grep -v` to the whole `sha7:path:count` line, while line 26 counts term-bearing paths on the path portion. Case 20: term `abe`, hit only in commit `0f33abe`; printed lines 0, withheld count 0. Needs a term made only of `0-9a-f` (short usernames and some codenames qualify), sitting only in an intermediate unpushed commit, with a 1-in-800 sha; rare, silent, and in a gate. Fix (verified in the diagnostic): decide withhold-or-print on the path portion, for example a `while read` over the hits with `p=$(printf '%s' "$line" | sed -E 's/^[0-9a-f]{7}://; s/:[0-9]+$//')` and `grep -q` on `$p`; one test with a hex-only term and an amended sha, or a fixture that fakes the hits line.

**R2-W2. The no-upstream fallback under-scans the common case.** Block line 19. On this branch `rev-list HEAD --not --remotes` is 12 and the block scanned 1. `git rev-list HEAD --not --remotes` gives the set a push carries whether or not an upstream is set: scratch r16 (no remote) 3, r17 after push 0, r18 1, r19 2, r20 2, hub 12. Fix: `revs=$(git rev-list HEAD --not --remotes 2>/dev/null)`; the bullet then shrinks to "a repository with no remote scans all of HEAD's history, which is what a first push carries". The current bullet is adequate as disclosure, not as a control.

**R2-W3. The ls-files test routes this repository's own uncommitted new files to the scratchpad.** Four surfaces. `git ls-files --error-unmatch <path>` fails for any untracked path, including a new file the lead wrote here and has not added. The team templates describe review before commit, so this will fire in normal use. The direction is safe (scratchpad) but the report lands in the wrong place and the agent says so every time. Fix, one clause: "if the material is outside this repository's working tree (`git ls-files --error-unmatch <path>` fails and `git ls-files --others --exclude-standard <path>` prints nothing) or was handed to you from outside it".

**Suggestions**

**R2-S1.** Block line 26: the once-per-path count counts a path twice when its index count and commit count differ (case 21). Strip `:[0-9]+$` before `sort -u`.

**R2-S2.** In a no-upstream repo HEAD and the index coincide, so every content hit prints twice (`<sha7>:path:count` and `path:count`; cases 2, 7 to 12b). Cosmetic. With R2-W2 it persists wherever HEAD is unpushed; dedupe on the path portion if it annoys.

**R2-S3.** "name the owning repository in your final message" (four surfaces): a sibling repository's name is one of the four term categories the check names. Add "or describe it when its name is itself private".

**R2-S4.** The W8 pin matches `write(s) (a) (proposal|findings|report) ... to `docs/`; "write the report to `docs/reviews/`" survives (N13). Fine for the three known lines; say so in the test, or widen to `(write|writes|put|save)[^|]*`docs/(reviews|plans)/``.

**R2-S5.** `pcc.md` comment line 6, "Two incidents on 2026-10-01, found 2026-10-02": the first was found the same day. "the second found 2026-10-02".

**R2-S6.** tasks `:127` "18 written by the run": 16 by mtime; `fist` and `schelling-point` were seeded at 20:08:38.

**R2-S7.** Draft A2 `:63` cites the CONOP for "blocked verification ... in 2 sessions"; `grep -i -E 'in 2 sessions|two sessions|blocked verif|unauthenticated'` over the CONOP finds nothing. Drop the number or cite the Insights report's wording.

**R2-S8.** Draft C `:195` "The full suite ... passed on Python 3.11.15": 394 passed with 38 matplotlib and pandas tests not run (two modules skipped as items plus three tests). Say "apart from the 38 matplotlib and pandas tests". The 43 did run.

**R2-S9.** Draft F row 5 and the bullet both say the list is matched "inside words too"; the check 7 comment says "the output carries a count, and a path only when the path itself is clean". Good. One more sentence worth having on both: "a term that is only hex digits and letters a to f can hide inside a commit sha" until R2-W1 lands.

Verdict: GO-WITH-FIXES. The round 1 defects are closed and the tests now pin them, but the redaction has not reached the remote (the public tip still holds the line), and the block still loses a hex-only term hidden in a short sha and scans 1 of the 12 commits a push of this very branch would carry; the push and the two block edits are small and should land before entry F copies the block downstream.

## Claims (round 2)

| Claim | Command | Output |
|---|---|---|
| Hub tree untouched apart from this report | `git status --porcelain` | `?? docs/reviews/20261002_private_terms_gate.md` |
| No real term in this round's text | the real list read only by `grep -c -i -F -f <list>` over files, trees, names, and messages; this report checked the same way | `0` |
| Block extracted matches `pcc.md` | python with the test's regex | `extracted 31 lines; sha 481abbd9` |
| 22 probe cases as tabulated | `bash scratchpad/probe_r2.sh` | section R2.1 |
| Case 20 mechanism and fix | diagnostic in `probes_r2/r20` | hits `0f33abe:hit.md:1`; n 0; printed 0; path-only withhold prints the line |
| 32 mutations, 30 caught | `.venv/bin/python scratchpad/mutate2.py` | section R2.2 |
| Red state against `680f080` | scratch run | `15 failed, 10 passed in 0.49s` |
| 25 and 458 pass | `.venv/bin/pytest tests/unit/test_pcc_private_terms.py -q`; `env -u CI .venv/bin/pytest -q`; `CI=true .venv/bin/pytest -q` | `25 passed in 0.76s`; `458 passed, 1 warning in 5.40s`; `458 passed, 1 warning in 6.21s`; all exit 0 |
| Block clean at the hub, root and `docs/` | `bash scratchpad/check7_r2.sh` | no output, exit 0 both |
| Five new commits clean (tree, names, message) | count-only greps per commit | `0 0 0` x5 |
| Branch has no upstream; a push carries 12 | `git rev-parse --abbrev-ref @{upstream}`; `git rev-list --count HEAD --not --remotes` | `fatal: no upstream configured`; `12` |
| Remote main is `368dd5a`; two local commits unpushed; its tree holds the line | `git ls-remote origin refs/heads/main`; `git rev-list --count origin/main..main`; count-only grep at `origin/main` | `368dd5a... refs/heads/main`; `2`; one file, count 1 |
| 3.11 arithmetic | `--co` per module; session record `:76`; `git diff --stat 84dd487 HEAD -- tests/unit/test_isolation.py` | 8, 27, 49; `394 passed, 5 skipped`; empty diff |
| `test_isolation.py` skips are platform-only | `grep -n -E 'importorskip\|skipif\|pytest\.skip\|mark\.skip'` | lines 223, 295, 307, 346, 511, 540, all `os.name`, `posix_spawn`, `sendmsg`, `/proc` |
| CONOP lacks the 2-sessions figure | `grep -n -i -E 'in 2 sessions\|two sessions\|blocked verif\|unauthenticated'` | nothing |
| Fleet counts | `find` with `stat`, `grep -c '^## 2026-'` | 16 files at `20:10:00` with 1, 1, 3, 5, 5, 5, 6, 6, 6, 6, 8, 9, 10, 10, 10, 10 headings; 19 marks |

Overclaims the user caught this session: 0
Overclaims a reviewer caught this session (round 2): 3 (the redaction's state; "once per path"; "18 written by the run")

---

## Round 3

**Scope**: `755286f..9a2ad3d`, five commits: `5f83e12` [gate] pcc.md, `2e113fa` [gate] code-reviewer.md, `4b4e1c5` [infra] README and two agents, `51c871e` [test] 29 tests, `9a2ad3d` [doc] CHANGELOG, draft, tasks. Same method and constraints as rounds 1 and 2. Gate surfaces alone in their commits; the two team templates are unchanged since round 2 (`git diff --stat 755286f 9a2ad3d -- .claude/teams/` empty).

**Summary**. The redesign closes R2-W1 by construction: `git grep -l` yields paths, the 40-hex prefix is stripped, paths are deduplicated, and one `grep` over the same strings splits withheld from printed, so no hit can fall between the two whatever the term is made of. `rev-list HEAD --not --remotes` closes R2-W2; the working-tree test closes R2-W3. Both harnesses (27 and 18 cases) print no term anywhere; the five cases that failed in round 2 now print their hits or count once. 35 of 36 mutations are caught, including all five round 2 edits; the one survivor is behavior-neutral. The one FAIL line the check prints at the hub is a true positive about an unpushed commit and is the right treatment. I retract R2-S7 and round 1's S11: the CONOP carries the 2-sessions figure at line 267; my grep matched that line both times and I cut the output short and misread it. Zero Critical, zero Warnings, four Suggestions. Verdict GO.

### R3.1 Harnesses against the block as now written

Block re-extracted: 31 lines, sha1 prefix `6092f82f`. Round 2 harness (22 cases) plus five round 3 cases; round 1 harness (18 labels) re-pointed at the same block. Term in output: no, in every case of both runs (`grep -c -i` over all output of the round 1 run: `0`).

| # | Case | stdout now | Round 2 state |
|---|---|---|---|
| 1 to 15, 17 to 19, 22 | as in R2.1 | same findings, each printed hit now one clean path, no sha, no count | unchanged, correct |
| 2, 7 to 12b | no-upstream repos | one line per file (was two) | **R2-S2 closed** |
| 16 | intermediate commit, no remote | `FAIL private term in: hist.md` | **R2-W2 closed** |
| 20 | term `abe`, hit only in commit `8abe4a8` (215 amend tries) | `FAIL private term in: hit.md` | **R2-W1 closed** |
| 21 | one term-bearing path, 1 hit in HEAD and 2 staged | `... 1 path name(s) ...` | **R2-S1 closed** |
| 23 | digits-only term `7731` in content | `FAIL private term in: num.md` | new; the old `:count` field is gone |
| 23b | `7731` as a directory name and in content elsewhere | one withheld count, `num.md` printed, one name count | new |
| 24 | hub-like: clone with a remote, `checkout -b topic`, no upstream, term in an intermediate commit | `FAIL private term in: b.md`; `--not --remotes` 3 | new; the case this branch is in |
| 25 | same path in the index (2 hits) and an unpushed commit (1 hit) | `FAIL private term in: both.md`, once | new |
| 26 | one term-bearing path and one clean path, both content hits | one withheld count, `plain.md` printed, one name count | new |
| 27 | from a subdirectory, same file in index and HEAD, no remote | `FAIL private term in: deep.md`, once | new |

Evidence: `bash scratchpad/probe_r3.sh`; `bash scratchpad/probe_r1_on_r3.sh`.

At the hub, with the real list: root prints `FAIL private term in: docs/sessions/20261001_assay_bootstrap_and_agent_output_destination.md`, exit 0, in 0.23 s; from `docs/`, the same path relative to `docs/`. `git rev-list --count HEAD --not --remotes` -> `17`; `2840c0f` is in that set; a count-only grep per unpushed commit finds the hit in `2840c0f` alone. The five new commits are clean (tree, names, message: `0 0 0` each).

### R3.2 Mutations against the 29 tests

Baseline `29 passed`. Against `755286f`'s surfaces: `8 failed, 21 passed`, matching `51c871e`.

| Group | Result |
|---|---|
| M01 to M20 (round 1 set, adapted) | all CAUGHT |
| N2, N4 to N7b, N8 to N12 (round 2 set) | all CAUGHT |
| N13 reworded unconditional line "write the report to `docs/reviews/`" | CAUGHT (was SURVIVED): `test_no_surface_sends_output_to_docs_unconditionally` |
| P1 drop the 40-hex prefix strip | CAUGHT: `test_each_printed_hit_is_one_clean_path...` |
| P2 drop `sort -u` | CAUGHT: same test |
| P3 `-l` back to `-c` | CAUGHT: same test and `test_term_that_would_match_only_a_hit_count_is_not_lost` |
| P4 `--not --remotes` back to the upstream fallback | CAUGHT: `test_branch_without_upstream...`, `test_repo_with_no_remote...` |
| P5 drop the private-name clause | CAUGHT: `test_surface_carries_the_rule...` |
| P6 drop `sed '/^$/d'` before `held` | SURVIVED, behavior-neutral: an empty line matches no non-empty fixed pattern, so the count is 0 either way |

35 of 36 caught. Evidence: `.venv/bin/python scratchpad/mutate3.py`.

### R3.3 Claims in the five commit messages and the records

| Claim | Command | Output | Status |
|---|---|---|---|
| `5f83e12`: closes R2-W1, R2-W2, R2-S1, R2-S2, R2-S5 | cases 20, 16, 24, 21, 2, 25; comment line 7 | as tabulated; "the second found 2026-10-02" | HOLDS |
| `5f83e12`: hub root one FAIL line naming the assay doc; from `docs/` the same path relative; `2840c0f` holds the line; 12 commits | re-run | one line, path only; relative from `docs/`; `2840c0f: 1 file(s)`; now 17 with the five new commits | HOLDS |
| `5f83e12`: remote tip `368dd5a` holds the same line | `git ls-remote origin refs/heads/main`; count-only grep at `origin/main` (round 2) | `368dd5a`; one file | HOLDS |
| `5f83e12`: both harnesses term-in-output no; cases 16, 20 print; 21 counts one | re-run | as stated | HOLDS |
| `2e113fa`, `4b4e1c5`: working-tree test and private-name clause on four surfaces | grep | code-reviewer `:68`, proposer `:63`, decision-scientist `:77`, README matrix note | HOLDS |
| `51c871e`: four new cases; 29 passed; 462 both; red 8 failed, 21 passed | `--co`; pytest; scratch run | `29`; `29 passed in 0.89s` exit 0; `462 passed, 1 warning in 5.19s` and `6.21s`... `5.99s` exit 0; `8 failed, 21 passed` | HOLDS |
| `9a2ad3d`: CHANGELOG and P1 name the redaction's state | read `:38`, tasks `:8` | "over local HEAD", "reaches the public tip when `main` is pushed", "Until `main` is pushed, the public tip itself still holds the line", the `2840c0f` flag explained | HOLDS (R2-C1 wording closed) |
| `9a2ad3d`: 16 marks written by the run, 2 seeded, 1 older | tasks | present; matches the mtimes | HOLDS |
| `9a2ad3d`: the CONOP's Status Log entry carries the 2-sessions figure | `sed -n 267p conop_overwatch...md \| grep -o` | "an unauthenticated `glab` blocked verification in 2 sessions" | HOLDS; my round 2 grep listed line 267 and I cut it at 260 characters |
| `9a2ad3d`: entry C says 394 passed apart from the 38, the 43 in the run | draft C `:31` of the section | present | HOLDS |
| `9a2ad3d`: F and CHANGELOG describe the check as rewritten | draft F `:8`; CHANGELOG `:27` | F says `git grep -l -i -F`; CHANGELOG still says `git grep -c -i -F` | F HOLDS; CHANGELOG stale on one flag (R3-S1) |

### R3.4 The two questions

**(1) R2-S7.** You are right and I was wrong. `grep -n -i -E 'in 2 sessions|two sessions|blocked verif|unauthenticated'` over the CONOP prints line 267, and that line reads "an unauthenticated `glab` blocked verification in 2 sessions". In round 2 I piped the match through `cut -c1-260`, saw the line's opening clause, and wrote "finds nothing". Round 1's S11 was the same miss through a 240-character cut. Both retracted; the draft's citation to the 2026-09-30 approved entry is correct and more precise than the original.

**(2) The FAIL at the hub.** The behavior is right and the block should not exclude content a remote already holds. Three reasons. First, the check's contract is "what a push would carry"; `2840c0f` is carried and its tree holds the line, so the line is a true statement. Second, the exclusion would be wrong in the one scenario where it matters most: after option (b) in the P1, a history rewrite, a stale local commit carrying the content is exactly what must not be pushed, and "a remote already holds it" would be read from the tracking refs, which are a cache of the pre-rewrite remote. Third, the cost of the true positive is one line that clears when `main` is pushed, and pushing `main` before this branch is the right order anyway, since it puts the redaction on the public tip first. The bullet "a hit in an old commit is already public: redact forward first, then decide about history" fits this case, with the P1 carrying the decision. One clause would make the bullet cover this shape without the P1: "a hit in an unpushed commit whose content the remote already holds is still a FAIL: the push re-sends it, and after a history rewrite that is how the content comes back; push or rewrite to clear it" (R3-S2).

### R3.5 Round 2 findings

| Finding | Status | Evidence |
|---|---|---|
| R2-C1 redaction state | **Closed** as a records finding: CHANGELOG `:38` and P1 `:8` name the state. The push itself has not happened (`ls-remote` -> `368dd5a`); that is the user's action and sits outside the branch | |
| R2-W1 sha-prefix miss | **Closed** | case 20 prints `hit.md`; P1, P3 caught; the class cannot occur by construction |
| R2-W2 upstream fallback | **Closed** | cases 16, 24; P4 caught; hub scans 17 |
| R2-W3 ls-files test | **Closed** | `git rev-parse --show-toplevel` on four surfaces; N8 caught |
| R2-S1 once per path | **Closed** | case 21 -> 1; the count is gone |
| R2-S2 duplicate lines | **Closed** | cases 2, 25, 27 -> one line each |
| R2-S3 private name in the final message | **Closed** | "or describe it when its name is itself private" on four surfaces; P5 caught |
| R2-S4 phrase-shaped pin | **Closed** | regex widened; N13 caught |
| R2-S5 "found 2026-10-02" | **Closed** | comment line 7 |
| R2-S6 "18 written by the run" | **Closed** | "16 written by the run, 2 seeded ..., daily_weather's predates it" |
| R2-S7 CONOP figure | **Retracted** (reviewer error) | CONOP `:267` carries it; the draft cites the entry |
| R2-S8 entry C wording | **Closed** | "apart from the 38 matplotlib and pandas tests ... the 43 ... were in that run" |
| R2-S9 hex-term sentence | **Moot** | the sha is gone from the output |

Closed 11, retracted 1, moot 1, open 0. Of round 1's partials: W2 and W11 are now closed by the above; S6 (vocabulary in entry bodies) and S5 (check 6 regex, filed as P3) stand as before.

### Round 3 findings

No Critical. No Warnings.

**Suggestions**

**R3-S1.** CHANGELOG `:27` says the check runs `git grep -c -i -F`; the block and draft F say `-l`. One character.

**R3-S2.** `--remotes` reads the remote-tracking refs, a cache (the trap already filed at `tasks.md`, the seventh candidate). After another box pushes or rewrites, a clean run here can be stale. One clause in the first bullet: "run `git fetch` first when another machine may have pushed", plus the clause under R3.4 (2) for a hit the remote already holds.

**R3-S3.** The working-tree test passes a symlink or nested repository under the top level that points into another repository. Rare in this fleet; `realpath` closes the symlink case if it ever bites.

**R3-S4.** The two team templates still say "write proposal to `docs/plans/` of the owning repository (Scope Matrix note)" and now the agent files carry a runnable test; a pointer from the templates to that test is one more place a lead sees it. Optional.

Verdict: GO. Every Critical and Warning from rounds 1 and 2 is closed and pinned, the output can carry no term in 45 harness cases, and the one FAIL line the check prints at the hub is a true positive that clears when `main` is pushed, which should precede the push of this branch.

## Claims (round 3)

| Claim | Command | Output |
|---|---|---|
| Hub tree untouched apart from this report | `git status --porcelain` | `?? docs/reviews/20261002_private_terms_gate.md` |
| No real term in this round's text | report checked with `grep -c -i -F -f <list>`; the list otherwise read only by count-producing greps | `0` |
| Block extracted matches `pcc.md` | python with the test's regex | `extracted 31 lines; sha 6092f82f` |
| 27 and 18 harness cases as tabulated, no term in output | `bash scratchpad/probe_r3.sh`; `bash scratchpad/probe_r1_on_r3.sh` | section R3.1; `0` |
| 36 mutations, 35 caught | `.venv/bin/python scratchpad/mutate3.py` | section R3.2 |
| Red state against `755286f` | scratch run | `8 failed, 21 passed in 0.77s` |
| 29 and 462 pass | `.venv/bin/pytest tests/unit/test_pcc_private_terms.py -q`; `env -u CI .venv/bin/pytest -q`; `CI=true .venv/bin/pytest -q`; `--co -q` | `29 passed in 0.89s`; `462 passed, 1 warning in 5.19s`; `462 passed, 1 warning in 5.99s`; `462 tests collected`; all exit 0 |
| Hub run: one true-positive line, 0.23 s | `time bash scratchpad/check7_r3.sh` at the root and from `docs/` | the assay session doc path, exit 0 both |
| `2840c0f` is the only unpushed commit holding the hit; 17 commits unpushed | per-commit count-only grep; `git rev-list --count HEAD --not --remotes` | `2840c0f: 1 file(s)`; `17` |
| Remote main still `368dd5a`; local main 2 ahead | `git ls-remote origin refs/heads/main`; `git rev-list --count origin/main..main` | `368dd5a`; `2` |
| Five new commits clean | count-only greps (tree, names, message) | `0 0 0` x5 |
| CONOP line 267 carries the 2-sessions figure | `sed -n 267p ... \| grep -o -i -E '.{60}in 2 sessions.{20}'` | "...because an unauthenticated `glab` blocked verification in 2 sessions. The 2026-10-16 dat" |
| Four surfaces carry the working-tree test and the private-name clause | grep | `:68`, `:63`, `:77`, README matrix note |

Overclaims the user caught this session: 0
Overclaims a reviewer caught this session (round 3): 1 (CHANGELOG `:27` still says `-c`)
Reviewer's own overclaims retracted this round: 2 (round 1 S11 and round 2 R2-S7, the same misread of CONOP line 267)
