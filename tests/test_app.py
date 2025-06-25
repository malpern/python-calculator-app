import pytest
import json
import math
from app import app


class TestFlaskApp:
    
    def test_index_route(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
        
    def test_calculate_basic_addition(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '2+3'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '5'
        
    def test_calculate_basic_subtraction(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '10-3'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '7'
        
    def test_calculate_basic_multiplication(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '4*5'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '20'
        
    def test_calculate_basic_division(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '15/3'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '5.0'
        
    def test_calculate_power_operation(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '2**3'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '8'
        
    def test_calculate_parentheses(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '(2+3)*4'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '20'
        
    def test_calculate_decimal_numbers(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '2.5+3.7'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert float(data['result']) == 6.2
        
    def test_calculate_sqrt_function(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'sqrt(16)'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '4.0'
        
    def test_calculate_sin_function(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'sin(0)'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert float(data['result']) == 0.0
        
    def test_calculate_cos_function(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'cos(0)'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert float(data['result']) == 1.0
        
    def test_calculate_tan_function(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'tan(0)'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert float(data['result']) == 0.0
        
    def test_calculate_log_function(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'log(1)'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert float(data['result']) == 0.0
        
    def test_calculate_exp_function(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'exp(0)'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert float(data['result']) == 1.0
        
    def test_calculate_complex_expression(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '2*3+sqrt(16)/2'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert float(data['result']) == 8.0
        
    def test_calculate_division_by_zero(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '5/0'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Cannot divide by zero'
        
    def test_calculate_invalid_expression(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '2++3'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '5'
        
    def test_calculate_empty_expression(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': ''}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Empty expression'
        
    def test_calculate_no_expression_key(self, client):
        response = client.post('/calculate',
                             data=json.dumps({}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'No expression provided'
        
    def test_calculate_invalid_content_type(self, client):
        response = client.post('/calculate',
                             data='expression=2+3',
                             content_type='application/x-www-form-urlencoded')
        assert response.status_code == 400
        
    def test_calculate_malformed_json(self, client):
        response = client.post('/calculate',
                             data='{"expression": 2+3}',
                             content_type='application/json')
        assert response.status_code == 400
        
    def test_calculate_negative_numbers(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '-5+3'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '-2'
        
    def test_calculate_spaces_in_expression(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '2 + 3 * 4'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '14'
        
    def test_calculate_nested_parentheses(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '((2+3)*4)/2'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert float(data['result']) == 10.0
        
    def test_calculate_multiple_functions(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'sqrt(sin(0)**2+cos(0)**2)'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert float(data['result']) == 1.0