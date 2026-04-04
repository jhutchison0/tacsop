# Design Pillars

Define the core design principles that guide all development decisions for this project.

## Instructions

Design pillars are the non-negotiable principles that shape every technical decision. A good set of pillars:
- Contains 3-5 principles (more dilutes focus)
- Each is actionable (tells you what to do, not just what to value)
- Each has a clear "violation" (you can point to code and say "this breaks Pillar 3")
- Together they cover: quality, reliability, maintainability, and extensibility

## Template

### 1. [Pillar Name]

**Principle**: One sentence stating the rule.

**Why**: Why this matters for this project specifically.

**In practice**:
- Concrete guideline 1
- Concrete guideline 2
- Concrete guideline 3

**Violation example**: What it looks like when this pillar is broken.

---

## Example Pillars (replace with your own)

### 1. Simplicity First

**Principle**: Make every change as simple as possible.

**Why**: Simple code is easier to debug, test, and extend. Complexity is the enemy of reliability.

**In practice**:
- Three similar lines of code > premature abstraction
- Only add features that are explicitly needed
- Prefer stdlib over third-party when the task is straightforward

**Violation example**: Creating a generic framework to solve a one-time problem.

### 2. Shift-Left Testing

**Principle**: Tests are written alongside code, not as an afterthought.

**Why**: Bugs found early are cheap to fix. Bugs found in production are expensive.

**In practice**:
- Every new function gets a test in the same PR
- Tests must pass before merge
- Edge cases are tested, not just happy paths

**Violation example**: A PR with 200 lines of new code and zero tests.

### 3. Config-Driven

**Principle**: Tunable parameters live in config files, not in source code.

**Why**: Changing behavior shouldn't require code changes, rebuilds, or redeployments.

**In practice**:
- All thresholds, limits, and toggles live in `config/project.yaml`
- API keys and secrets live in `.env` (never committed)
- Hardcoded magic numbers are a code smell

**Violation example**: A retry count hardcoded as `3` in the middle of a function.
