# Planning Retrospective — swimming-analytics (2026-07-17)

**Author**: `retro-swimming-analytics` agent (read-only, commissioned from `tacsop`)
**Charter**: find multi-session churn episodes; classify PREVENTABLE-BY-PLANNING vs DISCOVERY-PRICED-IN vs MIXED (hindsight-bias guard); map each to CONOP/OPORD format elements; surface process gaps a format cannot fix. Part of the four-repo validation pass for `docs/plans/CONOP-FORMAT.md` / `OPORD-FORMAT.md`.

---

Corpus read in full: 8 session docs (`docs/sessions/`) + 4 plans (`docs/plans/`) + `docs/tasks.md`. Repo not modified.

---

## EPISODE 1 — Plan-vs-Actual alignment algorithm abandoned (length-level NW → rep↔lap NW)
- **Docs:** `docs/sessions/20260629_plan_vs_actual_fixes_and_export.md`; plan `docs/plans/20260628_plan_vs_actual.md`.
- **Consumed vs. should-have:** ~0 wasted *implementation* sessions, but a fully-detailed 5-wave plan section was written then discarded. Planning waste, near-zero execution waste.
- **What happened:** The plan specified (Wave 2) a length-level global Needleman-Wunsch aligner and built ~4 waves of dependent detail on it (OD-3 isolation classifier, OD-4 adherence formula, full test tables). A live spike during the code-reviewer pass scored "49% garbage" — the +100yd warmup surplus cascaded misalignment — and proved the isolation-classifier wrongly relabeled a genuine backstroke. The bottom "Post-Review Locked Decisions" section (R1, R3) *replaces Wave 2* with rep↔lap alignment and drops the classifier, before any code shipped.
- **Classification:** MIXED. The failure mode was cheapest to learn by spiking (DISCOVERY-PRICED-IN); but detailing Waves 2–5 + two open-decisions on an unvalidated core before spiking it was avoidable plan rework.
- **Most-helpful artifact element:** Enemy-Forces (risks) — *correctly priced*. The register named "NW wrong alignment on warmup" as **Medium**, mitigated by "golden test." It was fatal. Naming ≠ sizing.
- **Process gap a format can't fully fix:** Maximum detail committed to a load-bearing algorithm before the cheap validation (the spike) that would kill or vindicate it. A format can add a "spike the load-bearing core before detailing dependent waves" gate; judging *what is load-bearing* still needs skill.

## EPISODE 2 — Rest-lap rule wrong for ~2 weeks; silently erased kick sets
- **Docs:** `docs/sessions/20260624_garmin_swim_parser.md` (introduced) → `docs/sessions/20260708_kick_laps_and_lossless_plan_record.md` (corrected); plan `docs/plans/20260623_garmin_mapping_and_tests.md` (R1, bug #5).
- **Consumed vs. should-have:** Defect lived ~2 weeks; correction + data-repair took a large chunk of the 07-08 session, and **3 stored sessions were found corrupted and had to be re-synced/healed** (06-05 28.6→60%, 06-30 76.9→100%, 07-07 81.2→100%). Should have been caught at the parser's birth.
- **What happened:** `is_rest_lap` = "swimStroke key absent → rest." True on the one sample workout, false in general: kick/drill laps also omit the key while carrying real distance. A 6x50 kick set (300 yd) was silently dropped (stored laps 82 lengths vs. summary 94). Corrected to key-absent AND distance-free.
- **Classification:** MIXED, leaning PREVENTABLE-BY-PLANNING. Seeing kick laps behave this way needs a kick-set fixture (DISCOVERY); but the plan (a) flagged the rest-lap heuristic as fragile in R1 yet mitigated only with "name the predicate + one test," and (b) in R2 separately noticed IM/kick laps carry `averageSWOLF:0.0`/`totalNumberOfStrokes:0` — two facts in the same doc, never crossed.
- **Most-helpful artifact element:** Assumptions — an explicit "is 'rest' really the ONLY lap type that omits swimStroke? how would we know, what's the blast radius?" Secondarily Exit-criteria: the eventual catch was a *lap-length-sum == summary activeLengths* sensor anchor; the original test used only a summary-level identity that cannot detect dropped laps.
- **Process gap a format can't fix:** The risk was registered but under-mitigated, and no one re-challenged R1 when R2 surfaced contradicting evidence. An analysis miss, not a format miss — though "per assumption: falsification test + blast radius" would raise the catch odds.

## EPISODE 3 — Original assumed-field Garmin mapping thrown away, rebuilt capture-first
- **Docs:** `docs/sessions/20260622_scaffolding_bootstrap.md` (found ~1,500 lines untested, wrong mapping) → `docs/sessions/20260624_garmin_swim_parser.md` (rebuilt); plan `docs/plans/20260623_garmin_mapping_and_tests.md`.
- **Consumed vs. should-have:** Pre-existing `garmin_client.py`/`data_parser.py` (~480 lines of parsing) built against *assumed* field names — wrong endpoint + five wrong fields — ultimately deprecated/deleted. Rebuild took one disciplined session.
- **What happened:** Initial code read `get_activity_typed_splits.splits` instead of `get_activity_splits.lapDTOs`, plus five field errors (SWOLF casing, cm-vs-m pool length, missing IM_BY_ROUND, rest-key detection, activeLengths). The 06-24 session captured real payloads first, confirmed every field live, then rebuilt via test-first TDD with a correctness anchor.
- **Classification:** PREVENTABLE-BY-PLANNING — building a parser against undocumented API fields without a single captured payload is the root cause; one "capture real data before coding the mapping" step prevents all of it. Caveat: the original code predates the documented process, and the *correction* was exemplary.
- **Most-helpful artifact element:** Assumptions (every field name was unverified) + TCS-detail (the rebuild plan specified exact fixture-anchored behaviors).
- **Process gap a format can't fix:** None — this is the case the process was introduced to eliminate, and it did.

## EPISODE 4 — Moving-time pace correction (latent, single-session fix)
- **Docs:** `docs/sessions/20260628_detail_view_and_metric_corrections.md`; related plan `docs/plans/20260624_dashboard_wiring.md`.
- **Consumed vs. should-have:** One session to fix; latent 06-24→06-28. Low churn.
- **What happened:** Session/lap pace computed over *total* time (rest included) → 3:17/100m instead of 1:43. The dashboard-wiring plan (v3, 06-24) had *already* corrected the sibling metric (stroke-rate) to a moving-time denominator and added `moving_duration_s`. Same insight applied to one derived metric but not to pace.
- **Classification:** PREVENTABLE-BY-PLANNING (minor). The insight + field existed on 06-24; a "which other metrics share this denominator?" sweep folds pace in.
- **Most-helpful artifact element:** Exit-criteria / consistency check ("propagate a formula correction to all metrics sharing the denominator"). Low blast radius.
- **Process gap a format can't fix:** None — a checklist item covers it.

## EPISODE 5 — Uncommitted work with no session doc (recurred twice)
- **Docs:** `docs/sessions/20260628_detail_view_and_metric_corrections.md` ("large uncommitted change set with no session doc") and `docs/sessions/20260629_plan_vs_actual_fixes_and_export.md` ("the entire, never-committed Plan-vs-Actual feature, Waves 0–6, ~1,300 LOC, no commits and no session doc").
- **Consumed vs. should-have:** No re-done work, but two sessions each had to *reconstruct intent from the diff* before proceeding — avoidable overhead.
- **What happened:** A prior session's plan-driven 6-wave feature landed as one uncommitted blob spanning a session boundary. The plan explicitly defined each wave as "a shippable vertical slice … before the next wave begins," yet all six arrived un-checkpointed.
- **Classification:** Not a planning-*format* failure (the format had wave checkpoints). A discipline/ownership gap — checkpoints were prose, not commit-gates.
- **Most-helpful artifact element:** NONE (format-wise). Lesson: wave checkpoints must be *commit-gates with an owner*, not descriptive prose.
- **Process gap a format can't fix:** Exactly this — strongest evidence in the corpus that OPORD "checkpointed waves" need enforcement teeth, not just wording.

## EPISODE 6 — Real-DB schema-version drift 500'd /workouts
- **Docs:** `docs/tasks.md` (2026-06-29 completed entry); plan `docs/plans/20260628_plan_vs_actual.md` (Schema Evolution v3→v5).
- **Consumed vs. should-have:** Part of one session to diagnose + self-heal + add a regression test.
- **What happened:** On-disk DB stamped `user_version=6` but still carried v2 schema — an intermediate build advanced SCHEMA_VERSION before its migration blocks landed. Invisible to tests (suite uses fresh in-memory DBs that create_all the full table). Fixed by making setup() self-healing.
- **Classification:** DISCOVERY-PRICED-IN / test-strategy gap — a plan can't stop an implementation putting the PRAGMA bump ahead of the ALTER. The plan's schema section was correct.
- **Most-helpful artifact element:** NONE (weakly Exit-criteria: "test migration on a *populated prior-version* DB, not just fresh in-memory"). A shift-left gap, not a format gap.

*(Non-qualifying, noted: `docs/sessions/20260701_claude_settings_hygiene.md` — `.claude/settings.json` committed with personal config then reverted (PR #8→#9). Config hygiene, one extra PR, not planning-preventable.)*

---

## Positive counter-examples (process working — guards against over-reading the failures)
- **garmin_client.py retirement, deferred cleanly:** `20260623` plan D1 scoped the 9-call-site retirement *out* as too big, deferred it to `docs/plans/20260624_dashboard_wiring.md`, executed in `20260625` (Block 5). Large change split + deferred with a named follow-up — no churn.
- **Graph-vs-SQL storage decision, debated up front:** `docs/plans/20260624_persistence_layer.md` evaluated three graph options vs. SQL core, chose SQL, parked graph as a gated Phase-2 item. Decided *before* building — exactly what a CONOP approaches-considered section is for.

---

## SUMMARY
- **Total qualifying episodes:** 6 (3 primary: E1, E2, E3; 3 secondary: E4, E5, E6). Plus 1 non-qualifying noted and 2 positive counter-examples.
- **Classification counts:** PREVENTABLE-BY-PLANNING: 2 (E3, E4). MIXED: 2 (E1, E2). DISCOVERY-PRICED-IN: 1 (E6). Process-discipline gap outside any plan format: 1 (E5).
- **Single strongest lesson for CONOP/OPORD format design:** A risk/Enemy-Forces section earns its ink only if every load-bearing assumption carries (a) a validation action *sized to its blast radius* and (b) an explicit "validate before building dependent detail" gate. Both MIXED episodes (E1, E2) had the fatal risk **named in the register** and both under-priced it ("we'll add a golden test," "name the predicate + one test") instead of spiking or fixture-covering it first. The format should force, per risk: a falsification test, the blast radius if wrong, and a checkpoint that cheap validation *precedes* expensive detailing. Naming a risk and deferring its mitigation to "a test later" is the recurring failure mode. Close second, from E5: wave checkpoints must be **commit-gates with an owner**, or a whole feature bypasses them in one uncommitted blob.
- **Live documents or shelf-ware:** Plans were genuinely **live during their planning-and-implementation window** — every plan carries an amendment/locked-decisions section responding to reviewer challenges and live spikes (the plan-vs-actual plan literally rewrites its own Wave 2), and sessions cite by name which plan they implement. They were **not** updated after reality diverged post-merge (the disproven rest-lap rule was corrected in the session doc and architecture.md, never back in `docs/plans/20260623`), had no named owner, and weren't re-read across the multi-week gap — defensible for point-in-time proposals, but exactly how a stale baked-in assumption (E2) survives.
