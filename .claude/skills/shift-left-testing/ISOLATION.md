# ISOLATION — Tests Never Touch the Real World

Sidecar to `SKILL.md`. A test that deletes real files, opens a network connection, or loads the repo's real `.env` has left its sandbox, and a green suite says nothing about what it did on the way. The failure this file exists for: an under-scoped guard fixture let a test suite delete about 138 GB of real cached data, in a session that was building cache-eviction code. The guard existed. It covered the wrong paths.

## The Design: Pass the Root In

Code that deletes, sweeps, or evicts takes its root as a parameter, and every test points that parameter at `tmp_path`:

```python
# BAD: the root is a module constant; a test reaches it only by monkeypatching
CACHE_ROOT = Path("/data/cache")

def evict_older_than(days: int) -> None:
    ...  # walks CACHE_ROOT

# GOOD: the root is an argument; config supplies it in production
def evict_older_than(root: Path, days: int) -> None:
    ...

def test_evict_removes_stale_files(tmp_path):
    stale = tmp_path / "old.bin"
    stale.write_bytes(b"x")
    ...
    evict_older_than(tmp_path, days=7)
    assert not stale.exists()
```

A config-driven repo reads the root from YAML in production and passes it in. Tests never load that value. Fixture patterns live in `FIXTURES.md`.

## The Backstop: The Tripwire Plugin

`tests/isolation.py` is a pytest plugin that raises `IsolationError` when a running test reaches outside its sandbox. Register it in `pyproject.toml`, not in `conftest.py`:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
addopts = ["-p", "tests.isolation"]
```

pytest runs a whole `conftest.py` before it reads that file's `pytest_plugins`. A production import anywhere in the conftest therefore runs before the plugin exists, and binds the real `load_dotenv`. A later `pytest_plugins = [...]` in the same file replaces the line and drops the tripwire with no error. A `-p` option in `addopts` loads before any conftest.

| Tripwire | Fires on | Allowed |
|---|---|---|
| Deletion | `os.remove`, `os.unlink`, `Path.unlink`, `os.rmdir`, `Path.rmdir`, `shutil.rmtree`; a launch (`subprocess`, `os.posix_spawn`, `os.spawn*`, `os.exec*`) whose program or `argv[0]` is `rm`, `rmdir`, `unlink`, or `shred` | the system temp dir (which holds `tmp_path`), `--basetemp` when set, Hypothesis's example directory, and `isolation_allow` entries |
| Network | `socket.connect`, `sendto`, `sendmsg`; the lookups `getaddrinfo`, `gethostbyname`, `gethostbyaddr`, `getnameinfo` | loopback, `0.0.0.0` and `::`, `localhost` in any case, this machine's own hostname, Unix sockets |
| dotenv | `load_dotenv()` with no path, or with a path outside the allowlist: loads nothing, returns `False` | a path inside the allowlist, or a stream with no path |

The first two are one Python audit hook (`sys.addaudithook`), armed only while a test runs. Arming covers setup, call, and teardown, so a fixture is inside it at both ends. An audit hook sees `shutil.rmtree` even when the code under test ran `from shutil import rmtree` before any patch existed. A monkeypatched guard does not, and that hole is the incident's shape. Paths resolve the way the kernel resolves them: symlinks before `..`, and the last component followed when a trailing slash makes the kernel follow it. A name relative to a directory descriptor (`dir_fd`) resolves through `/proc/self/fd` on Linux; where there is no `/proc`, an `rmtree` of such a name is refused and an `os.remove` or `os.rmdir` of one goes unchecked.

Each catch appends one line to `.claude/audits/isolation-tripwire.log`. A catch raises `IsolationError` even when that log cannot be written:

```
[2026-09-30T22:08:34-05:00] TRIPWIRE event=shutil.rmtree target=/data/cache test=tests/unit/test_evict.py::test_sweep
```

A session-scoped fixture's teardown is caught, but its line names the last test that ran.

### Extending the Allowlist

A repo whose tests legitimately delete somewhere else, such as a build cache inside the repo, adds the directory in `pyproject.toml`. Paths resolve relative to that file:

```toml
[tool.pytest.ini_options]
isolation_allow = ["build/test-cache"]
```

Never allowlist a production data root. A test that needs one is testing code that needs a root parameter.

## What the Tripwire Cannot See

- **Overwrites and moves.** `open(path, "w")` and a rename onto an existing file destroy data with no deletion event. A rename out of a real directory into the sandbox, followed by a delete there, passes both checks.
- **Shell strings and wrappers.** `shell=True`, `["sh", "-c", ...]`, and `os.system` show the tripwire only the shell. It reads the program and `argv[0]`, so `env rm`, `sudo rm`, `xargs rm`, `find -delete`, `git clean`, and `rsync --delete` pass.
- **Child processes.** A program the test launches deletes and connects in its own process, which has no audit hook. Python 3.14 makes forkserver the Linux default for `multiprocessing`, so pool workers fall in this class.
- **C extensions** that call `unlink(2)` or open sockets themselves. `psycopg` connecting to a host given as an IP raises no event; libcurl and gRPC clients are the same.
- **Descriptor-relative deletes off Linux.** Without `/proc`, `os.remove(name, dir_fd=fd)` and `os.rmdir(name, dir_fd=fd)` are not checked.
- **A lookup of this machine's own hostname** counts as local, because `socket.getfqdn()`, `HTTPServer(("", port))`, and `email.utils.make_msgid()` all make one. If the name is not in the hosts file, that query leaves the box.
- **A hostname passed to `connect`.** CPython resolves it in C before the `socket.connect` event, so the DNS query leaves. The connection itself is still refused.
- **Loopback that forwards.** An SSH tunnel, a local proxy, a published Docker port, and `/var/run/docker.sock` are all local addresses that reach past the box.
- **Code outside a test.** Collection (module-level code in a test file), `pytest_configure`, `pytest_sessionstart`, `pytest_sessionfinish`, `atexit` handlers, and threads that outlive their test all run disarmed. Collection stays disarmed on purpose: it imports libraries that build caches at import time (matplotlib's font cache is one), and arming it would trade a rare miss for routine false catches.
- **The temp dir itself.** A test may delete the temp dir root and other processes' files in it. A repo checked out under the temp dir allowlists its own `.env` and data.
- **`dotenv_values()`**, which reads a `.env` without setting variables, and any plugin that loads before this one and imports production code.
- **Commands typed into a shell.** Those belong to the permission layer, not to pytest.

That list is why the root parameter is the design and the tripwire is the backstop.

### False Catches

A library that deletes its own lock or temp file outside the sandbox on first use trips the wire. matplotlib does this when a test imports it inside the test body on a fresh font cache: every CI runner, and the first run after a matplotlib release that changes the cache version (patch releases reuse it). The catch blocks the lock's removal, so `fontlist-*.json.matplotlib-lock` stays in the real cache directory. Every later matplotlib import on that machine then waits about 5 seconds, warns `Could not save font_manager cache`, and rebuilds without saving, until someone deletes the lock file. Import such libraries at module level, where collection runs them disarmed; or set `MPLCONFIGDIR` to a temp dir for the test run; or add the library's cache directory to `isolation_allow`.

## Testing the Tripwire

The hub's tests are `tests/unit/test_isolation.py`. Each catch test narrows the allowlist to a directory inside `tmp_path`, targets a sentinel outside it, asserts `IsolationError` rather than any exception, and asserts the sentinel still exists. Known-good controls prove that deletion inside the allowlist, deleting a symlink, connections to loopback and to `0.0.0.0`, lookups of this machine's own name, and a dotenv stream all still work, so a tripwire that refused everything would fail. Four tests run a fresh project in its own pytest process: fixture setup and teardown are armed, registration survives a conftest that imports production code, a fresh checkout's `.pytest_cache` builds, and `--basetemp` outside the temp dir works.

Do not write `with pytest.raises(OSError): shutil.rmtree("/data/x")`. On a box with no `/data`, that test passes with no tripwire installed. On a box with `/data`, a regressed tripwire makes the test delete real data.

## Adopting Downstream

1. Copy `tests/isolation.py` and `tests/unit/test_isolation.py`. The plugin needs `tests` importable as a package (`tests/__init__.py`). The test file is the registration canary: with the plugin unregistered, its catch tests fail.
2. Add `"-p", "tests.isolation"` to `addopts` in `[tool.pytest.ini_options]`, beside `pythonpath = ["."]`. Add `"-p", "pytester"` too; the canary's fresh-project tests need it. Remove any `pytest_plugins` line for it from `conftest.py`.
3. Run the suite with and without `CI=true`, then read `.claude/audits/isolation-tripwire.log`. Each line is a test reaching the real world (fix the test: pass the root in) or a directory that belongs in `isolation_allow`.
4. Check that `.claude/audits/` is gitignored. The shift-left audit hook already needs it.

Measured at the hub, 2026-09-30, after three merge-gate rounds: 308 existing tests ran armed with 0 catches, with and without `CI=true`, including a forced matplotlib font-cache rebuild outside the temp dir. That rebuild ran at collection, disarmed, because the hub's tests import matplotlib at module level. The 43 tripwire tests pass on Python 3.11.15 and 3.12.13.

## See Also

- [`FIXTURES.md`](FIXTURES.md): `tmp_path` factories and shared fixtures.
- [`MOCKS.md`](MOCKS.md): stub network clients at the boundary. The tripwire catches the ones you missed.
- [`SCRIPTS.md`](SCRIPTS.md): the subprocess tier and dry-run contracts.
- [`ENFORCEMENT.md`](ENFORCEMENT.md): the hook layers that run outside pytest.
