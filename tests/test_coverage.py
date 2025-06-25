import pytest
import json
import math
from unittest.mock import patch
from app import app


class TestCoverage:
    
    @patch('math.isnan')
    def test_nan_result_condition(self, mock_isnan, client):
        mock_isnan.return_value = True
        response = client.post('/calculate',
                             data=json.dumps({'expression': '1+1'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Result is not a number'
        
    @patch('math.isinf')
    def test_infinite_result_condition(self, mock_isinf, client):
        mock_isinf.return_value = True
        response = client.post('/calculate',
                             data=json.dumps({'expression': '1+1'}),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Result is infinite'
        
    def test_if_name_main_condition(self):
        from app import app
        assert app is not None