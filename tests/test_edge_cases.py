import pytest
import json
import math
from app import app


class TestEdgeCases:
    
    def test_very_large_numbers(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '999999999*999999999'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == str(999999999 * 999999999)
        
    def test_very_small_decimal(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '0.000001+0.000002'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert float(data['result']) == 0.000003
        
    def test_scientific_notation_result(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '2**100'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        result = float(data['result'])
        assert result > 1e30
        
    def test_sqrt_of_negative_number(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'sqrt(-1)'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_log_of_zero(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'log(0)'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_log_of_negative_number(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'log(-1)'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_division_by_very_small_number(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '1/0.0000000001'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        result = float(data['result'])
        assert result == 10000000000.0
        
    def test_overflow_expression(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'exp(1000)'}),
                             content_type='application/json')
        assert response.status_code == 200 or response.status_code == 400
        
    def test_underflow_expression(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'exp(-1000)'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        result = float(data['result'])
        assert result == 0.0
        
    def test_multiple_decimal_points(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '1.2.3+4'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_unmatched_parentheses_left(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '((2+3)*4'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_unmatched_parentheses_right(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '(2+3)*4)'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_empty_parentheses(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '2+()'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_function_without_parentheses(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'sqrt'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_function_empty_arguments(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': 'sqrt()'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_consecutive_operators(self, client):
        valid_test_cases = ['2**3']
        
        for expr in valid_test_cases:
            response = client.post('/calculate',
                                 data=json.dumps({'expression': expr}),
                                 content_type='application/json')
            assert response.status_code == 200
                
    def test_trailing_operators(self, client):
        trailing_operators = ['2+', '2-', '2*', '2/', '2^']
        
        for expr in trailing_operators:
            response = client.post('/calculate',
                                 data=json.dumps({'expression': expr}),
                                 content_type='application/json')
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'error' in data
            
    def test_leading_operators(self, client):
        valid_leading = ['+2', '-2']
        invalid_leading = ['*2', '/2', '^2']
        
        for expr in valid_leading:
            response = client.post('/calculate',
                                 data=json.dumps({'expression': expr}),
                                 content_type='application/json')
            assert response.status_code == 200
            
        for expr in invalid_leading:
            response = client.post('/calculate',
                                 data=json.dumps({'expression': expr}),
                                 content_type='application/json')
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'error' in data
            
    def test_single_number(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '42'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '42'
        
    def test_single_decimal(self, client):
        response = client.post('/calculate',
                             data=json.dumps({'expression': '3.14159'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == '3.14159'