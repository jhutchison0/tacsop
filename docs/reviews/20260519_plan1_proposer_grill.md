# Review: Grill of Plan1 Framework Revamp Memo

**Author**: proposer
**Date**: 2026-05-19
**Type**: Planning review / proposal analysis

---

## What This Is

The plan memo ("Can't-Miss Ideas for the Claude Code Framework Revamp") is a 240-line step-1 deliverable: a prioritized inventory of ideas before a build sprint. The team lead has already issued a preliminary take — green-lighting some items, pushing back on others, and proposing a P1 scope. This review does not re-summarize the memo. It grills both the memo and the lead's take: hidden assumptions, smuggled decisions, shared blind spots, sequencing risks, and contrarian moves that should at minimum land on the table before scope is finalized.

The codebase inspected: `CLAUDE.md`, `.claude/README.md`, `.claude/skills/SKILLS_FRAMEWORK.md`, all five agent definitions, all six commands, and `config/project.yaml`.

---

## Part I: Hidden Assumptions Nobody Named

### 1.1 The Argonne Vocabulary Assumption

The memo recommends adopting Pocock's `LANGUAGE.md` vocabulary verbatim — specifically the terms "module," "interface," "depth," "seam," "adapter," "deletion test," and "one adapter rule." These are all from Ousterhout's software-design tradition, reinterpreted by Pocock for an agentic context.

The hidden assumption: this vocabulary will be legible and acceptable to the actual user of this framework at Argonne National Laboratory, an ORSA (Operations Research/Systems Analyst) working primarily in decision science, not software architecture.

The word "module" in Ousterhout means "anything with an interface and an implementation." In the ORSA/OR community, "module" often means a self-contained analytical model component, frequently in the simulation or optimization sense. "Interface" in OR usually means the connection between sub-models. "Seam" is pure software vocabulary that will draw a blank stare in an Argonne briefing.

The memo nods at this in section H.4 — "whether the `decision-scientist` agent should adopt Pocock's LANGUAGE.md or stay in OR/METL vocabulary" — but treats it as a single-agent concern. The real scope of the vocabulary collision is wider: it affects CONTEXT.md itself, which is supposed to be a project-wide glossary. If CONTEXT.md lives at the repo root and is shared across the codebase, and the codebase's primary work is OR analysis rather than TypeScript software design, then Pocock's vocabulary is the wrong substrate for the glossary. The glossary terms the user actually needs are things like "criterion," "alternative," "weight," "utility function," "dominated alternative," and "sensitivity analysis" — not "module depth" and "shallow interface."

The plan installs Pocock's LANGUAGE.md to fix one problem (vocabulary drift in code-review comments) and creates a different problem (vocabulary drift between the project's domain language and its code-review language). Neither the plan nor the lead's take names this.

**The real question**: Is CONTEXT.md a software-architecture glossary (Pocock's intended use) or a domain-language glossary (what this project actually needs)? The answer shapes everything about how it's authored and what terms go in it.

### 1.2 The 11-Downstream-Repos Propagation Assumption

The team lead notes this as "missing from the plan" but does not name the full shape of the assumption. The plan was written as if `utils` is the only repo in scope. It recommends actions — cherry-picking skills, migrating commands to skills, adding CONTEXT.md to the repo root, adopting LANGUAGE.md — without once acknowledging that every change to `utils` eventually propagates to 11 downstream repos via the doctrine-propagation system (evidenced in `config/project.yaml`: "propagated to 11 repos" appears in the last session summary).

This is not just a sequencing concern. It is a scope-of-impact concern that changes the risk profile of every recommendation. Here is the actual decision tree:

- If CONTEXT.md is added to `utils` and propagated, every downstream repo inherits a glossary that may or may not fit its domain. A data-pipeline repo and an OR-analysis repo have very different ubiquitous languages.
- If the TDD skill is upgraded to enforce vertical slicing and that skill propagates, every downstream Python developer who relies on the old pattern gets a behavior change in their agent's testing discipline without a migration notice.
- If PCC is migrated to a skill (which the plan recommends), and that migration propagates, every downstream repo's pre-push workflow changes. The `session-end` command currently calls PCC inline; the skill migration changes that coupling.

The lead's proposed sprint scope (P1 = adopt artifacts + TDD upgrade, defer agents and command migrations) is the right instinct but doesn't name why: the reason to defer command migration is specifically the propagation blast radius. That reasoning should be made explicit so it doesn't get relitigated every time someone asks "why are we keeping PCC as a command?"

### 1.3 The Skill Triggering Reliability Assumption

The memo cites Spence's data (20% baseline, 84% with forced-eval hook) and says "instrument an activation hook from day one." The plan then recommends migrating `session-end` and `pcc` to skills, which would make them autonomously-triggerable.

The hidden assumption: the activation hook will work reliably enough to trust for side-effect-heavy operations.

PCC runs `pytest`. Session-end commits to git, writes session docs, and updates `config/project.yaml`. These are not read-only operations. If the skill mis-triggers — fires at 20% baseline rate without a forced-eval hook in place, or even at 84% with one — the cost of a false positive is a git commit at the wrong moment or a test run that races with other work.

The memo's own data says the Haiku model (used by `test-runner`) does not mix well with caveman-compressed output. The same model-sensitivity applies here: autonomous skill triggering requires a sufficiently capable model to correctly evaluate "is this the right moment to run PCC?" Haiku will over- or under-trigger. The plan proposes migrating PCC to an autonomously-triggerable skill without specifying which model handles the triggering decision.

The lead's push-back on "migrating session-end/pcc to skills (auto-trigger + side effects is bad)" is correct, but the reasoning given is thin: "auto-trigger + side effects." The fuller argument is: even at 84% activation reliability, a 16% miss rate on a safety-gate operation is too high, and a false-positive rate on a commit workflow is unacceptably costly. These are not cases where "getting it wrong sometimes" is acceptable.

### 1.4 The Interface-Designer Token Cost Assumption

The plan recommends adding `interface-designer` as a new agent that spawns 3+ parallel subagents for design exploration. The memo cites Anthropic's multi-agent cost data: "roughly 3.75x more tokens than a single agent." But the plan applies this selectively — recommending against a "parallel-implementation agent fleet" for that reason while still recommending `interface-designer`.

The hidden assumption: interface exploration problems are categorically "breadth-first" (Anthropic's framing for when multi-agent is appropriate), whereas implementation problems are "dependency-heavy" (Anthropic's framing for when it's not). This distinction is real but overstated as binary. Most interface design questions for a Python utility library involve enough shared constraints (existing callers, existing test patterns, the venv's dependency set) that three independently-operating subagents will produce interfaces that conflict in ways that require a human to resolve. The "parallel subagents for design, sequential debate for evaluation" recommendation is theoretically sound but untested in this specific context.

The lead pushes back on `interface-designer` for the right reason — "3x token spend by default" — but doesn't name the deeper assumption: that interface exploration for a Python utility library (which has narrow, concrete scope) benefits from the same breadth-first multi-agent pattern that benefits open-ended research problems. It probably doesn't. The proposer/code-reviewer sequential debate is already doing design exploration; adding a parallel-subagent layer increases cost without guaranteed quality gain.

### 1.5 The "Grill-Master Is Redundant" Assumption

The lead pushes back on the `grill-master` agent as "redundant with proposer." The plan itself doesn't push this recommendation hard — it's listed under "Add" in section E but the memo's own mapping table (section C) already says "your OPORD/CONOP/TCS escalation does exactly this." So both the plan and the lead agree grill-master is redundant.

What neither names: the `proposer` agent as currently defined (`proposer.md`) does not ask questions one at a time and wait for answers. It reads the codebase, reasons through approaches, and writes a proposal document. That is design analysis, not interrogation. Pocock's `/grill-me` skill does something structurally different: it runs an interactive Q&A loop where the agent asks one question, recommends an answer, waits for feedback, and only proceeds when that question is resolved.

The proposer is the right tool for "here are three approaches, here are the trade-offs, recommend one." It is not the right tool for "I need to interview you about every aspect of this plan until we reach shared understanding." Those are two different shapes of work. Dismissing grill-master as redundant because both involve "asking questions" conflates the two shapes. The real question is: does the existing framework have a tool for structured interrogation in the CONOP-development phase? The answer is no — the `/grill-me` pattern lives in commands (CONOP/OPORD development) but as a document format, not as an interactive Q&A discipline enforced by an agent.

---

## Part II: Smuggled Decisions

### 2.1 "Migrate session-end to skill" smuggles "we trust autonomous triggering for commit workflows"

The plan's section F says: "Migrate to skill `handing-off-session` (P2 #7). The work it does (compact, produce handoff) is something Claude should be able to trigger autonomously when the conversation approaches a token budget."

That last clause is doing a lot of work. The claim is that Claude should autonomously decide to compact and produce a handoff document when the context window tightens. But `session-end` as it exists in `.claude/commands/session-end.md` does not just compact — it: runs PCC, stages and commits code, updates `config/project.yaml`, writes a session doc, and evaluates merge readiness. Migrating this to an autonomously-triggerable skill means Claude might decide to commit code in the middle of an in-progress task because the context looks full. That is a regime change in who controls the commit boundary.

The plan tries to thread this needle by saying "keep a `/session-end` slash trigger via skill frontmatter" — i.e., the explicit invocation path survives the migration. But the point of migrating to a skill is to enable autonomous triggering. If the safe behavior is to always invoke it explicitly, the migration provides no benefit and introduces the risk of accidental autonomous triggering. The plan can't have it both ways.

The real decision being smuggled: should the commit workflow ever be autonomously triggerable? That is a policy question about the human-in-the-loop boundary, not a technical question about skill vs. command format. The plan buries it in a table row.

### 2.2 "Adopt Pocock's LANGUAGE.md verbatim" smuggles "Ousterhout's vocabulary is correct for this domain"

Section B4 recommends adopting Pocock's LANGUAGE.md "verbatim because it disambiguates terms that DDD, REST, and TypeScript all overload." The memo is describing a TypeScript ecosystem problem — Pocock's audience is TypeScript engineers who work in environments where "module," "interface," and "component" are all overloaded by different frameworks. Adopting the vocabulary verbatim makes sense in that context.

This project is a Python utility library used by an ORSA at a national laboratory. The overloaded terms in this context are not "module" and "interface" — they're "model," "criterion," "sensitivity," and "alternative." The plan adopts Pocock's disambiguation of a different ecosystem's vocabulary conflicts and presents it as a universal fix.

The decision smuggled: Pocock's vocabulary is ecosystem-agnostic and applies to Python OR work. This has not been validated. The plan says nothing about whether Pocock has ever been applied outside TypeScript web development.

### 2.3 "Add interface-designer as your sixth agent" smuggles "three design alternatives is the right parallelism level"

Pocock's `/design-an-interface` spawns "3+ parallel subagents, each constrained to a different design philosophy (minimalist, maximally flexible, common-case optimized, paradigm-inspired)." The plan recommends porting this directly. But the memo's own citation of Anthropic's cost data says "multi-agent systems use about 15x more tokens than chats." An interface-designer agent that spawns three subagents does not cost 3.75x — it costs 15x more than a chat interaction, and 3.75x more than a single agent. For a Python utility library that adds one module at a time, the majority of interface design questions have two or three plausible answers, not four or five, and a single proposer agent already covers this space adequately.

The plan implicitly decides "the design exploration problem is always worth the 3.75x agent premium" without validating this against the actual design questions that come up in this project.

---

## Part III: What the Plan and the Lead Are Both Missing

### 3.1 The Propagation Protocol Is Not Defined

Neither the plan nor the lead's take describes how doctrine changes propagate from `utils` to the 11 downstream repos. The session summary mentions it happened ("propagated to 11 repos") but there is no artifact in the codebase describing the propagation mechanism. Is it a manual copy-paste process? A git submodule? A script? The plan proposes adding CONTEXT.md, LANGUAGE.md, ADRs, upgraded TDD enforcement, and potentially migrating commands — without specifying how any of these changes reach the 11 downstream repos or who is responsible for the propagation.

This matters because some of the recommended changes are more propagation-friendly than others:
- CONTEXT.md at the repo root: Every downstream repo would need its own CONTEXT.md, since their ubiquitous languages differ. Propagating the template is fine; propagating the content is wrong.
- LANGUAGE.md: Could propagate as a shared reference, but see the vocabulary-fit concern above.
- Upgraded `shift-left-testing.md` skill: This one propagates cleanly — it's a behavior change in an existing skill, not a new artifact.
- Command-to-skill migrations: Highest propagation risk. A downstream repo that has built workflows on top of `/pcc` as a command will break if `/pcc` silently becomes an autonomously-triggerable skill.

The plan needs a propagation-impact assessment for each P1 item. The lead's sprint scope doesn't provide one.

### 3.2 The SKILLS_FRAMEWORK.md Is the Wrong Carrier for Level 0/Level 1 Policy

The `SKILLS_FRAMEWORK.md` at `.claude/skills/SKILLS_FRAMEWORK.md` defines the Level 0 / Level 1 distinction (universal vs. project-specific), the skill structure template, content guidelines, and porting instructions. It is the governing document for how skills work in this project and its 11 descendants.

The plan recommends adding four new Level 0 skills (maintaining-ubiquitous-language, recording-architecture-decisions, writing-tests-first, evaluating-module-depth) and migrating existing commands to skills. None of the plan's recommendations address whether `SKILLS_FRAMEWORK.md` itself needs to be updated to reflect the new skill format (the plan's recommended format includes `description` field and gerund naming, but `SKILLS_FRAMEWORK.md`'s "Skill Structure Template" section uses a different frontmatter structure — `name`, `description`, `version` — and does not mention the `allowed-tools` field or autonomous-vs-explicit invocation mode).

The SKILLS_FRAMEWORK.md was last updated 2025-12-07. Anthropic's open standard for skills went live December 18, 2025. The framework predates the open standard by eleven days. It is plausible that the skill structure template in `SKILLS_FRAMEWORK.md` is already out of date with Anthropic's current spec. The plan should have flagged this but did not.

### 3.3 The Civilian/Military Crosswalk Has No Home

The lead's take flags "where the civilian/military crosswalk lives" as missing from the plan. This is correct and the problem is deeper than it looks.

The current codebase uses military vocabulary throughout: PCC/PCI (Pre-Combat Check/Inspection), CONOP/OPORD/TCS (military planning formats), SITREP (situation report), and "waves" for parallel execution units. This vocabulary is consistently applied across `CLAUDE.md`, `session-start.md`, `session-end.md`, `pcc.md`, `pci.md`, `task.md`, and `.claude/README.md`.

The plan recommends civilian-facing aliases for external publication (section H.6, "strongly recommend you keep PCC/PCI/OPORD/CONOP/TCS in your internal documentation but rename the user-facing slash commands and skill descriptions to civilian equivalents in any repo you publish externally"). But the plan does not specify:

1. Which of the 11 downstream repos are intended for external publication vs. internal use only
2. Whether the crosswalk should live in `CLAUDE.md`, `SKILLS_FRAMEWORK.md`, or a dedicated crosswalk document
3. Whether agents are expected to translate on the fly or whether there should be two canonical vocabularies
4. How CONTEXT.md would handle terms that have both a military internal name and a civilian external name — the glossary would need dual entries or a clear "canonical form"

The crosswalk is not just a naming convenience. It determines whether the 11 downstream repos can share skill files with each other or whether repos intended for different audiences need different skill bodies.

### 3.4 The Backwards-Compatibility Cliff for Command Users

The lead flags "backwards-compat plan if renaming commands" as missing. The fuller picture: this project's 11 downstream repos and their users have built muscle memory around `/pcc`, `/pci`, `/session-start`, `/session-end`, `/sitrep`, and `/task`. The plan's section F migration table is written as if these commands are only used in `utils`. They are likely used in all 11 downstream repos, possibly by people who do not follow `utils` development closely.

The Anthropic documentation cited in the plan says "a file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way" — meaning the user-facing invocation stays the same. But the behavioral change (autonomous triggering becoming possible) is invisible to users who have never read the migration rationale. A downstream user who has trained themselves to always run `/pcc` before pushing will not notice that `/pcc` can now also fire autonomously in mid-session. The risk is not that the slash command breaks; the risk is that the semantics change silently.

### 3.5 The Context Budget Discipline Has No Enforcement Mechanism

The plan cites Anthropic's "Effective context engineering" and the "smart zone" concept (roughly 100k tokens, past which attention degrades). It recommends adding "token-budget checkpoints" to session-start and session-end. But the current `session-start.md` command already loads: project.yaml, the most recent session doc, the task list, and runs git fetch + pytest + git status. That is already a substantial context load before any user work begins.

The plan's only response is "add a token-budget checkpoint." But a checkpoint that says "you are at X tokens" is observational, not behavioral. The mechanism that would actually constrain context bloat is: shorter skills, faster SKILL.md bodies, more aggressive use of progressive disclosure, and a hard rule on how much is loaded at session-start. None of these are proposed concretely.

The "compressing-output" skill (`/caveman`) is listed as P2/optional. If context budget discipline is the foundational problem (the plan makes this argument in section A.3), then compression and progressive disclosure tooling should be P0, not optional. The plan buries the most important mechanism.

---

## Part IV: Sequencing Risks

### 4.1 CONTEXT.md Before LANGUAGE.md Is Backwards

The plan recommends building `maintaining-ubiquitous-language` as P1 skill #1, which creates and maintains CONTEXT.md. It recommends adopting LANGUAGE.md as part of the `evaluating-module-depth` skill (#4 in P1). This sequences CONTEXT.md before LANGUAGE.md.

The problem: CONTEXT.md is a glossary that uses terminology. If you start writing CONTEXT.md before you've settled on LANGUAGE.md, you will use ad-hoc terminology in the glossary. When LANGUAGE.md arrives, you have to go back and rewrite every CONTEXT.md entry that used pre-LANGUAGE.md vocabulary. In a project with 11 downstream repos, that is a non-trivial retcon.

The right sequence: settle LANGUAGE.md first (or decide not to adopt it), then author CONTEXT.md using the settled vocabulary. This is the exact sequence Pocock uses in his own repo — LANGUAGE.md is a reference document that CONTEXT.md entries are allowed to cite.

### 4.2 TDD Upgrade Before Interface Design Is a Training Problem

The plan upgrades the `shift-left-testing.md` skill to enforce vertical slicing as P1 item #3. It adds `interface-designer` as a new agent (deferred by the lead, but still in the plan). Vertical-slicing TDD requires knowing the interface before writing the first test. If you enforce vertical TDD before you have an interface-design discipline, agents will try to write tests against interfaces they're inventing as they go. The resulting tests will be coupled to implementation details (the most common TDD failure mode) rather than stable public interfaces.

The correct sequence: establish interface-design discipline first (whether that's the `proposer` agent's expanded scope, a new `interface-designer` agent, or Pocock's six-item planning checklist embedded in the TDD skill), then upgrade TDD enforcement. The plan reverses this.

### 4.3 ADRs Before Architectural Vocabulary Is Misaligned Record-Keeping

The plan recommends `recording-architecture-decisions` as P1 item #2 and `evaluating-module-depth` (which carries Pocock's LANGUAGE.md vocabulary) as P1 item #4. That means ADRs get written using whatever vocabulary is at hand (#2) before the project's architectural vocabulary is settled (#4). ADRs written before LANGUAGE.md adoption will use terms like "class," "service," "component," and "boundary" — terms that LANGUAGE.md specifically replaces with "module," "interface," "seam," and "adapter." The ADRs written in P1 will be out of vocabulary with the vocabulary established in P1. The remediation is another retcon pass.

Correct sequence: LANGUAGE.md (or its substitute), then CONTEXT.md, then ADRs. The plan inverts all three.

---

## Part V: Contrarian Moves Worth Debating

### Contrarian A: Don't Build CONTEXT.md — Build a Decision Log Instead

**Thesis**: CONTEXT.md as Pocock defines it is a real-time glossary maintained during conversations. It requires the agent to have write access to the repo root during every conversation, it requires discipline from every agent to add terms as they're coined, and it requires a human to occasionally prune and curate. For a Python utility library with a relatively small vocabulary (the source modules are `logger`, `excel`, `parallel`, `geo`, `weights`, `slack`, `database`, `math_utils`), the glossary maintenance overhead exceeds the benefit.

What the project actually lacks is not a glossary — it's a record of architectural decisions. The last session summary says "propagated to 11 repos" for a change involving Python 3.11 and `docs/reviews/` convention adoption. There is no ADR explaining why 3.11 was chosen, what alternatives were considered, and whether the decision is revisable. The framework has a propagation mechanism but no record of what was propagated and why.

A Decision Log — a running `docs/decisions.md` with date-stamped entries, not a formal ADR directory — would capture this with lower overhead. Entries look like: "2026-04-21: Adopted docs/reviews/ convention. Previous: docs/ only. Reason: clearer agent output separation. Reversibility: low (11 downstream repos now expect this path)." This is lighter than Pocock's triple-filter ADR system, captures the same institutional knowledge, and requires no vocabulary pre-work.

**Why it's bold**: The plan and the lead both green-light ADRs. Replacing ADRs with a simpler decision log challenges both.

**Who it scares**: Anyone who wants the full Pocock ADR system (hard-to-reverse + surprising + real-tradeoff filter). The filter is valuable discipline, but it may be more apparatus than a small utility-library project needs.

**How to test cheaply**: Write three decision-log entries for real decisions already made (Python 3.11 choice, docs/reviews/ convention, the shift-left-testing pillar). Ask: would Pocock's triple-filter ADR format have added information? If yes, migrate to ADRs. If no, the log is sufficient.

---

### Contrarian B: Freeze the Template, Build the Propagation Protocol

**Thesis**: The highest-leverage work is not adding new skills, agents, or artifacts to `utils` — it's formalizing the mechanism by which changes in `utils` reach the 11 downstream repos. Right now that mechanism is implicit (evidenced by the session summary mentioning propagation but no document describing it). An implicit propagation mechanism means:

1. No one knows which changes propagate and which don't
2. No one knows how to validate that propagation happened correctly
3. No one knows the backwards-compatibility rules for propagated changes
4. The 11 downstream repos may have already diverged from `utils` in unknown ways

The plan adds six new things to propagate without first establishing what "propagate" means in operational terms. The contrarian move: declare a moratorium on new framework features and spend the sprint writing the propagation protocol — a document or script that defines: (a) what gets copied, (b) what gets adapted per-repo, (c) how a downstream repo signals it has accepted a propagation, and (d) what the rollback procedure is.

This is the "fix the supply chain before expanding the product line" argument.

**Why it's bold**: It explicitly defers everything the plan recommends — CONTEXT.md, ADRs, TDD upgrade, new agents — in favor of meta-infrastructure work that nobody asked for.

**Who it scares**: The team lead, who already has a green-lit P1 scope. This proposes scrapping P1 in favor of a different kind of P1.

**How to test cheaply**: Try to propagate a single change (say, adding CONTEXT.md template to `utils`) to one downstream repo and document every decision you have to make in the process. The list of decisions is the propagation protocol's first draft. If there are more than five decisions, the protocol is worth formalizing before proceeding.

---

### Contrarian C: Collapse Agents, Not Expand Them

**Thesis**: The plan recommends adding `interface-designer` (spawning 3+ subagents), `architecture-auditor`, and `grill-master` to the existing five agents. The lead pushes back on all three but for tactical reasons (token cost, redundancy). The more fundamental question: the current five-agent roster is already underutilized in practice. The `decision-scientist` was added recently; there is no evidence in the session docs of it being deployed on a real problem. The `proposer` is a new role being exercised right now for the first time on this grilling task.

Before adding agents, verify that the existing agents are actually being deployed on their intended problems. The pattern "add more agents to solve problems the current agents aren't being used on" creates a growing roster of theoretically-capable but practically-unused agents. Each agent definition is context overhead at session-start (the agent roster in `.claude/README.md` is loaded). Each additional agent adds cognitive load for the human deciding which team to assemble.

The contrarian move: instead of adding agents, consolidate. Merge `code-reviewer` into a mode of `proposer` (review is analysis in adversarial mode). Retire `decision-scientist` or fold it into `python-prototyper` as a domain-specific skill rather than a separate agent. Reduce to three agents: `python-prototyper` (builds), `test-runner` (verifies), and `proposer` (analyzes, reviews, and debates). This is a smaller roster with clearer swim lanes.

**Why it's bold**: The plan goes to seven or eight agents; this proposal goes to three. It challenges the entire "more specialized agents = better outcomes" assumption.

**Who it scares**: Anyone who has invested in the current agent definitions. The `decision-scientist` definition in particular represents real domain expertise encoded in agent instructions.

**How to test cheaply**: For the next three tasks in this project, deliberately use only `proposer` + `python-prototyper` + `test-runner`. See if anything is genuinely missing. If `decision-scientist` would have caught something the other three didn't, that is evidence for keeping it. If not, the three-agent roster is sufficient.

---

## Part VI: Specific Challenges to the Lead's Take

### 6.1 The Lead Green-Lights TDD Vertical-Slicing Without Naming the Prerequisite

The lead's green-light for "TDD vertical-slicing enforcement" is correct in principle. The missing prerequisite: vertical slicing requires a stable interface before the first test. The current `shift-left-testing.md` skill does not include Pocock's six-item interface-confirmation checklist (confirm interface changes, confirm behaviors to test, design for testability, list behaviors not steps, get approval). Upgrading the TDD enforcement without adding the interface-confirmation step will produce TDD that is formally "vertical" but practically still implementation-coupled, because developers will skip the interface-design step and jump straight to testing.

The lead should explicitly require that the TDD upgrade includes the full six-item checklist, not just the "one test at a time" rule.

### 6.2 The Lead's Sprint Scope May Be Too Wide on the Wrong Axis

P1 as proposed: CONTEXT.md + ADRs + LANGUAGE.md + TDD upgrade. That is two new artifact types (CONTEXT.md and ADRs), one new vocabulary standard (LANGUAGE.md), and one skill upgrade (TDD). This is additive on four dimensions simultaneously. The sequencing risks described in Part IV apply directly: LANGUAGE.md before CONTEXT.md before ADRs is the correct order, and the proposed P1 does all four in an unspecified order.

A tighter P1 that respects sequencing: LANGUAGE.md vocabulary decision only (adopt it, adapt it, or reject it — a single document decision, not a build task). Then, in a separate sprint, CONTEXT.md using the settled vocabulary. Then ADRs after CONTEXT.md establishes the glossary terms. TDD upgrade is orthogonal and can run in parallel with any of these, but should include the interface-checklist prerequisite.

### 6.3 The Lead's Push-Back on Bulk Cherry-Pick Is Correct but Under-Argued

"Push back on bulk cherry-pick from mattpocock/skills" is the right call. The reason given is light — implied "it's too much." The fuller argument: `mattpocock/skills` is TypeScript-first. His TDD skill references TypeScript interfaces, his architecture skill is tuned to TypeScript module resolution, and his LANGUAGE.md disambiguates TypeScript-ecosystem overloads. Cherry-picking individual skills means extracting content that was written for a different language, a different community (web development), and a different model of what "module depth" means in practice (class hierarchies vs. Python modules vs. pip packages vs. OR model components). Each cherry-picked skill needs a Python-specific adaptation pass, not just a rename. The lead should say "cherry-pick with required Python adaptation" not just "be selective."

### 6.4 The Lead Does Not Address the SKILLS_FRAMEWORK.md Update Need

The lead's take and the plan both omit what is arguably the most important piece of housekeeping: `SKILLS_FRAMEWORK.md` needs to be updated to reflect the Anthropic open standard (December 18, 2025), which postdates the framework's last update (December 7, 2025). Before adding four new skills authored to the open standard, the framework document that governs skill authoring should reflect the current standard. If `SKILLS_FRAMEWORK.md` still shows the pre-open-standard frontmatter template, the four new P1 skills will be authored inconsistently with it.

This is not a new capability gap — it's a documentation debt that predates the plan.

---

## Part VII: What Should Actually Happen Before P1 Starts

Rank-ordered by logical dependency:

1. **Decide the SKILLS_FRAMEWORK.md update**: Does the current skill structure template need to be updated to match the Anthropic open standard? Yes or no, but make the call explicitly. If yes, update first. If no, document why.

2. **Make the vocabulary decision**: Adopt Pocock's LANGUAGE.md verbatim, adapt it for Python/OR context, or reject it and define project-specific vocabulary. This is a single decision that gates both CONTEXT.md and ADR authoring. The decision should produce a one-page crosswalk if adapted.

3. **Define the propagation protocol**: Even informally. A list of: what propagates automatically, what requires per-repo adaptation, and what the signal is that a downstream repo has accepted a change. This takes one session and prevents the 11-repo blast-radius problem from happening silently.

4. **Specify the TDD upgrade scope**: The upgrade should explicitly include Pocock's six-item interface-confirmation checklist. If the upgrade doesn't include this, it's an incomplete port.

5. **Only then**: CONTEXT.md template, ADR structure, and the TDD skill upgrade as a single coordinated build.

---

## Summary Table

| Item | Plan Says | Lead Says | This Review Says |
|------|-----------|-----------|-----------------|
| CONTEXT.md | Build it (P1 #1) | Green-light | Sequence after LANGUAGE.md; consider Decision Log as lighter alternative |
| ADRs | Build it (P1 #2) | Green-light | Sequence after CONTEXT.md; beware vocabulary pre-requisite |
| LANGUAGE.md | Adopt verbatim (B4) | Green-light | Verify vocabulary fit for Python/OR domain before adopting verbatim |
| TDD upgrade | P1 #3 | Green-light | Include six-item interface checklist; sequence after interface-design discipline |
| session-end to skill | Recommend it (F) | Push back | Correct to push back; smuggled decision about autonomous commit control |
| pcc to skill | Recommend it (F) | Push back | Correct to push back; activation reliability at 84% is too low for safety-gate |
| interface-designer | Add it (E) | Push back | Correct to push back; design space in this project doesn't require 3+ parallel subagents |
| grill-master | Add it (E) | Push back (redundant) | Not redundant with proposer; but interactive Q&A discipline belongs in a skill, not a new agent |
| Propagation protocol | Not mentioned | Missing | Highest-priority missing item; blocks all other work at scale |
| SKILLS_FRAMEWORK.md update | Not mentioned | Not mentioned | Pre-dates the open standard; should be updated before new skills are authored |
| Civilian/military crosswalk | Mentioned briefly (H.6) | Flagged as missing | Needs a home and a canonical-form decision; affects CONTEXT.md authoring |
| Cherry-pick from mattpocock/skills | Cherry-pick, don't bulk-install | Push back on bulk | Correct, but cherry-picks need Python adaptation, not just renaming |

---

## One Sentence for Each Bold Move

**Contrarian A (Decision Log over CONTEXT.md)**: If the real gap is "no record of why we did things," a running decision log delivers that with less overhead than a live glossary that requires vocabulary pre-work.

**Contrarian B (Freeze the template, build the propagation protocol)**: You can't responsibly expand what you're distributing until you know how distribution works — the propagation mechanism is load-bearing infrastructure that is currently implicit.

**Contrarian C (Collapse agents, not expand them)**: Three agents used consistently outperform eight agents used occasionally, and the current roster has not been stress-tested at full deployment depth before expansion is proposed.
