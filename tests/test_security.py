import pytest
import json
from app import app


class TestSecurity:
    
    def test_invalid_characters_rejected(self, client):
        invalid_expressions = [
            'import os',
            '__import__("os")',
            'eval("2+2")',
            'exec("print(1)")',
            '2+3; print("hack")',
            'open("/etc/passwd")',
            'os.system("ls")',
            '__builtins__',
            'globals()',
            'locals()',
            'dir()',
            'vars()',
            '2+3#comment',
            '2+3;',
            'print(1)',
            'lambda x: x',
            'def func(): pass',
            'class Test: pass'
        ]
        
        for expr in invalid_expressions:
            response = client.post('/calculate',
                                 data=json.dumps({'expression': expr}),
                                 content_type='application/json')
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'error' in data
            
    def test_only_allowed_functions_work(self, client):
        allowed_functions = ['sqrt', 'sin', 'cos', 'tan', 'log', 'exp']
        
        for func in allowed_functions:
            response = client.post('/calculate',
                                 data=json.dumps({'expression': f'{func}(1)'}),
                                 content_type='application/json')
            assert response.status_code == 200
            
    def test_disallowed_functions_rejected(self, client):
        disallowed_functions = [
            'abs', 'pow', 'round', 'min', 'max', 'sum',
            'len', 'str', 'int', 'float', 'bool', 'list'
        ]
        
        for func in disallowed_functions:
            response = client.post('/calculate',
                                 data=json.dumps({'expression': f'{func}(1)'}),
                                 content_type='application/json')
            assert response.status_code == 400
            
    def test_sql_injection_attempts(self, client):
        sql_expressions = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "1; SELECT * FROM users",
            "UNION SELECT password FROM users"
        ]
        
        for expr in sql_expressions:
            response = client.post('/calculate',
                                 data=json.dumps({'expression': expr}),
                                 content_type='application/json')
            assert response.status_code == 400
            
    def test_code_injection_attempts(self, client):
        code_expressions = [
            "2+2; __import__('os').system('rm -rf /')",
            "eval('2+2')",
            "exec('print(1)')",
            "[x for x in ().__class__.__bases__[0].__subclasses__()]",
            "().__class__.__bases__[0].__subclasses__()[104].__init__.__globals__['sys']"
        ]
        
        for expr in code_expressions:
            response = client.post('/calculate',
                                 data=json.dumps({'expression': expr}),
                                 content_type='application/json')
            assert response.status_code == 400