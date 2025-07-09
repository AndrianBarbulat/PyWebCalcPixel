from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data['expression']
        
        allowed = set('0123456789+-*/.()')
        if not all(c in allowed for c in expression):
            return jsonify({'error': 'Invalid characters!'})
        
        result = eval(expression)
        return jsonify({'result': result})
    except:
        return jsonify({'error': 'Invalid expression!'})

if __name__ == '__main__':
    app.run(debug=True)