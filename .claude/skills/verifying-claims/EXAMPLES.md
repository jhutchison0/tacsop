# EXAMPLES — Before and After

Sidecar to `SKILL.md`. Seven pairs, one per failure shape. Pairs 1 to 6 are shapes: the systems are generic and the output is illustrative. Pair 7 is real. In every Before, nothing errored; that is why the claim felt safe.

---

## 1. The state overclaimed

**Before**:
> The timer is installed and tonight's run landed. The pipeline is live.

**After**:
> The timer is installed (deployed). The first run failed (observed), so the pipeline is not live.
> Evidence: `tail -2 logs/run.log` → `OperationalError: no such column: run_id`, `exit=1`
> The state database predates the new schema. Migrating it is the next step.

**Rules applied**: 1 (name the state), 3 (the check that could prove you wrong).
Installing a timer reaches deployed. "Landed" and "live" claim observed, and only output the run produced reaches that.

---

## 2. The check skipped

**Before**:
> Pushed to origin. The mirror is in sync.

**After**:
> Pushed to origin (deployed).
> Evidence: `git rev-parse HEAD` → `4f2a91c`; `git ls-remote origin main` → `4f2a91c refs/heads/main`
> The mirror is one push behind.
> Evidence: `git ls-remote mirror main` → `9be07d3 refs/heads/main`

**Rules applied**: 3, 4 (show it).
The push was checked and the mirror was assumed. Two claims need two probes.

---

## 3. The absence asserted

**Before**:
> That environment was never built, so I'll create its venv from scratch.

**After**:
> The venv exists (observed), so I'll use it as built.
> Evidence: `cat .venv-gpu/pyvenv.cfg` → `version_info = 3.12`; `.venv-gpu/bin/python -V` → `Python 3.12.13`

**Rules applied**: 3.
"It does not exist" is a claim, and one `cat` could have disproved it. Acting on the false absence would have rebuilt what was already there.

---

## 4. The fix not exercised

**Before**:
> Fixed: the scan now skips empty partitions.

**After**:
> The scan fix is tested: it skips empty partitions.
> Evidence: `.venv/bin/pytest -k empty_partition; echo "exit=$?"` → `2 passed, 61 deselected in 0.41s`, `exit=0`

**Rules applied**: 1, 3.
"Fixed" claims tested. Until a run exercised the change, the true sentence was "the fix is written".

---

## 5. The validation not run

**Before**:
> Production validation passed; the outputs match the reference.

**After**:
> The staging validation passed (tested).
> Evidence: `./validate --against staging; echo "exit=$?"` → `412 of 412 rows match`, `exit=0`
> UNVERIFIED: the production validation needs read access to the production store, and this session has none. To check: `./validate --against prod --read-only`.

**Rules applied**: 4, 6 (probes read).
A weaker check that ran does not carry the stronger claim. `UNVERIFIED` names the blocker and the command, so the reader can close it.

---

## 6. The stale number

**Before**:
> The cache is at 41 GB after the sweep.

**After**:
> The cache holds 58 GB (observed).
> Evidence: `du -sh cache/` → `58G	cache/`
> The 41 GB in my earlier message was measured before the last three runs.

**Rules applied**: 2 (this turn).
The number was true once. A figure carried forward from earlier in a session is a claim about then, reported as a claim about now.

---

## 7. The count from memory (real)

**Before**:
> The template `conftest.py` is 11 lines.

**After**:
> The template `conftest.py` is 12 lines.
> Evidence: `wc -l tests/conftest.py` → `12 tests/conftest.py`

**Rules applied**: 2, 3.
The plan that commissioned this skill made this claim in its first draft, and a reviewer's `wc -l` caught it. A count typed from memory is stale on arrival. Small numbers get the same probe as large ones.
