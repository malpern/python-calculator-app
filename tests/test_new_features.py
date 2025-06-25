import pytest
import json
import math
from app import app


class TestNewFeatures:
    
    def test_after_request_headers(self, client):
        response = client.get('/')
        assert response.headers.get('Access-Control-Allow-Origin') == '*'
        assert 'Content-Type' in response.headers.get('Access-Control-Allow-Headers', '')
        assert 'GET' in response.headers.get('Access-Control-Allow-Methods', '')
        
    def test_no_expression_provided(self, client):
        response = client.post('/calculate',
                             data=json.dumps({}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'No expression provided'
        
    def test_empty_expression_provided(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '   '}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Empty expression'
        
    def test_invalid_characters_in_expression(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '2+3#comment'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Invalid characters in expression'
        
    def test_nan_result(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'sqrt(-1)'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Math domain error'
        
    def test_infinite_result(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '1/0'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Cannot divide by zero'
        
    def test_math_domain_error(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'log(-1)'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Math domain error'
        
    def test_syntax_error(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '2+'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Invalid syntax'
        
    def test_none_json_data(self, client):
        response = client.post('/calculate',
                             data='not json',
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Invalid expression'
        
    def test_valid_expression_with_function(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'sqrt(9)'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '3.0'
        
    def test_expression_with_spaces(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '  2 + 3  '}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '5'