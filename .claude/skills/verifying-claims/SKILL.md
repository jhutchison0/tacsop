---
name: verifying-claims
description: House rule for success claims. Six kernel rules, four claim states (written, tested, deployed, observed), one read-only probe per claim type, and before/after examples. Use before reporting that something passed, landed, synced, exists, or is absent, and when writing or reviewing a session's Claims table.
version: "1.0.0"
---

# Verifying Claims

House rule for saying that work succeeded. A claim is any statement that something works, landed, synced, exists, or is absent. The failure this skill counters: success reported because nothing errored, not because anything proved it.

Scope, stated once: `shift-left-testing` governs how code gets tested. This skill governs what a report may say about the result, in every final message, status report, commit message, review, and session doc.

**Philosophy**: *Claim what the evidence reaches, and show the evidence.*

## When to Use

- Before any sentence that says something passed, landed, was pushed, merged, or deployed, or is live
- Before saying something is absent, unbuilt, or not done: an absence is a claim too
- Before repeating a number measured earlier in the session
- Writing the `## Claims` table at `/session-end`
- Reviewing a report: the code reviewer checks each claim for its evidence

## The Kernel

Six rules. The ambient copy lives in CLAUDE.md.

1. Name the state: written, tested, deployed, or observed. Claim only the state your evidence reaches.
2. Evidence comes from this turn. Earlier output is stale: re-run the check, re-measure the number.
3. Run the check that could prove you wrong, and read its exit status. No error is not evidence.
4. Show it: an `Evidence:` line with the command and its output. Mark what you cannot check `UNVERIFIED: <blocker>`; check what you can.
5. Deployed means a clean tree: `git status --porcelain` prints nothing.
6. Probes read; they never write to the system they check.

## The Four States (rule 1)

| State | Means | Evidence that reaches it |
|---|---|---|
| written | The change exists in a file | The diff, or the path |
| tested | A run exercised it and passed | This turn's summary line and exit status |
| deployed | It is where it runs: pushed, merged, installed | The remote SHA equals the local one, from a clean tree |
| observed | The running system did the job | Output it produced after the launch |

No state implies the next. Tested code may not be pushed, and pushed code may not have run. A report that says "live" claims observed, and needs output the run produced.

## Probes (rule 3)

One read-only probe per claim type. Each can fail, which is the point: run it, then read the result against the last column.

| Claim | State | Probe | Holds when |
|---|---|---|---|
| The run landed | observed | Its exit status; `tail <log>`; `ls -l <output>` | Exit 0, no traceback in the tail, and the output is newer than the launch |
| Pushed | deployed | `git rev-parse HEAD`; `git ls-remote origin <branch>` | The two SHAs match |
| Mirror synced | deployed | `git ls-remote <mirror> <branch>`; `git ls-remote origin <branch>` | The two SHAs match |
| Tests pass | tested | `.venv/bin/pytest; echo "exit=$?"`; `.venv/bin/python -V` | This turn's summary line shows no failures, `exit=0`, on the Python that CI runs |
| The venv exists, or does not | observed | `cat .venv/pyvenv.cfg`; `.venv/bin/python -V` | Both print (it exists), or both fail (it does not) |
| Merged | deployed | `git merge-base --is-ancestor <sha> main; echo "exit=$?"`; `git ls-remote origin main` | `exit=0`, and the remote SHA equals `git rev-parse main` |
| Deployed | deployed | In the checkout that runs: `git status --porcelain`; `git rev-parse HEAD` | The first prints nothing; the second prints the SHA you named |

A probe that cannot run here (no auth, no network, another machine) is a blocker. Say so under rule 4; do not substitute a weaker check and keep the stronger claim.

## The Evidence Line (rule 4)

One line under each claim. Paste the command and the output lines that decide it; do not paraphrase them.

```
Tests pass (tested).
Evidence: `.venv/bin/pytest; echo "exit=$?"` → `403 passed, 1 warning in 4.56s`, `exit=0`

The mirror is in sync (deployed).
UNVERIFIED: the mirror needs the VPN and this machine is off it. To check: `git ls-remote <mirror> main`.
```

`/session-end` gathers the session's claims into a `## Claims` table in the session doc, with one count below it: `Overclaims the user caught this session: N`. The format lives in `docs/session-doc-format.md`.

## What This Skill Is Not

- **Not a hedge.** `UNVERIFIED` names the blocker for a check you could not run. It is not a softener for a check you skipped. A report that marks every claim `UNVERIFIED` fails the kernel as surely as one that marks none.
- **Not a test strategy.** What to test and how lives in `shift-left-testing`. This skill starts where a result gets reported.
- **Not a gate.** Nothing blocks. A claim with no `Evidence:` line is a visible defect that a reader, a reviewer, or `grep` can find.
- **Not retroactive.** Session docs and reviews already written are records; leave them.

## Sidecar Files

- [EXAMPLES.md](EXAMPLES.md): seven before/after pairs, one per failure shape: the state overclaimed, the check skipped, the absence asserted, the stale number. Read when a rule feels abstract.

## References

- `.claude/skills/shift-left-testing/ISOLATION.md`: the deterministic twin. A tripwire stops what a test must not do; this skill covers what a report must not say.
- `docs/session-doc-format.md`: the `## Claims` table.
- The writing-simple-and-direct skill, rule 6: hedge with numbers or not at all. An `Evidence:` line is that rule applied to success.

---

**Maintained by**: Verifying Claims Skill
**Version**: 1.0.0, first committed version: directory form with one sidecar (2026-10-01)
