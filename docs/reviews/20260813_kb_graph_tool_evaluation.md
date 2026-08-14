# Review: graphify Adoption vs Build-Own for Agent KB Traversal

**Author**: session lead (Claude)
**Date**: 2026-08-13
**Type**: Tool evaluation / supply-chain review
**Branch**: `topic/kb-graph-traversal`
**Evidence basis**: shallow clone of `Graphify-Labs/graphify` at commit `7fe58b0` (v0.9.42), inspected read-only in the session scratchpad. No graphify code was executed or installed. File:line references cite that commit.

## Question

Should our agents traverse local knowledge bases (docs/, living docs, memory) by graph traversal instead of search? If yes, do we adopt graphify by cloning to `tools/`, or build a minimal traversal utility of our own? The user's stated concern is private data leaving the machine.

## What graphify is

Graphify ([Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)) turns a folder of code, docs, SQL, PDFs, images, and videos into a queryable knowledge graph. It parses code locally with tree-sitter (36+ languages), uses no embeddings and no vector store, tags every edge EXTRACTED or INFERRED, and ships a `/graphify` skill for Claude Code and 20+ other assistants. Outputs are `graph.html`, `GRAPH_REPORT.md`, and `graph.json`. It is a Y Combinator S26 company with roughly 106k GitHub stars, a hosted platform in beta at app.graphify.com, and a PyPI package named `graphifyy` at v0.9.42. The `graphify/` package is 58,998 lines of Python. Dual-licensed Apache-2.0 and MIT.

## Findings

### F1. Code parsing is local. Confirmed.
Tree-sitter grammars are direct dependencies (`pyproject.toml`); AST extraction makes no network calls. The README claim "Code is parsed locally with tree-sitter (no LLM, nothing leaves your machine)" holds for code.

### F2. Docs, PDFs, and images go to an LLM. Headless mode picks the provider from ambient API keys.
README.md:540 states docs, PDFs, and images are "sent to your AI assistant for semantic extraction." In a Claude Code session that means the session model (Anthropic), the same place our doc content already goes every session. The sharp edge is headless `graphify extract` (README.md:541): it auto-detects the backend from whichever API key exists in the environment, priority Gemini → Kimi → Claude → OpenAI → DeepSeek → Azure → Bedrock → Ollama. `graphify/llm.py:105-170` hardcodes endpoints for api.anthropic.com, api.moonshot.ai, generativelanguage.googleapis.com, api.openai.com, api.deepseek.com. A stray `GEMINI_API_KEY` or `MOONSHOT_API_KEY` in the environment silently routes our doc content to Google or to Moonshot servers in China. Our repos keep API keys in `.env` files; one exported key in a shell profile flips the destination.

### F3. The query log shipped default-on and undocumented. Now opt-in. README still says default-on.
CHANGELOG.md:375 (#1797) admits `querylog` wrote every query, corpus path, and optionally full responses to a default-on, unbounded, fail-silent plaintext file at `~/.cache/graphify-queries.log`, "outside any repo's .gitignore/retention, and undocumented, which contradicts graphify's on-device / no-telemetry posture." Current code (`graphify/querylog.py:15-31`) is off unless enabled. README.md:543 still documents the old default-on behavior. Two conclusions: the project has shipped a privacy regression before, and its docs drift from its code.

### F4. No telemetry SDKs. Confirmed.
No posthog, sentry, mixpanel, segment, or amplitude anywhere in the source. README.md:542: "No telemetry, no usage tracking, no analytics." Grep supports the claim.

### F5. Generated graph.html loads scripts from three CDNs.
`callflow_html.py:1708` (cdn.jsdelivr.net), `exporters/html.py:599` (unpkg.com), `tree_html.py:282` (d3js.org). Opening the generated artifact in a browser makes external requests. Not exfiltration, but a network dependency inside a "local" artifact and a supply-chain surface for the viewer page.

### F6. Remote ingest exists. The security module is defensive and mature.
`ingest.py:107,170` fetches from publish.twitter.com and export.arxiv.org (inbound enrichment, user-invoked). `security.py` is genuinely defensive: URL scheme allowlist, SSRF guards via ipaddress/socket checks, 50 MB fetch caps, graph.json memory-bomb caps. CVE-pinned dependency floors in `pyproject.toml` show they track their supply chain. Competent engineering, not a red flag.

### F7. Install writes into CLAUDE.md and installs read-gating hooks.
`graphify install` registers itself in CLAUDE.md / AGENTS.md / equivalent for each assistant (`install.py`, `always_on/claude-md.md`). `graphify claude install` adds PreToolUse hooks that intercept file reads to steer the agent toward graph queries; `--strict` blocks the first raw read per session until a `graphify query` runs (`install.py:689-690`). A third-party tool editing our doctrine files and gating our agents' file reads is an integration-depth decision, not a default to accept.

### F8. The PyPI name is `graphifyy`. `pip install graphify` installs a different package.
The command is `graphify` but the package is `graphifyy` (`pyproject.toml`). Anyone on the team who types the obvious `pip install graphify` gets an unrelated package with an unknown owner. Name-confusion is a standing supply-chain hazard for any written instruction we'd propagate.

### F9. Commercial gravity.
`install.py:682-683` closes every install with a pointer to the hosted platform ("Early access to the graphify platform is open free before the public v1 launch: https://app.graphify.com"). Open core today; the incentive points toward the hosted product. A doctrine bet on the OSS tool should price in that trajectory.

## Exposure analysis for our use case

The user's concern ("release our private data to someone else") splits into three distinct exposures:

1. **In-session use** (`/graphify` skill inside Claude Code): doc content reaches the session model only. That is identical to our existing exposure; every session already reads these files into Anthropic's API. No new party.
2. **Headless use** (`graphify extract` in scripts or CI): F2's ambient-key auto-detect can add a new party (Google, Moonshot, OpenAI, DeepSeek) silently. This is the real leak vector, and it is a foot-gun, not malice.
3. **At-rest artifacts**: graph.json and GRAPH_REPORT.md concentrate the corpus into single files; the F3 query log history shows local-leak regressions happen; F5's CDN loads make the HTML viewer phone out.

No evidence of intentional exfiltration. The risk profile is: honest tool, large surface, fast-moving pre-1.0, with defaults that assume you are not privacy-sensitive.

## Fit to our corpus

Our knowledge base is small and already link-structured: 103 markdown files repo-wide (49 in docs/), 160 relative markdown links, 16 session docs carrying explicit **Follows** lineage headers plus **Documents**/**References** headers, tasks.md referencing plans and reviews, and a memory system specified around `[[wikilink]]` syntax. We control the schema. Deterministic link extraction over this corpus is a few hundred lines of stdlib Python, not 59k lines. Graphify's differentiators (tree-sitter over 36 languages, PDF/image/video ingestion, community detection) target problems we do not have in this repo.

Two repo-specific arguments against cloning to `tools/`: this repo is a template propagated to 15 downstream repos, so vendored third-party code multiplies across the fleet; and a 21 MB, 59k-line dependency inverts our Simplicity First pillar for a corpus of 103 files.

## Options for the panel

- **A. Adopt graphify, pinned and constrained**: `uv tool install graphifyy==0.9.42` (never vendored into the repo), docs-only corpus, in-session or Ollama backends only, no `graphify claude install` hooks, `GRAPHIFY_QUERY_LOG_DISABLE=1` as belt-and-suspenders, upgrade only by diff review.
- **B. Build a minimal deterministic kb-graph utility**: stdlib parser for markdown links, Follows/Documents/References headers, and wikilinks; adjacency written to a committed JSON or YAML index; traversal queries (neighbors, lineage chain, backlinks, orphans, path) as a utility module and thin CLI; test-first; zero egress by construction; propagatable to the fleet as doctrine.
- **C. Hybrid**: B becomes the fleet doctrine for knowledge bases; graphify stays an individually chosen, off-repo tool for code-graph use cases in downstream repos that need it, revisited at its 1.0.

## Lead assessment

For this use case I recommend B, with C's framing for downstream repos. The privacy concern is real but specific: the danger is not graphify phoning home (it does not), it is silent provider selection by ambient API key, plus integration depth (CLAUDE.md edits, read-gating hooks) we do not need for markdown traversal. Cloning 59k lines into a template propagated to 15 repos to traverse 103 files fails Simplicity First on its face. A deterministic link-graph utility answers the actual need (agents following lineage and reference edges instead of grepping), keeps every byte on the machine, and is itself a candidate doctrine artifact. Graphify remains the right answer to a different question (multi-language code graphs), and adopting its two best ideas costs nothing: explicit EXTRACTED vs INFERRED edge provenance, and graph artifacts an agent can query in milliseconds.

Panel: challenge this. The proposer should feel free to reject all three options.

---

## Corrections after adversarial review (2026-08-13, same session)

`docs/reviews/20260813_kb_graph_adoption_review.md` re-verified all nine findings at the pinned commit and corrected this document in three places. The text above stands unedited; these corrections govern.

1. **"15 downstream repos" undercounts the fleet.** The known roster is 19 (`docs/propagation-protocol.md`, Roster section); 15 is what filesystem discovery reached from this box on 2026-08-03. Lead re-verified against the roster list. The fleet-multiplier argument gets stronger, but the number above is wrong.
2. **F7 named a command that does not exist, and Option A's mitigations are policy, not enforcement.** The inspected CLI installs read-gating via `graphify install --strict` (project hook), and there is a separate git-hook surface this document omitted; `graphify claude install` came from a secondary web source and is not in the CLI at `7fe58b0`. More important: nothing technical stops a future upgrade or an ambient API key from re-widening the surface. If A were chosen, its mitigations would need an enforcement layer, not a checklist.
3. **Exposure analysis addendum.** In-session use adds no new party, but it changes the shape of the exposure: a normal session reads files as needed; a graph build batches the full corpus systematically into single artifacts. Concentration, not destination, is the delta.
