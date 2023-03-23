import pytest
import server

@pytest.fixture
def api(monkeypatch):
    test_sp = [
        {'id': 1, 'username': 'test1', 'password': 'password'},
        {'id': 2, 'username': 'test2', 'password': 'password'}
    ]
    monkeypatch.setattr()
    api = server.server.test_client()
    return api