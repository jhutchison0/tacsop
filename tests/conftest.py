"""Shared test fixtures."""

import os

from hypothesis import settings

# Property-test profiles (see .claude/skills/shift-left-testing/PROPERTY-BASED.md):
# fast search in the inner loop, deeper search in CI. GitHub Actions sets CI=true,
# so the switch needs no workflow configuration.
settings.register_profile("dev", max_examples=50)
settings.register_profile("ci", max_examples=300, deadline=None)
settings.load_profile("ci" if os.getenv("CI") else "dev")
