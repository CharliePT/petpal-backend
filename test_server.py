import pytest
import server
import requests
import json


class TestAPI():
    def test_welcome(self, api):
        res = api.get('/')
        assert res.status == '200 OK'
        assert res.json['Welcome'] == 'Welcome to the petpal API'
    
    def test_pets(self, api):
        res = api.get('/pets')
        assert res.status == '200 OK'
    
    def test_dogs(self, api):
        res = api.get('/pets/dogs')
        assert res.status == '200 OK'

    def test_cats(self, api):
        res = api.get('/pets/cats')
        assert res.status == '200 OK'

    def test_notfound(self, api):
        res = api.get('/pets/dogs/test')
        assert res.status == '404 NOT FOUND'
    
    ## not currently working: key error sp_id
    def test_create_service(self, api):
        mock_data = json.dumps({'name': 'test1'})
        mock_headers = {'Content-Type': 'application/json'}
        res = api.post('/service-profile', data=mock_data, headers=mock_headers)
        assert res.json['name'] == 'test1'    


