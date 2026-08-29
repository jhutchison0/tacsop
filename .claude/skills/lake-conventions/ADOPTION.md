# Adopting `lake-conventions`

For a repo that reads from or writes to the lake. Once per repo.

## 1. Copy the skill

```bash
cp -r <hub>/.claude/skills/lake-conventions .claude/skills/
diff -r <hub>/.claude/skills/lake-conventions .claude/skills/lake-conventions && echo identical
```

Level 0: copy whole, never edit locally. Route fixes upstream so the next repo
gets them. A local edit is drift with a good excuse.

## 2. Point something at it

A skill nothing references is a skill nobody loads. Add a line to `CLAUDE.md`
naming the skill and the reference repo:

> Data going to or coming from the lake follows `.claude/skills/lake-conventions/`.
> The authoritative source is the `dis-lakehouse` repo, on work machines at the
> path in `config/project.yaml` under `machines.<host>.references.lakehouse`.

Then add it to the repo's `CONTEXT.md` Reading Order.

## 3. Add the machine roster, if the repo has none

`config/project.yaml` needs a `machines:` block so the preflight can find the
reference repo. See the hub's, and add only the hosts this repo is cloned on.
No usernames.

## 4. Copy the preflight, if the repo writes to the lake

```bash
cp <hub>/scripts/lake_preflight.py scripts/
cp <hub>/tests/unit/test_lake_preflight.py tests/unit/
pytest tests/unit/test_lake_preflight.py
```

It imports `resolve_machine` from the repo's own package. Fix that import to
match the local package name; nothing else is repo-specific.

Skip this step for a read-only consumer. A preflight nobody runs is worse than
none, because it looks like coverage.

## 5. Run it once and read the output

```bash
python scripts/lake_preflight.py --target dev
```

**Expect a nonzero first result.** Most repos are missing credentials in the
shell, or have never declared their legs. Read every line before wiring it into
anything. Do not add a check whose output you have not read.

## Rollback

Delete `.claude/skills/lake-conventions/`, `scripts/lake_preflight.py`, and its
test; drop the `CLAUDE.md` and `CONTEXT.md` lines. Nothing else depends on them.
The `machines:` block can stay; it is useful on its own.
