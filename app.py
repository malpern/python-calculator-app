from flask import Flask, render_template, jsonify, request
import math
import re

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        if not data or 'expression' not in data:
            return jsonify({'error': 'No expression provided'}), 400
            
        expression = data['expression'].strip()
        if not expression:
            return jsonify({'error': 'Empty expression'}), 400
        
        # Security: Only allow safe mathematical expressions
        # Allow numbers, operators, parentheses, decimal points, and specific functions
        allowed_pattern = r'^[0-9+\-*/.() ]+$'
        allowed_functions = ['sqrt', 'sin', 'cos', 'tan', 'log', 'exp']
        
        # Check if expression contains functions
        temp_expression = expression
        for func in allowed_functions:
            temp_expression = temp_expression.replace(func, '')
        
        # Replace ^ with ** for Python
        expression = expression.replace('^', '**')
        
        # Validate the cleaned expression
        if not re.match(allowed_pattern, temp_expression):
            return jsonify({'error': 'Invalid characters in expression'}), 400
        
        # Replace function names with math module functions
        for func in allowed_functions:
            expression = expression.replace(func, f'math.{func}')
        
        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": None}, {"math": math})
        
        # Handle special cases
        if math.isnan(result):
            return jsonify({'error': 'Result is not a number'}), 400
        if math.isinf(result):
            return jsonify({'error': 'Result is infinite'}), 400
            
        return jsonify({'result': str(result)})
        
    except ZeroDivisionError:
        return jsonify({'error': 'Cannot divide by zero'}), 400
    except ValueError as e:
        return jsonify({'error': 'Math domain error'}), 400
    except SyntaxError:
        return jsonify({'error': 'Invalid syntax'}), 400
    except Exception as e:
        return jsonify({'error': 'Invalid expression'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)