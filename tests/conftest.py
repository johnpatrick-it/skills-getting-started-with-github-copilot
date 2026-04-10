"""Pytest configuration and shared fixtures for FastAPI backend tests."""

import copy
import sys
from pathlib import Path

from fastapi.testclient import TestClient
import pytest

# Add src directory to the import path so we can import app.py directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities  # noqa: E402


@pytest.fixture
def client():
    """Provide a TestClient and restore activity state between tests."""
    original_activities = copy.deepcopy(activities)
    client = TestClient(app)
    yield client

    activities.clear()
    activities.update(copy.deepcopy(original_activities))
