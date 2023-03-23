import pytest
import server

@pytest.fixture
def api(monkeypatch):
    api = server.server.test_client()
    return api