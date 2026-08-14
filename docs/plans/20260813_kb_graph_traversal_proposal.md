# Proposal: Knowledge-Base Traversal, Skill Before Code

**Author**: proposer
**Date**: 2026-08-13
**Type**: Design proposal (debate stage, precedes implementation)
**Branch**: `topic/kb-graph-traversal`
**Follows**: [docs/reviews/20260813_kb_graph_tool_evaluation.md](../reviews/20260813_kb_graph_tool_evaluation.md) (session lead's graphify supply-chain evaluation; read it first)
**Status**: Accepted (Approach B shipped as Wave 0 of CONOP WHETSTONE, 2026-08-14; the deferred-build spec in Approach A, as amended, is live and governed by that CONOP's Wave 3)

---

## Problem

Agents reading this repo's knowledge base fall back to full-file reads and ad hoc grep, even though the corpus already carries an explicit, hand-authored graph. Session docs declare seven typed edges (`docs/session-doc-format.md`'s Follows, Documents, Implements, References, Completes, Requires, Cites). `CONTEXT.md` hand-maintains a Reading Order. `docs/tasks.md` and `docs/doctrine-updates.md` reference each other constantly. Nothing currently tells an agent to walk that structure instead of grepping past it.

The lead's review (`docs/reviews/20260813_kb_graph_tool_evaluation.md`) asked whether to adopt a third-party tool (graphify) or build a minimal one, and recommended building, with graphify held in reserve for downstream repos with real code-graph needs. This proposal answers the question the lead left open to the panel: not just how to build a traversal tool, but whether one needs to be built yet, and how small the eventual build can be if it does.

**Corpus snapshot, verified this session** (all counts from live commands against this branch, not estimates):

| Metric | Count |
|---|---|
| Markdown files in scope (docs/, .claude/, repo root; excludes `.venv/`, `.git/`, `.pytest_cache/`) | 103 (102 git-tracked, plus this proposal's predecessor review, added this session) |
| Total size of that corpus | 1,021,553 bytes (~1.0 MB) |
| Proper markdown links `[text](path.md)` | 157 |
| Bare backtick-quoted `.md` paths outside link syntax, e.g. `` `docs/tasks.md` `` | 816 unique matches |
| Bare `ADR-NNNN` mentions outside link syntax | 51 |
| Session docs carrying typed Follows/Documents/etc. headers | 17 of 18 |
| Full four-extractor regex sweep of the entire corpus, stdlib `re`, cold, no cache (20-run average) | 3.45 ms |

Two findings shaped this proposal more than the raw counts:

1. **Bare path mentions outnumber proper links five to one.** `docs/tasks.md` and `docs/doctrine-updates.md` reference most files as backtick-quoted paths in prose or in `Files (tacsop)` code blocks, not as clickable markdown links. A tool that only follows `[text](path)` syntax would miss most of the real reference graph in exactly the two files agents consult most for orientation.
2. **The corpus already has live drift a systematic check would catch.** `docs/tasks.md`'s P3 line "Decide the five untracked March decision-science docs" names `docs/decision_audit_20260326.md`, `docs/plans/decision_science_gaps.md`, `docs/review_decision_science_waves_2_3.md`, and two `docs/reviews/2026-03-26_*` files. I checked: none of the five exist in this working tree. The likeliest explanation is the multi-machine sync gap the P1/P2 tasks already name (work/home/laptop clones), but I do not know for certain. What is certain is that a 200-line hand-maintained task file has been carrying three dangling file references without anyone noticing, which is the exact failure class a validity check exists to catch.

Why this matters now: the user's stated concern is private data leaving the machine, and this repo is a template propagated to 15 downstream repos (`docs/propagation-protocol.md`). Whatever gets adopted here becomes doctrine that 15 or more independently maintained repos inherit. The bar for adding new machinery should be correspondingly high.

---

## Approaches Considered

### Approach A: Deterministic build-own kb-graph utility

A stdlib-only Python module plus a thin CLI that parses the corpus into a typed edge graph and answers query requests on demand. This is the shape the lead's review sketched as Option B. Below is the concrete design, specified fully so it can be built or shelved as one piece.

**Edge types, in descending order of confidence:**

1. **Markdown links** `[text](path.md)`, EXTRACTED provenance. 157 in the corpus today. Resolve relative to the source file's own directory; strip `#anchor` for node identity, keep it on the edge for display.
2. **Typed header relations**, EXTRACTED provenance, highest confidence. The seven relation labels session-doc-format.md already pins (Follows, Documents, Implements, References, Completes, Requires, Cites). Syntactically a subset of type 1: same link inside a `**Label**:` line, but the label gives the edge a semantic type instead of a generic "link."
3. **Bare backtick path mentions**, INFERRED provenance. 816 raw matches. Kept as an edge only if the referenced path resolves to a file that exists in the corpus. A mention that does not resolve is not discarded; it becomes a `validate()` finding instead of an edge (see below), because a dangling mention is itself useful information.
4. **Named-entity mentions**, INFERRED provenance. Bare `ADR-NNNN` tokens (51 found) resolved against `docs/adr/NNNN-*.md` by numeric prefix; dated doctrine entries (`## YYYY-MM-DD: Title` in `doctrine-updates.md`) resolved when a task or session doc cites the same date.
5. **Wikilinks** `[[name]]`, EXTRACTED provenance, resolved against a memory file's frontmatter `name:` field. `.claude/agent-memory/` is gitignored (`.gitignore:56`) and holds zero files right now, including this session's own `proposer/` directory. The extractor is roughly three lines sharing the markdown-link code path, so it costs nothing to write, but there is no wikilink corpus to traverse today. See Open Question 4.

**Traversal queries.** The task named five; I found a sixth live use case during this session's own exploration and added it.

- **`neighbors(path)`**: one-hop edges, both directions. `CONTEXT.md`'s Reading Order is a hand-maintained neighbors list; this query lets an agent check it against the actual link graph, or draft a first version for a new project's `CONTEXT.md`.
- **`backlinks(path)`**: inbound edges only. Before editing `docs/propagation-protocol.md` or `docs/design/pillars.md`, an agent could ask what depends on it instead of trusting memory. This is the same blast-radius question CONOP-FORMAT.md's "Enemy Forces" section already asks by hand.
- **`lineage(path, relation="Follows")`**: transitive walk of one relation type, both directions, generalized so the same function also serves an Implements chain or a Requires chain without new code. `/session-start` currently orients on "most recently modified file" in `docs/sessions/` (CONTEXT.md reading-order item 8); lineage would return the actual Follows chain the heuristic is standing in for.
- **`orphans()`**: nodes with zero inbound edges, excluding declared roots (`README.md`, `CONTEXT.md`, anything named as an entry point in `config/project.yaml`).
- **`path(a, b)`**: shortest path by breadth-first search over the union of typed edges. Example: tracing why the 2026-07-20 doctrine entry's Part 2 exists, from `doctrine-updates.md` back through its session doc to the four-repo retrospective reviews it cites.
- **`validate()`**, added beyond the requested five: every INFERRED mention that fails to resolve becomes a finding. The `docs/tasks.md` P3 case above is the worked example; it would surface on the first run.

**Storage format: none, by design.** A full four-extractor parse of all 103 files measured 3.45 ms per sweep, stdlib `re`, cold, no cache, averaged over 20 runs. At that cost, a committed `graph.json` buys no speed and adds a failure mode this repo does not currently have: a committed graph goes stale the moment someone edits a doc without regenerating it, and a generated JSON blob is a natural merge-conflict magnet under concurrent multi-agent editing. Rebuild the graph in memory on every CLI call. Source the file list from `git ls-files '*.md'`, not a hand-rolled directory walk. `git ls-files` gives the exact set of tracked files and, for free, excludes `.venv/`, `.git/`, and `.pytest_cache/`. The throwaway timing probe I wrote for this proposal used a naive `rglob("*.md")` and picked up 13 files from `.venv/` and one from `.pytest_cache/` that have nothing to do with the knowledge base; `git ls-files` would not have made that mistake. If a future, far larger corpus ever makes 3 to 4 ms too slow, the fallback is a gitignored cache under `.claude/audits/` (the shift-left violations log already lives there, gitignored), never a committed artifact.

**Placement: `scripts/kb_graph.py`, not `src/myproject/utils/`.** The `utils/` package (`geo.py`, `math_utils.py`, `weights.py`) is portable business logic meant for a downstream project's own application code to import. `kb_graph.py` parses this repo's own doctrine conventions, the same job `propagate_doctrine.py` and `adopt_doctrine.py` already do from `scripts/`. It operates on the repo; it is not a library the repo's eventual application would import. This follows a distinction the codebase already draws, not a new one.

**Rough size.** `propagate_doctrine.py` is the closest existing analog: 124 production lines, 14 tests across 245 lines, built test-first. `kb_graph.py` has more surface (four extractors instead of one, six query functions instead of zero), but each function is small and pure, in the same one-purpose-per-function shape as `geo.py`. Estimate 250 to 350 production lines and 12 to 16 vertical test slices, roughly one per extractor behavior and one per query function:

1. Markdown-link extraction: one link resolves to one edge.
2. Markdown-link extraction: non-`.md` targets ignored.
3. Header-relation extraction: a `**Follows**: [x](y.md)` line produces a typed edge.
4. Header-relation extraction: a fixture built from session-doc-format.md's own seven labels produces seven typed edges.
5. Bare-mention extraction: a backtick path resolving to a real file becomes an edge.
6. Bare-mention extraction: a backtick path resolving to nothing becomes a `validate()` finding, not an edge.
7. Wikilink extraction: empty corpus returns an empty list without error.
8. `build_graph()`: end-to-end assembly over a small `tmp_path` fixture repo (the SCRIPTS.md repo-factory pattern already used in `test_adopt_doctrine.py`), 3 to 4 fixture files.
9. `neighbors()`: both directions on a fixture graph.
10. `backlinks()`: inbound only.
11. `lineage()`: walks a three-doc Follows chain in order, both directions.
12. `orphans()`: an unlinked node is flagged; a declared root is excluded.
13. `path()`: finds a two-hop path; returns `None` when disconnected.
14. `validate()`: reproduces the `docs/tasks.md` P3 finding against a fixture that mirrors it, as a regression case.
15. CLI smoke test: `--json` output shape, one flag, mirroring `propagate_doctrine.py`'s `--dry-run` test.

**Pros:**
- Deterministic and zero-egress by construction: stdlib only, no network calls, no LLM calls.
- Answers three query shapes grep genuinely cannot: `lineage` (transitive), `orphans` (absence, needs the whole file universe first), and `validate` (existence-checking).
- Has a working precedent in this exact repo (`propagate_doctrine.py`) a reviewer can diff against line for line.
- Portable to the fleet as TEMPLATE-COPY doctrine with no per-repo substitution, because it parses conventions (Follows headers, link syntax) that are already doctrine, not this repo's package name.

**Cons:**
- Adds roughly 300 lines of code, a CLI, and 12 to 16 tests to maintain, in a repo whose own Anti-rules say not to add abstractions for hypothetical future requirements.
- Four of six query shapes (`neighbors`, `backlinks`, `lineage`, `path`) are answerable today, more slowly but adequately, by an agent that actually reads the headers and follows the links by hand. The tool buys speed and reliability there, not new capability.
- Adds one more thing all 15 downstream repos must decide whether to adopt and keep current, the same fleet-multiplication cost the lead's review raised against graphify, at roughly 1/200th the code size (300 lines against graphify's 59,000).
- Untested assumption: that agents call a CLI tool proactively without being told to. Nothing today routes an agent toward it.

**Risk level**: Low technical risk (stdlib, test-first, no egress). Medium adoption risk: without a companion skill or instruction, it ships and sits unused, the same gap that made the shift-left-testing discipline need a whole enforcement gradient (SKILL.md through a PostToolUse hook) before it reliably held.

### Approach B: Ship a skill, not a graph (bold alternative)

Write no code. Add `.claude/skills/traversing-the-knowledge-base/` (Level 0, directory form, matching `maintaining-project-context` and `maintaining-ubiquitous-language`). The skill does three things: names the graph structure that already exists in this corpus so an agent that has never opened `session-doc-format.md` still discovers the seven typed relations and `CONTEXT.md`'s Reading Order; gives grep and ripgrep one-liners for the four query shapes grep can do well at this size (neighbors: `grep -rn "\]($basename" docs/`; backlinks: `grep -rln "$basename" docs/`; a rough lineage walk: `grep -n "Follows" docs/sessions/*.md` chased by hand, one hop at a time; path: the same chase from both ends); and states plainly which two shapes grep cannot do reliably, `orphans` and `validate`, and defers them rather than faking a workaround.

This challenges what the lead's review, and the task that produced it, both assumed: that the problem is a missing tool. It is a 103-file, 1.0 MB corpus. Every agent already has Read, Grep, and Glob. The gap I found while researching this proposal was not "there is no way to answer these questions." It was "nothing tells an agent these headers exist and are meant to be followed before falling back to a keyword search." `CONTEXT.md` already hand-encodes a Reading Order. `session-doc-format.md` already hand-specifies seven relation types. Neither needs a traversal engine to matter; they need an agent to know they are there and use them first. This repo has reached for that fix once already: the shift-left-testing principle existed in `CLAUDE.md` for months before anyone wrote a hook. The first fix for "agents do not do X reliably" is usually to tell them to, clearly, with examples. Code is what comes next, only once that is shown not to be enough.

**Pros:**
- Ships this session. No new dependency, no new test surface, no egress risk beyond the baseline every session already has (doc content reaching the session model, which the lead's review names as "no new party").
- Trivially reversible: delete one directory.
- Matches this repo's own written Anti-rules directly ("do not add abstractions for hypothetical future requirements"; "do not add new agents until existing agents are demonstrably saturated," which generalizes cleanly to: do not add a graph tool until a skill is demonstrably insufficient).
- Answers the actual open question, tooling gap or behavior gap, before spending a build budget on the wrong one.

**Cons:**
- Does not solve `orphans` or `validate`. Those are the two shapes with a live, verified example in this exact session (the `docs/tasks.md` P3 drift). A skill cannot compute "what does nothing point to" from inside an agent's head; someone would have to enumerate the whole corpus by hand each time, which nobody does unprompted, which is plausibly how the drift went unnoticed for months.
- Weaker to verify than code. Its effect depends on an agent choosing to read and apply it: the probabilistic Layer 1 in the shift-left-testing enforcement gradient, with no deterministic layer behind it and no audit log if it fails quietly.
- The risk: if the skill does not change behavior, deferring the graph looks like avoidance dressed as minimalism.

**Risk level**: Low. The main risk is doing nothing useful and not finding out, which is why the recommendation below pairs this with an explicit, cheap trigger rather than leaving it open-ended.

### Approach C: Adopt or hybridize with graphify, rejected (the lead's Options A and C)

I reject both, for reasons narrower than but consistent with the lead's own findings.

**Adopting graphify, even pinned and constrained**: the lead's F2, F3, and F7 findings (ambient-API-key provider routing, a default-on query log shipped once and since reverted, CLAUDE.md and hook install depth) are real. I would reject graphify as tacsop doctrine even if all three were fixed today, on cost alone. This session's own timing probe put a full four-extractor parse of the entire 103-file corpus at 3.45 ms with nothing but the standard library. Installing a 59,000-line, actively changing, commercially backed tool to solve a problem that costs single-digit milliseconds and about 300 lines is not a close call under Simplicity First, independent of the privacy question. The privacy findings are reasons not to adopt it carelessly; the size mismatch is a reason not to adopt it at all.

**The hybrid framing (graphify stays available for downstream repos with real code-graph needs)**: reasonable in the abstract, but not a decision this proposal needs to make. No downstream repo has asked for multi-language code-graph traversal. Deciding this now decides a hypothetical for repos that are not in this session and have their own `CLAUDE.md` to write. If a downstream repo's own corpus genuinely needs tree-sitter-grade parsing later, that repo's own maintainer weighs graphify against that repo's own risk tolerance then. Recommend leaving graphify out of `docs/doctrine-updates.md` entirely, rather than writing an entry that formally pre-approves a tool nobody has asked for.

---

## Recommendation

Ship Approach B this cycle: the `traversing-the-knowledge-base` skill, zero new code. Specify Approach A in full, as done above, but do not build it yet.

Set one explicit trigger for building the `validate()` and `orphans()` slice of Approach A, and only that slice, not the full six-function surface: the next time an agent either misses a Follows, Documents, or References edge the skill's instructions should have surfaced, or a dangling reference like the `docs/tasks.md` P3 case is found by accident instead of by a systematic check. Build it test-first, per shift-left doctrine, at that point and not before.

This is a falsifiable bet, not a deferral for its own sake. Stated the way this repo's own `CONOP-FORMAT.md` now requires load-bearing assumptions to be stated: the assumption is that a skill closes the gap without code; the falsifier is either condition above; the blast radius if wrong is small, roughly 100 to 150 lines for the validate/orphans slice alone, not the full 300.

Reject graphify-adopt and the hybrid framing as doctrine. Neither belongs in `docs/doctrine-updates.md`.

**If this recommendation survives code-reviewer's challenge:**

- **Integration path.** Approach B touches only `.claude/skills/`, no `src/`, `tests/`, or `config/` changes, which under CLAUDE.md's Branching principle would normally qualify as lead-only doc work landing directly on `main`. Because debate on this question already started on `topic/kb-graph-traversal`, the clean close is to finish authoring the skill on this branch, merge via merge-commit at the audit gate, and delete the branch immediately after, per `using-topic-branches/SKILL.md`. If the validate/orphans trigger fires later, that slice is team-deployed code work (`scripts/`, `tests/`, possibly a `CLAUDE.md` quick-commands line) and should run through the `feature-development` team template (python-prototyper, test-runner, code-reviewer) on its own short-lived topic branch, test-first.
- **Doctrine artifact.** The skill passes `propagation-protocol.md`'s three-part test: cross-cutting, because every downstream repo has the same header conventions and the same under-exploitation problem; convention-bearing, because a skill is a convention; designed for adoption, because it is exactly the kind of thing a downstream maintainer would be expected to apply. A future `docs/doctrine-updates.md` entry would carry it as **TEMPLATE-COPY**, the same adoption mode as `maintaining-project-context` and `maintaining-ubiquitous-language`, through the same five-question Evaluation Gate every prior entry has passed. If the validate/orphans slice ships later, it would likely also be TEMPLATE-COPY: unlike the shift-left audit hook, `kb_graph.py` parses conventions rather than a repo-specific package path, so it needs no per-repo substitution.
- **ADR candidate.** "Build versus adopt for knowledge-base traversal" is a plausible future ADR (`docs/adr/000N-kb-graph-traversal-build-vs-adopt.md`) once a decision sticks, on the same triple filter ADR-0001 and ADR-0002 already passed: hard to reverse once 15 downstream repos have formed habits around a schema; surprising without context, since declining a 106,000-star tool needs the reasoning on record so a future maintainer does not reflexively reach for it; and a genuine trade-off between real alternatives, exactly what this document and the lead's review both debated. Write it at the audit gate, once decided, not before; `ADR-FORMAT.md`'s gate fires on a decision, not a proposal.
- **Escalation.** This stays below CONOP level for Approach B: one skill, one session, no open design decisions. If the validate/orphans trigger fires, that slice likely does warrant a CONOP before its first wave, since it touches three to four components (`scripts/`, `tests/`, `CLAUDE.md`, a doctrine entry) under `CONOP-FORMAT.md`'s promotion criteria. This document is deliberately not that CONOP.

---

## Open Questions

1. **Does the skill actually change agent behavior, or join the pile of skills that exist but go unread?** There is no way to know without running it and checking, the same wait this repo already accepted for shift-left-testing before it needed a hook. Suggest checking after 3 to 5 sessions that plausibly would have used it, any session touching `docs/sessions/`, `docs/tasks.md`, or a cross-doc dependency question.
2. **Where does the trigger for Approach A's slice get tracked so it is not only remembered by this document?** Recommend a `docs/tasks.md` P3 entry now: watch for a missed edge or a found dangling reference; if seen, build the validate/orphans slice specified in this proposal.
3. **Does `validate()`, when built, need to reach beyond markdown-to-markdown links?** The `docs/tasks.md` P3 case that motivates this proposal is a tasks-file-to-nonexistent-file edge, not a doc-to-doc edge. A `validate()` scoped only to `docs/*.md`-to-`docs/*.md` links would miss the exact case that justifies building it. This needs a decision before Approach A's slice is specified in implementation detail, not before this proposal ships.
4. **Does the wikilink extractor for `.claude/agent-memory/` get written proactively?** It shares the markdown-link code path and costs about three lines. I lean toward writing it even though it returns nothing today, but this is a call for whoever builds the slice, not for this proposal.
5. **Is `git ls-files '*.md'` the right corpus boundary for every downstream repo, not just tacsop?** Clean here. A downstream repo's `.claude/upstream-update.md` is real, load-bearing content (pending doctrine notifications) that is deliberately not gitignored anywhere this doctrine has shipped so far, and would be invisible to a `git ls-files`-only crawl if it were ever excluded from tracking. Worth checking before a future doctrine entry's Adoption-Mode Table is written, not before this proposal ships.

---

## Amendment (2026-08-14, incorporating the adversarial review)

`docs/reviews/20260813_kb_graph_adoption_review.md` sustained this proposal's recommendation and required spec corrections. The original text stands unedited; these corrections govern the deferred build.

1. **Extractor 3 widens from backtick-only to any path-shaped token.** The flagship `validate()` case (`docs/tasks.md` P3) writes its five paths as plain parenthesized prose with no backticks, which the backtick-only spec cannot catch. The corrected extractor matches path-shaped tokens (`(docs|src|tests|config|scripts|.claude)/...` with a file extension) regardless of quoting. Test slice 14's fixture must mirror the plain-prose form, not a backticked one.
2. **The neighbors recipe in Approach B was inbound-only.** Neighbors is both directions by its own definition in Approach A: outbound = read the doc's own links and path mentions; inbound = `grep -rln` on the basename. The shipped skill carries the corrected recipes.
3. **Extractor 5 (wikilinks) is unreachable under the proposal's own corpus rule**: `.claude/agent-memory/` is gitignored (`.gitignore:56`), so `git ls-files` never surfaces it. Resolution deferred to the build trigger: either name that directory an explicit extra corpus root or drop the extractor. Open Question 4 is superseded by this item.
4. **Corrections of record.** The 3.45 ms benchmark swept 117 files (tracked plus untracked `.md` present at measure time), not the 103 stated; "cold" and "20-run average" describe successive in-process runs, not cold-cache runs. The fleet figure is 19 known downstream repos (`docs/propagation-protocol.md` roster); 15 was one box's filesystem-discovery reach on 2026-08-03.
5. **Wave 0 shipped 2026-08-14** on `topic/kb-graph-traversal`: the skill (Approach B) at `.claude/skills/traversing-the-knowledge-base/SKILL.md` with the falsifiable five-session criterion the review required, and the living-docs reference-integrity check as `/pcc` check 5, which implements the corrected extractor-3 behavior over the orientation surfaces (measured baseline: 3 known-missing March paths; 2 runtime artifacts allowlisted). The parent plan is CONOP WHETSTONE (`docs/plans/conop_whetstone_recursive_doctrine_loop.md`).
