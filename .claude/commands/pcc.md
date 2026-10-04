# PCC - Pre-Code Check

Run a quick, standardized checklist before pushing code. Same checks every time - muscle memory.

**Military origin**: Pre-Combat Check - the quick gear check every soldier does before moving out. Ammo, water, weapon. No thinking required, just verify the basics.

## Philosophy

PCC is **fast and deterministic**. It answers: "Am I safe to push?"

- Same checklist every time
- Pass/fail, no judgment calls
- Takes seconds, not minutes
- Run before every push

For context-aware inspection based on what you changed, use `/pci` instead.

## Checklist

Run these checks and report results:

### 1. Secrets Check
```bash
# Check for staged secrets
git diff --cached --name-only | xargs grep -l -E "(API_KEY|SECRET|PASSWORD|TOKEN|PRIVATE_KEY)\s*=" 2>/dev/null || echo "clean"

# Check for .env files staged
git diff --cached --name-only | grep -E "^\.env" || echo "clean"
```
- FAIL if any secrets patterns found in staged files
- FAIL if .env files are staged

### 2. Tests Pass
```bash
# Run all tests
pytest
```
- FAIL if any tests fail
- Report count: "X tests passed"

### 3. No Debug Artifacts
```bash
# Check for common debug leftovers in staged files
git diff --cached | grep -E "^\+" | grep -E "(breakpoint\(\)|import pdb|print\(.*DEBUG)" || echo "clean"
```
- WARN if debug statements found (not a hard fail, but flag it)

### 4. Git State Check
```bash
# Check for uncommitted changes that might be forgotten
git status --short
```
- WARN if unstaged changes exist (might forget to include them)
- INFO showing current branch

### 5. Reference Integrity (living docs)
```bash
# Path-shaped references in orientation surfaces must resolve.
# Catches drift like the March-2026 case: tasks.md carrying paths to files
# that do not exist. Allowlist covers runtime artifacts that are
# legitimately absent (the two upstream notification files, gitignored audit logs).
# Extension bound is {2,8}, not {2,4}: a 4-cap truncates .geojson/.service/.shtml
# and then reports the truncated path as MISSING (found by the launch-control
# canary 2026-08-17, where it produced 3 false positives against real files).
# The task list is scanned from its first line, so the ## Focus section above
# ## Active is covered; ## Completed and below are records and are not.
{ cat CLAUDE.md CONTEXT.md README.md LANGUAGE.md .claude/README.md 2>/dev/null; \
  sed -n '1,/^## Completed/p' docs/tasks.md; } \
  | grep -oE '(docs|src|tests|config|scripts|\.claude|\.github)/[A-Za-z0-9_./-]+\.[A-Za-z0-9]{2,8}' \
  | grep -vE '^\.claude/(upstream-update\.md|upstream-lesson\.md|audits/)' \
  | sort -u | while read -r p; do [ -e "$p" ] || echo "MISSING: $p"; done
```
- Expected output: empty. WARN on any MISSING line, and record the run's count in the session doc (it is metric M2 in `.claude/skills/traversing-the-knowledge-base/SKILL.md`; an unrecorded run is indistinguishable from an unrun check)
- Any MISSING line is caught drift and fires that skill's build trigger

**Three known blind spots. A clean run means clean only within them** (found in the field, 2026-08-21 `contract-knowledge-graph` and 2026-08-22 `aar_ai_pipeline`; see the amendments to the 2026-08-21 doctrine entry):
1. **Directory references are invisible.** The regex requires a file extension, so `.claude/agents/` never matches. In `aar_ai_pipeline` this hid 4 of 5 broken references sitting in the same table as the one that was caught. Run the directory pass below alongside the file pass.
2. **No notion of a base directory.** Every path resolves against the repo root, so a cross-repo citation and a path inside a documented `cd subdir && ...` command both report MISSING while the file exists. Hand-verify before editing the doc.
3. **A missing surface costs coverage silently.** `cat` failures are swallowed by `2>/dev/null`; an absent `CONTEXT.md` reads the same as a clean one.

```bash
# Directory pass, covering blind spot 1. Same surfaces, no extension required.
{ cat CLAUDE.md CONTEXT.md README.md LANGUAGE.md .claude/README.md 2>/dev/null; } \
  | grep -oE '(docs|src|tests|config|scripts|\.claude|\.github)/[A-Za-z0-9_./-]*/' \
  | grep -vE '^\.claude/audits/$' \
  | sort -u | while read -r p; do [ -d "$p" ] || echo "MISSING-DIR: $p"; done
```

### 6. Gate-Surface Separation
```bash
# Gate surfaces (checks, hooks, settings) change alone, per CONOP WHETSTONE D4:
# never bundled with work those gates judge.
staged=$(git diff --cached --name-only)
gates=$(echo "$staged" | grep -E '^\.claude/(hooks/|settings\.json|commands/(pcc|pci)\.md)' || true)
if [ -n "$gates" ] && [ "$(echo "$staged" | grep -c .)" -ne "$(echo "$gates" | grep -c .)" ]; then
  echo "WARN: gate surfaces staged with other files; split into a [gate] commit:"; echo "$gates"
fi
```
- WARN only; the fix is two commits, with the gate change isolated and tagged `[gate]`

### 7. Private-Term Check
```bash
# Private terms (hostnames, usernames, codenames, sibling repo names) stay out
# of a public tree. The list lives outside every repo, so this check cannot
# republish it, and the output carries each hit as a path, withholding any
# path, file name, or commit message that is itself a hit and reporting those
# as counts. Two incidents on 2026-10-01, the second found 2026-10-02: agents
# wrote another repo's names into docs/reviews/, and the record of containing
# that pasted the five terms into an Evidence line, committed and pushed.
# Scans what a push would carry: the index, and every commit not on any
# remote, their file names and messages included. A line printed is the
# finding; the block itself exits 0.
terms="${TACSOP_PRIVATE_TERMS:-$HOME/.config/tacsop/private-terms}"
clean=$(sed -e 's/^[[:space:]]*//;s/[[:space:]]*$//' -e '/^$/d' "$terms" 2>/dev/null)
if [ -z "$clean" ]; then
  echo "WARN: no private-term list at $terms; check 7 did not run"
elif ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "WARN: not inside a git repository; check 7 did not run"
else
  revs=$(git rev-list HEAD --not --remotes 2>/dev/null)
  paths=$(for rev in --cached $revs; do
            git grep -l -i -F -f <(printf '%s\n' "$clean") $rev -- ':/'
          done | sed -E 's/^[0-9a-f]{40}://' | sort -u)
  names=$({ git ls-files --cached; for rev in $revs; do git ls-tree -r --name-only "$rev"; done; } | sort -u)
  msgs=$(for rev in $revs; do git log -1 --format=%B "$rev"; done)
  held=$(printf '%s\n' "$paths" | sed '/^$/d' | grep -c -i -F -f <(printf '%s\n' "$clean"))
  if [ "$held" -gt 0 ]; then echo "FAIL private term in $held path name(s) with content hits; paths withheld"; fi
  printf '%s\n' "$paths" | sed '/^$/d' | grep -v -i -F -f <(printf '%s\n' "$clean") | sed 's/^/FAIL private term in: /'
  m=$(printf '%s\n' "$names" | sed '/^$/d' | grep -c -i -F -f <(printf '%s\n' "$clean"))
  if [ "$m" -gt 0 ]; then echo "FAIL private term in $m tracked file name(s); names withheld"; fi
  k=$(printf '%s\n' "$msgs" | grep -c -i -F -f <(printf '%s\n' "$clean"))
  if [ "$k" -gt 0 ]; then echo "FAIL private term in $k unpushed commit message line(s); not printed"; fi
fi
```
- Expected output: empty. FAIL on any line. `FAIL private term in: <path>` names a file whose path is clean, in the index or in a commit not on any remote. The other three FAIL lines give counts only, because the path, the name, or the message is itself the hit: find them locally with the same grep, and do not paste what it prints. A hit in an old commit is already public: redact forward first, then decide about history. A repository with no remote scans all of HEAD's history, which is what a first push carries. "Not on any remote" reads the tracking refs, which are a cache: `git fetch` first when another machine may have pushed.
- WARN means this machine has no list, or this directory is not a git repository. Write the list (one term per line, matched case-insensitively as a fixed string, inside words too, so choose distinctive terms; a false positive is safe) before trusting a clean run. The list is per machine and is never committed anywhere.
- Never paste a term into this check's output, a commit message, a review, or a session doc. Give the count and, when it is clean, the path.

## Output Format

```
PCC Results
===========
[PASS] No secrets in staged files
[PASS] Tests pass (12 tests in 0.8s)
[WARN] Debug statement found: src/myproject/utils/logger.py:45
[INFO] Branch: main, 3 files staged

PCC Status: READY TO PUSH (1 warning)
```

Or on failure:
```
PCC Results
===========
[PASS] No secrets in staged files
[FAIL] Tests failing
       2 failed, 10 passed
       - tests/unit/test_math_utils.py::test_nCr - AssertionError
[PASS] No debug artifacts

PCC Status: NOT READY - 1 failure, resolve before pushing
```

## Quick Reference

| Check | Pass Condition | On Fail |
|-------|----------------|---------|
| Secrets | No API_KEY, SECRET, PASSWORD, TOKEN in diff | Block push |
| Tests | `pytest` all pass | Block push |
| Debug | No breakpoint/pdb/print in staged code | Warn only |
| Git state | Clean or intentional | Info only |
| Reference integrity | Zero MISSING paths in living docs (allowlist current) | Warn only |
| Gate separation | Gate surfaces staged alone (`[gate]` commit) | Warn only |
| Private terms | Zero hits for this machine's private-term list over the index and unpushed commits, list present | Block push |

## Integration

PCC is designed to be called:
- Manually before push: `/pcc`
- From session-end workflow (optional step)
- After completing a feature before PR

It does NOT:
- Analyze what you changed (that's PCI)
- Make judgment calls about code quality
- Take more than 60 seconds

## Escalation

If PCC passes but you want more confidence (big change, pre-merge):
```
/pci
```
