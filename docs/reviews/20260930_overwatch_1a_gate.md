# Review: OVERWATCH Wave 1 Task 1a Gate (`topic/overwatch-sealed-tests`)

**Author**: code-reviewer
**Date**: 2026-09-30
**Type**: Code review (merge gate)
**Subject**: `git diff main...HEAD`, one commit (`6039e14`), 7 files: `tests/isolation.py`, `tests/unit/test_isolation.py`, `tests/conftest.py`, `.claude/skills/shift-left-testing/ISOLATION.md`, `SKILL.md`, `SKILLS_FRAMEWORK.md`, `.claude/README.md`. Acceptance test: task 1a's Standard, `docs/plans/conop_overwatch_claim_verification_and_irreversible_guards.md:188`.

---

## Verdict: GO-WITH-FIXES

3 Critical, 9 Warning, 11 Suggestion (one of them a Minor prose finding).

The design holds: one audit hook, armed for setup, call, and teardown, catches the incident's import-bound `rmtree` and every case the Standard names. Two Standard clauses fail as shipped: the suite goes red with `CI=1` (C3), and the cannot-see list omits verified fail-open paths (W2 to W4) and misstates one (C2). Do not merge until C1 to C3 are fixed and each fail-open path in W2 to W4 is either closed or listed. Then re-run the full suite with and without `CI=1`.

The CONOP's Wave 1 exit (`:194`) asks for GO; its MOP (`:152`) accepts GO-WITH-FIXES with fixes applied. S10 asks the lead to pick one.

### Critical, one line each

- **C1**: `_inside` folds paths differently from the kernel. `shutil.rmtree("<allowlisted symlink>/")` emptied a real directory, and `os.unlink("<symlink>/../file")` deleted a real file, with no catch and no log line.
- **C2**: pytest runs all of `conftest.py` before it reads `pytest_plugins`. ISOLATION.md step 2 ("above any import of production code") therefore guards nothing. In fleet repos shaped like swimming-analytics and project-megan, the real `.env` loads anyway, or the tripwire never registers.
- **C3**: `test_default_roots_are_temp_hypothesis_and_configured_extras` fails whenever `CI` is set. The result is `1 failed, 324 passed` on 3.12.13 and the same failure on 3.11.15.

---

## Part 1a: The Task 1a Standard, Clause by Clause

| # | Clause | Mark | Evidence |
|---|---|---|---|
| 1 | Each tripwire test narrows the allowlist | PASS | All 6 deletion tests and the log test take `sandbox` (`test_isolation.py:34-42`). The 2 network tests need no allowlist. |
| 2 | Targets a sentinel outside it (never `/data`) | PASS | Sentinels sit in `tmp_path/outside`. `/data/grib/latest.grib2` appears only in a pure `_inside` call (`:211`). |
| 3 | Asserts the tripwire's own exception class | PASS | 8 uses of `pytest.raises(isolation.IsolationError)`. |
| 4 | Asserts the sentinel still exists | PASS | Holds for all 5 deletion cases. The log test does not check, and the clause does not require it. |
| 5 | Cases: `Path.unlink`, import-bound `rmtree`, `os.rmdir`, subprocess `rm`, non-loopback `connect` | PASS | All present. With the hook disabled (mutant M4), exactly these 8 catch tests fail (`8 failed, 9 passed`). |
| 6 | `load_dotenv` is a no-op for the repo's real `.env` | PASS at the hub | Probe run against the hub's real `.env`: `load_dotenv(REPO_ENV)` and `load_dotenv(str(REPO_ENV), None, False, True)` both return `False`, and 0 of its 1 key is set. It fails downstream (C2), and a `stream=` argument bypasses it (W1). |
| 7 | Passes through for a path under `tmp_path` | PASS | `test_load_dotenv_inside_allowlist_still_loads`. Mutant M6 (block everything) fails 2 tests. |
| 8 | A catch appends one line to the tripwire log | PASS | Test at `:135`. The probes wrote one line per catch to `<rootdir>/.claude/audits/isolation-tripwire.log`. |
| 9 | `ISOLATION.md` lists what the tripwire cannot see | FAIL | A list exists (`ISOLATION.md:63-72`). It omits 5 verified fail-open classes (C1, W2, W3, W4) and misstates the conftest case (C2). |
| 10 | The full suite passes armed | FAIL | Without `CI`, 325 passed and no catch log was created. With `CI=1`, the result is `1 failed, 324 passed` (C3). GitHub Actions sets `CI=true` (`tests/conftest.py:8`). |

---

## Part 1b: Findings

Probe harness: scratch projects under `$S/gate1a/` (`$S` is this session's scratchpad), each a copy of `tests/isolation.py` registered from a conftest. `TMPDIR` points at `$S/gate1a/tmpA`, so the allowlist is narrower than `/tmp` and every victim (`$S/gate1a/real*`) sits outside it. No probe ran inside the repo or against real data. The suite command is `TMPDIR=$G/tmpA .venv/bin/pytest -q -p no:cacheprovider tests/<probe>.py`.

### Critical

**C1. `_inside` and the kernel disagree on symlinks, so `shutil.rmtree` and `os.unlink` delete through an allowlisted link** (`tests/isolation.py:41-46`)

- **Issue**: `os.path.abspath` (`:42`) folds `..` lexically before any symlink is resolved. The final component is never resolved, even when a trailing `/` or `.` makes the kernel follow it.
- **Evidence** (a link in `tmpA` pointing at a victim directory in `real/`):

  ```
  test_P1  shutil.rmtree(str(link) + "/")
           -> no IsolationError; rmtree then raised
              OSError: [Errno 20] Not a directory: '.../tmpA/p1link/'
           $ ls -A real/test_P1_rmtree_trailing_slash_through_symlink
           (empty: data.bin deleted)
  test_P2  os.unlink(f"{link}/../data.bin")   # link -> real/test_P2/sub
           $ ls -A real/test_P2_unlink_dotdot_after_symlink
           sub                                  (data.bin deleted)
  ```

  Neither catch appears in the probe's tripwire log.
- **Why it matters**: `shutil.rmtree` is the incident's call. Two ordinary data-repo habits are enough to trigger it: a test that symlinks the real cache into `tmp_path` instead of copying it, and a config path with a trailing slash (`cache_dir: ".../cache/"`).
- **Fix** (verified: P1 and P2 now raise `IsolationError`; the 8 probe controls and the 17 hub tests still pass):

  ```python
  def _inside(path, roots) -> bool:
      raw = os.fsdecode(path)
      if not os.path.isabs(raw):
          raw = os.path.join(os.getcwd(), raw)  # no abspath: it folds ".." before symlinks resolve
      parent, name = os.path.split(raw.rstrip(os.sep) or os.sep)
      if raw.endswith(os.sep) or name in ("", ".", ".."):
          target = Path(os.path.realpath(raw))  # the kernel follows the last component here
      else:
          target = Path(os.path.realpath(parent)) / name  # deleting a link removes the link
      return any(target == root or root in target.parents for root in roots)
  ```

  Add three tests: a symlinked parent, a trailing slash, and `..` after a link. They also kill mutant M2 (W8).

**C2. Adoption step 2 leaves the dotenv guard off in downstream conftests, and in one shape drops the tripwire entirely** (`ISOLATION.md:71`, `:85`, `:44` last sentence; `tests/isolation.py:107-108`)

- **Issue**: pytest imports the whole `conftest.py` module, then reads `pytest_plugins`. Where the line sits in the file does nothing. A production import anywhere in `conftest.py` runs before the guard exists. A later `pytest_plugins = [...]` assignment in the same file replaces the line.
- **Evidence** (`$G/proj3`: `prodpkg/__init__.py` calls `load_dotenv()` at import, and `.env` sits at the project root):

  | conftest shape | Result |
  |---|---|
  | A: plugin line only (control) | `2 passed` |
  | B: plugin line first, then `import prodpkg` (step 2 as written) | `2 failed`: `LOADED_AT_IMPORT` is `True`, and a later `prodpkg.later.configure()` loads the real `.env` through a real `load_dotenv` bound at conftest import |
  | B plus a later `pytest_plugins = ["tests.fixtures.audio_fixtures"]` | `AssertionError: tripwire plugin not registered`; the suite is otherwise green with no tripwire |
  | D: `addopts = ["-p", "tests.isolation"]` in `[tool.pytest.ini_options]`, shapes B and megan | `2 passed` from the project root, from `tests/`, and via `python -m pytest` |

- **Fleet shapes** (read-only grep of `~/projects/github`): `swimming-analytics/tests/conftest.py:15` imports `web.app`, which imports `config.settings`, whose line 10 calls `load_dotenv()` at import. `project-megan/tests/conftest.py:12` imports `megan.safety`, and `:31` assigns `pytest_plugins`. `fist/tests/conftest.py:8` imports `fist.roots`, which binds the real `load_dotenv` at `roots.py:21`; fist's own autouse patch covers that one.
- **Why it matters**: two of the 14 local repos with test suites would follow the doc and get no dotenv guard (swimming-analytics) or no tripwire at all (project-megan). The doc's own limit bullet tells them they are covered. Chained with W4, a real `PGHOST` from a leaked `.env` and a `psycopg` connect by IP reach a real database with no catch.
- **Fix**: register through `addopts = ["-p", "tests.isolation"]` beside `pythonpath = ["."]` (verified on pytest 9.1.1; older pytest not measured). This changes 1a's Condition ("registered from `tests/conftest.py` by one line"), so log it in the CONOP Status Log. Rewrite `ISOLATION.md:71` and `:85` and the `_guard_dotenv` docstring. Optional hardening: in `_guard_dotenv`, rebind any `sys.modules` attribute that `is real` to the guard, which covers names bound before the plugin loaded.

**C3. One tripwire test fails whenever `CI` is set** (`tests/unit/test_isolation.py:209`)

- **Evidence**:

  ```
  $ CI=1 .venv/bin/pytest -q
  FAILED tests/unit/test_isolation.py::test_default_roots_are_temp_hypothesis_and_configured_extras
         - AttributeError: 'NoneType' object has no attribute 'path'
  1 failed, 324 passed, 1 warning in 4.44s
  $ CI=1 $S/py311/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_isolation.py
  1 failed, 16 passed
  ```

  Under the hub's own `register_profile("ci", max_examples=300, deadline=None)`, `settings().database` is `None` (Hypothesis 6.165.0).
- **Why it matters**: `tests/conftest.py:8` states that GitHub Actions sets `CI=true`, and `CI.md` ships that workflow downstream. Any repo that takes this test file goes red on every CI run. The plugin itself already handles `None` (`isolation.py:135` catches the `AttributeError`). Only the test assumes a path.
- **Fix**:

  ```python
  db_path = getattr(settings().database, "path", None)
  if db_path is not None:
      assert Path(os.path.realpath(db_path)) in roots
  ```

  Add `CI=1 .venv/bin/pytest -q` to the gate checklist for any change that touches Hypothesis.

### Warning

**W1. `load_dotenv(real_path, stream=...)` loads the real file** (`tests/isolation.py:118`)

- The guard passes the call through whenever `stream is not None`. python-dotenv reads `dotenv_path` first when it names a file (`DotEnv._get_stream`, python-dotenv 1.2.2).
- Evidence, from a probe against the hub's real `.env` that counted key names and never printed values: `load_dotenv(REPO_ENV, stream=io.StringIO(""))` returned `True` and set 1 of 1 real keys.
- Fix:

  ```python
  @functools.wraps(real)
  def load_dotenv(dotenv_path=None, stream=None, *args, **kwargs):
      allowed = _inside(dotenv_path, _allow) if dotenv_path is not None else stream is not None
      return real(dotenv_path, stream, *args, **kwargs) if allowed else False
  ```

  Positional and keyword calls already match python-dotenv's signature `(dotenv_path, stream, verbose, override, interpolate, encoding) -> bool`. The positional probe in Part 1a, clause 6 confirms it.

**W2. Six deletion paths the cannot-see list omits or misstates** (`ISOLATION.md:63-72`; `isolation.py:76-91`)

Each probe below deleted its victim with no `IsolationError` (`8 failed` in `test_failopen.py`; P1 and P2 are C1):

| Probe | Listed? | Fix |
|---|---|---|
| P3: `shutil.rmtree("victimdir", dir_fd=<fd of real/>)`, cwd in `tmpA` | Misstated: `:69` says rmtree "is checked at its top directory", but the check resolves the name against cwd, not `dir_fd` | Trip when rmtree's `dir_fd` is not `None` and the path is relative |
| P4: `subprocess.run(["cleanup", "-f", victim], executable=which("rm"))` | No | Check `os.path.basename(executable)` too, with `.exe` stripped for Windows |
| P5: `["env", "rm", "-f", victim]` | Only as a "child process" (`:67`) | Name `env`, `sudo`, `xargs`, `find -delete`, `git clean`, and `rsync --delete` in `:67` |
| P6: `os.posix_spawn(rm, ["rm", "-f", victim], os.environ)` | No | Apply the argv check to the `os.posix_spawn`, `os.spawn`, and `os.exec` audit events, and name `os.system` beside shell strings |
| P7: `os.rename(real_dir, tmpA/moved)`, then `rmtree` | No: `:65` covers a rename onto a file, not a rename away | Check the `os.rename` source against the allowlist, excluding `__pycache__` (Python's pyc writes use `os.replace`), or list it |
| P8: `["find", real, "-name", "data.bin", "-delete"]` | Only as a "child process" | List it with P5 |

**W3. The armed window has four exits the list does not name** (`isolation.py:155-164`; `ISOLATION.md:44`)

- Evidence (`$G/proj2`: one victim per shape, `2 passed, 2 errors`):

  ```
  collection: DELETED          # module-level unlink in a test module
  sessionfinish: DELETED       # conftest pytest_sessionfinish
  atexit: DELETED              # atexit.register(os.unlink, ...)
  fixture_teardown: SURVIVED   # caught: the setup/teardown claim holds
  session_teardown: SURVIVED   # caught, logged against the last test (S6)
  thread: DELETED              # thread that outlives its test
  ```

- **Why it matters**: conftest session hooks and module-level cleanup are harness code, the same class as the incident's fixture.
- **Fix**: arm collection as well, through a `pytest_collection` hookwrapper. Collection imports production code, and pytest's pyc writes rename rather than delete; re-run the suite to confirm. List session hooks (`pytest_configure`, `pytest_sessionstart`, `pytest_sessionfinish`), `atexit` handlers, and threads or finalizers that outlive their test.

**W4. Network paths the list omits** (`ISOLATION.md:41`, `:70`)

| Probe (`test_net.py`, `test_pg.py`) | Result |
|---|---|
| `psycopg.connect("host=192.0.2.1 ...")` (psycopg 3.3.4, binary) | NO-TRIP (`ConnectionTimeout`) |
| `psycopg.AsyncConnection.connect("host=192.0.2.1 ...")` | NO-TRIP (`ConnectionTimeout`) |
| `psycopg.connect("host=db.example.invalid ...")` | TRIPPED: psycopg resolves the name in Python |
| `socket.gethostbyname`, `socket.gethostbyaddr` | NO-TRIP; the lookup ran (`gaierror`, `herror`) |
| `s.connect(("example.invalid", 80))` | NO-TRIP: CPython resolves the name before it raises the `socket.connect` event, so the DNS query leaves first |
| UDP `sendmsg` to `192.0.2.1:9` | NO-TRIP (succeeded) |
| IPv6 `2001:db8::1`, `::ffff:192.0.2.1`, `connect_ex`, `127.0.0.1.nip.io`, decimal IP `3221225985` | TRIPPED |

- **Why it matters**: the template's `database.py` uses psycopg. libpq opens its own socket, so a host given as an IP raises no audit event. Loopback and Unix sockets are allowed, so an SSH tunnel (`ssh -L 5432:prod-db:5432`), a local proxy, a Docker-published port, or `/var/run/docker.sock` all reach past the box.
- **Fix**: handle the `socket.gethostbyname`, `socket.gethostbyaddr`, `socket.getnameinfo`, `socket.sendto`, and `socket.sendmsg` events with the same allowlist, then drop "UDP `sendto`" from the list. List C-extension clients (libpq, libcurl, gRPC) and loopback that forwards.

**W5. A test that uses pytest's cache fails on a fresh checkout** (`isolation.py:128-136`; D4 at CONOP `:131`)

- Evidence (`$G/proj4`, no `.pytest_cache`; the test calls `request.config.cache.set("probe/value", 1)`):

  ```
  E   tests.isolation.IsolationError: isolation tripwire: shutil.rmtree
      '.../gate1a/proj4/pytest-cache-files-b995x7lb' is outside the test sandbox
  1 failed
  --- second run (cache dir now exists)
  1 passed
  ```

  The cause is `_pytest/cacheprovider.py:58-86`: `_make_cachedir` creates a temp dir beside the cache and calls `rmtree` on it in a `finally`.
- **Why it matters**: the test fails in CI on a fresh clone and passes locally. That flaky shape is how guards get disabled. D4 allowlisted `.pytest_cache`, and the implementation dropped it with no Status Log entry. Allowlisting `.pytest_cache` alone would not cover this temp dir anyway, because it sits in the rootdir.
- **Fix**: in `pytest_configure`, which runs disarmed, call `config.cache.mkdir("isolation")` when `config` has a `cache` attribute. Record the D4 change in the Status Log.

**W6. `--basetemp` outside the system temp dir errors every `tmp_path` test** (`isolation.py:130`; `ISOLATION.md:40`)

- Evidence: `--basetemp=$G/bt2` with `TMPDIR=tmpA` raises `IsolationError: os.remove '.../bt2/test_writes_tmpcurrent'` (`1 error`). pytest replaces its `current` symlink inside basetemp.
- None of the 14 local repos sets `--basetemp` (grep), so nothing breaks today. But the table's "the system temp dir (which holds `tmp_path`)" stops being true the day one does.
- Fix: add the resolved `config.option.basetemp` to the roots in `pytest_configure` when it is set.

**W7. A connection to `0.0.0.0` trips** (`isolation.py:49-57`)

- Evidence: `HTTPServer(("", 0))` reports `server_address == ("0.0.0.0", port)`, and `urlopen(f"http://0.0.0.0:{port}/")` raised `IsolationError`. `"LOCALHOST"` and `getaddrinfo(socket.gethostname())` trip too.
- **Why it matters**: tests that start a local `http.server` or `socketserver` and connect to its reported address break. That counts toward A2's kill-criterion of 1 broken legitimate test in 100.
- Fix: `ip.is_loopback or ip.is_unspecified`, and lowercase the host before comparing it to `"localhost"`.

**W8. Two load-bearing properties have no test** (`tests/unit/test_isolation.py`)

The mutation run used a scratch copy with one mutant per run, executed as `pytest -q tests/unit/test_isolation.py`:

| Mutant | Result |
|---|---|
| M1: arm only during call (setup and teardown unarmed) | **17 passed** |
| M2: no symlink resolution in `_inside` | **17 passed** |
| M7: never disarm | **17 passed** |
| M4: no tripwire | 8 failed, 9 passed |
| M3: refuse everything | 17 errors |
| M5: no dotenv guard / M6: dotenv blocks all | 2 failed / 2 failed |
| M8: subprocess ignores `cwd` / M9: no subprocess check | 1 failed / 2 failed |
| M10: no `getaddrinfo` check / M11: no log / M12: any explicit dotenv path passes / M13: no Hypothesis root | 1 failed each |

- The known-good controls discriminate. M3 fails everything, and M4 leaves exactly the 9 non-catch tests passing. No test is vacuous.
- The gap is M1. The incident was a fixture, and `ISOLATION.md:44` claims setup and teardown are armed, but no test pins it. Fix: add a `pytester.runpytest_subprocess("-p", "tests.isolation")` test whose fixture teardown deletes a sentinel outside the allowlist, then assert 1 error and that the sentinel survives. C1's three tests kill M2.

**W9. The `SKILLS_FRAMEWORK.md` inventory tree omits `ISOLATION.md`** (`.claude/skills/SKILLS_FRAMEWORK.md:358-371`)

Line 115 now names 13 sidecars, but the tree under `shift-left-testing/` still lists 12. The CONOP's own registration checklist (2c, `:205`) names this tree as a surface. Fix: add `│   ├── ISOLATION.md` after `SCRIPTS.md`, matching line 115's order. PCC check 5 passes as-is (0 MISSING on both passes) because it does not read this file.

### Suggestion

- **S1. A test may delete the system temp dir itself and other processes' files in it** (`isolation.py:46`, `target == root`). Probe: `_inside(tempfile.gettempdir(), _allow)` returns `True`, and a test removed `tmpB/other_process_state`. On this box, `/tmp` holds Claude Code session state. Refuse `target == root` at least.
- **S2. An unwritable log dir turns a catch into `PermissionError`** (`isolation.py:62-66`). Probe: with `.claude` set to mode 555, the catch raised `PermissionError`. The delete was still blocked, but an `except OSError:` around a delete swallows it and no log line is written. Wrap the log write in `try/except OSError` and always raise `IsolationError`.
- **S3. Ship `test_isolation.py` downstream as the registration canary.** With the plugin unregistered (`-p no:tests.isolation`), it reports `9 failed, 8 passed`. Step 1 currently copies only `isolation.py`. Fix C3 first.
- **S4. The `tests/conftest.py:14-15` comment names only deletion.** Add network and dotenv.
- **S5. `test_disarmed_tripwire_lets_deletion_through` sets `_armed` itself** (`:191`). It tests the early return, not its comment's claim that pytest disarms between tests, and mutant M7 survives it. Rename it, or replace it with a pytester check.
- **S6. Session-scope teardown catches are logged against the last test.** In the W3 run, `session_deleter` was logged as `test=tests/test_window.py::test_thread`. Say so in ISOLATION.md, or log the phase.
- **S7. Warn at configure when `config.rootpath` sits inside an allow root.** A repo checked out under `/tmp` allowlists its own `.env` and data.
- **S8. `test_isolation.py:212` asserts `Path.home() / "real.txt"` is outside the roots.** That assertion fails on a runner whose `HOME` is under the temp dir. Build the path from `config.rootpath` instead.
- **S9. The `SKILL.md` frontmatter description (`:3`) never mentions isolation.** Add the terms a lead would search for: test isolation, deletion and network tripwire, `load_dotenv` guard.
- **S10. The CONOP's Wave 1 exit (`:194`) requires GO, and the MOP (`:152`) accepts GO-WITH-FIXES with fixes applied.** Record which one governs in the Status Log.
- **S11 (prose, Minor, rule 1)**: "The fix is structural." (`ISOLATION.md:7`). Rewrite: delete the sentence, so the section opens on "Code that deletes, sweeps, or evicts takes its root as a parameter, and every test points that parameter at `tmp_path`."

### Prose Pass (per `writing-simple-and-direct/REVIEWING.md`)

- **Point**: the opening states the point (a test that left its sandbox makes a green suite meaningless). Only the one section opener in S11 fails rule 1.
- **Structure**: no packed sentences found.
- **Words**: 0 matches for the `LANGUAGE.md:147-149` list across `ISOLATION.md`, `isolation.py`, and `test_isolation.py`. The only hedge, "about 138 GB", is a number.
- **Punctuation**: one em dash, in the H1. Headings are exempt, and all 12 sibling sidecars use the same form.
- **Accuracy**: the prose is clean but wrong in three places: C2 (`:71`, `:85`), W2 (`:69`), and W6 (`:40`).

---

## Numbers in ISOLATION.md, Re-Run

| Claim (`ISOLATION.md`) | Re-run | Result |
|---|---|---|
| 308 existing tests, 0 catches (`:89`) | `.venv/bin/pytest -q`: 325 passed; `--co`: 325; 325 minus 17 is 308; no `isolation-tripwire.log` created | Holds, with `CI` unset |
| Forced matplotlib font-cache rebuild outside the temp dir (`:89`) | `MPLCONFIGDIR=<fresh dir outside> TMPDIR=<narrowed>`: 325 passed, `fontlist-v3.11.0.json` written, 0 catches | Holds |
| 17 tripwire tests pass on 3.11.15 and 3.12.13 (`:89`) | Both: `17 passed` | Holds with `CI` unset; 16 of 17 on both with `CI=1` (C3) |
| Log line format (`:49`) | Probe log lines match `[<iso>] TRIPWIRE event=... target=... test=...` | Holds |
| `isolation_allow` paths resolve relative to `pyproject.toml` (`:53`) | Run from `tests/sub`: the root resolved to `.../proj6/build/test-cache` | Holds |
| Arming covers setup, call, and teardown (`:44`) | W3 run: fixture and session teardown deletes caught | Holds |

## What the Hub's 308-Test Measurement Does Not Cover

| Condition | Measured here | Result |
|---|---|---|
| `CI=1` (Hypothesis `ci` profile) | Yes | 1 failure (C3) |
| Fresh checkout, no `.pytest_cache` | Probe | Tests that use the pytest cache fail (W5) |
| `--basetemp` outside the temp dir | Probe | Every `tmp_path` test errors (W6) |
| Production imports in `conftest.py`; an existing `pytest_plugins` list | Probe plus fleet grep | Guard bypassed, or plugin dropped (C2) |
| Local servers bound to `""` | Probe | Trips (W7) |
| pytest-xdist 3.8.0, `-n 2` | Hub tripwire tests and the 8 probe controls | `17 passed`; the controls hold in workers |
| pytest-cov (`--cov`) with xdist | Probe controls | Hold |
| Notebook kernels (nbclient 0.11.0, schelling-point's venv, which runs notebooks in `test_lessons.py`) | Probe | `1 passed`, 0 catches |
| Python 3.13 and 3.14, macOS, Windows | Not measured | Python 3.14 makes forkserver the Linux default for `multiprocessing`, so pool workers in the template's `parallel.py` run without the hook (covered by `:67`, but worth naming) |
| Population | Not measured | 22 of 27 hub commits since 2026-08-01 touched no code (CONOP `:64`). The hub suite is light on deletion and network code; the pipeline repos are the population A2 needs. |

## What Holds

- An audit hook, not a monkeypatch. The import-bound `rmtree` case is caught, and the hub's test proves it against the incident shape.
- Bytes paths, relative paths after `chdir`, lexical `..` from the temp dir, a symlinked parent, `rmtree(onexc=)`, `rmtree(ignore_errors=True)`, `os.removedirs`, and `rm -- path`: all 8 caught (`test_failopen.py` C1 to C8).
- The `dir_fd` skip in `os.remove` is correct for rmtree's inner calls. CPython reports a default `dir_fd` as `-1`, which falls through to the check.
- The commit is path-scoped. `6039e14` touches 7 files, and `git status --short` lists the same 5 untracked files as before.
- Registration surfaces: `SKILL.md`, the `SKILLS_FRAMEWORK.md` Level 0 block, and the `.claude/README.md` count all say 13 sidecars (`ls` agrees). W9 is the one miss. PCC check 5 reports 0 MISSING on the file pass, the directory pass, and `git diff --name-only main...`.

---

## Part 2: Round-1 Findings Against the Approved CONOP

Round 1: `docs/reviews/20260930_overwatch_review.md`. Line numbers below refer to the approved CONOP.

| Round-1 finding | Status | Where |
|---|---|---|
| C1. Wave 2 exit gate uncalibrated | ADDRESSED | A6 row `:75`; 2d Standard `:206` (held-out set, two arms, non-author scorer, at least 5 of 6, at most 1 of 6 clean, at least 2 more than control) |
| C2. 1a tests would pass the failed guard shape | ADDRESSED | 1a Standard `:188` (sentinel outside, never `/data`, own exception class, import-bound `rmtree`); D4 `:131`; A2 `:71`. The clause "listed beside the test that shows it" was dropped, and W2 to W4 are its cost. |
| W1. Two readings of `ENFORCEMENT.md` | ADDRESSED | Problem `:15` (test-first scope); D3 `:130` (new MAUT; `:83-89` scopes the re-run); Friendly Forces `:25` (PREFLIGHT.md and the fail-closed gate) |
| W2. Approval waits on later data | ADDRESSED | D1 to D10 `:126-137` with conditional branches; Deferred with rationale `:139-142`; `:179` (1a to 1d do not depend on Wave 0) |
| W3. A `.claude/` file assigned to `python-prototyper` | ADDRESSED | `:183` (the lead writes 1a) |
| W4. Swept-commit conditions | ADDRESSED | 0a `:174` (committed by path); one branch per task `:188-192`; verified on `6039e14` (above) |
| W5. No downstream deliverable; widened stub | ADDRESSED in the plan | Terrain `:60`; 1a `:188` (one module, one line, dotenv scoped). The one-line conftest registration is C2 at this gate. |
| W6. Wrong machine and population | ADDRESSED | A1 `:70` (work terminal); A4 `:73` (offline replay, counts only); 0c `:176` |
| W7. Deadline cannot deliver the purpose | ADDRESSED | Mission `:81` (2026-10-16); ask rules prompt rather than log (D3 `:130`) |
| W8. MOEs cannot observe | PARTIAL | MOE 1 `:158` (ledger, same instrument, own baseline) and the tripwire log (`:131`, `:159`) are fixed. The ask rules (1e) name no stream, so MOE 2 counts tripwire catches only. |
| W9. Unmarkable Standards | ADDRESSED | 1b `:189` (grep); 2c `:205` (surface checklist); MOP `:153` (check 5 over `git diff`) |
| W10. Evidence table overstates | ADDRESSED | `:36-44`; Approach A cons `:92`; Wave 3 `:213`; 2b `:204` |
| W11. O6 breaks propagation rules | ADDRESSED | O6 `:142`; 1c `:190` (marked breaking) |
