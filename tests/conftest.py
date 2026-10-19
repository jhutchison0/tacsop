"""Shared test fixtures."""

import os

from hypothesis import settings

# Property-test profiles (see .claude/skills/shift-left-testing/PROPERTY-BASED.md):
# fast search in the inner loop, deeper search in CI. GitHub Actions sets CI=true,
# so the switch needs no workflow configuration.
settings.register_profile("dev", max_examples=50)
settings.register_profile("ci", max_examples=300, deadline=None)
settings.load_profile("ci" if os.getenv("CI") else "dev")

# The isolation tripwire (no deletes outside the sandbox, no network, no real
# .env) registers in pyproject.toml addopts, not here: pytest runs this whole
# file before it reads pytest_plugins. See shift-left-testing/ISOLATION.md.
