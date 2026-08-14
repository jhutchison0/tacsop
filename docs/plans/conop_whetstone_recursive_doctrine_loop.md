# CONOP WHETSTONE — Recursive Doctrine Self-Improvement via the Knowledge Graph

**Status**: In Debate (adversarial review complete 2026-08-14, `docs/reviews/20260814_conop_whetstone_debate.md`, verdict ready-with-fixes; fixes applied same day; awaiting the user's Approve gate)
**Date**: 2026-08-14
**Lead**: jhutchison (session lead: Claude)
**Parent task**: `docs/tasks.md`, WHETSTONE line (added 2026-08-14)
**Evidence base**: four commissioned research digests, persisted verbatim at `docs/reviews/20260814_whetstone_research_archaeology.md`, `_systems.md`, `_loops.md`, `_institutions.md`. Corpus baseline measured at branch `topic/kb-graph-traversal`, HEAD `01d3073`.

---

## Problem

This repo already runs a doctrine self-improvement loop, and the archaeology proves both halves of its character. When a lesson and its doctrine artifact meet inside one session, latency is same-day: the append-mode fix, the enforcement layer, the uv field exercise all closed the loop before the session ended. When a lesson must survive a session boundary, it rots: 14 days (clone-cleanup gaps), 5 weeks (branch doctrine), 3 months (.gitattributes entry), 37 days for a Windows fix whose session doc states the diagnosis plainly: "the act of writing a fix and the act of upstreaming a fix are different tasks." Four doctrine entries were never propagated at all because the script ships only the newest entry (a documented process rule, violated four times, not an unknown bug). One escalation gate has been unfireable for its entire 87-day life (since 2026-05-19) because its evidence stream (the audit log) never existed. CONTEXT.md is stale by three cycles despite a dedicated skill for maintaining it.

The user's intent: doctrine that supports recursive self-improvement through the knowledge-graph traversal layer. Recursive here means the loop's own artifacts (this CONOP, the traversal skill, the gates) are subject to the same loop. Bounded means every canonical write passes a human gate, and the loop is structurally unable to edit its own evaluators. The knowledge graph's role, per the institutional evidence, is not to make lessons findable but to route each lesson to the doctrine artifact it should update: a switchboard lessons pass through, not an archive they rest in.

---

## Situation

### Friendly Forces (what we have)

- **A working in-session loop** with 14 documented instances of field experience changing doctrine (archaeology digest §1, L1-L14).
- **Typed edges already in the corpus**: seven relation headers pinned by `docs/session-doc-format.md`, roughly 160 markdown links and 800-1,300 path mentions (method-dependent counts; discrepancy documented in the debate review), a hand-maintained Reading Order in `CONTEXT.md`.
- **Wave 0, shipped this session**: `.claude/skills/traversing-the-knowledge-base/SKILL.md` v1.0.0 with a falsifiable five-session criterion (M1 uptake, M2 integrity, M3 routing value), and `/pcc` check 5 (living-docs reference integrity, baseline 3 known-missing).
- **Culture that already implements two literature-mandated guards**: append-only amendments (the ACE delta-only rule against context collapse: ADR-0001/0002 Amendments, CONOP append-only-after-approval) and author-never-approves (proposer vs code-reviewer vs human gate, the self-preference-bias guard).
- **Propagation machinery**: `scripts/propagate_doctrine.py` (push, append mode), `scripts/adopt_doctrine.py` (downstream pull), `docs/propagation-protocol.md`, a 19-repo roster.
- **Versioned doctrine layers**: skills carry semver (3 of 8 revised at least once); doctrine entries are dated and append-only; ADRs govern hard-to-reverse decisions. This maps cleanly onto the Army's layered change velocity (principles slow, techniques fast, local practice provisional).

### Enemy Forces (what works against us)

- **Cross-session lesson rot**, the dominant failure: `docs/tasks.md` is the only parking mechanism and has no aging, no owner field, no closure check (archaeology §2, channel 11).
- **Silent doctrine loss**: the `entries[0]`-only extraction dropped the 2026-03-31, 05-29, and both 06-28 entries from propagation without any signal (archaeology §3).
- **Gates without evidence streams**: the Layer-5/6 escalation decision has waited its whole 87-day life (since 2026-05-19) on audit-log data; `.claude/audits/` does not exist in this working tree, so the trigger has never had data to fire on.
- **Recurring living-doc staleness**: the Day-1 playbook was rewritten 2026-05-19 after 11 FAILs and had drifted again by 2026-07-26; "the drift recurs because nothing gates it." `session-end.md` Step 2 enumerates a PCC checklist that has already drifted from `pcc.md` (found while authoring this CONOP).
- **Append debt**: roughly half of each recent propagation cycle lands as appends onto unread downstream notifications; nothing verifies integration (archaeology §2: all 14 channels are pull or unverified push).
- **The literature's failure modes** now quantified: whole-artifact rewrites collapse context (ACE); loops iterating on self-opinion rather than external evidence diverge (Huang et al., Kamoi et al.); a self-improving system sabotaged its own evaluator when allowed to touch it (Darwin Gödel Machine incident); memory-driven drift is large and self-generated (Misevolution: refusal 99.4% to 54.4%); tiny poison fractions dominate shared stores (AgentPoison: under 0.1% contamination, over 80% attack success).

### Terrain

- 19 known downstream repos (`docs/propagation-protocol.md` roster); discovery is filesystem-based per machine; three machines (work, home, laptop) hold clones this box cannot see, and the five March docs proved lessons can live and die on one machine.
- The corpus is markdown; every proposed metric is grep-countable, which keeps evaluation deterministic and out of model-judgment territory (the memory-benchmark collapse in the systems digest is the cautionary tale for judged metrics).
- No CI on this repo yet (open P3 task); deterministic checks currently run only inside sessions via `/pcc`.
- Claude Code loads `CLAUDE.md` and skills as context, not enforcement; anything that must always happen needs a hook (its own documentation states over-cap context measurably reduces adherence).

### Assumptions

| Assumption | Cheapest falsifier | Blast radius if wrong | Kill-criterion |
|------------|--------------------|-----------------------|----------------|
| A1: Agents apply the traversal skill without enforcement | The skill's own M1/M3 over the five-session window (Wave 1) | Waves 2-5 all presume routing happens at session-end | The skill's full M1 x M3 outcome matrix is authoritative (no undefined cells); the kill cell is M1 < 3/5 AND M3 = 0: halt Waves 2+, retire-or-escalate decision recorded in tasks |
| A2: The link graph is dense enough to route lessons to owner artifacts | Retroactive routing test on the last 3 substantive session docs: for each recorded lesson, does a blast-radius traversal reach the artifact that was (or should have been) updated? One afternoon, Wave 1 | The switchboard concept; D2 collapses into hand-filing | Routing returns empty or wrong artifact sets for more than half the lessons tested |
| A3: Downstream repos respond to a must-acknowledge tier | One canary cycle to 2-3 active repos with an ack request (Wave 4 entry) | Wave 4's verification half; E4 | Zero acknowledgments after 2 canary cycles: verification stays hub-side pull, drop the tier |
| A4: Grep-countable metrics resist gaming better than judged metrics | Red-team each metric definition in the In Debate pass: can it be satisfied without the behavior it measures? | The gate system's integrity (D7, D8) | A metric found trivially satisfiable without its behavior, with no detectable trace: replace it with reviewed-diff evidence before it gates anything |
| A5: The audit hook actually fires on this machine | Touch a `src/myproject/` file under the hook's matcher and check for the log line. Minutes, Wave 1 | D7's claim that dead evidence streams are detectable; the 87-day-blocked escalation task | Hook provably broken and unfixable in a session: remove the escalation task's gate condition and re-decide it on direct evidence |
| A6: Downstream sessions will flag fleet-scope lessons at the source | Seed the D10 convention in 1-2 active downstream repos (tactics-game is a natural canary) during the next machine visits; check whether their next cross-repo-relevant lessons land in `.claude/upstream-lesson.md` | D10 and the upward half of Wave 4; without capture at the source, upward flow stays operator memory | Two consecutive downstream sessions produce fleet-relevant lessons (visible in their session docs) that the convention fails to capture: redesign the capture point before fleet rollout |

---

## Mission

Tacsop formalizes its doctrine loop as collect → route → gate → propagate → verify, instrumented by the knowledge-graph traversal layer and gated by humans at every canonical write, closing the loop's first full pass (Waves 1-5) by the second consolidation session, approximately two propagation cycles out, **in order to** cut cross-session lesson-to-doctrine latency from weeks-or-never to bounded-and-tracked, and to make silent doctrine loss (unpropagated entries, dead gates, stale living docs) structurally detectable.

---

## Approaches Considered

### Approach A: Full instrumentation now

Build everything in one push: the utility slices, the session-end routing step, the state machine, propagation tiers, the consolidation cadence.

- **Pros**: one coherent rollout; no waiting.
- **Cons**: violates validate-before-detail; A1 and A2 are unfalsified and the skill's five-session bet is three days old; builds enforcement for a behavior gap not yet demonstrated (the exact anti-pattern the kb-graph panel rejected 2026-08-13).
- **Risk**: Medium-high. The waste mode is building a switchboard nobody calls.

### Approach B: Convention-first switchboard, mechanisms staged behind evidence (bold alternative)

Ship conventions and evidence streams first; every mechanism is a convention plus a grep-countable stream; code builds only on demonstrated triggers. The bold part is the claim that a recursive self-improvement loop needs almost no new software: the corpus, the headers, semver, the propagation script, and five conventions borrowed from institutions that run this loop at national scale.

- **Pros**: each wave's gate consumes the previous wave's evidence, so the plan cannot outrun its own validation; zero egress by construction; reversible at every stage; matches Simplicity First and the panel's standing verdict.
- **Cons**: slower to full capability; depends on session discipline holding through the observation window; some mechanisms (acknowledgment ledger) are genuinely worse without small tooling and will feel manual.
- **Risk**: Low. The waste mode is a few unused conventions, deleted cheaply.

### Approach C: Tool-first (revisit graphify, or adopt a Cognee/Graphiti-class memory engine)

- **Pros**: mature capability immediately.
- **Cons**: re-litigates the 2026-08-13 MAUT (adopt-graphify could not win at any egress weight); the systems digest's do-not-do list is explicit: precomputed corpus graphs lost to read-time traversal on Microsoft's own evidence, and LLM-extracted entity graphs rot non-deterministically.
- **Risk**: High, and already adjudicated.

### Approach D: Minimal repairs, no loop doctrine (the null challenger)

Fix the specific defects the archaeology found (the entries[0] process violations, the playbook-drift task, the missing audit directory) and write no loop doctrine at all.

- **Pros**: smallest possible change; repairs are needed under every approach.
- **Cons**: repairs instances, not the class. The class demonstrably recurs: the Day-1 playbook was fully rewritten 2026-05-19 and had drifted again by 2026-07-26 "because nothing gates it"; the un-upstreamed-fix pattern (L8) repeated in this very corpus with the three unpushed sibling commits. Instance repair without a detection loop re-arms the same failures.
- **Risk**: Low cost, high recurrence. Rejected as the whole answer, absorbed as parts: its repairs land inside Waves 1, 2, and 4.

**Recommendation**: Approach B, with D's repairs absorbed into its waves. B is the only approach whose failure mode is cheap, and the only one consistent with both the panel verdict and the loop-design literature's convergence condition (iterate on external evidence, in small validated steps).

---

## Design Decisions

Resolved by this CONOP (each cites its evidence):

- **D1. Lesson state machine.** Every lesson gets a status: `OBSERVED` (recorded in a session doc) → `IDENTIFIED` (routed to an owner artifact, human-endorsed at session-end) → `LEARNED` (the artifact changed AND the change verified in use). Only a human flips status. A lesson is not learned because it was written down; it is learned when behavior changed (NATO JALLC lifecycle; AR 11-33's definition). Carried as a greppable line, schema in D9.
- **D2. Routing step at session-end (the AAR Chapter 5 analog).** Session-end gains a step: for each lesson, run the blast-radius traversal, name the owner artifact, and record a verdict: `ADD` (new doctrine), `UPDATE` (refines existing), `SUPERSEDE` (replaces, with D3 header), or `NOOP` (already covered), the Mem0 write-time arbitration protocol. A lesson with no reachable owner artifact gets an explicit parked disposition with an expiry session count, killing the no-aging parking lot. Ships in Wave 2, gated on A1/A2.
- **D3. Supersession headers with temporal validity.** `**Supersedes**:` / `**Superseded-by**: <path> (YYYY-MM-DD)` join the typed-edge set. Doctrine claims are never deleted, only marked invalid with date and pointer (Graphiti's invalidate-not-delete). One grep yields the complete stale set; lineage plus validity reconstructs what was doctrine on any date, which is exactly the dispute a downstream repo brings.
- **D4. Evaluator independence (the DGM rule).** Changes to gate criteria, metrics, hooks, `/pcc` checks, or this CONOP's kill-criteria ride in dedicated commits tagged `[gate]`, are never bundled with work those gates judge, and always carry a reviewer other than the author. The Darwin Gödel Machine removed its own hallucination markers when allowed to touch its evaluator; the traceable lineage caught it, and this decision is that lineage, made structural. Structure, not just policy: the gate surfaces are a deterministic path list (`.claude/hooks/`, `.claude/settings.json`, `.claude/commands/pcc.md`, `.claude/commands/pci.md`), and `/pcc` check 6 WARNs whenever they are staged together with other files. Two gate-adjacent channels sit outside the list and are covered separately: CONTEXT.md's Reading Order steers orientation (watched by E3), and `.claude/agent-memory/` is O1's decision. This is the boundary that makes "recursive" safe: the loop improves its own gates only through the narrowest, most-reviewed channel.
- **D5. Provisional status and canary propagation.** New doctrine entries carry `PROVISIONAL` until independently confirmed from a second repo, session, or agent (never self-confirmed by the author: the Misevolution mitigation; independence is limited by the fleet's single operator, so the floor is a different repo and a different session). Propagation gains two tiers borrowed from the NRC: `MUST-ACK` (downstream repo records a one-line acknowledgment and disposition) and `FYI` (review for applicability). Fleet-wide MUST-ACK rollout goes through a 2-3 repo canary first (A3). Provisional entries never propagate MUST-ACK.
- **D6. Standing consolidation session (the CALL function; Letta's sleep-time compute; two lanes converged on this independently).** A recurring session type whose only deliverables are hygiene: cross-session trend rollup, the stale-set grep (D3), CONTEXT.md and Reading Order refresh, entry-shipping integrity check (closes the `entries[0]` drop class), append-debt and parked-lesson expiry review. Cadence: every propagation cycle or 5 sessions, whichever first; first instance is Wave 5's entry task.
- **D7. No gate without a live evidence stream.** Every gate names its stream, and a stream silent for a full cycle is itself a WARN surfaced at session-start. The 15-month unfireable escalation is the type specimen; A5 tests the hook now. Streams as of Wave 0: `KB-graph:` lines, `/pcc` check 5 output, the shift-left audit log (existence pending A5), the propagation ledger (Wave 4).
- **D8. Forbidden metric.** Doctrine throughput (entries shipped, lines of doctrine, cycle count) never gates anything and never appears as a success measure. Value is measured downstream only: adoption dispositions, drift catches, latency reduction (CAST's monitor-effectiveness step; the Goodhart guard). MOEs below comply.
- **D9. Fixed lesson schema.** One line, greppable, in session docs: `LESSON (<status>): <claim> | evidence: <path or command> | scope: <repo|fleet> | owner: <artifact path or PARKED(n)> | verdict: <ADD|UPDATE|SUPERSEDE|NOOP>`. Failures and no-lesson dispositions are first-class (ReasoningBank: failure entries carried the same weight as successes; success-only accretion loses the tail).
- **D10. Upward lesson channel (added at the user's gate feedback, 2026-08-14, after the debate review).** The loop's collection step extends below the hub: a downstream session whose lesson carries `scope: fleet` also appends it to `.claude/upstream-lesson.md` in that repo, the exact mirror of `.claude/upstream-update.md` (append mode, same never-gitignore rule, opposite direction). The hub harvests these files with the same filesystem discovery propagation already uses, at consolidation sessions (D6) or on any machine visit; a harvested lesson enters the hub loop at `OBSERVED` with provenance naming the origin repo and session doc. If it becomes doctrine, the entry credits the origin repo by name: visible credit is the incentive half (the ASRS/SRE finding: collection quality is bought with blamelessness and recognition, never punishment). Evidence this channel is real: five of the archaeology's fourteen loop instances originated downstream (L2 magic-movies, L4 velocity-scoring, L7 MEGAN, L8 heimdall-darkroom, L13b siblings), all carried by operator memory, with 37-day and ~3-month rots and one never-carried lesson that a sibling repo re-learned at full cost a week later. D10 absorbs the parked "cross-component lessons-learned register" finding (`docs/tasks.md`, parked since 2026-07-17), implementing it as a flow through the hub rather than a static register.

Open decisions, flagged per format (block OPORD promotion but not Wave 1):

- **O1. Agent memory tracking.** `.claude/agent-memory/` is gitignored while agent instructions call it version-controlled shared memory; it currently holds live corrections nobody can see (fleet count, evidence-layer finding). Options: track it in git (making agent-authored memory reviewable, the natural AgentPoison defense, and Anthropic's own stance that agent memory is untrusted input needing host-side gates) or amend the agent instructions to match the gitignore. Leaning track-it; decide at the In Debate gate.
- **O2. Backlog disposition for the four never-propagated entries.** Fold into the next cycle's entry (the `d996d10` merge precedent), ship as a catch-up cycle, or write them off with a dated note. The fold option must respect Batching Rule 2 in `docs/propagation-protocol.md` (independently adoptable Parts, the 2026-07-20 three-part precedent). Decide at Wave 4 entry.
- **O3. Consolidation cadence tuning** (every cycle vs every 5 sessions) after the first instance runs.

---

## Measures of Success

**MOP (performance)**: Wave artifacts shipped and reviewed; any code test-first with suite green; `/pcc` clean at each commit gate; review findings dispositioned.

**MOE (effectiveness)**, each with when-measurable and its calibration reference:

- **E1. Cross-session lesson latency**: median sessions from `OBSERVED` to `LEARNED`, reported alongside the full open inventory. Baseline known-bad references: 37 days (tzdata), ~3 months (.gitattributes), still-open at 19+ days (playbook). Known-good: same-day in-session instances. Measurable from Wave 2 onward at each consolidation session. Target: no lesson older than 2 consolidation reviews without a status change or explicit parked expiry. Survivorship guard: the consolidation report lists every `OBSERVED` and expired-`PARKED` lesson by name, so never-learned lessons cannot vanish into a median.
- **E2. Silent doctrine loss**: unpropagated-entry count at each cycle. Baseline known-bad: 4. Target: 0, checked by the D6 integrity step. Measurable at Wave 4's first cycle.
- **E3. Living-doc staleness**: cycles-behind for CONTEXT.md and the Day-1 playbook. Baseline known-bad: 3 cycles / twice-drifted. Target: ≤ 1 cycle. Measurable each consolidation session.
- **E4. Downstream integration**: MUST-ACK disposition rate on canary repos. Baseline: 0 (nothing verifies today; the only stated watch was never recorded as performed). Measurable 1-2 cycles after Wave 4. This is the CAST two-step: track implementation, then monitor effect.
- **E5. The traversal skill's own M1/M2/M3** (five-session window, defined in the skill). Measurable at Wave 1 exit. E5 gates Wave 2.
- **E6. Upward lesson flow**: fleet-scope lessons harvested per cycle, and latency from downstream observation to hub doctrine change. Baseline known-bad references: 37 days (L8 tzdata), ~3 months (L2 .gitattributes), never (the master-clock re-learn). Known-good: same-day (L4 velocity-scoring convention, adopted and propagated the day the hub saw it). Measurable 1-2 cycles after the D10 canary seeds (A6).

Metric hardening from the In Debate red-team (A4's falsifier, run 2026-08-14): M2's baseline was zeroed via the check-5 allowlist and each run's count is recorded in the session doc, because an unrecorded run was indistinguishable from an unrun check and a count-vs-baseline compare allowed net-masking; M3 lines are verified by a non-author at window close, because a decorative line is otherwise traceless. Gaming M1 and E1-E4 leaves grep-detectable traces; the per-metric analysis is in `docs/reviews/20260814_conop_whetstone_debate.md`.

Calibration rule compliance: every gating metric above is anchored to named known-bad references from the archaeology (the 4 dropped entries, the 37-day fix, the 3-cycle-stale CONTEXT.md) and known-good references (same-day instances), so each metric demonstrably rank-orders bad below good before it gates a wave.

---

## Wave Breakdown

Per the validate-before-detail rule: A1/A2 are unfalsified, so Waves 2-5 stay at sketch level until Wave 1 reports. Wave 1 is fully specified.

### Wave 0 — Traversal layer (COMPLETE, committed this session)
Skill v1.0.0, `/pcc` checks 5 (reference integrity, baseline zeroed via allowlist) and 6 (gate-surface separation), proposal amendment, session-end PCC-list drift fix. Evidence: branch `topic/kb-graph-traversal` commit history.

### Wave 1 — Observation window and falsifiers
- **Team**: lead only (observation), test-runner if A5 needs a hook fix.
- **Tasks**:

  | Task | Condition | Standard |
  |------|-----------|----------|
  | Run A2 retroactive routing test | Against the 3 most recent substantive session docs, using only the skill's recipes | Each recorded lesson traced to its owner artifact or explicitly unreachable; result table appended to this CONOP |
  | Run A5 hook liveness check | Touch a matcher-covered `src/` path in a working session | Log line appears in `.claude/audits/`, or a defect task is filed same session |
  | Collect M1/M2/M3 | Across the next 5 qualifying sessions per the skill's definition | Counts recorded by the stated grep commands, appended to this CONOP with session-doc citations |
  | Commit latency baseline | Archaeology digest's L-instance latencies recorded in this CONOP's References | Numbers cited above verified against the named session docs |
  | Verify M3 lines are non-decorative | At window close, each `KB-graph:` line spot-checked by someone other than its author | A line whose traversal did not precede and inform the edit fails; results in the Wave 1 amendment |

- **Exit criterion**: M1/M2/M3 measured and A1/A2/A5 verdicts appended here as a dated amendment.

### Wave 2 — The routing step (sketch; gated on Wave 1: A1 pass AND A2 pass)
Session-end gains the D2 routing step; `session-doc-format.md` gains D9 schema, D1 statuses, D3 headers; the session-end/pcc checklist drift found 2026-08-14 is fixed in the same change. Lead + code-reviewer.

### Wave 3 — Utility slice (sketch; trigger-gated per the amended proposal, independent of Wave 2)
The ~150-line validate/orphans slice, test-first, feature-development team, only on the skill's stated trigger (a demonstrated miss or a new `/pcc` MISSING beyond baseline).

### Wave 4 — Verified propagation, both directions (sketch; gated on Wave 2 bedded in for ≥ 2 sessions)
Propagation tiers (D5), acknowledgment ledger, canary set selection, O2 backlog disposition, `entries[0]` integrity fix in `propagate_doctrine.py` (test-first; this one is code), the D10 harvest step (reads `.claude/upstream-lesson.md` via the existing filesystem discovery; A6 canary seeds precede fleet rollout), and the next cycle's doctrine entry (numbering per the ledger at that time) carrying WHETSTONE's conventions fleet-wide as TEMPLATE-COPY, including the downstream session-end addition that writes fleet-scope lessons to the upstream-lesson file.

### Wave 5 — Close the recursion (sketch; gated on first consolidation session complete)
First D6 consolidation session runs; WHETSTONE's own artifacts enter the loop (this CONOP, the skill, the gates get D1 statuses and D3 headers; changes to them ride `[gate]`-tagged commits per D4). Kata check adopted at session-start: before planning new work, check the last change's verdict.

---

## What We Do NOT Build

- No committed graph artifact, no `graph.json`, no cache (read-time traversal; LazyGraphRAG's economics and the proposal's storage decision).
- No LLM-extracted entity graphs and no vendor memory engines (non-deterministic extraction rot; the benchmark collapse).
- No agent that commits doctrine, flips lesson status, or edits gates autonomously. Humans gate every canonical write; agents propose and evidence.
- No doctrine-throughput dashboards (D8).
- No hard-blocking enforcement of the routing step in this CONOP's scope; escalation beyond WARN-level evidence streams is a future decision on Wave 1-2 data, per the enforcement gradient.
- No new downstream obligations before the canaries validate A3 and A6.
- No cross-repo scraping beyond the filesystem discovery propagation already uses: the hub reads only the two designated channel files (`.claude/upstream-update.md` outbound, `.claude/upstream-lesson.md` inbound), never downstream repos' content at large.

---

## Agent and Team Design

None new. Existing roster covers every wave: lead + reviewer for convention waves, feature-development template for Wave 3/4 code, decision-scientist only if a wave gate becomes a contested decision model. The consolidation session (D6) is a session type, not an agent.

---

## References

- **Commissioned digests (2026-08-14, persisted at `docs/reviews/20260814_whetstone_research_*.md`)**: in-repo archaeology (loop instances L1-L14, 14-channel inventory, census); systems lane (Graphiti bi-temporal edges, Mem0 arbitration, Letta sleep-time compute, LazyGraphRAG economics, Claude Code memory caps, benchmark collapse); loop-design lane (Reflexion/Self-Refine convergence condition, Voyager verification gate, DGM evaluator sabotage, ACE context collapse, ReasoningBank schema, Misevolution drift, AgentPoison, model collapse); institutions lane (NATO JALLC lifecycle, AR 11-33, TC 25-20 AAR Ch.5, CALL/JLLIS, ADP 1-01 layered velocity, ASRS/CAST, NTSB taxonomy, SRE postmortem culture, error budgets, Toyota kata, M&M failure case). Key sources: arXiv 2303.11366, 2303.17651, 2310.01798, 2305.16291, 2505.22954, 2510.04618, 2509.26354, 2407.12784, 2509.25140, 2501.13956; sakana.ai/dgm; JALLC Lessons Learned Handbook 3rd ed.; AR 11-33; TC 25-20; ADP 1-01; sre.google/sre-book/postmortem-culture.
- **In-repo**: `docs/reviews/20260813_kb_graph_tool_evaluation.md` (+ corrections), `docs/plans/20260813_kb_graph_traversal_proposal.md` (+ amendment), `docs/reviews/20260813_kb_graph_adoption_review.md`, `docs/reviews/20260813_kb_graph_adopt_vs_build_maut.md`, `.claude/skills/traversing-the-knowledge-base/SKILL.md`, `docs/propagation-protocol.md`, `.claude/skills/shift-left-testing/ENFORCEMENT.md`, `docs/session-doc-format.md`.
