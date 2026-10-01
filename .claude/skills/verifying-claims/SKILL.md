---
name: verifying-claims
description: House rule for success claims. Six kernel rules, four claim states (written, tested, deployed, observed), one read-only probe per claim type, and before/after examples. Use before reporting that something passed, landed, synced, exists, or is absent, and when writing or reviewing a session's Claims table.
version: "1.0.0"
---

# Verifying Claims

House rule for saying that work succeeded. A claim is a statement a reader will act on, or one that closes a task: that something works, landed, synced, exists, or is absent. A plan, an opinion, an explanation of code, or a diff shown in the same message is not a claim. The failure this skill counters: success reported because nothing errored, not because anything proved it.

Scope, stated once: `shift-left-testing` governs how code gets tested. This skill governs what a report may say about the result, in every final message, status report, commit message, review, and session doc. It also covers working narration that acts on an unchecked belief: "that was never built, so I will rebuild it" is a claim.

**Philosophy**: *Claim what the evidence reaches, and show the evidence.*

## When to Use

- Before any sentence that says something passed, landed, was pushed, merged, or deployed, or is live
- Before saying, or acting on the belief, that something is absent, unbuilt, or not done
- Before repeating a number measured earlier in the session
- Writing the `## Claims` table at `/session-end`
- Reviewing a report: the code reviewer checks each claim for its evidence

## The Kernel

Six rules. The ambient copy lives in CLAUDE.md.

1. Name the state: written, tested, deployed, or observed. Claim no higher than your evidence reaches; an absence is a claim too.
2. Evidence comes from this turn, after your last change. Earlier output is stale: re-run the check, re-measure the number.
3. Check the outcome the claim names, with a check that can fail. A launcher's exit 0 is not the outcome; no error is not evidence.
4. Under each claim a reader will act on: an `Evidence:` line with the command and its output, or `UNVERIFIED: <blocker>`. A skipped check is not a blocker; run it.
5. A checkout that runs code is deployed only when clean: `git status --porcelain` prints nothing.
6. Probes read; they never write to the system they check.

## The Four States (rule 1)

| State | Means | Evidence that reaches it |
|---|---|---|
| written | The change exists in a file | The diff, or the path |
| tested | A run exercised it and passed | This turn's summary line and exit status. An import or a compile does not reach it |
| deployed | It is delivered: pushed, merged, installed, or running from a checkout | The remote SHA equals the local one; for a checkout that runs code, a clean tree as well |
| observed | The live system, looked at: output it produced, or its present state | Output the run produced after the launch, or a read of the thing as it is now |

No state implies the next. Tested code may not be pushed, and pushed code may not have run. A report that says "live" claims observed, and needs output the run produced.

## Probes (rule 3)

One read-only probe per claim type. Each can fail, which is the point: run it, then read the result against the last column.

| Claim | State | Probe | Holds when |
|---|---|---|---|
| The run landed | observed | The run's own exit status; `tail <log>`; `ls -l <output>` | Exit 0, the log ends with the run's completion line, and the output is newer than the launch |
| Pushed | deployed | `git rev-parse HEAD`; `git ls-remote origin <branch>` | The second prints one line, and its SHA equals the first |
| Mirror synced | deployed | `git ls-remote <mirror> <branch>`; `git ls-remote origin <branch>` | Each prints one line, and the two SHAs match |
| Tests pass | tested | `.venv/bin/pytest; echo "exit=$?"`; `.venv/bin/python -V` | The summary line shows no failures and `exit=0`, on the Python the CI config names (with no CI, say which Python ran) |
| The venv exists, or does not | observed | `ls -d .venv*`; `cat <venv>/pyvenv.cfg`; `<venv>/bin/python -V` | The cfg prints and Python runs: usable. The cfg prints and Python fails: there, but broken. `ls` finds nothing: absent |
| Merged | deployed | `git merge-base --is-ancestor <sha> main; echo "exit=$?"`; `git ls-remote origin main` | `exit=0`, and the remote SHA equals `git rev-parse main` |
| Deployed | deployed | In the checkout that runs: `git status --porcelain`; `git rev-parse HEAD`; `git ls-remote origin <branch>` | The first prints nothing, and the two SHAs match |

Four traps the table cannot hold:

- **Empty output is not a match.** `git ls-remote` prints nothing and exits 0 for a branch the remote lacks.
- **An exit status after a pipe belongs to the pipe's last command.** `pytest | tail -1; echo $?` reports `tail`.
- **A long-running process** must also have started after the code arrived: `ps -o lstart= -p <pid>`.
- **Tests are the one probe that runs code.** Rule 6 holds for them through the test tripwire (`shift-left-testing/ISOLATION.md`).

A probe that cannot run here (no auth, no network, another machine) is a blocker. Say so under rule 4; do not substitute a weaker check and keep the stronger claim.

## The Evidence Line (rule 4)

One line under each claim. Paste the command and the output lines that decide it; do not paraphrase them. Claims that share a check share the line.

```
Tests pass (tested).
Evidence: `.venv/bin/pytest; echo "exit=$?"` → `403 passed, 1 warning in 4.56s`, `exit=0`

UNVERIFIED: the mirror sync. `git ls-remote mirror main` → `fatal: unable to access: Could not resolve host`; this machine is off the VPN.
```

Make the blocker checkable too: paste its error when there is one, and name the machine or the access when there is not. `/session-end` gathers the session's claims into a `## Claims` table in the session doc, with one count below it: `Overclaims the user caught this session: N`. The format lives in `docs/session-doc-format.md`.

## What This Skill Is Not

- **Not a hedge.** `UNVERIFIED` names the blocker for a check you could not run. It is not a softener for a check you skipped. A report that marks every claim `UNVERIFIED` fails the kernel as surely as one that marks none.
- **Not a line under every sentence.** Evidence goes under what a reader will act on. Saying what you did not do ("I have not run the tests") is a true report, not an unverified claim.
- **Not proof.** A weak check honestly labeled passes the letter, and so does invented output. The line makes a claim checkable; a reader or a second agent re-running it does the checking.
- **Not a test strategy.** What to test and how lives in `shift-left-testing`. This skill starts where a result gets reported.
- **Not a gate, and not retroactive.** Nothing blocks; a missing line is a defect a reader or `grep` can find. Docs already written are records; leave them.

## Sidecar Files

- [EXAMPLES.md](EXAMPLES.md): seven before/after pairs, one per failure shape (the state overclaimed, the check skipped, the absence asserted, the stale number), and one clean report that needs nothing added. Read when a rule feels abstract.

## References

- `.claude/skills/shift-left-testing/ISOLATION.md`: the deterministic twin. A tripwire stops what a test must not do; this skill covers what a report must not say.
- `docs/session-doc-format.md`: the `## Claims` table.
- The writing-simple-and-direct skill, rule 6: hedge with numbers or not at all. An `Evidence:` line is that rule applied to success.

---

**Maintained by**: Verifying Claims Skill
**Version**: 1.0.0, first committed version: directory form with one sidecar (2026-10-01)
