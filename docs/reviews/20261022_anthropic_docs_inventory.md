# Anthropic guidance inventory and update cadence

**Author**: claude-code-guide agent, directed by the lead. **Date**: 2026-10-22.

Measured 2026-10-22 (UTC). All checks were read-only. Raw fetches were kept in the session scratchpad and are not committed; the commands below reproduce them.

## 1. Inventory

### Claude Code docs (code.claude.com, all 200, Markdown via `.md`)

| Page | Title | Covers | Type |
|---|---|---|---|
| `https://code.claude.com/docs/en/best-practices.md` | Best practices for Claude Code | Coding practice with Claude Code | Docs |
| `https://code.claude.com/docs/en/memory.md` | How Claude remembers your project | CLAUDE.md files and auto memory | Docs |
| `https://code.claude.com/docs/en/hooks-guide.md` | Automate actions with hooks | Hook recipes and patterns | Docs |
| `https://code.claude.com/docs/en/hooks.md` | Hooks reference | Hook events and schema | Docs |
| `https://code.claude.com/docs/en/sub-agents.md` | Create custom subagents | Subagent definitions | Docs |
| `https://code.claude.com/docs/en/skills.md` | Extend Claude with skills | Skill authoring | Docs |
| `https://code.claude.com/docs/en/settings.md` | Settings files and precedence | settings.json scopes | Docs |
| `https://code.claude.com/docs/en/changelog.md` | Claude Code changelog | Release notes, one section per version | Docs |
| `https://code.claude.com/docs/en/common-workflows.md` | Common workflows | Task recipes | Docs |
| `https://code.claude.com/docs/en/costs.md` | Manage costs effectively | Token and cost control | Docs |

The docs index at `https://code.claude.com/docs/llms.txt` (200, text/plain, 63682 bytes) lists these pages with one-line descriptions.

### Anthropic engineering posts (anthropic.com)

| Requested URL | Result | Current location |
|---|---|---|
| `/engineering/claude-code-best-practices` | 308 redirect | `https://code.claude.com/docs/en/best-practices` (folded into the docs) |
| `/engineering/writing-tools-for-agents` | 308 redirect | `/research/writing-tools-for-agents` |
| `/engineering/building-effective-agents` | 200 after redirect | `/research/building-effective-agents` |
| `/engineering/effective-context-engineering-for-ai-agents` | 200 after redirect | `/research/effective-context-engineering-for-ai-agents` |
| `/engineering/equipping-agents-for-the-real-world-with-agent-skills` | 200 after redirect | `/research/equipping-agents-for-the-real-world-with-agent-skills` |
| `/engineering/effective-harnesses-for-long-running-agents` | 200 after redirect | `/research/effective-harnesses-for-long-running-agents` |
| `/research/harness-design-long-running-apps` | 200, not a redirect | Found in the sitemap; content not fetched |

The `/engineering/` path now redirects to `/research/`. The `/engineering` index itself returns 200.

Other sitemap entries that fit the topic, listed but not fetched: `/research/long-running-claude`, `/research/claude-code-auto-mode`, `/research/claude-code-sandboxing`, `/research/claude-code-expertise`, `/research/demystifying-evals-for-ai-agents`, `/research/managed-agents`, `/research/multi-agent-research-system`.

### Platform prompting guidance (platform.claude.com)

| URL | Result |
|---|---|
| `/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices` | 308 to the new path |
| `/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md` | 200, 74566 bytes, title "Prompting best practices" |

The page moved. The old `claude-4-best-practices` path redirects to `claude-prompting-best-practices`. `https://platform.claude.com/llms.txt` returns 200, 89717 bytes.

## 2. Cadence

### Claude Code releases

Command: `curl -s https://api.github.com/repos/anthropics/claude-code/releases?per_page=100`

| Month (2026) | Releases |
|---|---|
| June (from the 26th) | 3 |
| July | 22 |
| August | 27 |
| September | 27 |
| October (through the 22nd) | 21 |

The 100 most recent releases span 2026-06-26 to 2026-10-22, about 0.85 releases per day. The API page cap was reached, so older releases were not counted.

The CHANGELOG has no per-version dates. `https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md` (200, 1081887 bytes, ETag present) holds 429 version headings. Only 8 date strings appear in the file, so the changelog cannot be counted per month.

### Table of measured cadence

| Surface | Command | Result |
|---|---|---|
| GitHub releases Atom | `curl -s https://github.com/anthropics/claude-code/releases.atom` | 200, 10 entries, newest 2026-10-22T22:18:57Z |
| Wayback, best-practices | `curl -s "https://web.archive.org/cdx/search/cdx?url=https://code.claude.com/docs/en/best-practices&output=json&fl=timestamp,digest&collapse=digest"` | 143 digest-change rows (137 unique digests), 2026-01-22 to 2026-10-20 |
| Wayback, memory | Same CDX query for `https://code.claude.com/docs/en/memory` | 211 digest-change rows, 2025-11-06 to 2026-10-21 |
| Wayback, engineering best-practices | Same CDX query for `https://www.anthropic.com/engineering/claude-code-best-practices` | 205 digest-change rows (199 unique digests), 2025-04-20 to 2026-04-07 |
| Sitemap, code.claude.com | `curl -s https://code.claude.com/sitemap.xml` | 200, 2713 URLs, each with `lastmod` |
| Wayback, code.claude.com sitemap | CDX query for `https://code.claude.com/sitemap.xml` | No captures |

The Wayback rows overcount. The CDX query collapses only adjacent duplicates, so each row marks a change in the digest sequence. A digest hashes the raw HTML, which changes with build tokens and layout, so each count is an upper bound on real content revisions. The engineering post's last capture predates its redirect, so its count stops in April.

Sitemap `lastmod` values are per page. The best-practices page showed `2026-10-20T02:14:20Z` and the memory page `2026-10-23T00:36:20Z` in the same fetch. The anthropic.com sitemap, however, stamps many pages with one shared time, such as a run of entries at `2026-10-18T21:2x`. That makes its `lastmod` a weak change signal.

## 3. Machine-readable signals

| Signal | Probe | Result | Usable? |
|---|---|---|---|
| anthropic.com news RSS | `curl -sI https://www.anthropic.com/news/rss.xml` | 404 | No |
| anthropic.com engineering RSS | `/engineering/rss.xml` | 404 | No |
| anthropic.com generic feed | `/feed.xml` | 404 | No |
| GitHub releases feed | `releases.atom` | 200, 10 entries | Yes |
| llms.txt, Claude Code docs | `https://code.claude.com/docs/llms.txt` | 200, 63682 bytes | Yes, for page discovery |
| llms.txt, platform | `https://platform.claude.com/llms.txt` | 200, 89717 bytes | Yes, for page discovery |
| Sitemap lastmod, code.claude.com | `sitemap.xml` | 2713 entries with `lastmod` | Yes, per page |
| Sitemap lastmod, anthropic.com | `https://www.anthropic.com/sitemap.xml` | 200, bulk stamps | Weak |
| Last-Modified on docs `.md` | `curl -sI https://code.claude.com/docs/en/memory.md` | `last-modified` equals request time, no ETag | No |
| Last-Modified on platform `.md` | `curl -sI` on the platform page | No `last-modified`, `cache-control: private, no-store` | No |
| Git source for docs | `https://github.com/anthropics/claude-code-docs`, `anthropics/docs`, `anthropics/claude-docs` | All 404 | No public source found |

A daily hash-and-diff of the `.md` pages would detect a content change on each known page, at daily resolution. It is not enough alone, for two reasons. It cannot find new pages, so the watcher must also hash `llms.txt`. It also says nothing about anthropic.com posts, which have no feed; those need the sitemap or a page hash.

The `claude-code` repository itself exists (api returns 200). It is the public source for the release notes.

## 4. Built-in alternatives

| Surface | Evidence | Coverage |
|---|---|---|
| `/release-notes` command | The changelog states that `/release-notes` is "now an interactive version picker." | Release notes only |
| Docs mentions of `/release-notes` | Grep of best-practices, memory, hooks, settings and common-workflows `.md`: 0 hits | None |
| claude-code-guide agent | Listed in the agent roster with WebFetch and WebSearch tools. Its definition is not on disk, so whether it fetches live docs is UNVERIFIED. | UNVERIFIED |

Claude Code already shows release notes in the CLI. A watcher would be redundant for release-level news. It would still be needed for doc-page content changes, because the CLI does not report those.

## Blockers and gaps

- The claude-code-guide live-fetch behavior is UNVERIFIED, because its definition was not found on disk.
- The release count covers only the 100 most recent releases.
- Wayback counts are upper bounds on content revisions.
- The engineering post and platform page are checked by redirect, not by reading full content.

## 5. Per-page lastmod and monthly revision bounds

Ages are calendar days from 2026-10-22. A negative age means the sitemap stamps the page 2026-10-23 UTC, one day after the stated date.

Command for the docs pages: `curl -s https://code.claude.com/sitemap.xml`, then read each page's `<lastmod>` by its `<loc>`.

| Page | lastmod (UTC) | Age (days) |
|---|---|---|
| best-practices | 2026-10-20T02:14:20Z | 2 |
| memory | 2026-10-23T00:36:20Z | -1 |
| hooks-guide | 2026-10-22T00:14:50Z | 0 |
| hooks | 2026-10-23T00:36:20Z | -1 |
| sub-agents | 2026-10-23T00:24:00Z | -1 |
| skills | 2026-10-23T00:36:20Z | -1 |
| settings | 2026-10-22T00:33:55Z | 0 |
| changelog | 2026-10-22T22:30:05Z | 0 |
| common-workflows | 2026-10-22T00:01:44Z | 0 |
| costs | 2026-10-22T00:08:22Z | 0 |
| claude-prompting-best-practices (platform) | UNVERIFIED | UNVERIFIED |

The platform sitemap at `https://platform.claude.com/sitemap.xml` (200, 399130 bytes) lists the page, but it carries no `<lastmod>` fields at all. Its age cannot be read from the sitemap.

Command for the monthly counts: the saved CDX responses from `curl -s "https://web.archive.org/cdx/search/cdx?url=<page>&output=json&fl=timestamp,digest&collapse=digest"`, counting rows by the first six digits of the timestamp.

| Month (2026) | best-practices digest changes | memory digest changes |
|---|---|---|
| August | 11 | 27 |
| September | 18 | 27 |
| October (through the 21st) | 25 | 34 |

Each count is an upper bound on revisions. A digest changes whenever the raw HTML changes, including build noise. The October count is partial, and the best-practices capture stops on the 20th.

## 6. Content-level diffs between monthly captures

Method. For each target date, the CDX API returned the capture closest to it: `curl -s "https://web.archive.org/cdx/search/cdx?url=<page>&output=json&fl=timestamp,digest&closest=<YYYYMMDD>000000&sort=closest&limit=1"`. Each raw capture came from `https://web.archive.org/web/<timestamp>id_/<page>`, fetched with `curl --compressed`, and gunzipped where needed. The script `/tmp/claude-1000/-home-jhutchison-projects-github-tacsop/f5bbe5d6-fdcc-42e0-a480-477098d84dba/scratchpad/probe/textdiff.py` strips tags, drops script, style and navigation blocks, and diffs visible text blocks with difflib. The script lives in the scratchpad probe folder, not in a repo. Line counts are text blocks, not source lines.

Capture timestamps actually obtained (UTC):

| Target | best-practices capture | memory capture |
|---|---|---|
| 2026-08-01 | 2026-07-31 18:14 (1 day before) | 2026-08-02 04:51 (1 day after) |
| 2026-09-01 | 2026-09-01 01:40 | 2026-08-31 21:00 (1 day before) |
| 2026-10-01 | 2026-10-01 00:52 | 2026-10-02 22:38 (2 days after) |
| 2026-10-20 | 2026-10-20 08:46 | 2026-10-20 04:45 |

Diffs between consecutive captures:

| Page | Pair | Blocks in A to B | Added | Removed | Most substantive change |
|---|---|---|---|---|---|
| best-practices | Jul 31 to Sep 1 | 294 to 284 | 28 | 38 | The permissions passage replaces the auto-mode, allowlist and sandbox paragraph with a fuller classifier-based auto mode description. |
| best-practices | Sep 1 to Oct 1 | 284 to 283 | 7 | 8 | Auto mode becomes the starting permission mode for Pro, Max and Team plans on Claude Code 2.1.283 or later. |
| best-practices | Oct 1 to Oct 20 | 283 to 283 | 6 | 6 | The batch example adds `--permission-mode dontAsk`, and the text moves from scoping tools to pre-approving them. |
| memory | Aug 2 to Aug 31 | 241 to 243 | 20 | 18 | Auto memory now describes typed notes (user, feedback and others) instead of a list of build commands and debugging insights. |
| memory | Aug 31 to Oct 2 | 243 to 353 | 138 | 28 | AGENTS.md support is added, and a new section recommends CLAUDE.md files under 200 lines with consistent structure. |
| memory | Oct 2 to Oct 20 | 353 to 355 | 23 | 21 | AGENTS.md is read in place of CLAUDE.md, not alongside it, and path-scoped rule loading is reworded. |

No pair is build noise only. Every pair changes instructions Claude follows or the settings that govern them. The best-practices pair from September to October is the smallest change, but it changes the default permission mode.
