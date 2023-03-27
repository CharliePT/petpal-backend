import pytest
from server import server
import requests
import json


class TestAPI():
    def test_welcome(self, api):
        res = api.get('/')
        assert res.status == '200 OK'
        assert res.json['Welcome'] == 'Welcome to the petpal API'
    
    # def test_pets(self, api):
    #     res = api.get('/pets')
    #     assert res.status == '200 OK'
    
    def test_dogs(self, api):
        res = api.get('/pets/dogs')
        assert res.status == '200 OK'

    def test_cats(self, api):
        res = api.get('/pets/cats')
        assert res.status == '200 OK'

    def test_notfound(self, api):
        res = api.get('/pets/dogs/test')
        assert res.status == '404 NOT FOUND'

    def test_services(self, api):
        res = api.get('/services')
        assert res.status == '200 OK'
    
    
## tests outside of class

@pytest.fixture
def client():
    server.config['TESTING'] = True
    with server.test_client() as client:
        yield client

def test_login_route_fail(client):
    payload = {'username': 'test1', 'email': 'test@test', 'password': 'jkl'}
    headers = {'content-type': 'application/json'}
    res = client.post('/service-login', json=payload, headers=headers)

    assert res.status_code == 404

def test_service_register(client):
    payload = {'username': 'test2', 'email': 'test2@test', 'password': 'jkl'}
    headers = {'content-type': 'application/json'}
    res = client.post('/service-register', json=payload, headers=headers)

    assert res.status_code == 201

def test_login_route_pass(client):
    payload = {'username': 'test2', 'email': 'test2@test', 'password': 'jkl'}
    headers = {'content-type': 'application/json'}
    res = client.post('/services/service-login', json=payload, headers=headers)

    assert res.status_code == 200

def test_get_services(client):
    res = client.get('/services')
 
    assert res.status_code == 200

def test_get_servicebyid(client):
    res = client.get('/services/1')

    assert res.status_code == 200

def test_get_servicebyid2(client):
    res = client.get('/services/1000000000000')

    assert res.status_code == 404

def test_get_servicebyid(client):
    res = client.get('/services/providers/1')

    assert res.status_code == 200

def test_get_serviceprofilebyid(client):
    res = client.get('/services/providers/1')

    assert res.status_code == 200

def test_delete_provider(client):
    res = client.delete('/services/providers/1')

    assert res.status_code == 202

def test_service_login(client):
    payload = {'username': 'test2', 'email': 'test2@test', 'password': 'jkl'}
    headers = {'content-type': 'application/json'}
    client.post('/service-register', json=payload, headers=headers)
    res = client.post('/services/service-login', json=payload, headers=headers)
    assert res.status_code == 200

    payload = {'username': 'test2', 'email': 'test2@test', 'password': 'wrong'}
    res = client.post('/services/service-login', json=payload, headers=headers)
    assert res.status_code == 401

    payload = {'username': 'wrong', 'email': 'test2@test', 'password': 'jkl'}
    res = client.post('/services/service-login', json=payload, headers=headers)
    assert res.status_code == 404

## Messaging tests ##

### The below test causes tests to run forever and I don't know why
def test_user_signup(client):
    payload = {'username': 'test', 'password': 'jkl'}
    headers = {'content-type': 'application/json'}
    res = client.post('/register', json=payload, headers=headers)

    assert res.status_code == 201

# users tests















