from flask import Flask, render_template, jsonify, request
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        expression = request.json.get('expression', '')
        
        # Security: Only allow certain characters and functions
        allowed_chars = '0123456789+-*/().^ '
        allowed_functions = ['sqrt', 'sin', 'cos', 'tan', 'log', 'exp']
        
        # Replace ^ with ** for Python
        expression = expression.replace('^', '**')
        
        # Check for allowed characters
        for char in expression:
            if char not in allowed_chars and not any(func in expression for func in allowed_functions):
                return jsonify({'error': 'Invalid character'}), 400
        
        # Replace function names with math module functions
        for func in allowed_functions:
            expression = expression.replace(func, f'math.{func}')
        
        # Evaluate the expression
        result = eval(expression, {"__builtins__": None}, {"math": math})
        
        return jsonify({'result': str(result)})
    except ZeroDivisionError:
        return jsonify({'error': 'Cannot divide by zero'}), 400
    except Exception as e:
        return jsonify({'error': 'Invalid expression'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)