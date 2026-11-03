# Session: CONOP PICKET, Three Rulings Measured, Then Shelved

**Date**: 2026-10-30, with the closing ruling on 2026-11-02 (on Nidhogg)
**Branch**: main
**Tags**: #session #doctrine #infra #docs #complete
**Documents**: [docs/tasks.md](../tasks.md), [docs/plans/conop_picket_unattended_doctrine_sweeps_and_guidance_watch.md](../plans/conop_picket_unattended_doctrine_sweeps_and_guidance_watch.md), [docs/reviews/20261029_picket_review.md](../reviews/20261029_picket_review.md)
**References**: [20261022_anthropic_docs_feed_proposer.md](../reviews/20261022_anthropic_docs_feed_proposer.md), [20261022_anthropic_docs_feed_review.md](../reviews/20261022_anthropic_docs_feed_review.md), [20261005_assay_adoption_feedback.md](../reviews/20261005_assay_adoption_feedback.md), [.claude/commands/pcc.md](../../.claude/commands/pcc.md)
**Follows**: [20261022_anthropic_docs_feed_and_prompt_audit.md](20261022_anthropic_docs_feed_and_prompt_audit.md)

---

## Summary

The session opened on a dirty tree: the 2026-10-29 session had drafted CONOP PICKET, taken its round 1 review and added its task line, then ended without `/session-end`, so none of it was committed or recorded. Those three files were committed first. The user then asked to roll on PICKET's open items. Four measurements on Nidhogg settled three of them: a survey of twenty repositories found seven with CI on pull requests and `propter`, one of the plan's proposed canaries, with none; the same survey found branch protection a GitHub Pro feature on every private repository here, which removed the plan's write boundary; a headless auto-mode run wrote three files under `.claude/` with zero denials; and no candidate canary had ever had a pull request. The user ruled: canaries `stx-server`, `schelling-point`, `hallmark`; pull requests from forks held by a service GitHub account in place of branch protection; model `claude-sonnet-5-5`. The plan was rewritten around the fork, with the GitHub mechanics verified against GitHub's docs.

On 2026-11-02 the user, returning and asking why a service account was needed, judged a second GitHub account and a paid plan both unnecessary and shelved the automation rather than build either: "I'd rather scrap the automation effort than build a second GitHub account." What stands is the local, programmatic path: the Anthropic source register as a `/session-start` step, and doctrine delivery by hand with the propagation script. The plan remains as the record of its design and its readings.

| Metric | Value |
|---|---|
| Hub tests, start / end | 566 / 566 |
| Agents deployed | 0 |
| Model runs | 1 probe, `claude -p` on Nidhogg, 2 turns, $0.045 |
| Repositories surveyed on this box | 20 with `.claude/commands` and a GitHub remote |
| Of those, CI on `pull_request` | 7 |
| Private repositories where branch protection is available | 0 of 18 |
| Reference integrity at close (M2) | 0 MISSING of 57 paths |
| Hub commits this session, before this doc | 3 |

---

## Work Completed

### 1. Session start, and a day's work left uncommitted

The pull fast-forwarded one commit from the Windows side (`dc11844`, the `assay` adoption feedback review). The tree held the PICKET plan (253 lines), its round 1 review (115 lines) and one task line, all from 2026-10-29, with no session doc for that day. Check 7 over the index with this machine's six-term list printed no hit; the secrets check printed clean; the three landed as `a836838`. The docs-feed memory was corrected the same hour, since the 2026-10-29 rulings had settled three of the decisions it listed as owed.

### 2. Measurements for the open items

- **The survey.** Every repository under the GitHub projects directory with a `.claude/commands` directory: visibility, default branch, last push, workflow files and their triggers, branch protection by API, rulesets by API, unread notification, delivery-mark lines. Output filtered through the private-term list before reading: 0 lines withheld. Seven repositories run a workflow on `pull_request`; `propter` has no workflow. The protection endpoint answered `403 Upgrade to GitHub Pro or make this repository public` for all eighteen private repositories and `404 Branch not protected` for the two public ones.
- **A1, first reading.** In a scratch repository under the scratchpad: `claude -p --permission-mode auto --permission-prompts none --max-turns 12 --strict-mcp-config --model claude-sonnet-5-5 --output-format json` with a four-step prompt. All four files written, three under `.claude/`; `subtype` `success`, `num_turns` 2, `permission_denials` `[]`, 7 s, $0.045; the classifier's calls billed on `claude-haiku-5-5`. The box reading as the service account was still owed when the plan was shelved.
- **A4, first reading.** `/usr/bin/time -v` around the same run: maximum resident set 276 MB.
- **A6.** `gh pr list --state all` on eight repositories: 0 pull requests on seven; `daily_weather` 65, 56 merged, median open-to-close 0.0 days, longest 300, 5 open at 4 to 17 days. Unread notifications on this box: 24 days old in three repositories; `stx-server`'s holds 2 entries, `veil-engine`'s 8, `magic-movies`' 13.
- **Propagation dry run.** 23 clones listed; every mark at 17 of 17 headings except one clone with no mark; 0 lines withheld by the term filter.

### 3. The rulings of 2026-10-30 and the fork design

The user chose the canaries, the fork boundary and the model in one question round. Before rewriting D3, D4, 0c and 0e, three GitHub mechanics were pinned from GitHub's own pages: a fine-grained token "is limited to access resources owned by a single user or organization" and is listed as unsupported to "contribute to repositories where the user is an outside or repository collaborator", so the service account's token had to be a classic `repo`-scope one; fork pull request workflows in private repositories are a per-repository setting running with a read-only token and no secrets; and a private repository can be forked by a collaborator only "if the owner permits forking". `gh pr list --head` rejects the `owner:branch` form (its help text says so), so D2's idempotency guard moved to the REST `pulls?head=` endpoint. A9 was added for the fork mechanics with the Pro upgrade as its fallback. Twenty-one hunks in the plan, two in the task line, `f695872`.

### 4. The shelving of 2026-11-02

The user's words, on being reminded why a service account was needed: "that is a clever option - but that is too much. we don't need it ... I'd rather scrap the automation effort than build a second GitHub account." The plan's Status reads Shelved with a dated Status Log line; the task line moved to Completed with the rulings and readings; the register task narrowed to its pull half; the CI-workflow task notes that the scheduled docs check is out; the Focus was rewritten with hand delivery and five owed decisions. Three memory files changed and one feedback memory was added so the next session does not re-propose an account or a fee. `8201d55`.

---

## Claims

| Claim | State | Evidence |
|---|---|---|
| The hub suite passes at `8201d55` | tested | `.venv/bin/pytest -q` at close → `566 passed, 1 warning in 5.63s` |
| Reference integrity is clean with the Focus rewritten (M2) | tested | check 5 file pass at close → 0 MISSING of 57 paths; directory pass printed nothing |
| The 2026-10-29 files are committed | written | `git log --oneline -1 a836838` → `[doc] CONOP PICKET: the plan, its round 1 review, and the task line, from the 2026-10-29 session`; `git status --porcelain \| wc -l` → `0` |
| Auto mode under `-p` with prompts set to none writes under `.claude/` on Nidhogg with zero denials | observed, 2026-10-30 | the A1 probe: `subtype success, num_turns 2, permission_denials []`; `git status --short` in the scratch repo listed `.claude/commands/probe.md`, `.claude/doctrine-delivered`, `.claude/commands/existing.md` modified, `docs/sessions/a1.md` |
| `--output-format json` carries `permission_denials` | observed, 2026-10-30 | `jq 'has("permission_denials")'` on the result → `true` |
| The probe's peak memory was 276 MB | observed, 2026-10-30 | `/usr/bin/time -v` → `Maximum resident set size (kbytes): 276028` |
| Branch protection is unavailable on every private repository here | observed, 2026-10-30 | `gh api repos/<owner>/<repo>/branches/main/protection` → `403 Upgrade to GitHub Pro or make this repository public` for 18 of 18 private; `404 Branch not protected` for the 2 public |
| Seven candidate repositories run CI on `pull_request`; `propter` runs none | observed, 2026-10-30 | `grep -lE '^\s*pull_request' .github/workflows/*.y*ml` → 1 file in each of `stx-server`, `schelling-point`, `hallmark`, `fist`, `veil-engine`, `daily_weather`, `magic-movies`; `propter` has no `.github/workflows` |
| No candidate canary has ever had a pull request | observed, 2026-10-30 | `gh pr list --state all --limit 100 --json ...` → 0 rows for seven repositories, 65 for `daily_weather` |
| A fine-grained token cannot act for a collaborator | observed, 2026-10-30 | GitHub's token page, fetched: "contribute to repositories where the user is an outside or repository collaborator" listed as unsupported |
| `gh pr list --head` takes no `owner:branch` form | observed, 2026-10-30 | `gh pr list --help` on gh 2.102.0 → `("<owner>:<branch>" syntax not supported)` |
| The plan's Status reads Shelved | written | `grep -c '^\*\*Status\*\*: Shelved 2026-11-02'` → `1` |
| PICKET is in Completed and out of the Focus | written | `grep -c '^- \[x\] 2026-11-02: CONOP PICKET shelved'` → `1`; the Focus names PICKET once, as the shelved sweep; active lines `70` |
| No private term in the index or the unpushed commits | observed | check 7 at close over the index and `3` unpushed commits, 6-term list: no FAIL line; counts only |
| The box reading of A1 and the container reading of A4 | UNVERIFIED: the plan was shelved before Wave 0; neither will be taken | |

Overclaims the user caught this session: 0

Overclaims a reviewer caught this session: 0

No reviewer ran this session. One statement was corrected before anyone relied on it: the first summary of the open decisions listed decision 7 as superseded by PICKET, as the 2026-10-29 task line said; with PICKET shelved it returns to the owed list, and the Focus and the memory say so.

---

## Key Decisions

| Decision | By | Rationale |
|---|---|---|
| Canaries `stx-server`, `schelling-point`, `hallmark` | the user, 2026-10-30 | All three run CI on pull requests; `propter` runs none and would have made its pull request a rubber stamp |
| The write boundary by ownership (forks of a service account), not by rule | the user, 2026-10-30 | Branch protection on a private repository needs GitHub Pro; a fork the account owns is a boundary GitHub enforces at no fee |
| `claude-sonnet-5-5` | the user, 2026-10-30 | The plan's pin, probed the same day, on auto mode's list |
| Shelve PICKET | the user, 2026-11-02 | A second GitHub account and a paid plan are both unnecessary; the local programmatic options stand; stopping beats carrying either |
| Commit the 2026-10-29 work on `main` before anything else | the lead | Lead-only doc work lands on `main`; a day's work with no commit and no record is the first thing a session start should fix |

---

## Pillar Compliance

| Pillar | Status | Notes |
|---|---|---|
| **Simplicity First** | PASS | The session ended by removing a service, two credentials and an account from the plan rather than adding them |
| **Shift-Left Testing** | PASS | No production code changed; the suite ran at every commit |
| **Config-Driven** | PASS | Nothing hardcoded; the opt-in list the plan proposed never left the plan |

---

## Lessons

1. **Measure the platform's permission model before designing a boundary on it.** D3, D4 and 0c rested on branch protection that no measurement had checked; one API call per repository found it paid, and the design that replaced it cost the whole plan.
2. **Name a design's standing costs in the first sentence.** The fork design was presented as clever before its price (an account, a token, four forks, per-repo settings) was weighed with the user. The user shelved the effort the moment the price was clear. The feedback memory written this session says to lead with the cost.
3. **A probe on the wrong box still de-risks.** The Nidhogg A1 run showed auto mode writing `.claude/` under `-p` before any NAS work; had it failed, Wave 0 would never have started.
4. **A session that skips `/session-end` leaves its work for the next session start to find.** The dirty tree was the only record of 2026-10-29; the first commit of this session was that day's.

---

## Commits

| Hash | Subject |
|---|---|
| `a836838` | [doc] CONOP PICKET: the plan, its round 1 review, and the task line, from the 2026-10-29 session |
| `f695872` | [doc] CONOP PICKET: three rulings of 2026-10-30 and the first readings of A1, A4 and A6 |
| `8201d55` | [doc] CONOP PICKET shelved 2026-11-02: the user stops the automation rather than add a GitHub account or a paid plan |
| this doc's commit | [doc] Session 2026-10-30: PICKET's rulings measured, then shelved; the Focus rewritten; this record |

---

## Next Steps

1. The user rules on the five 2026-10-22 decisions still owed (Focus step 1).
2. Read the 2026-10-06 cycle's consumption records, then the cycle that carries entries H and P, delivered by hand (Focus step 2).
3. Build the register's pull half test-first as a `/session-start` step, gap G13's collector (Focus step 3).
4. CONOP SEXTANT Wave 0 and CONOP DISPATCH's rulings (Focus steps 4 and 5); the work-terminal list (step 6); picture slice 3 (step 7).
