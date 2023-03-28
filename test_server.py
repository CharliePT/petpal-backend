import pytest
from flask import Flask, session
from server import server, db, User, Conversation, Message, Services
import requests
import json
from unittest.mock import MagicMock, create_autospec, patch



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
    server.secret_key = 'test'
    with server.test_client() as client:
        yield client

def test_login_route_fail(client):
    payload = {'username': 'test1', 'email': 'test@test', 'password': 'jkl'}
    headers = {'content-type': 'application/json'}
    res = client.post('/service-login', json=payload, headers=headers)

    assert res.status_code == 404

def test_service_register(client):
    payload = {'serviceName': 'test2', 'serviceEmail': 'test2@test', 'servicePassword': 'jkl'}
    headers = {'content-type': 'application/json'}
    res = client.post('/service-register', json=payload, headers=headers)

    assert res.status_code == 201

def test_login_route_pass(client):
    payload = {'serviceName': 'test2', 'serviceEmail': 'test2@test', 'servicePassword': 'jkl'}
    headers = {'content-type': 'application/json'}
    res = client.post('/services/service-login', json=payload, headers=headers)

    assert res.status_code == 200

def test_get_services(client):
    res = client.get('/services')
 
    assert res.status_code == 200

def test_get_servicebyid(client):
    with server.app_context():
        server.config['SECRET_KEY'] = 'supersecret'
        mock_db = create_autospec(db)
        with patch('server.db', mock_db):
            service = Services(username = "test_service", email = "test@test", password = "jkl")
            db.session.add(service)
            db.session.commit()

            res = client.get('/services/1')
            assert res.status_code == 200

def test_get_servicebyid2(client):
    res = client.get('/services/1000000000000')

    assert res.status_code == 404

def test_get_providerbyid(client):
    res = client.get('/services/providers/1')

    assert res.status_code == 200

def test_get_serviceprofilebyid(client):
    res = client.get('/services/providers/1')

    assert res.status_code == 200

def test_delete_provider(client):
    res = client.delete('/services/providers/1')

    assert res.status_code == 202

def test_service_login(client):
    payload = {'serviceName': 'test2', 'serviceEmail': 'test2@test', 'servicePassword': 'jkl'}
    headers = {'content-type': 'application/json'}
    client.post('/service-register', json=payload, headers=headers)
    res = client.post('/services/service-login', json=payload, headers=headers)
    assert res.status_code == 200

    payload = {'serviceName': 'test2', 'serviceEmail': 'test2@test', 'servicePassword': 'wrong'}
    res = client.post('/services/service-login', json=payload, headers=headers)
    assert res.status_code == 401

    payload = {'serviceName': 'wrong', 'serviceEmail': 'test2@test', 'servicePassword': 'jkl'}
    res = client.post('/services/service-login', json=payload, headers=headers)
    assert res.status_code == 401


# users tests
## The below test causes tests to run forever and I don't know why
def test_user_signup(client):
    with server.app_context():
        mock_db = create_autospec(db)
        with patch('server.db', mock_db):
            
            payload = {'username': 'test', 'password': 'jkl'}
            res = client.post('/register', data=json.dumps(payload), content_type='application/json')
            assert res.status_code == 200

            # res_data = res.data
            # assert res_data[0] == 'test'

#this block will test all remaining user functions
def test_user(client):
    with server.app_context():
        server.config['SECRET_KEY'] = 'supersecret'
        mock_db = create_autospec(db)
        with patch('server.db', mock_db):

            # create user
            user = User(id = 0, username = 'test', password = 'jkl')
            db.session.add(user)
            db.session.commit()
            
            # check login
            payload = {'userName': 'test', 'password': 'jkl'}
            res = client.post('/login', data=json.dumps(payload), content_type='application/json')
            assert res.status_code == 200

            payload2 = {'username': 'test', 'password': 'fail'}
            res = client.post('/login', data=json.dumps(payload2), content_type='application/json')
            assert res.status_code == 401

            payload = {'username': 'test2', 'password': 'jkl'}
            res = client.post('/login', data=json.dumps(payload), content_type='application/json')
            assert res.status_code == 401

            res = client.get('/users/0')
            assert res.status_code == 200

            res = client.get('/users/99999')
            assert res.status_code == 404

            res = client.get('/users/test')
            assert res.status_code == 200

            res = client.get('/users/fail')
            assert res.status_code == 404

            ##update user
            payload = {'new_username': 'test_update'}
            res = client.put('/users/0', data=json.dumps(payload), content_type='application/json')
            assert res.status_code == 200

            res = client.put('/users/999999999', data=json.dumps(payload), content_type='application/json')
            assert res.status_code == 404

            ##delete user
            res = client.delete('/users/0')
            assert res.status_code == 200

            res = client.delete('/users/999999999')
            assert res.status_code == 404

## Messaging tests ##

def test_messaging(client):
    with server.app_context():
        mock_db = create_autospec(db)
        with patch('server.db', mock_db):
            # enter test data into db
            user = User(id = 1, username = 'test1', password = 'jkl')
            db.session.add(user)
            db.session.commit()
            service = Services(id = 1, username = 'service', email = 'service@test', password = 'jkl')
            db.session.add(service)
            db.session.commit()

            payload = {'user_id': 1, 'service_id': 1}
            res = client.post('/conversations', data=json.dumps(payload), content_type='application/json')
            assert res.status_code == 201

            payload = {'user_id': 999999, 'service_id': 999999}
            res = client.post('/conversations', data=json.dumps(payload), content_type='application/json')
            assert res.status_code == 404        



