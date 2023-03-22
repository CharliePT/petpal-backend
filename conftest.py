import pytest
from .server import server

@pytest.fixture
def api(monkeypatch):
    test_pets = [

    ]