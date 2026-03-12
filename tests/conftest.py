"""Shared test fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def sample_data() -> dict:
    """Return sample data for testing."""
    return {
        "name": "test",
        "values": [1, 2, 3, 4, 5],
    }
