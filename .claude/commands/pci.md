# PCI - Pre-Code Inspection

Context-aware code inspection based on what you changed. The inspection adapts to your commit.

**Military origin**: Pre-Combat Inspection - the leader's check based on the specific mission. Going to the mountains? Check cold weather gear. Night mission? Check NVGs and IR. The inspection fits the operation.

## Philosophy

PCI is **contextual and intelligent**. It answers: "What should I look closely at given these changes?"

- Analyzes your actual diff
- Applies relevant checks based on files touched
- Catches issues PCC can't (architectural, design principle violations)
- Run before merge/PR, or when PCC passes but you want confidence

For the quick standardized checklist, use `/pcc` first.

## Workflow

### Step 1: Analyze the Change Set

```bash
# Get changed files (staged + unstaged, or branch diff)
git diff --name-only HEAD~1  # Last commit
git diff --name-only main    # Branch diff from main
git diff --cached --name-only  # Staged only
```

Categorize files into domains based on the project structure:

| Domain | Paths |
|--------|-------|
| **Utilities** | `src/myproject/utils/*.py` |
| **Config** | `config/*.yaml` |
| **Tests** | `tests/**/*.py` |
| **Documentation** | `docs/**/*.md` |
| **Infrastructure** | `.claude/**`, `pyproject.toml`, `.gitignore` |

### Step 2: Apply Domain-Specific Checks

---

#### Utility Changes (`src/myproject/utils/*.py`)

- [ ] **Type hints**: All public functions annotated?
- [ ] **Docstrings**: Google-style with Args/Returns/Raises?
- [ ] **No global state**: Module-level mutables avoided?
- [ ] **Error handling**: External calls (network, file I/O) handled gracefully?
- [ ] **Dependencies**: Only uses deps from the correct optional group in pyproject.toml?
- [ ] **Backward compatible**: Existing callers still work?

---

#### Config Changes (`config/*.yaml`)

- [ ] **YAML valid**: Config files parse without errors?
- [ ] **No secrets**: API keys come from environment variables, not config files?
- [ ] **New fields documented**: Comments explaining purpose?

---

#### Test Changes (`tests/**/*.py`)

- [ ] **Coverage for new code**: New functions/classes have corresponding tests?
- [ ] **No flaky tests**: Tests don't depend on network, timing, or execution order?
- [ ] **Assertions match intent**: Tests check the right thing, not just "no exception"?
- [ ] **Edge cases covered**: Empty input, malformed data tested?

---

### Step 3: Report Findings

```
PCI Report - Branch: feature-name (vs main)
============================================

Changes Analyzed:
  4 files changed, 95 insertions(+), 12 deletions(-)

Domains Touched:
  [Utilities] src/myproject/utils/geo.py
  [Tests] tests/unit/test_geo.py

Inspection Results:

[Utility Compliance] src/myproject/utils/geo.py
  [OK] Type hints on all public functions
  [OK] Google-style docstrings
  [WARN] Line 42: Missing error handling for negative radius

[Tests]
  [OK] New functions have test coverage
  [MISS] No edge case test for antipodal points

Summary:
  0 blocking issues
  1 warning
  1 missing test
```

## Output Levels

### Quick Mode (default)
Just the summary and action items:
```
/pci
```

### Verbose Mode
Full inspection details for each file:
```
/pci --verbose
```

## Integration with PCC

Typical workflow:
```
1. /pcc              # Quick check - am I safe to push?
2. [fix any failures]
3. /pci              # Deep inspection - what should I review?
4. [address findings]
5. git push
```

## Key Files to Reference

| Purpose | File |
|---------|------|
| Project status & phases | `config/project.yaml` |
| Design principles | `docs/design/pillars.md` |
| Project roadmap | `docs/design/roadmap.md` |
