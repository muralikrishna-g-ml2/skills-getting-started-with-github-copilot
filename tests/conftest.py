import sys
import os
from copy import deepcopy
import pytest
from fastapi.testclient import TestClient

# ensure tests can import src.app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import app as fastapi_app, activities as activities_dict

ORIGINAL_ACTIVITIES = deepcopy(activities_dict)


@pytest.fixture(scope="session")
def client():
    with TestClient(fastapi_app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: restore baseline before each test
    activities_dict.clear()
    activities_dict.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # Teardown: restore baseline after each test
    activities_dict.clear()
    activities_dict.update(deepcopy(ORIGINAL_ACTIVITIES))
