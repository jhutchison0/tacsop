# Propagation Protocol

How doctrine updates flow from this template repo to downstream consumer repos. Formalizes the implicit process around `scripts/propagate_doctrine.py`.

**Audience**: anyone proposing a change that will affect downstream consumers.

**Authority**: this protocol is itself doctrine. Changes to the protocol go through the protocol.

---

## What Counts as Doctrine

Not every change in `tacsop` is doctrine. A change is **doctrine** if it satisfies all three:

1. **Cross-cutting**: it changes how multiple repos *should* be set up, not just how this repo *is* set up.
2. **Convention-bearing**: it codifies a way of working (naming, layout, agent behavior, skill structure, workflow) rather than a local utility implementation.
3. **Designed for adoption**: it's something we would tell a downstream maintainer to adopt, not just something we did.

A pyproject.toml minimum-Python bump that is intentionally cross-repo? Doctrine.
A new Slack webhook integration in `slack.py`? Not doctrine (utility code, opt-in).
A change to `.claude/skills/SKILLS_FRAMEWORK.md`? Doctrine.
A new test for `geo.py`? Not doctrine (local quality).

If unsure, ask: *would I expect a downstream maintainer to apply this?* If yes, doctrine.

---

## Evaluation Gate (Before Drafting an Update)

Before adding an entry to `docs/doctrine-updates.md`, the proposer answers all five:

1. **What is the change?** One sentence, specific. Files, conventions, or behaviors that change.
2. **Why is it doctrine?** Cite at least two of the three criteria above. If only one applies, it's not doctrine — fold it back to a normal commit.
3. **Who is the audience?** All downstream repos, or a specific subset (e.g., "repos that use the decision_science module")? If subset, the entry must say so explicitly.
4. **What is the action a downstream maintainer takes?** Spell out the steps verbatim — file paths, before/after snippets, expected outcomes. A doctrine update with no `### Action Required` section is incomplete.
5. **What is the rollback path?** If a downstream maintainer applies this and regrets it, how do they reverse? If the answer is "they can't," elevate to an ADR first and let the ADR justify the irreversibility.

A doctrine update that cannot answer all five is not ready to propagate.

---

## Batching Rules

The propagation script extracts **only the most recent entry** in `docs/doctrine-updates.md` (`entries[0]`). This is a hard constraint of the current implementation, and it shapes how changes are batched.

**Rule 1 — One propagation cycle = one entry.** If you have two unrelated changes, you have two options:
- Combine into one entry covering both (preferred when changes are coherent or co-dependent).
- Propagate one, wait for downstream consumption, then add and propagate the next.

**Rule 2 — Never let a doctrine entry mix unrelated changes.** A downstream maintainer who agrees with change A but not change B should be able to apply A and skip B cleanly. Mixing forces all-or-nothing.

**Rule 3 — Trivial bumps batch with the next substantive update.** A single-line Python version bump or a path constant rename does not justify its own propagation cycle. Hold it as a P2 task in `docs/tasks.md` and bundle.

**Rule 4 — Breaking changes get their own entry, no matter how small.** A renamed command, a removed skill, a changed default — these need standalone attention from downstream maintainers, not co-mingled with additive changes.

---

## Cycle Anatomy

A single propagation cycle has six steps:

1. **Draft entry.** Add a `## YYYY-MM-DD: <Subject>` section to the top of `docs/doctrine-updates.md` (most recent first). Include: files changed, files added, change description, scope per audience, **Action Required** checklist.
2. **Pre-flight review.** Run the change through the Evaluation Gate (five questions above). If any fails, fix or downgrade.
3. **Dry run.** `python scripts/propagate_doctrine.py --dry-run` — confirm the expected repo list and notification content.
4. **Propagate.** `python scripts/propagate_doctrine.py` — script writes `.claude/upstream-update.md` in each downstream repo (or appends if a notification already exists).
5. **Log the cycle.** In the next session doc, record: cycle number (continuing from prior count), repo count (new vs appended), and any anomalies (missing repos, append-target mismatches).
6. **Track unread.** Append mode means notifications accumulate until a downstream maintainer deletes the file. This is intentional — never overwrite — but it means you should check `docs/sessions/` for a doctrine consumption record before propagating again.

---

## Downstream Discovery

The script discovers downstream repos by recursive scan of `~/projects/` for any directory containing `.claude/commands/`. Two filters apply:

- **The `tacsop` repo itself is excluded.** Hardcoded by path equality.
- **Nested repos are excluded.** If repo A is inside repo B, only B is notified — A is treated as a submodule or sub-checkout, not an independent consumer.

**Implications**:

- No explicit registry. A new downstream repo is auto-discovered the moment it gets a `.claude/commands/` directory.
- A repo that adopts our template but is in a non-standard parent path (not under `~/projects/`) is invisible. This is acceptable for now but should be revisited if it ever bites.
- A repo that intentionally opts out cannot. The only workaround is to delete its `.claude/commands/` directory, which defeats the purpose.
- **A repo that gitignores `.claude/` is undiscoverable on any fresh clone.** Discovery reads the filesystem, not the roster, so an ignored and therefore untracked `.claude/` is absent the moment the repo is cloned somewhere new. Observed 2026-08-22 in `aar_ai_pipeline`: on the roster since before 2026-07-26, ignoring `.claude/` since commit `1020a43`, and undiscoverable in the clone at `~/projects/gitlab/ops_research/`. **Ignoring `.claude/` is often deliberate** — a repo shared with outside collaborators is commonly scoped to the deliverable, with internal workflow tooling versioned elsewhere. Discovery does not distinguish that from a repo that has simply lost its tooling, and it cannot: both look like an absent directory. The consumer-side fix is the private-sidecar mode in the 2026-08-22 amendment to the 2026-08-21 entry, which restores discovery as a side effect, because a sidecar cloned to `.claude/` puts `.claude/commands` back on disk. Until a consumer adopts one of the two modes, **hand-delivery is the only channel into it.**

**Discovery is not a census.** It reports what is on this machine right now. A name absent from a discovery run may be alive on another machine, cloned without its `.claude/`, or genuinely gone, and the run cannot tell you which. Never prune the roster on a single machine's discovery output.

**Open question (track in `docs/tasks.md` if it becomes pressing)**: should the script support an opt-out file (`.claude/no-propagate`)?

---

## Append Mode

Adopted 2026-03-30. Default and only mode.

**Behavior**: if `.claude/upstream-update.md` already exists in the target repo, the script appends the new entry below the existing content, separated by `\n\n---\n\n`. If absent, it writes a fresh notification with the standard header.

**Why**: a downstream maintainer might not have consumed the prior notification yet. Overwriting would silently drop unread updates. Append preserves the full history of pending notifications.

**Cost**: notification files can grow long if a downstream repo is consistently behind. This is a feature, not a bug — visible debt forces attention.

---

## Version Coordination

The template's `version` in `config/project.yaml` is currently `0.1.0` and does not formally constrain downstream repos. Downstream repos are not expected to track our version explicitly.

**However**: a doctrine entry that depends on a specific template version (e.g., "requires `propagate_doctrine.py` v2 with the new opt-out flag") should say so at the top of the entry. Do not assume downstream repos pull our latest template before applying our doctrine.

If a doctrine change ever becomes version-gated, this protocol gets an ADR.

---

## Rollback

If a propagated change turns out to be wrong:

1. **Author a corrective doctrine entry.** Title it `## YYYY-MM-DD: REVERT — <original subject>`. Spell out what to undo and how. Include before/after snippets in the reverse direction.
2. **Propagate the correction.** Use the same script. Append mode means it lands cleanly even if downstream has not consumed the original yet.
3. **Update `docs/doctrine-updates.md`** to mark the original entry with `(REVERTED YYYY-MM-DD)` after its date header. Do not delete the original; keep the history visible.

**Do not**: rewrite history by editing or removing past entries in `docs/doctrine-updates.md`. Future readers need to see what we asked downstream to do, even when we changed our minds.

---

## Authoring Tone for Action-Required Sections

Doctrine entries are read by maintainers, sometimes weeks after the fact, often by humans who did not participate in the originating discussion. The `### Action Required` section is the contract.

**Do**:
- Lead with the action verb: "Rename X to Y", "Add field Z to project.yaml", "Delete file Q".
- Show before/after when behavior changes silently.
- Number the steps so they can be checked off.
- Name files by full repo-relative path.

**Don't**:
- Reference internal team discussion or session context ("as we discussed Tuesday").
- Use first-person plural ("we decided") — use imperative.
- Assume downstream is on the latest template version.

---

## Civilian/Military Vocabulary

Doctrine entries are downstream-facing. They use the **civilian** vocabulary from `LANGUAGE.md`'s crosswalk. Internal authoring may draft in military terms, but the published entry substitutes:

- PCC → pre-commit-check
- PCI → pre-merge-inspection
- SITREP → status-report
- OPORD → operations-order
- CONOP → concept-of-operations
- TCS → task-condition-standard
- wave → execution-phase

This is enforced at review time, not at draft time. The reviewer checks for military terms in the proposed entry before propagation.

---

## When to Update This Protocol

The protocol itself is doctrine. Updates to the protocol go through the protocol.

Triggers:
- A new propagation mode is added (e.g., opt-out, version-gated, selective subset).
- The script gains or loses capabilities.
- A repeated failure mode is observed (e.g., consistent unread debt in a specific repo).
- A downstream repo reports the protocol fails their workflow.

---

## Roster

Current known downstream consumers (as of 2026-07-26, by name only — discovery is automatic):

`paperboy`, `fema_cria`, `flood_model`, `rmi-reboot`, `shark`, `agent-eval`, `beesly-equilibrium`, `elephant-graveyard`, `magic-movies`, `project-megan`, `quest-engine`, `tactics-game`, `contract-knowledge-graph`, `velocity-scoring`, `fps/maut_platform`, `aar_ai_pipeline`, `ldrd2025_ai_pipeline`, `tc_hurr_risk_modeling`, `veil-engine` (bootstrapped 2026-07-26 from the template at `5f70a48`; successor to `elephant-graveyard`)

This list is informational. The script does not read it. Actual notification targets are determined by filesystem discovery at propagation time.

---

**Last Updated**: 2026-08-22 (Downstream Discovery: recorded the gitignored-`.claude/` failure mode and the rule that discovery is not a census, both from the `aar_ai_pipeline` traversal. Roster itself still wrong in both directions and tracked as a P2 in `docs/tasks.md`.)
**Authoring Skill**: none yet (candidate: future `propagating-doctrine` skill if this protocol gets enough use)
