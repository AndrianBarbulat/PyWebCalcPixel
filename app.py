from flask import Flask, render_template, request, jsonify
import os
import re

app = Flask(__name__)

# In-memory storage for calculation history
history = []

def validate_expression(expr):
    """Validate expression format to prevent errors and multiple operators"""
    expr = expr.replace(' ', '')
    
    # Check for empty expression
    if not expr:
        return False
    
    # Prevent multiple operators in a row (e.g., 7+++9)
    if re.search(r'[+\-*/]{2,}', expr):
        return False
    
    # Don't allow expressions starting with operators (except negative numbers)
    if expr[0] in '*/+':
        return False
    
    # Don't allow expressions ending with operators
    if expr[-1] in '+-*/':
        return False
    
    # Check for invalid decimal points (e.g., 7..5 or 7.8.9)
    parts = re.split(r'[+\-*/]', expr)
    for part in parts:
        if part and part.count('.') > 1:
            return False
    
    return True

def sanitize_expression(expr):
    """Remove spaces from expression for clean processing"""
    return expr.replace(' ', '')

@app.route('/')
def index():
    """Render the main calculator page with current history"""
    return render_template('index.html', history=history)

@app.route('/calculate', methods=['POST'])
def calculate():
    """Process calculation requests and update history"""
    try:
        data = request.get_json()
        expression = data['expression']
        
        # Clean and validate the expression
        expression = sanitize_expression(expression)
        
        # Security: Only allow basic math characters
        allowed = set('0123456789+-*/.() ')
        if not all(c in allowed for c in expression):
            return jsonify({'error': 'Invalid characters!'})
        
        # Validate expression format
        if not validate_expression(expression):
            return jsonify({'error': 'Invalid expression format!'})
        
        # Safely evaluate the mathematical expression
        result = eval(expression, {"__builtins__": {}}, {})
        
        # Clean up result formatting
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 10)
        
        # Update history (keep last 10 calculations)
        history.append(f"{expression} = {result}")
        if len(history) > 10:
            history.pop(0)
        
        return jsonify({
            'result': result,
            'history': history
        })
        
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero!'})
    except SyntaxError:
        return jsonify({'error': 'Invalid syntax!'})
    except Exception:
        return jsonify({'error': 'Invalid expression!'})

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Clear all calculation history"""
    global history
    history = []
    return jsonify({'history': history})

if __name__ == '__main__':
    # Run the app on the configured port (supports cloud deployment)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)