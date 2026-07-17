# Planning Retrospective — magic-movies (2026-07-17)

**Author**: `retro-magic-movies` agent (read-only, commissioned from `tacsop`)
**Charter**: find multi-session churn episodes; classify PREVENTABLE-BY-PLANNING vs DISCOVERY-PRICED-IN vs MIXED (hindsight-bias guard); map each to CONOP/OPORD format elements; surface process gaps a format cannot fix. Part of the four-repo validation pass for `docs/plans/CONOP-FORMAT.md` / `OPORD-FORMAT.md`.

---

**Corpus read:** 6 session docs (2026-01-16 to 2026-01-17, two calendar days), roadmap.md, CHANGELOG.md, adversarial/research-plan.md, full git history (15 commits, no reverts/rebases, linear with two dev-branch merges). No `docs/plans/`, no `docs/adr/`.

---

## EPISODE 1 — Self-destruct redone (unlink-while-running → fork-and-delete)

- **Session docs:** `20260116_mvp_0_1_3_e2e_packaging.md` (problem observed) → `20260117_self_destruct_fix.md` (redone). Original design set in `20260116_project_initialization.md` (M0.1.2). Spanned ~2 sessions of elapsed time; the actual redo was ~1 session, vs. ~0 extra work if designed right the first time.
- **What happened:** The Unix self-destruct shipped an in-process approach (multi-pass overwrite then `unlink` of its own running binary). The v0.1.3 manual E2E on WSL surfaced `Text file busy (os error 26)` — you cannot open a running executable for writing. The v0.1.3 doc labeled this "Expected" and deferred it; v0.1.5 rewrote `self_destruct_unix()` to spawn a detached `setsid` helper that waits for the parent to exit, then overwrites and deletes.
- **Classification:** **MIXED.** The ETXTBSY behavior on WSL is genuinely execution-discovered (discovery-priced), but the project's own Windows path *already* used the detached-helper/batch-script pattern — so "a running binary can securely-overwrite-and-delete itself on Unix" was an unstated assumption that contradicted knowledge the team already held.
- **Most-helpful artifact element:** **Assumptions** (surface "the self-destruct must overwrite its *own running* executable — is that possible per-platform?"; the answer was already "no" on Windows). Runner-up: an Approaches-Considered / cross-platform-parity check.
- **Process gap a format can't fix:** The roadmap checkbox M0.1.2 was edited *in place* to read "fork-and-delete for WSL/Linux compatibility," erasing the record that the original design was broken. In-place checklist mutation hides churn from exactly this kind of retro; that needs an append-only decision log / ADR discipline, not a CONOP/OPORD template.

---

## EPISODE 2 — Local cross-compilation abandoned for CI

- **Session docs:** `20260117_v02_target_flag.md` (single session).
- **What happened:** Installed the `cross` tool for local cross-compilation; its Docker container hit GLIBC issues. Pivoted same-session to GitHub Actions CI for multi-platform builds. Roadmap M0.2.3 reflects the split outcome (`cross` for Linux checked; Windows mingw cross-compile still open).
- **Classification:** **DISCOVERY-PRICED-IN.** Whether `cross`'s containers hit GLIBC friction on a given host is toolchain-specific and self-corrected within one session at trivial cost. A faint preventable edge exists ("prefer CI runners over local Rust cross-compile" is semi-known lore), but the churn was near-zero.
- **Most-helpful artifact element:** **NONE** (defensibly Approaches-Considered, but the same-session self-correction makes it not worth the ceremony).
- **Process gap a format can't fix:** None material.

---

## Non-qualifying signals (checked, rejected to avoid hindsight inflation)

- **Import-path fix** (`magic_movies.cli.packager.embedder` → `…packager.embedder`, v0.1.4): typo-class, single-line, single-session. Not a planning failure.
- **Repurposing tactics-game scaffolding** (init): reuse, no observed rework.
- No `revert`/rewrite commits anywhere in history; two dev-branch merges are clean feature integrations, not thrash.

---

## SUMMARY

- **Episodes found:** 2 (only 1 truly multi-session).
- **Classification counts:** PREVENTABLE-BY-PLANNING 0 · MIXED 1 · DISCOVERY-PRICED-IN 1.
- **This is a near-clean record** — two days, six sessions, linear no-revert history. I am deliberately not manufacturing preventability that isn't there.
- **Single strongest lesson for CONOP/OPORD format design:** The one place this repo planned deeply — `adversarial/research-plan.md` — already contains exactly the elements the ladder should mandate: explicit hypotheses (Assumptions), per-question "**What if it fails?**" contingency branches (pre-decided Branches), Open Questions (risks/enemy-forces), and quantified success metrics (exit criteria). The team demonstrably *knows how* to write these. Yet it applied that rigor only to exciting future research, while the actual churn (Episode 1) happened in near-term engineering work that got a bare roadmap checkbox and no Assumptions section. So the format should (a) require **Assumptions + What-if-it-fails Branches** for *engineering* work, not just research — realistic here because the repo already proves it can produce them; and (b) pair them with an early **"run it on the real target"** execution checkpoint, since both failures (ETXTBSY on WSL, GLIBC in `cross`'s Docker) were only ever going to surface by running, not by more paper. A format can mandate that the checkpoint *exists*; it cannot supply the platform fact.
- **Does this repo plan at all?** Shallowly and forward-only: the roadmap carries per-milestone Goals and Success Criteria, but there is no `docs/plans/`, no CONOP/OPORD, and no ADRs — the sole deep plan is for not-yet-started research, so day-to-day it runs essentially session-to-session against a roadmap checklist.
