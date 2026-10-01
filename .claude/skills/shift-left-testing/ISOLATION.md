# ISOLATION — Tests Never Touch the Real World

Sidecar to `SKILL.md`. A test that deletes real files, opens a network connection, or loads the repo's real `.env` has left its sandbox, and a green suite says nothing about what it did on the way. The failure this file exists for: an under-scoped guard fixture let a test suite delete about 138 GB of real cached data, in a session that was building cache-eviction code. The guard existed. It covered the wrong paths.

## The Design: Pass the Root In

The fix is structural. Code that deletes, sweeps, or evicts takes its root as a parameter, and every test points that parameter at `tmp_path`:

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

`tests/isolation.py` is a pytest plugin that raises `IsolationError` when a running test reaches outside its sandbox. One line in `tests/conftest.py` registers it:

```python
pytest_plugins = ["tests.isolation"]
```

| Tripwire | Fires on | Allowed |
|---|---|---|
| Deletion | `os.remove`, `os.unlink`, `Path.unlink`, `os.rmdir`, `Path.rmdir`, `shutil.rmtree`; a subprocess whose program is `rm`, `rmdir`, `unlink`, or `shred` | the system temp dir (which holds `tmp_path`), Hypothesis's example database, and `isolation_allow` entries |
| Network | `socket.connect`, `socket.getaddrinfo` | loopback, `localhost`, Unix sockets |
| dotenv | `load_dotenv()` with no path, or with a path outside the allowlist: loads nothing, returns `False` | a stream, or a path inside the allowlist |

The first two are one Python audit hook (`sys.addaudithook`), armed only while a test runs. Arming covers setup, call, and teardown, so an autouse fixture is inside it. An audit hook sees `shutil.rmtree` even when the code under test ran `from shutil import rmtree` before any patch existed. A monkeypatched guard does not, and that hole is the incident's shape. The dotenv guard is applied when pytest imports the plugin, before test modules import the code they test.

Each catch appends one line to `.claude/audits/isolation-tripwire.log`:

```
[2026-09-30T22:08:34-05:00] TRIPWIRE event=shutil.rmtree target=/data/cache test=tests/unit/test_evict.py::test_sweep
```

### Extending the Allowlist

A repo whose tests legitimately delete somewhere else, such as a build cache inside the repo, adds the directory in `pyproject.toml`. Paths resolve relative to that file:

```toml
[tool.pytest.ini_options]
isolation_allow = ["build/test-cache"]
```

Never allowlist a production data root. A test that needs one is testing code that needs a root parameter.

## What the Tripwire Cannot See

- **Overwrites.** `open(path, "w")` and a rename onto an existing file (`os.replace`, `shutil.move`) destroy data with no deletion event.
- **Shell strings.** `subprocess.run("rm -rf x", shell=True)` and `["sh", "-c", "rm ..."]` show the tripwire only the shell.
- **Child processes.** A program the test launches deletes in its own process, which has no audit hook.
- **C extensions** that call `unlink(2)` directly.
- **Deletion relative to a directory descriptor** (`os.remove(name, dir_fd=fd)`) outside `shutil.rmtree`, which is checked at its top directory instead.
- **UDP `sendto`** without `connect`.
- **Code that runs before the plugin loads.** A `conftest.py` that imports production code above its `pytest_plugins` line binds the real `load_dotenv`. `dotenv_values()` is not guarded.
- **Commands typed into a shell.** Those belong to the permission layer, not to pytest.

That list is why the root parameter is the design and the tripwire is the backstop.

## Testing the Tripwire

The hub's tests are `tests/unit/test_isolation.py`. Each one narrows the allowlist to a directory inside `tmp_path`, targets a sentinel outside it, asserts `IsolationError` rather than any exception, and asserts the sentinel still exists. Known-good controls prove that deletion inside the allowlist and connections to loopback still work, so a tripwire that refused everything would fail.

Do not write `with pytest.raises(OSError): shutil.rmtree("/data/x")`. On a box with no `/data`, that test passes with no tripwire installed. On a box with `/data`, a regressed tripwire makes the test delete real data.

## Adopting Downstream

1. Copy `tests/isolation.py`. It needs `tests` importable as a package (`tests/__init__.py`; the hub also sets `pythonpath = ["."]`).
2. Add `pytest_plugins = ["tests.isolation"]` to `tests/conftest.py`, above any import of production code.
3. Run the suite, then read `.claude/audits/isolation-tripwire.log`. Each line is a test reaching the real world (fix the test: pass the root in) or a directory that belongs in `isolation_allow`.
4. Check that `.claude/audits/` is gitignored. The shift-left audit hook already needs it.

Measured at the hub on adoption, 2026-09-30: 308 existing tests ran armed with 0 catches, including a forced matplotlib font-cache rebuild outside the temp dir. The 17 tripwire tests pass on Python 3.11.15 and 3.12.13.

## See Also

- [`FIXTURES.md`](FIXTURES.md): `tmp_path` factories and shared fixtures.
- [`MOCKS.md`](MOCKS.md): stub network clients at the boundary. The tripwire catches the ones you missed.
- [`SCRIPTS.md`](SCRIPTS.md): the subprocess tier and dry-run contracts.
- [`ENFORCEMENT.md`](ENFORCEMENT.md): the hook layers that run outside pytest.
