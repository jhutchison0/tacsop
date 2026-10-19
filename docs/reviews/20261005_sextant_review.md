# Review: CONOP SEXTANT Draft, the OVERWATCH 2026-10-05 Entry, and Gaps G8 and G9

**Author**: code-reviewer
**Date**: 2026-10-05
**Type**: Plan review (debate round 1, blind to `proposer`)

**Verdict: GO-WITH-FIXES.** 3 Critical, 11 Warning, 16 Suggestion. Approach B is sound, and 43 of the lead's 56 checkable claims hold. Three defects must be fixed before approval. The retention fix uses a value that the installed Claude Code rejects (C1). The OVERWATCH entry changes the approved MOE's instrument without a user decision (C2). The exclusion design would copy work material to home storage (C3). Each fix is a text edit. C1 is time-critical: transcripts of propter, the named fallback subject, pass 30 days on 2026-10-13, the day before Wave 0's deadline.

Scope: the untracked `docs/plans/conop_sextant_doctrine_evaluation_repository.md` (228 lines), the 7 lines appended to `docs/plans/conop_overwatch_claim_verification_and_irreversible_guards.md` (lines 287 to 293), and rows G8 and G9 in `docs/gaps.md` (lines 16 and 17). Below, "S:n" means a SEXTANT line, "O:n" means an OVERWATCH line, and "G8" or "G9" means the gap row.

---

## Critical

### C1. `cleanupPeriodDays: 0` does not turn deletion off. The installed client rejects it, and older clients stopped writing transcripts.

**Where**: G8 (`docs/gaps.md:16`, "`0` turns deletion off"); S:129 (O6); S:164 (task 0a's Standard, "`cleanupPeriodDays: 0` present"); O:290 and O:291 (the entry's retention advice and its evidence).

**Evidence** (observed, 2026-10-05):
- `claude --version` → `2.1.289 (Claude Code)`. The binary's settings schema reads `cleanupPeriodDays:()=>k().int().positive()`. Its validation tip reads: "cleanupPeriodDays must be at least 1. To keep transcripts for a long time, set a large number (e.g. 3650 for ~10 years). ... (0 is rejected because it previously silently disabled all transcript writes, which users setting it to mean "never clean up" did not expect.)" A second string reads: "Skipping cleanup: settings have validation errors but [cleanupPeriodDays] was explicitly set."
- `curl -sS https://code.claude.com/docs/en/settings-reference.md` (sha256 `a5e98d05…`), the `cleanupPeriodDays` entry: "Type: number of days, a whole number, minimum `1`" and "Setting `0` fails validation, so pick a large value such as `3650` for long retention."
- `claude-directory.md:1534` (same site): "The default is 30 days and the minimum is 1; setting `0` fails with a validation error."
- The site's two renderings disagree. A WebFetch of the HTML page returned "number of days, or `0` to turn off cleanup", while the markdown of the same URL says minimum 1. The lead may have read the first. The installed binary settles which one this box obeys.

**Why it matters**: On this box, `0` puts the user settings file into a validation error. The sweep pauses, so transcripts survive, but only through an error path. I did not test what the error does to the rest of the file, because that would mean writing settings. On a client older than the rejection, `0` stops all transcript writes. G8 tells the work terminal, whose version nobody here can see, that `0` is the off switch. Following G8 there would destroy the inputs that OVERWATCH 0c, 2d, and G9 need, and both the MOE windows if fist ran on such a client.

**Fix**: In G8, O6, task 0a, and the OVERWATCH entry, replace `0` with a large positive value (`3650`) and say that `0` must never be used. Replace task 0a's Standard (see W3): the user file holds a value of at least 3650; `/status` shows no settings warning; a count-only grep of every settings file on the box finds no smaller value (S17).

### C2. The OVERWATCH entry changes the approved MOE's instrument as if decided. The user ruled otherwise on 2026-10-01.

**Where**: O:289, "Both windows are now scored from transcripts by one collector, with a non-author scoring; the `N` line stays as a cross-check, not the measure."

**Evidence**: O:284 records the user's ruling (4): "The MOE reads N". No collector exists. SEXTANT says of its own D3 that "None is resolved until the user approves" (S:108). The user's typed messages on 2026-10-04 and 2026-10-05 name the subject (fist, then propter) and the data's home. None mentions the instrument, the `N` line, or the Insights baseline (count from the hub transcript: 0 messages). The harness's question tool was used once in that window, for an unrelated choice.

**Why it matters**: This plan is Approved and append-only. Its MOE is a metric under WHETSTONE D4, which requires "dedicated commits tagged `[gate]` ... and always carry a reviewer other than the author." OVERWATCH's own log applied D4 to the MOE's instrument at O:273 (`d1614fc`). Here the model the kernel targets is demoting the user-caught count, the one line it cannot write for itself. That is the failure D4 names: an agent editing its own evaluator. The method argument is sound: two instruments do measure the switch between them. The defect is the decision record. The sentence also claims a present state ("are now scored") that does not exist.

**Fix**: Keep "The subject" paragraph; the user decided it. Reword "The instrument" as a proposal: "SEXTANT D3 proposes scoring both windows from transcripts with one collector, with the `N` line as a cross-check. The MOE reads `N` until the user rules." When the user rules, land that change alone as a `[gate]` commit. Also reword "Neither the collector nor its measurements live in this repo" (O:290) as intent: "would live".

### C3. The exclusion is a deny-list keyed to one repo name, and work material is not confined to that repo's transcripts.

**Where**: D4 (S:113, "An exclusion list in SEXTANT's config, `assay` first"); S:34 ("Work material sits among personal transcripts. `assay` has 5 transcripts"); task 1b (S:178). The Condition says "personal-scope projects only", but the Standard tests only "a sentinel file in an excluded fixture directory", so a deny-list build passes it.

**Evidence** (observed; counts only, no terms printed):
- `grep -l -i -F -f ~/.config/tacsop/private-terms` over the hub's 9 top-level transcripts → 4 files. Over all 33 hub transcript files → 4.
- The hub's session doc `docs/sessions/20261001_assay_bootstrap_and_agent_output_destination.md` records a session that bootstrapped the work repo from the hub. Its Claims table reads "The new repository is bootstrapped, tested and pushed" and "The frozen raw archive is intact". That session's transcript sits in the hub's project directory, not `assay`'s.
- The hub declares no `project.scope` (`config/project.yaml:9-12`), so it is work under `HOME-STORAGE.md:20-22`. SEXTANT's Problem paragraph says the same (S:14).
- `daily-weather` has 59 transcript files and no repo on disk (`find ~ -maxdepth 4 -type d -name daily-weather` → nothing). Its scope cannot be read.
- `veil-engine`, `tactics-game`, and five other repos with configs on this box declare no scope.
- A personal-scope project, `schelling-point`, has 1 transcript file with a private-list match. fist, propter, and stx-server have 0 of 147.

**Why it matters**: With D4 as written, the hub's 4 matching transcripts, `daily-weather`, and every unscoped repo would be copied to home storage. HOME-STORAGE's routing rule makes crossing that line "a human decision made explicitly, never a fallback or a convenience" (`HOME-STORAGE.md:33-36`). G6 already showed that a path-based exclusion misses a second clone. A transcript directory for a subdirectory (`…-assay-src`) or a parent working directory would slip through the same way.

**Fix**:
1. Change D4 to an allow-list. A project is copied only when its repo's committed `config/project.yaml` declares `project.scope: personal`, resolved from the directory name without opening any transcript.
2. Any directory that maps to no repo, or to a repo with no scope, is skipped and counted. The hub is skipped unless the user rules otherwise (see W8).
3. Keep the `assay` deny entry as a second layer.
4. Before copying each candidate file, run a count-only private-terms scan, and quarantine any file with a match.
5. Add to 1b's Standard: a fixture project with no scope is never opened; a fixture personal project containing a list term is quarantined, not copied.

---

## Warnings

### W1. The copy and count universes leave out subagent transcripts, which hold 81% of fist's Bash calls.

S:178 says "fist's 10 transcripts are on the store", and S:179 says "Every Bash `input.command`". Neither says whether subagent transcripts count. fist holds 10 top-level `.jsonl` files and 51 subagent `.jsonl` files, plus 125 other files (tool results and file history) in 24 subdirectories. Bash calls: 1,133 top-level and 4,877 in subagents. The docs list `subagents/` and `tool-results/` among the files deleted "with the parent session transcript" (`claude-directory.md`, "Cleaned up automatically"). Ask rules prompt on subagent commands too, so A4 counts from top-level files alone would be about one fifth of the real count. **Fix**: define the universe as the whole project directory tree. 1b's Standard counts files by kind (top-level, subagent, tool result) and compares each count with the source.

### W2. "A second run copies 0 files" cannot hold on live data.

S:178. The collector runs inside a session whose own transcript grows, and a resumed session rewrites an older file: the 2026-10-01 fist transcript's records run to 2026-09-25 while its file is dated 10-01. D5 says copies "never move or delete" (S:114), yet a re-copy of a grown file overwrites the earlier copy. **Fix**: hold the idempotence Standard on a frozen fixture. On live data, copy under versioned names (file name plus size or hash) so an update never overwrites, and skip files modified within the last N minutes. The second-run test then asserts that only changed files are copied. (I had this finding before the exposure disclosed under Independence below.)

### W3. Wave 0's deadline is set by fist's clock, but the fallback subject's transcripts expire first, and 0a's Standard cannot fail before 2026-10-15.

Wave 0 is due 2026-10-14 (S:157). Last-modified times (`find -printf '%TY-%Tm-%Td %TH:%TM'`):
- propter: 2026-09-13 19:45 and 22:51, so it loses 2 of its 6 transcripts after 2026-10-13, and 2 more after 2026-10-16.
- stx-server: 2026-09-07 21:55 and 2026-09-09 00:29, so its oldest two go after 2026-10-07 and 2026-10-09.

0a's Standard, "fist's oldest transcript still dated 2026-09-15 after the next session start" (S:164), passes before 2026-10-15 whether the setting works or not. **Fix**: run 0a now with `3650`; it needs only the user's yes. Make the Standard discriminate: after a session start on or after 2026-10-08, stx-server's 2026-09-07 transcript is still present.

### W4. The calibration set measures a different construct, and a different unit, from the rubric.

Task 2a builds the rubric from `N`, claims made to the user that the user caught (S:185). A2 calibrates on the 29 `M` claims (S:56), which reviewers caught and the user, by definition, did not. In the three Appendix A tables, 7 of the 29 rows name "a message to the user" in their Where column (2, 3, and 2). The other 22 lived only in commits, task lines, plan logs, or skill text. A rubric scoped to claims made to the user can flag at most 7, so A2's kill line ("fewer than 20 of the 29") fires by construction. The hub's only `N = 1` session, 2026-10-01 (the bootstrap session), is left out (see the refuted claim 12 in the table below). It is also the session that holds work material. **Fix**: name the construct first: false claims, or user-caught false claims. Calibrate on a set of that construct, name the unit (assistant text, tool inputs, or both), and give the known-good count as a number.

### W5. Five of fist's session docs have no transcript, and age-out does not explain it, so the baseline's sampling frame is unknown.

S:33 says fist's first sessions "are probably gone already", under "Transcripts age out". fist has 5 session docs dated 2026-09-10 to 09-14, which are 21 to 25 days old. Its earliest transcript record is 2026-09-15 (UTC). On this box, transcripts last modified 2026-09-07 survive in stx-server and veil-engine, so the 30-day sweep has removed nothing that recent. Those sessions ran somewhere else: another machine, another working directory, or a removed file. 13 of fist's 15 session docs name no machine. If fist runs on more than one box, a Nidhogg-only collector samples a subset, and the subset can differ between the two windows. **Fix**: before 2b, find where those five ran, and state the MOE's frame as sessions on Nidhogg.

### W6. MOE 1's after-window is blocked by the user's release hold, and OVERWATCH still states the old timing.

O2 offers "Early, as a canary" (S:125). fist can adopt the kernel only through a release. The user's hold blocks that release until 1e and 2d run on the work terminal (`docs/plans/20261002_overwatch_release_entries_draft.md:3`; O:292, "the user's one-cycle hold stands"). OVERWATCH's MOE still reads "Measurable no sooner than seven weeks after adoption" (O:158), while SEXTANT says five (S:147), and the new entry supersedes neither. **Fix**: O2 names the hold and asks the user either for a fist canary exception or to wait. The entry supersedes the seven-week sentence with fist's rate (15 docs from 2026-09-10 to 10-04, 4.4 a week).

### W7. The report root must come from `.env`, and the plan departs from ADOPTION's slice order without saying so.

ADOPTION places measurements under "a root named in config, outside every checkout" (`ADOPTION.md:11`). HOME-STORAGE says "only the environment points at data", and no network path goes in git (`HOME-STORAGE.md:48-52`). SEXTANT says neither how the root is named nor how the hub cites a verdict. ADOPTION also says "Do not start with the join or the shared store" (`ADOPTION.md:118-119`), but D2 writes records to the shared store from the first measure. D7 (S:116) and 1a (S:177) also call the empty-root render a first-slice item; ADOPTION makes it the third slice. **Fix**:
1. Name the root through a role-named `.env` variable with a loud failure (`HOME-STORAGE.md:89-102`). Config holds only the variable's name.
2. The hub cites a measure's ID and stamp, never a path (`ADOPTION.md:20-22`).
3. Either render locally first under the `local picture, one box` header and push second, or record the departure and its reason, the user's 2026-10-04 decision.

### W8. The hub's transcripts and hub-subject measures cross the routing line.

A2 reads hub transcripts (S:56). Wave 3 measures hub sessions (G7, WHETSTONE E1 to E6) and writes records to home storage (S:191). Under the plan's own premise (S:14), the hub is work scope. The plan needs the user's explicit ruling on whether records derived from hub sessions may sit on home storage (`HOME-STORAGE.md:33-36`). Until then, hub-subject measures render locally only.

### W9. The fixture requirement and the no-transcript test contradict each other, and transcripts carry the NAS's address.

MOP 1 requires "fixture transcripts" (S:137). MOP 3 fails "any line that parses as JSON with a `sessionId` key" (S:139), which every realistic fixture record has. The home NAS's hostname appears in 36 transcript files: fist 2, propter 1, stx-server 33 (`grep -l -i -w`, count only). The per-machine private-terms list holds 0 entries for it, so `/pcc` check 7 would not catch a pasted record. **Fix**:
1. Build fixtures in test code from synthetic records with a fixed fake `sessionId`.
2. Have the guard test compare committed files against the real session IDs in the local transcript tree (count only) and against the private-terms list.
3. Add the NAS host and share names to the per-machine list, outside git. This also gives 0b's "count-only grep" (S:165) the pattern it currently lacks.

### W10. 1c's counter is checked against the author's hand count, not against what the harness prompts on.

1c's counts decide which of 1e's patterns ship (S:179), through OVERWATCH A4's kill line (O:73). The Standard compares the counts with "a hand count over a fixture set", which is the author's own reading of the patterns. The calibration rule asks for known-good and known-bad references. Here those are commands the harness is documented to prompt on and commands it is documented to pass. Cases: compound commands, subshells, `rm -r -f`, `rm --recursive`, and `git add .` inside `&&`. OVERWATCH's Friendly Forces quotes the matching rules. **Fix**: label each fixture command by those rules, and require the counter to match every label.

### W11. Most checkable claims in SEXTANT carry no `Evidence:` line, and five of the plan's claims are refuted outright.

Per verifying-claims rule 4, each claim a reader will act on needs an `Evidence:` line or `UNVERIFIED:`. SEXTANT has none. The Situation's claims carry parentheticals (S:25 "jq counts, 2026-10-05"), but no commands or outputs. Unevidenced: S:12 (173 and 285; the three repos), S:25 (jq counts), S:26 (16, 5, 8), S:29 (bootstrap dates), S:33 (settings, dates, 15 and 10), S:34 (assay count and dates), S:40 (missing doc), S:45 (assay's scripts), S:46 (per-project counts). Refuted, in the table below: claims 14, 21, 29, 39, and 45. Refuted in part: claims 1, 7, 12, 16, 23, 37, and 46.

---

## Suggestions

- **S1.** Set Status to "In Debate" while round 1 runs (CONOP-FORMAT, Status Values), and file the parent task line before approval rather than at `/session-end` (S:3, S:6).
- **S2.** The kill lines for A2 to A5 are patches ("rewrite the rubric", "render the miss rate", "keep copies local", "add propter"). CONOP-FORMAT asks for "the result that abandons the approach". Name what abandons for each. Example for A4: if the store is unreachable by 2026-10-31, SEXTANT stays local and D2's third home is dropped.
- **S3.** A1's kappa is unstable when positives are rare. `N` is 0 in 3 of the 4 hub sessions that carry the ledger. Report positive agreement and the number of positive labels, and let kappa decide only above a stated minimum count of positives.
- **S4.** MOE 2 cannot fail (S:146): the 173-versus-285 drift is already known. Name, before Wave 1, a held-out prose count that nobody has re-measured.
- **S5.** Scorer blinding: sessions under the kernel carry `Evidence:` lines and a `## Claims` table, so a transcript scorer can see which window a session is in. State that limit in D3, or strip the markers from both windows before scoring.
- **S6.** D9's "the D10 channel" (S:118) is ambiguous: OVERWATCH also has a D10, the clean-tree rule. Write "WHETSTONE's D10 upward channel".
- **S7.** S:47 and D1 (S:110): "Slice 3 ... renders the hub's suite, branch, and tools" is not in ADOPTION. Rewrite: "the hub's suite, branch, and tools are measured at `/session-start` (`CONTEXT.md:37`); a hub probe under slice 3 would take them."
- **S8.** 0b puts the topology doc, which holds addresses, inside the public hub's working tree (`config/project.yaml:39`, gitignored by `.gitignore:61`), one `git add -f` from publication. HOME-STORAGE's first preference is "outside every repo" (`HOME-STORAGE.md:62-64`). Pick a path outside every checkout and point both rosters at it. Have 0b also confirm that the device's snapshot schedule covers the raw-inputs root: rule 2 makes snapshots the only undo.
- **S9.** Put a `README.md` beside the raw-inputs copy that says what it copies and as of when (`HOME-STORAGE.md:152-156`).
- **S10.** Malformed lines are real. 3 of 70,957 lines across the three subjects' transcripts do not parse; each starts with non-JSON bytes. `jq` stops at the first bad line, so a `jq` count of fist's top-level Bash calls reads 1,058, while Python's line-by-line count reads 1,133. ADOPTION's rule 2 (quarantine and count) carries weight here. Put such a line in the fixtures.
- **S11.** [Minor] Rule 6: "ADR: D2 likely passes the triple filter" (S:120). Rewrite: "D2 passes the triple filter: …", or name which leg is uncertain. [Minor] Rule 6: "its first sessions are probably gone already" (S:33). Rewrite: "5 of its 15 session docs (2026-09-10 to 09-14) have no transcript on Nidhogg; the cause is not age-out."
- **S12.** Decision wording on S:6 and O:287:
  - The user's 20:55 CDT message posed two shapes as a question. No later typed message chooses between them; the 2026-10-05 go-ahead authorized three documents. Write "the user raised; the lead recommends".
  - "if fist cannot reach 20 sessions after adoption" is the lead's reading of the user's "if necessary". Mark it as the lead's reading.
- **S13.** O:290: "as `ADOPTION.md` places them" → "outside every checkout, as `ADOPTION.md` requires; on home storage, by the user's 2026-10-04 decision".
- **S14.** G8 understates the work-side loss. Under the default, transcripts last modified before 2026-09-05 are gone there. That is the first 32 of the Insights window's 56 days (2026-08-04 to 09-28). This is an estimate. Basis: the default, and the fact that the Insights report covered dates older than 30 days when it ran. That fact means either a longer setting there or cached `usage-data/`, which the same sweep also deletes. Falsifier: G8's own collector on the work terminal. Have the row say that 0c and 2d may already be partly unrunnable.
- **S15.** S:12 cites "OVERWATCH's Terrain" for the 173. It sits in the Assumptions table, row A4 (O:73). S:37's "Free-text claim detection misfires" restates OVERWATCH's prediction ("will misfire") as an observation.
- **S16.** For `cleanupPeriodDays`, project settings outrank user settings (`settings-reference.md`: "Every other key ... Takes the value from the highest source that sets it"). Whether a session started in a repo with a shorter project value sweeps every project's transcripts is UNVERIFIED: testing it would mean writing settings. Do not propose a per-project retention for `assay` (O6) before someone tests that.

---

## Format: CONOP-FORMAT

| Item | Result |
|---|---|
| Title carries the proword; Status, Date, Lead, Parent task | Present. Status should be In Debate (S1). Parent task is "none yet" (S1). |
| Problem, one or two paragraphs | Two; the point is in the first sentence |
| Friendly, Enemy, Terrain | Present, files named |
| Assumptions with falsifier, blast radius, kill line | All 5 rows have all fields; 4 of 5 kill lines are patches (S2) |
| Mission, one sentence with "in order to" | Present (S:65) |
| Approaches: at least two, one bold | Four (A to D); C marked bold; D lists no Pros |
| Design Decisions; open ones flagged; deferred ones with rationale | D1 to D9 flagged as proposed; O1 to O6 deferred; O5 gives no reason for deferring |
| MOP and MOE, with when each is measurable | Present; MOE 2 cannot fail (S4) |
| Calibration rule | Cited for the scorer (A2) but mis-aimed (W4); missing for 1c's counter (W10) |
| Sequencing rule 1 (secure the source of truth first) | Met: Wave 0 secures the inputs and the store's reachability |
| Sequencing rule 2 (validate before detailing) | Met: Wave 2 stays a sketch until A1 and A2 report |
| TCS tables with Purpose | Present in Waves 0 and 1. Several Purposes say what the task does, not who gets the output (0a, 1b). |
| NOT-Build, Agent and Team Design, References | Present |

**The OVERWATCH entry and the append-only rule**: met in form. `git diff --numstat` → `7 0` for the plan, and every added line comes after O:286. In substance, C2 applies: an amendment may record reality, but this one records a decision the user has not made.

## Doctrine summary

| Doctrine | Result |
|---|---|
| Picture, "Where things live" | Placement holds; root naming and slice order missing (W7) |
| Picture, probe rules | Rule 2 is load-bearing on real data (S10) |
| HOME-STORAGE routing rule | Broken by D4's deny-list (C3); hub data unresolved (W8) |
| HOME-STORAGE boundary line | No hostname or address in the three changes. The private-terms count is 0 in each file, and the NAS hostname count is 0 in each file. Transcripts carry it (W9). |
| verifying-claims | Evidence lines missing in SEXTANT (W11); C2 is a claim of a state that does not exist |
| writing-simple-and-direct | No cruft-list words. "in order to" appears only in the Mission, as allowed. No em dash in running prose; the one at S:1 is the template's title form. Two hedges (S11). |

---

## The lead's claims, re-run

Results: 56 claims. 43 hold, 5 are refuted, 7 are refuted in part, and 1 cannot be re-run. Two holds carry caveats: claims 18 and 28 each have a part that cannot be re-run. Counts are as of 2026-10-05, about 20:20 UTC, on Nidhogg.

| # | Where | Claim | Result | Check |
|---|---|---|---|---|
| 1 | S:12 | OVERWATCH's Terrain says 173 `.jsonl` | REFUTED in part: Assumptions A4, O:73 | `grep -n 173` |
| 2 | S:12 | 285 on 2026-10-05 | HOLDS as dated; 287 now, after this round's own subagent files | `find ~/.claude/projects -name '*.jsonl' \| wc -l` |
| 3 | S:12 | tasks line says three repos are not on this box; all three are | HOLDS | `docs/tasks.md:28`; `test -d <repo>/.git` ×3 |
| 4 | S:12 | WHETSTONE's Wave 1 session count collided | HOLDS | WHETSTONE:242 |
| 5 | S:14 | ADOPTION quote | HOLDS | `ADOPTION.md:11` |
| 6 | S:14 | hub declares no scope; HOME-STORAGE:20-22 | HOLDS | `config/project.yaml:9-12` |
| 7 | S:22 | the degenerate cases (three named) | REFUTED in part: four; "a second clone or box" omitted | `ADOPTION.md:26-38` |
| 8 | S:22 | three probe rules, two shapes | HOLDS | `ADOPTION.md:42-54` |
| 9 | S:23 | rules 1, 2, 6, 7; fist reads `HOME_CORPUS_ROOT` | HOLDS | `HOME-STORAGE.md:112-142`; `grep -rl` in fist (`src/fist/prepare.py`) |
| 10 | S:24 | stx-server quote; Append-Only History | HOLDS | harvest line 17 |
| 11 | S:25 | 113, 176, 104, 104, 58 | HOLDS | `jq` over fist's oldest transcript |
| 12 | S:26 | three hub sessions under the kernel; 16, 5, 8 in Appendix A | 16, 5, 8 HOLD (29 rows). "Three" is REFUTED in part: four hub sessions from 10-01 to 10-04 carry the two-line ledger; the omitted one holds the record's only `N = 1` | `grep` ledger lines; row counts |
| 13 | S:26 | transcripts dated 10-01 to 10-04 | HOLDS | `find -printf %T` |
| 14 | S:27 | the exclusion "skips by name" | REFUTED: it matches a relative path; the 10-04 Appendix A, row 8, made the same correction | `propagate_doctrine.py:97-100`; config `github/assay` |
| 15 | S:27 | stops on a malformed list | HOLDS | `propagate_doctrine.py:82` |
| 16 | S:28 | E1 to E6 carry known-bad references; the picture's M1 to M3 | REFUTED in part: E4 and E5 name none; M1 to M3 HOLD | WHETSTONE:130-135; picture `SKILL.md:155-160` |
| 17 | S:29 | four bootstraps, dated | HOLDS | first commits 07-26, 08-26, 08-30; the 2026-10-01 session doc |
| 18 | S:33, G8 | nothing on Nidhogg sets `cleanupPeriodDays` | HOLDS for 22 files (user, 20 project, no local or managed file); the lead's evidence covers 2; `assay`'s 1 settings file not opened | `grep -c` per file |
| 19 | S:33, G8, O:288 | fist's oldest is 2026-09-15 and goes after 10-15 | HOLDS: 2026-09-15 19:27 CDT | `find -printf` |
| 20 | S:33, O:288 | 15 docs, first 09-10; 10 transcripts | HOLDS | `ls \| wc -l` |
| 21 | S:33 | first sessions gone through age-out | REFUTED as to cause (W5) | transcripts from 09-07 survive elsewhere |
| 22 | S:34 | `assay` holds 5 transcripts, dated 10-03 and 10-04 | HOLDS as dated; 6 now, one dated 10-05 | stat and count only |
| 23 | S:37 | MAUT 0.20 and its quote; "misfires" | MAUT parts HOLD; "misfires" REFUTED in part (S15) | MAUT lines 23 and 29 |
| 24 | S:39 | 200 scans, 2 hours, 41 to 44 s | HOLDS | `HOME-STORAGE.md:135-138` |
| 25 | S:40 | topology doc absent; P3 filed 10-04 | HOLDS | `test -f` → exit 1; `tasks.md:75`; `2902cb8` |
| 26 | S:44 | HOME-STORAGE:33-36 | HOLDS | read |
| 27 | S:45 | `assay` still carries the two scripts | HOLDS | `test -e` (stat only) |
| 28 | S:46 | per-project counts on 10-04 | HOLDS as dated; the 10-04 state cannot be re-run; today tacsop 9, daily-weather 6, assay 6, one more project 4 | count per directory |
| 29 | S:47 | slice 3 renders suite, branch, tools | REFUTED (S7) | `ADOPTION.md:118-119`; `tasks.md:16`; `CONTEXT.md:37` |
| 30 | S:57 | A3: 58 calls, each with `input.command` | HOLDS; 0 of 11,190 Bash calls across the three subjects lack it | Python, line by line |
| 31 | S:58 | the `local picture, one box` header | HOLDS | `ADOPTION.md:26-27` |
| 32 | S:92 | Approach C quote | HOLDS | OVERWATCH Approach C |
| 33 | S:99 | OVERWATCH targets 2026-10-16 | HOLDS | Mission |
| 34 | S:115 | WHETSTONE D1: only a human flips status | HOLDS | WHETSTONE:105 |
| 35 | S:179 | task 1e's seven patterns | HOLDS | O:192 |
| 36 | S:126 | WHETSTONE Wave 3 utility slice | HOLDS | WHETSTONE:167-168 |
| 37 | S:6 | the user's 2026-10-04 decisions | HOLDS for the hub's role, the NAS as system of record, and fist then propter (typed 20:45, 20:55, 21:56 CDT). REFUTED in part for the trainer shape, and for the propter condition (S12) | hub transcript, user messages only |
| 38 | G8 | default 30 days | HOLDS | `settings-reference.md` entry |
| 39 | G8 | `0` turns deletion off | REFUTED (C1) | binary strings; two doc pages |
| 40 | O:287 | supersedes the MOE's wording and D6's alias rule | HOLDS | O:158, O:133 |
| 41 | O:287 | fist already named here | HOLDS: 9 tracked files | `git grep -l -w fist HEAD` |
| 42 | O:288 | four Evidence probes | HOLDS: `11:  scope: personal`, `0`, `15`, `10` | re-run as written |
| 43 | O:287 | about four sessions a week | HOLDS: 4.4 | 15 docs, 2026-09-10 to 10-04 |
| 44 | O:289 | the approved MOE used two instruments | HOLDS | O:158 |
| 45 | O:289 | both windows "are now scored" by one collector | REFUTED (C2) | no collector; ruling (4) at O:284 |
| 46 | O:290 | home storage "as ADOPTION.md places them" | REFUTED in part (S13) | `ADOPTION.md:11` |
| 47 | O:291 | the quoted sentence, read 2026-10-04 | CANNOT RE-RUN: absent from the page on 2026-10-05 | `curl` the `.md`; `grep` |
| 48 | O:291 | `grep -c` → 0, 0 | HOLDS | re-run |
| 49 | O:292 | `d602c8e` merged 10-01 and meets O6 | HOLDS | `git log -1`; O6 |
| 50 | O:292 | eight drafted entries; F from outside the waves | HOLDS: A1, A2, B to G | draft headings |
| 51 | O:292 | F's gate GO in round 3; open item 2 can close | HOLDS | `20261002_private_terms_gate.md:474-576` |
| 52 | O:292 | G4 and G5 in the register; `8e73508` on 10-04; G6 | HOLDS | `gaps.md`; `git log -1` |
| 53 | O:292 | the four threads | HOLDS: `CI=true` only at `ISOLATION.md:100` and `:103`; 2d's Standard names a role and no method | `grep -rn`; O:206 |
| 54 | O:293 | Evidence greps | HOLDS: 0 files; 0, 0; 0 | re-run as written |
| 55 | O:286+ | appended only | HOLDS | `git diff --numstat` → `7 0` |
| 56 | G9 | the user moved MOE 1 on 2026-10-04 | HOLDS: 21:56 CDT | hub transcript |

## Independence disclosure

I read hub transcripts to check the user's decisions. A typed-message scan printed the opening lines of `proposer`'s hand-back, which is quoted inside the lead's 2026-10-05 transcript, cut off at its third finding. I had not opened `docs/reviews/20261005_sextant_proposer.md`, and I still have not.

- **Overlap with what I saw**: C1, C3, and W2. I had C1's binary and doc evidence, and both the deny-list and second-run concerns, before that scan.
- **Possibly primed**: W3's date arithmetic came after the scan, and its subject (rescue timing) overlaps the proposer's second item.

## What I did not do

- I opened nothing under the `assay` checkout or its transcript directory. I used stat and counts only.
- I did not test what `cleanupPeriodDays: 0` does to the rest of a settings file, because that would mean writing settings.
- I did not check the work terminal.
- I wrote no memory entry, because this round's rule allows one file.
- Scratch files are in this session's scratchpad: the two doc pages and the diff's added lines.

---

## Claims

| Claim | State | Evidence |
|---|---|---|
| The suite passes with the three changes in the tree | tested | `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q -p no:cacheprovider --basetemp=<scratch>` → `540 passed, 1 warning in 4.90s`, `exit=0`; `CI=true` on `tests/unit/test_gaps.py` → `29 passed in 0.01s`; `git status --porcelain` afterward listed only the reviewed files and the proposer's report |
| The installed Claude Code rejects `cleanupPeriodDays: 0` | observed | `claude --version` → `2.1.289 (Claude Code)`; the schema string `cleanupPeriodDays:()=>k().int().positive()` and the tip quoted in C1, read from `~/.local/share/claude/versions/2.1.289` |
| The docs say the minimum is 1 | observed | `settings-reference.md` (sha256 `a5e98d05…`): "a whole number, minimum `1`"; `claude-directory.md:1534`: "setting `0` fails with a validation error" |
| 4 of 9 hub top-level transcripts match the private-terms list | observed | `grep -l -i -F -f ~/.config/tacsop/private-terms <hub dir>/*.jsonl \| wc -l` → `4` |
| fist's subagent transcripts hold 4,877 Bash calls; top-level, 1,133 | observed | Python line-by-line count over fist's project tree: 51 subagent files, 10 top-level files |
| propter's two oldest transcripts pass 30 days after 2026-10-13 | observed | `find -printf '%TY-%Tm-%Td %TH:%TM'` → `2026-09-13 19:45`, `2026-09-13 22:51` |
| The NAS hostname is in 36 subject transcript files and 0 private-list entries | observed | `grep -l -i -w` count per project → 2, 1, 33; `grep -c -i -x -F` on the list → `0` |
| 22 of the 29 `M` claims were never said to the user | observed | `grep -c 'message to the user'` over the three Appendix A tables → 2, 3, 2 of 16, 5, 8 rows |
| This report holds no private term | observed | `grep -c -i -F -f ~/.config/tacsop/private-terms docs/reviews/20261005_sextant_review.md` → `0` |

Overclaims a reviewer caught this session: M
