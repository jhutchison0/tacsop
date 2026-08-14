# Review: CONOP WHETSTONE — In Debate Adversarial Review

**Author**: code-reviewer
**Date**: 2026-08-14
**Type**: Plan review (CONOP debate; runs assumption A4's falsifier as assigned)

**Scope**: `docs/plans/conop_whetstone_recursive_doctrine_loop.md` (primary), `.claude/skills/traversing-the-knowledge-base/SKILL.md`, `/pcc` check 5 diff, the 2026-08-14 proposal amendment, the WHETSTONE tasks.md line. All uncommitted on `topic/kb-graph-traversal` at HEAD `01d3073`.

**Verdict up front**: ready-with-fixes. The architecture survives attack: approaches are honest about the panel verdict, validate-before-detail is genuinely honored (Waves 2-5 are one to two sentences each; only Wave 1 carries a TCS table), the NOT-build list is substantive, and most factual claims verify against primary sources. What does not survive: one load-bearing number inflated ~5x, an evidence base that is not in the repo, a "structural" safety claim that is actually policy, and two gating metrics that fail the CONOP's own A4 kill-criterion. All fixes are text-level; the must-fix set is listed at the end.

---

## Critical

### C1. The "15 months" unfireable-gate figure is wrong by roughly 5x

**Location**: CONOP Problem ("unfireable for 15 months"), Enemy Forces ("waited 15 months on audit-log data"), D7 ("The 15-month unfireable escalation is the type specimen"). Three occurrences.

**Issue**: The Layer-5/6 escalation task landed 2026-05-19 (`git log -S "audit-log data" -- docs/tasks.md` → commit `028ed67`, 2026-05-19, the enforcement-layer session). 2026-05-19 to 2026-08-14 is 87 days, about 3 months. Session-doc history starts 2026-03-12; nothing in this loop can be 15 months old.

**Why it matters**: This is the type specimen for D7 in a plan whose thesis is evidence integrity. The true figure (a gate blocked ~3 months because its evidence stream never existed) supports D7 fine; the inflated one, if approved, becomes doctrine and eventually a downstream citation. It is also the strongest single argument for C2: the number almost certainly came from an unverifiable digest.

**Fix**: Replace all three occurrences with "~3 months (since 2026-05-19)" and cite the generating command inline.

### C2. The evidence base is not in the repo

**Location**: CONOP References ("Commissioned digests (2026-08-14, this session)") and every §-citation: "archaeology digest §1, L1-L14", "§2, channel 11", "§3", "the systems digest", "the loop-design lane".

**Issue**: No digest files exist in the working tree or at HEAD; `git status` shows only the five review artifacts. The CONOP's per-claim citations resolve to documents a reader cannot open. Because "archaeology digest §1" is not path-shaped, these dangling references are invisible to the very `/pcc` check 5 this branch ships.

**Why it matters**: In Debate exists to test the evidence. I could re-verify most claims only by going around the digests to primary sources (ledger below), and the one claim I could not ground (C1) turned out wrong. Approving a plan whose evidence base is a vanished conversation repeats the exact cross-session rot the plan diagnoses.

**Fix**: Persist the four digests under `docs/reviews/` or `docs/research/` and cite paths, or re-cite each load-bearing claim directly to primary sources (session docs, script lines, protocol sections). Either is acceptable; unciteable is not.

### C3. "Structurally unable to edit its own evaluators" is an overclaim; D4 is policy, not structure

**Location**: CONOP Problem ¶2 ("the loop is structurally unable to edit its own evaluators"); D4.

**Issue**: D4's mechanism is a commit-message tag (`[gate]`) plus a review convention. Nothing detects an untagged commit that bundles a gate edit with the work the gate judges. This is the same gap the panel's own adoption review named W4 on graphify's Option A mitigations: "review-enforced policy, not controls."

**Why it matters**: Bounded recursion is the plan's headline safety property. Wave 5 explicitly feeds WHETSTONE's own gates back into the loop; if the only boundary is a tag nobody checks, the DGM incident the CONOP cites is mitigated by vocabulary. Note also two gate-adjacent channels outside D4's list entirely: CONTEXT.md (refreshed each D6 consolidation, loaded by every future session) and `.claude/agent-memory/` (gitignored, agent-written, review-invisible; O1 covers the second).

**Fix**: Two parts, both cheap. (1) Reword the Problem sentence to "policy-bounded and human-gated." (2) Add the deterministic backstop as a `/pcc` check: if `git diff --cached --name-only` intersects a pinned gate-file list (`.claude/commands/pcc.md`, `.claude/hooks/`, skill success-criterion files, this CONOP) AND non-gate files, WARN "gate files bundled with gated work; split into a [gate] commit." About four lines, same shape as check 5. Schedule it Wave 2 at latest; add CONTEXT.md to the D4 list or state why it is exempt.

---

## A4's falsifier, executed (assigned to this review)

Question per A4: can each gating metric be satisfied without the behavior it measures, and does the gaming leave a detectable trace? A4's kill-criterion: a metric trivially satisfiable with no detectable trace gets replaced with reviewed-diff evidence before it gates anything.

| Metric | Gaming move | Trace left? | Cheapest hardening |
|---|---|---|---|
| M1 uptake (3/5 docs carry `KB-graph:` line) | Cosmetic line, no traversal run | Partial: the line format demands command + concrete result, so a fabricated line is checkable, but nothing requires checking. Denominator is also gameable: "any cross-doc question" is judgment, so weak sessions can be ruled non-qualifying | Define qualifying deterministically (session's commits touch `docs/` or `.claude/`); D6 consolidation re-runs one sampled line per window |
| M2 integrity (no new MISSING beyond baseline 3) | (a) Never run `/pcc`; (b) net-masking: one new path goes missing while one baseline path is fixed, count stays 3 | **None for (a)**: check output is console-only, a skipped check is indistinguishable from a clean one. **None for (b)**: baseline is a count, not a path set | (a) Session doc records the check-5 MISSING count whenever `/pcc` runs, one line. (b) Move the three dispositioned March paths into the check's allowlist (labeled with the P3 task), making the baseline 0: any MISSING line = WARN |
| M3 routing value (≥1 line names an artifact the session edited) | Reverse causality: make the planned edit, then write a KB-graph line naming it | **None**: co-occurrence cannot distinguish informed-by from decorated-with | At Wave 1 exit, a non-author reviewer re-runs each claimed traversal and confirms the finding was not already in the session's opening task list; only verified lines count |
| E1 latency | Status inflation (flip LEARNED at artifact-change time; "verified in use" is judgment) and survivorship (see W2) | Partial: LESSON evidence field is checkable at D6 | LEARNED requires evidence dated after the artifact change and not self-confirmed by the authoring session (D5's own independence rule, currently absent from D1) |
| E2 unpropagated count | Declare entries covered by folding or write-off | Yes: the fold/write-off is a visible dated artifact | Make cycle logs greppable one-liners so E2 is computed, not asserted (Wave 4's ledger can carry this) |
| E3 staleness | Date-bump CONTEXT.md without real refresh | Yes, in the diff, if anyone looks | Define staleness by content, not mtime: newest session/plan doc referenced by CONTEXT.md vs newest existing; greppable |
| E4 ack rate | Hub-side self-ack; in a single-operator fleet this is the default, not an attack | Weak: authorship is identical on both ends by construction | See W8; require repo-specific disposition content so rubber-stamps are visible |
| E5 | = M1/M2/M3 | as above | as above |

**A4 verdict**: fires for M2 (both moves traceless) and M3 (traceless). Per the CONOP's own kill-criterion these two must be hardened before E5 gates Wave 2. The hardenings above are one-line to one-paragraph changes. A4's underlying claim (grep-countable beats judged) survives: every hardening above is itself grep-or-diff-based.

---

## Warnings

### W1. M2/M3 hardening is mandatory by the CONOP's own rule

Covered by the table above; listed here because it belongs in the must-fix set. The CONOP wrote the kill-criterion; this review triggered it; the fix must land in the skill and check text before the Wave 2 gate can consume E5.

### W2. E1's median cannot see the failure class the plan exists to fix

**Location**: E1 definition vs target.

**Issue**: E1 is "median sessions from OBSERVED to LEARNED", a statistic over completed transitions. The dominant documented failure is never-completed (the four dropped entries; the still-open playbook). Those lessons never enter the median; worse, the PARKED-expiry escape lets a hard lesson exit the metric with a clean disposition. The target sentence ("no lesson older than 2 consolidation reviews...") is also in different units than the measure (max-age bound vs median).

**Fix**: E1 reports three numbers: median of completed, age distribution of open lessons, count of expired-unresolved parks. The third is a loss counter, not throughput, so it is D8-clean.

### W3. The calibration-compliance paragraph overclaims for E5

**Location**: Measures of Success, closing paragraph.

**Issue**: "Every gating metric above is anchored to named known-bad references from the archaeology" is false for E5, the only metric that actually gates the next wave. M1/M3 are novel adoption metrics with no archaeology anchor and no demonstrated rank-ordering.

**Fix**: Scope the claim to E1-E3. For E5, either name the available known-bad reference (`maintaining-project-context`: a shipped skill with zero uptake evidence while CONTEXT.md went three cycles stale; its M1-analog scores 0) or state plainly that E5 gates on an uncalibrated novel metric compensated by W1's reviewer verification.

### W4. Skill and CONOP gate rules disagree at the edges

**Location**: skill Success Criterion vs CONOP A1 kill-criterion vs Wave 2 gate.

**Issue**: Skill pass = M1 AND M3; skill fail = M1 alone. CONOP kill = M1 < 3/5 AND M3 = 0. Wave 2 gate = "A1 pass AND A2 pass." Undefined zones: M1=2, M3=1 (blocked but not killed) and M1=3, M3=0 (skill-failed but not killed). M2 appears in gating E5 but is informational in the skill's outcome rule.

**Fix**: One sentence in both docs: Wave 2 gate = the skill's pass rule; halt = the skill's fail rule; anything between = one recorded escalation rung plus one re-run window; M2 is informational.

### W5. Wave 0 is marked COMPLETE while uncommitted, and it widens the drift it cites

**Location**: Wave 0; Enemy Forces (session-end/pcc drift).

**Issue**: The skill is untracked and pcc.md unstaged; branch HEAD `01d3073` predates all Wave 0 artifacts, so "Evidence: branch `topic/kb-graph-traversal`" names a branch whose committed state lacks the evidence. Separately, check 5 was added to pcc.md without touching `session-end.md` Step 2, whose enumeration already disagreed with pcc.md (it lists large-files and config-validation, which pcc.md lacks; it lacks git-state and now reference-integrity). The CONOP cites this drift as an enemy force, then defers the one-line fix to Wave 2, five-plus sessions out.

**Fix**: Commit Wave 0 at the gate; a wave is complete when its evidence is durable. Sync session-end.md now, ideally by replacing the enumerated list with a pointer to pcc.md so this drift class dies rather than resets.

### W6. Wave 4 collides with the propagation protocol in three places

**Location**: O2; Wave 4; D5.

**Issue**: (a) O2's fold-into-one-entry option violates Batching Rule 2 ("never let a doctrine entry mix unrelated changes"); the four orphans are mutually unrelated (git-sync, Windows patch, .gitattributes, branching). The cited `d996d10` precedent (verified: 2026-07-17, "Merge Cycle 8 into the unpropagated Cycle 7 entry") also cuts against Rule 2's spirit. (b) D5's tiers amend the protocol, and "changes to the protocol go through the protocol"; Wave 4's sketch names no protocol-amendment step. (c) "Cycle 8" is probably the wrong label: by ship events (04-21 = 5, 05-19 = 6, 07-20 = 7, 08-03 = 8) the uv cycle occupies 8, unnumbered in its own session doc (a protocol step-5 miss worth logging), and a different "Cycle 8" was already merged away at `d996d10`. One nuance for the fix design: `entries[0]` is documented protocol ("hard constraint of the current implementation", protocol line 44, with Rule 1 as the compensating process). The four losses are Rule 1 process violations, not an unknown bug; the D6 integrity check is the real fix, the script change a hardening.

**Fix**: Prefer the catch-up-cycle option for O2, or amend Rule 2 through the protocol first. Add "amend `docs/propagation-protocol.md` through its own process" to Wave 4's sketch. Write "the next cycle" and settle numbering at the first D6 consolidation.

### W7. The genuinely challenging alternative is missing: fix the two bugs and stop

**Location**: Approaches Considered.

**Issue**: A is rejected by the standing panel verdict and C was pre-adjudicated by the MAUT (verified: "A (adopt graphify) cannot win at any egress weight, including zero"), so B wins by default; the "bold" label sits on the recommended-safe option. The unrepresented challenger: fix `entries[0]` shipping and audit-log liveness (A5), adopt nothing else. That closes E2's loss class and D7's type specimen at roughly 1% of the plan's surface, zero new conventions, and is the natural Simplicity First reading.

**Fix**: Add it as an approach and argue it down on the page. The argument exists (bugfix-only fixes the two named instances, not the class: no routing, no aging, no verification) but the debate record needs it stated, not implied.

### W8. Single-operator independence is thinner than D5/E4 admit

**Location**: D5 ("never self-confirmed by the author"); E4.

**Issue**: One human operates the hub and all 19 downstream repos. "Independently confirmed from a second repo, session, or agent" and MUST-ACK dispositions are the same person in a different working directory. E4 therefore measures whether the reading ritual ran, not independent judgment; hub-side self-ack is the default state, not an attack someone must mount.

**Fix**: State it honestly in D5: independence here means a different context window, repo, and time, which guards against context-carryover, not operator bias. Require MUST-ACK dispositions to carry repo-specific content (what was applied, what skipped, why) so a rubber-stamp is visible in review.

### W9. The corpus snapshot numbers do not reproduce and carry no commands

**Location**: skill table ("157" links, "816" path mentions, "5:1"); CONOP Friendly Forces repeats both.

**Issue**: At this HEAD I count 168 links (`git ls-files '*.md' | xargs grep -oE '\[[^]]*\]\([^)]+\.md[^)]*\)' | wc -l`) and 1,321 raw path-shaped mentions (check-5 regex over `git ls-files '*.md'`). 816 is the same figure the 2026-08-13 review could not reconcile; this is now the third document carrying it. The direction (mentions outnumber links) holds; the stated precision does not.

**Fix**: Put the generating command in each table row and refresh the numbers, or round ("~160 links; path mentions outnumber links several-fold"). This is the recurring counts-without-commands pattern; a skill teaching corpus traversal should model the standard.

### W10. Mission has no "by when"

**Location**: Mission.

**Issue**: The template mandates who, what, by when, in order to. Who, what, and purpose are present; no time element. For a plan whose MOE is latency, the omission is conspicuous.

**Fix**: Anchor to the plan's own clock, e.g. "...within two propagation cycles of approval..."

---

## Suggestions

- **S1. Dual supersession mechanisms.** D3's `Superseded-by:` header will coexist with CONOP-FORMAT's "Superseded by OPORD" status value. Define precedence in Wave 2's format change (headers for artifacts, status vocabulary for plans).
- **S2. Run the ADR triple filter on D5.** A downstream-facing contract change, hard to reverse once fleet-wide, surprising without context. The CONOP runs the filter on none of D1-D9; D5 is the live candidate.
- **S3. Checklist budget.** The plan adds a session-end routing step (D2), a session-start kata check (Wave 5), and a session-start stream-silence WARN (D7) while Terrain cites over-cap context reducing adherence. Adopt a net-zero rule: each added standing step names what it consolidates or removes.
- **S4. Anchor the check-5 extractor.** A prefixed path like `veil-engine/docs/foo.md` would extract `docs/foo.md` and false-MISSING. No false positives today (verified: exactly the 3 baseline lines), so fix when convenient: prepend `(^|[^A-Za-z0-9_/-])`.
- **S5. MUST-ACK rides the dead letterbox.** The ack request is delivered by append onto the unread pile whose unreadness motivated the tier. A3's canary tests exactly this; the tier spec should still require delivery-with-read-receipt semantics (canary = the next session inside that repo), not another append.
- **S6. Fold `.claude/audits/` into O1.** It is gitignored (`.gitignore:58`), so even after A5 passes, D7's audit stream is machine-local and review-invisible; the same track-or-amend decision applies.

---

## Checks that came back clean

- **Format compliance**: everything else present and conforming. Assumptions table carries all three mandatory fields for A1-A5 with real falsifiers; three approaches with recommendation and named trade-offs; open decisions flagged (O1-O3) and correctly blocking OPORD, not Wave 1; MOP/MOE split with when-measurable per MOE; Waves 2-5 genuinely sketch-level per validate-before-detail; NOT-build substantive; agent design present ("none new" is correct, the roster covers it).
- **D8 self-check**: no throughput metric gates or measures success anywhere in the CONOP. E2 counts losses, not output; MOP's "artifacts shipped" is wave tracking, not doctrine volume.
- **Prose**: clean in both new artifacts. Em dashes only in headings (exempt per RULES.md 8); "in order to" only in the Mission (the stated exception); zero LANGUAGE.md cruft words; Problem and skill both open point-first.
- **O1's factual basis**: verified. `.claude/agent-memory/` gitignored at line 56; agent instructions do call it version-controlled shared memory; it does hold live corrections (the fleet-count and evidence-layer findings this review relies on).

## Verification ledger

| Claim | Source checked | Result |
|---|---|---|
| entries[0]-only extraction, lines 47-66 | `scripts/propagate_doctrine.py` | Verified; `return entries[0].strip()` at line 66. Documented as a known constraint at `propagation-protocol.md:44` |
| 4 never-propagated entries (03-31, 05-29, both 06-28) | doctrine-updates.md headings; run records in session docs (04-21: 11 repos; 05-19: 12; 07-20: 14; 08-03: 15) | Verified on this box's records: none was newest at any recorded run. Caveat: other machines' runs are invisible, as the CONOP's Terrain admits |
| 37 days, tzdata; the upstreaming quote | `docs/sessions/20260529_windows_portability_fixes.md:307-312` | Verified: 2026-04-22 → 2026-05-29; quote verbatim |
| ~3 months, .gitattributes | 20260325 session → 2026-06-28 entry | Verified: 95 days |
| 14 days, 5 weeks | Session-doc dates (03-17 → 03-31; 05-23 → 06-28) | Plausible; formal check is Wave 1 task 4 |
| CONTEXT.md 3 cycles stale | `CONTEXT.md:112` (Last Updated 2026-05-19; snapshot cites cycle 5, 2026-04-21) | Verified: cycles 6, 7, 8 have run since |
| 15 months unfireable gate | `git log -S "audit-log data"` → `028ed67` 2026-05-19 | **Wrong**: 87 days (C1) |
| `/pcc` check 5, baseline 3, allowlist | Ran the command as written | Verified: exactly 3 MISSING, all March decision-science paths, dispositioned at `docs/tasks.md:9`; allowlist suppresses the two runtime artifacts |
| 17 of 18 session docs typed-headered | grep over `docs/sessions/` | Verified: 18 docs, 17 match |
| 19-repo roster | `docs/propagation-protocol.md:171` | Verified |
| Graphify "cannot win at any egress weight" | `docs/reviews/20260813_kb_graph_adopt_vs_build_maut.md` headline | Verified |
| W4 "policy, not controls" parallel for D4 | `docs/reviews/20260813_kb_graph_adoption_review.md` W4 | Verified |
| `d996d10` fold precedent | `git show d996d10` | Verified: 2026-07-17 merge of Cycle 8 into Cycle 7 |
| 157 links / 816 path mentions | Recounted at HEAD | **Not reproducible**: 168 / 1,321 by the natural commands; no generating commands given (W9) |
| Five March docs, `.gitignore:56` | `docs/tasks.md:9`; `.gitignore` | Verified |

---

## Verdict

**Ready-with-fixes.** The plan's spine (staged conventions behind evidence, human gates, deterministic streams) survives adversarial reading and is consistent with the panel verdict and the repo's enforcement doctrine. The must-fix set before the user's Approve gate, all text-level, roughly one afternoon:

1. **C1**: correct the 15-month figure (three occurrences) to ~3 months with the command.
2. **C2**: persist the four digests or re-cite every §-claim to primary sources.
3. **C3**: reword "structurally unable" to "policy-bounded and human-gated"; schedule the gate-file `/pcc` check (Wave 2 at latest).
4. **W1**: harden M2 (zero-based allowlist baseline; check-5 count recorded in the session doc) and M3 (non-author verification at Wave 1 exit); mandated by A4's own kill-criterion, which this review fired.
5. **W4**: align the skill's pass/fail rule with A1's kill-criterion and the Wave 2 gate; classify M2 as informational.
6. **W5**: commit Wave 0; sync `session-end.md` Step 2 now (pointer, not enumeration).
7. **W7**: add the bugfix-only approach and argue it down on the page.
8. **W10**: give the Mission a "by when."

W2, W3, W6, W8, W9 should be dispositioned in the debate but need not block approval if explicitly deferred with rationale; S1-S6 are at the lead's discretion.
