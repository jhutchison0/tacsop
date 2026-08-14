# Review: KB Graph Traversal, Adoption Decision (graphify vs build vs skill)

**Author**: code-reviewer
**Date**: 2026-08-13
**Type**: Decision review (tool evaluation + proposal challenge)
**Reviews**: [20260813_kb_graph_tool_evaluation.md](20260813_kb_graph_tool_evaluation.md) (session lead), [20260813_kb_graph_traversal_proposal.md](../plans/20260813_kb_graph_traversal_proposal.md) (proposer)
**Verdict (short form)**: Gate through skill-first (proposal's Approach B), conditional on the two Critical fixes below. Reject graphify adoption; concur with both documents there, and I verified their evidence.

I re-verified the lead's graphify findings against the read-only clone at commit `7fe58b0` (no code executed, nothing installed) and the proposer's factual claims against this working tree. The lead's evaluation is accurate to a degree that is rare: F1 through F9 all hold at or within one line of the cited locations, and the 58,998-line / 21 MB figures are exact. The proposal's direction is sound and matches this repo's own escalation pattern (skill, then evidence, then mechanism), but its two load-bearing exhibits are broken as written: the trigger is unfalsifiable, and the flagship `validate()` example cannot be caught by the extractor the proposal specifies. Neither document uses the correct fleet size.

## Critical (must fix before the user decides)

### C1. The proposal's trigger and wait-and-see have no detection mechanism. As written, the bet cannot lose.

**Location**: proposal, Recommendation (lines 131-133) and Open Question 1 (line 148).

**Issue**: The falsifier is "the next time an agent misses a Follows/Documents/References edge the skill should have surfaced, or a dangling reference is found by accident." Both conditions require someone to *notice* a miss, and the party positioned to notice is the same agent that missed. A missed edge produces no artifact. Open Question 1 proposes "checking after 3 to 5 sessions" but names no metric to check and admits "there is no way to know without running it and checking." Checking *what* is never stated. Absence of noticed misses is survivorship, not evidence.

**Why it matters**: This repo already litigated exactly this. `ENFORCEMENT.md` (shift-left-testing): "A skill describes; it does not enforce. Whether any agent invokes the skill on any given turn is decided by the model: probabilistic, not deterministic." The 20260519 enforcement MAUT was convened *because* skill-only adherence was known-unreliable, and its escalation triggers are quantified ("more than 20 `MISSING_TEST` events in a single month") and fed by a deterministic evidence stream. The proposal's own Con list names this gap ("no deterministic layer behind it and no audit log if it fails quietly") and then the Recommendation ships without closing it. A bet whose loss condition produces no signal is a deferral, which is the exact charge the proposal tries to preempt ("avoidance dressed as minimalism").

**Suggested fix** (stays zero-code, consistent with ENFORCEMENT.md's "add more evidence collection, not more refusal"):

1. Name the observable: session docs. The typed headers and the prose already record what a session consulted. Add one line to the skill and to `/session-end`: sessions that touched `docs/sessions/`, `docs/tasks.md`, or a cross-doc dependency question record whether navigation used typed headers/links, and which query shape.
2. State the criterion with numbers: "After 5 qualifying sessions: if 0 or 1 of 5 show header-driven navigation, the skill failed; escalate per the ENFORCEMENT.md gradient (evidence layer first, not the utility first)."
3. Make the dangling-reference falsifier deterministic and cheap: a two-line grep for unresolvable `.md` mentions in `docs/tasks.md` and `docs/doctrine-updates.md`, run at `/pcc` or at review time. That is `validate()` by hand at a cost of seconds, and it converts "found by accident" into "found on schedule."

### C2. The flagship `validate()` example is not catchable by the proposed extractor, and its framing misstates what happened.

**Location**: proposal, Problem finding 2 (line 33), extractor 3 (line 49), test 14 (line 81), Open Question 3 (line 150).

**Issue**, two parts:

1. **Spec misses the example.** Extractor 3 is specified as "bare **backtick** path mentions." The `docs/tasks.md` P3 line, verified at the byte level this review, contains **no backticks**: the five paths sit in plain parenthesized prose (`... (docs/decision_audit_20260326.md, docs/plans/decision_science_gaps.md, ...)`). Under the proposal's own spec, `validate()` extracts nothing from that line and flags nothing. Test 14's "fixture that mirrors it" cannot mirror it without adding backticks the real file does not have, at which point it tests a different case.
2. **"Without anyone noticing" is false.** The task line itself is the notice: it says "the five **untracked** March decision-science docs" and closes "Untracked since March." Someone noticed, filed a task, and characterized the state. What the proposer genuinely found, and it is worth keeping, is narrower: the files are absent from *this working tree entirely*, so the P3 task's premise (files present but untracked) does not hold on this machine and the task is unactionable here. I confirmed all five are absent (`ls` on the three named paths; glob on `docs/reviews/2026-03-26*`).

**Why it matters**: This example is the proposal's entire case for the deferred slice. It is the trigger's archetype, the worked example for `validate()`, and regression test 14. If the spec cannot catch the motivating case and the case is not the "unnoticed drift" it is sold as, the deferred build is mis-specified and its urgency is overstated in the same paragraph that says "What is certain is that a 200-line hand-maintained task file has been carrying three dangling file references without anyone noticing."

**Suggested fix**: Extend extractor 3 (or a fourth pattern) to unquoted path-shaped tokens (`[A-Za-z0-9_./-]+\.md` outside link syntax), with the existing resolve-or-finding rule. Reframe finding 2: the new information is "the P3 task is unactionable on this clone because its subject files are absent," and the value of `validate()` is *systematic* detection on every machine rather than accidental detection on one. Rewrite for line 33: "The task line records the gap; what nothing records is that on this clone the five files are absent entirely, so the task cannot be acted on here. A `validate()` run on any machine would surface which clones can act on it." Fold Open Question 3 into this fix; the real scope problem is extraction syntax, not source-file scope (tasks.md is already in the corpus).

## Warnings (should fix)

### W1. Both documents use "15 downstream repos." The roster says 19.

**Location**: lead, Fit to our corpus and Lead assessment; proposal, lines 35, 93; source of truth at `docs/propagation-protocol.md:171`.

**Issue**: The roster lists 19 repos (paperboy through veil-engine, registered 2026-07-26). The "15" traces to `config/project.yaml:59`, a summary of one propagation run ("propagated to 15 repos"), which counts that cycle's reach, not the fleet. The proposal cites `docs/propagation-protocol.md` for the 15, the very file that lists 19.

**Why it matters**: The fleet multiplier is load-bearing in both documents. Both use it against graphify; the proposer uses it to set "the bar for adding new machinery." The correct number strengthens their shared direction by ~27 percent, but a decision document citing a file for a number that file contradicts undercuts every other count it offers. Fix the number in both, and note elephant-graveyard's undecided consumer status (tasks.md P3) if precision matters.

### W2. "Trivially reversible: delete one directory" is only true before propagation.

**Location**: proposal, Approach B Pros (line 106) and Doctrine artifact (line 140).

**Issue**: The same document that prices Approach A's fleet-multiplication cost claims the skill is reversible by deleting a directory. After TEMPLATE-COPY adoption, reversal is a doctrine retraction across up to 19 independently maintained repos. `propagation-protocol.md`'s own Evaluation Gate question 5 asks for the rollback path; the proposal answers it for the utility and not for the skill.

**Why it matters**: The asymmetry flatters the recommended option. The honest statement is: reversible this cycle, doctrine-sticky after the first propagation. That argues for holding the skill out of a doctrine entry until the C1 evidence check passes, which the proposal already half-implies but never states.

**Suggested fix**: One sentence in the Pros and one in the Doctrine artifact paragraph: propagate only after the 5-session criterion passes; until then the skill is a tacsop-local experiment.

### W3. The skill's `neighbors` recipe is inbound-only. It contradicts the proposal's own definition.

**Location**: proposal, Approach B (line 100) vs. Approach A's `neighbors()` definition (line 55, "one-hop edges, both directions").

**Issue**: The recipe `grep -rn "\]($basename" docs/` finds files that link *to* the target: inbound. Outbound edges require grepping the target file itself for link syntax. As written, the neighbors and backlinks one-liners are both inbound, nearly the same command.

**Why it matters**: The skill is the deliverable of the recommended approach, and this recipe is one third of its content. A directionally wrong recipe propagated to 19 repos multiplies a wrong recipe; W2's stickiness applies to content bugs too.

**Suggested fix**: neighbors = union of outbound (`grep -oEn "\]\([^)]*\.md[^)]*\)" "$file"` plus the file's own `**Label**:` header lines) and inbound (the existing command). Keep backlinks as-is.

### W4. The lead's Option A mitigation list is policy-only, names a command that does not exist, and omits the second hook surface.

**Location**: lead, Options for the panel (Option A) and F7.

**Issue**, three parts:

1. **Unenforceable by construction.** "Docs-only corpus, in-session or Ollama backends only, no hooks, `GRAPHIFY_QUERY_LOG_DISABLE=1`" are all conventions. Nothing technical prevents one bare `graphify extract` with a stray `GEMINI_API_KEY` exported in a shell, which is F2's exact scenario. (The env var itself is real; `querylog.py:22-24` honors DISABLE as a back-compat override on top of the now-off default. Belt-and-suspenders, correctly labeled.)
2. **Command name.** "No `graphify claude install` hooks" names a form the CLI does not have. The install usage is `graphify install [--project] [--strict] [--platform P|P]` (`install.py`, `_print_install_usage`). A written constraint that names a nonexistent command is harder to follow and easier to argue around.
3. **Omitted surface.** `graphify hook install` (separate from assistant integration; `hooks.py`) installs git post-commit and post-checkout hooks that trigger detached graph rebuilds. Opt-in, and rebuilds appear AST-only per graphify's own injected CLAUDE.md text ("no API cost"), but the hooks have a bug history (#1809: rogue `graph.json` written into linked worktrees, races with CI `git clean`). A constraint list claiming containment should name this hook class alongside the assistant hooks.

**Why it matters**: Option A stays on the table for the panel. If it is chosen, these mitigations are the entire containment story, and the panel should know they are review-enforced policy, not controls.

**Suggested fix**: Add to Option A: "All constraints are policy, enforceable only by review; `graphify hook install` (git hooks) is excluded along with assistant integration; correct incantation for the excluded install is `graphify install --platform claude`."

### W5. The proposal's agent-memory claims: one now false, one design dead-end.

**Location**: proposal, extractor 5 (line 51) and Open Question 4 (line 151); `.gitignore:56`.

**Issue**:

1. "`.claude/agent-memory/` ... holds zero files right now, including this session's own `proposer/` directory" is false as of this review: three files exist (`proposer/MEMORY.md`, `agent_memory_scope_gitignored.md`, `kb_graph_traversal_proposal.md`), written by the proposer later in the same session. True at drafting, stale before its first reader. The gitignore cite (line 56) is correct.
2. The deeper defect: extractor 5's corpus can never contain those files under the proposal's own corpus rule. Storage design mandates `git ls-files '*.md'`; agent-memory is gitignored, so it is never in `git ls-files`. The wikilink extractor as specified is unreachable, permanently, not just "no corpus to traverse today."

**Why it matters**: Point 1 is a small staleness irony that supports the proposal's own argument against committed graphs; fix the wording ("held zero files at session start"). Point 2 means Open Question 4 ("write the extractor proactively?") is moot until the corpus rule or the gitignore changes. There is also a genuine config contradiction here worth its own task: the agent harness text describes memory as "shared with your team via version control" while `.gitignore:56` makes it machine-local. The proposer's own memory file documents this; nothing user-facing does.

**Suggested fix**: Correct the sentence; in extractor 5, state the dependency ("unreachable under `git ls-files` while agent-memory is gitignored; requires an explicit second corpus root if ever built"); file a tasks.md entry to resolve the memory-scope contradiction one way or the other.

### W6. The 3.45 ms benchmark is self-contradictory, measured on the wrong corpus, and unreproducible.

**Location**: proposal, corpus table (line 28) and storage paragraph (line 62); also used at line 121 against graphify.

**Issue**: "Cold, no cache (20-run average)" contradicts itself: runs 2 through 20 hit a warm OS page cache; a 20-run average is a warm average. The probe is described as "throwaway" and "used a naive `rglob('*.md')`" that "picked up 13 files from `.venv/` and one from `.pytest_cache/`", so it measured 117 files, not "all 103 files" as both citations state, unless a corrected run happened and went unrecorded; the document does not say. The probe script is not preserved, so no one can rerun it.

**Why it matters**: This number carries the argument twice: against a committed `graph.json` (no cache needed at 3.45 ms) and against graphify ("a problem that costs single-digit milliseconds"). The order of magnitude is not in doubt for 1 MB of text, so the conclusions survive, but a repo whose prose doctrine is "hedge with numbers or not at all" and whose review protocol models "(measured, n=5)" should not rest a decision on a number whose method contradicts itself and whose instrument was discarded.

**Suggested fix**: Restate as a bound with the method inline: "under 10 ms per sweep (stdlib `re`, four extractors, 117 files including 14 later excluded, n=20, warm cache, this machine)", or preserve the probe (a pytest marked `slow`, or a `scripts/` snippet in the eventual slice) and cite it.

### W7. Load-bearing counts differ between the two documents and neither records its method.

**Location**: lead, Fit to our corpus ("160 relative markdown links", "16 session docs"); proposal, corpus table ("157 proper links", "816 unique" backtick mentions, "17 of 18 session docs").

**Issue**: The proposal claims "all counts from live commands against this branch, not estimates" but records no commands. My re-counts today: 164 proper `.md` links (whole repo minus `.venv`/`.git`/`.pytest_cache`, including this session's new files); backtick-quoted `.md` mentions 1,439 raw / 302 unique with an end-anchored regex, and I cannot reconcile either figure with "816 unique" without knowing the regex. The session-doc counts, for the record, both check out on their own metrics: 16 of 18 carry `**Follows**` (lead) and 17 of 18 carry at least one typed header (proposer; only `20260312_template_review_and_agent_rewrite.md` has none). The link counts (157 vs 160 vs 164) are all plausible snapshots of a moving corpus under unstated regexes.

**Why it matters**: The "five to one" ratio (816 vs 157) is the stated reason extractor 3 exists and is ranked where it is. The direction (bare mentions outnumber links) survives any of my counts; the specific ratio does not. Two same-day documents on the same branch disagreeing on the same metric, with no method stated in either, is exactly the reproducibility failure W6 describes, fleet-wide.

**Suggested fix**: For each count that carries an argument, put the command in the document (one backticked line each). Where a count will drift, say "at commit X."

## Suggestions (consider)

### S1. Lead: cited line numbers for README.md and CHANGELOG.md run one line high.

"Sent to your AI assistant" is README.md:539 (cited 540); auto-detect priority 540 (cited 541); no-telemetry 541 (cited 542); query logging 542 (cited 543); the #1797 CHANGELOG entry starts at 374 (cited 375). Systematic +1, content all present, conclusions unaffected. Fix the cites or cite by section heading, which survives upstream edits better.

### S2. Lead F7: state strict mode's actual mechanics.

`cli.py:582-640`: strict mode denies only the *first* raw read of indexed, in-project, fresh code per session, then downgrades to a soft nudge; search and glob are nudge-only; every path fails open. "Blocks the first raw read per session until a `graphify query` runs" (graphify's own usage text) reads as persistent gating. The integration-depth conclusion stands either way; the review's value is precision. Worth adding: once installed, the hook runs graphify code on every Read/Grep/Bash tool call in the session, which is the real integration-depth fact.

### S3. Lead F5 sharpening: two of three CDN script tags lack SRI.

Only the vis-network tag carries an `integrity=` hash (`exporters/html.py:600`). The mermaid (jsdelivr) and d3 (d3js.org) tags are unpinned, so a compromised CDN can inject script into the viewer page that displays the corpus. One sentence upgrade to F5.

### S4. Lead exposure analysis: point 1 is honest on the party question; add the volume nuance.

"Identical to our existing exposure ... no new party" is correct and fairly stated for in-session use. The difference worth one sentence: sessions read files as needed; a graphify extraction systematically batches the entire corpus through the model, and re-extractions repeat it. Same party, larger and scheduled payload.

### S5. Lead: credit graphify's secret-detection stage; note the unexamined MCP surface.

`detect.py` excludes `.env`/`.envrc` files from the corpus (with committed-template exceptions, #2184), a defensive layer the evaluation never mentions, and it supports the review's own "honest tool" reading. Conversely `graphify-mcp` (a second entry point, `serve.py`; MCP `query_graph` appears in the query-log list) goes unexamined; if Option A is ever revisited, the MCP server needs its own look.

### S6. Proposal: `orphans()` references a config key that does not exist.

"Anything named as an entry point in `config/project.yaml`" (line 58): project.yaml has no entry-point or roots key today. The Config-Driven pillar supports putting one there; the proposal should say the key must be added, so the deferred slice does not inherit a silent dependency.

### S7. Prose (per REVIEWING.md; both docs are 0 for em dashes, rule 8 clean).

- [Minor] Rule 1: the lead's recommendation first appears in the final section. (evaluation, Lead assessment) Rewrite: add one line to the header block: "**Recommendation**: build minimal (Option B); graphify remains right for a different problem."
- [Major, folded into C2] Rule 6: "What is certain is that a 200-line hand-maintained task file has been carrying three dangling file references without anyone noticing" (proposal, line 33) asserts certainty about the part that is wrong. Rewrite given in C2.
- [Minor] Rule 3: proposal line 100 packs three grep recipes with nested parentheticals into one sentence. When the skill is authored, one recipe per line.

## What must change before the user decides

**In the proposal**: C1 (measurable criterion and evidence line, numbers stated), C2 (extractor spec covers unquoted paths; P3 example reframed), W1 (19, not 15), W2 (reversibility scoped to pre-propagation; no doctrine entry before the criterion passes), W3 (fix neighbors recipe), W5.1 (stale sentence), W6 (benchmark restated or probe preserved).

**In the lead's evaluation**: W1 (19, not 15), W4 (mitigations labeled policy-only; git-hook class named; command name corrected). S1 through S5 at the lead's discretion; none change the conclusion.

## Verdict

**Gate through skill-first (proposal's Approach B), conditional on C1 and C2.** Do not adopt graphify for this corpus: the lead's findings held up under adversarial re-verification, and the size mismatch argument (59k lines for a 1 MB link-structured corpus) is decisive independent of the privacy findings, which are themselves real (F2's ambient-key routing is confirmed in code, priority order and endpoints exact). Do not build the utility now: the strongest case for immediate code, the P3 "unnoticed drift" exhibit, is weaker than presented (the drift was noticed and tasked; only its per-machine unactionability is new) and is currently uncatchable by the proposed spec, so building today would build the wrong extractor. The skill is the right first move for the right reason, this repo's own documented pattern: skill, then evidence, then mechanism. But the repo's pattern also says the evidence layer is not optional, and the proposal ships without one. Add the measurable check, fix the spec and the recipe, correct the fleet count in both documents, and the skill-first bet becomes what it claims to be: falsifiable.
