# Session: uv Environment Doctrine — Authored, Field-Verified, Propagated

**Date**: 2026-08-03
**Branch**: main
**Tags**: #session #doctrine #environment #uv #propagation #complete

**Documents**: [docs/doctrine-updates.md](../doctrine-updates.md) (2026-08-03 entry), [.claude/skills/python-venv-management/SKILL.md](../../.claude/skills/python-venv-management/SKILL.md) (3.0.0), [docs/tasks.md](../tasks.md)
**References**: elephant-graveyard `383ebc7`, quest-engine `aa9304c`, dnd-minis `3f9d4a4` (sibling spec fixes, committed local); scratchpad freezes for the 10 migrated venvs
**Follows**: [20260726_veil_engine_bootstrap.md](20260726_veil_engine_bootstrap.md)

---

## Summary

uv (Astral) is now the environment engine, at the drop-in level the user selected: `uv venv --managed-python` + `uv pip`, no lockfile, pyproject untouched. The doctrine was not just written; it was run against this machine before shipping, and the field exercise changed it. A `pyvenv.cfg` sweep found 10 incumbent-coupled venvs where the entry's original name-glob saw 5; 8 rebuilt at exact test parity (6,898 passing tests), 2 torch/CUDA venvs were deferred by explicit decision, pyenv came off the box only after the sweep came back clean, and the corrected entry then went live to 15 downstream repos. The parity gate also caught three latent dependency bugs in sibling repos, each fixed and committed in its own repo the same day.

## Work Completed

1. **tacsop converted** (269 tests, up from 268). Living docs (`CLAUDE.md`, `README.md`, `CONTEXT.md`), `config/project.yaml` (`package_manager: "uv"`, stale numpy known-issue dropped), and the two in-code install hints, changed test-first: guard tests tightened to `match="uv pip install"` plus one new pandas-guard test, watched fail, then the strings. Audit hook logged both src edits `OK_TEST_EXISTS`.
2. **`python-venv-management` rebuilt as 3.0.0** on uv across all three files: managed-interpreter principle, uv command surface, pyenv → `uv python` / pip-tools → `uv pip compile` / pipx → `uvx`, uv failure modes (no in-venv pip; `.python-version` collides with pyenv during migration), incumbent-migration order. Shift-left `CI.md` moved to `astral-sh/setup-uv` with built-in caching.
3. **Doctrine entry authored, then field-verified on this box.** Ten venvs across nine repos rebuilt or dispositioned; parity results: daily_weather 443+1s, elephant-graveyard 2200+27s, paperboy 166, quest-engine 3246, veil-engine 200, swimming-analytics 343, dnd-minis 14, heimdall-darkroom 17, all exact against pre-rebuild baselines.
4. **The exercise corrected the doctrine before propagation.** Three fixes shipped into the entry and SETUP.md: discover venvs by `pyvenv.cfg`, never by name (the name-glob missed `.venv-audio`, `.venv-training`, bare `venv/`, and two repos outside `~/projects/github`); `uv venv --clear` instead of `rm -rf` (refuses to replace a non-venv); freeze the old venv first as insurance. The entry now names the three dependency-drift classes a parity shortfall means.
5. **pyenv retired.** Four init lines out of `~/.bashrc` (backup: `~/.bashrc.pre-uv-migration`), `~/.pyenv` deleted, then re-verified: fresh shells resolve `/usr/bin/python3`, only the two consciously deferred venvs dangle, tacsop and veil-engine suites green post-removal.
6. **Propagated live to 15 repos** (6 new notifications, 9 appended to unread).
7. **Sibling spec bugs fixed in place**, each proven by a from-spec-alone rebuild: elephant-graveyard `requirements.txt` += `scikit-learn>=1.8` (48 tests silently uncollected without it); quest-engine `mcp>=1.0,<2.0` (2.0.0 removes `mcp.server.fastmcp`; fresh resolve lands 1.29.0 and passes 3246/3246, validating the bound); dnd-minis `[tool.setuptools] packages = []` (the documented editable install had never worked against its flat layout). Commits local to each repo, not pushed.

## Key Decisions

| Decision | Rationale |
|---|---|
| Drop-in level, not uv-native | User call after presented fork. Simplicity First; forward-compatible; lockfile adoption is a real trade-off deserving its own ADR after drop-in beds in. |
| Field-verify on this box before propagating | The user's explicit sequencing. It paid: the blast-radius command was wrong in a way that would have bricked five venvs downstream. |
| Defer both 8 GB torch venvs | User call. `.venv-training` held an expired March torch nightly no tool can reproduce; `.venv-audio` belongs to a completed show. Freezes saved; rebuild paths documented. |
| Remove pyenv only after a clean sweep | The doctrine's own removal-last rule, applied to its author. |
| Fix sibling spec bugs in their repos, same day | The parity gate's findings are each repo's bugs; proving fixes by from-spec-alone rebuilds keeps the venvs honest. |

## Pillar Compliance

- **Shift-Left**: src message changes driven by failing guard tests first; hook trail confirms.
- **Simplicity First**: drop-in over native; three one-line spec fixes over refactors.
- **Config-Driven**: `package_manager` now states what is true; stale known-issue removed rather than worked around.

## Commits

- (this commit) [doctrine] uv environment doctrine: drop-in adoption, skill 3.0.0, field-verified entry, propagation
- elephant-graveyard `383ebc7`, quest-engine `aa9304c`, dnd-minis `3f9d4a4` (in their own repos)

## Next Steps

- Work/home/laptop machines: run the corrected migration sequence (fold into the P1 rename visits); conda/miniforge expected there.
- Push the three sibling commits when ready; each sibling repo runs its own uv adoption session off the notification.
- Day-1 playbook rewrite (P2) now includes swapping its environment steps to uv.
- 0.2.0 cut when ready; the uv doctrine is in `[Unreleased]`.
- Future cycle: evaluate uv-native (`uv sync` + lockfile) with an ADR.

---

*Session closed 2026-08-03. The doctrine that tells downstream repos to verify before removing was itself verified before shipping, and needed the verification.*
