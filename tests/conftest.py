import copy

import pytest

from src import app as app_module

# Keep a deep copy of the initial in-memory state so each test starts with a clean slate.
ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities data before each test."""
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    yield
