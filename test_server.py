import pytest
import server
import requests

@pytest.fixture
def test_res():
    res = requests.get('https://petpal.onrender.com')
    assert 
