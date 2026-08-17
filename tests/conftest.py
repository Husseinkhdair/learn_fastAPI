import os
import pytest

@pytest.fixture(autouse=True, scope="session")
def setup_test_environment():
    # Use fake repository during general test suite execution to avoid modifying MongoDB Atlas
    os.environ["USE_FAKE_REPO"] = "true"
