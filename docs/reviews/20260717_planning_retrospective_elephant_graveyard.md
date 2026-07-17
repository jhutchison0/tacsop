# Planning Retrospective — elephant-graveyard (2026-07-17)

**Author**: `retro-elephant-graveyard` agent (read-only, commissioned from `tacsop`)
**Charter**: find multi-session churn episodes; classify PREVENTABLE-BY-PLANNING vs DISCOVERY-PRICED-IN vs MIXED (hindsight-bias guard); map each to CONOP/OPORD format elements; surface process gaps a format cannot fix. Part of the four-repo validation pass for `docs/plans/CONOP-FORMAT.md` / `OPORD-FORMAT.md`.

---

Repo: `/home/jhutchison/projects/github/elephant-graveyard`. Read-only. 57 session docs + 8 review artifacts triaged; 6 candidate clusters deep-read against `docs/plans/`.

---

## EPISODE 1 — The Great Pivot: audio-driven cue *generation* → director's-notes authoring

**Session docs:** `20260307_audio_analysis_pipeline.md`, `20260307_knowledge_graph_build.md`, `20260308_analyze_track_orchestrator.md`, `20260308_conop005_phase_a.md`, `20260308_conop005_phase_bc.md`, `20260309_opord001_speaker_diarization_build.md`, `20260310_opord001_first_real_pipeline_run.md`, `20260310_opord001_full_pipeline_run.md`, `20260310_conop008_semantic_knowledge_graph.md` → pivot at `20260311_directors_guidance_and_task_system.md` + `20260311_conop009_implementation.md`.
**Sessions consumed vs. should-have:** ~12–16 sessions built the audio→diarization→KG→semantic-cue pipeline (Mar 7–10). Audio-analysis-for-sync and KG-as-understanding retained value; the choreography-*authoring* purpose — the auto-derived 103-cue Be Prepared and CONOP 008's semantic cue engine — was superseded ONE DAY after CONOP 008 was declared complete. Roughly 3–5 sessions of net cue-generation effort were stranded (post-pivot grep: zero substantive reuse of the semantic-cue/diarization stack in the 30+ later sessions).

**What happened:** For a month the mission executed bottom-up: analyze audio, build a knowledge graph, generate LED cue suggestions. On 2026-03-10 the SME called CONOP 008 "the plan we have been building toward." On 2026-03-11 the director's handwritten notes were transcribed, the team declared director's intent the "primary source of truth," archived the audio-derived `be_prepared.py` as `_legacy`, and rebuilt top-down from notes (CONOP 009). The semantic cue engine never drove the actual show.

**Classification:** MIXED. Learning that bottom-up audio features don't capture artistic intent had real discovery value, and the analysis/sync infra was reusable; but committing ~12+ sessions to a cue-*generation* engine before establishing whether the human director would supply authoritative cues was an avoidable bet.
**Format element that would have helped most:** Mission-intent + Non-goals — an explicit "audio informs sync/understanding; it does NOT author final choreography — the director does" would have reframed the pipeline as an aid, not an authoring path.
**Process gap a format can't fix:** Every SME review drew the mission flow as `Director's intent → … → LED choreography` with intent at the FRONT, yet the build was sequenced intent-LAST. The plans encoded the right dependency in prose but nobody used it to order the build waves. A dependency stated but not used to drive sequencing is the core failure.

---

## EPISODE 2 — Constellations: astronomical accuracy → three theatrical remaps

**Session docs:** `20260314_conop011_constellation_sky_maps.md`, `20260315_conop011_constellations_and_clouds.md` (build) → `20260404_starfield_config_authority_and_constellation_scale.md` (remap #1, scale=2.0), `20260405_theatrical_constellation_remap.md` (remap #2, theatrical replace), `20260405_ground_cover_refit_conop.md` (remap #3 planned, CONOP 014). Plan + review: `conop_011_constellation_sky_maps.md`, `conop_011_sme_review.md`, `conop_014_ground_cover_refit.md`.
**Sessions consumed vs. should-have:** ~2 build + 3 remap passes. ~2 remap sessions were avoidable.

**What happened:** CONOP 011 built astronomically-accurate constellations with aspect-ratio correction. On the 16-strip grid the shapes were unrecognizable (Big Dipper bowl 1.3 strips wide; Orion's belt 3 stars on one strip). Remap #1 tried `constellation_scale=2.0`; still overlapping/unreadable. Remap #2 replaced the raw coordinates with theatrical placements ("planetarium adapts proportions to its dome"). Remap #3 was forced separately when the first hardware photos showed ~4 ft rocky ground cover occluding 37–73 LEDs (4–5× the `sky_floor=15` estimate).

**Classification:** MIXED. The readability remaps (#1–#2) are the preventable part; the occlusion remap (#3) is DISCOVERY-PRICED-IN — ground-cover height was unknowable until hardware was mounted.
**Format element that would have helped most:** Approaches-Considered (astronomical-accurate vs. theatrical-recognizable, as a forced either/or) + a concrete Exit-criterion. The SME review DID flag "Risk 1: readability" but rated it LOW and its only exit test was "recognizable to a human viewer" (TCS #10) — subjective and unfalsifiable. A checkable standard ("Big Dipper bowl ≥ 4 strips wide, verified on simulator") would have forced the theatrical choice in Phase A, before code.
**Process gap:** The risk was named in the review, then filed and never tracked to closure — Phase E "visual verification" passed a vague check, and the same risk resurfaced weeks later. Named risk with no falsifiable exit criterion = decoration.

---

## EPISODE 3 — CONOP 006: viewer built with shared-global-scope JS, crashed on init

**Session docs:** `20260308_graph_visualization_suite.md` (CONOP 004 build) → `20260308_conop006_js_scope_fix.md` (fix), plus a 4-artifact review apparatus: `audit_conop006_scope_collisions.md`, `redteam_conop006_iife_review.md`, `test_conop006_verification.md`, `sme_conop006_blueforce_review.md`. Plan: `conop_006_viewer_js_scope_fix.md`.
**Sessions consumed vs. should-have:** 1 same-day fix (should have been 0), but with disproportionate review overhead (~50 KB of agent review for wrapping 9 files in IIFEs).

**What happened:** The Cytoscape viewer (CONOP 004) loaded 9 vanilla-JS files as plain `<script>` tags sharing global scope, each declaring top-level state (`let _cy`, `const OPACITY_ACTIVE`…). Redeclaration `SyntaxError`s prevented the viewer from ever initializing. CONOP 006 fixed it by IIFE-wrapping all files — then spawned a full audit + red-team + test + SME chain.

**Classification:** PREVENTABLE-BY-PLANNING. With 9 files sharing one global namespace, name collisions were a near-certainty; a module-isolation convention decided at CONOP 004 architecture time avoids both the crash and the entire remediation cycle.
**Format element that would have helped most:** TCS-detail / Non-goals — a stated "no bare top-level globals; every viewer file is IIFE/namespace-isolated" constraint in the CONOP 004 architecture.
**Process gap:** Review weight wildly exceeded risk. A mechanical, well-understood fix drew four separate agent reviews. The format standard should let effort scale to risk, not mandate a full buddy-check chain for a deterministic refactor.

---

## EPISODE 4 — Show-day Windows/network deployment discovery burst

**Session docs:** `20260406_network_setup_tooling.md`, `20260407_production_hardening.md`, `20260408_wsl2_firewall_lesson.md`, `20260408_network_config_cleanup.md`, `20260408_windows_compat_packet_fix.md`, `20260408_windows_compat_vine_diagnosis.md`.
**Sessions consumed vs. should-have:** ~6 sessions compressed into the final 3 days before the 2026-04-08 show. Much was irreducible; ~2 sessions' worth was foreseeable and could have been spread out.

**What happened:** Six weeks of development ran on WSL2/Linux against a simulator. Every deployment reality landed at once at the venue: `noise` C-extension won't compile on Windows (pure-Python fallback written on-site), `cp1252` vs UTF-8 crashes on em-dashes across ~8 files, MTU-based DNRGB packet split cutting through a strip so WLED zeroed 4 LEDs at the seam, and a Windows 11 *dual* firewall (the invisible Hyper-V layer) blocking LAN access to Flask.

**Classification:** MIXED. WLED inter-packet rendering behavior and the Hyper-V firewall are genuine DISCOVERY-PRICED-IN. But "deployment target is a Windows 11 machine" was knowable from day one — the encoding/path/C-extension issues are foreseeable, and `20260408_wsl2_firewall_lesson.md` self-diagnoses that the pre-flight runbook tested outbound UDP but never inbound connectivity from a second device.
**Format element that would have helped most:** Assumptions (named deployment target = Windows) + Branches (pre-decided contingencies: pure-Python fallbacks, an inbound-connectivity pre-flight test) + phasing that forces a real-hardware integration checkpoint early rather than at show-day.
**Process gap:** The deployment runbook existed but its checklist was incomplete (outbound-only), and integration-with-reality was deferred to the very end — a phasing/sequencing failure, not a missing section.

---

## EPISODE 5 — Audio-sync "master clock" lesson re-learned across surfaces (minor)

**Session docs:** `20260308_viewer_audio_led_fixes.md` (viewer, CONOP 007) → `20260315_media_sync_jitter_fix.md` (simulator, explicitly "same pattern") → recurs in `20260314_engine_fix_audio_sync_poison_sun.md`, `20260403_vine_narrative_and_audio_sync.md`, `20260403_vine_fixes_mourning_choreo_audio_sync.md`.
**Sessions consumed vs. should-have:** The "don't fight the browser's media clock with per-frame seeks — use one master clock" fix was solved in the viewer (Mar 8), then re-discovered and re-applied to the simulator a week later (Mar 15), with audio-sync fixes recurring into April.

**What happened:** Two parallel media-playback surfaces (viewer, simulator) each shipped the same per-frame-seeking anti-pattern; the fix found in one was not proactively carried to the other.
**Classification:** MIXED (process/lesson-propagation, not a failed plan).
**Format element that would have helped most:** NONE of the format sections directly — this is a cross-cutting "known-patterns / known-issues register" gap, not a per-plan artifact.
**Process gap:** No shared lessons-learned register meant an architectural fix in one component wasn't applied to its structural twin.

---

## EPISODE 6 — Config-authority (Pillar 6) adopted late, retrofitted across many sessions (minor)

**Session docs:** `20260401_pathlib_migration_config_authority.md`, `20260403_pillar6_config_authority_and_rain.md` (Pillar 6 formalized here), `20260403_grassfield_tuning_and_config_authority.md`, `20260404_starfield_config_authority_and_constellation_scale.md`, `20260405_scar_green_smoke_plume_refactor.md` (Be Prepared config extraction), `20260408_network_config_cleanup.md`.
**Sessions consumed vs. should-have:** The principle was retrofitted across ~5–6 sessions and required consolidating three divergent config-loading patterns (`constants.py`, `song_config.py`, inline YAML) into `show_config.py`.

**What happened:** Song durations and show params were hardcoded/estimated in Python; Pillar 6 ("Config Drives Content") wasn't formalized until 2026-04-03 — even though, per the session doc, "4 of 6 sister repos had explicit config-authority pillars." The late adoption forced retrofit across 10+ choreography modules.
**Classification:** PREVENTABLE-BY-PLANNING. A known, already-standardized sibling-repo principle was available at project start.
**Format element that would have helped most:** Assumptions / stated design principle at project inception (a Pillar from day one, not month two).
**Process gap:** Cross-repo doctrine that already existed wasn't inherited up front — an onboarding/propagation gap, not a plan-format gap.

---

## SUMMARY

**Total episodes:** 6 (4 substantial, 2 minor).
**Classification counts:** PREVENTABLE-BY-PLANNING ×2 (Ep 3 CONOP 006, Ep 6 config-authority); MIXED ×4 (Ep 1 pivot, Ep 2 constellations, Ep 4 deployment, Ep 5 audio-sync). Pure DISCOVERY-PRICED-IN ×0, though Ep 2 (ground-cover occlusion) and Ep 4 (WLED packet behavior, Hyper-V firewall) contain irreducible discovery cores.

**Single strongest lesson for CONOP/OPORD format design:** The most expensive churn did not come from missing plan *sections* — it came from plans that stated the right thing and were never enforced. The mission-dependency order (director-intent-first) was documented but not used to sequence build waves (Ep 1); named risks (constellation readability) had no falsifiable exit criterion and were never tracked to closure (Ep 2). So the format standard must make two things mandatory and machine-checkable, not merely present: **(1)** build-wave order must be *derived from* the stated mission/source-of-truth dependency, and every plan must carry an explicit Non-goal naming what the effort will NOT author or replace; **(2)** every named risk must carry a concrete, falsifiable exit criterion bound to a re-check checkpoint (e.g., "Big Dipper bowl ≥ 4 strips wide, verified at Phase E" — never "recognizable to a human viewer"). A risk register or mission flow that is written but not tracked-to-closure is the failure mode a prettier template cannot cure.

**Were docs/plans live documents or shelf-ware?** Split by lifecycle stage: **live at birth, shelf-ware in middle age.** Up-front discipline was genuinely strong — CONOPs were heavily SME buddy-checked before execution (`sme_conop006/008/013`, `sme_opord001`, `conop_011_sme_review`), sessions consistently cite `Implements: conop_XXX`, and CONOP 009 edited its own plan during execution. But once reality diverged, plans were rarely updated or retired: the pivot orphaned CONOP 008 with no plan-level "superseded" annotation, and the constellation readability risk sat in a filed review that no one re-read until it resurfaced weeks later. The plans drove work at authoring/review time and then went static — read once, seldom revisited.
